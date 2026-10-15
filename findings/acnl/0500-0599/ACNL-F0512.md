---
id: ACNL-F0512
aliases:
- IDA-opus-5.5-F019
title: 物を置ける／花を植えられる属性の表と、それで決める建物の衝突判定（2026-09-24、MEDIUM（静的）。定義は利用者）
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の定義「物を置けない範囲、または花を植えられない範囲。それが 1x1 以上ならそれ、0x0 ならバッファを一回り削った範囲」。'
date: '2026-09-24'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1463368
- 3145996
- 6083440
- 5857412
- 3141540
- 6083932
- 5857260
- 6083956
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2440-2457
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F019: 物を置ける／花を植えられる属性の表と、それで決める建物の衝突判定（2026-09-24、MEDIUM（静的）。定義は利用者）

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の定義「物を置けない範囲、または花を植えられない範囲。それが 1x1 以上ならそれ、0x0 ならバッファを一回り削った範囲」。

- `Field_CanPlaceItemAt 0x165448(x, y, room, mode, …)` の属性判定はモードで分かれる:
  - mode 0 → `Field_CanDropItemAt 0x30010C` → **`FieldAttr_CanPlaceItem 0x5CD370` = (byte_957D32[code] & 2) >> 1**。`Player_DropItem 0x596084`（通常ドロップ 0x0A）が使う
  - mode 1 → `Field_CanPlantFlowerAt 0x2FEFA4` → **`FieldAttr_CanPlantFlower 0x5CD55C` = byte_957A35[code]**。`Player_PlantFlower 0x595FEC`（種別 0x0C 花を植える）が使う
  - mode 2 → `Field_CanLayDesignAt 0x5CD574`（byte_957D32 & 4 と地形。種別 0x0D、LOW）
  - どれも先に「上 2 マスの属性が 3 か」を見る（地形。建物の足元の判定には使わない）
- 足元の主なコード: 0x02/0x03/0x04（本体）置けない・植えられない、0x05（外周）置けない・植えられる、0x11/0x17 置ける・植えられない、
  0x31/0x32/0x33 どちらもできる、0xA0/0xA2〜0xA5 どちらもできない
- 結果: ベンチ 4x3、街灯 3x3、噴水 5x5、柵 7x6、交番 10 マス（本体 3x3＋入口）、南北の橋 12 マス（橋板＋四隅）。
  置けない・植えられないマスが 1 つも無いのは 4 種（dobj_dummy / dobj_livehouse / sobj_buoy / sobj_crossing）で、これらは範囲を一回り削る
- F017 の byte_957B34（FieldAttr_CollisionClass）は利用者の確認で「一部が違う」とされ、今回の定義に置き換えた

実機（2026-09-24、読み取りのみ）: 親ヒープの空き 208 KB（UnitCursor 40 体）。1 体 6,083 B を実測（instance ヒープの残りから）。
プレビュー（交番 ≒ 200 KB）は F018 の 128 KB の余白で断られていた → 余白 48 KB、UnitCursor は小さい形に戻れば減らす（gohan `9386db9`）。

