---
id: ACNL-F0469
aliases:
- IDA-opus-5.5-F064
title: 'マップエディターのマスの色 — 上画面の単色の四角形（UnitCursor 資源の別の体）と盤面の 5x5 の輪郭（2026-09-28、MEDIUM: 既存の実機知見の組み合わせ＋描画器。gohan 実機未確認）'
summary: '解析ソフト: IDA（主 IDB）＋既存の実機知見 / 解析モデル: opus-5.5。利用者指示: 盤面の中心から 5x5 の輪郭のマスを真っ白に。上画面の 7x7 にマス単位の単色四角形'
date: '2026-09-28'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5875968
tags:
- map
supersedes: []
source: IDA:work/FINDINGS.md:1599-1615
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F064: マップエディターのマスの色 — 上画面の単色の四角形（UnitCursor 資源の別の体）と盤面の 5x5 の輪郭（2026-09-28、MEDIUM: 既存の実機知見の組み合わせ＋描画器。gohan 実機未確認）

解析ソフト: IDA（主 IDB）＋既存の実機知見 / 解析モデル: opus-5.5。利用者指示: 盤面の中心から 5x5 の輪郭のマスを真っ白に。上画面の 7x7 にマス単位の単色四角形
（輪郭 = 白、真ん中 = 赤、ほか = 黄）、マイデザインより上・それ以外より下。アルファを一括で変える一時項目。方式は任せる。
- **方式**: 自前の GPU 命令ではなく、GridCursor が読む UnitCursor.bcres（板 32x32 = 1 マス）から色ごとに 1 体（計 3 体、bufferOption 0x834）を作り、
  InstancedDraw で置く（世界の曲面変換は fgobj_Object_SetModelView とゲームの FieldPositionToRenderSpace。F059）。1 か所の費用は UnitCursor と同じ。
- **材質**（BuildingHighlight の F011〜F013 と同じ欄・同じ作法）: TEV を gohan の配列へ写し、体の色の部分 +648 から指して材質 +72 を色の部分へ。
  段 0 = REPLACE(Constant5 の rgb / a)、段 1〜5 = REPLACE(前段)。ブレンド（frag +328 = PICA 0x101）を 0x71760000（SRC_A / 1−SRC_A）に（元の UnitCursor は 0x01160000 = 加算）、
  +300 = 0、深度を書かない（+280 bit1、F061）。フラグメントの設定が体のもの（frag == 色の部分、0x100/0x101 の既定の形）でなければ組まない（理由 102 をメニューに通知）。
  色・アルファ = 体ごとの Constant5（毎フレーム書く。GridCursor::ApplyTint と同じ）。
- **描く順**: InstancedDraw::SubmitOver = 村の物体の描画ノードの層 0 のコールバックを包み、ゲームの 0x59A900（マイデザインを含む層 0）の**後**に描く。深度テスト LT のまま
  → 手前の物体の画素では隠れる。高さは UnitCursor と同じ GroundHeight（D の前、同じ置き方の UnitCursor がマイデザインの上に出ていた = 板の方が手前、利用者の実機報告）。
- **盤面**: 隠した窓 P_Window_00（5x5 = 100、白）と P_Window_01（3x3 = 60、地の白色 = P_Room_00 の材質 +0x14）を、自分の材質の黒色・白色を同じ値にして
  （出力 = lerp(黒色, 白色, テクセル) × 頂点色、F040）地の後・真ん中・方眼の前へ。+0x4D bit2 を落として送り直させる（コマの色と同じ）。描画器で確認（board_preview.mjs）。
- 検査: verify_map_editor 群 15（8 項目。欄は BuildingHighlight と一致、ブレンドの値、TEV、並べ方 16 白 / 1 赤 / 32 黄、描く順）。
- 反証条件: 実機で四角形が出ない（理由の通知）、マイデザインの下に隠れる・物体の上に出る、色が違う、UnitCursor の見た目が変わる、盤面の輪郭が白くない。

