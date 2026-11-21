---
id: ACNL-F0773
aliases: []
title: "InstSelect8の一覧操作欄と埋込み部品"
summary: "InstSelect8の4812B境界を保ち、Layout・UiAnim・CommonScrollBarと一覧操作用の欄を型付けした。先頭行は埋込みscroll_bar.top_rowであり、行の語はvt[25]から取得する。"
date: 2026-11-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: export-static
addresses: [0x7C6EB0, 0x1C5AC8, 0x1C513C, 0x1AF858, 0x1AF9A0, 0x1B0314, 0x1B0698]
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

InstSelect8の4812B境界を保ち、Layout・UiAnim・CommonScrollBarと一覧操作用の欄を型付けした。先頭行は埋込みscroll_bar.top_rowであり、行の語はvt[25]から取得する。

確度MEDIUM。互いに独立した生成・設定側と利用側の複数の静的命令列が一致。今回は実測なし。

## 根拠

ビルド acnl_jpn_v15。書き出しの元commitは4914ab98f271092df116b05c38a6183939b88b16。現在名はsymbolsから引いた。全関数書き出し all_functions.txt を指定ripgrepの複数行検索で抽出した。抽出スクリプトと命令列は _local/evidence/158/ にある。個別関数ファイルの検索、IDB、gitコマンドは使用していない。
旧版は依頼指定の GameList.cpp・GameLabel.cpp・DecorLayout.cpp（読むだけ）。ソースの定数だけでは命名せず、ゲームの構築・設定側と独立した利用側の命令を照合した。既存知見の事前確認は _local/evidence/158/precheck.txt。F0460/F0492/F0494はS、F0766..F0769はA。F0177/F0178/F0325は?のため手がかりだけに使用。

|ずれ|型|名前|書き出しの命令・根拠|
|---|---|---|---|
|0x0|void *|vptr|F0769|
|0x2c|SsysMaLayoutNode|layout|1C5B10 ctor; 1C5218/21C build|
|0x178|UiAnim|enter_anim|1C5254/258; 1C55BC..D0 bind/start|
|0x1a0|UiAnim|leave_anim|1C5288/28C; CatalogBase ctor|
|0x218|NwLytPane *|frame_pane|1C5374/37C N_frame_00; 1C55F8 consumer|
|0x21c|void *|row_messages|1C52C0..CC alloc row_count*196; 1B02D8..F4 consumer; element type undefined|
|0x220|void *|row_layouts|F0769; 28B elements, +C pane, +10..18 position|
|0x224|CommonScrollBar|scroll_bar|1C5B48 ctor; 1C5434/438 init|
|0x9bc|u8|scroll_kind|1C5B54 default2; 1C5354 init kind|
|0x9c0|int|row_count|F0769=8, number of reusable rows|
|0x9c4|int|item_count|1C5424..30 init N; 1C5518 refresh count|
|0x9c8|unsigned int|text_capacity|1C52F0..F4 alloc message buffer; ctor1C5B6C=0|
|0x9cc|float|row_pitch|1C53B0..BC row0.y-row1.y; scroll init|
|0x9d0|u8|animation_active|1C55DC/5688 set on transition; 1C59F0/5A80 clear|
|0x9d1|u8|input_disabled|1B0320..338 maps to controller bit8; 1C56F4 clear|
|0x9fc|void *|row_nodes|F0769; 1AF898..B0 224B stride|
|0xae4|NwLytPane *|selection_pane|1AFC38/40 P_slct_00; 1AF958..968 prepend|
|0xae8|int|selected_index|1AF8D4 new index; 1B06C0/C4 -1 sentinel|


- CatalogBase_Ctor 0x1C5B10..48はLayout、4個のUiAnim、CommonScrollBarを連続構築。SetupStep 0x1C5218/21Cは+2CをBuild、0x1C5254/58と5288/8Cは+178/+1A0へアニメ資源をLoadする。EnterEnter 0x1C55BC..D0は+178を結合しframe0に戻す。
- 0x7C6EC4..6F08は+AECに28*8、+BCCに224*8を構築し、+220/+9FCにその先頭を保存する。全体4812B境界はF0769の独立した派生ctorとも一致。既存row_layouts/row_nodes/row_countの名前は維持した。
- +940は独立欄ではない。0x224 + 0x71C = 0x940でありscroll_bar.top_rowとして公開。+944の最大値も同様。重複した直接メンバーを作らない。
- +9C4は件数、+9C0は再利用行の数。0x1C5414..5438はrows-1と件数をスクロールへ渡す。+9C8は0x1C52F0/F4で行ごとの文字器確保へ渡る容量で、UTF-16列へのpointerではない。
- 選択+AE8: 0x1AF8D4 STR R7,[R4,#0xAE8]、独立WaitCalc 0x1B06C0/C4で-1判定、0x1B0724..30で決定行+topを保存。+AE4: SetupRowsがP_slct_00を検索保存、選択側がPrependChildする。
- +9D0: 0x1C55DCと5688で入退場時1、0x1C59F0/5A80で完了時0。+9D1: 0x1B0320..338がLDRB→ORRNE/BICEQ #8→ButtonActionControlフラグ+AD4へ反映する。独立0x1C56F4はアニメ解除後0にする。
- 行の語はF0460のvt[25]。旧版ListWordAtも自己の配列から返すだけで、InstSelect8にその配列欄は存在するとの根拠がない。

## 反証条件・未確認点


+AB4（旧版controller+180）は取得済みノードとの比較に使われるが、0x2F7234がcontrol+0xB4へノードpointerを保存し、0x2F72F0が0に戻すことは確認した。ただし選択中・取得済み等の厳密な役割名と完全な型は未確定。+A00のButtonActionControl領域はrawのまま、コメントのみ。+AEC/+BCCは構築strideをコメントしたが要素全型は未復元。row_layouts/row_nodes/row_messagesの要素型未定義のためvoid *を維持。fade系の他のUiAnim欄やその他unk領域も名前を追加しない。実機の入力・破棄・描画は未検証。

別ビルド・異なるstride・範囲外アクセスが見つかれば再検討する。
