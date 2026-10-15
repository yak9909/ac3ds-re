---
id: ACNL-F0059
aliases:
- F-21
title: F-21 `FieldAction_Dispatch` の case 3 へは case 7 から来る — `MEDIUM`
summary: '```'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1151-1168
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-21 `FieldAction_Dispatch` の case 3 へは case 7 から来る — `MEDIUM`

```
case 7u:
  rec[13] = rec[13] & 0xC3 | 0xC;   // bits[5:2] = 3
  sub_59E8F8(rec);                   // → case 3 = FieldObj_ApplyDigRecord
  return sub_623F80(58, 4, rec, 22); // 58番メッセージで 22B レコードを送信
```

`0xC >> 2 = 3` なので case 3 に入る。TODO-01b の答え。

`sub_59EC9C`（case 0）は `rec[13] |= 8`（→ case 2）または `|= 4`（→ case 1）に
落とすため、**case 0 から case 3 へは直接行かない**。

**根拠**: decompile。case 7 に入る経路自体は未確認。

---

