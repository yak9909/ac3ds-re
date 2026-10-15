---
id: ACNL-F0680
aliases:
- Ghidra-gpt-sol-5.6-F039
- G-F039
title: 二系統の独立再解析は主要結論で一致し、旧timing説明だけが矛盾していた
summary: '**確度: HIGH（main raw bytesのfresh Ghidra decompile + raw ModuleVillage.cro命令列 + 既存hardware observations）。Ghidra-gpt-sol-5.6-F039 AR実装自体は未実機。**'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 1478152
- 5868524
- 6052400
- 5871636
- 5860484
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:2217-2301
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F039: 二系統の独立再解析は主要結論で一致し、旧timing説明だけが矛盾していた

**確度: HIGH（main raw bytesのfresh Ghidra decompile + raw ModuleVillage.cro命令列 + 既存hardware observations）。Ghidra-gpt-sol-5.6-F039 AR実装自体は未実機。**

系統AではJPN v1.5 exchange bytesから新規Ghidra ProgramDBを構築し、既存comment/nameを使わずUI/drop/balloon/fgobj/field commitを再decompileした。系統Bではraw ModuleVillage.cro terminal routineとmain XML/XREF/current Ghidra-gpt-sol-5.6-F032 hookを独立に追った。

両系統は以下で一致:
- BsMenuItemはPlayer_DropItem returnをopaque tokenとして扱い、poll result 0/1 wait, 2 success, 3 failureのみを要求する。
- handle 4は0x596C84のnative table index計算前、entryで捕捉すれば成立する。Ghidra-gpt-sol-5.6-F032 hardwareが実証済み。
- Item_PlaceItemはDropData allocate直後にnormal FieldActionを開始するためallocator APIとして分離利用できない。
- natural balloon action 0x21はinventory DropDataとは別lifecycle。
- 0x59AC50はFgObjPresent_SpawnFalling non-NULL後だけ到達するため、Ghidra-gpt-sol-5.6-F032のshared+0x68 captureはfalling-object生成成功の直接marker。
- falling objectは0x58FB40でItemをobject+0x64へcopyし、positionもobject内に保持する。impact後のshared再利用は旧visual cleanupを壊さない。
- FgObjPresent_Update mode 1はvisual cleanupのみ。completionをmode-1削除まで待つ必要はない。
- stock action 0x0Aも0x168E08 -> 0x599814後にoperation state 2へ進むため、Ghidra-gpt-sol-5.6-F039 completion publicationも同pair後とする。

矛盾:
- 旧Ghidra-gpt-sol-5.6-F025 explanationの「A4はstate helper return後」と、旧Ghidra-gpt-sol-5.6-F027 explanationの「landingはstate helper内で同期」は同一terminal invocation説明として両立しない。
- raw ModuleVillage terminal file 0x19BA8は main 0x598BEC landing attempt -> main 0x5C5A30 A4 reaction -> cleanup の順を直接示す。
- よって旧timing因果説明はRETIRED。Ghidra-gpt-sol-5.6-F025/Ghidra-gpt-sol-5.6-F027/Ghidra-gpt-sol-5.6-F032のhardware observations自体はVALID。

Ghidra-gpt-sol-5.6-F039設計:
- state setter前に shared+0x60=custom AcBalloon*, +0x68=0, +0x6C=1(WAIT)。
- synthetic handle 4 pollはshared+0x6Cをそのまま返す。2/3はpoll時にclearしない。
- exact A4 guard到達時、+0x68==0ならlanding visual生成失敗としてstatus=3。+0x68!=0ならstatus=1維持。
- exact impactで0x168E08 -> 0x599814完了後だけstatus=2、その後+0x68 clear。
- custom-success pathではItem_PlaceItem/normal FieldAction/full natural 0x21 bodyを呼ばない。
- 初回実機scopeはoffline/local。terminal前の異常actor破棄とonline同期は未確認として残す。

設計: `docs/balloon_drop_gf039_design.md`  
証拠: `work/evidence/balloon_drop_dual_verification_20260916.md`


### Ghidra-gpt-sol-5.6-F039 implementation: static audit PASS

**Hardware status: PENDING.**

The frozen Ghidra-gpt-sol-5.6-F039 design was assembled as a minimal delta over Ghidra-gpt-sol-5.6-F032.

Confirmed implementation invariants:
- actor/status/object state is armed before AcBalloon state transition;
- handle 4 is intercepted before native DropData indexing;
- status 1 keeps BsMenuItem waiting throughout flight;
- exact post-landing A4 guard maps missing falling-object capture to status 3;
- exact impact runs `0x168E08` then `0x599814`;
- falling-object identity is cleared before SUCCESS=2 is published;
- native handle values continue through the stock `0x596C84` prologue/continuation;
- custom-success path still does not call Item_PlaceItem/native DropData/normal FieldAction.

Static audit:
- raw source hook words: all match;
- cave E-block overlap: 0;
- ARM branch target audit: all exact;
- initialized B/BL targets into caves: 0;
- initialized direct pointers into caves: 0;
- highest write: 0x8384EB.

Implementation evidence:
`work/evidence/balloon_drop_gf039_implementation_20260916.md`.


### Ghidra-gpt-sol-5.6-F039 hardware validation — SUCCESS

User hardware validation confirms the implementation behaves exactly as designed.

Verified:
- selected inventory Item falls through the custom balloon path;
- source inventory Item remains present while the balloon/falling-present operation is in flight;
- inventory completion waits instead of returning immediate synthetic success;
- the custom Item persists on the field after impact;
- source inventory slot is consumed only after the impact completion point;
- lower-screen inventory UI releases normally after completion;
- Player state remains preserved as intended;
- the operation no longer exposes the Ghidra-gpt-sol-5.6-F032 early-completion race.

Therefore Ghidra-gpt-sol-5.6-F039 is now the current **hardware-verified** implementation.

Completion architecture now accepted:
- operation path = Ghidra-gpt-sol-5.6-F032 custom balloon/persistence path;
- UI token = synthetic handle 4;
- status = 1 WAIT / 2 SUCCESS / 3 FAILURE;
- SUCCESS publication point = after `0x168E08 -> 0x599814`;
- native DropData integration designs Ghidra-gpt-sol-5.6-F034..G-F037 remain retired.


