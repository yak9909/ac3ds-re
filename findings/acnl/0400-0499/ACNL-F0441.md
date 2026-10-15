---
id: ACNL-F0441
aliases:
- IDA-gpt-6-sol-F007
title: 下位種別12の送信APIと2台同時接続時の座標宛先（2026-10-04、静的＋実測）
summary: NEW 3DS LLとOLD 3DSを同じ村に同時接続した屋外で、両機とも `Town=0x31F49A80`、`XYZ=0x33099E50` と実測。Python計算で下位種別12の累積オフセットは `0x11514BA`、16B本文は `[u32 streamOffset, X, Y, Z]`。汎用 `NetTransfer_SendSegments 0x616E10` は町サイズで制限しないが、通常町送信 `0x61FE5C` は制限する。送信の9引数ABI、2Bヘッ
date: '2026-10-04'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 6385168
- 6422108
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:235-238
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F007: 下位種別12の送信APIと2台同時接続時の座標宛先（2026-10-04、静的＋実測）

NEW 3DS LLとOLD 3DSを同じ村に同時接続した屋外で、両機とも `Town=0x31F49A80`、`XYZ=0x33099E50` と実測。Python計算で下位種別12の累積オフセットは `0x11514BA`、16B本文は `[u32 streamOffset, X, Y, Z]`。汎用 `NetTransfer_SendSegments 0x616E10` は町サイズで制限しないが、通常町送信 `0x61FE5C` は制限する。送信の9引数ABI、2Bヘッダ、相手選択・キューをcallerとcalleeで照合した。受信側は町外コピー後に完了処理を必ず呼ぶため、連続座標同期の成立は未検証。両機が表示したslot0は通信管理上の生番号の証明ではない。管理フィールドを追加した読取り診断版は `work/coord-sync-map-editor` でpush済み。IDB rename/型/コメントを保存しXML検証PASS。今回のアドレス計算はHIGH、偽造片の実配送・書込みはLOW。根拠・反証条件: [coord_sync_send_20261004.md](evidence/network/coord_sync_send_20261004.md)。

