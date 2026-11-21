---
id: ACNL-F0775
aliases: []
title: "TextWriterの100バイト実体と書体倍率設定"
summary: "nw::font::TextWriterは100B（0x64）。書体は+0x3C、倍率floatは+0x24/+0x28。RecomputeScaleは要求する幅・高さをS0/S1で受け、書体の固有寸法で割る。"
date: 2026-11-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: export-static
addresses: [0x7E8488, 0x4D5B18, 0x4D5BCC, 0x8268E0, 0x4BAD78, 0x4D51B0, 0x5E9430, 0x4BB1E8]
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

nw::font::TextWriterは100B（0x64）。書体は+0x3C、倍率floatは+0x24/+0x28。RecomputeScaleは要求する幅・高さをS0/S1で受け、書体の固有寸法で割る。

確度MEDIUM。互いに独立した生成・設定側と利用側の複数の静的命令列が一致。今回は実測なし。

## 根拠

ビルド acnl_jpn_v15。書き出しの元commitは4914ab98f271092df116b05c38a6183939b88b16。現在名はsymbolsから引いた。全関数書き出し all_functions.txt を指定ripgrepの複数行検索で抽出した。抽出スクリプトと命令列は _local/evidence/158/ にある。個別関数ファイルの検索、IDB、gitコマンドは使用していない。
旧版は依頼指定の GameList.cpp・GameLabel.cpp・DecorLayout.cpp（読むだけ）。ソースの定数だけでは命名せず、ゲームの構築・設定側と独立した利用側の命令を照合した。既存知見の事前確認は _local/evidence/158/precheck.txt。F0460/F0492/F0494はS、F0766..F0769はA。F0177/F0178/F0325は?のため手がかりだけに使用。

|ずれ|型|名前|書き出しの命令・根拠|
|---|---|---|---|
|0x24|float|scale_x|4D5BA8 default1; 4D51F4 width/font width|
|0x28|float|scale_y|4D5BAC default1; 4D5200 height/font height|
|0x3c|void *|font|4BAD80/88 TextBox font; 4D51C4 virtual metrics; abstract Font type undefined|
|0x4c|float|width_limit|7E84A8 FLT_MAX; 4BADBC pane width; 7E7C38 consumer|
|0x50|float|line_spacing|4BADB0/B4; 5E947C/80; 7E7D5C consumer|
|0x54|float|char_spacing|4BADA8/AC; 5E946C/78; 7E7B08 consumer|
|0x5c|unsigned int|draw_flags|4BAE74 alignment flags; ctor7E84B0 zero|
|0x60|NwFontTagProcessor *|tag_processor|7E849C default; 4BADCC override; 7E7BFC dispatch|


- Ctor 0x7E848Cは基底初期化0x4D5B18を呼び、0x7E849Cは+60に既定TagProcessor、0x7E84A8は+4CにFLT_MAX、0x7E84B0..B8は+58=4,+5C=0,+50/+54=0。基底末尾は+49 byte、TextWriter末尾は+60のpointer。
- 独立CalcStringWidth 0x82690C MOV R2,#0x64 / 0x826914 BL Mem_Copyはwriterを100BだけコピーしCalcStringRectへ渡す。DrawText 0x4BB1F4はSPを68減じ、0x4BB22C/230はSPに同じctorを呼ぶ。領域68や74全体を本体サイズと数えない。
- 型のメンバーは32bit pointer/floatで4バイト自然整列。ゲーム呼び元の一時オブジェクトは8整列のSPに置かれる（MeasureTextのPUSH 20B + VPUSH 8B + SUB 0x74Bで計144B）。8整列で確保すれば既存使用例と一致する。命令だけで8整列を必須ABI属性とは断言しない。
- +0はvptrではない。0x4D5B7Cは0を書き、+4など色に-1を保存する。別CharWriter型は必須でないため追加しない。TextWriterのraw prefixに含め、基底の範囲+0..4Bをコメントした。
- ConfigureTextWriter 0x4BAD80/88はTextBox+E0の書体を+3Cへ保存。0x4BADA0は+E4/+E8からS0/S1を読みRecomputeScaleへ。独立MeasureText 0x5E9458..68も同じ手順。
- RecomputeScale 0x4D51C4..5200は+3Cのfont vt+8/+Cの固有幅高さで要求寸法を割り、0x4D51F4/5200に+24/+28へfloat保存する。倍率そのものを関数へ渡す仕様ではない。直接倍率floatを変える場合の場所は+24/+28。
- +54=char spacing / +50=line spacing は0x4BADA8..B4と独立0x5E946C..80のコピーが一致。CalcLineRect 0x7E7B08が+54、0x7E7D5Cが+50をfloatとして使う。+4Cは0x4BADBCのpane幅設定と0x7E7C38の幅制限消費で確認。
- +5CはConfigureTextWriter 0x4BAE74が寄せの組合せflagsを設定。+60はCtorの既定processorとConfigureのoverride、CalcLineRect 0x7E7BFCのdispatchで確認。xrefs.tsvも既定processor 0x97C0B4の初期化→Ctorのreadを示す。
- Dtor 0x4D5BCCはNOP / 0x4D5BD0 BX LR（F0763のAと今回書き出しが一致）。何も解放しない。CalcStringWidthの結果は0x826934..940で矩形right-leftをS0に返す（F0766のABIを維持）。
- 指定の旧版GameLabel.cppは概算の幅を足す実装でTextWriterを呼ばない。実際の計測例はDecorLayout.cppのMeasureText。そこでの0x74確保の+64以降は独自TagProcessorと倍率控えで、本体ではない。ゲーム0x5E9488..98も末尾processorを別に組む。

## 反証条件・未確認点


+58（既定4）の意味名、raw prefixの色・描画状態、base CharWriterの全メンバー名は保留。fontは抽象Fontの型が未登録のためvoid *（ResFont限定と誤らせない）。実機で自前の呼出・整列制約の限界値は未検証。旧F0711本文の表は+EC/F0を「行間/字間」と書くが、コピー命令と旧版定数は逆順「字間/行間」。表の語順訂正を提案する（旧記録は未変更）。

別ビルド・異なるstride・範囲外アクセスが見つかれば再検討する。
