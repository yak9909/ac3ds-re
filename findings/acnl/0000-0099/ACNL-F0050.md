---
id: ACNL-F0050
aliases:
- F-12
title: F-12 `Field_GetItemAtXY` はポインタを返す — `HIGH`
summary: '`Field_GetItemAtXY(mapmgr, x, y, 0)` → そのマスのアイテム(4B)への**ポインタ**。'
date: '2026-09-08'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:846-854
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-12 `Field_GetItemAtXY` はポインタを返す — `HIGH`

`Field_GetItemAtXY(mapmgr, x, y, 0)` → そのマスのアイテム(4B)への**ポインタ**。
`mapmgr` は `unk_6A53DC()` で取得。

**根拠**: decompile。`Player_BeginFieldObjAction` 内の使用例。

---

