---
id: ACNL-F0123
aliases:
- F-85
title: 'F-85: CameraCatalog、Catalog専用3灯、3つのrenderer layerはroom 0にも存在する'
summary: 'confidence: **MEDIUM**（各ctor/createとroom分岐、global renderer loopを静的照合）'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6876636
- 6875832
- 1639800
- 5150668
- 5184740
tags:
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:5116-5140
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-85: CameraCatalog、Catalog専用3灯、3つのrenderer layerはroom 0にも存在する

confidence: **MEDIUM**（各ctor/createとroom分岐、global renderer loopを静的照合）

`BsCamera_Ctor` (`0x68EDDC`) は全 `BsCamera+768` に `CameraCatalog` を構築し、
`BsCamera_CreateContexts` (`0x68EAB8`) はCatalog renderer context `+220`も初期化する。

`BsLightMgr_CreateRoomLights` (`0x190578`) は対応roomでroom固有lightを生成後、type `0x105`
`BsLightDiffuseCatalog`、`0x106` `BsLightAmbientCatalog`、`0x107`
`BsLightHemiSphereCatalog` を生成してactiveにする。room 0は除外されない。

global renderer初期化 `0x4E97CC` は3組のlayer objectを作り、frame処理 `0x4F1CE4` は全3組を処理する。
Catalog modelが使うindex 2は常設の第3 layerである。従って現在の屋外3D非表示は
Catalog camera、Catalog light、render passの欠落では説明できない。

初版adapterは `g_BsFtrMgr` 公開直後にselection cacheを1度だけ無効化する設計だった。
F-83の通りmanagerは未完了で、F-84の通り失敗後は同一品を再試行しないため、これは
manager生成に成功した後にも残る不具合である。第2版は
`(ownedManager[19] & 3) == 3` 後にcacheを無効化するよう修正したが、F-86/F-87の通り
manager自身がcreate phase中に即時失敗している。

詳細: `DOCS/furniture_rendering.md`

---

