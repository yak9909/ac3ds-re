---
id: ACNL-F0686
aliases:
- Ghidra-gpt-sol-5.6-CHAT-T007
- CHAT-T007
title: mode1 sender bypass preserves tags on hardware
summary: '**Hardware-confirmed.**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 9456884
- 9449400
- 6294740
- 6153748
tags:
- chat
supersedes: []
source: Ghidra:work/FINDINGS.md:2428-2457
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-CHAT-T007: mode1 sender bypass preserves tags on hardware

**Hardware-confirmed.**

At the final submit breakpoint, changing only the temporary source object's vtable:

```text
0x00904CF4 (mode0)
    ->
0x00902FB8 (mode1 read-only)
```

caused the first destination `WordPtrSv` after `Chat_SubmitLocal` assignment to retain the complete LMS tag sequence.

Therefore the T006 model is confirmed on hardware:

- mode0 source -> mode1 destination = sanitizer/conversion; tags removed;
- mode1 source -> mode1 destination = structured/raw-preserving copy; tags retained.

This proves the failure of the original injection was not caused by timing, pointer selection, endian packing, or malformed tag bytes. It was specifically the `WordPtrSv_Assign` mode conversion.

Next validation stage:
- continue with the preserved tag and observe the sender's displayed chat bubble;
- if necessary trace `0x600CD4` and `0x5DE614`;
- remote stock receiver still has its own mode0->mode1 sanitizer in `Chat_InsertReceived`, so remote decoration requires a receiver-side bypass for testing.

Evidence chain:
- Ghidra-gpt-sol-5.6-CHAT-T006: `work/evidence/chat_tag_sanitizer_20260916.md`


