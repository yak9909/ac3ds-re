---
id: ACNL-F0041
aliases:
- F-03
title: F-03 地面オブジェクト定義テーブル — `HIGH`
summary: '`0x3306FA00 + 16 * ID`（16B × 254、リニアヒープ）。`+0x0A` = カテゴリ、'
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:695-710
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-03 地面オブジェクト定義テーブル — `HIGH`

`0x3306FA00 + 16 * ID`（16B × 254、リニアヒープ）。`+0x0A` = カテゴリ、
`+0x0D` = 成長段階数 (signed, `-1` は非成長)。

**根拠**: decompile (`Item_GetFieldObjDef`, `Item_GetCategory`) + memory 実読。

実測: ID38→cat4/段階4、ID43→cat8/段階4、ID139→cat23/段階2、
ID153→cat10/段階-1、ID158→cat0/段階-1、ID201・204→cat21/段階-1。

`Item_GetCategory` が返す cat4/cat8 は `Item_IsGrowableCategory` の
判定集合 `{4,6,8,25}` と一致する。独立に求めた 2 結果が噛み合っており、
テーブル構造の解釈が正しいことの裏付けになる。

---

