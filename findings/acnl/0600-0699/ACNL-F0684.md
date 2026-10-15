---
id: ACNL-F0684
aliases:
- Ghidra-gpt-sol-5.6-CHAT-T005
- CHAT-T005
title: direct 0x958108-pointee test negative; parse is still post-submit
summary: '**Hardware observation:** a valid Color-tag sequence written to the current pointee read from `0x958108` did not visibly decorate chat.'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 9797896
- 1653032
- 6275868
- 1653036
- 6111924
- 6169048
- 6294484
- 1653060
- 6294740
- 6153748
tags:
- chat
supersedes: []
source: Ghidra:work/FINDINGS.md:2366-2389
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-CHAT-T005: direct 0x958108-pointee test negative; parse is still post-submit

**Hardware observation:** a valid Color-tag sequence written to the current pointee read from `0x958108` did not visibly decorate chat.

Fresh static reanalysis:
- WordPtrSv virtual +8 used at `0x193928` is `0x5FC31C`, a trivial pointer getter only.
- final submit source is loaded at `0x19392C`.
- `WordPtrSv_CopyTagAware @ 0x5D42B4` runs MsgStream structurally, but copy-stream callbacks for character/start-tag/end-tag are no-op.
- after the scan it raw-copies the original UTF-16 source span.
- display-time `ChatMessageBox_EmitText @ 0x5E21D8 -> MsgStream_Emit @ 0x600BD4` happens after submit.

Therefore "tag interpretation already completed before send" is rejected.

Next hardware discriminator:
- break at `0x193944`;
- obtain exact `P=*(r1+4)`;
- inject tag/text at P at that instruction boundary;
- then trace `0x600CD4` and `0x5DE614`.

This distinguishes stale/overwritten input-buffer injection from renderer/tag-semantics failure.

Evidence: `work/evidence/chat_submit_injection_20260916.md`.


