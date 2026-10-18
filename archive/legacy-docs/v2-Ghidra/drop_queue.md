# Native drop queue — ACNL JPN v1.5

This note consolidates the existing IDA-side drop analysis with a fresh JPN v1.5 instruction-level audit. It intentionally precedes any further balloon-drop queue implementation.

## Address correction

`0x955FF4` is not the native drop queue base.

IDA/local XML:
- `0x955FF4`: `ItemToPlace`, type `ItemID`, 4 bytes
- it is the empty/sentinel Item value used by drop/inventory code

The native four-slot drop queue is:
- `g_DropDataTable @ 0x9AE15C`
- entry size `0x12`
- entry count `4`

The related tables are distinct:
- `g_FieldActionActive @ 0x9AE1A4`: 5 bytes × 32 tile/action locks; free marker playerNo=0xA5
- `g_DigRecordArray @ 0x9AE244`: 0x16 bytes × 32 operation records

Do not treat these three structures as one queue.

## DropData layout

IDA comment at `0x9AE15C`, confirmed against `Item_PlaceItem @ 0x59E5B4`:

| offset | size | field |
|---|---:|---|
| +0x00 | 4 | ItemToReplace |
| +0x04 | 4 | ItemToPlace |
| +0x08 | 4 | ItemToShow |
| +0x0C | 1 | wX |
| +0x0D | 1 | wY |
| +0x0E | 1 | DropType |
| +0x0F | 1 | State |
| +0x10 | 1 | SlotIndex |
| +0x11 | 1 | Flags |

Flags:
- bit0 IsInside
- bit1 PlayerSide
- bit2-4 FruitTree
- bit5 CrashTree
- bit6-7 HitCount

## Queue allocation — Item_PlaceItem

`Item_PlaceItem @ 0x59E5B4` is the native producer.

At `0x59E5C0-0x59E5F0`:
- scan slot 0..3
- test `entry+0x0F State`
- first `State==0` is selected
- if all four are occupied, return `-1`

At `0x59E604-0x59E690`:
- copy ItemToReplace / ItemToPlace / ItemToShow
- store X/Y
- store `State=1`
- store DropType
- build Flags

DropType `0x10` is exceptional and is immediately changed to `State=2`; all normal types proceed into the field-action record path.

The IDA comment on `vc_DROPM @ 0x59E5DC` is especially useful: the old rapid-drop cheat changes the free-slot branch into an unconditional branch, effectively forcing slot 0 and overwriting an in-flight record. This confirms that the stock queue is explicitly intended to prevent record destruction during overlapping drops.

## Slot identity propagation

`FieldAction_QueueToRecord @ 0x59EBE8` converts a DropData slot into the 0x16-byte field-action packet/record.

Important point:
- `DropData+0x10 SlotIndex` is copied into the low two bits of record `processFlags` at `record+0x0D`
- later completion packets therefore carry the original queue-slot identity

The record also carries:
- DropType in `record+0x0C` high bits, with player ownership in low bits
- Flags in `record+0x0E`
- player id in `record+0x12`
- X/Y in `record+0x13/+0x14`
- the three Item values at +0/+4/+8

## State transition — FieldAction_Dispatch

`FieldAction_Dispatch @ 0x59E8F8` dispatches by `processFlags(record+0x0D).bits2-5`, not by DropType.

Relevant completion cases:
- case 1: `g_DropDataTable[record.processFlags & 3].State = 2`
- case 2: `...State = 3`

Therefore native DropData states are:

- `0` = free
- `1` = request in flight
- `2` = completed successfully
- `3` = completed with error/failure

Case 0 is the initial apply path:
- `FieldAction_CanApply`
- active-tile lookup
- `FieldAction_RegisterActive`
- type-specific work
- then `FieldAction_SendOrDispatch`

The active-tile lock at `0x9AE1A4` is separate from the four DropData completion slots.

## Consumer/free — 0x596C84

`0x596C84` is the DropData handle poll/finalize function used by inventory UI.

Entry address calculation:
`entry = 0x9AE15C + handle * 0x12`

It reads:
- `entry+0x0F State`
- `entry+0x0E DropType`

Behavior relevant to ordinary inventory drop type `0x0A`:
- State 0: return 0
- State 1: return 1, leave slot occupied
- State 2: perform type-specific success finalization, then clear the queue entry and return 2
- State 3: clear the queue entry and return 3

