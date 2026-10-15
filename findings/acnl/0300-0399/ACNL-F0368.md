---
id: ACNL-F0368
aliases:
- F-342
title: 'F-342（2026-09-07）: 共有バッチの設計 — ★費用の 8 割は「コマンド語の器の取りすぎ」'
summary: '**confidence: HIGH**（静的解析 + 実機で確認。設計の数字は `PATCHES/design_shared_batch.py`）'
date: '2026-09-07'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5067156
- 5066412
- 5072240
- 5067276
- 5070000
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:22149-22208
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-342（2026-09-07）: 共有バッチの設計 — ★費用の 8 割は「コマンド語の器の取りすぎ」

**confidence: HIGH**（静的解析 + 実機で確認。設計の数字は `PATCHES/design_shared_batch.py`）
根拠: decompile（`ResetBatch 0x004D5194` / `EmitGlyphQuad 0x004D4EAC` /
`BuildCommandStream 0x004D6570` / `CopyToCommandBuffer 0x004D520C` /
`EmitStatePrefix 0x004D5CB0`）+ memory 値 + 画面
詳細: `scratchpad/MEMO_f342_design.md`

### 発見

ゲームは `TextBox` のバッチを `(78n + 57) & ~3` 語（**1 字 312 B**）で取るが、
F-341 の式で実際に積まれるのは **1 字 12 語 = 48 B**。

```
28 字のスロット: ゲーム流 2240 語 = 8,960 B  /  実際 478 語 = 1,912 B  → 4.7 倍
```

**器の大きさ `batch+0x20` は描画にも提出にも一切読まれない**
（上の 5 関数を全部読んで確認）。だから自前で詰められる。

### 3 案の収支（`GuiV2.cpp` の現状 上 63 本 756 字 / 下 11 本 116 字）

| 案 | 領域計 | 借用比 | 上画面の記録 | 通知の上限 |
|---|---|---|---|---|
| A いまのまま | 351,904 B | 79.6% | 84,848 B | **5 件** |
| **B 器だけ詰める** | **143,952 B** | **32.5%** | 84,848 B | **12 件** |
| C 連続する文字列のかたまりごとに共有バッチ | 101,744〜107,840 B | 23〜24% | 63,648〜66,176 B | さらに上 |

**案 B だけで Simulator の 7 件を超える。** 描画の作りを一切変えないので危険が小さい。

### ★共有バッチ（案 C）の制約 — 重ね順

輪は**描画順そのまま**に組んでいる（`GuiV2.cpp` の `st.oKind`/`st.oIdx` を順に積む）。
矩形と文字が交互に並ぶので、**全文字を 1 本のバッチにまとめると重ね順が壊れる**
（後から描く帯がその帯自身の文字まで覆う）。
案 C の単位は「画面 1 本」ではなく**表示リスト中で連続する文字列のかたまり 1 つ**。
8〜16 本/画面で足りる見込み。1 本の固定費は 376 B（`TextBox` の 488 B より小さい）。

### 実機で確かめた（案 B）

`ui_font_hw.py` の `TIGHT_CMD` で器だけ詰め、`TextBox` 4 本（7/16/17/33 字）を描画。

| | 器ゲーム流 | 器を詰めた |
|---|---|---|
| バッチ実寸 4 本計 | 25,616 B | **8,240 B** |
| 語数 | 158/266/306/526 | **同一** |
| 記録長 | 5,792 B | **同一** |
| 画 | 正常 | **正常** |

### プラグインへ入れた（第 1 段）

`GuiV2.cpp` に `BatchCmdWords(n) = 46 + 12n + 28*ceil(n/16) + (f==1?20:40) + 32` を新設し
`BatchSize()` の器の項を置換。`WriteBatch()` は `batch+0x06 = n`（二重の弁）も書く。
`verify_plugin_port_v2.py` 群 4 が C++ の係数と「使う語数 <= 器」を検査する。

**配置 438,784 B -> 231,552 B（借用 0x6C000 の 99.2% -> 52.3%）。検証器は異常 0 件。**
★借用の値はまだ変えていない（空いた 207,296 B の使い道は利用者の判断）。

---

