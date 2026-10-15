---
id: ACNL-F0586
aliases:
- IDA-gpt-6-sol-F005
title: 下位 `0x0C` でgohanの壁抜けを相手へ強制できるか（2026-10-04、MEDIUM）
summary: 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。gohanの実機確認済み壁抜けは `AcPlayer_UpdatePositionWithFieldChecks 0x64EBE0` 内の3**命令** `0x64F03C/0x64F19C/0x64F1B4` をON/OFFする。gohanのローカルPatchListはコード書換え後にキャッシュを更新する。一方、下位転送種別12の受信 `NetTransfer12_ReceiveTownChunk`
date: '2026-10-04'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6613984
- 6615100
- 6615452
- 6615476
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4423-4426
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F005: 下位 `0x0C` でgohanの壁抜けを相手へ強制できるか（2026-10-04、MEDIUM）

解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。gohanの実機確認済み壁抜けは `AcPlayer_UpdatePositionWithFieldChecks 0x64EBE0` 内の3**命令** `0x64F03C/0x64F19C/0x64F1B4` をON/OFFする。gohanのローカルPatchListはコード書換え後にキャッシュを更新する。一方、下位転送種別12の受信 `NetTransfer12_ReceiveTownChunk` は普通の `Mem_CopyBytes3` のみで、権限変更も命令キャッシュ更新も行わない。静的配置で3語は `.text` の `rx` にあり、実機ページ権限と任意片配送は未確認。gohan導入端末でローカルパッチが成功した事実は、未導入の相手でも受信コピーによる命令書換えが可能な証拠ではない。既存PatchListのON/OFFが `0x0C` 単独で相手に成立する根拠はない。位置処理とcallerを調べた範囲で独立のデータのみの壁抜けスイッチも未同定。IDA命令・原本bytes/SHA・gohan実装の独立照合は `work/evidence/network/town_transfer_wallclip_feasibility_20261004.md`。反証条件: 実機で相手コードページの書込みとキャッシュ反映が確認される、または独立のデータのみの壁抜け経路が確定する。主IDBへ関数2件・グローバル2件のrename、引数/グローバル型と根拠コメントを保存し、再読込で確認。実機送信・適用は行っていない。

