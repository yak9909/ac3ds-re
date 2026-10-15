---
id: ACNL-F0676
aliases:
- Ghidra-gpt-sol-5.6-F036
- G-F036
title: native DropData allocation from the Ghidra-gpt-sol-5.6-F032 callsite context
summary: 'Hardware results leading here:'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 9789428
- 5857672
- 9735636
- 9735644
- 5857676
- 5891508
- 5891748
- 5891752
- 5891852
- 1478152
- 5871636
- 5848884
- 5860484
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1969-2064
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
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

