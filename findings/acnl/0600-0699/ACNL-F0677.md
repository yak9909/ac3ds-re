---
id: ACNL-F0677
aliases:
- Ghidra-gpt-sol-5.6-F037
- G-F037
title: Ghidra-gpt-sol-5.6-F036 crash-dump root cause and ABI-safe bridge
summary: 'Hardware:'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 10150240
- 10150236
- 5891508
- 5891608
- 3131512
- 5891596
- 5891600
- 5891604
- 9789428
- 5857672
- 5891852
- 5891752
- 1478152
- 5871636
- 5848884
- 5860484
- 8622080
- 5891748
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:2065-2161
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: superseded
consolidated_into: ''
duplicate_of: ''
superseded_by: ACNL-F0678
---
## Ghidra-gpt-sol-5.6-F037: Ghidra-gpt-sol-5.6-F036 crash-dump root cause and ABI-safe bridge

Hardware:
- Ghidra-gpt-sol-5.6-F036 crashed immediately when starting the inventory drop.
- crash dump: `crash_dump_00000010.dmp`
- SHA-256: `c350a6c97074e160f46bae592007ca3c8620c70866f0202075be9941b27df128`

Crash-dump register block (r0-r15 beginning at file offset 0x28):
- r0 = 0x009AE160
- r1 = 0x00000000
- r2 = 0x00003B68
- r3 = 0x00000001
- r4 = 0x009AE15C
- r5 = 0
- r6 = 0x52
- r7 = 0x35
- r8-r11 = 0
- r12 = 0x0059E5B4
- sp = 0x0FFFFD28
- lr = 0x0059E618
- pc = 0x002FC878
- cpsr = 0x10

Instruction correlation:
- `0x59E60C LDR r1,[sp,#0x24]`
- `0x59E610 ADD r0,r4,#4`
- `0x59E614 BL 0x2FC878`
- return LR = `0x59E618`
- `0x2FC878 LDRH r2,[r1]`

At the fault:
- r4 = 0x9AE15C = DropData slot 0 base
- r0 = 0x9AE160 = slot0 +4 = ItemToPlace destination
- r1 = 0 = source Item* passed to ItemID::Write
- therefore the crash is a NULL source dereference inside stock Item copy

The dump also contains `0x838E38`, the instruction immediately after Ghidra-gpt-sol-5.6-F036's BLX Item_PlaceItem, confirming the call originated from the new high cave.

Root cause:
- Ghidra-gpt-sol-5.6-F036 entered the high cave with the correct stock Item_PlaceItem ABI:
  r0=0x0A, r1=0x955FF4, r2=actual Item*, r3=shown Item*
- but eligibility code reused/clobbered r1/r2/r3 before BLX Item_PlaceItem
- Item_PlaceItem therefore received invalid argument registers
- this is an ABI-preservation bug in Ghidra-gpt-sol-5.6-F036, not a native DropData queue design failure

### Ghidra-gpt-sol-5.6-F037 fix

Before any eligibility logic:
- save original r0/r1/r2/r3 to shared+0x7C/+0x80/+0x84/+0x88
- save original LR to shared+0x78

Before BLX stock Item_PlaceItem:
- restore all original r0-r3 exactly
- do not alter SP, so all stock stack arguments remain at their original locations

Before calling stock:
- copy world X/Y from original stack into shared+0x08/+0x00
- copy the full Item from original r2 Item* into shared+0x04
- this removes later dependence on Player_DropItem stack-frame offsets

After native slot allocation:
- save returned slot index at shared+0x74
- reconstruct exact DropData* as `0x9AE15C + slot*0x12` and store at shared+0x6C
- no longer depend on Item_PlaceItem's transient r4 value being exported by the hook

During custom balloon construction:
- preserve all callee-saved registers r4-r11 plus LR around the custom path
- Ghidra-gpt-sol-5.6-F032 coordinate/Vec3/AcBalloon logic is then run from the original 0x596188 callsite context

Allocator-stop hook:
- moved to 0x838FD0
- armed: jump to stock Item_PlaceItem epilogue 0x59E70C before FieldAction construction
- unarmed: execute original MOV r0,sp and resume 0x59E6A8

Failure paths:
- native queue full returns the real stock -1
- custom spawn failure marks the exact native DropData.State=3 and returns its real handle for stock failure finalization

Queue completion/persistence remains unchanged:
- Ghidra-gpt-sol-5.6-F032 impact field commit 0x168E08 -> 0x599814
- exact native DropData.State=2 after mode-1 cleanup at 0x593F34
- stock 0x596C84 consumes/clears the slot and releases inventory UI
- synthetic handle 4 remains absent

### Ghidra-gpt-sol-5.6-F037 cave boundaries

- main bridge: 0x838E00-0x838FCF, 0x1D0 bytes
- allocator-stop: 0x838FD0-0x838FF7, 0x28 bytes
- highest written address is below 0x839000 .rodata start

Static AR audit:
- all E-block byte counts exact
- malformed lines: 0
- 0x596188 -> 0x838E00
- 0x59E6A4 -> 0x838FD0
- synthetic 0x596C84/handle-4 hook absent

