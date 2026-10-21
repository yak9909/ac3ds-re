---
id: ACNL-F0731
aliases: []
title: "タイトルの地は16角の2画像を6枚のPictureで重ね、150フレームで動かす"
summary: "opng_titl_bgの実資源はA4/L4の16×16各128 Bを6枚のPictureで共有する。明示TEV段は0、各材質の画像は1枚、4層のUVと親の位置を150フレームで動かす。"
date: 2026-10-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: "全関数export・RomFS・公開ソース"
addresses: [0x004BCEA8, 0x0073B650, 0x004B541C, 0x004B9830]
tags: ["layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

更新側タイトルの地は2枚の小画像を6枚のPictureで共有し、SRTと親位置で動かす。画像150枚や6テクスチャの単一マテリアルではない。
確度 MEDIUM：実DARC/BCLYT/BCLANの独立した画像・ペイン・材質・キー列と、ゲームの材質読込/UV計算/CLTS適用命令を照合。実画面との再照合なし。

## 根拠

一次証拠は `_local/evidence/107/arcs.json`、`layouts.json`、`title_animation.json`、`assets.py`、`layouts.py` と同所の展開 `assets/opng_titl/`。元資源と内包ファイルのSHA256はarcs.json。コードは `0x004bcea8.txt`、`0x0073b650.txt`、`0x004b541c.txt`、`0x004b9830.txt`、出所はexports.json。

- 更新側 `Layout/Title/opng_titl.arc` は216,872 B。`my_opn_bg_00.bclim` と `_01` は各168 Bで、画素128 B + footer40 B。寸法16×16、BCLIM/nw::lyt書式13=A4、12=L4（GPU書式11/10とは別）。この変換はTexMap生成命令と公開GPU enumを照合した。
- `opng_titl_bg.bclyt` のtxl1はこの2名のみ。6つの材質はflags0x15（画像/SRT/座標生成各1、TEV0、独自alpha/blendなし）。wrap/filterのbytesは5/5で、コードを介すとRepeat/Linearになる。

| 描画順 | ペイン | 画像 | Pane alpha | SRT scale | 寸法 |
|---|---|---|---:|---|---|
| 1 | P_bg_00 | L4 `_01` | 255 | 11,8.5 | 352,272 |
| 2 | P_bg_01 | A4 `_00` | 70 | 11,8.5 | 352,272 |
| 3 | P_bg_02 | A4 `_00` | 70 | 11,8.5 | −352,272 |
| 4 | P_bg_03 | A4 `_00` | 70 | 11,8.5 | 352,−272 |
| 5 | P_bg_04 | A4 `_00` | 70 | 11,8.5 | −352,−272 |
| 6 | P_filter | A4 `_00` | 55 | 160,120 | 352,272 |

- P_bg_00の材質二色はRGBA `(253,172,101,255)` / `(231,238,103,255)`。P_bg_01…04の頂点色は `(0,246,255,255)`、filterは白。これはタイトルの原色であり、別の二色化処理の式ではない。
- loop資源のpai1はframeSize150・loop1。P_bg_01…04はSRTのtranslate S/Tをともに0→1（frame0→150）のHermiteキーで動かす。同時に親N_setのtranslate Xを16→−16へ動かす。動きはUVだけではない。
- 最初の5層の幾何/SRTから名目の反復幅高は32 px。一方filterは352/160、272/120で異なる。**2枚が16角だから最終6層も16角の単一タイルへ無損失に縮められる、とまではいえない**。
- arc全体には47枚のBCLIM・画素184,128 Bがある。2つの背景画素256 Bのためにarc全体や全timgを維持する費用と、既存256 Bの画素だけを参照する費用は違う（[ACNL-F0728]）。タイトル終了後の所在は別途確認が必要。

公開資料 `STUDY107_PUBLICS`： [Clypo](https://github.com/pleonex/Clypo)、[bclimtool](https://github.com/dnasdw/bclimtool)、[3dbrew CLYT](https://www.3dbrew.org/wiki/CLYT_format) は形式の照合に使用。今回の個数・キー・色はゲーム資源を直接読んだ値。

## 反証条件・未確認点

- タイトルの原描画を緑へ変換したCPU実装、150コマのatlas配置、描画寸法・フィルタまで同じかは未確認。別の地にタイトル原色をそのまま当てたときの見た目を保証しない。
- 更新前/baseとの差分を全調査した記録ではない。現在の資源選択は更新に存在すれば更新を採る前提。生DARCと各ファイルのハッシュを保存した。
