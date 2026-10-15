---
id: ACNL-F0681
aliases:
- Ghidra-gpt-sol-5.6-CHAT-T002
- CHAT-T002
title: remote chat Size/Color tags survive transport and render
summary: '**確度: HIGH（JPN v1.5 raw bytes / fresh Ghidra ProgramDB）。実機remote decoration testは未実施。**'
date: '2026-09-19'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 1652972
- 2195524
- 2191384
- 7382228
- 2185320
- 2179276
- 6169048
- 6294484
- 6275116
- 6111924
- 9450312
- 6153748
tags:
- chat
supersedes: []
source: Ghidra:work/FINDINGS.md:2302-2338
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-CHAT-T002: remote chat Size/Color tags survive transport and render

**確度: HIGH（JPN v1.5 raw bytes / fresh Ghidra ProgramDB）。実機remote decoration testは未実施。**

Normal player chat is not flattened to plain glyph text before networking.

End-to-end:
- `BsMenuChat_SubmitInput 0x1938EC`
- `Chat_SubmitLocal 0x218044`
- chat packet IDs `0x8C..0x8F`
- 0x90-byte packet, UTF-16 field at +0x0E with capacity0x41
- `BsBalloonChat_ProcessIncoming 0x217018`
- `ChatPacket_CopyTextOut 0x70A4D4`
- `Chat_InsertReceived 0x215868`
- `ChatBubbleNode_RenderMessage 0x2140CC`
- `ChatMessageBox_EmitText 0x5E21D8`
- `MsgStream_Emit 0x600BD4`

No control-tag sanitizer was found in the send/receive string path.

`WordPtrSv_Assign 0x5FC02C` uses tag-aware `0x5D42B4`/MsgStream copying over explicit pointer/capacity, so a structurally valid System-group tag containing `group=0x0000` is not truncated at that zero code unit.

Normal chat body uses `script::RenderTrace` vtable `0x903348`.
`RenderTrace_OnTag 0x5DE614` explicitly accepts/preserves:
- group0/type2 Text Size
- group0/type3 Text Color

and ignores group0/type4 PageBreak and group0/type1 Font in this path.

Therefore a mod/plugin that constructs the UTF-16 control sequence before `Chat_SubmitLocal` can send Size/Color decoration that the stock remote chat body will parse/render.

Standard software-keyboard entry of U+000E is not established; injection/hook/plugin string construction is required for a practical implementation.

Detailed analysis: `docs/chat_text_tags.md`.
Evidence: `work/evidence/chat_text_tags_remote_20260916.md`.


