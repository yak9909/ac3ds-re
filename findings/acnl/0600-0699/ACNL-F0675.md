---
id: ACNL-F0675
aliases:
- Ghidra-gpt-sol-5.6-F035
- G-F035
title: stock inventory-call signature for native queue interception
summary: 'Ghidra-gpt-sol-5.6-F034 hardware result:'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5857672
- 5857676
- 5857656
- 5857664
- 5857708
- 9789428
- 5848884
tags:
- inventory
supersedes: []
source: Ghidra:work/FINDINGS.md:1920-1968
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
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

