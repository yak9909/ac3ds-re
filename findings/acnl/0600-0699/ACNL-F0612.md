---
id: ACNL-F0612
aliases:
- IDA-opus-5.5-F096
title: 'ゲームのフォント（Garden_msg_size16）で描けない文字 = 代わりの字形 0xE03A（2026-10-06、MEDIUM: 実機の写し + 元の ARM との照合。候補の除外は実機未確認）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。'
date: '2026-10-06'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7616360
tags:
- font
- save-data
supersedes: []
source: IDA:work/FINDINGS.md:4747-4756
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F096: ゲームのフォント（Garden_msg_size16）で描けない文字 = 代わりの字形 0xE03A（2026-10-06、MEDIUM: 実機の写し + 元の ARM との照合。候補の除外は実機未確認）

解析ソフト: IDA / 解析モデル: opus-5.5。
- FINF+0x02（u16）= 代わりの字形の番号。実機の写し（work/evidence/chat_kanji/font_tables_sparse.bin、資源 0x3187CA00 / FINF 0x3187CA1C）では 5131。
  CMAP でこの番号に当たるコードは **0xE03A の 1 つだけ**（利用者の観察「ハテナ文字 0xE03A」と一致）。CMAP に無いコードはすべてこの字形で描かれる。
- 描ける（自分の字形を持つ）コードは 5,363 種。例: 鷗 U+9DD7 / 龘 U+9F98 / 辻 U+8FBB / ゔ U+3094 / 𠮷（サロゲート）は描けない。
- 根拠 2 経路: (1) work/evidence/kanji_unsupported/probe_drawable.txt（GameFontView を写しに当てた全走査）、(2) tools/chat_kanji/verify.py の font_oracle（GameFontView の引き方が元の ARM `MapCharToGlyph` 0x743768 と BMP 全 65,536 コードで一致。work/logs/chat_kanji_font_oracle_unsupported.txt）。
- 用途: gohan work/kanji-unsupported f1fba56 で、描けない文字を含む漢字候補を出さない（ChatKanji::Poll）。実機未確認。
- 注: verify.py の source_gate は Engine.cpp が src/SwkbdEngineProbe と食い違っていて止まる（この変更より前から。未調査）。

