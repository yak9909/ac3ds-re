---
id: ACNL-F0504
aliases:
- IDA-opus-5.5-F027
title: '橋の高さは村の中で一定＝「村の川底で一番多い段 + flt_6DE560」（2026-09-24、HIGH（静的＋実機の地形全体・実物の橋 y と一致＋利用者の実機確認）。gohan 1754f62 は利用者が実機で確認: 橋を出しているとき、どこにカーソルがあっても UnitCursor とカメラは同じ高さ）'
summary: '**利用者の前提**: 橋の描画は海でも陸でも川でも崖でも常に同じ高さ。物理的な位置だけが下の地形で変わる（海へ動かすと下がる）。'
date: '2026-09-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5400168
- 7098120
tags:
- camera
supersedes: []
source: IDA:work/FINDINGS.md:2303-2319
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F027: 橋の高さは村の中で一定＝「村の川底で一番多い段 + flt_6DE560」（2026-09-24、HIGH（静的＋実機の地形全体・実物の橋 y と一致＋利用者の実機確認）。gohan 1754f62 は利用者が実機で確認: 橋を出しているとき、どこにカーソルがあっても UnitCursor とカメラは同じ高さ）

- **利用者の前提**: 橋の描画は海でも陸でも川でも崖でも常に同じ高さ。物理的な位置だけが下の地形で変わる（海へ動かすと下がる）。
  描画が一定なのは F024（平行移動 (x,0,0)、半径はモデルが持つ）と整合。
- **物理的な位置が変わる理由（静的）**: `Structure_StampTile 0x526668`（旧 sub_526668、`Structure_StampFootprint` の 1 マス分）が
  板のマス（属性 23/24）の 4 隅へ **+0x1084（3 つの 5 ビット欄それぞれ +4 段 = +32）**。実機の床 16 = 川底 10 + 足元 2 + 4 と一致。
  起動時の `BsStrcMgr_SpawnStructures` も基点の地面 + flt_6DE560（=32.0）。つまり下の地形が浜なら浜 + 32。
- **F026 の「最寄りの川底」は不可**（利用者の実機確認: 海の近くで浜に合う）。実機で Suspend: カーソル (24,47)、橋の高さ 32 = 河口の川底 0 + 32。
  `work/evidence/strc/bridge_height_sea.json`（`tools/strc/probe_bridge_height.py`）。
- **村の地形全体**（`tools/strc/dump_village_terrain.py` → `work/evidence/strc/village_terrain.bin`、7x6 区画 108,696 B）:
  川底（水の種類 1）の段 = 10: 269 マス / 0（浜の河口）: 38 / 22: 1。陸 = 14: 3,746 / 26: 1,665 / 4（浜）: 767。
  → 一番多い川底 10 x 8 + 32 = **112** = 実物の橋 y（F024）= 利用者が「この高さで固定」とした値（`bridge_height_land_112.json`）= 役場の y。
- **gohan**: `PublicWorks::BridgeHeight` = 村の全マスで `WaterKind(Field_GetAttrAt(pos,0)) == 1` の地面の段を数え、最多の段 x 8 + flt_6DE560
  （ゲームから読む）。部屋データ（dword_9AEA04[0]）ごとに 1 回。UnitCursor とカメラが使う。
- **Field_GetAttrAt 0x6C4F08**（旧 sub_6C4F08）= 位置のマスの属性コード（0xFF 以上・区画なしは 0）。
- 反証条件: 本土以外の段の川が本土の川より長い村（最多の段が本土でなくなる）。その村の実物の橋の y と比べる。

