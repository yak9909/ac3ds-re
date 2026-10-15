---
id: ACNL-F0137
aliases:
- F-99
title: 'F-99: 描画解析の再精査 — 数値変換 2 件とレジスタ名 3 件の誤りを訂正'
summary: 'confidence: **MEDIUM**（機械的な検算は確実だが、`registers.h` は `REFERENCES/` 配下＝一次情報ではない。F-101 で訂正）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5791-5869
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-99: 描画解析の再精査 — 数値変換 2 件とレジスタ名 3 件の誤りを訂正

confidence: **MEDIUM**（機械的な検算は確実だが、`registers.h` は `REFERENCES/` 配下＝一次情報ではない。F-101 で訂正）

### ★資料が repo 内にあった

**`REFERENCES/CTRPF PROJECTS/FOXXY/Includes/ctrulib/gpu/registers.h`**
に **724 個の `GPUREG_*` 定義**がある。FOXXY の同梱 ctrulib。
**これを使わず記憶でレジスタ名を書いたのが誤りの原因。**

### 誤り 1: 16 進変換を暗算して 2 件間違えた

| 定数 | 誤った記載 | 正しい値 |
|---|---|---|
| `983491` | `0x000F0083`（TEXUNIT0_PARAM） | **`0x000F01C3`**（reg `0x1C3`） |
| `262596` | `0x00040284` | **`0x000401C4`**（reg `0x1C4`） |

CLAUDE.md の「数値・アドレス変換を暗算しない」を破っていた。

### 誤り 2: レジスタ名を記憶で書いて 3 件間違えた

| reg | 誤った記載 | `registers.h` の正解 |
|---|---|---|
| `0x105` | BLEND_FUNC | **`GPUREG_STENCIL_TEST`** |
| `0x107` | BLEND_COLOR | **`GPUREG_DEPTH_COLOR_MASK`** |
| `0x110` | EARLYDEPTH_CLEAR | **`GPUREG_FRAMEBUFFER_INVALIDATE`** |

正しかったもの: `0x010` FINALIZE / `0x06D` DEPTHMAP_ENABLE /
`0x111` FRAMEBUFFER_FLUSH / `0x25E` PRIMITIVE_CONFIG /
`0x149` を「ライト別 `+16*i`」と読んだ推論（`GPUREG_LIGHT0_CONFIG` で正解）。

### ★結論も変わる: `SimpleMaterialActivator` はライティング設定が主体

正しく引き直すと積んでいるのは:

| reg | 名前 |
|---|---|
| `0x08F` | `GPUREG_LIGHTING_ENABLE0` |
| `0x1C6` | `GPUREG_LIGHTING_ENABLE1` |
| `0x1C3` | `GPUREG_LIGHTING_CONFIG0` |
| `0x1C4` | `GPUREG_LIGHTING_CONFIG1` |
| `0x149` | `GPUREG_LIGHT0_CONFIG`（`+16*i`） |
| `0x0E0` | `GPUREG_TEXENV_UPDATE_BUFFER` |
| `0x080` | `GPUREG_TEXUNIT_CONFIG` |
| `0x105` / `0x107` | `GPUREG_STENCIL_TEST` / `GPUREG_DEPTH_COLOR_MASK` |
| `0x06D` | `GPUREG_DEPTHMAP_ENABLE` |

**「テクスチャユニットを設定している」という当初の読みは誤りで、
実体はフラグメントライティングの設定が主体。**

### ★`sub_4DE7F4` の正体も確定

| reg | 名前 |
|---|---|
| `0x2C0` | `GPUREG_VSH_FLOATUNIFORM_CONFIG` |
| `0x2C1` | `GPUREG_VSH_FLOATUNIFORM_DATA`（extra=11） |

**頂点シェーダの float ユニフォーム転送**だった。
併せて `sub_148E94(dst, src, header)` が
**「ヘッダ + 連続データ」を積むヘルパ**であること、
値の bit31 が**連続書き込みモード**の印であることも判明。

### ヘッダ形式の理解の補強

`header = reg | (mask << 16) | (extra << 20) | (consec << 31)`

- **`mask` は 1/2/4/5/8/0xF と多様**（0xF 固定ではない）
- **`extra` は後続の追加ワード数**。一括転送はこれを使う

### 今回の精査で妥当と確認できたもの

- GSP スタブ 6 本の引数対応（`WriteHWRegs(pSession, addr, data, size)` 等）
- `g_GpuCmdPtr` / `GpuCmd_Advance` / `GpuCmd_GetProperty`
- `GpuCmd_SplitAndSubmit` の終端 4 コマンドの**構成**（名前だけ誤っていた）
- `GX_SetCommandList` / `GX_SetDisplayTransfer`
- RTTI による継承関係（`nw::lyt::Drawer` ← `nw::font::RectDrawer` ほか）

---

