---
id: ACNL-F0670
aliases:
- Ghidra-gpt-sol-5.6-F031
- G-F031
title: Player-origin updaterを外し、balloon impact位置からpersistent ground objectを生成
summary: 'Ghidra-gpt-sol-5.6-F030 hardware result:'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5901356
- 5874848
- 5848680
- 5848908
- 5876816
tags:
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:1513-1583
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F031: Player-origin updaterを外し、balloon impact位置からpersistent ground objectを生成

Ghidra-gpt-sol-5.6-F030 hardware result:
- バグ/操作不能はない
- しかしcustom balloon dropではなく、通常ドロップとして見える

原因は`FieldActionType0A_GroundDropUpdate @ 0x5A0C2C`のdecompileで確定。
このupdaterはoperation 0x0Aを処理する際:
- record+0x0DからPlayerを取得
- Player+0x14/+0x18/+0x1Cをlocal Vec3へcopy
- Yへstock offsetを加える
- そのPlayer位置Vec3をfifth argumentとして`GroundItem_SpawnPersistentFgObj @ 0x59A4A0`へ渡す

従ってGhidra-gpt-sol-5.6-F030はballoon impact後に、Player位置を始点とした通常drop objectをもう一度生成していた。

`FgObjPresent_Update @ 0x593E68`も再decompile。
`0x593F4C`は:
- current Yがground target `object+0x140`以下になった後
- mode 0 caseで`FUN_00590EA0`を実行した直後
- mode byte `object+0x146`を1へ変更する
実際のground-contact transitionであることを再確認。

### Ghidra-gpt-sol-5.6-F031

Ghidra-gpt-sol-5.6-F030のoperation record / 0x5A0C2C callを完全撤去。
custom falling objectが0x593F4Cへ到達した最初の1回だけ:
- shared+0x68 custom falling-object identityを確認
- identityをclear
- Item* = shared+0x04
- tile X = shared+0x08
- tile Y = shared+0x00
- flag = 0
- fifth argument = `fallingObject+0x40` (impact時のcurrent Vec3)
- `GroundItem_SpawnPersistentFgObj @ 0x59A4A0`を直接call

これによりstock FieldAction state machineもoperation 0x0A updaterも通さず、persistent ground objectの生成primitiveだけを使用する。
開始位置はPlayerではなくballoon visualの着地点なので、通常drop animationを再生成しない。

maintained:
- Ghidra-gpt-sol-5.6-F027 direct balloon falling visual
- shared+0x04 original inventory Item
- custom fgobj capture at 0x59AC50
- synthetic completion handle 4
- Player state 0x16 preservation
- custom AcBalloon terminal A4 suppression

Impact cave:
- 0x838464-0x8384C3
- E-block 0x60 bytes
- direct BL at 0x8384A8 -> 0x59A4A0 (`EBF587FC`)
- existing main-image B/BL targets into cave: 0
- initialized aligned pointers into cave: 0

AR E-block audit:
- 0x838424: 0x40 exact
- 0x838464: 0x60 exact
- 0x838200: 0x1D8 exact
- 0x8383D8: 0x20 exact
- malformed/incomplete lines: 0

Ghidra-gpt-sol-5.6-F031 exchange:
- XML `acnl_jpn_v15_balloon_direct_ground_spawn_delta.xml` size 21158 SHA-256 a9a472d4b8c1a03e6cbe2bdbe2d0ea3772a66a76ca75170ef430895d0b6971ac
- bytes size 2409 SHA-256 5df78c7a0520caf66b933b2af90ca0e3ad00a419c4fb20c827fa9b72fb5a92f7

Hardware validation pending:
- still falls from balloon
- no second normal-drop animation
- ground Item remains after impact
- lower screen stays interactive
- Player state stays 0x16

