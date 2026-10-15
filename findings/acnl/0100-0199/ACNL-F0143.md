---
id: ACNL-F0143
aliases:
- F-105
title: 'F-105: ★MCP 側から Suspend できる（CLAUDE.md の記述を訂正）'
summary: 'confidence: **HIGH**（実機で制御実験）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1273956
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6337-6407
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-105: ★MCP 側から Suspend できる（CLAUDE.md の記述を訂正）

confidence: **HIGH**（実機で制御実験）

### 結論

**`py_eval` から `ida_dbg.suspend_process()` / `request_suspend_process()` で停止できる。**
CLAUDE.md の旧記述「呼んでも停止できない」は**誤り**だった。

| 呼び方 | 走行中の戻り値 | 停止中の戻り値 | 結果 |
|---|---|---|---|
| `suspend_process()` | `True` | `False` | **停止する** |
| `request_suspend_process()` + `run_requests()` | `True` / `run_requests` は `False` | — | **停止する** |

**`run_requests()` が `False` を返しても失敗ではない。**

### ★決定的な仕組み: ハンドラ復帰後に効く

制御実験（ユーザーには IDA を触らないよう依頼した上で実施）:

```
呼び出しA: state=-1 → continue_process() → state=1
           → request_suspend_process()=True, run_requests()=False
           → sleep(1) しても state=1 のまま → そのまま返る
呼び出しB: state=-1 ★停止していた  PC=0x00137064
```

同期版も同じ:

```
呼び出しC: continue → state=1 → suspend_process()=True
           → sleep(2) しても state=1 のまま → そのまま返る
呼び出しD: state=-1 ★停止していた  PC=0x00137064
```

**停止が反映されるのは `py_eval` のハンドラが返って
IDA のイベントループが回ったあと。**
**同じ呼び出しの中で `time.sleep` して待っても止まらない。**
必ずツール呼び出しを分けること。

### 途中で踏んだ誤り 2 件

1. **「走行中は MCP 呼び出しが一切処理されない」と結論しかけた。**
   実際はユーザーが IDA の設定ダイアログを開いていたためで、
   モーダルダイアログがメインスレッドを塞いでいた。
   **交絡した観測から構造的な結論を出しかけた。**
   CLAUDE.md「一度の観測を一般化しない」に反していた。
2. 最初に `suspend_process()` が `False` を返したのを「効かない証拠」と読みかけたが、
   **既に停止済みだったから**だった。
   戻り値は「走行中に呼べば `True`、停止中なら `False`」という状態判定に使える。

### 運用への影響

**ユーザーへの手動 Suspend 依頼が不要になった。**
「continue → ユーザー操作 → 手動 Suspend → 読み出し」という往復が、
`suspend_process()` を挟むだけで自動化できる。
breakpoint も自由に使えるようになった（F-104）ので、
**動的解析の手数が大幅に下がった。**

### タイムアウトの解釈（CLAUDE.md に追記）

**タイムアウト = フリーズではない。** 原因は少なくとも 3 つある:

- IDA でモーダルダイアログが開いている（今回の実例）
- 先行の要求が滞留して後続が詰まる
- 実際に対象がフリーズしている（bp を残したまま再開した場合。F-104）

**切り分けるまで原因を断定しない。**

---

