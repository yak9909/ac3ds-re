---
id: ACNL-F0292
aliases:
- F-269
title: 'F-269: TEV を自前で組んだ。**設計から借り物が消えた** — `HIGH`（静的のみ）'
summary: F-268 でマテリアルのテンプレートの符号化が全部割れたので、
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9942764
- 9942788
- 3145776
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16189-16270
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-269: TEV を自前で組んだ。**設計から借り物が消えた** — `HIGH`（静的のみ）

F-268 でマテリアルのテンプレートの符号化が全部割れたので、
借りた列（`MATCMD` に捕獲したもの）を**自分で組んだ列**に置き換えた。

### 出したい合成

自前アトラスは 64x64 の **LA4**（輝度 + アルファ）。求めるのは

```
出力.rgb = 頂点カラー.rgb × テクスチャ.rgb（= 輝度）
出力.a   = 頂点カラー.a   × テクスチャ.a
```

段 0 で合成し、**段 1〜5 は `PREVIOUS` の素通し**にする。
6 段すべてを明示するのが要点で、書かなかった段は
直前の描画が残した設定がそのまま効く（F-268）。

### 生成される 36 語（144 バイト）

書式はゲームのテンプレート（`0x97B6EC` / `0x97B704`）と同じ、
値ワード + ヘッダ `0x804F00xx`（mask `0xF` / extra 4 / consecutive）の 6 語バースト。

| 段 | reg | SOURCE | COMBINE | 意味 |
|---|---|---|---|---|
| TexEnv0 | `0x0C0` | `0x00300030` | `0x00010001` | `MODULATE(PRIMARY, TEXTURE0, PRIMARY)` |
| TexEnv1 | `0x0C8` | `0x0FFF0FFF` | `0x00000000` | `REPLACE(PREVIOUS, …)` |
| TexEnv2 | `0x0D0` | 同上 | 同上 | 素通し |
| TexEnv3 | `0x0D8` | 同上 | 同上 | 素通し |
| TexEnv4 | `0x0F0` | 同上 | 同上 | 素通し |
| TexEnv5 | `0x0F8` | 同上 | 同上 | 素通し |

`OPERAND` は全段 0（`SRC_COLOR` / `SRC_ALPHA`）、`COLOR` は白、`SCALE` は 1 倍。

各バーストは 6 語（値 1 + ヘッダ 1 + extra 4）で**偶数**なので、
PICA の 8 バイト境界は保たれる。

### 組み込み方（ケーブは 1 語も変えていない）

`MATCMD` を流す経路は「今フレーム捕まっていない」側（`usecopy`）に既にある。
そこは `LOG+LOG_CMDLEN` バイトぶんを `MATCMD` から流すだけなので、

1. 導入時に `MATCMD` へ自前 36 語を書き、`LOG+LOG_CMDLEN = 144` にする
2. `LOG+0x24` / `+0x28`（優先／予備マテリアル）を 0 にする
3. **マテリアル選定フック（`HOOK_P` → `CAVE_P`）を入れない**

これだけで毎フレーム自前の列が流れる。`OWN_TEV = False` に戻せば F-268 までの
「マテリアル捕獲」に戻る。**ケーブのコードは差分ゼロ。**

自前テクスチャレジスタ（`0x082` / `0x083` / `0x085` / `0x08E`）は
これまで通り **TEV の後**に積むので、ユニット 0 の結び付きは自前のアトラスになる。

### 検証

**ゲームのテンプレートを読んだのと同じ復号器**（`scratchpad/pica_decode.py` と同じ規則）で
生成語を読み直した。

- 6 バーストすべて `mask 0xF / extra 4 / consecutive 1`、想定外 0 件
- 36 語をきっかり消費して末尾一致
- 段 0 = `MODULATE(PRIMARY, TEXTURE0, PRIMARY)`、段 1〜5 = `REPLACE(PREVIOUS, …)`
- 144 バイト。`MATCMD` の容量 1024 バイト以内、ケーブの安全弁 `CMP R2,#0x400` 未満

監査: 総異常 0 件・重なりなし。

### ★これで自前ノードの GPU 状態は全部自前になった

| 状態 | 出所 | 決まった回 |
|---|---|---|
| 投影行列 | ノード `+0x34`（`SetupProjectionMatrix` を自分で呼ぶ） | F-265 / F-266 |
| 幅・高さ（scissor） | ノード `+0x28` / `+0x2C` | F-264 |
| ブレンド・色演算・深度 | Drawer の既定ブロック（全レイアウト共通・固定） | F-268 |
| **TEV 6 段** | **自前 36 語** | **F-269** |
| テクスチャユニット 0 | 自前 4 語（`0x082`/`0x083`/`0x085`/`0x08E`） | F-191 |
| 頂点・行列・幾何 | 自前（`DrawCtx_FlushBatch` 経由で uniform 6 番以降） | F-268 |
| 描画順 | 優先度 `0xFF` でリスト末尾＝最前面 | F-253 / F-254 |

**「他のレイアウトが何を残したか」に依存する要素は残っていない。**

**未適用。実機へは入れていない。**

---

