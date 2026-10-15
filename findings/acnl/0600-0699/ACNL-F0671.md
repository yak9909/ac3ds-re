---
id: ACNL-F0671
aliases:
- Ghidra-gpt-sol-5.6-F032
- G-F032
title: 0x0A visual生成を外し、stock post-visual field commitだけ再利用
summary: 'Ghidra-gpt-sol-5.6-F031 hardware result:'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5901356
- 5901832
- 5901968
- 5902000
- 5874848
- 5902016
- 3110348
- 5902028
- 3110372
- 5902044
- 5902072
- 1478152
- 5902076
- 5902084
- 5871636
- 5902228
- 5848680
- 5848908
- 5848912
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1584-1671
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F032: 0x0A visual生成を外し、stock post-visual field commitだけ再利用

Ghidra-gpt-sol-5.6-F031 hardware result:
- custom balloon 0x21の落下挙動は正常
- selected inventory Itemの見た目も正常
- しかし着地後は定着せず消滅
- 着地時に0x21由来の着地animationと0x0A由来の着地animationが同時再生され、二重表示に見える
- animation終了後、定着直前で消えるように見える

この観測でGhidra-gpt-sol-5.6-F031の誤認を修正。

### stock action 0x0A caseを命令単位で分離

`FieldActionType0A_GroundDropUpdate @ 0x5A0C2C` のcase 0x0A targetは `0x5A0E08`。

case 0x0Aでは:
- 0x5A0E90..0x5A0EB0: Player位置から開始Vec3を作り、`0x59A4A0`をcall
- 0x5A0EB0: `BL 0x59A4A0`
- success後 0x5A0EC0: current player id取得 (`0x2F75CC`)
- 0x5A0ECC: local/authority gate (`0x2F75E4(8,id)`)
- 0x5A0EDC..0x5A0EF8: X/Y, flags, player id, Item*を構成して `0x168E08`
- 0x5A0EFC..0x5A0F04: same X/Yで `0x599814`
- 0x5A0F94: record stateを2へ

従って`0x59A4A0`はpersistent field commitそのものではない。
Ghidra-gpt-sol-5.6-F031 hardwareで0x21 visualと同時に0x0A landing animationが出たことからも、`0x59A4A0`はoperation 0x0A側のdrop/landing visual constructorであることが実機確認された。

persistent field data側はその後段:
- `FieldTile_CommitItem @ 0x168E08`
- `FieldTile_RefreshAfterCommit @ 0x599814`
である。

### Ghidra-gpt-sol-5.6-F032

Ghidra-gpt-sol-5.6-F031のimpact hookから `0x59A4A0` callを完全撤去。

custom `fgobj_ObjectPresent` が `FgObjPresent_Update @ 0x593E68` のground-contact transition `0x593F4C` に到達した最初の1回だけ:
- shared+0x68 custom falling object identityを確認してclear
- fifth arg = Item* `shared+0x04`
- r0 = saved tile X `shared+0x08`
- r1 = saved tile Y `shared+0x00`
- r2 = flags 0
- r3 = current player id from `0x2F75CC`
- `FieldTile_CommitItem @ 0x168E08`
- then `FieldTile_RefreshAfterCommit @ 0x599814` with same X/Y
- stock `FgObjPresent_Update+0xE8 (0x593F50)`へ復帰

これにより:
- 0x21 falling/landing visualは1本だけ残す
- 0x0A visualを新規生成しない
- operation 0x0A/0x12 state machineを起動しない
- stock 0x0Aがvisual生成成功後に行うfield data確定だけを再利用する

Impact cave:
- 0x838464-0x8384E7 executable 0x84 bytes
- E-block 0x88 bytes (4-byte padding含む)
- payload SHA-256 `19c489e8952ec952f4ea94401665e0cc3c52ebfb3533cbeddde3626be9535f8c`
- caveは0x838500 replacement stringsより前に収まる

Ghidra annotations:
- 0x59A4A0 -> `GroundItem_SpawnDropVisual`
- 0x168E08 -> `FieldTile_CommitItem`
- 0x599814 -> `FieldTile_RefreshAfterCommit`
- 0x5A0C2C comment updated with split 0x0A path
- 0x593E68 comment updated with Ghidra-gpt-sol-5.6-F032 impact commit

Ghidra-gpt-sol-5.6-F032 exchange:
- XML `acnl_jpn_v15_balloon_field_commit_delta.xml` size 32069 SHA-256 `4cbb9cac1987701f822fc2c421c317672a6c7f7d02d72cddc674f583bacc4662`
- bytes size 2522 SHA-256 `15432816dee3d936dbe541369ea2793a277e7fa06fb4d241e50efd4f159cc339`

Hardware validation pending:
- 0x21 balloon landing animationだけが再生される
- 0x0A由来の二重animationが消える
- impact後に同じItemがfield tileへ定着する
- lower screen remains interactive
- Player state remains 0x16

### Ghidra-gpt-sol-5.6-F032 hardware validation — SUCCESS

実機確認:
- custom balloon/0x21 landing animationのみ再生され、Ghidra-gpt-sol-5.6-F031で発生した0x0A由来の二重表示は消失
- selected inventory Itemが風船から落下
- impact後、そのItemがfield tileへ正常に定着
- lower-screen UIは正常に解放され操作可能
- Player state 0x16を維持

従ってGhidra-gpt-sol-5.6-F032の`FieldTile_CommitItem @ 0x168E08 -> FieldTile_RefreshAfterCommit @ 0x599814`だけを0x21 impact時に実行する設計はhardware-validatedとする。

