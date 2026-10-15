---
id: ACNL-F0040
aliases:
- F-02
title: F-02 アイテムは 4 バイト構造 — `HIGH`
summary: '```'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9789428
- 9789432
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:679-694
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-02 アイテムは 4 バイト構造 — `HIGH`

```
+0 : u16  ID | bit15フラグ    (ID は 0x7FFF でマスク)
+2 : u16  フラグ             (bit15 = 埋設)
```

**根拠**: decompile。
`Item_IsId` = `return (*(u16*)a1 & 0x7FFF) == a2;`
`Item_Copy` = u16 を 2 回コピー（計 4 バイト）。
`Item_IsBuriedFlag` = `*(u16*)(item+2) >> 15`。

特殊値: `0x7FFE` = 空マス（`g_EmptyItem` @ `0x00955FF4`）、`0x7FFC` @ `0x00955FF8`。

---

