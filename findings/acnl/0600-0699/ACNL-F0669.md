---
id: ACNL-F0669
aliases:
- Ghidra-gpt-sol-5.6-F030
- G-F030
title: action 0x12誤用を撤回し、stock action 0x0Aでimpact定着
summary: 'Ghidra-gpt-sol-5.6-F029 hardware result:'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5899988
- 5901292
- 5903708
- 5901356
- 5874848
- 5904048
- 5876816
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1433-1512
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F030: action 0x12誤用を撤回し、stock action 0x0Aでimpact定着

Ghidra-gpt-sol-5.6-F029 hardware result:
- selected inventory Itemの見た目で風船から落下
- 着地後は依然として消滅
- 着地時に岩破壊のようなeffectが発生
- user hypothesis: drop/action ID 0x12

この0x12仮説は静的解析で確認できた。

`FieldAction_DispatchGroundOperation @ 0x5A06D4` のjump table:
- operation byte = record+0x10
- case 0x12 -> 0x5A0BEC -> BL 0x5A155C
- case 0x0A -> このdispatcherではdefault/no-op arm

従ってGhidra-gpt-sol-5.6-F029が直接呼んだ0x5A155Cはgeneric ground finalizerではなく、operation 0x12専用handlerだった。
hardwareで見えた岩破壊様effectは、この誤った0x12 handler実行と整合する。

### normal drop action 0x0A

`FieldActionType0A_GroundDropUpdate @ 0x5A0C2C` を復元。
record+0x11 == 1 かつ operation +0x10 が0x0A/0x22の時:
- local player idをrecord+0x15と照合
- player/network index record+0x0DからPlayer positionを取得
- `GroundItem_SpawnPersistentFgObj @ 0x59A4A0` を record+0x08 Item, tile X/Yでcall
- 成功時に必要条件ならtile state更新
- record+0x11 = 2

`FieldAction_CreateOperationRecord @ 0x5A16B0` からlayoutも確認:
- +0x00/+0x04/+0x08 = 4-byte Item fields
- +0x0C = flags
- +0x0D = player/network index
- +0x0E/+0x0F = tile X/Y
- +0x10 = operation type
- +0x11 = state
- +0x15 = player id

### Ghidra-gpt-sol-5.6-F030

Ghidra-gpt-sol-5.6-F027/Ghidra-gpt-sol-5.6-F029の成功部分は維持:
- direct falling-present visual
- custom fgobj capture at 0x59AC50
- synthetic inventory completion handle 4
- Player state 0x16 preservation

着地hook 0x593F4Cでcustom falling objectがmode 0->1になる最初の1回だけ:
- transient recordを shared+0x80 に構築
- Item shared+0x04をrecord+0x04/+0x08へcopy
- flags=0
- current player/network indexを0x305F6Cで取得し+0x0D
- saved worldX/worldYを+0x0E/+0x0F
- +0x10=0x0A
- +0x11=1
- player idを0x2F75CCで取得し+0x15
- `FieldActionType0A_GroundDropUpdate @ 0x5A0C2C` を直接call

stock FieldAction slot/poolは新規allocateしないため、inventory側synthetic completionとの競合を避ける。
`0x5A155C` / action 0x12は完全に不使用。

Impact cave:
- 0x838464-0x8384EB
- executable 0x84 bytes + 4-byte padding
- E-block length 0x88
- binary SHA-256 a228d276acb1f022a3994a09f2699ae1833262cf5a81140948fa7bd2c097aa77 (executable 0x84)
- existing B/BL targets into cave: 0

Ghidra export:
- acnl_jpn_v15_balloon_action0a_persistence_delta.xml
- size 34004
- SHA-256 a4b6a5b2e2229fe0009cdd7aad1615f8f216dc40ec52c66045714261370b8a14
- companion bytes size 4481
- bytes SHA-256 6a9acf6d2ef4e7aa0d2fa54b6e64272b8b242115db23d74701d771ac9d939a59

Hardware validation pending:
- selected Item still falls from balloon
- rock-destruction-like effect is gone
- same Item persists on ground
- lower-screen UI releases
- Player state remains 0x16

