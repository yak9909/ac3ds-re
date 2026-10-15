---
id: ACNL-F0687
aliases:
- Ghidra-gpt-sol-5.6-CHAT-T008
- CHAT-T008
title: sender local Color render hardware success
summary: '**Hardware-confirmed.**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 9456884
- 9449400
- 2185468
- 2185500
- 2185480
tags:
- chat
supersedes: []
source: Ghidra:work/FINDINGS.md:2458-2493
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-CHAT-T008: sender local Color render hardware success

**Hardware-confirmed.**

After switching the final submit source from the stock mode0 WordCPtr vtable `0x904CF4` to the mode1 read-only vtable `0x902FB8`, the embedded LMS Color tag survived `Chat_SubmitLocal` and the sender's own chat bubble rendered `ABC` in red.

This confirms end-to-end on hardware:

```text
mode1 source
 -> mode1 Chat_SubmitLocal body storage
 -> mode1 ChatBubbleNode copy
 -> ChatMessageBox_EmitText
 -> MsgStream_Emit
 -> RenderTrace/System Color tag
 -> red glyph output
```

Thus System group0/type3 Color is not merely parser-visible; it is visually effective in normal chat rendering when the normal mode-conversion sanitizer is bypassed.


### Ghidra-gpt-sol-5.6-CHAT-T008: stock remote normal-chat styling blocked

For ordinary player-chat packets 0x8C..0x8F, no stock receive branch was found that both bypasses the mode0->mode1 sanitizer and renders arbitrary incoming body text.

- type 0x0A bypasses Chat_InsertReceived but does not render arbitrary normal body text;
- types 5/6/7/9 are special generated-message/state branches and ignore the incoming body for normal chat;
- every other type uses the sanitizer at 0x2158FC..0x21591C.

The receiver creates the mode0 view locally at 0x215908, so sender-side packet contents cannot select the receiver's mode1 vtable.

Conclusion: modified sender -> stock receiver cannot carry LMS Size/Color styling through the normal player-chat protocol.

Evidence: `work/evidence/chat_stock_remote_limit_20260916.md`.


