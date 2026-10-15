---
id: ACNL-F0242
aliases:
- F-217
title: 'F-217: ★★★★SD から任意の画像を読む（TODO-130 完了）— `HIGH`（実機）'
summary: 3DS の GPU は **8x8 タイル + Morton 順**で、幅・高さは 2 の冪しか読めない。
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:13064-13120
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-217: ★★★★SD から任意の画像を読む（TODO-130 完了）— `HIGH`（実機）

### 変換は PC 側でやり切る

3DS の GPU は **8x8 タイル + Morton 順**で、幅・高さは 2 の冪しか読めない。
PNG をそのまま置いても描けない。
**展開器をプラグインへ持ち込むと失敗の仕方が増える**ので、
並べ替えと形式変換は PC で終わらせ、3DS 側は「読んで転送するだけ」にした。

`PATCHES/make_gui_image.py` — PNG を `.acgx` へ変換する。
**PIL は入っていないので zlib だけで PNG を読む**（8bit・非インタレース、
グレースケール/パレット/RGB/RGBA に対応）。
2 の冪でない画像は左上へ置いて余白を透明で埋め、UV をそのぶんに詰める。

### `.acgx` の形式

```
0x00  4  "ACGX"
0x04  2  版 = 1
0x06  2  テクスチャ形式（PICA reg 0x08E。0=RGBA8 / 9=LA4 / 11=A4）
0x08  2  幅（2 の冪）      0x0A  2  高さ（2 の冪）
0x0C  2  スプライト数（1〜14）
0x10  4  画素データの位置   0x14  4  画素データの長さ
0x20  スプライト表（1 件 16 バイト: s16 x,y,w,h + u16 u0,v0,u1,v1）
      UV は 0..65535 が 0.0..1.0。v は上が 1（F-194）
```

### プラグイン側

`/luma/plugins/00086200/gui_image.acgx` があれば読み、無ければ埋め込みのフォントで動く。

1. 頭を検査する（版・2 の冪・スプライト数・データ長がバッファに収まるか）
2. 画素データをバッファへ転送し `svcFlushProcessDataCache`
3. 描画ケーブの**寸法ワードと形式ワード**を差し替える
   （位置は `export` が `kGuiTexSizeWord` / `kGuiTexFmtWord` として出す。
   一意なヘッダ語 `0x000F0000|reg` を探し、その 1 つ前が値の語）
4. スプライト表の**位置・大きさ・アンカー・UV だけ**を書き換える。
   **`0x30` 以降は索引と配列内オフセットなので触らない。**
   使わない枠は幅・高さを 0 にして消す（ダミーと同じ扱い）

### 検証用の道具

- `PATCHES/apply_gui_image.py` — プラグインと**同じ手順**をデバッガから行う。
  作り直して再起動しなくても、形式と計算を実機で確かめられる。
- `PATCHES/export_caves.py` — **IDA 無しで**ヘッダを書き出す。
  書き出しは純粋な計算なのに、実機が走っていると `MODE="export"` すら
  実行できないのは理不尽だったので、偽の `ida_dbg` を差し込んで回避する。

### 制限

バッファは 0x4000 バイト（`Alloc(0x4000, 0x80)`）。
RGBA8 なら 64x64、LA4 なら 128x128、A4 なら 256x128 まで。
超えるものは変換ツールが警告する。


---

