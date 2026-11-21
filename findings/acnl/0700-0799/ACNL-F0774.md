---
id: ACNL-F0774
aliases: []
title: "CommonScrollBarの実体境界とドラッグ用の欄"
summary: "CommonScrollBarは1944B（0x798）。埋込みLayoutは+0x24C、ドラッグ中の旗は+0x6FA、入力モードは+0x744。先頭行と最大値は+0x71C/+0x720である。"
date: 2026-11-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: export-static
addresses: [0x299FE8, 0x298664, 0x2987A8, 0x299910, 0x298BA8, 0x2993E4, 0x299590, 0x2997B0, 0x29915C]
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

CommonScrollBarは1944B（0x798）。埋込みLayoutは+0x24C、ドラッグ中の旗は+0x6FA、入力モードは+0x744。先頭行と最大値は+0x71C/+0x720である。

確度MEDIUM。互いに独立した生成・設定側と利用側の複数の静的命令列が一致。今回は実測なし。

## 根拠

ビルド acnl_jpn_v15。書き出しの元commitは4914ab98f271092df116b05c38a6183939b88b16。現在名はsymbolsから引いた。全関数書き出し all_functions.txt を指定ripgrepの複数行検索で抽出した。抽出スクリプトと命令列は _local/evidence/158/ にある。個別関数ファイルの検索、IDB、gitコマンドは使用していない。
旧版は依頼指定の GameList.cpp・GameLabel.cpp・DecorLayout.cpp（読むだけ）。ソースの定数だけでは命名せず、ゲームの構築・設定側と独立した利用側の命令を照合した。既存知見の事前確認は _local/evidence/158/precheck.txt。F0460/F0492/F0494はS、F0766..F0769はA。F0177/F0178/F0325は?のため手がかりだけに使用。

|ずれ|型|名前|書き出しの命令・根拠|
|---|---|---|---|
|0x0|void *|vptr|299FF0/FF4; vt[4] takes local point|
|0x4|ArcResAccReader|arc_reader|299FF8; F0768|
|0x24c|SsysMaLayoutNode|layout|29A000 ctor; 2986D4/D8 touch transform|
|0x398|UiAnim|select_anim|299958/95C select resource|
|0x3c0|UiAnim|touch_anim|299968/96C touch resource|
|0x3e8|UiAnim|kind_anim|299978/97C kind resource|
|0x410|UiAnim|ng_anim|299988/98C ng resource|
|0x6f8|u8|input_disabled|299E40 setter; controller flags bit8 at 6DC|
|0x6fa|u8|drag_active|2982F8=1; 2997BC=0; 298674 gate|
|0x71c|int|top_row|2987B0 store; signed clamp at 2987BC..D4|
|0x720|int|max_top_row|299AD4..AF0 max(0,N-V+1); SetPos clamp|
|0x724|float|row_offset|299440/444 remainder; 29886C clears|
|0x744|u8|input_mode|299194/198=2 touch; 29931C/338=3 hand|
|0x748|float|row_pitch|299998/9A4; 299414/41C divide|
|0x74c|unsigned int|row_limit|2999C4/C8 rows-1; CalcKnob uses row_limit-1|
|0x750|unsigned int|item_count|2999A8/9B4; CalcKnob division|
|0x760|void *|callback_context|29A10C stores ctor R1; 29950C loads before callback|
|0x764|NwLytPane *|knob_pane|2995A4 N_btn_00; 2987E0/8818 translate|
|0x788|NwLytPane *|all_pane|299634 N_All; 299B2C/B44 visible|


- CatalogBase_Ctor 0x1C5B48は一覧+224に構築、0x1C5B54は次の+9BC byteを初期化。0x9BC-0x224=0x798。CommonScrollBar自身のctor最終store 0x29A13C [R0,#0x794]とも一致するため、単なるprefixではなく実体境界として扱う。
- 0x299FF4は+4へArcResAccReader、0x299FFC..29A000は戻り+248（全体+24C）へLayoutを構築。独立UpdateDrag 0x2986D4 ADD R0,R4,#0x24C / 0x2986D8 BL Layout_TransformTouchPixelsToLocal。旧版半倍率も同じLayoutで開始位置と現在位置を変換する。
- 旧版の持ち主判定はscroll == list+548。+760はctor R1とコールバックのcontextであり、普遍的なownerクラスのpointerとは断定しない。一覧のctorではR1=thisなのでcallback_contextは一覧を指す。持ち主判定用の別名ownerは作らない。
- +6FAは0x2982F8でtouch開始時1、EndDrag 0x2997BCで0。UpdateDrag 0x298674..84は+6FA!=0かつ+6FB!=1のみ通す。+6FBは0x299C54..5Cで毎フレーム1をクリアし、0x2990E0で書かれるが意味名は保留。
- SelectInputMode 0x299164..198はtouch held/previous held→+744=2、0x2992F8..338は手カーソル状態→3または0。UpdateDragの0x298688..98で2/3を分岐。enum全体は未定義、byteのまま。
- Init 0x299AD4..AF0はmax(0,N-V+1)を+720へ保存。SetPosの0x2987B0..D4は+71Cをsigned clamp。独立UpdatePositionFromKnob 0x2993FC..444も+71Cと+724を更新する。
- FindPanes 0x2995A0/A4はN_btn_00→+764、0x299630/34はN_All→+788。SetPosは前者のtranslationを変え、CalcKnob/Initは後者の表示bitを読む/書く。データ参照もxrefs.tsvの0x854D58→0x299590、0x854CE4→0x299590で一致。
- 旧版の0.5はゲーム構造体の倍率欄ではなく変換後のローカル座標差に掛ける値。UpdateDrag末尾0x298774..784はvt[4](this,point)を呼ぶ。+748は行間であってドラッグ倍率ではない。

## 反証条件・未確認点


+6FBはbyteの抑制ゲートという命令事実だけコメント。その他raw領域（特に+6DCのnested controller、座標履歴・比率・callback関数pointer・pane群）は必要箇所の意味を本文で示すにとどめ完全定義を主張しない。サイズは静的な境界で、実機で別の派生や割当を測定していない。

別ビルド・異なるstride・範囲外アクセスが見つかれば再検討する。
