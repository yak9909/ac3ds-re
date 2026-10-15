---
id: ACNL-F0495
aliases:
- IDA-opus-5.5-F038
title: '一覧の行の文字の TagProcessor は script::RenderMain。タグ 0x0E/0/2 = 大きさ（縦横）、タブは 4 × 文字幅（2026-09-25、MEDIUM: 静的のみ。実機未確認）'
summary: '一覧の組み立て段 1（`sub_1C513C`）: 行ごとにメッセージ箱（196 B、`sub_5E24B0(箱, *(list+2504))` = 文字数の器）を作り、`vc_ACMESSAGEBOX_FUNC1 0x5E2020(箱, T_itm_%02d, 0)` で結ぶ。FUNC1 は TextBox vt[28] で器を取り、**TextBox+244（TagProcessor）に箱自身**を入れ、箱+12/+16 = 文字の大きさ ÷ 書体の幅／高さ（元の拡大率）'
date: '2026-09-25'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6168608
- 9448560
- 6117576
- 9426328
- 5244788
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2136-2145
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F038: 一覧の行の文字の TagProcessor は script::RenderMain。タグ 0x0E/0/2 = 大きさ（縦横）、タブは 4 × 文字幅（2026-09-25、MEDIUM: 静的のみ。実機未確認）

- 一覧の組み立て段 1（`sub_1C513C`）: 行ごとにメッセージ箱（196 B、`sub_5E24B0(箱, *(list+2504))` = 文字数の器）を作り、`vc_ACMESSAGEBOX_FUNC1 0x5E2020(箱, T_itm_%02d, 0)` で結ぶ。FUNC1 は TextBox vt[28] で器を取り、**TextBox+244（TagProcessor）に箱自身**を入れ、箱+12/+16 = 文字の大きさ ÷ 書体の幅／高さ（元の拡大率）。T_itm の bclyt の器は 0 byte。
- 箱の vtable 列 `script::RenderMain`（0x902C70）の Process `0x5D58C8`: 9 = タブ（`x = 原点 + n × writer+88 × 文字幅`、文字幅 = `sub_7435D4` = 書体の幅 × writer+0x24）、10 = 改行、14 = タグ → `sub_5D55E8`。
- `sub_5D55E8`: グループ 0・種類 2 = 大きさ（％）→ writer+0x24 / +0x28 = 元の拡大率 × 値/100（**縦横とも**）。種類 3 = 色（7 未満の番号）。グループ 0xFF・種類 1 = カーソル X を 値/32 に、種類 0 = ルビの位置を記録。
- 比較: `lyt::TagProcessor`（vtable 0x8FD598、Process 0x500774）の種類 2 は writer+0x24 だけ（横だけ）を変える。一覧の行ではこちらは使われない。
- 行の文字: ctlg_cntnt_00 の T_itm_XX は 168x20、左端・上下中央が基準、左詰め、文字の大きさ 14.4x19.2。書体 Garden_msg_size16（FINF の高さ 24・幅 18）→ 拡大率 0.8。送り幅は数字 12、A 13、B 13、C 12、D 14、E 12、F 12、x 10（`tools/layout/bcfnt_widths.py`）。
- gohan の使い方（b0553a3）: `[0E 0 2 2 65] 0xXX 	 [0E 0 2 2 100] 名前`。タブの位置は 4 × 14.4 × 0.65 = 37.44 px。T_itm を左へ 37.44 ずらして同じだけ広げる。
- 反証条件: 実機で ID が大きさの変わらないまま出る／タブが空白や □ になる／名前の位置がずれる（→ FUNC2 の MsgStream_Emit がタグかタブを落としているか、タブ幅 writer+88 が 4 ではない）。

