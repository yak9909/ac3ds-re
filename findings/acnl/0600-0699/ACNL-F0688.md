---
id: ACNL-F0688
aliases:
- Ghidra-gpt-sol-5.6-TEXT-T009
- TEXT-T009
title: player/town name tag sanitizer
summary: group5/type0 current player name -> Insert method 0x5ECAB8.
date: '2026-09-19'
category: text
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 6212280
- 6210816
- 6212452
- 9455564
- 6126024
- 9449400
- 5690508
- 6213680
tags:
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:2494-2510
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-TEXT-T009: player/town name tag sanitizer

- group5/type0 current player name -> Insert method 0x5ECAB8.
- group5/type5 town name -> 0x5EC500.
- group5/type6 alternate town name -> 0x5ECB64.
- caches are `script::WordFix<9>` mode0 objects (vtbl 0x9047CC).
- player-name source is wrapped mode1 by 0x5D79C8.
- town-name source is forced to mode1 vtable 0x902FB8 at 0x56D48C.
- mode1 -> mode0 assignment invokes ContainTagEngine.
- any valid LMS start/end tag causes WordFix destination clear/reset; tag-bearing normal names are rejected before scripted insertion.
- downstream `Insert_ProcessPhrase 0x5ED030` does run MsgStream over the cached phrase, so direct post-sanitizer cache injection could still execute a tag.

Conclusion: ordinary player/town name fields are not a stock bypass for message-window tag execution.

Evidence: `work/evidence/name_tag_insertion_20260916.md`.


