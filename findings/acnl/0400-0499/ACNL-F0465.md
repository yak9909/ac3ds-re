---
id: ACNL-F0465
aliases:
- IDA-opus-5.5-F068
title: 'マップエディター第 2 段 — 真ん中のカーソルと A・実行範囲・薄いカーソル（UnitCursor の TEV 段 4 = アルファ × Constant4）（2026-09-29、MEDIUM: 資源の解析＋ホスト試験＋成果物の確認。gohan 実機未確認）'
summary: '解析ソフト: IDA（主 IDB）＋ romfs の UnitCursor.bcres / 解析モデル: opus-5.5。利用者指示（2026-09-28）: 盤面に触れていないときは真ん中に UnitCursor、A でモードの操作（FOXXY と同じ）。'
date: '2026-09-29'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 3141176
- 3132320
- 3132628
- 3133020
- 3133540
tags:
- map
supersedes: []
source: IDA:work/FINDINGS.md:1470-1512
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F068: マップエディター第 2 段 — 真ん中のカーソルと A・実行範囲・薄いカーソル（UnitCursor の TEV 段 4 = アルファ × Constant4）（2026-09-29、MEDIUM: 資源の解析＋ホスト試験＋成果物の確認。gohan 実機未確認）

解析ソフト: IDA（主 IDB）＋ romfs の UnitCursor.bcres / 解析モデル: opus-5.5。利用者指示（2026-09-28）: 盤面に触れていないときは真ん中に UnitCursor、A でモードの操作（FOXXY と同じ）。
十字上下で実行範囲（奇数、最大 7x7）、十字左右は何もしない、盤面はスライドパッドだけ。真ん中以外は薄く（項目で調整）。削除・選択は範囲内のアイテムをハイライト（カーソルを二重に出さない）。
スポイトは 1x1 に固定（モードを変えたら元の範囲）。範囲選択の A = タッチで範囲を引いたのと同じ選択、A を押したまま盤面を動かすとその方向へ広げる。UnitCursor はマイデザインの上だけ薄く。
- **UnitCursor の TEV**（Ftr/Chip/UnitCursor.bcres、ファイル 0xCD0 から 6 段 × 28 B、見出し 0x804F00C0/C8/D0/D8/F0/F8）: 段 0（Constant0、入力 0x0E430EE4）・段 1（Constant1、0x03EF0FE4、MULTIPLY_ADD）だけ使い、
  段 2〜5 は素通し（入力 0x0E1F0E1F・オペランド 0・合成 0）。色付け（F013 の PlanBlock）は段 5 と Constant5。
- **アニメが書く物**（CANM の DICT を解いた名前）: 0x1148 の常時アニメ = Constant0・Constant1・TexCoord1.Translate、0x161C の向き = TexCoord1.Rotate。**Constant4 / 5 は書かない**。
- **薄い体**: 段 4 を「色 = 前段（REPLACE）、アルファ = 前段 × Constant4.a（MODULATE）」（入力 0x00EF000F、合成 0x00010000、定数 4）。資源の TEV は全インスタンスで共有、Constant4 は体ごと（bufferOption 0x834）
  → 普通の体は Constant4 = 0xFF000000（そのまま）、薄い体は項目の値（既定 96）。薄い体が同じ TEV を指していることを確かめてから使う。ヒープは体 1 つ分増やした（2 + マスの色 2）。
  マス指定の形（エディター）だけ作る。束は「普通 → 薄い」の 2 つ。マイデザイン（Field_GetItemAtXY 0x2FEE38 の (item & 0x7FFF) == 0x9D）のマスは呼ぶ側に関係なく薄い（毎フレーム見る）。
- **マップエディター**: 盤面に触れていない・持ち上げていない・一覧が出ていない間は、真ん中（盤面 + kView/2）を中心に一辺 1/3/5/7 のカーソル（真ん中以外は薄い、ほかのカーソルと同じマスは足さない）。
  A（メニュースレッドが通算を進め、描画スレッドがタッチの後に行う）: 配置 = 範囲の空きに置く、削除 = 消す、範囲選択 = 範囲を選ぶ（SelectOn の音）＋ A を押したまま盤面が動くと押したときの範囲と今の範囲を囲む四角へ（RangeStep の音）、
  スポイト = 真ん中を拾って配置モードへ。削除・範囲選択・スポイトは範囲のアイテムを赤（スポイトは青）。十字上下 = 範囲（スポイト中は変えない）、盤面はスライドパッドだけ。
- **描画順の条件**（利用者指示 2026-09-29）: マイデザインを先に描くのは groundFirst の登録（エディターのカーソルとマスの色）があるフレームだけ。単独のグリッドカーソル（足元の形）では並べ替えない。
- 検査: test_map_select 0 失敗（試験 25 = 10 項目、旧試験 5 項目を真ん中のカーソル込みに更新）、test_map_trace PASS、verify_map_editor 0（群 18 = 5 項目: TEV の段・アニメの名前・段 4 と Constant4・薄い体・十字と A）、
  building 0、publicworks 99/0、gridcursor 76/0。成果物: FrameCallback に 0x0E1F0E1F / 0x00EF000F / 0x2FEE38 と (item << 17 >> 17) − 157 の比較。gohan ce082f8。
