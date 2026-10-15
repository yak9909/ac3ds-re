---
id: ACNL-F0689
aliases:
- Ghidra-gpt-sol-5.6-FONT-T010
- FONT-T010
title: dedicated ruby font
summary: Conversation ruby/furigana uses a dedicated logical font resource `Garden_ruby`, separate from `Garden_msg_size16`.
date: '2026-09-19'
category: text
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5428248
- 5429304
- 5428904
- 5760812
- 5079112
- 5079736
tags:
- font
supersedes: []
source: Ghidra:work/FINDINGS.md:2511-2525
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-FONT-T010: dedicated ruby font

- Conversation ruby/furigana uses a dedicated logical font resource `Garden_ruby`, separate from `Garden_msg_size16`.
- `FontMgr_EnsureGardenFontsLoaded @ 0x52D418` loads `Garden_msg_size16`, `Garden_ruby`, `Garden_no`, and `Garden_no_f16` into distinct font slots.
- `FontSlot_BeginLoadBcfntByName @ 0x52D838` combines `Font/%s` and `%s.bcfnt`; therefore the ruby resource resolves to `Font/Garden_ruby.bcfnt`.
- `FontMgr_GetGardenFont @ 0x52D6A8`: kind0 = `Garden_msg_size16`, kind1 = `Garden_ruby`, kind2 = `Garden_no`.
- `MessageSystem_SetupGardenFonts @ 0x57E72C` obtains kind0 and kind1 separately and registers both with the layout/resource accessor; ruby is not merely a scaled main font.
- `Garden_ruby` uses the normal NintendoWare CTR `nw::font::ResFont`/BCFNT backend (`0x4D8048`, `0x4D82B8`).
- BCFNT is a bitmap glyph-sheet resource format, explaining the visibly raster/pixel character of ruby glyphs.
- External Fontworks material identifies Humming for ACNL in-game conversation text generally, but does not identify `Garden_ruby.bcfnt` specifically. Exact commercial family of the ruby asset remains unresolved.
- Exact FINF/TGLP/CWDH/CMAP metrics and visual glyph-family comparison require the actual RomFS `Font/Garden_ruby.bcfnt`.

Evidence: `work/evidence/ruby_font_20260917.md`.


