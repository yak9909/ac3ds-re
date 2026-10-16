# Drop / balloon pipeline re-analysis — Ghidra-gpt-sol-5.6-F038 design before AR

Status: **analysis/design only**. No Ghidra-gpt-sol-5.6-F038 AR payload is introduced here.

## Conclusion

The native four-slot DropData queue is **not required** for the custom balloon path.

Ghidra-gpt-sol-5.6-F032 already hardware-proved two critical facts:

1. `Player_DropItem` may return synthetic handle `4` to BsMenuItem.
2. If `DropQueue_PollAndFinalize @ 0x596C84` intercepts handle 4 and returns success, the stock BsMenuItem success path removes the source Item and restores the UI correctly.

The Ghidra-gpt-sol-5.6-F032 defect was narrower: its handle-4 hook returned `2` immediately. That released the inventory UI while the custom balloon was still in flight and allowed the shared Item/X/Y buffer to be overwritten by another drop.

The minimal fix is therefore to make synthetic handle 4 **asynchronous**.

```
custom request accepted:
    syntheticStatus = 1
    return handle 4

poll(handle 4):
    status 1 -> return 1      // wait
    status 2 -> clear -> 2    // success
    status 3 -> clear -> 3    // failure

custom visual impact:
    FieldTile_CommitItem(...)
    FieldTile_RefreshAfterCommit(...)
    syntheticStatus = 2
```

No native DropData slot, normal-drop FieldAction, or custom busy flag is needed.

## 1. Inventory UI contract

### BsMenuItem_DropStart @ 0x19AD30

Ghidra re-decompile confirms:

- obtains the selected Item pointer;
- calls `Player_DropItem @ 0x596084`;
- stores the return value at `BsMenuItem+0xD8`;
- only `-1` is treated as immediate failure.

BsMenuItem does not independently validate that the token is 0..3.

### BsMenuItem_DropWait @ 0x19AF8C

Every update it calls:

```
result = DropQueue_PollAndFinalize(this->dropHandle)
```

Observed result contract:

- 0 / 1: remain in the wait state;
- 2: run the stock success path, remove/refresh the source inventory slot, advance UI state;
- 3: run the stock error path.

Therefore the menu only requires an opaque token whose poll operation obeys this result contract.

This is also hardware-supported by Ghidra-gpt-sol-5.6-F032: handle 4 plus an entry hook at 0x596C84 successfully completed the inventory/UI lifecycle.

## 2. Stock normal drop lifecycle

### Player_DropItem @ 0x596084

Normal flow:

```
selected Item*
    -> Drop_FindTargetTile @ 0x5979E4
    -> Item_PlaceItem(type=0x0A, ...)
    -> native handle 0..3
```

`Drop_FindTargetTile` is a true prerequisite for a normal inventory drop. It requires a valid player/field context and searches candidate tiles through the stock placeability checks.

### Item_PlaceItem @ 0x59E5B4

This function must not be treated as a queue allocator API.

It:

1. scans four `g_DropDataTable @ 0x9AE15C` entries for State=0;
2. copies ItemToReplace / ItemToPlace / ItemToShow;
3. stores X/Y, DropType, flags;
4. sets State=1;
5. except for special type 0x10, immediately converts the slot into a FieldAction record and dispatches it.

Thus calling or partially splicing Item_PlaceItem solely to acquire a handle necessarily couples the custom operation to the normal-drop lifecycle. Ghidra-gpt-sol-5.6-F034/Ghidra-gpt-sol-5.6-F035 visibly regressed to ordinary drop; Ghidra-gpt-sol-5.6-F036/Ghidra-gpt-sol-5.6-F037 added ABI/call-contract failures while trying to separate the two halves.

Ghidra-gpt-sol-5.6-F038 does not call Item_PlaceItem on the custom-success path.

## 3. Natural balloon lifecycle

### BalloonPresent_TryLandAndPlace @ 0x598BEC

The natural AcBalloon terminal path is independent of inventory DropData.

On a valid landing it:

1. resolves tile candidates;
2. calls `FieldAction_RegisterActive @ 0x59FCFC` with action type `0x21`;
3. initializes a record;
4. `BalloonPresent_BuildRecord @ 0x59EB3C` encodes action type 0x21;
5. sends/dispatches the record through `0x59E878`;
6. independently calls `BalloonPresent_CreateAtTile @ 0x59ABE8`.

