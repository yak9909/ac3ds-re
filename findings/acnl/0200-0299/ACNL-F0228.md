---
id: ACNL-F0228
aliases:
- F-203
title: 'F-203: ★★★★★最後に再生されるレイアウトは固定。注入点が確定 — `HIGH`（実機 301 フレーム）'
summary: '`PATCHES/probe_layout_order.py`。'
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5669596
- 5670768
- 5670612
- 5670616
- 1260132
- 9894968
- 5075300
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:12483-12547
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-203: ★★★★★最後に再生されるレイアウトは固定。注入点が確定 — `HIGH`（実機 301 フレーム）

### 1. 観測（読み取りのみのプローブ）

`PATCHES/probe_layout_order.py`。
`ssys_ma_lyt_Layout_ReplayRecordedList`（`0x5682DC`）の入口で `R0`（レイアウト）を記録し、
`Render_FrameEnd` で「そのフレームの最後の 1 つ」を拾う。

| 項目 | 結果 |
|---|---|
| 総フレーム数 | **301**（10 秒。30fps と一致） |
| 最後に再生されたレイアウト | **常に `0x32C4CBCC`（リスト id 8）** |
| **基準と違ったフレーム数** | **0** |
| 1 フレームの再生数 | **15 / 19 / 40 と変動**（場面による） |

**メニュー開閉を 2〜3 回挟んでも、最後の 1 つは一度も変わらなかった。**

★**リングは直近 16 フレームしか残らない**ので、それだけでは「安定」と言えない。
**全フレームを監視するカウンタを併用して初めて確定できた。**

### 2. ★★注入点 — `0x568770` の NOP

`ssys_ma_lyt_Layout_RecordPaneTree`（`0x5686D4`）の中核:

```
0056876C  BL nwlyt_DrawPaneTreeToCurrentList   記録本体
00568770  NOP    ★ここを分岐に置き換える（元命令を潰さない）
00568774  NOP
00568778  BL sub_133A64
...
0056879C  BL GpuCmd_CommitListAndCaptureDelta  長さを確定
```

**この時点で揃っているもの:**

| 条件 | 状態 |
|---|---|
| レイアウトのポインタ | **`R4`**（`0x5686D8` の `MOV R4,R0`） |
| 選択中のリスト | **そのレイアウト専用のリスト** |
| **UI の GPU 状態** | **確立済み**（F-202 で欠けていた条件） |
| カーソル | `g_GpuCmdPtr`（`nwlyt_DrawPaneTreeToCurrentList` が書き戻す） |
| 記録長の確定 | **この後**（`GpuCmd_CommitListAndCaptureDelta`）なので追記が反映される |

**`NOP` を潰すだけなので、移設が必要な元命令が無い。**

### 3. `R0` は気にしなくてよい

直後の `sub_133A64`（`0x133A64`）は **引数を無視**して `*(0x96FC38)` を返すだけ。

```
LDR R0, =0x96FC38 ; LDR R0,[R0] ; BX LR
```

また `GpuCmd_GetCurrentWritePtr`（`0x4D7164`）は `return g_GpuCmdPtr` そのもの。
**F-200 の「レイアウトの境目では cursor はグローバル」が改めて裏付けられた。**

### 4. 対象の見分け方

レイアウトのポインタは起動ごとに変わるので、**`*(layout + 256) == 8`（リスト id）**で判定する。
これが起動をまたいで安定かは**未確認**。実装では「一致しなければ何もしない」ので、
外れても安全側に倒れる。


---

