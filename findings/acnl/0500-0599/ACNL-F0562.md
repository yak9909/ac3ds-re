---
id: ACNL-F0562
aliases:
- IDA-unknown-F020
- V2-F020
title: 家具モデルは屋外でも出る（部屋ごとの収容数）。UnitCursor だけが屋内限定（2026-09-18、MEDIUM）
summary: 利用者の指摘（オートキャンプは屋外判定で家具モデルを表示）を受けて IDA-unknown-F019 の表現を訂正。Room_GetFurnitureCapacity 0x5B5E18 が引く g_RoomFurnitureCapacity 0x8835BC は屋外でも非0で、村 0x00=38、Downtown 0x01=2、オートキャンプ場 0x9F/0xA0=10、カー内部 0xA1/0xA2=36、家1F 0x03=48。BsFtrMgr_CreateResource
date: '2026-09-18'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5987864
- 8926652
- 6880324
- 6359492
- 6364892
- 6961880
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:4251-4254
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F020: 家具モデルは屋外でも出る（部屋ごとの収容数）。UnitCursor だけが屋内限定（2026-09-18、MEDIUM）

利用者の指摘（オートキャンプは屋外判定で家具モデルを表示）を受けて IDA-unknown-F019 の表現を訂正。Room_GetFurnitureCapacity 0x5B5E18 が引く g_RoomFurnitureCapacity 0x8835BC は屋外でも非0で、村 0x00=38、Downtown 0x01=2、オートキャンプ場 0x9F/0xA0=10、カー内部 0xA1/0xA2=36、家1F 0x03=48。BsFtrMgr_CreateResources 0x68FC44 がこの数だけ家具枠（1枠 CPU 96000B＋VRAM 2本）を作るので、家具モデルの表示基盤は code.bin 側で屋外でも動く。ItemIndoor.bin は ScStage_PrepareStep 0x6109C4 が bit8 または bit28(0x10000000=オートキャンプ場) または bit29(0x20000000=カー内部) で読み、bit28/29 では ScStage_LoadCampingCarInfo 0x611EDC が NpcCampingCarInfo/*.bin を読む。一方 UnitCursor.bcres の条件は bit8 のみで、モジュール選択 Room_SelectModules 0x6A3AD8 も bit8 のときだけ "Indoor"/"Ftr" を積む（"Ftr" の参照はこの1か所）。オートキャンプ場は "AutoCamp" を積む。よって「屋外に UnitCursor が無い」は変わらないが、「屋外に家具モデルが出ない」は誤りだった。屋外でも BsFtrMgr が動く分、自前表示の見込みは上がる。反証条件: 屋外の部屋で UnitCursor.bcres が読まれている、または bit8 以外で "Indoor" が積まれる。根拠 work/evidence/unit_cursor/README.md §6。

