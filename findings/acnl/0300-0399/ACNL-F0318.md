---
id: ACNL-F0318
aliases:
- F-294
title: F-294 (HIGH・静的のみ) — ★自前フォントで `TextBox` を使えることを確認。`Glyph` 構造を確定
summary: 利用者の要望は「ゲームのフォントではなく**自前フォント**で描くこと」。**可能**である。
date: '2026-09-04'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9423420
- 9423256
- 9423532
- 9423648
- 7616692
tags:
- font
supersedes: []
source: v1:RE/FINDINGS.md:18728-18790
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-294 (HIGH・静的のみ) — ★自前フォントで `TextBox` を使えることを確認。`Glyph` 構造を確定

利用者の要望は「ゲームのフォントではなく**自前フォント**で描くこと」。**可能**である。

### nw::font のクラス構成（RTTI）

```
nw::font::Font          vtable 0x008FCA3C   ★26 スロット中 24 個が純粋仮想
  └ nw::font::ResFontBase  vtable 0x008FC998
      └ nw::font::ResFont   vtable 0x008FCAAC   ★24 個すべてを実装
nw::font::PairFont      vtable 0x008FCB20
nw::font::RectDrawer / TagProcessorBase<char|wchar_t>
```

`Font` は**抽象インタフェース**（`__class_type_info` = 基底なし、24 スロットが `__cxa_pure_virtual`）。
→ **自前の vtable を用意すれば、我々の Font を TextBox に渡せる。**

`ResFont` の実装を見ると、24 個のうち **20 個ほどは 8〜0x1C バイトの単純な取得子**
（`SetLineFeed` / `SetAlternateChar` / `SetDefaultCharWidths` / `HasGlyph` /
`GetGlyphSheetCount` など）で、**実質的な中身は `GetGlyph`（スロット 16、0x150 バイト）だけ**。

### ★`Glyph` 構造（`nwfont_ResFont_GetGlyph` 0x7438B4 より確定）

`GetGlyph(this, Glyph* out, u16 code)` が書く欄:

| オフセット | 中身 |
|---|---|
| `+0x00` | **テクスチャの番地**（TGLP のシート先頭 + シート大きさ × シート番号） |
| `+0x04` | CWDH の left bearing / glyphWidth（u16） |
| `+0x06` | CWDH の advance（u8） |
| `+0x07` | 行数関連（u8） |
| `+0x08` / `+0x0A` | シートの幅・高さ（u16） |
| `+0x0C` | セルの U = **(cellWidth + 1) × 列 + 1** |
| `+0x0E` | セルの V = **(cellHeight + 1) × 行 + 1** |
| `+0x10` | 書式（u16） |
| `+0x14` | シートごとの補助データ（`*(this+12) + 20 × シート番号`） |

**つまり自前 Font の `GetGlyph` は「文字コード → 我々のアトラスの番地・セル UV・幅」を書くだけ。**
アトラスは既に 128x128 LA4 で用意してあり、セル割りも 16x16 で確定している。

★注意: セル座標に **+1 の余白**が入る（`(セル幅+1) × 列 + 1`）。
nw::font のシートは**グリフの周囲に 1 画素の余白**を持つ前提。
自前アトラスをそのまま使うならこの式に合わせるか、`GetGlyph` 側で吸収する。

### 容量の比較（文字 270 個・矩形 30 個・文字列 20 本と仮定）

| 方式 | `.bss` | 追加コード |
|---|---|---|
| 旧（手書きループ＋表） | 26.1 KB | CAVE_Q 205 語 |
| **Picture 方式（F-293。いま動いている）** | **98.4 KB** | **0 語** |
| **TextBox ＋ 自前 Font** | **15.0 KB** | 自前 Font の stub（推定 60〜90 語） |

**Picture 方式は 1 文字ごとにオブジェクトが要るので容量が重い。**
TextBox なら 1 文字列 264 バイトで済み、**6.6 倍節約**できる。

### ★容量は別の手でも解ける

Picture は **CPU 側のただのデータ**で GPU 可視である必要がない。
アトラスと同じようにゲームのアロケータから借りれば `.bss` の 60 KB 制限は外れる。
**「TextBox に移る」以外に「Picture のままヒープから借りる」道もある。**

---

