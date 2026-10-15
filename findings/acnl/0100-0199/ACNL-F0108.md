---
id: ACNL-F0108
aliases:
- F-70
title: 'F-70: 標準カタログの家具3Dは `BsFtrMgr` 経路。stock屋外はmanagerを生成しない'
summary: 'confidence: **HIGH**（生成経路と屋外許可は静的確認、室内オブジェクトは実機確認）、'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2206204
- 6884904
- 6888136
- 9382888
- 1639800
tags:
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:4667-4703
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-70: 標準カタログの家具3Dは `BsFtrMgr` 経路。stock屋外はmanagerを生成しない

confidence: **HIGH**（生成経路と屋外許可は静的確認、室内オブジェクトは実機確認）、
**MEDIUM**（屋外での実際の構図・照明品質は未試験）

F-69で `dword_94A6AC == 0` から標準カタログに3D系が不要とした範囲は広すぎた。
このグローバルは `OrderList` が使う特殊な `BsStrcCatalog` を示すだけで、通常 `FtrList` の
家具プレビューは別の共通経路にある。

`BsMenuCatalog::sub_21A9FC` (`0x21A9FC`) は選択品が変わると
`sub_690E28` (`0x690E28`) を呼ぶ。`vc_GET_CURRENT_CATALOG_ITEM` (`0x691AC8`) が返す
`g_CatalogPreview` は `+0=preview actor`、`+4=Item`。室内実機では actor=`0x3041E900`、
Item=`0x2EA3`だった。親は `g_BsFtrMgr=0x330BC474`、vptr=`0x008F2BE8`、
type=`0xEE` の `BsFtrMgr`。

生成時は `Item/Param/Item.bin` の30-byte record `+17`にある家具familyを読み、
固定表 `g_FurnitureActorTypeByFamily` から家具アクター種別を選ぶ。
`sub_57ADFC(type, g_BsFtrMgr, request, ...)` で `UiScreen_OpenById` を呼ぶ。
`sub_5B3A98` の拒否bit `0x10000` は村 room 0 (`flags=0x26`) と商店街 room 1
(`flags=0x206`) には無い。`BsFtrMgr` の容量表 `dword_8835BC` もroom 0に38枠、room 1に2枠を持つ。
ただしroom builderはflags bit `0x8` が立つ場合だけtype `0xEE`を含む室内共通groupを生成し、
room 0の固有type列にも `0xEE` は無い。容量値はmanagerの存在を意味せず、stock屋外の
`g_BsFtrMgr` はnullである。actor typeのfactory自体は実行ファイル内に固定登録されている。

`g_BsFtrMgr` が無ければ `sub_57ADFC` は0を返し、メニューは3Dなしで継続するため安全に縮退する。
`CameraCatalog` は共通 `BsCamera` の `+768` に内包され、独立した店内専用オブジェクトではない。

室内実機では `BsLightDiffuseCatalog` (type `0x105`, `0x3309BA0C`)、
`BsLightAmbientCatalog` (`0x106`, `0x3309BBDC`)、`BsLightHemiSphereCatalog`
(`0x107`, `0x3309BC50`) が全て存在しactive=1。追加静的解析で `BsLightMgr_CreateRoomLights`
(`0x190578`) がroom固有lightの後に3灯を生成すること、その経路へroom 0も到達することを確認した。
従ってCatalog専用3灯は店内scene限定ではない。CameraCatalogとglobal render layer 2も全room共通である。

詳細: `DOCS/catalog_outdoor.md`

---

