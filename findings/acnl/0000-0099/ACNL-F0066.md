---
id: ACNL-F0066
aliases:
- F-28
title: F-28 マスへのアイテム書き込み API — `MEDIUM`
summary: '`sub_168E08(X, Y, flag, pNo, item)` (`0x168E08`):'
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1478152
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1438-1455
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-28 マスへのアイテム書き込み API — `MEDIUM`

`sub_168E08(X, Y, flag, pNo, item)` (`0x168E08`):

```
unk_2FC8F0(tmp, item);                      // item をローカルへコピー
mapmgr = (pNo == 165) ? Field_GetMapManager()
                      : unk_2FE9D4(unk_6F8954(pNo));
if (unk_2F75E4(4, pNo)) { ... 既存アイテムの後始末 ... }
unk_2FC950(mapmgr, tmp, X, Y, flag);        // マスへ書き込む
```

`sub_5A037C(rec)` は actionID (`rec[16]`) で分岐し、
**case 19 を含む多数のケース**で `sub_168E08(rec[14], rec[15], rec[12]&1, rec[21])` を呼ぶ。
これはレコードをキャンセルするときに**元のアイテムへ戻す**処理。

---

