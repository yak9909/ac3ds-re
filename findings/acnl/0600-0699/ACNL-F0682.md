---
id: ACNL-F0682
aliases:
- Ghidra-gpt-sol-5.6-CHAT-T003
- CHAT-T003
title: local/self and inline tag scope
summary: '**確度: HIGH (static JPN v1.5 path analysis; hardware tagged-chat test still pending).**'
date: '2026-09-19'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 2195524
tags:
- chat
supersedes: []
source: Ghidra:work/FINDINGS.md:2339-2352
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-CHAT-T003: local/self and inline tag scope

**確度: HIGH (static JPN v1.5 path analysis; hardware tagged-chat test still pending).**

- Embedded group0/type2 Size and group0/type3 Color are not remote-only.
- `Chat_SubmitLocal 0x218044` stores the submitted tag-aware WordPtr into local chat storage before/alongside network send.
- Normal chat body rendering goes through the same MsgStream-based renderer surface, so the sender's own displayed bubble is expected to parse the tags too.
- Tags are embedded directly at the desired UTF-16 position inside the chat body.
- A setting tag affects following glyphs until another applicable tag changes/resets that renderer state.
- For partial styling, insert the tag immediately before the target substring and an explicit reset tag immediately after it.
- Valid tags are consumed structurally and are not drawn as glyphs.
- Tag header/payload code units count against the 0x41 chat body capacity.


