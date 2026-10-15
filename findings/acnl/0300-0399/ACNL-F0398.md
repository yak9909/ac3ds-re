---
id: ACNL-F0398
aliases:
- F-371
title: 'F-371（2026-09-08）: 訂正 pitch—項目OFF・発火なしでも落ちる'
summary: 利用者の訂正： 現在の停止は**チートON＋項目OFF**での遷移中のもの。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 5664248
- 5672856
- 5555236
- 5555256
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24087-24105
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-371（2026-09-08）: 訂正 pitch—項目OFF・発火なしでも落ちる

利用者の訂正： 現在の停止は**チートON＋項目OFF**での遷移中のもの。
発火は起きていない（要求 `0xFFFF` と一致）。「項目ON/OFFは無関係」
「自前チートONだけ・他に変更なし」の申告どおり。

### 確定した状態（実機値）

- A1 `0x00566DF8`＝B、A2 `0x00568F98`＝B（チートON）
- SH `0x0054C424`＝B（フック入り）。
  項目OFFなのでコールバックは読むだけで帰る。発火なし。
- PC=`0x0054C438`（`LDR R0,[R4,#0x148]`）、R4=`0x0`、部屋 `0x63`。

### 残る軸（発火は除外済み）

1. フック存在自体、2. チートON状態の他要素（A1/A2・入力遮断等）、
3. 素の遷移バグ。次はフルOFF（3 語とも PUSH に戻ったことを確認）
で同遷移。落ちれば (3)、落ちなければフック抜きビルドで (1)/(2) を分ける。

