---
id: ACNL-F0662
aliases:
- Ghidra-gpt-sol-5.6-F024
- G-F024
title: Actor_SetState無条件hit + state 0x16 first-departure trace
summary: 'Ghidra-gpt-sol-5.6-F023実機結果:'
date: '2026-09-19'
category: actor
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 6604424
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:994-1036
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F024: Actor_SetState無条件hit + state 0x16 first-departure trace

Ghidra-gpt-sol-5.6-F023実機結果:
- shared 0x01E81020..0x44に記録なし
- したがって「current=0x16 && requested=0x06」の直接遷移は観測されていない

Ghidra-gpt-sol-5.6-F024ではhook到達と遷移条件を分離する。

Actor_SetState @ 0x64C688 hookは毎回:
- shared+0x48: hit counter++
- +0x4C: last requested
- +0x50: last current
- +0x54: last caller LR
- +0x5C: unconditional marker 0x24F1A57F

さらに current==0x16 && requested!=0x16 の最初のdeparture候補で:
- +0x20 caller LR
- +0x24 requested
- +0x28 current
- +0x2C desired
- +0x30 marker 0x16F1A57F
- +0x34 previous
- +0x38 Player*
- +0x3C r2
- +0x40 r3
- +0x44 MENU_FLAGS
- +0x58 Ghidra-gpt-sol-5.6-F022 armed flag (shared+0x0C)

trace cave:
- 0x838444-0x8384E3
- payload 0xA0 bytes
- SHA-256 a83f85c2309d46f90e7e1089b89c273dfad1f0642832cb8013a01fe3cf07b5f5

static collision:
- ARM B/BL target into cave: 0
- initialized aligned direct pointer into cave: 0

Interpretation:
- +0x5Cが出ない: Actor_SetState hook自体が実行されていない/適用されていない
- +0x5Cは出るが+0x30が出ない: state 0x16からのdepartureがActor_SetState経由で観測されていない
- +0x30が出る: +0x24 requested と +0x20 LR が実際の最初のdeparture


