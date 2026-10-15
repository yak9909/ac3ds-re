---
id: ACNL-F0018
aliases:
- F-396
title: 'F-396: 旧SWKBDケーブとGUI v2の重複を回避し再適用'
summary: HIGH（配置の重複と適用内容をソース/実機メモリで照合。移設後の起動動作は未観測）。
date: '2026-09-10'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:136-148
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-396: 旧SWKBDケーブとGUI v2の重複を回避し再適用

HIGH（配置の重複と適用内容をソース/実機メモリで照合。移設後の起動動作は未観測）。
旧0x00838D20..0x00838F20はGUI A2=0x00838CE8..0x00838E4C、
N=0x00838E60..0x00838E8Cと重なる。再起動後のauditが非ゼロを検出し、書込み前に中止。
新0x00838200..0x00838400は現行GUIの常設/一時コードと非重複で、実機で全域ゼロ。
SWKBDだけ再リンク。元の実機成功バイナリとの機械比較で外部BLの相対変位13語だけが変わり、
各宛先は同一。その他命令・局所分岐・リテラル・初期データは同一。
全分岐/LDR監査と12経路エミュレーションPASS後に実機適用・独立読み戻しPASS。
実機ケーブページの新規512 bytes以外、GUIデータと各hookが不変。F-394の3gxも不変。
IDAのmapping列挙は-6で未対応。6入口のIDB/実機一致と実機読取りで対象領域を確認した。
再現SYSTEM_KEYBOARD/verify_native_chat_relocation.py、詳細scratchpad/MEMO_f396_swkbd_reapply.md。

