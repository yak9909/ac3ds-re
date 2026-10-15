---
id: ACNL-F0661
aliases:
- Ghidra-gpt-sol-5.6-F023
- G-F023
title: Ghidra-gpt-sol-5.6-F022後に残るdirect 0x16→0x06を観測する
summary: '**確度: HIGH（hook ABI/分岐/cave collision静的検証。caller実機値待ち）。**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 6604424
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:979-993
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F023: Ghidra-gpt-sol-5.6-F022後に残るdirect 0x16→0x06を観測する

**確度: HIGH（hook ABI/分岐/cave collision静的検証。caller実機値待ち）。**

Ghidra-gpt-sol-5.6-F022でAcBalloon terminal dropのPlayer state 0xA4 reactionをcustom時だけ抑止しても、実機ではdrop直後にcurrent state 0x06へ遷移した。

この結果から、0xA4 reactionは実在するが0x06の唯一原因ではない。trace時点ですでにdesired stateが0x06であったため、desired/current同期または別callerによるdirect state 6要求を区別する必要がある。

Ghidra-gpt-sol-5.6-F023診断版はGhidra-gpt-sol-5.6-F022を維持したまま Actor_SetState @ 0x64C688 を観測hookし、current=0x16 / requested=0x06の実caller LRとcontextをshared 0x01E81020..0x44へ保存する。state遷移はそのままstockへ通す。

markerは0x06F1A57E。trace E-blockは0x838444-0x8384BB、0x78 bytes、SHA-256 b8f198c50fe74d827dc3a6e919de7ac982499462f44137ec4ed3b603fda71234。

実機取得後、LRが0x672F44付近なら desired/current normalizer FUN_00672CAC、0x64BE00付近なら generic safety setter FUN_0064BBC8 と判別できる。その他なら新callerとして追跡する。


