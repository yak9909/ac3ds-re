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
|0x50|float|char_spacing|7E7D58..64 conditional horizontal advance; 7E83A0..AC cursor X|
|0x54|float|line_spacing|7E7AFC..7E7B48 vertical extent; 8268CC..D8 line advance|
|0x5c|unsigned int|draw_flags|4BAE74 alignment flags; ctor7E84B0 zero|
|0x60|NwFontTagProcessor *|tag_processor|7E849C default; 4BADCC override; 7E7BFC dispatch|


- Ctor 0x7E848Cは基底初期化0x4D5B18を呼び、0x7E849Cは+60に既定TagProcessor、0x7E84A8は+4CにFLT_MAX、0x7E84B0..B8は+58=4,+5C=0,+50/+54=0。基底末尾は+49 byte、TextWriter末尾は+60のpointer。
- 独立CalcStringWidth 0x82690C MOV R2,#0x64 / 0x826914 BL Mem_Copyはwriterを100BだけコピーしCalcStringRectへ渡す。DrawText 0x4BB1F4はSPを68減じ、0x4BB22C/230はSPに同じctorを呼ぶ。領域68や74全体を本体サイズと数えない。
- 型のメンバーは32bit pointer/floatで4バイト自然整列。ゲーム呼び元の一時オブジェクトは8整列のSPに置かれる（MeasureTextのPUSH 20B + VPUSH 8B + SUB 0x74Bで計144B）。8整列で確保すれば既存使用例と一致する。命令だけで8整列を必須ABI属性とは断言しない。
- +0はvptrではない。0x4D5B7Cは0を書き、+4など色に-1を保存する。別CharWriter型は必須でないため追加しない。TextWriterのraw prefixに含め、基底の範囲+0..4Bをコメントした。
- ConfigureTextWriter 0x4BAD80/88はTextBox+E0の書体を+3Cへ保存。0x4BADA0は+E4/+E8からS0/S1を読みRecomputeScaleへ。独立MeasureText 0x5E9458..68も同じ手順。
- RecomputeScale 0x4D51C4..5200は+3Cのfont vt+8/+Cの固有幅高さで要求寸法を割り、0x4D51F4/5200に+24/+28へfloat保存する。倍率そのものを関数へ渡す仕様ではない。直接倍率floatを変える場合の場所は+24/+28。
- +50=char_spacing（字間）、+54=line_spacing（行間）。意味はコピー元の名前ではなく、独立した縦・横の消費側で判定した。
  - CalcLineRect 0x7E7AFCのLDR R1,[R1,#0x24] / 0x7E7B00 BLX R1はfontのget_line_feedを呼ぶ。0x7E7B08 VLDR S0,[R5,#0x54]、0x7E7B0C VLDR S2,[R5,#0x28]（scale_y）、0x7E7B28 VMLA.F32 S1,S3,S2から、0x7E7B44/48で矩形の縦（+4/+C）へ保存する。
  - 独立したGetLineAdvance 0x8268A8もfont vt+0x24を呼び、0x8268CC VLDR S0,[R4,#0x54]、0x8268D0 VLDR S2,[R4,#0x28]、0x8268D8 VMLA.F32 S0,S1,S2で「+54 + lineFeed×scale_y」を返す。
  - CalcLineRect 0x7E7D58 CMP R7,#0 / 0x7E7D5C VLDRNE S0,[R5,#0x50] / 0x7E7D64 VADDNE.F32 S17,S0,S17は先頭以外の文字で横の送りに+50を加える。独立したDrawString 0x7E8328も+50を条件付きで読み、0x7E83A0..ACのVLDR/VADD/VSTRはカーソルX（+2C）へ+50を加算する。
  - ConfigureTextWriter 0x4BADA8/ACはTextBox+EC→writer+54（行間）、0x4BADB0/B4はTextBox+F0→writer+50（字間）を写す。旧版DecorLayout.cppの87行のkBoxCharSpace=0xECとkBoxLineSpace=0xF0は名前が逆。407/408行はゲームと同じずれのコピーであり、名前の根拠にはならない。
  - symbolsの0x4BAD78のF-131コメントにあった「+0xEC char spacing, +0xF0 line spacing」も逆なので「+0xEC line spacing, +0xF0 char spacing」へ訂正した。F0711の「+EC/F0=行間/字間」は正しく、訂正対象ではない。
- +4Cは0x4BADBCのpane幅設定と0x7E7C38の幅制限消費で確認。
- +5CはConfigureTextWriter 0x4BAE74が寄せの組合せflagsを設定。+60はCtorの既定processorとConfigureのoverride、CalcLineRect 0x7E7BFCのdispatchで確認。xrefs.tsvも既定processor 0x97C0B4の初期化→Ctorのreadを示す。
- Dtor 0x4D5BCCはNOP / 0x4D5BD0 BX LR（F0763のAと今回書き出しが一致）。何も解放しない。CalcStringWidthの結果は0x826934..940で矩形right-leftをS0に返す（F0766のABIを維持）。
- 指定の旧版GameLabel.cppは概算の幅を足す実装でTextWriterを呼ばない。実際の計測例はDecorLayout.cppのMeasureText。そこでの0x74確保の+64以降は独自TagProcessorと倍率控えで、本体ではない。ゲーム0x5E9488..98も末尾processorを別に組む。

## 反証条件・未確認点


+58（既定4）はNWのtabWidthに当たる候補（LOW）だが、今回タブ幅としての消費命令は再照合していないため名前を付けない。raw prefixの色・描画状態、base CharWriterの全メンバー名は保留。fontは抽象Fontの型が未登録のためvoid *（ResFont限定と誤らせない）。実機で自前の呼出・整列制約の限界値は未検証。

別ビルド・異なるstride・範囲外アクセスが見つかれば再検討する。
