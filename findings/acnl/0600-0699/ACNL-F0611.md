---
id: ACNL-F0611
aliases:
- IDA-opus-5.5-F095
title: 'Layout ノード 1 つにつき 1 枚のシザー（自前の候補欄の切り抜きに使う）（2026-10-06、HIGH: 静的 + 実機。縦の向きは実機で訂正）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。'
date: '2026-10-06'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5669596
- 5673612
- 1308748
- 5669676
tags:
- layout
supersedes: []
source: IDA:work/FINDINGS.md:4735-4746
by: opus-5.5
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F095: Layout ノード 1 つにつき 1 枚のシザー（自前の候補欄の切り抜きに使う）（2026-10-06、HIGH: 静的 + 実機。縦の向きは実機で訂正）

解析ソフト: IDA / 解析モデル: opus-5.5。
- `ssys_ma_lyt_Layout_ReplayRecordedList` 0x5682DC: Layout+0x138（u8）が 1 なら、再生の前に PICA のシザー（モード 3、reg 0x65）を float の +0x13C / +0x140 / +0x144 / +0x148 から出す。
  下位 16 ビット = +0x140 から +0x140 + +0x148 - 1（+0x2C の高さで切る）、上位 16 ビット = +0x13C から +0x13C + +0x144 - 1（+0x28 の幅で切る）。1 以外ならモード 0（全面）。**+0x108（記録の長さ）が 0 でも毎回出す。**
- 下画面の画素の矩形 [x0,x1) x [y0,y1) なら +0x13C = 320 - x1 / **+0x140 = 240 - y1** / +0x144 = x1 - x0 / +0x148 = y1 - y0（画面バッファの向きで、縦横とも反転）。
  - ★訂正（2026-10-06 実機）: 最初は `sub_1C55F8` の式（+0x140 = 120 - ty - h/2）を「上端」と読んで +0x140 = y0 にしたが、欄の中身が全部切れた（文字・ハイライトとも見えず、当たり判定だけ残った）。デバッガで +0x140 = 173（= 240 - 67）を直書きすると、候補が見え欄の縁で切れた（利用者の目視）。`sub_1C55F8` の ty の符号の扱いは未確認（ゲームの一覧の位置では差が出ないのかもしれない）。
  独立経路: 一覧のシザーを置く `sub_1C55F8`（F039）が画素の矩形から同じ形で書く。
- `LayoutMgr_AddLayout` 0x56928C の下画面のリスト = mgr+0x10（+4 先頭 / +8 末尾）。挿入は `SeadList_PushBack` 0x13F84C（ノード +4 前 / +8 次。前か次が 0 でなければ何もしない）か優先度順の挿入。
- 用途: gohan work/kanji-clip で漢字候補欄の内側（矩形・候補の文字）を専用ノード（シザー付き）へ回した（d2673b9 段 1、e4f8cf7 段 2、8d6fba0 で縦を 240 - y1 に修正）。
- IDB: 0x56832C と 0x13F84C にコメント、0x13F84C を `SeadList_PushBack` に命名。

