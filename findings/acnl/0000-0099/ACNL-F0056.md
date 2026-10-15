---
id: ACNL-F0056
aliases:
- F-18
title: F-18 `Player_StartFieldAction` の呼び出し元は 16 箇所 — `HIGH`
summary: '`0x590000`-`0x5B0000` の BL 全走査で 16 件。'
date: '2026-09-08'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5832704
- 5963776
- 5867144
tags:
- player
supersedes: []
source: v1:RE/FINDINGS.md:1012-1026
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-18 `Player_StartFieldAction` の呼び出し元は 16 箇所 — `HIGH`

`0x590000`-`0x5B0000` の BL 全走査で 16 件。

```
595C6C  595E54  59605C  596188  596B30  596B94  597128  5976DC
597798  597868  597DFC  597F94  598688  59892C  598B90  598E9C
```

`0x598688`（スコップ経路）はそのうちの 1 つに過ぎない。

**含意**: `0x598688` だけをフックしても、そこを通らないアクション経路がある。

---

