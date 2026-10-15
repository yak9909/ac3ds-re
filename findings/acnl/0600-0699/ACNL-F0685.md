---
id: ACNL-F0685
aliases:
- Ghidra-gpt-sol-5.6-CHAT-T006
- CHAT-T006
title: normal chat strips embedded tags
summary: '**Hardware-confirmed.**'
date: '2026-09-19'
category: text
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 1653060
- 9456884
- 7712868
- 9457344
- 7719136
- 6275196
- 6194168
- 6294836
- 6294464
- 7382228
- 6126024
- 2185480
- 2185500
- 9449400
- 1653048
tags:
- chat
supersedes: []
source: Ghidra:work/FINDINGS.md:2390-2427
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-CHAT-T006: normal chat strips embedded tags

**Hardware-confirmed.**

At `0x193944`, final submit source still contained:
`000E 0000 0003 0002 0006 0041 0042 0043 0000`.

After the first `Chat_SubmitLocal` WordPtrSv assignment, destination contained only:
`0041 0042 0043 0000`.

Cause:
- normal submit WordCPtr vtable 0x904CF4, +0x2C -> 0x75B064 -> returns0
- chat storage WordPtrSv vtable 0x904EC0, +0x2C -> 0x75C8E0 -> returns1
- mode0 -> mode1 enters WordPtrSv_Assign conversion path 0x5FC07C
- conversion character callback 0x5E83F8 emits ordinary characters
- start/end tag callbacks 0x600D34 / 0x600BC0 are no-op
- structured LMS tags are therefore consumed but not copied

Sender packet serializer repeats the same mode0 -> mode1 sanitization.

Receiver:
- packet extraction 0x70A4D4 uses mode1 source constructor 0x5D79C8 and can preserve raw tags temporarily;
- ordinary Chat_InsertReceived reconstructs the text as mode0 at 0x215908 and sanitizes again at 0x21591C.

Therefore prior Ghidra-gpt-sol-5.6-CHAT-T002 stock-remote decoration claim is **RETIRED**.

Minimal sender diagnostic bypass:
- at 0x193944 change stack source vtable 0x904CF4 -> 0x902FB8; or
- patch 0x193938 `EB11A66C -> EB111022` (BL 0x5D79C8).

Modified receiver bypass:
- patch 0x215908 `EB0F9E78 -> EB0F082E`.

Stock unmodified remote still strips tags.

Evidence: `work/evidence/chat_tag_sanitizer_20260916.md`.


