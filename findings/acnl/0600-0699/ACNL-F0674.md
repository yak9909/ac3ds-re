---
id: ACNL-F0674
aliases:
- Ghidra-gpt-sol-5.6-F034
- G-F034
title: native DropData queue integration
summary: Ghidra-gpt-sol-5.6-F032 remains the hardware-verified visual/persistence baseline. Ghidra-gpt-sol-5.6-F033's independent busy flag is retired.
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5891508
- 5891748
- 10150236
- 5857672
- 5857676
- 5891752
- 5891852
- 5860484
- 1478152
- 5871636
- 5848680
- 5848908
- 5848884
- 5848888
- 5868524
- 5876816
- 6052400
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1784-1919
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
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

