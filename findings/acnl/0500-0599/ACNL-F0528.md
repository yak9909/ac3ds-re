---
id: ACNL-F0528
aliases:
- IDA-opus-5.5-F003
title: 建物の高さは属性ブロックから。カタログ表示の読み込み手順（2026-09-23、MEDIUM（静的））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の指摘「建物配置における地面判定の高さ算出方法」に対する途中経過。'
date: '2026-09-23'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6972260
- 7099564
- 2260220
- 2259004
tags:
- catalog
supersedes: []
source: IDA:work/FINDINGS.md:3016-3048
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F003: 建物の高さは属性ブロックから。カタログ表示の読み込み手順（2026-09-23、MEDIUM（静的））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の指摘「建物配置における地面判定の高さ算出方法」に対する途中経過。

### 1. 地面の高さは当たり判定と同じ表にある

既知の `Field_TileToWorld 0x6A6364`（x = 32x+16、z = 32y+16、y = 地面の高さ、IDA-unknown-F023）の
`Field_GetGroundHeight 0x6C54AC(x, y, 部屋)` は、マスを「区画＋区画内の位置」に分けて
`sub_7520D8` で**区画の属性ブロック**（F001 / F002 と同じ 2,560 B）を引き、`sub_6A8C80` で高さを読む。
つまり**高さも当たり判定と同じ 10 B のマスに入っている**。建物の足元データが byte 0–7 を書いているのは
高さの情報の可能性が高い（橋が床を持ち上げるなど）。`sub_6A8C80` の読み方は未解明。

**村に建つ実物の位置を決める関数はまだ特定していない。** 実機で村に入る瞬間に
`Building_GetName` を止めて呼び出し元を見るのが速い（IDA-opus-5.5-T001 / T004）。

### 2. 公共事業のカタログ表示（村の実物ではない）

`Strc/fobj/%s/%s.bcres` を参照するのは `PwpPreview_LoadSlot 0x227CFC` だけで、これは
**2 枠を交互に使う表示用**（`PwpPreview_Update 0x22783C`、位置は ID ごとの表示変換 `sub_5C96B4` ＋ y に -7/-10）。
しずえの公共事業メニューの見本と推定。村に建つ実物は別の経路。

ただし読み込み手順はプレビューの実装にそのまま使える:

1. `Strc/fobj/<名>/<名>.bcres` と **`Strc/fobj/<名>/Textures/season00.bcres`（テクスチャは別ファイル）**
2. モデルの holder を `G3dResHolder_Setup(model, alloc, 0, 1)` のあと `Setup(model, alloc, テクスチャの holder, 1)`
3. `ModelInstance_Create(…, 0, 1, 1)`、マテリアル・スケルタルのアニメがあれば slot 0 へ結線
4. `ResModel_SetRenderLayer(…, 2)`

**モデルビューア（F035）はモデルの bcres しか読まないので、fobj はテクスチャが付かないはず。**
プレビュー（T002）では 2 本読む必要がある。

根拠: `acnl_jpn_v15_annotated.i64` の `0x6C54AC` / `0x6A6364` / `0x227CFC` / `0x22783C`。

