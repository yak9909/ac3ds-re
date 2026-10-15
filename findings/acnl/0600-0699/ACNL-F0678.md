---
id: ACNL-F0678
aliases:
- Ghidra-gpt-sol-5.6-F037@Ghidra:work/FINDINGS.md:2162
- G-F037@Ghidra:work/FINDINGS.md:2162
title: e-analysis after Ghidra-gpt-sol-5.6-F037
summary: 'Current implementation status:'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 5746172
- 9732072
- 9732076
- 5746456
- 5860484
- 5857672
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:2162-2189
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Drop/balloon pipeline re-analysis after Ghidra-gpt-sol-5.6-F037

Current implementation status:
- Ghidra-gpt-sol-5.6-F032 is restored as the current AR baseline because it is the last hardware-verified implementation for visual/persistence/state.
- Ghidra-gpt-sol-5.6-F034/Ghidra-gpt-sol-5.6-F035 are retired: they regressed to normal drop by mixing custom balloon with Item_PlaceItem/normal FieldAction lifecycle.
- Ghidra-gpt-sol-5.6-F036/Ghidra-gpt-sol-5.6-F037 are retired: both violated hidden call contracts while trying to bridge native queue through stock Item_PlaceItem.

Critical corrections:
1. Item_PlaceItem has two responsibilities: native DropData allocation and immediate normal FieldAction dispatch. These must not be coupled for custom balloon.
2. Natural balloon-present landing uses a separate 0x21 FieldAction/active-table path and does not allocate a four-slot DropData handle.
3. 0x57ADFC is not balloon-specific. Static scan finds 105 direct BL callers. It stages r3 and caller stack arg#5 into 0x947FE8/0x947FEC before generic creation.
4. crash_dump_00000011 proves Ghidra-gpt-sol-5.6-F037 violated that contract: pc=0x57AF18, r2=0x947FE8, r1=0xA. The constructor dereferenced 0x947FEC==0xA. Ghidra-gpt-sol-5.6-F032 correctly supplied stack arg#5=0.
5. DropQueue_PollAndFinalize 0x596C84 State=1 is a pure wait. For ordinary DropType 0x0A, State=2 follows generic clear and returns 2; it does not replay Item_PlaceItem.

Design selected for next implementation:
- use the native g_DropDataTable slot only as inventory UI completion token;
- reserve a free 0x12-byte slot directly at the Ghidra-gpt-sol-5.6-F032 0x596188 context;
- do not call Item_PlaceItem / FieldAction_QueueToRecord / FieldAction_Dispatch;
- keep the exact Ghidra-gpt-sol-5.6-F032 custom balloon spawn and impact persistence path;
- return the real native slot index to BsMenuItem;
- keep State=1 while balloon visual is active;
- after exact custom falling-present mode1 cleanup, set that slot State=2;
- let stock 0x596C84 clear it and let BsMenuItem run normal success handling.

Detailed design is in docs/drop_pipeline_reanalysis.md.
No new AR has been assembled from this design yet.


