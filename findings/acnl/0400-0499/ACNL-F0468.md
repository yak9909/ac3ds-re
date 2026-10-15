---
id: ACNL-F0468
aliases:
- IDA-opus-5.5-F065
title: 'マップエディターのスポイトモード（一覧 4 行・窓の拡張）、Y、モードごとの UnitCursor の色、下画面左上の箱、マスの色の手直し（2026-09-28、MEDIUM: 静的＋描画器＋ホスト試験。gohan 実機未確認）'
summary: '解析ソフト: IDA（主 IDB）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示（5540abf の確認後）: 黄 → 青、真ん中を白（上下とも）、濃さ 50 で決定、'
date: '2026-09-28'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 4939996
- 2244964
- 4210943
- 5881836
- 5668912
tags:
- map
supersedes: []
source: IDA:work/FINDINGS.md:1564-1598
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F065: マップエディターのスポイトモード（一覧 4 行・窓の拡張）、Y、モードごとの UnitCursor の色、下画面左上の箱、マスの色の手直し（2026-09-28、MEDIUM: 静的＋描画器＋ホスト試験。gohan 実機未確認）

解析ソフト: IDA（主 IDB）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示（5540abf の確認後）: 黄 → 青、真ん中を白（上下とも）、濃さ 50 で決定、
スポイトモード（離したマス・タッチ中は青のハイライト・名前枠が指に追従・拾ったら配置モード）、Y で中心をスポイト、モードごとの UnitCursor の色、
下画面左上に「配置: {アイテム名}」（左揃え、没アイテム表示と同じ名前の取り方）、上画面のマスの色をマイデザインより上に。
- **モード一覧 4 行（窓の拡張）**: W_list_win_00 は行の親で、行のアニメが絶対の y を書くので窓だけを動かせない（F062）。
  → 使わない行 N_icon_06 を「代わりの親」にして窓と同じ位置（16, −2）に置き、窓の子（P_list_win_00・P_tag・P_list_note_00・P_list_arrow_00・N_slct_00・N_icon_00..05・P_list_btn_R/L）を
  AppendChild（0x4B60DC）で移し、子の無い窓を 4 行ぶん（高さ 110.5、y 33.25）に置く。★ResetRowButtons 0x224164（SelectById が呼ぶ）は N_icon_00..06 の位置を
  list +5992 + 228i の保存値へ戻すので、行 6 の保存値にも代わりの親の位置を書く。一覧全体は N_All の y = −20（左上の箱の下）。
  文字は T_msg の幅 36.4（sub_5E91F0 が幅に収まるよう書体を横に縮める）で「スポイト」が収まる。描画器 tools/layout/mode_list_preview.mjs、タッチの枠 {0,74,36,159}。
- **スポイト**（描画スレッド）: 押す = TouchKind::Spoit、指の下のマスの名前を出す。名前枠は基準ペインを盤面の中心 s_roomPane にし、ずれ = 指の位置 − 盤面の大域位置
  （NameShow の第 4 引数）。動かす = 指の下のマスへ名前を差し替え。離す = そのマスを PickAt（id & 0x7FFF = 長押しのスポイトと同じ）→ RequestMode(Place)
  （s_modeReqSeq/Value 経由でメニュースレッドが s_mode へ移す。一覧で選んだときと同じ道）。空のマスでは何もしない。
- **Y**: メニュースレッドが s_spoitCenterSeq を進め、描画スレッドが PickAt(vx + kView/2, vy + kView/2)。
- **UnitCursor の色**（ApplyModeLook、モードが変わったときだけ）: 配置 = SetTint(0,0)（色合成なし）、削除 = 赤 0x000000FF、範囲選択 = いまの kCursorBlue、
  スポイト = 青 0x00FF2000。実体のハイライト（MapEditor3D::SetHighlightColor）はスポイトの間だけ青 0x00FF6020、ほかは従来の 0x004040FF。
- **左上の箱**: GameLabel の箱 0（公共事業エディターの鐘の箱 time_bel_win）を下画面へ（AddLayout の画面 1、左 −152）、文字位置 3（左寄せ）。
  名前は ItemNames::NameUtf8（没アイテム表示と同じ）。箱は公共事業エディターと共有なので、BuildingEditor 側で下画面・左寄せを明示的に戻す。
- **マスの色**: 種類 2（白 = 距離 0 と 2 の 17 マス、青 0x00FF0000 = 32 マス）、アルファ 50 固定（一時の濃さ項目は外した）。盤面の真ん中も P_door_00 を
  自分の材質で白の 1x1 板にした（材質の差し替えと RestoreBoardParts は廃止）。
- **マイデザインより下に出た件（5540abf の 3 NG）**: 静的には原因未特定（F064 の層 0 の振り分けではマイデザインは層 0）。描く段を一時項目「マスの色を描く段（仮）」で
  0 = 層 0 の後 / 1 = 層 1 の前（fgobj の cb1 0x59BFEC を包む UnderCb1）/ 2 = 自前の描画ノード（既定。以前の UnitCursor がマイデザインの上に出ていた形）に切り替えて実機で確かめる。
- 検査: verify_map_editor 0 失敗（群 13〜15 を更新: 4 行・代わりの親・段 0/1/2・種類 2・真ん中の白）、test_map_select 0 失敗（試験 24 = スポイト）、
  verify_building_editor 0、verify_gridcursor 76/0。ビルド work/logs/gohan_build_spoit2.log（警告は従来の 2 件）。
- 反証条件: 一覧の 4 行目が欠ける・窓がずれる・選び直しで行がずれる、名前枠が指に付いてこない、離したマスと違う物を拾う、Y で中心以外を拾う、
  色がモードと違う、左上の箱が出ない・公共事業エディターの箱が崩れる、どの段でもマスの色がマイデザインの下。
- **追記（2026-09-28、利用者の実機確認: 5 以外 PASS）**:
  - **マスの色の段 = 自前の描画ノードで確定**（利用者: 2 のときだけマイデザインの上に出た。0 = 層 0 の後・1 = 層 1 の前はどちらも下）。一時項目を外し、DrawMarks は InstancedDraw::Submit だけ。
  - **下画面の箱が左上の端に無く、文字がはみ出た → 原因 HIGH（静的 2 経路＋写真の実測）**: nw::lyt::Layout::Build sub_4B9474 は節 'lyt1'（829716844）で
    *(u64 *)(Layout+0x28) = *(u64 *)(節+12)（bclyt の幅・高さ）を写し、LayoutCalc 0x568030 が毎回 sub_73BAC0 でそこから正射影（±幅/2, ±高さ/2）を作る。
    time_bel_win.bclyt の lyt1 は 400x240（上画面用。下画面の map_village / chip の bclyt は 320x240）→ 下画面では横が 320/400 に縮み中心へ寄る。
    写真（work/evidence/map_editor/place_label/）の箱 x 45..180・文字 x 43..146 は、縮まない場合の予測 8..198 ではなく、縮む場合の 38..190（丸い端の透明ぶんを除く）に合う。
    → 下画面に出す間は Layout+0x28 = 320（LayoutCalc の前に毎フレーム。上画面では bclyt の値に戻す）。左揃えの文字枠は幅 − kPad（左右 30 ずつ）で丸い端に掛けない。
    予測: 箱 x 8..198、y 8..31、文字の始まり x ≈ 30。検査 verify_map_editor 群 16。gohan f440226。

