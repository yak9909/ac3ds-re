---
id: ACNL-F0365
aliases:
- F-339
title: 'F-339（2026-09-07）: ★実機ゲート通過「1 本のバッチに複数の文字列」'
summary: '**confidence: HIGH**（実機で描画・画で確認）'
date: '2026-09-07'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21946-22001
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-339（2026-09-07）: ★実機ゲート通過「1 本のバッチに複数の文字列」

**confidence: HIGH**（実機で描画・画で確認）

全文 `scratchpad/MEMO_f339_gate.md`。道具は `PATCHES/textwriter_multi.py` と
`PATCHES/textwriter_multi_hw.py`（F-306 の 1 文字列ケーブを表駆動の繰り返しへ広げた 91 語）。

| # | 問い | 結果 |
|---|---|---|
| 1 | `ResetBatch` を挟まず `DrawString` を続けて 1 本のバッチに積み上がるか | **YES**（`batch+0x04` = 34 = 16+8+10） |
| 2 | 色は字ごとに効くか | **YES**。提出記述子は `0xFFFFFFFF` のままで**画面に 3 色出た**。効くのは**グリフ記録側** |
| 3 | 2 書体が 1 本のバッチで両方出るか | **YES。しかも群は分かれない** |

3 は F-337 の予想どおり。**2 つの記述子の `+0x08` が同値**（`0x045D81F0`）だった。
群を切る鍵は `記述子+0x08`（テクスチャの物理番地）なので、
**同じアトラスに載せている限り書体を混ぜても 1 群のまま・描画順も保たれる。**

### 記録の式が共有バッチでも成立

| 条件 | 実機 | 式 | 差 |
|---|---|---|---|
| 34 字・**単色・単書体** | **538 語** | `74 + 12*34 + 28*2` = 538 | **0** |
| 34 字・色 3 種・書体 2 種 | 630 語 | （色の項が無い） | +92 |

**切り替えの費用は 34 字・3 本で +92 語 = 368 B。** 内訳の分解はこれから。

### ★踏んだ落とし穴

1. **`BuildMatrix` は Y 列を反転する。**
   `world_y = ペインの平行移動Y − rec.cy` / `画面 y = 画面高/2 − world_y`。
   平行移動を `(-画面幅/2, +画面高/2)` に置けば **`cursorX = x` / `cursorY = y`**。
   最初 `cursorY = -(y+行送り)` にして画面外へ飛ばした。
   **正常な `TextBox` の `rec` と平行移動を読んで逆算した**のが決め手。推測で符号を決めない。
2. デバッガから生の番地を手で足して **writer のひな型を壊した**
   （`OFF_M + 0x300` = `0x18400` なのに `0x18300` と書いた）。
   **スクリプトが印字した番地を使うこと。**

### ★ケーブの検証手段（重要）

| 手段 | 結果 |
|---|---|
| `textwriter_cave.audit()` | 異常 0 件 |
| **objdump**（`--adjust-vma=0x00838540`） | 意図どおり。BL 9 本の飛び先すべて一致 |
| **IDA の逆アセンブラ**（書き込み後・輪へ繋ぐ前） | objdump と完全一致 |

★**idalib（`code.bin.i64`）ではケーブを検証できない。**
  静的 IDB の segment は **`0x00838020` より手前で終わっており**、
  `patch` が「Address not mapped」で拒否する（`get_bytes` は読めるので紛らわしい）。
  **ケーブの逆アセンブル検証は objdump + IDA（デバッグ側）で行う。**

### 実機の後片付け

§5.3 の順序で戻し、**nw::lyt 1,331,224 B / nngx 1,220,172 B と素の値へ完全復帰**（差 0）。

---

