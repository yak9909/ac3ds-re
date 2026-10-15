---
id: ACNL-F0476
aliases:
- IDA-opus-5.5-F057
title: 'モデルの資源の Setup と後片付け — 自前の体を壊すと元の資源の LUT 参照が外れる（2026-09-28、HIGH: 静的＋停止中の実機の読み取り）'
summary: '解析ソフト: IDA（主 IDB を idalib-mcp で静的、停止中の実機を ida-pro-mcp で読み取りのみ）/ 解析モデル: opus-5.5。'
date: '2026-09-28'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4918356
- 3242328
- 4906308
- 4906696
- 4906732
- 5178684
- 4911752
- 4818456
- 4879224
- 4883600
- 5675844
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:1734-1764
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F057: モデルの資源の Setup と後片付け — 自前の体を壊すと元の資源の LUT 参照が外れる（2026-09-28、HIGH: 静的＋停止中の実機の読み取り）

解析ソフト: IDA（主 IDB を idalib-mcp で静的、停止中の実機を ida-pro-mcp で読み取りのみ）/ 解析モデル: opus-5.5。
gohan 7d3dff3 で「複製できないモデルを触ると落ちる」（利用者）。3 回のクラッシュ（F056 の 2 回を含む）はどれも 0x4B0C54 = 未解決の LUT 参照。
**原因は「未解決の資源」ではなく、こちらが外していた。**

- **資源の Setup（参照を結ぶ側）**: `G3dResHolder_Setup 0x317958` → `sub_4A5A74`（ResGraphicsFile::Setup。file +28 モデル / +36 テクスチャ / +44 LUT / +60 シェーダ / +76 / +84 / +100〜+132 アニメ…の辞書ごとに型別の Setup）→
  モデル `sub_4A91A4`（+196 形状 → `sub_4A9368`、+188 材質 → `sub_4A530C`、+180 メッシュ → `sub_4A8B44`）→
  材質 `sub_4A530C`: 旗 +24 の 0x100 テクスチャ（`sub_4A4AD4`）/ 0x80 シェーダ +644（`sub_4A4980`）/ 0x200 TEV +648 の参照表（`sub_4A68D4` → `sub_4A7554`）/ 0x40 済み。
  参照表は TEV +40 の 6 項目、項目 +8 → 参照。`sub_4A6A7C` が未解決（+12 = 0 か先の型語の bit31 = 0）なら `sub_4A6DFC` で名前（参照 +4 のファイル名・+8 の LUT 名）を引き、**参照 +12 に相対を書く**。
  見つからなければ 0x80000004 を返し、旗 0x200 は立たない。第 3 引数の holder を渡すとその資源（別の LUT ファイル）で引く（IDA-opus-5.5-F016 の `G3dResHolder_Setup(モデル, alloc, LUT holder, 1)`）。
- **体の作成（写しを作る側）**: `ModelInstance_Create` の bufferOption（mask）→ `sub_4AF068`（Material 88 B を作る）→ `sub_4ADBAC`（写しの配列 Material+12..+24）→ `gfx_ResMaterial_CopyForInstance 0x4ADD44`。
  写しは 728 B の本体と、mask 0x20 のテクスチャマッパー（`sub_4A6574` → `sub_4A87F0` / `sub_4A88EC`。**参照テクスチャ 0x20000004 ごと `sub_4A5900` で新しく作る**）、
  0x40 の +640、0x780 の TEV（244 B。0x100 が無ければ TEV +40 = 0）。**TEV を写さないとき +648 は 0**（0x4ADEC8 `MOV R0,#0` → 0x4ADEEC `STR R0,[R6,#0x288]`）。
- **体の破棄（後片付け）**: `ModelInstance_Destroy 0x4F053C` → …（体の dtor から材質の dtor までの中間は一段ずつは追っていない。実機の外れ方が「作って壊した体のモデルだけ」なのと一致）→ Material の dtor `0x4AF288`（vtbl_nw_gfx_Material）が写しの配列を全部 `sub_4AE2A4` へ →
  `sub_13B7EC`（写しの Cleanup。旗 0x40/0x200/0x80/0x100 を落とす）→ `sub_13F15C(写し +648 の TEV)` → `sub_140F6C(TEV +40 の表)` → 項目ごとに `sub_13F0F4` →
  型 0x40000000 なら `off_96F100` = **`sub_4A7420`: `MOV R1,#0 / STR R1,[R0,#0xC]`（参照を外す）**、0x80000000 なら `0x498618`。テクスチャマッパーは `sub_13F128` → `sub_4A87C8` → `sub_1375B8`
  （型で `off_96F118..` へ: 0x20000011 画像 = `0x4A7378` GPU メモリの解放、0x20000004 参照 = `0x4A8490` +0x1C = 0）。
  続けて `sub_4AE958(alloc, 写し +648 の TEV)` が表の各参照・項目・表・TEV を **alloc の vtable +12（Allocator::Free 0x569B44）で解放**する。
- **gohan の誤り**: 7d3dff3 までの MapEditor3D は写しの +648 に自前の TEV を繋ぎ、その +40 を**元の季節資源の表**（または gohan の .bss の全部 0 の表）へ向けていた。
  自前の体を壊すたびに元のモデルの LUT 参照が +12 = 0 にされ（さらに資源の中身を自前のヒープで「解放」）、ゲームがそのモデルを次に描いた所で 0x4B0C54 で落ちた。
  赤くできなかった体（途中の材質まで繋いだところで失敗）も壊すと同じことが起きる = 利用者の言う「複製できないモデルを触ると落ちる」。
- **実機の照合（読み取りのみ、`tools/dynamic/scan_res_bindings.py`、`work/evidence/map_editor/res_bindings_crash_7d3dff3.json`）**:
  季節資源 0x30C91E00（148 モデル、LUT 参照 287、参照テクスチャ 148）で外れていたのは **LUT 参照 10 個 = 5 モデル**（fg_bushA_2 / fg_bushC_2_bl / fg_grassC / fg_treeB_4 / fg_treeD_4_b）だけ。旗は全部 0x3D5（Setup 済み）。
  一般アイテム資源 0x30CE0E00（140 モデル、LUT 280、テクスチャ 140）は全部結ばれていた。gohan の s_slots[0]（生きている、壊していない）= fg_grassD は結ばれたまま、s_slots[1..4] は作って壊した跡。
  落ちた材質 0x30DC1BF4 の資源 0x30CC430C は fg_treeD_4_b の材質。テクスチャ参照は 1 つも外れていない（写しが自前の参照テクスチャを持つので静的とも一致）。
- **直し方（gohan d3438f5）**: 自前の体を壊す前に、材質ごとに写しの +648 を 0 に戻し（0x834 の写しなら 0 でない = 自前）、自前の TEV を Allocator::Free で返す。ゲームが写した TEV（mask 0x780）には書かない。
- **一本で追う方法**: どの物体（fgobj・家具・自前）が描いていても、モデルは ResGraphicsFile → ResModel → ResMaterial（+648 TEV → +40 表 → 参照 / +628.. マッパー → 参照テクスチャ）で同じ形。
  `scan_res_bindings.py` は file の辞書から全モデルを辿り、参照の結び付きを数える（`fgobj::Proc` +0x34 季節資源 / +0x13C 一般アイテムが既定、ほかは FILES_OVERRIDE）。
- 反証条件: d3438f5 でも自前の体を壊したあとに `scan_res_bindings.py` で外れた参照が出る、または 0x4B0C54 で落ちる。未確認: 家具・自前資源（BuildingPreview）での後片付けは自前資源なので実害が出ない（外れても次に使わない）と見ているが、実測していない。

