---
id: ACNL-F0029
aliases:
- F-151
title: 'F-151: native TextBox draw の descriptor は `R2=0x330A605C` — `HIGH`（trace＋既存実測照合）'
summary: '`scratchpad/trace_textbox_draw_args.py` を `nwlyt_TextBox_DrawToCommandList`'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7589704
- 4947280
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:373-389
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-151: native TextBox draw の descriptor は `R2=0x330A605C` — `HIGH`（trace＋既存実測照合）

`scratchpad/trace_textbox_draw_args.py` を `nwlyt_TextBox_DrawToCommandList`
(`0x73CF48`) に一時適用し、本文 `T_msg_00=0x32D20788` だけを289回記録した。
最後の記録は `R0=self=0x32D20788`、`R1=0x327DFC90`、
`R2=0x330A605C`、`R3=draw context=0x32FF62EC`。`0x330A605C+0x80`
は有効pointer `0x32FF5FA4` である。

これはF-144で同じ会話 batch が `TextBox_EmitBatchToGpuCommands` に入った時の第5引数
`0x330A605C` と一致する。`0x73CF48` は入力R2を保存してこの第5引数に渡すため、
commit hookに残る `DrawPaneTree` のR6（この試行では別種の `0x32A0B0A0`）は置換不能である。
後者を渡したcloneは `0x004B7D50` で `*(a5+0x80)` が `0x1C` となりSIGSEGVした。

**根拠**: source vtable/name検証付きのin-game trace、F-144の独立したemitter入口停止記録、
`0x73CF48` の `MOV R6,R2; STR R6,[SP,...]; BL TextBox_EmitBatchToGpuCommands` 静的命令列。
traceは読出し後にhook/cave/bufferをstock/zeroへ復元済み。

