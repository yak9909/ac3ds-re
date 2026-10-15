---
id: ACNL-F0122
aliases:
- F-84
title: 'F-84: Catalog actor typeはItemParam由来。`AcFtr` はbank確保、model非同期読込、layer 2登録の3 phase'
summary: 'confidence: **MEDIUM**（Item.bin loader、family table、AcFtr vtableと各phaseの静的照合）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5460360
- 6884904
- 5692964
- 5692132
- 5690988
- 5178508
- 3242960
tags:
- catalog
- model
supersedes: []
source: v1:RE/FINDINGS.md:5098-5115
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-84: Catalog actor typeはItemParam由来。`AcFtr` はbank確保、model非同期読込、layer 2登録の3 phase

confidence: **MEDIUM**（Item.bin loader、family table、AcFtr vtableと各phaseの静的照合）

`ItemParam_GetRecord` (`0x535188`) は `Item/Param/Item.bin` の30-byte recordを返す。
record `+17` の家具familyを `g_FurnitureActorTypeByFamily`へ通し、固定type `0xBB`～`0xEB`を得る。
86 entryのfactoryは実行ファイル内にあり、現在room descriptorやCRO登録からtypeを選ぶ処理ではない。

`CatalogPreview_UpdateActor` (`0x690E28`) は生成を試す前に `g_CatalogPreview+4` のcacheを更新する。
失敗/null actorでも同一選択を再試行しない。`AcFtr_CreatePrepare` (`0x56DE24`) はmanager bankと
scene handleを確保し、`AcFtr_LoadResources` (`0x56DAE4`) はbankの96KB CPU heapを使って
`Item/Model/%s.bcres`、必要なmaterial/jewel/remake textureを非同期で読む。
CPU heapがnullならモデルを読まずreturn 2へ安全縮退する。

`AcFtr_CreateFinalize` (`0x56D66C`) はmaterialをbindし、`ModelInstance_Create` (`0x4F048C`) で
g3d model instanceを作る。Catalog mode 2は `ModelInstance_SetRenderLayer` (`0x317BD0`) で
各model entryのlayerを2へ設定する。破棄phaseはmodel/resource、scene handle、bank handleを解放する。

