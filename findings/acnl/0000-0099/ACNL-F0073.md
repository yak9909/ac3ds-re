---
id: ACNL-F0073
aliases:
- F-35
title: F-35 【訂正】`FieldObj_RevertRecord` は「結果を確定させる」処理 — `HIGH`
summary: F-28 で「レコードをキャンセルするときに元のアイテムへ戻す処理」と記録したが**誤り**。
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1478152
- 5899420
- 5899416
- 10150472
- 10150468
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1674-1694
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-35 【訂正】`FieldObj_RevertRecord` は「結果を確定させる」処理 — `HIGH`

F-28 で「レコードをキャンセルするときに元のアイテムへ戻す処理」と記録したが**誤り**。

斧で竹を切り、**倒れる演出がフェードアウトし終わる直前**に
`Field_SetItemAt` (`0x168E08`) で停止させて観測:

```
LR = 0x5A049C  → 呼び出し元 0x5A0498 (FieldObj_RevertRecord 内)
R0(X)=64  R1(Y)=27
[SP+0] = 0x9AE248 = レコード配列 rec[4] = item1（結果アイテム）→ ID 0x21 (切断竹)
R4 = 0x9AE244 = 22B レコード配列の先頭
```

**`FieldObj_RevertRecord(rec)` は「演出が完了した時点でレコードの `item1` をマスへ設定する」。**
建物侵入時にも呼ばれるのは、マップ遷移で進行中のレコードを片付けるため。

**含意**: レコードさえ登録されていれば、演出完了後の置換はゲームが自動で行う。

---

