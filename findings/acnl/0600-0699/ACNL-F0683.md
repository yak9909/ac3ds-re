---
id: ACNL-F0683
aliases:
- Ghidra-gpt-sol-5.6-CHAT-T004
- CHAT-T004
title: 0x958108 is pointer storage
summary: '`0x958108` is a global dword pointer slot, not inline UTF-16 storage.'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 9797896
- 1653312
- 1653484
- 1652972
- 1653036
tags:
- chat
- storage
supersedes: []
source: Ghidra:work/FINDINGS.md:2353-2365
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-CHAT-T004: 0x958108 is pointer storage

- `0x958108` is a global dword pointer slot, not inline UTF-16 storage.
- `BsMenuChat_SetupTextInput @ 0x193A40` stores `*(BsMenuChat+0x50)` into this slot at `0x193AEC`.
- `BsMenuChat_SubmitInput @ 0x1938EC` reads the actual source pointer again from `*(BsMenuChat+0x50)` at `0x19392C`, then builds a capacity-0x41 WordCPtr and submits it.
- Correct direct-memory test is to read `P=*(u32*)0x958108` and write the tag/text to `P`.
- Writing tag words directly to `0x958108` corrupts/replaces the pointer.
- Since the text-object virtual method runs again immediately before `0x19392C`, submit-path injection is more robust than assuming the mirrored pointer remains stable.
- `0x958108` is shared by other text/UI flows and is not chat-exclusive.

Evidence: `work/evidence/chat_buffer_pointer_20260916.md`.


