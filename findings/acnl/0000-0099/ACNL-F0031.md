---
id: ACNL-F0031
aliases:
- F-153
title: 'F-153: direct-emitter patch generator 監査 — `MEDIUM`（独立の静的照合）'
summary: '`PATCHES/cave_ui_picture_clone.py` の `MODE=audit` はゲームメモリを書き換えず、生成された'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:406-420
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-153: direct-emitter patch generator 監査 — `MEDIUM`（独立の静的照合）

`PATCHES/cave_ui_picture_clone.py` の `MODE=audit` はゲームメモリを書き換えず、生成された
body/aux codeを検査する。最終生成はbody 744 bytes (`0x01E81948-0x01E81C2F`)、aux 168 bytes
(`0x01E81C60-0x01E81D07`)で、flag `0x01E81C50`、name clone `0x01E81DA0`、text clone末尾
`0x01E82000` と重複しない。

BL行先数は独立に復号して `Mem_Copy=10`、live transform helper=10、Picture draw=8、
`TextBox_EmitBatchToGpuCommands=2`、P_allow emit helper=2 と一致した。二つのText emitter前は
`R3=[clone+0x100]`, `R2=clone`, `R0=drawctx`, `R1=cursor`, `R12=descriptor`,
`STR R12,[SP]` の順を満たし、descriptor literalは `0x330A605C` を指す。

これはF-144/F-151の静的ABIと合うが、direct emitterを同一frameに追加する副作用は未実機検証なので
確度はMEDIUMのままにする。

