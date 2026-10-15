---
id: ACNL-F0672
aliases:
- Ghidra-gpt-sol-5.6-F033
- G-F033
title: custom falling objectをbusy tokenにしてdrop queueをlock
summary: 'Ghidra-gpt-sol-5.6-F032 hardware success後の残課題:'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5876712
- 5848908
- 5857412
- 5857672
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1672-1735
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0673"]
---
## Ghidra-gpt-sol-5.6-F033: custom falling objectをbusy tokenにしてdrop queueをlock

Ghidra-gpt-sol-5.6-F032 hardware success後の残課題:
- synthetic completion handle 4によりinventory UIは早期に解放される
- custom balloon/drop animation中でも次のinventory dropを開始できる
- 2回目dropがshared Item/worldX/worldY等を更新し、同じ場所への重複dropを起こし得る

既存のshared+0x68は`BalloonPresent_CreateAtTile @ 0x59ABE8`で生成されたexact custom `fgobj_ObjectPresent*`を保持し、Ghidra-gpt-sol-5.6-F032 impact hook `0x593F4C`でground-contactした最初の1回にclearされる。

このlifetimeはqueue lockにそのまま利用できる:
- custom falling object生成前: shared+0x68 == 0
- falling/drop animation中: shared+0x68 != 0
- ground impact/field commit開始: shared+0x68をclear

### precheck cave

既存drawing cave終了0x8381D7とballoon main cave開始0x838200の間のgap:
- `0x8381D8-0x8381F7`
- static ARM B/BL target into range: 0
- initialized aligned direct pointer into range: 0

payload:
- `0x8381D8 LDR r12,=0x01E81000`
- `0x8381DC LDR r12,[r12,#0x68]`
- `0x8381E0 CMP r12,#0`
- `0x8381E4 MVNNE r0,#0`  // -1
- `0x8381E8 BXNE lr`
- `0x8381EC B 0x838200`
- literal/padding at 0x8381F0/0x8381F4

`Player_DropItem @ 0x596084`内のstock Item_PlaceItem callsite hook:
- old `0x596188 EB0A881C -> 0x838200`
- new `0x596188 EB0A8812 -> 0x8381D8`

busy時は`r0=-1`で元callerへ即returnする。
BsMenuItem stock callbackは-1だけをimmediate failureとして扱うため:
- 2回目Itemを消費しない
- completion handle待機stateへ入らない
- stock Item_PlaceItem fallbackを実行しない
- shared drop coordinates/Itemを上書きしない

not busy時は0x838200へbranchし、Ghidra-gpt-sol-5.6-F032のhardware-validated custom balloon pathをそのまま実行する。

### lock/unlock timing

lock setに専用writeは不要。
`shared+0x68`はcustom falling object生成時に同期的に設定され、Player_DropItemがsynthetic handle 4を返すより前に有効になる。

unlockはGhidra-gpt-sol-5.6-F032 impact hookがexact custom objectのground contactを検出した時の既存:
`MOV r6,#0 ; STR r6,[shared,#0x68]`
を利用する。

従ってuser inputから見たlock windowは、custom falling object生成完了からground impactまで。

Ghidra-gpt-sol-5.6-F033 Ghidra scoped export:
- XML `acnl_jpn_v15_balloon_queue_lock_delta.xml` size 26593 SHA-256 `0007605911aac0b1859c96a56548bd7e7a9a21bddb7981c4741a4469713b1e39`
- bytes size 1237 SHA-256 `0fd2ad6fbe827e157db4cb62331a691b2d414118db1a44b2f35ed1e5f683aa66`

Hardware validation pending:
- 1個目のcustom balloon drop中に2個目をdropしても2個目はfieldへ出ない
- 2個目inventory Itemは残る
- UI lock/操作不能にならない
- 1個目impact後は次のdropを正常に開始できる

