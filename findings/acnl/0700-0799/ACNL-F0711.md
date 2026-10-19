---
id: ACNL-F0711
aliases: []
title: "TextBox と ResFont の文字描画用構造および既定 TagProcessor"
summary: "TextBoxと文字バッチ、ResFontと正規化されたFINF/TGLP/CWDH/CMAP、既定wide TagProcessorを型にした。ResFontは通常確保0x18と独立した埋込み境界が整合し、0x20にはしない。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x008FC07C, 0x008FCAAC, 0x008FCA24, 0x0097C0B4, 0x0097C0B0, 0x004B4AB4, 0x0052D8EC, 0x0079B70C, 0x00743768, 0x007438B4]
tags: ["layout", "font", "rtti"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

`NwLytTextBox` (0x108)、文字バッチ先頭0x28、`NwFontResFont`、正規化されたフォント資源本体とvtable、既定wide TagProcessorを型にした。旧実験 [ACNL-F0326] は格付け?のため今回の確度根拠には数えず、各本体の生産/消費を照合した。
確度 MEDIUM：資源工場・ctor・文字列確保・batch構築/提出と、独立したfont初期化・資源parse・glyph取得が整合。実機なし。

**ResFontは0x18バイトである。** 依頼の0x20とは異なる。通常確保が0x18で、別クラス内のResFont開始+0x178から次のメンバー+0x190までの差も0x18。末尾に未確認の8Bを付け足すと実際のオブジェクト境界を越えるため採用しない。

| 型/大域 | 確認した内容 |
|---|---|
| TextBox | +0xD4 UTF16列、+0xD8/DC上下色、+0xE0 font、+0xE4/E8文字幅高さ、+0xEC/F0行間/字間、+0xF4 processor、+0xF8バイト容量、+0xFA文字数、+0xFC/FD配置、+0xFE dirty、+0x100 Material、+0x104 batch |
| batch先頭0x28 | +0最大字数、+8構築済、+9 flags、+0xC文字bits、+0x10現在commands、+0x14本来のcommands、+0x18補助buffer、+0x1C使用語数、+0x20容量語数 |
| ResFont 0x18 | +4 resource、+8 FINF本体、+0xC glyph texture記述子列（stride0x14）、+0x10 filter flags、+0x14/16文字/glyphキャッシュ |
| FINF本体0x18 | +1 line feed、+2代替glyph、+4既定幅3B、+7 encoding、+8 TGLP、+0xC CWDH、+0x10 CMAP、+0x14/15/16高さ/幅/ascent |
| TGLP本体0x18 | +0/1 cell幅高さ、+2 baseline、+3最大字幅、+4 sheetサイズ、+8枚数、+0xA書式、+0xC/E列/行数、+0x10/12寸法、+0x14データ |
| CWDH先頭8B | +0/2 glyph区間、+4次、+8以降にleft/glyph_width/char_widthの3B列 |
| CMAP先頭0xC | +0/2文字区間、+4方式、+8次、+0xC以降に方式依存データ |
| 0x0097C0B4 | `g_DefaultWideTagProcessor`。ポインタの格納欄ではなくvptr1語の実オブジェクト |
| 0x0097C0B0 | `g_DefaultWideTagProcessorGuard`。bit0を読む4B guard語。boolへ縮めない |

FINF等の型の先頭は8Bのブロックヘッダより後の**本体**である。CWDH/CMAPとbatchは可変長全体のsizeofではなく、確認した固定先頭部分のみを表す。

## 根拠

一次証拠：`_local/evidence/98/primary.txt`、原本vtable/範囲ハッシュと計算 `primary-index.json`、型照合 `type-verification.json`。

- `0x4B8D14` のTextBox分岐は0x108確保。`0x4BB2A4` と `0x4BB084` が欄を初期化し、`0x13B9A8` は `2*(N+1)` を別確保して+0xF8へ保存。文字列とbatchは別確保である。
- `0x4BAFB0` は+0x104のbatchをwriterへ設定し、+0xFE dirty時は+0xD4/+0xFAで文字列を処理。`0x73CF48` の4引数入口は長さ/font/materialを確認し、`0x4B7CE0`→`0x4D520C` がbatch+0x1C語をcursorへ提出する。`0x4D76BC` の初期化と独立した提出側でbatch欄を照合した。
- `0x4B4AEC` は `MOV R0,#0x18`、直後AllocMemoryして `0x4B4AFC` でResFont ctor。別の `0x52D9A8` も同ctorを呼び、`0x52D9AC` がthisを0x178戻し、`0x52D9B0` が+0x190へ書く。差は道具で0x18と計算。`0x4D7590` は末尾の+0x14/16を初期化し、実体範囲と整合する。
- `0x4D8048` のparseはFINF等のchunk先頭を走査し、本体はchunk+8として `0x4D7468` に渡す。FINF/CWDH/CMAP/TGLP内部のファイル相対offsetをresource基底からの実ポインタへ直す。正規化前のファイルへ今回のポインタ型をそのまま当てない。
- `0x743768` はFINF+0x10からCMAP鎖を辿り、方式0は差分、1は直表、2は組の二分探索。結果をResFont+0x14/16に保存。`0x7438B4` は代替glyphとCWDHの3B幅、TGLPのsheet/列行数からglyphを作る。取得子 `0x7436F0` と `0x743A40/74/68`、サイズ設定側も整合。
- `0x79B750..64` が0x97C0B0のwordを読みbit0を検査、guard acquireへその番地を渡す。`0x79B774..80` は0x97C0B4へwide版vtableを書き、独立したTextWriter ctor `0x7E8488` は同番地そのものをwriter+0x60へ保存する。TagProcessor vslot+8/+0xCは `0x7E877C/0x7E8854`。Tab/改行の処理と矩形計算を確認した。

## 反証条件・未確認点

- 0x20が別の派生/別ビルドの実体を意味する資料があれば対象を分ける。このビルドの通常ResFontは0x18。
- CMAPの可変データとCWDHの幅列は固定先頭型の後ろに続く。全フォント形式、GLGR、補助batchの全flagsは網羅していない。
- FINF+7の全encoding値の意味は型名に追加していない。自前資源・文字の表示と寿命を実機検証した記録ではない。
