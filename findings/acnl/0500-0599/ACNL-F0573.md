---
id: ACNL-F0573
aliases:
- IDA-unknown-F010
- V2-F010
title: Create全引数・instance共有範囲・更新/破棄（2026-09-17、MEDIUM）
summary: 正常callerのR0=holder、R1=ResModel、R2/R3=HeapAllocator、stack=mask0/flag0/count1をassembly照合。普通Model本体0x220、holderのRTTIとは別。mesh記述子等はinstanceへコピーするがgeometry/textureとmask0のmaterial fieldは共有。Material_GetResourceForMaskが資源/privateを選ぶ。world更新→条件付き骨格更新
date: '2026-09-17'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4303-4306
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F010: Create全引数・instance共有範囲・更新/破棄（2026-09-17、MEDIUM）

正常callerのR0=holder、R1=ResModel、R2/R3=HeapAllocator、stack=mask0/flag0/count1をassembly照合。普通Model本体0x220、holderのRTTIとは別。mesh記述子等はinstanceへコピーするがgeometry/textureとmask0のmaterial fieldは共有。Material_GetResourceForMaskが資源/privateを選ぶ。world更新→条件付き骨格更新を正常pose callerで確認。Destroy前処理はmesh pointerの昇順復元で、dtorが先頭entryから連続領域をfreeするため必要。局所65要素の上限とGPU終了は別に検証が必要。根拠tree_static.json/tree_lifecycle.json/tree_idb_bytes.json、詳細docs/topics/models3d.md。

