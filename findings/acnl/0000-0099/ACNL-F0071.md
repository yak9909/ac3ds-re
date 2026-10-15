---
id: ACNL-F0071
aliases:
- F-33
title: F-33 `Item_Copy` ではオブジェクトが破棄されない — `HIGH`
summary: マップデータに直接 `Item_Copy` で書き込むと、**元々そこにあった物のオブジェクトが
date: '2026-09-08'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1478152
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1611-1632
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-33 `Item_Copy` ではオブジェクトが破棄されない — `HIGH`

マップデータに直接 `Item_Copy` で書き込むと、**元々そこにあった物のオブジェクトが
実体なしで残る**（見た目だけ残り当たり判定が無い状態）。

正しくは `Field_SetItemAt(X, Y, flag, pNo, item*)` (`0x168E08`) を使う。
内部の `unk_2FC950` が古いオブジェクトを破棄してから設定する。
中心マスの case 19 もこれを使っている。

引数の取り方（中心マスと同一）:

```
flag = rec[12] & 1        LDRB R2,[R4,#0xC] / AND R2,R2,#1
pNo  = rec[21]            LDRB R3,[R4,#0x15]
item = スタック引数 a5     STR R0,[SP,#0]
```

書き込む値だけが中心マスと異なる（中心は `g_EmptyItem`、周囲は 158＝穴）。
その後 `Field_MarkDirty(X, Y)` も本来どおり呼ぶ。

---