The normal clear path at `0x596ED4-0x596EE0`:
- writes the handle back to `entry+0x10 SlotIndex`
- sets `DropType=0`
- sets `State=0`

Thus a normal slot is not reusable merely because the visual animation reached the ground. It becomes free when the completion state is consumed by the native poll/finalize path.

Some special DropTypes intentionally bypass the generic clear branch and have separate lifecycle rules; ordinary inventory drop 0x0A is not one of them.

## Inventory UI contract

`FUN_0019AD30`:
- calls `Player_DropItem @ 0x596084`
- stores return handle at `BsMenuItem+0xD8`
- only `-1` is immediate failure
- otherwise transitions into the drop-wait state

`FUN_0019AF8C`:
- loads `BsMenuItem+0xD8`
- calls `0x596C84(handle)`
- state/result 0 or 1: keep waiting
- result 2: success; remove the source inventory Item, refresh icon/UI, advance menu state
- result 3: error path

Therefore the native queue is also the inventory completion token. The queue lifetime and lower-screen UI wait lifetime are the same mechanism.

## Why the current balloon implementation can be re-entered

Hardware-verified Ghidra-gpt-sol-5.6-F032 deliberately bypasses `Item_PlaceItem` and returns synthetic handle 4. Its `0x596C84` hook returns status 2 immediately for handle 4.

Consequences:
1. no `g_DropDataTable` slot is allocated
2. no native State=1 exists while the balloon is flying
3. BsMenuItem immediately observes success and leaves its wait state
4. another inventory drop can be initiated while the first balloon/falling object is still alive
5. the custom shared Item/X/Y state can then be overwritten

The Ghidra-gpt-sol-5.6-F033 shared+0x68 busy guard treats this symptom externally, but it duplicates a lifecycle that the game already owns. Ghidra-gpt-sol-5.6-F033 is therefore retired as the integration direction.

## Correct integration direction

Do not add a second independent busy flag.

The next balloon implementation should use a real `g_DropDataTable` slot and return its native slot index to BsMenuItem.

Required lifecycle:
1. allocate a normal DropData slot with the same contract as `Item_PlaceItem`
2. keep that slot at `State=1` while the custom balloon/falling object is in flight
3. preserve Ghidra-gpt-sol-5.6-F032's hardware-verified 0x21 visual and field commit
4. after successful impact/field commit, set that same slot to `State=2`
5. let stock `0x596C84` consume State=2, clear the slot to 0, remove the source inventory Item, and release the UI
6. on custom failure, set `State=3` and let the same stock error/finalize path handle it

Once this is done:
- synthetic handle 4 should no longer be necessary
- the custom `0x596C84` special case should be removable
- no custom queue busy flag should be necessary
- the native menu wait state itself prevents a second local inventory drop from starting before completion

## Existing IDA sources used

- IDA names/comments in `acnl_jpn_v15.xml`
- `reference/old_project/REFERENCES/TEXTS/drop_method.txt`
- IDA branch FOXXY/Vapecord references, especially the `DROPM` patch comment
- instruction-level JPN v1.5 verification of:
  - `0x59E5B4`
  - `0x59EBE8`
  - `0x59E8F8`
  - `0x596C84`
  - `0x19AD30 / 0x19AF8C`

No new queue implementation is introduced by this analysis.

## Ghidra-gpt-sol-5.6-F034: native DropData queue integration

Ghidra-gpt-sol-5.6-F032 remains the hardware-verified visual/persistence baseline. Ghidra-gpt-sol-5.6-F033's independent busy flag is retired.

### Key integration point

Stock `Item_PlaceItem @ 0x59E5B4` is now allowed to run normally through native DropData allocation and initialization.

At `0x59E6A4`, immediately after:
- first free `g_DropDataTable @ 0x9AE15C` slot is selected,
- three Item values are copied,
- X/Y/DropType/Flags are stored,
- `State=1` is written,

but before the normal FieldAction record is constructed, Ghidra-gpt-sol-5.6-F034 intercepts only the inventory caller.

The discriminator is the saved LR in the Item_PlaceItem frame:
- prologue pushes r0-r3,r4-r11,lr and subtracts 0x1C,
- saved LR is therefore `[sp+0x4C]`,
- inventory Player_DropItem callsite `0x596188` returns to `0x59618C`.

