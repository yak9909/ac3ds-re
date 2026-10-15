---
id: ACNL-F0618
aliases:
- IDA-opus-5.5-F102
title: 'ACNL の部屋の家具の持ち方と「かざる」「拾う」の入口（2026-10-06、LOW〜MEDIUM: 静的 + 先行資料。途中）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。T022 の ACNL 側の下調べ。'
date: '2026-10-06'
category: item
build: acnl_jpn_v15
confidence: LOW
tool: IDA
addresses:
- 6877632
- 8712004
- 2467728
- 6780328
- 6780344
- 7774132
- 2555304
- 5137620
- 5112652
- 6684700
- 8066088
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4805-4818
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F102: ACNL の部屋の家具の持ち方と「かざる」「拾う」の入口（2026-10-06、LOW〜MEDIUM: 静的 + 先行資料。途中）

解析ソフト: IDA / 解析モデル: opus-5.5。T022 の ACNL 側の下調べ。
- セーブの部屋（Vapecord GameStructs.hpp の ACNL_Room、0x302 B。**未裏取り = LOW**）: RoomFlags 0x22 B → 点灯の旗 0x20 x 2 → **RoomItems[100]**（4 B = Item）→ 家具の上の **[64]** → **Wallpaper / Flooring / 曲 / 予備**。家 = ACNL_PlayerHouse（中央・2 階・地下・右・左・奥の 6 部屋）。
  実行時の部屋（Vapecord House.hpp RoomData 0x12D0 B、LOW）: 当たり collision[0x500]（+0x90）、家具 furnitureInRoom[256]（+0xAA8）、furnitureOnFurniture[256]（+0xEC0）。
- 模様替え UI（ModuleIndoor）が使う ModuleFtr の窓口 27 本（work/cache/cro_elf/ModuleIndoor.imports.json）。既知: +0x6E44 移動、+0x7108 離したとき置く／戻す、+0x8D8C 1 個の移動音。
  ModuleFtr のチップの一覧 = 0xB480D4（.bss）の 112 個 x 32 B（+4 = 本体の家具オブジェクトの参照、+8 = もう 1 つの参照、+25〜+28 = 状態のバイト）。空きへの登録 `sub_B1CF44`（ModuleFtr）。家具の実体は本体（AcFtr_* / BsFtrMgr_PopulateRoom 0x68F1C0）。
- 持ち物の画面の「へやにかざる2」（状態表 0x84EF44、calc 0x25A790）: `sub_259EC4(…,12,1)` のあと、選んだ操作を表 off_949F80 から引いて呼ぶ。実際に置く処理は未。
- `Player_TryPickUpFurniture` 0x6775A8（命名、MEDIUM）: ポケットの空き（Inventory_FindEmptySlot）・目の前の家具の番号（sub_6907E0）→ Actor_SetState(0x43) かメッセージ。Vapecord の PICKING_UP_FURNITURE（0x6775B8）はこの中の判定の差し替え。
  同 PLACING_FURNITURE1〜3 / MOVING_FURNITURE も「置けるか」の判定の差し替え先（0x769FB4 / Item_CanPlaceHere 0x26FDA8 / 0x4E64D4 / 0x4E034C）で、置く処理そのものではない。
- `Player_TryPickUpItemAt` 0x66001C（命名、MEDIUM）: 拾うのは家具専用ではなく汎用の「マップの品物」の処理（`Field_GetMapManager` → `Field_GetItemAtXY(管理, x, z, 層)`。層 0 = 床、1 = 家具の上）。**家の家具は部屋のマップの品物として持たれている**（屋外の落とし物と同じ持ち方）。状態 0x43 は中身の無い状態（全欄 0x7B1428）。
- 未確定（実機で確かめる）: 部屋のマップの品物を書き換えたとき、家具の表示（BsFtrMgr / AcFtr）が追従するか。屋外の Field_MarkDirty（F005）は fgobj のビットマップの仕組みで、家の中には無い。
- 次: 上の実機試験、置く本体（sub_660348 の続き・家具の上に置く経路）、壁紙・床紙を替えて反映させる処理、部屋のマスと家具の大きさの表（ItemParam+23 & 0xF、F050）。

