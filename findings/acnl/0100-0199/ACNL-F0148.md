---
id: ACNL-F0148
aliases:
- F-110
title: 'F-110: ★`Use stepping support` を OFF にしても、ヒットした bp の削除は必要（TODO-54 完了）'
summary: 'confidence: **HIGH**（実機で対照実験。ユーザーの目視確認つき）'
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5158976
- 5150632
- 4603428
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6712-6783
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0153"]
---
## F-110: ★`Use stepping support` を OFF にしても、ヒットした bp の削除は必要（TODO-54 完了）

confidence: **HIGH**（実機で対照実験。ユーザーの目視確認つき）

TODO-54 の検証。CLAUDE.md に「未検証」と書いてあった仮説を実機で否定した。

### 前提

- 3DS を再起動し、IDA で再アタッチ
- **`Use stepping support` を OFF** にした状態（前回の試行はこれが ON だったため無効）
- 対象 bp: `Scene_DrawLayers`(`0x4EB840`)。**毎フレーム到達する**ので
  再開が正常なら約 16ms 後に必ず再ヒットする

### 手順と結果（同一の呼び出しを並べた対照実験）

| # | 操作 | 直後のプローブ (`get_process_state` / `PC`) |
|---|---|---|
| 1 | `state=-1` 確認、既存 bp 全削除、`add_bpt(0x4EB840, 0, BPT_SOFT)` | — |
| 2 | `continue_process()` → `True` | **成功**: `state=-1 PC=0x4EB840 LR=0x4E97A8` |
| 3 | **bp を削除せず** `continue_process()` → `True` | **タイムアウト ×2** |
| 4 | ユーザーが目視確認 | **3DS の画面更新が停止**。手動 Suspend |
| 5 | Suspend 後に読む | `state=-1` **`PC=0x4EB840` `LR=0x4E97A8`** |
| 6 | `del_bpt(0x4EB840)` → `continue` + `suspend` | `state=-1` **`PC=0x463E24`** — 正常に進行 |

**#2 と #3 は呼び出し内容もタイミングも同一で、違いは「bp を削除したか」だけ。**

### 結論

**`Use stepping support` の ON/OFF は関係ない。**
ヒットした bp を削除せずに再開すると、ON でも OFF でもゲームが停止する。
CLAUDE.md の「削除せずに再開するとフリーズする」は**そのまま有効**。

### ★フリーズの正体（#5 が示すもの）

手動 Suspend 直後の `PC` が **`0x4EB840`（bp 位置そのもの）** だった。
つまり**ターゲットは暴走していない。bp 位置に停止したまま一歩も進んでいない。**

説明（**仮説**。スタブの実装は見ていない — F-115）:
`BPT_SOFT` は元命令を trap 命令に差し替えている。
その位置から再開するには、**一旦 bp を外して元命令を 1 命令だけ実行し、
再び bp を戻す**（step-over-breakpoint）必要がある。
これを担うのが `Use stepping support`……ではなく、
**Luma3DS の GDB スタブ側にこの処理が無い**（あるいは効いていない）。
結果、再開要求は出るがターゲットは trap に再突入し続け、
外から見ると「フリーズ」に見える。

これは**「フリーズ」というより「bp 位置で永久停止」**であり、
だから bp を削除するだけで何事もなく復帰する（#6）。
「フリーズしても IDA から Suspend でき、bp を削除して再開すれば普通に動く」
という既知の挙動とも整合する。

### 実務上の扱い（変更なし）

同じ場所を繰り返し観測するときのサイクルは従来どおり:

**bp を削除 → 再開 → Suspend → 同じ位置に再設置**

### 副次的に確認できたこと

- `Scene_DrawLayers` の呼び出し元は `LR=0x4E97A8`（`sub_4E976C` 経路）で
  F-109 と一致。**再起動後も同じ経路**である
- F-105 の MCP 側 Suspend には**書き漏らしていた制約**がある:
  **走行中に外から自発的に止めることはできない。**
  `py_eval` の呼び出し自体が、ターゲットが停止するまでサービスされないため。
  F-105 の実験が通ったのは `continue` と `suspend` を**同じ呼び出しに束ねていた**から
  （＝呼び出しが停止中に開始していた）。
  したがって使い方は「`continue_process()` と `suspend_process()` を 1 回の
  `py_eval` に束ね、次の呼び出しで停止を確認する」に限られる。
  この形は #6 で実際に機能した

---