Only when:
- saved LR == 0x59618C, and
- DropData.DropType == 0x0A,

does the custom balloon path run. Otherwise execution resumes stock at `0x59E6A8`.

Queue-full handling remains entirely stock: if all four DropData entries are nonzero, Item_PlaceItem returns -1 before the custom intercept is reached.

### Native handle

The selected DropData pointer is saved at custom shared+0x6C.

No synthetic handle is returned.

On custom success the cave branches directly to the stock Item_PlaceItem epilogue `0x59E70C`, which returns the real native slot index in r0.

Consequences:
- BsMenuItem+0xD8 stores slot 0..3,
- stock `DropQueue_PollAndFinalize @ 0x596C84` sees State=1 while the balloon is active,
- lower-screen inventory stays in its normal wait state,
- another local inventory drop cannot start through the same menu action,
- no independent custom queue lock is needed.

The old `0x596C84(handle==4)->2` hook is removed and `0x596C84` is fully stock.

### Visual/persistence path

Ghidra-gpt-sol-5.6-F032 behavior is preserved:
- custom AcBalloon identity guard,
- selected inventory Item used for the falling present,
- only 0x21 balloon landing visual,
- impact field commit via `FieldTile_CommitItem @ 0x168E08`,
- tile refresh via `FieldTile_RefreshAfterCommit @ 0x599814`,
- Player state 0x16 retention via the terminal A4 guard.

The exact custom falling-object capture moved from cave 0x8383D8 to 0x838308.

### Completion timing

Ghidra-gpt-sol-5.6-F032 used shared+0x68 only until first impact. Ghidra-gpt-sol-5.6-F034 keeps the exact custom falling-object pointer through mode 0 -> mode 1.

At `FgObjPresent_Update @ 0x593E68`:
- mode 0 ground contact stores mode=1 at `0x593F4C`,
- Ghidra-gpt-sol-5.6-F032 field commit still runs there,
- shared+0x68 is intentionally not cleared at impact.

On the next mode-1 update, stock dispatch reaches `0x593F34`.

Ghidra-gpt-sol-5.6-F034 hooks `0x593F34` and, only when r4 == shared+0x68:
- loads the exact native DropData pointer from shared+0x6C,
- writes `State=2` to entry+0x0F,
- clears shared+0x6C and shared+0x68,
- executes the original `MOV r0,#1`,
- resumes stock at `0x593F38`.

This means queue completion is delayed until the falling-present visual enters its stock cleanup mode, rather than being reported immediately at request time or at initial impact.

Stock `0x596C84` then consumes State=2, performs ordinary type-0x0A completion semantics, clears the DropData slot back to State=0, and returns success to BsMenuItem.

### Failure/fallback

If the custom eligibility checks fail, the hook resumes stock `Item_PlaceItem` before FieldAction construction.

If custom AcBalloon creation fails after native slot allocation:
- shared+0x6C is cleared,
- execution resumes stock at 0x59E6A8,
- the already initialized native slot continues through the normal drop path.

Thus there is no stranded custom State=1 slot on the known spawn-failure path.

### Cave map

- 0x8381D8-0x838307: native-slot custom interceptor (0x130 bytes)
- 0x838308-0x838327: custom falling-object capture (0x20)
- 0x838330-0x83837F: custom BalloonPresent landing hook (0x50)
- 0x838380-0x8383BF: custom AcBalloon state helper (0x40)
- 0x8383C0-0x8383EF: native DropData completion hook (0x30)
- 0x838424-0x838463: terminal A4 reaction guard
- 0x838464-0x8384EB: impact field commit
- 0x838400-0x838423 remains untouched

### Hooks

ON:
- 0x596188 remains stock `BL Item_PlaceItem` = EB002109
- 0x59E6A4 -> 0x8381D8 = EA0A66CB
- 0x598BEC -> 0x838330 = EA0A7DCF
- 0x59AC50 -> 0x838308 = EA0A75AC
- 0x593F34 -> 0x8383C0 = EA0A9127
- 0x593F4C -> 0x838464 = EA0A9144
- 0x5C5A30 -> 0x838424 = EA09CA7B
- 0x596C84 is stock; synthetic poll hook removed

