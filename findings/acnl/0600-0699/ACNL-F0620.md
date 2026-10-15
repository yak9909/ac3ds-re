---
id: ACNL-F0620
aliases:
- IDA-opus-5.5-F104
title: '家具をその場で消すゲーム自身の手順（2026-10-06、MEDIUM: 静的。実機は試験 4 待ち）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。T022。'
date: '2026-10-06'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6889676
- 6879876
- 10230260
- 10230452
- 5147892
- 5700880
- 5702448
- 5726000
- 5136960
- 5147488
- 6888148
- 6884644
- 1703996
- 5147140
- 5702996
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4833-4846
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F104: 家具をその場で消すゲーム自身の手順（2026-10-06、MEDIUM: 静的。実機は試験 4 待ち）

解析ソフト: IDA / 解析モデル: opus-5.5。T022。
- **実機 試験 3**（利用者）: 置く（Room_TryPutFurnitureAt 0x6920CC → BsFtrMgr_SpawnFromRecord 0x68FA84）は即反映で「かざる」と同じ（向き = プレイヤーと同じ）。位置がプレイヤーの左上なのは試験の自前の輪探索の順（HHD の順へ替える予定）。
  消す（Item_PlaceItem 操作 6）は即反映せず、出入りでリンゴ 0x2001 になった（0x2001 は空ではなく品物）。→ この経路は不採用。
- 家具オブジェクトの表: `g_RoomFtrObjects` 0x9C19F4（48 個）と `g_RoomFtrCellGrid` 0x9C1AB4（層 0 = 64x80 B、層 1 = +5120 の 16x16 B、0xFF = 無し）。マス → 家具 = `FtrGrid_GetFurnitureAt` 0x4E8CF4(表, x, z, 層)。
- `AcFtr_ChangeState` 0x56FD10(家具, 状態 0..12): 表 off_83E604 の PMF を呼び、成功なら +1528 に状態を書く。
  ゲーム自身の部屋の家具の消去 sub_4E4FD0 は「vtable+144 が真なら状態 6、偽なら +1892 |= 0x800（後で）」。状態 7 は UiScreen_RequestDestroyRecursive（呼び手 0 の sub_4E6118 が使う）。
- 片付け `AcFtr_DestroyBegin` 0x570330（状態 6/7）→ `AcFtr_ReleaseCells` 0x575F30 → `Room_ClearFurnitureFootprint` 0x4E6240（大きさの全マスへ空 ItemToPlace を書く。家具の上の層も消す。通信中は通信 0x50）+ `FtrGrid_ClearCells` 0x4E8B60。
  ※家具の上に置いた物も一緒に消える（HHD のゴミ箱と挙動を比べる必要あり）。
- 試験 4（gohan work/furniture-test 7daf01d、artifacts/plugins/furniture_test3）: 消す = 一番近い家具オブジェクトへ状態 6、マップが 0x7FFE になりオブジェクトが消えるまで毎フレーム監視して通知。
- IDB: 上記と Room_SearchPutSpot 0x691AD4 / Room_FindPutSpotForPlayer 0x690D24 / Pocket_DecorateInHouse 0x1A003C / FtrGrid_SetCells 0x4E8A04 を命名、コメント。
- 追記（2026-10-07、試験 4 = HIGH: 静的 + 実機）: 状態 6 で 8 フレーム後にマップ 0x7FFE・オブジェクト消滅・即反映（利用者）。上に載った物は浮いて残る: 通常の部屋の経路は 0x570554 で R2=0 → AcFtr_ReleaseCells(a3=0) なので層 1 を消さない（静的）。ACNL の拾う処理は上の物から先に拾う（sub_690588 の層の順）ので、土台だけを消す場面はゲームに無い。

