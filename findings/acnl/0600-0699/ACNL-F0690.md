---
id: ACNL-F0690
aliases:
- Ghidra-gpt-sol-5.6-ITEM-T011
- ITEM-T011
title: item name/icon resource pipeline
summary: 'Normal Item ID index: `((id & 0x7FFF)-0x2000)`, valid for index < `0x172B`.'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5460240
- 8858692
- 2854572
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:2526-2543
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-ITEM-T011: item name/icon resource pipeline

- Normal Item ID index: `((id & 0x7FFF)-0x2000)`, valid for index < `0x172B`.
- `Item.bin` record size is `0x1E`; record +0x00 u16 is item icon-name-table index.
- `ItemParam_GetIconBaseName @ 0x535110` maps that index through the 507-entry table at `0x872C44` to `icn_NNN`.
- `ItemIconWidget_SetItem @ 0x2B8EAC` formats `%s.bclim`, looks up layout resource type `timg`, and falls back to `icn_000.bclim`.
- core ItemWin loads `Layout/ItemWin/item_icon.arc`; other UI surfaces also load `Layout/ItemWin/item_icon_tex.arc`.
- exact .arc on-disk packing remains unverified without archive samples.
- normal item names use the same item param index to fetch `STR_Item_name[index]`.
- resource path is `Script/Str/STR_Item_name.umsbt`.
- special/dynamic item classes can bypass STR_Item_name and generate names separately.
- Existing-icon remap can be done by editing Item.bin record +0x00.
- Replacing a shared icn_NNN.bclim affects all items sharing that table index.
- A unique new basename requires a reusable table entry, table extension, or icon resolver hook.

Evidence: `work/evidence/item_name_icon_20260917.md`.


