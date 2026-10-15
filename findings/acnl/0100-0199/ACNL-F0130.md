---
id: ACNL-F0130
aliases:
- F-92
title: 'F-92: rev7は家具3Dには成功。壁紙・絨毯は非表示、服カテゴリは`ModelInstance_SetRenderLayer`でSIGSEGV'
summary: 'confidence: **HIGH**（家具表示結果とcrash PCを既解析の静的関数へ照合）、'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 3242960
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5311-5337
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-92: rev7は家具3Dには成功。壁紙・絨毯は非表示、服カテゴリは`ModelInstance_SetRenderLayer`でSIGSEGV

confidence: **HIGH**（家具表示結果とcrash PCを既解析の静的関数へ照合）、
**LOW**（服カテゴリで無効になった具体的なmodel pointerと原因。register/stack未採取）

第7版の連続試験では、家具は一通り3D表示された。一方、壁紙・絨毯などはpreviewに何も表示されず、
服カテゴリへ移動するとthread 220が `PC=0x00317BD0`、exc.code bのSIGSEGVで停止した。
ユーザーが解析作業を中断して3DSを電源断するため、今回のregister、stack、actor、選択Itemは採取していない。

`0x317BD0`は既に静的解析済みの `ModelInstance_SetRenderLayer` である。
`AcFtr_CreateFinalize`はCatalog mode 2でこの関数を呼び、g3d model instanceの各model entryに
render layer 2を設定して既存render keyを無効化する。従って今回は以前の
`PC=0xE1A04000`（無効vtable slot呼出し）とは別で、少なくともmodel finalize/layer設定段階まで
進んだ後の失敗である。

現時点では、次の二案を区別できない。

- 第7版の `0xBC..0xEB -> 0xBB` が家具には安全でも、服・mannequin系が必要とする派生actorの
  model/resource構造まで基底化してしまった。
- 屋外で生成した服previewのmodel instanceまたはentryが未初期化で、layer設定側が無効pointerを受けた。

いずれも仮説であり確定しない。第7版は「家具カテゴリで3D表示する実験版」としては成功したが、
全Catalogカテゴリ対応版ではない。次回は動的patchを進める前に、`CatalogPreview_UpdateActor`の
服カテゴリ変換、mannequin分岐、`AcFtr_CreateFinalize -> 0x317BD0`の引数生成を静的に追う必要がある。

---

