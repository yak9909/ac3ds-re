---
id: ACNL-F0193
aliases:
- F-167
title: 'F-167: ★★★テキストのグリフは「定数から四角形を生成するシェーダ」で描かれる。頂点データが存在しない — `HIGH`（実機の batch を解読）'
summary: '適用: `scratchpad/decode_text_batch.py`'
date: '2026-08-28'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8388736
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:10026-10129
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-167: ★★★テキストのグリフは「定数から四角形を生成するシェーダ」で描かれる。頂点データが存在しない — `HIGH`（実機の batch を解読）

適用: `scratchpad/decode_text_batch.py`

### 1. 経緯

TODO-118 は「頂点属性 regs `0x200`-`0x22F` を確定する」だった。
batch のソース（`batch+0x10`、F-145）を PICA コマンドとして解読したところ、

**`reg 0x200`-`0x226`（頂点属性の設定）が 1 つも入っていなかった。**

代わりに**頂点シェーダの float 定数**でグリフの矩形を渡していた。
つまり **1 グリフ = 1 四角形を、頂点バッファなしで描いている。**

### 2. 1 グリフ分のコマンド列（`T_slsh` "/"、86 ワード）

```
reg 0x2B1 = 1
reg 0x111 = 1
reg 0x100 COLOROUTPUT_CONFIG = 0x00E40100
reg 0x101 BLEND_FUNC         = 0x76760000
reg 0x104 ALPHA_TEST         = 0x00000061
reg 0x0F8 TEXENV5 x5 (consec) = 0FF00FF0 / 0 / 00010001 / 0 / 0
reg 0x06F SH_OUTATTR_MODE mask=2 = 0x00000100
reg 0x080 mask=0 x3 = 0,0,0
reg 0x080 mask=B    = 0x00011001
reg 0x0D8 TEXENV3 x3 (consec) = 0EE30EE3 / 00000001 / 00010001
reg 0x0DC = 0
reg 0x0F0 TEXENV4 x3 (consec) = 0FE30FE3 / 00001000 / 00080008
reg 0x0F4 = 0
reg 0x08E TEXUNIT0_TYPE  = 0x0B          ← A4（アルファ 4bit）
reg 0x080 mask=4 = 0x00011001
reg 0x085 TEXUNIT0_ADDR1 = 物理 >> 3
reg 0x082 TEXUNIT0_DIM   = 0x00800080    ← 128 x 128
reg 0x083 TEXUNIT0_PARAM = 0x00000006
reg 0x2C0 = 0x80000006 ; reg 0x2C1 x4     ← 定数 c6 以降（1 グリフ 1 vec4）
reg 0x2C0 = 0x80000040 ; reg 0x2C1 x8     ← ★定数 c64 以降（1 グリフ 2 vec4）
reg 0x227 INDEXBUFFER_CONFIG = 0x80000000 ← offset 0、u16
reg 0x228 NUMVERTICES = 6                 ← 2 三角形 = 四角形 1 枚
reg 0x253 mask=1 = 1
reg 0x245 mask=1 = 0
reg 0x22E DRAWELEMENTS = 1
reg 0x245 mask=1 = 1
reg 0x231 = 1
reg 0x25E mask=8 = 0（2 回）
reg 0x253 mask=1 = 0
```

### 3. ★★定数 `c[0x40]` の意味を確定した

**`T_minute` の "29"（2 グリフ）を読んで、同じ文字列内の差分から確定した。**

| | u0 | v0 | u1 | v1 | 5 番目 | 6 番目 | 7 番目 | 8 番目 |
|---|---|---|---|---|---|---|---|---|
| "2" | 0.570312 | 0.601562 | 0.648438 | 0.414062 | **10.0** | **-24.0** | **-12.0** | -12.0 |
| "9" | 0.570312 | 0.406250 | 0.656250 | 0.218750 | **11.0** | **-24.0** | **0.0** | -12.0 |

UV 幅を texel に直すと

```
(0.648438 - 0.570312) * 128 = 10.0   ← 5 番目と一致
(0.656250 - 0.570312) * 128 = 11.0   ← 5 番目と一致
(0.601562 - 0.414062) * 128 = 24.0   ← 6 番目と一致（符号は負）
```

**したがって:**

```
c[0x40 + 2k]     = (u0, v0, u1, v1)        UV。0..1
c[0x40 + 2k + 1] = (幅, 高さ, X, Y)         レイアウト単位。高さは負（Y 下向き）
NUMVERTICES      = 6 * グリフ数
```

`T_slsh` "/" は `4.8 / 6.0 = 0.8`、`19.2 / 24.0 = 0.8` と比が揃うので、
**pane の 0.8 倍スケールが幅・高さに乗っているだけ**。UV は texel のまま。

X は "2" が -12、"9" が 0 なので送りは 12。Y は両方 -12。

`c[6 + k]` にもグリフごとに 1 vec4 ある（"/"→`(0,1,0,3)`、"2"→`(0,1,0,3)`、"9"→`(0,3,2,3)`）。
**意味は未確定。** インデックスやシート番号の類とみられる。

### 4. ★これが自前 GUI に与える影響

**「半透明の任意サイズ矩形」「SD から読んだ画像の描画」「自前ビットマップフォント」は、
頂点バッファを一切用意せずに書ける。**

必要なのは既存のコマンド列を複製して次を差し替えるだけ:

| 変えるもの | レジスタ／定数 |
|---|---|
| テクスチャの実体 | `reg 0x085` = 物理 >> 3（F-166 で確保方法は確立） |
| テクスチャの寸法 | `reg 0x082` |
| テクスチャの形式 | `reg 0x08E`（`0x0B` = A4、`0x00` = RGBA8 など） |
| フィルタ・wrap | `reg 0x083` |
| **UV と矩形** | **`c[0x40 + 2k]` / `c[0x40 + 2k + 1]`** |
| 枚数 | `reg 0x228` = 6 * 個数 と、定数を個数分 |
| 色 | `reg 0x0DB` / `reg 0x0F3`（F-157） |
| ブレンド | `reg 0x101` |

**TODO-118 の当初の前提（頂点属性を解析する必要がある）は外れていた。**
2D の矩形に関しては、その解析は不要である。

---

