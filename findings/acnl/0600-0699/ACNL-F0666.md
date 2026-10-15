---
id: ACNL-F0666
aliases:
- Ghidra-gpt-sol-5.6-F027
- G-F027
title: landing identityをstate helper内でpre-arm
summary: 'Ghidra-gpt-sol-5.6-F026 hardware result:'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5868524
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1186-1257
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F027: landing identityをstate helper内でpre-arm

Ghidra-gpt-sol-5.6-F026 hardware result:
- custom balloon経路にならず、通常ドロップへfallbackした

再監査で原因を特定。

Ghidra-gpt-sol-5.6-F026ではcustom AcBalloon*をshared+0x60へ保存する命令が:
- spawn cave 0x8382E8
- AcBalloon state helper 0x838380からreturnした後
に置かれていた。

しかしBalloonPresent_TryLandAndPlace @ 0x598BECはAcBalloon state transitionの実行中に同期的に呼ばれる。
従来のshared+0x0C armed方式でlanding overrideが成立していたこと自体も、この順序を示す。

従ってGhidra-gpt-sol-5.6-F026のlanding時点ではshared+0x60がまだ未設定で:
- incoming r4 == shared+0x60 が不一致
- custom landing pathへ入らない
- stock BalloonPresent_TryLandAndPlaceへfallback
となっていた。

### Ghidra-gpt-sol-5.6-F027 fix

state helper内、AcBalloon state setterをBLXする前に:
- r4 = custom AcBalloon*
- STR r4,[r10,#0x60]
を実行する。

具体的にはhelper:
- old MOV r2,#1 ; STR r2,[r10,#0x0C]
- new STR r4,[r10,#0x60] ; NOP
へ変更。

Ghidra-gpt-sol-5.6-F026以降landing判定はshared+0x0Cを使わないため、armed=1設定は不要。
helper後半のshared+0x0C clearは残し、旧値を確実に0へ戻す。

landing同期call時点:
- shared+0x60 = custom AcBalloon*
- ModuleVillage caller r4 = same AcBalloon*
となるためidentity判定が成立する。

helper return後のspawn cave STR r0,[r10,#0x60] も残し、subsequent terminal A4 reaction guard用にidentityを再確認保存する。
helperはreturn直前にr0=r4としているため同一pointer。

### ABI revalidation

ModuleVillage AcBalloon_TerminalDrop_CRO @ 0xBFCBA8:
- entry MOV r4,r0
- item path call BL 0xBE3DE8 at 0xBFCC08/2C/94/C4
- r4 remains AcBalloon* through these calls
- later 0xBFCCD8 LDRSB r0,[r4,#0x240]
- 0xBFCCDC reaction helper call

Main BalloonPresent_TryLandAndPlace @ 0x598BEC decompile confirms formal ABI is two arguments:
- r0 = impact/position pointer
- r1 = Item*
so r2 is not an incoming formal argument。

Ghidra-gpt-sol-5.6-F027 therefore keeps landing comparison:
- LDR r2,[shared,#0x60]
- CMP r4,r2
and on match passes shared+0x04 inventory Item to BalloonPresent_CreateAtTile.

Ghidra export:
- XML acnl_jpn_v15_balloon_inventory_item_timing_delta.xml
- size 23251
- SHA-256 6c394eeef7444a2d9bad634b2a9b354c7000dcbd8ed163a2ed24775e6102365d
- bytes size 576
- bytes SHA-256 81e13c44bd4e05c21ea2b853a21851ed3059444e39ba422ba75ad077d4ec1d22

Hardware validation pending.

