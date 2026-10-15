---
id: ACNL-F0540
aliases:
- IDA-opus-5-F021
title: park の BP は焼き付かない。直前に外した番地だけが一時的に拒む（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。'
date: '2026-09-21'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1798684
- 1798688
- 1798692
- 1798700
- 1798708
- 1798712
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3776-3803
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F021: park の BP は焼き付かない。直前に外した番地だけが一時的に拒む（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。

このセッションで「park の BP が焼き付いた」と7回判断し、そのたびに NOP を
`0x1B721C` → `0x1B7220` → `0x1B7224` → `0x1B722C` → `0x1B7234` → `0x1B7238` と消費した。
**これは誤り。番地は回復する。**

実験（`0x1B7238` が拒んだ直後）:

| 操作 | 結果 |
|---|---|
| `0x1B7238` に BP あり → `continue_process()` | **失敗** |
| BP を外して `continue_process()` | 成功 |
| `0x1B7238` に BP を付け直して `continue_process()` | **失敗** |
| `0x1B7238` を外し、**以前「焼き付いた」`0x1B722C`** に付けて `continue_process()` | **成功。park もヒットした** |

つまり **「直前に BP を外した番地」だけが一時的に再武装を拒む**。
対策は簡単で、**2つ以上の park NOP を交互に使う**。新しい NOP を探して消費しなくてよい。

### 併せて: `run_timed` の成否判定が偽陰性を出していた

`tree_live.timed()` は `runpy` の戻り値の `_timer` が `None` かどうかで失敗を判定していた。
ところが**再開に成功しても `_timer` が `None` になることがある**（`print` などの最中に IDA が
イベントループを回し、タイマのコールバックが `_timer = None` を書くため）。
このせいで「再開できなかった」と誤判定し、上の「焼き付き」の誤診断を招いた。
`run_timed.py` に `_ok = main()` を持たせ、`timed()` はそちらを見るように直した。

