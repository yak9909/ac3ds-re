---
id: ACNL-F0643
aliases:
- Ghidra-gpt-sol-5.6-F005
- G-F005
title: crash_dump_00000005 の直接fault
summary: '**確度: HIGH（dump＋本体命令列）。根本原因の旧帰属は撤回。**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 3240100
- 5868552
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:82-90
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F005: crash_dump_00000005 の直接fault

**確度: HIGH（dump＋本体命令列）。根本原因の旧帰属は撤回。**

PC=`0x3170A4`, LR=`0x598C08`, r2=`0x96FCC3B0`。`0x3170A4` は `BalloonPresent_TryLandAndPlace` 内部でimpact Vec3*を読む命令なので、直接faultは無効Vec3 pointer。

ただしユーザーから「dropしておらず、AR enable直後に発生」と確認され、Ghidra-gpt-sol-5.6-F007で旧balloon caveが既存描画caveを上書きしていたことが判明した。従って「landing-side actor identity判定が根本原因」という旧推論は採用しない。