It does not allocate a four-slot DropData handle for inventory UI.

Ghidra-gpt-sol-5.6-F028 hardware showed that restoring this complete stock 0x21 lifecycle inside the custom inventory operation produced the wrong visible behavior and left the inventory lifecycle unreleased. It therefore remains excluded from the custom path.

## 4. Hardware-verified Ghidra-gpt-sol-5.6-F032 operation path

The working custom operation remains unchanged:

1. intercept the `Player_DropItem` callsite at `0x596188`;
2. preserve the original Item and target tile;
3. create the custom AcBalloon using the Ghidra-gpt-sol-5.6-F032 call contract;
4. pre-arm exact custom AcBalloon identity before its synchronous terminal call;
5. identify only that actor at `0x598BEC`;
6. bypass the full natural 0x21 FieldAction body;
7. call `BalloonPresent_CreateAtTile @ 0x59ABE8` with the original inventory Item;
8. capture the exact `fgobj_ObjectPresent*`;
9. on mode-0 ground contact, call only:
   - `FieldTile_CommitItem @ 0x168E08`
   - `FieldTile_RefreshAfterCommit @ 0x599814`;
10. preserve the existing custom-AcBalloon A4 reaction guard.

Hardware result for Ghidra-gpt-sol-5.6-F032:

- selected Item is the falling visual;
- only the custom/0x21-style landing visual is seen;
- the same Item persists on the field;
- lower-screen UI is usable;
- Player state remains 0x16.

No other operation path should be reintroduced until this baseline is preserved.

## 5. Function preconditions

### ActorFactory_CreateByTypeId @ 0x57ADFC

This is a generic creation wrapper, not a balloon-specific API.

Verified hidden/staged call contract:

- r1 must be a valid manager pointer;
- r3 is staged through 0x947FE8;
- caller stack argument #5 is staged through 0x947FEC;
- nonzero staged values are later dereferenced as structured pointers.

Ghidra-gpt-sol-5.6-F037 crashed because stack arg #5 became 0x0A. Ghidra-gpt-sol-5.6-F032 explicitly supplies stack arg #5 = 0. Keep that exact sequence.

### BalloonPresent_CreateAtTile @ 0x59ABE8

Inputs are effectively:

```
(Item*, tileX, tileY, impactVec3*, mode)
```

It requires:

- active field-object manager;
- tile/object creation availability check to succeed;
- a free falling-present object slot.

It returns false if creation fails. On success it calls `FgObjPresent_SpawnFalling @ 0x593D0C`.

For Ghidra-gpt-sol-5.6-F038, a synchronous false result is a valid custom failure condition and should publish synthetic status 3.

### FgObjPresent_Update @ 0x593E68

Mode 0:

- integrates falling position;
- at ground contact performs the stock impact transition;
- writes mode 1.

Mode 1:

- performs visual-object cleanup/destruction;
- does not commit field Item data.

Therefore mode-1 cleanup is **not** a prerequisite for inventory completion.

### FieldTile_CommitItem @ 0x168E08

At the hardware-verified Ghidra-gpt-sol-5.6-F032 call site:

- r0 = tile X
- r1 = tile Y
- r2 = flags (0)
- r3 = local player id
- stack arg #5 = Item*

This is the persistent field-data write used after the custom falling visual reaches the target.

### FieldTile_RefreshAfterCommit @ 0x599814

Called with the same tile X/Y after 0x168E08. It marks the tile dirty for refresh.

Ghidra-gpt-sol-5.6-F038 must publish success only after both calls have returned.

## 6. Ghidra-gpt-sol-5.6-F038 synthetic completion state

Use one unused Ghidra-gpt-sol-5.6-F032 shared word, proposed `shared+0x6C`:

- 0 = idle
- 1 = custom operation active / wait
- 2 = field commit completed / success pending consumption
- 3 = custom operation failed / failure pending consumption

This is not a second queue. It is one state word belonging to the one synthetic token value 4.

### Arm timing

Do not set status=1 before AcBalloon creation succeeds.

Recommended sequence:

```
ActorFactory...
if actor == NULL:
    stock fallback

status = 1
call AcBalloon state helper
return synthetic handle 4
```