- 未確認: 木の影がマイデザインに乗る（利用者報告 2026-09-29）。影は別の資源（Shadow/sdw_fg_tree*.bcres、BsShadowMapMgr / BsShadowViewMgr）で、描く順はまだ調べていない。
  エディターを切れば並べ替えないので、そのときの見え方と比べれば元のゲームと違うかが分かる。
- 反証条件: 薄いカーソルが消える・濃さが変わらない・色付けが崩れる、A が触れている間にも働く、範囲選択の拡張が逆向き、スポイト後に範囲が戻らない。
- **追記（2026-09-29、利用者: ce082f8 の 1〜7 PASS、木の影は元のゲームと同じ扱いで問題なし）→ gohan e781297（実機未確認）**:
  - 薄い体を 2 つに（kDimKinds = 2。dims 1 = 実行範囲の真ん中以外 90、2 = マイデザインの上 50。利用者の決定）。どのマスを薄くするかは呼ぶ側だけが決める
    （GridCursor のマイデザイン判定は削除 → 公共事業エディターでは薄くしない。マップエディターは PublishCursor の全カーソルで (item & 0x7FFF) == 0x9D なら 2）。
  - 色の入れ替え: 盤面は地（P_Room_00 の自分の材質）を白 → 地の色 5x5 → 白 3x3 → 地の色 1x1。上画面のマスの色は白だけ（kMarkKinds = 1）で、5x5 の輪郭と中心には置かない。
  - ハイライトはマスごとの種類（MapEditor3D: 赤 = 触れている・選択・削除、青 = スポイト、白 = 配置モードの中心マス）。濃さ = TEV 段 5 の定数アルファ（既定 赤 192・青 192・白 128、項目で調整）。
  - A で範囲選択 → A を離したときに一覧（盤面の中心のマス）。一覧に「移動」（埋めるの下。決定音は表に移動の種類が無いので 0 DECIDE）。「複製」「移動」の待ちは A でも置ける（盤面をずらした分）。
  - 配置モードの名前はスポイトと同じく指に追従（押し始め・なぞり・離さず移動のたびに指の下のマスの名前、物が無ければ消す）。
  - 検査: test_map_select 0（試験 26 = 9 項目）、trace PASS、verify_map_editor 0（群 19 = 5 項目、群 14/15/18 と一覧の音を更新）、building 0、publicworks 99/0、gridcursor 76/0。見本 board7 を再生成。
- **追記 2（2026-09-29、利用者: e781297 の 1〜7 PASS）→ gohan 94d98cf（実機未確認）**:
  - ハイライトの濃さを固定（赤 150・青 80・白 40、項目は外した）。配置モードの触れている所・名前の物は白。モード切替の通知は出さない。
  - ボタン: L = 実行範囲を縮小・R = 拡大（スポイト中は変えない）、十字上 = 一覧の 1 つ上のモード・下 = 1 つ下。
  - カメラ: 見る位置は中心の 1 マス南のまま、高さは中心マスの地面（GroundHeight を中心で取る）。
  - 盤面のコマの色をゲームの分類関数と同じ規則で: Item_IsBuriedFlag 0x2FCBA0（*(u16 *)(item+2) の bit15 = 32 ビットの bit31。LDRH [R0,#2]; LSR #15）= 茶、
    id > 0xFD（Item_GetCategory 0x2FCCD4 が 29 を返す物）= 黄、区分 10 岩 = 灰色寄りの白、24 マイデザイン = 水色、9 雑草・21 クローバー = C の元の色（黄緑）、
    Item_IsFlowerCategory 0x2FCE5C（11〜17・20 タンポポ・27・28）+ 19 枯れた花 = ピンク、ほかの fgobj（木・株・竹・ラフレシアなど）= 濃い緑。
    Item_GetCategory は R0 の品物の番地をそのまま Item_GetFieldObjDef 0x2FD064 へ渡す（逆アセンブルで確認）。区分の一覧は Fg.bin（work/cache/fg_param_all.txt）。
  - 検査: test 0、trace PASS、verify_map_editor 0（カメラ・一覧の指・十字と L/R・項目・白・コマの色の分類）、building 0、publicworks 99/0、gridcursor 76/0。
- **追記 3（2026-09-29、利用者: 94d98cf の 1〜5 PASS。コマの配色を色覚の多様性に配慮した色に、お任せ）→ gohan ee2b013（実機未確認）**:
  Okabe-Ito の 8 色 + 岩の明るい灰色: 雑草・クローバー #009E73、ほかの fgobj #0072B2、花・枯れた花 #CC79A7、アイテム #F0E442、埋まっている物 #D55E00、
  マイデザイン #56B4E9、建物 #E69F00、岩 #DCDCDC（黒色 = 白色 × 0.45）。全部の種類を塗る（雑草・クローバーも）。
  見え方の真似（Machado 2009、tools/layout/chip_colour_cvd.py、結果 work/evidence/map_editor/chip_colours/cvd_check.json）の最小 ΔE: 通常 26.4・1 型 20.7・2 型 17.0・3 型 16.1。
  前の配色は 1 型 7.6（木と建物）・2 型 5.8（アイテムと雑草）で見分けにくかった。verify_map_editor 群 20（どの型も 15 以上）。

