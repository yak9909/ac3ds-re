---
id: ACNL-F0664
aliases:
- Ghidra-gpt-sol-5.6-F025-HW
- G-F025-HW
title: actor identity guard keeps inventory Player state 0x16
summary: '**確度: VERIFIED ON HARDWARE.**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses: []
tags:
- inventory
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:1109-1114
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F025-HW: actor identity guard keeps inventory Player state 0x16

**確度: VERIFIED ON HARDWARE.**

Ghidra-gpt-sol-5.6-F025実機試験でcustom balloon drop成功後もPlayer current state 0x16が維持された。これによりModuleVillage terminal A4 reactionのcustom actor identity guardが実機で有効と確定。

