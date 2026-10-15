---
id: ACNL-F0478
aliases:
- IDA-opus-5.5-F055
title: '村のアイテムの実体（fgobj）の辿り方とモデルの引き方（2026-09-27、MEDIUM: 静的のみ。gohan 165b571 で使用、実機未確認）'
summary: '解析ソフト: IDA（主 IDB）/ 解析モデル: opus-5.5。マップエディターの上画面（赤いハイライト・移動の複製）のため。設計 docs/topics/map_editor_3d.md（D004）。'
date: '2026-09-27'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9735792
- 5905040
- 5873972
- 3132320
- 5870292
- 4906308
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:1783-1795
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F055: 村のアイテムの実体（fgobj）の辿り方とモデルの引き方（2026-09-27、MEDIUM: 静的のみ。gohan 165b571 で使用、実機未確認）

解析ソフト: IDA（主 IDB）/ 解析モデル: opus-5.5。マップエディターの上画面（赤いハイライト・移動の複製）のため。設計 docs/topics/map_editor_3d.md（D004）。
- **実体の連結**: `fgobj::Proc`（`*0x948E70`）+13732（= +0x3400 +0x1A4）が先頭、次 = 実体 +8、マス = +40 / +44。`fgobj_DestroyObjectsAt 0x5A1A90`
  （呼び元 `FieldObj_FellObject 0x59A134` が `[0x948E70]` を渡す）と同じ辿り方。アイテム = +100、インスタンスのホルダ = +88（ノード = +92）。
- **実体のモデル**: `sub_58EEC0` → `ModelInstance_Create(obj+88, res, obj+32, obj+32, a6, a7, 1)`。一般のアイテム（`sub_58FB40` → `sub_58EEC0(…, 0, 0)`）は bufferOption 0。
- **モデルの引き方（sub_58FB40）**: 埋まっている（+2 の bit15、`Item_IsBuriedFlag 0x2FCBA0`）→ fg_crack_sand/soil(_s)（`sub_300A84(x, y, 0) == 1` で砂）、
  ID 158 → fg_hole_sand/soil、fgobj（≤0xFD）→ `Item_GetFieldObjDef` +12（≥0x87 は 0）→ `*(proc+0x414)` + 22n の +5 の名前 →
  `FieldSeasonResource_FindModel 0x5992D4`（= FindModel(proc+0x34)）、0x2000〜0x372A（`sub_2FCB40`）→ `sub_58E978`: ItemParam +11（≥0xAA は 0、`sub_76BE04` なら
  `sub_313654` で 9/8）→ `sub_5350C0(&n, byte_948E5F)` の名前 → FindModel(proc+0x13C)、`(ID & 0x6000) == 0x4000`（`sub_767930`）→ fg_wrapping(_out)。
- **材質の写し 0x4ADD44**: 写す元は M+8（資源）、割り当ては allocator の vtable +8、TEV は mask & 0x780（`TST R0,#0x780`）。TEV の +40 は mask 0x100 が無いと 0。
- 反証条件: 実機で赤がそのアイテムだけに付かない（材質の物体が体をまたいで共有）、複製が出ない（0x834 で季節資源から体を作れない）。

