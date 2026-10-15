---
id: ACNL-F0392
aliases:
- F-365
title: 'F-365（2026-09-08）: メニューON/OFF でホットキー判定を送る（opt-in）'
summary: 利用者の要求：ホットキーが無いときにチートが ON/OFF されたら、
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23884-23907
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-365（2026-09-08）: メニューON/OFF でホットキー判定を送る（opt-in）

利用者の要求：ホットキーが無いときにチートが ON/OFF されたら、
ホットキーによる有効化／無効化の判定として扱う。
送らないようにもできること。

### 実装（`Sources/GuiMenu.cpp` / `Includes/GuiMenu.hpp`）

- `ToggleEvaluate(index, now)` を新設。ホットキー押下時とメニューON/OFF時
  の共通路（読取検証→反転→通知。題はチート名）。
  `FireHotkeyItem()` のエンジン部はこれを呼ぶだけにした。
- `SetEffectMenuJudgment(index, send)`（既定 OFF）+ `g_fxMenuJudge[]`。
  ON の項目だけ、`ApplyItem()` で適用値が反転したときに
  `ToggleEvaluate()` を送る。値だけ・束縛だけの変更では送らない。
  `DiscardAll()`（適用値は不変）・`SetItemApplied()`（関数側の同期用）では
  送らない。
- 読みは「束縛の有無を問わない」とした。フラグ自体が利用者の項目ごとの
  制御であり、ホットキーを持たない項目の運用が主用途のため。
  既定 OFF のままなら従来通り（メニューはアームだけで効果に触らない）。

confidence: MEDIUM（検証器 2 種 0 件 + ビルド。実機未確認）。
実機で見ること： 判定ONの項目でメニューON→反転＋通知、メニューOFF→
反転＋通知。既定OFFの項目は従来通り何もしないこと。

