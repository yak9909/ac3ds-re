---
id: ACNL-F0600
aliases:
- IDA-opus-5.5-F084
title: '部屋の内部名の表、メッシュ 1 つを半透明で描く命令の挟み方、T018 第 1 段の実機（2026-10-05、HIGH（部屋の表: ID 一覧とゲームの表の 2 経路）/ MEDIUM（半透明: 静的、実機未確認））'
summary: '解析モデル opus-5.5。IDB: `g_RoomInternalNames 0x9515F0`（命名・注記）、`gfx_DrawMesh 0x48D26C` に注記。'
date: '2026-10-05'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9770480
- 4772460
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4605-4617
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F084: 部屋の内部名の表、メッシュ 1 つを半透明で描く命令の挟み方、T018 第 1 段の実機（2026-10-05、HIGH（部屋の表: ID 一覧とゲームの表の 2 経路）/ MEDIUM（半透明: 静的、実機未確認））

解析モデル opus-5.5。IDB: `g_RoomInternalNames 0x9515F0`（命名・注記）、`gfx_DrawMesh 0x48D26C` に注記。
- 部屋の内部名の表 0x9515F0（4 B 刻み、部屋 ID 順）: 0 Village / 1 Downtown / 2 Station … **0x48 BeautySalon**（前後 0x47 CLUB444_Live・0x49 Museum_Entrance）。Vapecord の Room_IDS.txt（16 進）と一致。
- 実機（2026-10-05、gohan 3d37359）: 吹き出しの複製・反映・回転・Y・音・開け閉めは PASS。**美容室の小物の音（GROUP_SHOP）は屋内・屋外で鳴らず、美容室では鳴る**（F083 の見込みどおり）。
  → 美容室以外では常駐の SE_ACT_CLOTHES_CMN_CHANGE 0x1000530 で代わりに鳴らす。利用者の指定: 位置 y 170・大きさ 60、吹き出しの登場後にフェードイン、かみがた・かおで別の音。
- 半透明（gohan、実機未確認）: `gfx_DrawMesh` = 材質（node+0x164 の表の mesh+0x1C 番目を文脈 +0x20）→ `gfx_RenderContext_BindMaterial` → `sub_4957C4(文脈, mesh)` →
  `gfx_DrawShapePrimitives(dc, node, 資源 +0xC8 の表の mesh+0x18 番目, mesh+0x28)` → mesh+0x68 の命令列（長さ +0x6C）を写す。これを写し、形の直前に
  フレームバッファの読み書き（`gfx_MaterialActivator_Activate` 末尾の 40 B = [1, 0xF0111][1, 0xF0110][読み 15, 0x803F0112, 書き, 深度読み, 深度書き, 0]。
  初期化 `sub_79B0C0`、今の値 dword_96F088 / 8C / 90）と合成 [0xE40100, 0x803F0100, 0xD1DC0000, 3, α<<24, 0]（IDA-gpt-6-astra-F002 と同じ値）を積む。
  描き終えたら文脈 +36 と材質の部分ごとの鍵 +256..+296 を 0 にして、次の材質に状態を全部送り直させる。
- 色見本の枠: 選択を外すとき通常の色へ塗り戻していなかった（押すと前の選択の縞が出た。利用者）→ kSwatchNormal で塗り戻す。

