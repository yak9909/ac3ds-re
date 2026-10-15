---
id: ACNL-F0413
aliases:
- F-388
title: 'F-388: ACNLのSuspendでは動作中SWKBDプロセスは停止しない（2026-09-09）'
summary: 利用者が内蔵キーボードへ未確定の`かんじ`を入力したまま現在のIDAでSuspendしたところ、
date: '2026-09-09'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 4603428
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:24393-24404
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-388: ACNLのSuspendでは動作中SWKBDプロセスは停止しない（2026-09-09）

利用者が内蔵キーボードへ未確定の`かんじ`を入力したまま現在のIDAでSuspendしたところ、
キーボードは動作を継続した。同時にACNL側を読み取るとdebugger state=-1、
PC=`0x00463E24`、breakpoint 0、launcher state=2、run count=3だった。state 2は本ケーブの
`ST_RUNNING`で、ACNLがSWKBDのAPT要求を開始し、まだ戻り結果を受け取っていない状態である。

利用者の画面観測とACNL側の待機状態が一致するため、**現在のport 4000接続がSuspendするのは
ACNLプロセスだけであり、ライブラリアプレットSWKBDは別プロセスとして走行を続ける**ことを
HIGHで確認した。候補cacheを読むにはSWKBD自身を空きGDBポートへ割り当てて停止する必要がある。
一次記録:`SYSTEM_KEYBOARD/evidence/native_chat_active_applet_acnl_side.json`。

