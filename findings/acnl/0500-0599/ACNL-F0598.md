---
id: ACNL-F0598
aliases:
- IDA-opus-5.5-F082
title: 'レイアウトの材質の TEV の段と座標生成の意味（2026-10-05、HIGH 相当: 逆アセンブル + ACNL の実在の材質 215 個と照合。実機の描画は未確認）'
summary: '解析モデル opus-5.5。IDB: `nwlyt_Material_EmitTevStages 0x4B8790`（命名・注記）、`nwlyt_CalcTexCoordsForGpu 0x73B650`（注記）。'
date: '2026-10-05'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4949904
- 7583312
- 4946020
- 7584956
tags:
- layout
supersedes: []
source: IDA:work/FINDINGS.md:4576-4589
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F082: レイアウトの材質の TEV の段と座標生成の意味（2026-10-05、HIGH 相当: 逆アセンブル + ACNL の実在の材質 215 個と照合。実機の描画は未確認）

解析モデル opus-5.5。IDB: `nwlyt_Material_EmitTevStages 0x4B8790`（命名・注記）、`nwlyt_CalcTexCoordsForGpu 0x73B650`（注記）。
- `Material_EmitState 0x4B7864` は材質の旗 +48 の 0x1C0（TEV の段の数）があれば `nwlyt_Material_EmitTevStages` を呼ぶ。段は bclyt mat1 の 12 B（rgb 語 / α 語 / 定数色の番号）。
  語のニブル: [3:0][7:4][11:8] 入力（0 tex0 / 1 tex1 / 2 tex2 / 3 tex3 / 4 定数 / 5 頂点色 / 6 前の段 / 7 前のバッファ。PICA の番号へ表 {3,4,5,6,14,0,15,13}）、
  [15:12][19:16][23:20] 成分（rgb 0 色 / 1 1−色 / 2 α / 3 1−α …、α 0 α / 1 1−α …）、[27:24] 合成（0 置換 / 1 乗算 / 2 加算 / 3 符号付き加算 / 4 補間 s0·s2 + s1·(1−s2) / 5 減算 / 6 AddMult / 7 MultAdd）、
  [29:28] 倍率、bit30 バッファへ書く。第 3 語 [3:0] rgb / [7:4] α の定数色の番号（材質の色 n）。最後にバッファの初期色 reg 0xFD = 色 0（黒色）。
- 照合: ACNL の窓の枠（atm_win W_msg_00LT 等）= 段 0 rgb (1−tex0)×tex1・α tex0、段 1 rgb 補間(白色, 黒色, 前)・α 前×頂点色 → 「縞の窓の枠」として意味が通る。
  ACNL の全レイアウト 33 本の材質 4,938 個のうち テクスチャ 2 枚以上か TEV ありが 215 個（work/cache/hhd/tev/scan_tev.py）。
- 座標生成（mat1 の 4 B）は **+1 バイト目 = 使う UV の組の番号だけ**で、投影は無い（`0x73B650`）。SRT は t = R(θ)·diag(sx, sy)·(uv − 0.5) + 0.5 + T。
- 窓の枠（`nwlyt_Window_DrawSelf 0x73BCBC`）: 枠の配列 win+0x160、1 枚 8 B（+0 反転、+4 材質）。4 枚のときの並びは 左上 / 右上 / 左下 / 右下（+0 / +8 / +16 / +24）で、
  描くのは左上 → 右上 → 右下 → 左下。枠の UV は画素に比例（1 = 枠のテクスチャの幅）で、右上・左下などは反転される。
- 使い道（設計）: HHD の選択枠の縞（色 = 白色と黒色を縞で補間、形 = 枠の α。HHD-F011）を ACNL の TEV 2 段で作る。窓は 4 枚に分け、縞の SRT を角ごとに解いて継ぎ目を揃える。

