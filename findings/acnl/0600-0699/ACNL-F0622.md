---
id: ACNL-F0622
aliases:
- IDA-opus-5.5-F106
title: '家の部屋の壁紙・床をその場で替えるゲーム自身の手順（2026-10-07、MEDIUM: 静的 2 経路。実機未確認）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。T022 の壁紙・床紙リストの前提。主 IDB に命名・注記・保存済み。'
date: '2026-10-07'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9357084
- 2643028
- 2910584
- 5408028
- 5407508
- 2910092
- 5770832
- 5413816
- 7311140
- 7468912
- 2970324
- 7469124
- 2971432
- 2908072
- 2911436
- 1688956
- 1695608
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4876-4891
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F106: 家の部屋の壁紙・床をその場で替えるゲーム自身の手順（2026-10-07、MEDIUM: 静的 2 経路。実機未確認）

解析ソフト: IDA / 解析モデル: opus-5.5。T022 の壁紙・床紙リストの前提。主 IDB に命名・注記・保存済み。
- **家の部屋（Room_HasFlags(0x80)）の背景は ModuleIndoor ではなく本体の `BsCharRoomViewMgr`**（RTTI 17BsCharRoomViewMgr、vtable 0x8EC71C）。
  ModuleIndoor の `BsIndoorViewMgr` が読む場面ごとの表 word_9921F4（壁）/ word_992340（床）（165 部屋）は `SceneBgTable_Init` 0x285454 で特別な部屋（43, 57〜62）以外 0x7FFE（空）になる。家の部屋はこの表を使わない。
- `BsCharRoomViewMgr_Calc` 0x2C6978（vtable 9、毎フレーム。+48 を 1800 まで数える）が毎フレーム `Room_GetCurrentWallpaper` 0x52851C / `Room_GetCurrentFlooring` 0x528314 で**セーブの部屋データから壁 → this+34、床 → this+40 に写し直す**。
  `BsCharRoomViewMgr_ApplyAndSubmit` 0x2C678C（vtable 12）が毎フレーム `RoomFloor_ApplyItem` 0x580E50(this+13728, this+40)・`RoomWall_ApplyItem` 0x529BB8(this+14416, this+34)・sub_60CBB4(this+15336, this+34) を呼ぶ（逆アセンブルで R1 = this+0x28 / +0x22 を確認）。
  Apply は読み込み済みの品（obj+40〜+54）と比べ、違えば vtable+12 で読み込みを始め、vtable+20 が準備完了を返したら 2 面の片方と入れ替える（RoomFloor_ApplyItem の逆コンパイル）。
- 部屋データ: `Room_GetSaveRoomData` 0x6F8F24(部屋番号) = 770 B（0x302）。+754（0x2F2）壁紙、+758（0x2F6）床、+32 / +33 = それぞれの品の付属 1 バイト。`RoomData_Get/SetWallpaper` 0x71F770 / 0x2D52D4、`RoomData_Get/SetFlooring` 0x71F844 / 0x2D5728。
- ゲーム自身の貼り替え: `HouseRoom_SetWallpaper` 0x2C5FA8(品*, 音を鳴らす) / `HouseRoom_SetFlooring` 0x2C6CCC。種類 3 / 4（または sub_76A390）を確かめ、通信中なら Net_SendPacket 0x78 / 0x79（**0x0C ではない**）、音 0x100094E SE_ACT_WALLPAPER_CHANGE / 0x100094F SE_ACT_CARPET_CHANGE、部屋データ +754 / +758 に書き +32 / +33 = 0。**画面への反映の呼び出しは無い**（上の毎フレームの写し直しに任せている）。
  呼び手はポケットの「貼る」`PocketMenu_UseWallpaper` 0x19C57C / `PocketMenu_UseFlooring` 0x19DF78 だけ（前の壁紙をポケットのその枠へ戻す）。
- 照合: (1) 貼り替え関数がデータを書くだけで返る、(2) 表示側が毎フレームデータを読み直し差分で入れ替える、の 2 経路が一致。→ **リストからの貼り替えは HouseRoom_SetWallpaper / SetFlooring を呼ぶだけで済む見込み**（MEDIUM）。反証条件: 実機で呼んでも見た目が変わらない／部屋を出入りするまで変わらない。
- ModuleIndoor 側の同類（特別な部屋用、表に書く）: sub_B1DB84（壁、通信 0x7A）/ sub_B1FD00（床、0x7B）/ sub_B1E220（部屋 62、0x7C）、表から貼り直す BsIndoorViewMgr vtable 12 = sub_B1F534。家の部屋では使わない。

- 訂正（F105、2026-10-07、IDA-gpt-6.1-sol-F001 による指摘を親 opus-5.5 が ModuleFtr 0xB08D48 の逆コンパイルで照合）: 記録の **+24 は記録自身の番号**（`FtrMgr_CreatePrepare` 0xB08CA4 が i を書く）で、親の番号ではない。親は `FtrRec_GetParentRecordIndex` 0xB1EB74（AcFtr +1548 の親から記録を探す）。+25 は UnitCursor の枠番号でチップの番号ではない。

