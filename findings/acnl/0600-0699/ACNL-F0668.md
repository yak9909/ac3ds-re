---
id: ACNL-F0668
aliases:
- Ghidra-gpt-sol-5.6-F029
- G-F029
title: direct falling visualを維持し、impact時だけground itemを確定
summary: 'Ghidra-gpt-sol-5.6-F028 hardware result:'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5848680
- 5903708
- 5876712
- 3110348
- 5876816
- 5848908
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1328-1432
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F029: direct falling visualを維持し、impact時だけground itemを確定

Ghidra-gpt-sol-5.6-F028 hardware result:
- custom balloonではなく通常ドロップになった
- drop後inventory completionが解放されず、下画面が操作不能になった

Ghidra-gpt-sol-5.6-F028は撤回する。full stock BalloonPresent_TryLandAndPlaceを戻す方式は、custom側のsynthetic completion handle 4とstock FieldAction type 0x21を二重に走らせ、custom inventory lifecycleと競合する。

### Ghidra-gpt-sol-5.6-F027の成功部分

Ghidra-gpt-sol-5.6-F027では:
- selected inventory Itemの見た目で風船から落下した
- Player state 0x16を維持した
- synthetic handle 4でinventory/UI completionを維持できた

失敗は着地後にvisualが消える点だけだった。

### fgobj_ObjectPresent着地処理

`FgObjPresent_Update @ 0x593E68` を追跡すると、mode 0のfalling presentは最初の着地時に:
- 0x590EA0をcall
- 0x593F4Cでobject+0x146へmode 1を書込
- 後続mode 1処理でvisual objectを削除
する。

このupdate自体はpersistent ground Itemを生成しない。従ってGhidra-gpt-sol-5.6-F027は正しいfalling visualだけが存在し、着地後に消えるのが構造上の動作だった。

### stock ground-item finalizer

`0x5A155C` を `FieldAction_FinalizeGroundItem` と同定。
このroutineはaction-entry-like構造を受け取り:
- 0x168E08でfield/tile data更新
- 0x59DA7Cでtile/object occupancy更新
- 0x59A4A0でpersistent ground fgobj生成
を行う。

実際に参照するentry field:
- +0x00 shown/empty Item
- +0x04 actual Item
- +0x0C flags
- +0x0E tile X
- +0x0F tile Y
- +0x15 player id

### Ghidra-gpt-sol-5.6-F029 design

Ghidra-gpt-sol-5.6-F027のdirect balloon falling pathとsynthetic completionを復元した上で、custom falling objectだけを捕捉する。

`BalloonPresent_CreateAtTile @ 0x59ABE8` 内:
- r6はItem*を保持
- custom pathではr6 == shared+0x04
- 0x593D0Cが作ったfgobj_ObjectPresent*は0x59AC48後のr1

0x59AC50をhookし、r6 == shared+0x04の時だけr1をshared+0x68へ保存する。

次に0x593F4Cをhookし:
- original `STRB r0,[r4,#0x146]`を実行
- new mode == 1
- r4 == shared+0x68
の時だけ一度:
- shared+0x68をclear
- synthetic entryをshared+0x80に構築
- actual Item = falling object+0x64
- X/Y = saved shared+0x08/+0x00
- player id = 0x2F75CC
- `FieldAction_FinalizeGroundItem @ 0x5A155C`をcall
する。

その後stock FgObjPresent_Update @ 0x593F50へ戻る。

これによりfull stock balloon FieldAction type 0x21を起動せず、Ghidra-gpt-sol-5.6-F027で正常だったinventory completion/UI releaseを維持したまま、visual impactの瞬間に地面Itemだけ確定する。

### caves / hooks

- capture cave 0x8383D8-0x8383F7 (0x20 bytes)
- impact cave 0x838464-0x8384F3 (AR E-block 0x90 bytes including padding)
- 0x59AC50 -> 0x8383D8 = EA0A75E0
- 0x593F4C -> 0x838464 = EA0A9144
- OFF restore 0x59AC50 = E5980014
- OFF restore 0x593F4C = E5C40146

Static collision:
- existing ARM B/BL target into both new cave ranges: 0
- initialized aligned direct pointers into both ranges: 0

AR E-block audit:
- 0x838424 length 0x40: exact
- 0x838464 length 0x90: exact
- 0x838200 length 0x1D8: exact
- 0x8383D8 length 0x20: exact
- all payload lines are complete 2-word CTRPF lines

Ghidra export:
- acnl_jpn_v15_balloon_impact_persistence_delta.xml
- size 25832
- SHA-256 5801d08e4973ab13afed1d0bb348794752c5f3070dd4d0cd8ef6943b2853c28e
- bytes size 1237
- bytes SHA-256 bb113b4c6e2d1913677f11745df79ba2698603e0c2e780cc99cc6d67f09b6087

Hardware validation pending:
- selected Item falls from balloon
- after visual impact the same Item remains on the ground
- inventory slot/drag state releases normally
- Player state remains 0x16