OFF restores:
- 0x59E6A4 = E1A0000D
- 0x593F34 = E3A01000
- plus the previously known Ghidra-gpt-sol-5.6-F032 restores.

### Static validation

- all AR payload lines are complete 2-word lines,
- every E-block encoded word count equals its declared byte length,
- all direct branch targets were recomputed from the final cave addresses,
- synthetic handle-4 compare/poll code is absent,
- Player_DropItem's stock BL to Item_PlaceItem is present.

Hardware validation pending:
- first inventory drop uses the 0x21 balloon visual and persists,
- source inventory Item remains present while State=1/in flight,
- a second drop cannot begin through the inventory UI during flight/landing,
- on mode-1 cleanup, State becomes 2, source Item is removed once, UI releases,
- a subsequent drop after completion works normally,
- no duplicate 0x0A landing visual,
- Player state remains 0x16.

## Ghidra-gpt-sol-5.6-F035: stock inventory-call signature for native queue interception

Ghidra-gpt-sol-5.6-F034 hardware result:
- behavior regressed to an ordinary normal drop, matching the visible result previously seen in Ghidra-gpt-sol-5.6-F030
- no crash or UI lock was reported
- therefore the custom branch at the post-allocation Item_PlaceItem intercept was not being selected on hardware, or it fell back before custom balloon creation

Static re-audit:
- Item_PlaceItem prologue is `STMDB sp!,{r0-r11,lr}; SUB sp,sp,#0x1C`
- saved LR is indeed `[sp+0x4C]`
- Player_DropItem calls Item_PlaceItem at `0x596188`, nominal LR `0x59618C`
- despite that static layout, LR-based discrimination did not work as a reliable hardware selector and is retired

IDA already documents a stronger stock signature for ordinary inventory drop:
`Player_DropItem -> Item_PlaceItem(0x0A, g_EmptyItem, ItemToPlace, ItemToShow, ...)`

