---
id: ACNL-F0644
aliases:
- Ghidra-gpt-sol-5.6-F006
- G-F006
title: crash_dump_00000006 の直接fault
summary: '**確度: HIGH（dump＋本体命令列）。timing raceという旧帰属は撤回。**'
date: '2026-09-19'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 3240100
- 5868552
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:91-99
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F006: crash_dump_00000006 の直接fault

**確度: HIGH（dump＋本体命令列）。timing raceという旧帰属は撤回。**

PC=`0x3170A4`, LR=`0x598C08`, r2=`0x9F9E4F4A`, r12=`0x01E81000`。直接faultはGhidra-gpt-sol-5.6-F005同様、無効impact Vec3*。

旧解析ではframe-side timing raceと解釈したが、ユーザー確認とGhidra-gpt-sol-5.6-F007のcave衝突により、このdumpもenable時の制御フロー破壊に汚染されている可能性が高い。F0 timing raceをこのdumpから確定することはできない。


