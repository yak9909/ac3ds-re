---
id: ACNL-F0594
aliases:
- IDA-opus-5.5-F078
title: 'HHD の「ペインに投影」の座標生成を ACNL の UV で再現する規則（HHD-T006 の水玉の謎の答え）（2026-10-05、MEDIUM: レイアウトのデータ 2 種と HHD のスクショの照合。HHD のコードは未読）'
summary: '解析ソフト: なし（3DSkit の BFLYT の読み + acnl-ui-designer の描画）。解析モデル opus-5.5。段階 2（上画面）の変換で判明。'
date: '2026-10-05'
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags:
- layout
supersedes: []
source: IDA:work/FINDINGS.md:4518-4531
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F078: HHD の「ペインに投影」の座標生成を ACNL の UV で再現する規則（HHD-T006 の水玉の謎の答え）（2026-10-05、MEDIUM: レイアウトのデータ 2 種と HHD のスクショの照合。HHD のコードは未読）

解析ソフト: なし（3DSkit の BFLYT の読み + acnl-ui-designer の描画）。解析モデル opus-5.5。段階 2（上画面）の変換で判明。

- HHD の材質のうち、座標生成が **pane based projection（pane r and s projection、投影の拡大 1・平行移動 0）** のものがある:
  fce_BG_00 / fce_Top_00 の P_Pattern_00（水玉）、fce_Top_00 の P_Ccl_00 / P_Ccl_01（吹き出しの小さな丸）。ほかに 2 枚目のテクスチャ（縞）の座標生成でも使われる（cbn/fce_Btn_00 P_Btn_00、fce_Color_00 P_Frame_00、fce_Eye/Hair_00 W_Frame_00LT。未使用）。
- 規則: **u = ペイン上の x / テクスチャの幅 + 0.5、v = −y / 高さ + 0.5**（ペインの中心が 0）を UV として焼き、その上に材質のテクスチャ SRT を掛ける。
  照合 2 点: (1) 水玉 430×240 / 64 に SRT 拡大 2・回転 45 → 周期 32 px（HHD のスクショ・ACNL 実機の測定と一致。設計 §3.2-5 の実測合わせを置き換え）、
  (2) 小さな丸 64 / 32 → −0.5〜1.5、SRT 平行移動 0.5 → 0〜2 を反転で 4 分の 1 の円が丸になる（HHD のスクショと一致）。
- 文字の基準点: HHD の x alignment / y alignment を ACNL の TextBox の基準点（横 + 縦×3）に写す（上画面の「まわす」は左揃え。全部中央にしていて右へずれた）。
  HHD の文字の影（shadow enabled）は ACNL の TextBox に欄が無いので出ない。十字キーの記号 = Garden_msg_size16 の U+E006（私用領域の字形を描いて確認: E000〜E005 = A B X Y L R）。
- 上画面 hhd_top（fce_Top_00）: 11 ペイン、テクスチャ 4。モデルの部分（中央）を除き HHD のスクショと一致。残る差は loop アニメ（吹き出し・小さな丸の伸び縮み、水玉の流れ）の位相と文字の影。
- 反証条件: 投影の拡大・平行移動が 1・0 以外の材質、中心以外の基準点のペインで合わなければ、規則の式が違う（HHD の FLYT の座標生成コードで確かめる = HHD-T006）。

