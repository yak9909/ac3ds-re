---
id: ACNL-F0048
aliases:
- F-10
title: F-10 掘る経路の後段にアクションID 上書きがある — `MEDIUM`
summary: 掘る経路 `0x5984F0` (`R4=19`, `R1=158`) に入った**後**、
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5866736
- 5866832
- 5866616
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:815-828
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-10 掘る経路の後段にアクションID 上書きがある — `MEDIUM`

掘る経路 `0x5984F0` (`R4=19`, `R1=158`) に入った**後**、
`unk_7237D8` が非0を返すと `0x598550 : MOVNE R4,#0x1A (26)` で上書きされる。

**根拠**: assembly（機構の存在は確実）。

**訂正**: 当初これを「岩の跳ね返りの原因」と結論したが、**実機で否定された**。
`0x598550` を NOP にしても岩は掘れず、岩が掘れたのは F-11 の cat10 経路
（`0x598478`）を潰した後。この上書きが実際に何のケースで発動するかは未確認で、
`unk_7237D8` の役割も不明（TODO-07）。

---

