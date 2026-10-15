---
id: ACNL-F0179
aliases:
- F-143
title: 'F-143: TextBox vtable の実描画入口は `0x73CF48` — `HIGH`（静的＋実機）'
summary: '`nw_lyt_TextBox` vtable (`0x8FC07C`) の slot `+0x64` は `nwlyt_TextBox_DrawText`'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7589704
- 9420924
- 4960744
- 4960888
- 4960176
tags:
- rtti
supersedes: []
source: v1:RE/FINDINGS.md:9101-9118
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-143: TextBox vtable の実描画入口は `0x73CF48` — `HIGH`（静的＋実機）

`nw_lyt_TextBox` vtable (`0x8FC07C`) の slot `+0x64` は `nwlyt_TextBox_DrawText`
(`0x4BB1E8`)、slot `+0x68` は `0x73CF48` である。`sub_73CF48` は TextBox の length/font/
material と dirty/processor flags を検査し、条件が成立すると `sub_4BAFB0(a1,R3)` を呼ぶ。
`sub_4BAFB0` は `sub_7E8488` で local TextWriter を作り、TextBox+0x104 を writer+0x44 に
設定して `sub_4D5194`（batch count reset）→`sub_7E7F48`（UTF-16 emission）へ進む。
この経路では writer+0x40 context は初期値0のままで、`sub_4D5858`（immediate用GPU state
setup）は呼ばれない。

`0x73CF48` の実機 BP では、会話を開いていない状態で `R0=0x32D07674` の TextBox、
`R3=0x32FF62EC` の描画補助、`TextBox+0xD4=0x32D07790` の UTF-16 `"00"`、
font=`0x3302ABE0`、material=`0x32D07BA0`、length=2 を取得した。これは時計表示だった。
したがって先の `0x4BB278` 未ヒットは BP 不良ではなく、対象UIが別vtable経路を使ったためである。

**根拠**: vtable の slot 値と `0x73CF48`/`0x4BAFB0` の静的命令列、実機停止時の PC/register/
TextBox/string memory。読み出し後、BPは削除済み。

