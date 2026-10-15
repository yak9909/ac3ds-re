---
id: ACNL-F0045
aliases:
- F-07
title: F-07 アイテムID 158 は「穴」 — `MEDIUM`
summary: '**根拠**: 多くの掘る系アクションの結果として 158 が生成され、'
date: '2026-09-08'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:751-761
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-07 アイテムID 158 は「穴」 — `MEDIUM`

**根拠**: 多くの掘る系アクションの結果として 158 が生成され、
**158 のマスをさらに掘るとアクション28で `g_EmptyItem` に戻る**という対称性
(decompile)。実機でキュー残骸に `対象=201 / 結果=158` を観測 (memory)。

**未確定**: アイテム名は romfs 側のテーブルにあり `.code` からは引けない。
ID 38 / 43 / `0x20A1`-`0x20A6` の実体も同様に未確定。

---

