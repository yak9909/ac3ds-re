---
id: ACNL-F0566
aliases:
- IDA-unknown-F016
- V2-F016
title: sub_5C9C24 は夢見の館で落とした町を読み込んだ直後の作り直し（2026-09-18、MEDIUM）
summary: Dream_RebuildDownloadedTown 0x5C9C24 の呼び出し元は DreamNet_ApplyDownloadedTown 0x6E205C だけ。こちらは受信 465024 B（0x71880）を TownBase へ複写し vc_PLOAD の後に呼ぶ。そこへ入る状態を設定する DreamNet_BeginDownloadTown 0x6E2850 / DreamNet_BeginDownloadListedTown 0x6E2774 の呼び出し元
date: '2026-09-18'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6069284
- 7217244
- 7219280
- 7219060
- 1082192
- 2256164
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4268-4271
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F016: sub_5C9C24 は夢見の館で落とした町を読み込んだ直後の作り直し（2026-09-18、MEDIUM）

Dream_RebuildDownloadedTown 0x5C9C24 の呼び出し元は DreamNet_ApplyDownloadedTown 0x6E205C だけ。こちらは受信 465024 B（0x71880）を TownBase へ複写し vc_PLOAD の後に呼ぶ。そこへ入る状態を設定する DreamNet_BeginDownloadTown 0x6E2850 / DreamNet_BeginDownloadListedTown 0x6E2774 の呼び出し元は ModuleDream.cro の 1 関数だけ（CRO インポート解決、code.bin 内の BL/リテラル走査 0 件）。中身は時刻を町の日付へ、FIXFURNO、Structure_StampAll(1,1)（建物の足元のアイテム削除）、Bbs_ResetToDefault 0x108350、Field_DeleteHouseMarkers 0x226D24 など。日替わり・成長処理は呼ばない。IDA-unknown-F015 の「アイテム消えない」のパッチ 1/2 が日替わり以外で効く場面の一つは夢見の館の町読み込み。LOW: 2 つの Begin のどちらが夢番地入力か、sub_6070CC/sub_606964、[garden+401890] の 16 個の正体。反証条件: 実機で夢見の館以外（通信の訪問等）で 0x5C9C24 に到達する。根拠 work/evidence/prepare_screen/growup.md 追記。

