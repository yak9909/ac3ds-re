---
id: ACNL-F0074
aliases:
- F-36
title: F-36 木にぶつかったときの経路 — `HIGH`
summary: '**`Player_BeginFieldObjAction` も `FieldObj_ResolveResultItem` も通らない**別系統だった'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5873844
- 5874828
- 5873948
- 5873860
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1695-1717
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-36 木にぶつかったときの経路 — `HIGH`

**`Player_BeginFieldObjAction` も `FieldObj_ResolveResultItem` も通らない**別系統だった
（どちらも bp で実機確認し、ぶつかっても呼ばれないことを確認）。

```
FieldObj_FellObject (0x59A0B4-0x59A48C)
  └ 0x59A11C  BL FieldObj_SpawnFallActor(item*, X, Y, kind, fx)
```

観測値（竹にぶつかったとき）:

```
a1(R0) = 0x31F9E8AC -> ID 0x0039 (竹)   ← 正しい対象アイテム
a2(R1) = 37 (X)   a3(R2) = 39 (Y)
a4(R3) = 0        a5([SP]) = 0
```

`a4` は呼び出し元で `AND R3, R4, #0xFF`。`R4` は `FieldObj_FellObject` の引数
(`0x59A0C4  LDM R5, {R4,R7}`)。斧で切ったときは `a4 = 3` だった。

---

