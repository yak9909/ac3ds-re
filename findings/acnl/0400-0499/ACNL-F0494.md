---
id: ACNL-F0494
aliases:
- IDA-opus-5.5-F039
title: '一覧の切り抜きは N_frame_00 から作るシザー。一覧の Layout は自前のデータで先に組み立てられる（2026-09-25、MEDIUM: 静的＋利用者の見た目の報告。組み立ては実機未確認）'
summary: '`sub_1C55F8`（組み立て段 2 から呼ばれる）: N_frame_00（一覧+536）の大域行列の位置と大きさから、一覧+356 = 1、+360/+364 = 画面の x/y（回した座標）、+368/+372 = 幅/高さを置く。一覧+356 は ssys Layout（一覧+44）の +312 にあたる切り抜き。行の 7 行目が半分隠れるのも、名前の左の空き（N_frame_00 の左端 62.5 より左）に置いた文字が見えないのもこの切り抜き（利用者は「リスト'
date: '2026-09-25'
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5670308
tags:
- layout
supersedes: []
source: IDA:work/FINDINGS.md:2128-2135
by: opus-5.5
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F039: 一覧の切り抜きは N_frame_00 から作るシザー。一覧の Layout は自前のデータで先に組み立てられる（2026-09-25、MEDIUM: 静的＋利用者の見た目の報告。組み立ては実機未確認）

- `sub_1C55F8`（組み立て段 2 から呼ばれる）: N_frame_00（一覧+536）の大域行列の位置と大きさから、一覧+356 = 1、+360/+364 = 画面の x/y（回した座標）、+368/+372 = 幅/高さを置く。一覧+356 は ssys Layout（一覧+44）の +312 にあたる切り抜き。行の 7 行目が半分隠れるのも、名前の左の空き（N_frame_00 の左端 62.5 より左）に置いた文字が見えないのもこの切り抜き（利用者は「リストの上にシェイプが描かれて隠れている」と報告）。
- `ssys_ma_lyt_Layout_Build 0x5685A4`: Layout+32 が 0 でなければすぐ 1 を返す。組み立ての本体は accessor（holder+4）の vt[2]('blyt', 名前, 0) で得たデータを `nw::lyt::Layout::Build` `sub_4B9474(L+16, data, accessor)` へ渡すだけ（前後にコマンドリストの用意: GetProperty(519) / GenCmdlists / SelectList / CmdlistStorage）。→ InstSelect の組み立て段 0（`sub_1C513C`）より前に、同じ手順で書き換えたデータを使って組み立てておけば、段 0 はそれを使う。
- 選択中の色: アニメ `ctlg_cntnt_00_select.bclan` は CLMC（マテリアルの色）でマテリアル `T_itm_XX` を動かす。`_touch` は CLPA（ペインの SRT）で `T_itm_XX` を動かす。
- gohan（8ccc6f9、実機未確認）: ctlg_cntnt_00.bclyt を写し、T_itm_XX の後ろに T_id_XX（x = -42、幅 36、右寄せ、文字の大きさ 0.65 倍、マテリアル番号は同じ）を足し、N_frame_00 を左へ 26 広げる（左端 -97.5 → -123.5、右端は同じ）。`tools/layout/check_id_layout.py` で同じ手順を Python で組み、構造を検査（PASS）。毎フレーム T_itm の Material の色 7 個・文字色・位置の差分・拡大率を T_id へ写す。
- 反証条件: 実機で組み立て中に落ちる／ID が出ない（→ データか手順の誤り）／名前の行が崩れる。

