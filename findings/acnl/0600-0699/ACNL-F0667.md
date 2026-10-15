---
id: ACNL-F0667
aliases:
- Ghidra-gpt-sol-5.6-F028
- G-F028
title: custom Item substitutionをstock landing persistence経路へ戻す
summary: 'Ghidra-gpt-sol-5.6-F027 hardware result:'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5876712
- 5868524
- 5868876
- 5868888
- 5868924
- 5868936
- 5868960
- 5868528
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1258-1327
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: superseded
consolidated_into: ''
duplicate_of: ''
superseded_by: ACNL-F0668
---
## Ghidra-gpt-sol-5.6-F028: custom Item substitutionをstock landing persistence経路へ戻す

Ghidra-gpt-sol-5.6-F027 hardware result:
- dropped item visual matches the selected inventory Item
- Player state 0x16 remains preserved
- however the falling Item disappears after landing instead of remaining on the ground

原因:
- Ghidra-gpt-sol-5.6-F027 custom landing bypasses BalloonPresent_TryLandAndPlace body
- it directly calls BalloonPresent_CreateAtTile @ 0x59ABE8
- this creates/activates the falling fgobj_ObjectPresent visual
- but skips the stock success path that registers and dispatches the persistent field action

Ghidra stock BalloonPresent_TryLandAndPlace @ 0x598BEC confirms the persistent success path:
- 0x598D4C: FieldAction_RegisterActive(type=0x21, tile, context, 1)
- 0x598D58: FieldAction_InitRecord
- 0x598D7C: BalloonPresent_BuildFieldActionRecord(record, Item*, x, y, ...)
- 0x598D88: FieldAction dispatch/send
- 0x598DA0: BalloonPresent_CreateAtTile(Item*, x, y, impact, 0)

Thus 0x59ABE8 alone is only the falling-present object creation side of the stock landing operation; persistence requires the preceding FieldAction/record chain.

### Ghidra-gpt-sol-5.6-F028 design

Do not directly call 0x59ABE8 for custom balloons.
Instead, hook the entry of BalloonPresent_TryLandAndPlace only to substitute its Item argument:

- incoming r0 = impact/position pointer
- incoming r1 = stock ModuleVillage Item* (normally Item 0x2036 for default balloon)
- incoming r4 = AcBalloon* retained by the ModuleVillage caller

At cave 0x838330:
- load shared base
- load shared+0x60 custom AcBalloon*
- compare incoming r4
- if equal, set r1 = shared+0x04 (captured original inventory Item)
- execute original prologue PUSH {r0,r1,r4-r11,lr}
- branch to stock continuation 0x598BF0

Natural balloons do not match the custom actor identity, so their original r1 Item remains unchanged.

Relevant patch words:
- 0x838330 E59FC040  LDR r12,=0x01E81000
- 0x838334 E59C2060  LDR r2,[r12,#0x60]
- 0x838338 E1540002  CMP r4,r2
- 0x83833C 028C1004  ADDEQ r1,r12,#4
- 0x838340 E92D4FF3  original BalloonPresent_TryLandAndPlace prologue
- 0x838344 EAF58229  B 0x598BF0

This keeps:
- Ghidra-gpt-sol-5.6-F027 pre-armed custom AcBalloon identity
- Ghidra-gpt-sol-5.6-F025 terminal A4 reaction suppression
- synthetic inventory completion handle 4
while restoring stock field-placement persistence.

Ghidra export:
- XML acnl_jpn_v15_balloon_landing_persistence_delta.xml
- size 25055
- SHA-256 8fafb1b3c2049208f51d94ba70459dd95482e781ff9ead0e5c330e9987c18d16
- bytes size 576
- bytes SHA-256 81e13c44bd4e05c21ea2b853a21851ed3059444e39ba422ba75ad077d4ec1d22

Hardware validation pending:
- selected inventory Item falls from balloon
- Item remains on ground after landing
- source inventory slot clears once
- Player state remains 0x16
- inventory remains interactive
- natural balloon behavior stays stock

