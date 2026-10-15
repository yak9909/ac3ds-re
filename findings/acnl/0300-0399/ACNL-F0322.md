---
id: ACNL-F0322
aliases:
- F-298
title: F-298 (HIGH・静的のみ) — ★TextBox 方式は実装可能。**自前フォントの「コード」はほぼ要らない**
summary: 利用者の指示で、基準仕様を詰める前に TextBox 方式の実現性を静的に判定した。
date: '2026-09-04'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9423532
- 9420796
- 9420924
- 7589704
- 9423420
- 1163567
- 7616692
- 7616360
- 5066412
- 5072240
- 7589752
tags:
- font
supersedes: []
source: v1:RE/FINDINGS.md:18973-19067
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-298 (HIGH・静的のみ) — ★TextBox 方式は実装可能。**自前フォントの「コード」はほぼ要らない**

利用者の指示で、基準仕様を詰める前に TextBox 方式の実現性を静的に判定した。

### 結論

**実装できる。** しかも F-294 が想定していた「自前 `nw::font::Font` 派生（26 スロット
vtable、24 個のスタブ + `GetGlyph`）を書く」必要はない。

`Font` の純粋仮想 24 スロットは **`ResFontBase` が全部実装済み**で、その実装は
**標準 BCFNT の FINF / TGLP / CWDH / CMAP を読むだけ**。
したがって **ゲームの `ResFont` vtable（`0x008FCAAC`）をそのまま自前オブジェクトに使い、
リソース構造だけ合成すればよい。** F-293 と同じ「コードでなくデータを書く」路線に乗る。

★`ResFontBase` と `ResFont` の 24 スロットは**完全に同一**（違いはデストラクタ 2 つだけ）。

### 番地（RTTI から。Picture `0x8FBFFC` が既知値と一致することで手順を検証済み）

| | |
|---|---|
| `nw::lyt::TextBox` vtable | `0x008FC07C` |
| TextBox `DrawSelf`（スロット 26 / +0x68） | `0x0073CF48` |
| `nw::font::Font` vtable（抽象） | `0x008FCA3C`（26 中 **24 が `__cxa_pure_virtual` = `0x0011C12F`**） |
| **`nw::font::ResFont` vtable** | **`0x008FCAAC`** |
| `ResFont::GetGlyph`（スロット 16） | `0x007438B4` |
| `ResFont::MapCharToGlyph`（CMAP） | `0x00743768` |

### 描画経路が実際に呼ぶ Font スロット

スロット 14（文字送り）/ 15（CMAP 引き）/ 16（GetGlyph）/ 19（baselinePos）/
23・24・25（`this+0x10` のビット）/ 2・3・4・6・18（FINF・TGLP の 1 バイトを返すだけ）/
7（`MOV R0,#2` = **文字コードは UTF-16**）。**どれも重い処理はしていない。**

### CMAP は方式 0（直接写像）が使える

```
CMAP+0 開始コード / +2 終了コード / +4 方式 / +8 次 / +12 先頭字形番号
方式 0: index = 先頭字形番号 + code − 開始コード
```

**ASCII `0x20`〜`0x7E` は CMAP 1 個で賄える。**
TGLP は標準 BCFNT の配置と完全一致（`cellWidth` / `cellHeight` / `baselinePos` /
`sheetSize` / `format` / `numColumns` / `numRows` / `sheetWidth` / `sheetHeight` /
シートデータ番地）。

### ★バッチ経路のテクスチャは `glyph+0` ではなく「シート記述子」から出る

`CharWriter_EmitGlyphQuad`（`0x4D4EAC`）は **writer+0x44（バッチ）が非 0 なら
44 バイトの記録を積むだけ**でテクスチャ設定をしない。TextBox はこちらの経路。
`TextBatch_BuildCommandStream`（`0x4D6570`）が記録の `+40`
（= `glyph+0x14` = `*(ResFont+0x0C) + 20 × シート番号`）から組む。

| 記述子（20 バイト） | 用途 |
|---|---|
| `+0x00` | GL テクスチャ名（**即時経路専用。バッチ経路では読まない**） |
| `+0x04` | オブジェクト。**その vtable +0x64 の戻り値が reg `0x083`（フィルタ）** |
| `+0x08` | reg `0x085` = テクスチャ番地（PA>>3） |
| `+0x0C` | reg `0x082` = (高さ<<16)\|幅 |
| `+0x10` | u8 reg `0x08E` = PICA 書式（9 = LA4） |

**いまの共有 texMap と同じ情報**で、配置が違うだけ。
**唯一コードが要るのは `+0x04` の vtable スロット 25 で、`MOV R0,#imm / BX LR` の 2 命令。**

### TextBox オブジェクト（264 = `0x108` バイト）

```
+0xD4  → 文字列（UTF-16）      +0xD8/+0xDC  上の色 / 下の色
+0xE0  → Font   ★0 なら即 return
+0xEC/+0xF0  文字の大きさ X / Y  +0xF4 → TagProcessor（0 で既定）
+0xFA  u16 文字数 ★0 なら即 return   +0xFC/+0xFD 整列   +0xFE dirty
+0x100 → Material ★0 なら即 return   +0x104 → バッチ構造
```

折り返し幅は **Pane の幅（+0x48）**が writer+0x4C に入る（高さは入らない）。

`DrawSelf` は Picture と同じく **自分でも `DrawCtx_FlushBatch` を呼ぶ**
（`0x73CF78`）。F-296/F-297 で見た作法と一致し、独立した裏付けになっている。

### 残る未確定（実装前に詰める）

1. **バッチ構造（TextBox+0x104）の全欄と、誰が確保するか**
   （容量 `+0x04` / 件数 `+0x06` / 済みビット列 `+0x0C` / コマンドバッファ `+0x10` /
   語数 `+0x1C`・`+0x28` / 記録は `+0x28` から 44 バイト刻み）
2. 記述子 `+0x04` のオブジェクト（2 命令スタブか既存流用か）
3. **アトラスの 1 画素余白**: `U = (cellWidth+1) × 列 + 1`。
   いまの 128x128・8px 詰めアトラスは**そのままでは合わない**ので作り直す
4. Material を Picture 用の共有 Material で代用できるか

### 容量

TextBox 1 本 264 バイト。文字列 10 本で 2,640 バイト + リソース一式（数百バイト）。
「1 文字 1 Picture」の 174 枚 × 352 = 61,248 バイトとは桁が違う。

詳細は `scratchpad/MEMO_f298_textbox.md`。**実機は触っていない。**