At the callsite:
- 0x596178 = MOV r0,#0x0A
- 0x596180 = LDR r1,[pc,#0x24]
- literal 0x5961AC = 0x00955FF4
- 0x596188 = BL Item_PlaceItem

Inside Item_PlaceItem, after its push/sub frame:
- saved original r0 is [sp+0x1C]
- saved original r1 is [sp+0x20]
- saved original r2 is [sp+0x24]
- saved original r3 is [sp+0x28]

Ghidra-gpt-sol-5.6-F035 therefore changes only the custom-selector predicate:
- old: saved LR [sp+0x4C] == 0x59618C
- new: saved original r1 [sp+0x20] == 0x955FF4
- still require DropData.DropType(+0x0E) == 0x0A
- existing Ghidra-gpt-sol-5.6-F032 inventory-context globals and custom spawn/fallback behavior remain unchanged

All native queue behavior from Ghidra-gpt-sol-5.6-F034 is retained:
- stock Item_PlaceItem allocates one of four DropData slots
- queue full still returns -1 in stock code
- native slot remains State=1 during custom balloon flight/landing
- Ghidra-gpt-sol-5.6-F032 impact field commit remains unchanged
- exact slot becomes State=2 only after fgobj_ObjectPresent mode-1 cleanup at 0x593F34
- stock DropQueue_PollAndFinalize consumes State=2, removes inventory source once, clears slot to State=0, and releases UI
- synthetic handle 4 remains removed

AR cave change is only two words:
- 0x8381D8: E59D004C -> E59D0020
- literal 0x8382F4: 0x0059618C -> 0x00955FF4

Hardware validation pending.

## Ghidra-gpt-sol-5.6-F036: native DropData allocation from the Ghidra-gpt-sol-5.6-F032 callsite context

Hardware results leading here:
- Ghidra-gpt-sol-5.6-F034: ordinary normal drop
- Ghidra-gpt-sol-5.6-F035: unchanged ordinary normal drop
- both versions moved AcBalloon creation into Item_PlaceItem after native DropData allocation
- changing the post-allocation selector from saved LR to saved original r1==0x955FF4 did not change hardware behavior

Conclusion:
- the selector was not the material problem
- moving the custom balloon spawn into Item_PlaceItem's post-allocation execution context was the regression
- Ghidra-gpt-sol-5.6-F032's hardware success depended on executing the custom spawn from the Player_DropItem callsite context at 0x596188

### Ghidra-gpt-sol-5.6-F036 split design

The stock queue allocation and the custom visual creation are now split.

At Player_DropItem 0x596188:
- the hook enters a new high-page cave at 0x838E00
- SP is left untouched before calling stock Item_PlaceItem, so all seven stack arguments remain exactly stock
- the same Ghidra-gpt-sol-5.6-F032 eligibility globals are checked: 0x948DD4 must be nonzero and 0x948DDC must be zero
- if not eligible, the cave tail-jumps to stock Item_PlaceItem with LR still 0x59618C

For an eligible inventory drop:
- save original return LR in shared+0x78
- set transient allocator-arm shared+0x70=1
- BLX stock Item_PlaceItem @ 0x59E5B4

At Item_PlaceItem 0x59E6A4:
- hook now points to a tiny allocator-stop cave at 0x838F98
- no caller signature, no balloon spawn, no coordinate work occurs here
- if shared+0x70==0: execute original MOV r0,sp and resume stock 0x59E6A8
- if armed: save exact DropData* r4 at shared+0x6C and return through stock epilogue 0x59E70C before FieldAction construction
- native slot scanning, queue-full -1, Item copies, X/Y, DropType, Flags and State=1 all remain stock

Back in the 0x838E00 callsite cave:
- clear shared+0x70
- preserve the real native slot index at shared+0x74
- world X/Y are read from the original Player_DropItem stack arguments
- the selected Item is read from Player_DropItem's local Item copy at original sp+0x28
- the same Ghidra-gpt-sol-5.6-F032 Vec3 construction and AcBalloon spawn path is executed
- custom helper at 0x838380 is unchanged
- return to 0x59618C with r0 = the real native slot index

Thus the queue is stock, but AcBalloon creation is again performed from the same caller context that was hardware-verified in Ghidra-gpt-sol-5.6-F032.

### Failure behavior

If native queue is full:
- stock Item_PlaceItem returns -1
- Ghidra-gpt-sol-5.6-F036 returns that same -1 to Player_DropItem/BsMenuItem

If custom AcBalloon spawn fails after native slot allocation:
- exact DropData.State is changed to 3
- the real slot index is returned
- stock DropQueue_PollAndFinalize handles the error/finalization path

### Completion

The Ghidra-gpt-sol-5.6-F034/Ghidra-gpt-sol-5.6-F035 native completion path is retained:
- custom falling object remains exact identity at shared+0x68
- Ghidra-gpt-sol-5.6-F032 impact commit 0x168E08 -> 0x599814 is unchanged
- after mode-1 visual cleanup at 0x593F34, exact DropData* shared+0x6C receives State=2
- stock 0x596C84 consumes success, removes the source inventory Item once, clears the slot to State=0, and releases UI
- synthetic handle 4 remains absent

### Cave layout

Existing low caves are preserved:
- 0x838308-0x838327 custom falling-object capture
- 0x838330-0x83837F BalloonPresent landing substitution
- 0x838380-0x8383BF AcBalloon helper
- 0x8383C0-0x8383EF native queue completion
- 0x838424-0x838463 terminal A4 guard
- 0x838464-0x8384EB Ghidra-gpt-sol-5.6-F032 impact field commit

New high caves:
- 0x838E00-0x838F93 callsite/native-allocation bridge (0x194 bytes)
- 0x838F94 left as padding separation
- 0x838F98-0x838FC3 allocator-stop cave (0x2C bytes)

This leaves 0x838500-0x838DFF (0x900 bytes) untouched for the previously reserved replacement-string area.

Static original-image audit for 0x838E00-0x838FC4:
- ARM B/BL targets into range: 0
- aligned direct 32-bit initialized pointers into range: 0
- source image is part of the known executable zero-fill page after .text

Hooks:
- 0x596188 -> 0x838E00 = EB0A8B1C
- 0x59E6A4 -> 0x838F98 = EA0A6A3B
- existing Ghidra-gpt-sol-5.6-F032/Ghidra-gpt-sol-5.6-F034 landing/capture/completion/state hooks retained
- stock 0x596C84 remains unhooked

Hardware validation pending.

## Ghidra-gpt-sol-5.6-F037: Ghidra-gpt-sol-5.6-F036 crash-dump root cause and ABI-safe bridge

Hardware:
- Ghidra-gpt-sol-5.6-F036 crashed immediately when starting the inventory drop.
- crash dump: `crash_dump_00000010.dmp`
- SHA-256: `c350a6c97074e160f46bae592007ca3c8620c70866f0202075be9941b27df128`

Crash-dump register block (r0-r15 beginning at file offset 0x28):
- r0 = 0x009AE160
- r1 = 0x00000000
- r2 = 0x00003B68
- r3 = 0x00000001
- r4 = 0x009AE15C
- r5 = 0
- r6 = 0x52
- r7 = 0x35
- r8-r11 = 0
- r12 = 0x0059E5B4
- sp = 0x0FFFFD28
- lr = 0x0059E618
- pc = 0x002FC878
- cpsr = 0x10

Instruction correlation:
- `0x59E60C LDR r1,[sp,#0x24]`
- `0x59E610 ADD r0,r4,#4`
- `0x59E614 BL 0x2FC878`
- return LR = `0x59E618`
- `0x2FC878 LDRH r2,[r1]`

At the fault:
- r4 = 0x9AE15C = DropData slot 0 base
- r0 = 0x9AE160 = slot0 +4 = ItemToPlace destination
- r1 = 0 = source Item* passed to ItemID::Write
- therefore the crash is a NULL source dereference inside stock Item copy

The dump also contains `0x838E38`, the instruction immediately after Ghidra-gpt-sol-5.6-F036's BLX Item_PlaceItem, confirming the call originated from the new high cave.

Root cause:
- Ghidra-gpt-sol-5.6-F036 entered the high cave with the correct stock Item_PlaceItem ABI:
  r0=0x0A, r1=0x955FF4, r2=actual Item*, r3=shown Item*
- but eligibility code reused/clobbered r1/r2/r3 before BLX Item_PlaceItem
- Item_PlaceItem therefore received invalid argument registers
- this is an ABI-preservation bug in Ghidra-gpt-sol-5.6-F036, not a native DropData queue design failure

### Ghidra-gpt-sol-5.6-F037 fix

Before any eligibility logic:
- save original r0/r1/r2/r3 to shared+0x7C/+0x80/+0x84/+0x88
- save original LR to shared+0x78

Before BLX stock Item_PlaceItem:
- restore all original r0-r3 exactly
- do not alter SP, so all stock stack arguments remain at their original locations

Before calling stock:
- copy world X/Y from original stack into shared+0x08/+0x00
- copy the full Item from original r2 Item* into shared+0x04
- this removes later dependence on Player_DropItem stack-frame offsets

After native slot allocation:
- save returned slot index at shared+0x74
- reconstruct exact DropData* as `0x9AE15C + slot*0x12` and store at shared+0x6C
- no longer depend on Item_PlaceItem's transient r4 value being exported by the hook

During custom balloon construction:
- preserve all callee-saved registers r4-r11 plus LR around the custom path
- Ghidra-gpt-sol-5.6-F032 coordinate/Vec3/AcBalloon logic is then run from the original 0x596188 callsite context

Allocator-stop hook:
- moved to 0x838FD0
- armed: jump to stock Item_PlaceItem epilogue 0x59E70C before FieldAction construction
- unarmed: execute original MOV r0,sp and resume 0x59E6A8

Failure paths:
- native queue full returns the real stock -1
- custom spawn failure marks the exact native DropData.State=3 and returns its real handle for stock failure finalization

Queue completion/persistence remains unchanged:
- Ghidra-gpt-sol-5.6-F032 impact field commit 0x168E08 -> 0x599814
- exact native DropData.State=2 after mode-1 cleanup at 0x593F34
- stock 0x596C84 consumes/clears the slot and releases inventory UI
- synthetic handle 4 remains absent

### Ghidra-gpt-sol-5.6-F037 cave boundaries

- main bridge: 0x838E00-0x838FCF, 0x1D0 bytes
- allocator-stop: 0x838FD0-0x838FF7, 0x28 bytes
- highest written address is below 0x839000 .rodata start

Static AR audit:
- all E-block byte counts exact
- malformed lines: 0
- 0x596188 -> 0x838E00
- 0x59E6A4 -> 0x838FD0
- synthetic 0x596C84/handle-4 hook absent
