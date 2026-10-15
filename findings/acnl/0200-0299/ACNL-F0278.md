---
id: ACNL-F0278
aliases:
- F-255
title: 'F-255: 自前 Layout ノードから実際に描けた。ロード画像より前面 — `HIGH`（実機・目視）'
summary: F-254 の空ノードに描画を載せた。`PATCHES/cave_node_draw.py`
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5670772
- 11376988
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:14983-15022
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-255: 自前 Layout ノードから実際に描けた。ロード画像より前面 — `HIGH`（実機・目視）

F-254 の空ノードに描画を載せた。`PATCHES/cave_node_draw.py`
（`cave_draw_topmost.py` を複製し、入口・画面選択・出口の 3 点だけ差し替えたもの）。

### 差し替えた 3 点だけで動く

| 箇所 | 旧（記録リストへ相乗り） | 新（自前ノード） |
|---|---|---|
| 入口 | `Layout_RecordPaneTree` の記録直後、`R4` = レイアウト | vtable `+0x08` として呼ばれ、`R0` = 自前ノード |
| 画面選択 | 「最後に再生されたレイアウト」と `R4` を照合 | **`ノード+0x134` の display**（`0x400`/`0x410`/`0x401`） |
| 出口 | `B 0x568774` | `MOV R0,#0` / `BX LR` |

マテリアル・UV セット数・テクスチャレジスタ・スプライトループ・色・フラッシュ・
カーソル書き戻しは F-206〜F-216 のものをそのまま使える。

### 実機で確認できたこと（利用者の目視）

- 上画面: `ACNL GUI OK`（緑、`I OK` は水色）／下画面: 同（白、`I OK` は赤）
- **ロード画像より前面。完全に最前面で常に描画された**
- → F-234（ロード画像に隠れる）と F-230（相乗り先ごとに座標系が違う）は**解消**

### 主リストの記帳（F-253 の続き。`mgr = *(0x00AD995C)`）

| フィールド | 意味 |
|---|---|
| `mgr[1]` (+0x04) | base |
| `mgr[3]` (+0x0C) | 現在のオフセット（`g_GpuCmdPtr - base`） |
| `mgr[5]` (+0x14) | **提出済み**のオフセット |
| `mgr[6]` (+0x18) | GX キューのエントリ配列（28 バイト/件） |
| `mgr[8]` (+0x20) | エントリ数 |

提出 = 「`addr = mgr[1] + mgr[5]` / `len = mgr[3] - mgr[5]` のエントリを 1 件作り、`mgr[5] = mgr[3]`」。
`GpuCmd_ReplayRecordedListRange` は冒頭で `mgr[5] != 現在オフセット` を見て、
**未計上の追記バイトを次のエントリへ畳み込む**。したがって主リストへ直接積んでも提出はされる。
ケーブでは書き戻し後に `mgr[3] = g_GpuCmdPtr - mgr[1]` を同期させ、
残量検査（`g_GpuCmdPtr + 0x2000 > g_GpuCmdEnd` なら描かない）も入れた。

---

