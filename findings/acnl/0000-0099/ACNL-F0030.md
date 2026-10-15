---
id: ACNL-F0030
aliases:
- F-152
title: 'F-152: commit中の `TextBox_Draw` wrapper再入は不可 — `HIGH`（static＋実機例外）'
summary: F-151のdescriptorを渡してcommit hookから `TextBox_Draw (0x73CF48)` を呼ぶ試行は、
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7589704
- 1185500
- 5670696
- 4947168
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:390-405
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-152: commit中の `TextBox_Draw` wrapper再入は不可 — `HIGH`（static＋実機例外）

F-151のdescriptorを渡してcommit hookから `TextBox_Draw (0x73CF48)` を呼ぶ試行は、
`0x001216DC` (`GpuCmd_SelectList`) でSIGSEGVした。停止時はlist key `R5=0x10`、
探索node `R4=0x000F0085` が無効だった。LR=`0x00568728`は
`ssys_ma_lyt_Layout_RecordPaneTree` の `GpuCmd_SelectList` 呼出し直後である。

`0x73CF48` はdraw context `a4+0x24` が非0なら `sub_4B8360(a4)` を呼ぶ。このwrapperを
既にlist record中のcommit hookから再実行すると、layout recordが再入しGPU command-list選択
状態を壊す。従ってcloneはwrapperを呼ばず、その後段
`TextBox_EmitBatchToGpuCommands (0x4B7CE0)` を直接呼ぶ必要がある。

新しいpatch版は `(drawctx, cursor, clone, clone+0x100, descriptor)` をARM ABIで渡す:
`R0=R5`, `R1=cursor`, `R2=clone`, `R3=[clone+0x100]`, stack arg=`0x330A605C`。
Text shadowとmainのみをまず検証し、`T_nam_00`はcave容量と安全性確認後に戻す。

