---
id: ACNL-F0665
aliases:
- Ghidra-gpt-sol-5.6-F026
- G-F026
title: terminal landingをcustom AcBalloon identityで識別し、元Inventory Itemをpayloadにする
summary: Ghidra-gpt-sol-5.6-F025実機成功後、fieldへ落ちるItemがなお 0x2036 のプレゼント（中身ランダム）だった。
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5868524
- 5857672
tags:
- inventory
supersedes: []
source: Ghidra:work/FINDINGS.md:1115-1185
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F026: terminal landingをcustom AcBalloon identityで識別し、元Inventory Itemをpayloadにする

Ghidra-gpt-sol-5.6-F025実機成功後、fieldへ落ちるItemがなお 0x2036 のプレゼント（中身ランダム）だった。

原因:
- Player_DropItem hookでは actual inventory Item* から4-byte Itemを読み、shared+0x04へ保存済み
- しかし従来landing hook 0x598BEC は shared+0x0C == 1 のときだけcustom pathへ入る
- Ghidra-gpt-sol-5.6-F024で判明した通り、このarmed flagはstate helper return後に0へ戻る
- ModuleVillage terminal dropはその後に実行されるため、landing hookはstock pathへ流れる
- stock ModuleVillage terminal dropはdefault variantでItem 0x2036を構築し BalloonPresent_TryLandAndPlaceへ渡す
- そのため実機ではランダムプレゼントになる

ModuleVillage terminal-drop Ghidra disassembly:
- function entry 0xBFCBA8 でAcBalloon*をr4へ保持
- default Item path: 0xBFCC08 BL 0xBE3DE8
- variant 2/1/3も同importを 0xBFCC2C / 0xBFCC94 / 0xBFCCC4 からcall
- function後半 0xBFCCD8 LDRSB r0,[r4,#0x240] までr4はAcBalloon*のまま
- import 0xBE3DE8 はmain BalloonPresent_TryLandAndPlace @ 0x598BEC

したがってmain 0x598BEC入口でもincoming r4でcaller AcBalloon*を識別できる。

Ghidra-gpt-sol-5.6-F026 landing hook:
- shared = 0x01E81000
- if r4 == shared+0x60(customAcBalloon*) then custom path
- BalloonPresent_CreateAtTile receives Item* = shared+0x04
- worldX = shared+0x08, worldY = shared+0x00, impact Vec3 = shared+0x10
- otherwise execute stock BalloonPresent_TryLandAndPlace

変更命令:
- 0x838334: LDR r2,[r12,#0x0C] -> LDR r2,[r12,#0x60] (E59C2060)
- 0x838338: CMP r2,#1 -> CMP r4,r2 (E1540002)
- 0x83833C BNE stock は不変
- custom pathの0x838350 ADD r0,r12,#4以降は既存のまま

shared+0x04は Player_DropItem @ 0x596188 hook入口で:
- r2 = actual inventory Item*
- LDR r6,[r2]
- STR r6,[shared,#4]
として4-byte Item全体をcopyしている。
従ってitem IDだけでなくItem metadataも元持ち物の値を保持する。

自然風船はr4がshared+0x60と一致しないためstock Item選択を維持する。
custom actor identityはterminal landing後もGhidra-gpt-sol-5.6-F025 A4 guardで使い、A4 skip時にclearする。

### AR text completeness correction

Ghidra-gpt-sol-5.6-F025先頭guard E-blockは E0838424 0000003C (60 bytes) で、payload末尾が単独 00000000 1word行になっていた。
CTRPFのコードテキスト行は2word形式で扱うため不完全。

Ghidra-gpt-sol-5.6-F026では:
- block length 0x40
- final padding 00000000 00000000
へ修正。

全AR code lineを 8hex + 8hex の2word形式で再検査済み。

hashes:
- identity/reaction guard E payload 0x40: 43765ecdd5930943099b3aac2c9daf29d152f47b8dbe354e88464e84cf3fecf7
- main balloon cave 0x1D8 (inventory-item landing identity版): 7976029b7f4290c86a4aaf32b3e91c0c3cc7ee8b133f72731fdcca8ffea38a15
- combined: 6e37be11d1cc66cc323867915f0f15117a0c0ee5c2ec6b076b8bfb4a8de749cb

Ghidra scoped export:
- XML acnl_jpn_v15_balloon_inventory_item_delta.xml size 21817 SHA-256 b606806a91dbdde7a5b4776001e7f36649e88f71380c13c395fb6aa585ded3a8
- bytes companion size 576 SHA-256 81e13c44bd4e05c21ea2b853a21851ed3059444e39ba422ba75ad077d4ec1d22

Hardware validation pending:
- dropped present contains the exact inventory Item/ID selected for drop
- Player state remains 0x16
- inventory slot clears and UI remains interactive
- natural balloon payload behavior remains stock

