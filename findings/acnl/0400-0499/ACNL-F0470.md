---
id: ACNL-F0470
aliases:
- IDA-opus-5.5-F063
title: 'マップエディターの盤面を 9x9 へ（chip_room_00 の大きさの規則）と、L / R の音（2026-09-28、MEDIUM: 静的＋描画器。gohan 実機未確認）'
summary: '解析ソフト: IDA（主 IDB）＋ romfs の bclan / bclim ＋ acnl-ui-designer / 解析モデル: opus-5.5。利用者指示: 盤面を 9x9 に、真ん中のマスの背景を少し赤く。L / R でも一覧で選んだときの音。'
date: '2026-09-28'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7455544
- 2846516
tags:
- map
supersedes: []
source: IDA:work/FINDINGS.md:1616-1633
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F063: マップエディターの盤面を 9x9 へ（chip_room_00 の大きさの規則）と、L / R の音（2026-09-28、MEDIUM: 静的＋描画器。gohan 実機未確認）

解析ソフト: IDA（主 IDB）＋ romfs の bclan / bclim ＋ acnl-ui-designer / 解析モデル: opus-5.5。利用者指示: 盤面を 9x9 に、真ん中のマスの背景を少し赤く。L / R でも一覧で選んだときの音。
- **kind アニメ（chip_room_00_kind、G_kind_00）**: 大きさのキーは 4x4/6x6/8x8 の 3 種だけ。部屋 = P_Room_00・N_Sound_00・B_Room_00 = 80/120/160（P_Room_00・P_RoomGrid_00 は 6x6 で 128）、
  壁 = W_Wall_00・N_SoundW_00 = 108/148/188（**常に部屋 + 28**）。方眼 P_RoomGrid_00: パターン（CLTP）フレーム ≥1 で my_min_Grid08_00（128x128 A4）、
  texSRT 倍率（CLTS）1.25、平行移動 0.5（マテリアル）、ラップはミラー。テクスチャの線は**テクセル 7.5 + 20k**（2 画素、ミラーの 128 をまたいでも同じ間隔）
  → 8x8 は部屋の左端がテクセル 48、1 画素 = 1 テクセル。出入り（in/out）は N_inout_00 の y だけ。
- **9x9（gohan）**: 8x8 を焼いたあと、部屋 180・壁 208 を書き、方眼は Picture の座標を t = (c − 0.5)·1.25 + 1.0 から解いて左端 = テクセル 28（線 27/28）。
  描画器（tools/layout/board9_preview.mjs）で線がマスの辺ごと（0/19 … 160/179）に来ることを確認。真ん中の交点の小さな点はミラーの継ぎ目で、8x8 の中心にも同じ物がある。
  盤面は右へ 11（壁の左端 = 67 = モード一覧の右端の次、右端 275）。真ん中のマス = 隠した P_door_00 に P_Room_00 のマテリアルを付け、頂点色 (255,227,242) で赤みを足して方眼の直前に描く（壊す前に戻す）。
  吸着（CollectChip sub_B359D4 の式）は原点 O = 半マス（ゲームは偶数の部屋なので O = 0.0）、カメラの中心は 32·(v + kView/2) を小数で（奇数はマスの真ん中）。コマ 224、カーソル 121 ≤ 128。
- **L / R の音**: 行ボタンの決定音 = ButtonActionNode vt+56 0x71C338（+218 が真なら +204 を Game_PlaySound）。SetupButtons が行ノードに +204 = 0x1000485、+218 = 1。
  StartDecide 0x2B6F34 が同じ vt+56 を呼ぶ = タップで鳴る音と同じ。L / R で選び直した直後に呼ぶ。
- 検査: verify_map_editor 群 14（8 項目、kind のキー・CLTS/CLTP・見本の線・位置・後始末・音）、test_map_select は kView = 9 で 0 失敗（吸着は O = 10 でも格子線へ）。
- 反証条件: 実機で方眼がずれる・継ぎ目が出る、壁が一覧と重なる、タップしたマスと盤面の位置がずれる、真ん中の色が出ない、L / R で音が出ない・別の音。
- **追記（2026-09-28、利用者の実機確認: 9x9 は 1〜6 PASS）→ 7x7 へ**: 大きさの規則は同じ（部屋 140・壁 168）。方眼は左端 = テクセル 48（8x8 と同じ線 47/48）、右端の画素 187 → ミラーで 68 = 線 67/68。
  描画器で線がマスの辺ごと（0/19 … 120/139）。盤面は真ん中のまま（壁の左端 76、一覧は x < 67）、一覧は盤面と盤面のコマの後に登録して手前に。真ん中の頂点色 (255,200,220)（目安 (255,185,150)）。gohan 実機未確認。

