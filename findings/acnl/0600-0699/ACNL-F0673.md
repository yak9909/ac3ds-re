---
id: ACNL-F0673
aliases:
- Ghidra-gpt-sol-5.6-F032@Ghidra:work/FINDINGS.md:1736
- G-F032@Ghidra:work/FINDINGS.md:1736
title: dit (post Ghidra-gpt-sol-5.6-F032)
summary: 'User correction accepted: ACNL already owns the drop queue; adding a second custom busy lock before fully understanding the native lifecycle was the wrong integration direction.'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 9789428
- 10150236
- 10150308
- 10150468
- 5891508
- 5892344
- 5860484
- 5893096
- 5891548
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1736-1783
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Native drop queue re-audit (post Ghidra-gpt-sol-5.6-F032)

User correction accepted: ACNL already owns the drop queue; adding a second custom busy lock before fully understanding the native lifecycle was the wrong integration direction.

Address clarification:
- 0x955FF4 = ItemToPlace (4-byte empty/sentinel Item), not the queue base.
- native four-slot queue = g_DropDataTable @ 0x9AE15C, 0x12 bytes x 4.
- g_FieldActionActive @ 0x9AE1A4 and g_DigRecordArray @ 0x9AE244 are separate structures.

DropData layout (IDA comment + JPN instruction audit):
- +00 ItemToReplace
- +04 ItemToPlace
- +08 ItemToShow
- +0C wX
- +0D wY
- +0E DropType
- +0F State
- +10 SlotIndex
- +11 Flags

Native State lifecycle:
- 0 = free
- Item_PlaceItem 0x59E5B4 allocates first free slot and sets 1
- FieldAction_Dispatch 0x59E8F8 case 1/2 sets the originating slot to 2/3
- 2 = success completion pending consumption
- 3 = failure completion pending consumption
- 0x596C84 polls by returned slot index and, for ordinary DropType 0x0A, consumes 2/3 then clears DropType/State back to 0

The slot index is propagated through FieldAction_QueueToRecord @ 0x59EBE8 via DropData+0x10 into processFlags low two bits, which is how completion packets address the correct queue slot.

Inventory menu contract:
- FUN_0019AD30 stores Player_DropItem return in BsMenuItem+0xD8.
- FUN_0019AF8C polls 0x596C84(handle).
- 0/1 -> wait.
- 2 -> inventory source slot removal + UI refresh/advance.
- 3 -> error path.
Thus the native DropData queue is also the inventory UI completion token.

IDA vc_DROPM comment at 0x59E5DC explicitly documents that the old rapid-drop cheat bypasses the State scan and always overwrites slot 0, destroying an in-flight record. This independently confirms the intended queue protection semantics.

Impact on current balloon design:
- Ghidra-gpt-sol-5.6-F032 remains HW VERIFIED for visual/state/persistence.
- synthetic handle 4 is the reason a second local inventory drop can start early: its 0x596C84 special case returns 2 immediately and bypasses native State=1.
- Ghidra-gpt-sol-5.6-F033 custom shared+0x68 busy lock is RETIRED as the future integration direction.
- current AR restored to hardware-verified Ghidra-gpt-sol-5.6-F032 baseline.
- next integration must allocate/use a real DropData slot, keep State=1 during balloon flight, set that same slot to 2 only after Ghidra-gpt-sol-5.6-F032 impact+field commit, and let stock 0x596C84 free it and release the UI. Failure should use State=3.
- no new queue implementation is introduced by this analysis.