The status must be 1 before the state helper because the terminal landing call is synchronous inside that helper.

### Landing-creation failure

The custom `0x598BEC` replacement directly calls `0x59ABE8`.

If `0x59ABE8` returns false:

```
status = 3
```

The BsMenuItem wait state then exits through its stock failure path without removing the source Item.

An additional post-state-helper invariant may be used:

```
if status == 1 && shared.customFallingObject == NULL:
    status = 3
```

This covers a synchronous terminal path that failed to create the expected visual.

No speculative asynchronous failure state is invented until a concrete object-abort path is identified.

## 7. Poll hook contract

`DropQueue_PollAndFinalize @ 0x596C84` must be intercepted before it indexes `g_DropDataTable`, because handle 4 is out of native range.

Pseudo-code only:

（疑似C を省略。原本は _local/legacy-src/…）

For non-4 handles, execute the original prologue and resume stock at 0x596C88.

## 8. Completion point

At the existing Ghidra-gpt-sol-5.6-F032 exact-object impact hook:

```
if exact custom falling object:
    clear customFallingObject
    FieldTile_CommitItem(...)
    FieldTile_RefreshAfterCommit(...)
    syntheticStatus = 2
resume stock FgObjPresent_Update
```

This is intentionally earlier than mode-1 object deletion.

Reason: after mode 0 -> 1 transition, the object owns all remaining cleanup state internally. Ghidra re-decompile shows mode 1 does not use the shared Item/X/Y buffer and does not perform persistence. Once 0x168E08 and 0x599814 have completed, allowing BsMenuItem to remove the source inventory Item and accept a later drop cannot corrupt the old visual cleanup.

## 9. Functions excluded from the Ghidra-gpt-sol-5.6-F038 custom-success path

Do not call:

- `Item_PlaceItem @ 0x59E5B4`
- `FieldAction_QueueToRecord @ 0x59EBE8`
- `FieldAction_Dispatch @ 0x59E8F8`
- `FieldActionType0A_GroundDropUpdate @ 0x5A0C2C`
- action 0x12 handler `0x5A155C`
- normal-drop visual constructor `0x59A4A0`
- full stock `BalloonPresent_TryLandAndPlace @ 0x598BEC` for the custom actor.

These belong to other lifecycles and caused previous regressions/duplicate effects.

## 10. Final invariant

The custom balloon operation and inventory completion are separate:

- **actual operation:** unchanged hardware-verified Ghidra-gpt-sol-5.6-F032 path;
- **inventory wait/completion:** synthetic handle 4 with a 1 -> 2/3 asynchronous status.

This removes the only Ghidra-gpt-sol-5.6-F032 race without touching native DropData or normal FieldAction processing.

## 11. Validation order before any AR is accepted

After implementation, verify in this order:

1. request returns synthetic handle 4 and status becomes 1;
2. while falling, repeated 0x596C84(4) returns 1;
3. source Item remains in inventory while falling;
4. no second inventory drop can start while the BsMenuItem wait state is active;
5. exact selected Item lands using only the Ghidra-gpt-sol-5.6-F032 visual;
6. 0x168E08 then 0x599814 execute once;
7. only after those calls, status becomes 2;
8. next poll returns 2 and clears status to 0;
9. source inventory Item is removed once and UI releases;
10. Player state remains 0x16;
11. next drop can start normally;
12. forced/synchronous 0x59ABE8 failure returns status 3 and preserves the source inventory Item.



## Superseded by Ghidra-gpt-sol-5.6-F039 independent cross-check

The Ghidra-gpt-sol-5.6-F038 async synthetic-token direction remains valid, but its timing explanation and failure handling were re-audited independently.

Ghidra-gpt-sol-5.6-F039 supersedes this document for implementation design:
- no assumption about whether terminal processing is synchronous with the custom state setter;
- pre-arm actor identity, falling-object state, and WAIT status before the state transition;
- use existing 0x59AC50 capture as visual-creation success evidence;
- classify missing falling-object pointer at the exact post-landing A4 reaction as FAILURE;
- publish SUCCESS only after 0x168E08 -> 0x599814;
- keep status 2/3 persistent instead of clearing in poll.

See `docs/balloon_drop_gf039_design.md` and `work/evidence/balloon_drop_dual_verification_20260916.md`.
