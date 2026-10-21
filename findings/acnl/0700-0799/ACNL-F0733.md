---
id: ACNL-F0733
aliases: []
title: "通常フォントの未収録文字と追加 JIS 書体の補完範囲"
summary: "更新側の通常フォントCMAPには汎・符・濁など18漢字とU+301Cが無く、18漢字は追加GardenPlus_JisLevel1にはある。通常フォントだけで任意の日本語UI文字が揃うとはいえない。"
date: 2026-10-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: "全関数export・実RomFS・提供停止ログ・公開ソース"
addresses: [0x00743768, 0x007438B4, 0x0052D6A8, 0x0052D418]
tags: ["font"]
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

通常 `Garden_msg_size16.bcfnt` と追加 `GardenPlus_JisLevel1.bcfnt` の文字範囲は異なる。通常書体だけでは欠ける漢字があり、追加書体の存在は通常slotの自動的な補完を意味しない。
確度MEDIUM：実RomFSのCMAP全件解析と、ResFontのlookup/欠字処理、状態付きfont getterを照合。実機での追加slot常駐は未確認。

## 根拠

一次証拠 `_local/evidence/107/fonts.json` のmapping（入力ファイルのpath/SHA256付き）、同所 `assets.py` のCMAP parser。全関数exportは `0x00743768.txt`、`0x007438b4.txt`、`0x0052d6a8.txt`、`0x0052d418.txt`。

通常書体に無く、追加JIS書体に存在することを全CMAPで確認した文字:

`汎 符 濁 隔 癖 肢 没 縞 曇 範 阻 遣 崖 掴 閲 遷 斜 矩`

U+301C（WAVE DASH、〜）は両方のCMAPに無い。外見が似た別Unicodeを同一文字の収録と数えない。

`0x743768` は指定ResFontのCMAPを探索し不在なら0xFFFF。`0x7438B4` の欠字処理は指定fontの代替glyphへ進む。`0x52D6A8` はslotの状態3だけを返す。別書体を自動で読み込んで欠字を補完する根拠にはならない。

通常書体はA4・128×128・154枚、追加JISはA4・128×128・85枚、sheetの合計696,320 B（F0729）。既存fontを借りるために追加書体の新規ロードを前提にすると、無確保の参照ではなくなる。

公開資料 `STUDY107_PUBLICS` の [ObsidianX BCFNT parser](https://github.com/ObsidianX/3dstools/blob/master/bcfnt.py) のCMAP3方式と照合した。ゲーム/実ファイルを主証拠とし、このparserの結果だけでは判定していない。

## 反証条件・未確認点

追加slotの実際のロード時期、全場面での生存、他の書体による代替表示は未確認。別コードポイントへの置換は表記変更として別に判断する。
