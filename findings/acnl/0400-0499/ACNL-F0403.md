---
id: ACNL-F0403
aliases:
- F-376
title: 'F-376（2026-09-08）: A1/A2 抜き診断ビルド（遷移クラッシュの切り分け用）'
summary: F-375 修正後も切り分け中のため、変数を 1 つずつ潰す診断ビルド。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24206-24219
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-376（2026-09-08）: A1/A2 抜き診断ビルド（遷移クラッシュの切り分け用）

F-375 修正後も切り分け中のため、変数を 1 つずつ潰す診断ビルド。
`OwnGui.cpp` の `InstallHooks()` 先頭で `kDiagNoHooks = true` のとき
素のまま通す（検証器の順序検査に触れない形）。しずえフック抜きは継続。
検証器 2 種 0 件。**切り分けが済んだら両方とも戻すこと。**

診断計画：
- T-C2（本ビルド）： A1/A2 なし＋しずえフックなし＋他は全部入りで
  タイトル→しずえ遷移。落ちれば A1/A2 は無罪（メニュースレッド・
  フォント/木・素の遷移バグへ）。落ちなければ A1/A2 が有罪。
- 併せて素の遷移の反復（E1 は 1 回きり。レースなら素でも落ちうる）と、
  村ドア等ほかの遷移がチートONで通るかも確認する。

