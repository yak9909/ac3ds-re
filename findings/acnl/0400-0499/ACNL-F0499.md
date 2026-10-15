---
id: ACNL-F0499
aliases:
- IDA-opus-5.5-F032
title: 画面固定の複製でズボンが止まる＝部品のスキニング行列は Scene の更新が計算する。光はフラグメントライティングではない（★光の部分は F033 で訂正：読んだ組が違った）（2026-09-24、MEDIUM（実機の読み取り＋静的）。gohan 8908f5d は実機未確認）
summary: '**利用者の実機確認（gohan 246865a）**: 上画面の決まった位置に固定・世界の物に隠れない（2D UI には隠れる）・部品は欠けない・設定は全部効く。'
date: '2026-09-24'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 4786200
- 4833420
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2217-2235
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F032: 画面固定の複製でズボンが止まる＝部品のスキニング行列は Scene の更新が計算する。光はフラグメントライティングではない（★光の部分は F033 で訂正：読んだ組が違った）（2026-09-24、MEDIUM（実機の読み取り＋静的）。gohan 8908f5d は実機未確認）

- **利用者の実機確認（gohan 246865a）**: 上画面の決まった位置に固定・世界の物に隠れない（2D UI には隠れる）・部品は欠けない・設定は全部効く。
  問題: ズボンだけ動き・向きに付いてこない／髪型・髪色を一度変えると -1 で 0 の見た目／髪を変えると環境光に影響される／影響されないときは暗い／上を向きすぎ。
- **ズボン（実機の読み取り、tools/models3d/probe_clone_parts.py・probe_clone_meshes.py）**: 部品は頭（nw::gfx::Model）と上着・ズボン・靴下・靴
  （SkeletalModel、各自の StandardSkeleton ノード+0x220、ボーン 18）。向き 90 度で全部のノード行列が回り、骨格のワールド行列（48B の表）も体と一致。
  それでも拡大画像ではズボンだけ正面のまま（`work/evidence/screens/clone_20260924/screen_yaw90_zoom.png`）。
  **スキニング行列（ワールド × 逆バインド）は `sub_737378`（`sub_4E9EB4` / `sub_49009C` から。Scene の更新 `nwgfx_SceneUpdater_UpdateAll 0x490818`）が計算**し、
  部品を Scene に積まないと更新されない。ワールド行列をそのまま使う部品（上着など）は回る。世界に置いた版（Scene 0 に積む）ではズボンも正しかった。
  → gohan 8908f5d: 画面固定でも Scene 0 に積み、(0, -5000, 0)（far 1750 より遠い）に置いて世界では見えなくし、late pass は同じ位置を見る。
- **右下の茶色の板と白い塊**は複製を動かしても残る世界側の物（複製と無関係。`screen_x100.png`）。
- **光**: `LightSet` 4 つは空（環境光・半球・フラグメントライト無し、`tools/models3d/probe_light_sets.py`）、描画の文脈のライト数 0。
  `gfx_MaterialActivator_Activate 0x49C08C` はライト数が 1 以上のときだけフラグメントライティングを有効にする → キャラクターはフラグメントライティングを使っていない。
  マテリアルの光の色・定数色は本物と複製で同じ（`tools/models3d/probe_clone_materials.py`）。頂点シェーダの定数をゲーム独自に焼き込む `sub_1C1514`
  （プレイヤー管理役の近く、色 1.0 の組 `dword_980AF0`・`dword_980B20`）が次の調査先。**未解決**。
- **髪 -1**: 以前は最後に書いた値が残った。gohan 8908f5d で本物の PlayerModel +548/+552 を毎フレーム写す。
- **傾き**: RotX(傾き) × RotY(向き)、既定 10 度（正で頭が専用カメラ側へ）。
- 反証条件: 8908f5d でもズボンが止まる（Scene の更新以外がスキニングを計算している）。

