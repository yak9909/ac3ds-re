---
id: ACNL-F0021
aliases:
- F-393
title: 'F-393: 通常フックのR0保持不足によるOFF時SIGSEGV'
summary: HIGH（故障箇所と引数破壊。修正は未実施）。利用者のしずえスキップOFF時のSIGSEGVを
date: '2026-09-10'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5555256
tags:
- hook
supersedes: []
source: v1:RE/FINDINGS.md:178-187
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-393: 通常フックのR0保持不足によるOFF時SIGSEGV

HIGH（故障箇所と引数破壊。修正は未実施）。利用者のしずえスキップOFF時のSIGSEGVを
IDAで確認: PC=0x0054C438、R4=0、room=0x63、state=-1、bp=0。
idalib/code.bin.i64と実機命令はLDR R0,[R4,#0x148]で一致し、参照先は0x00000148。
実機wrapper 0x060B2BBCはOnFrame前後のR0を保存しない。OFF判定のItemAppliedが返す
R0=0を残したまま元関数0x0054C428へ戻り、MOV R4,R0がthisをゼロにする。
F-392のInitialize化は引数保持不足であり、使用不可。停止状態は変更していない。
詳細scratchpad/MEMO_f393_shizue_off_sigsegv.mdと生メモリJSONを参照。

