---
id: ACNL-F0042
aliases:
- F-04
title: F-04 型ID 113-122 は ASCII ではない — `HIGH`
summary: '`FieldObj_ResolveResultItem` (`0x597148`) が比較する 113-122 は'
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5861704
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:711-722
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-04 型ID 113-122 は ASCII ではない — `HIGH`

`FieldObj_ResolveResultItem` (`0x597148`) が比較する 113-122 は
ASCII `q`-`z` ではなく地面オブジェクトの型ID。

**根拠**: 比較が `==` でなく `Item_IsId()` 経由であること（assembly）。
加えて memory 実読で、ID113-117 の定義 16 バイトが ID38 と、
ID118-122 が ID43 と**バイト単位で完全一致**することを確認。
つまり 5 個ずつのバリエーションであり、文字ではない。

---

