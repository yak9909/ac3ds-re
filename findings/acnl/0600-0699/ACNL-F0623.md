---
id: ACNL-F0623
aliases:
- IDA-gpt-6.1-sol-F001
title: '模様替え UI を開いたまま家具を出す材料（2026-10-07、MEDIUM: 静的のみ。途中で打ち切り）'
summary: '解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_spawn.md）。利用者の 5 時間枠の都合で途中で打ち切り、同じセッションを再開してまとめさせた（IDB には触れさせず）。記録・採番・照合は親（opus-5.5）。'
date: '2026-10-07'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7669592
- 5977292
- 6889676
- 6879876
- 5692964
- 1703996
- 6884644
- 6888148
- 5977884
- 7621076
- 2642856
- 3240080
- 9751048
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4892-4904
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F001: 模様替え UI を開いたまま家具を出す材料（2026-10-07、MEDIUM: 静的のみ。途中で打ち切り）

解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_spawn.md）。利用者の 5 時間枠の都合で途中で打ち切り、同じセッションを再開してまとめさせた（IDB には触れさせず）。記録・採番・照合は親（opus-5.5）。
詳細と全根拠は **work/evidence/t022_spawn/report.md**（evidence/ に逆アセンブル・逆コンパイル、static_tables.json、room_bounds.json）。主 IDB に命名 18 関数 + 1 大域・コメント 28、ModuleFtr.elf に命名 10 関数 + 2 大域・コメント 15（ID は親が F??? → 本 ID に置換）。主 IDB の関数定義 0x750758 / 0x5B34CC は保存前に打ち切られたので親が定義し直した。
- **置く**: `Room_TryPutFurnitureAt` 0x6920CC は判定だけ（R0 = 12 B の出力記録、R1 = x、R2 = z、R3 = 向き、スタックに Item*・層・プレイヤー X/Z・向きの四分円・探索パターン。戻り 0 = 可、3/4/5 = 不可の種類）。`BsFtrMgr_SpawnFromRecord` 0x68FA84(記録) が生成（0 = 失敗）。生成の準備 `AcFtr_CreatePrepare` 0x56DE24 がマップへ書き、ModuleFtr の記録へ自動登録。**チップは自動では作られない**。
  かざるの本来の呼び手は `Pocket_DecorateInHouse` 0x1A003C → `Room_FindPutSpotForPlayer` 0x690D24 → `Room_SearchPutSpot` 0x691AD4 → TryPut → Spawn（ポケット消費とカメラの復帰を伴うので、リストからは下位の判定・生成だけを使う案）。
- **上限**: 家の家具のアクターは 48（`Room_GetFurnitureActorCapacity` 0x5B371C、空き `FtrObjectTable_CountFreeSlots` 0x7449D4）。記録・チップの 112 とは別。TryPut は空きを保証しない。
- **部屋の範囲**: `Room_GetInteriorCellBounds` 0x2853A8 は両端を含む（max から 1 引く。親が照合）。
- **チップ**: `Editor_CreateChips` 0xB3CC08 は重複を調べないので開いている間に呼び直してはいけない。1 件だけ作るなら `Chip_Setup` 0xB43160(空きチップ, エディター+76 = chip.arc の資源, 記録) → 層 1 なら親チップを探して `0xB2FB2C(親, 子)` で結ぶ（子は最大 4）→ `0xB42084(チップ, *(エディター+1168))` で N_All をエディターのペインへ接続。空きチップの再利用の後片付けは LOW。
- **空き場所探しの材料**: プレイヤー = GetPlayerObject(4,0) の +20 XYZ と +46 の向き（u16）、`Field_WorldToCellXZ` 0x317090、マスの中心 (32x+16, 0, 32z+16)。家具の大きさは ItemParam+23 の下位 4 ビットで 5 種類（1×1 / 2×1 / 2×2 / 3×2 / 3×3）、向きごとのマスの表 0x94CA08。模様替え中のカメラはモード 25（入口で yaw = 0）。HHD の四分円の番号との対応は未照合。
- 親の独立照合: (1) ModuleFtr 0xB08CA4 の +24 = i、(2) 0x2853A8 の上端 −1。どちらも一致。
- 未確定: 開いたエディターでの更新順、生成と Chip_Setup の同じフレームでの安全性、失敗時の巻き戻し、空きチップの再利用。全部実測なし。

