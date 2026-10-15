---
id: ACNL-F0006
aliases:
- F-406
title: F-406 実機ヒープコード実行成功・全復元済み（2026-09-11、最新）
summary: F-405の停止はユーザー提供dumpでカーネルのD-cache clean by MVAに確定。F-406では全体cache SVC 0x92/0x94へ変更し、組立前ソース検査・全4リテラル/1分岐・4条件ABI試験・実機の領域/アンカー照合後に1回だけ実行した。plugin heap 0x061BE000の2命令から0x5Aが返り、control phase4を確認（HIGH）。後続の5 MiB全域照合、内蔵辞書/code全Read/CRC/Close/Release/
date: '2026-09-11'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4603428
tags:
- heap
supersedes: []
source: v1:RE/FINDINGS.md:39-46
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-406 実機ヒープコード実行成功・全復元済み（2026-09-11、最新）

F-405の停止はユーザー提供dumpでカーネルのD-cache clean by MVAに確定。F-406では全体cache SVC 0x92/0x94へ変更し、組立前ソース検査・全4リテラル/1分岐・4条件ABI試験・実機の領域/アンカー照合後に1回だけ実行した。plugin heap 0x061BE000の2命令から0x5Aが返り、control phase4を確認（HIGH）。後続の5 MiB全域照合、内蔵辞書/code全Read/CRC/Close/Release/freeもstate2/failure0で成功。これは最小コードの実行成功であり、変換エンジン本体/VFP/実機候補取得は未検証。

結果をSYSTEM_KEYBOARD/evidence/f406_exec/hardware_result.jsonへ保存後、vtable slot0x07029DD8を0x070012B8へ復元。cave0x00838600の予約全0x200 bytes、control0x009BE840の全0x20 bytesはbackup一致。別の読取りでもゼロ/元vtable/command0を確認しrestored.jsonへ保存。最終ACNL Suspend(-1)、ARM32、PSR0x20000010、PC0x00463E24、SP0x32283B98、bp0。map APIの空リストは未マップ判定に使わない。試験buffer/handles保持なし。F-396 launcherは再起動後に未再適用。

現行の実機プラグインと3gxファイルは独立Plugin/SwkbdProbeのF-404版。gohan正常版は変更なし。次は内蔵取得codeのRAM展開/再配置・辞書context初期化・実機候補照合。辞書やcodeのSD/3gxリソース同梱、自前メニュー統合はしない。詳細DOCS/system_keyboard_plugin_probe.md。

