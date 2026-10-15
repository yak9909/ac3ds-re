---
id: ACNL-F0691
aliases:
- Ghidra-gpt-sol-5.6-ITEM-T012
- ITEM-T012
title: low field-object display fallback
summary: 'User hardware observation: Item IDs 0x0000..0x00FA appear with one shared furniture/default icon and name `???`.'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses: []
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:2544-2559
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-ITEM-T012: low field-object display fallback

- User hardware observation: Item IDs 0x0000..0x00FA appear with one shared furniture/default icon and name `???`.
- Static cause: all these IDs are outside normal Item.bin domain; Item_ToParamIndex returns -1 and ItemParam_GetRecord returns NULL.
- icon resolver NULL fallback is `g_ItemIconBaseNameTable[0] = icn_000`.
- name resolver leaves Phrase empty and reaches common fallback; hardware output is `???`.
- Item_Is4000Class is false for these IDs.
- field/map instantiation code uses 0xFB/0xFC as special/sentinel values, consistent with 0x00..0xFA being concrete low IDs.
- Do not globally remap low IDs into Item.bin: Item_ToParamIndex has 17 direct BL callers and ItemParam_GetRecord has 324 direct BL callers in .text.
- Recommended icon mapping: display-only resolver, masked low ID -> fixed basename `fgo_%03x`; fixed 8-byte string slots permit `base + (id<<3)`.
- Recommended name mapping: display-only ItemName_ResolvePhrase branch. Minimal resource plan is appending 0xFB entries to existing STR_Item_name UMSBT tail and mapping `tailBase + lowId`.
- .arc member order is not semantic; runtime lookup is by filename/resource name.
- Maintain one manifest as source-of-truth for ID/icon/name generation.
- Existing `Strc/fobj/lut/Lut_fieldobj.bcres` may contain useful field-object metadata, but no sample is available and no user-facing name/icon mapping is proven from it.

Evidence: `work/evidence/low_field_item_display_20260917.md`.
