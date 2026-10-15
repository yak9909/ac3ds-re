---
id: ACNL-F0545
aliases:
- IDA-opus-5-F007
title: park 用の BP は `0x1B721C` では張れなくなる。`0x1B7220` が同値（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。同じ boot の前半では `0x001B721C` への'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1798684
- 1798688
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3998-4016
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F007: park 用の BP は `0x1B721C` では張れなくなる。`0x1B7220` が同値（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。同じ boot の前半では `0x001B721C` への
`add_bpt` ＋ `continue_process` が何度も成功していたが、**その番地へフック語を書いて元へ戻したあと、
`continue_process` が必ず `False` を返すようになった**（3 回再現）。BP を消すと resume は通る。
`0x00838FFC` の BP は最後まで正常なので、番地固有の現象。

迂回: **`0x001B7220` は `0x001B721C` と同じく NOP で、xref は `0x1B721C` からの落下 1 件のみ**
（`Frame_DrawPass1024` 内、ラベル無し）。したがってそこで停めた機械状態は park と同一で、
実測でも SP は `0x0FFFFE20` で一致した。`tree_live.PARK` を差し替えるだけで動く
（語の検査は NOP 比較なのでそのまま通る）。

**運用の訂正: `ida_dbg.continue_process()` を直接呼ばない。** 必ず `tools/dynamic/run_timed.py`
経由にする（タイマーを先に登録するので、失敗しても走りっぱなしにならない）。
本セッションでは直接呼んで 2 回ターゲットを無制限走行させ、利用者に手動 Suspend を依頼した。

根拠: `events.jsonl`、本文の再現手順。反証条件: 再起動後に `0x1B721C` の BP が復活する
（＝ boot 内の状態に依存する現象であることの確認になる）。

