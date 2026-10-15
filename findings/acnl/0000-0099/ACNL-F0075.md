---
id: ACNL-F0075
aliases:
- F-37
title: F-37 `FieldObj_InitFallActor` の `kind` が演出を決める — `HIGH`
summary: '`FieldObj_SpawnFallActor` は `FieldObj_InitFallActor(obj, item*, X, Y, kind)` を呼ぶ。'
date: '2026-09-08'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5902608
- 5902620
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1718-1758
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0078"]
---
## F-37 `FieldObj_InitFallActor` の `kind` が演出を決める — `HIGH`

`FieldObj_SpawnFallActor` は `FieldObj_InitFallActor(obj, item*, X, Y, kind)` を呼ぶ。
`kind` = `sub_592F8C` の第4引数。

```c
obj[365] = kind;
v8 = 2;
switch (obj[365]) {
    case 0: v8 = 0; break;
    case 2: v8 = 3; break;
    case 3: v8 = 1; break;
    case 4: v8 = unk_592394(obj,X,Y,-2) ? 5 : 4;  obj[364] = 1; break;
    case 5: v8 = unk_592394(obj,X,Y, 2) ? 7 : 6;  obj[364] = 1; break;
}
obj[366] = v8;
...
v17 = unk_59AAB8(モデル名, v8);     // v8 でモデル/アニメを選択
```

| kind | v8 | 実機での見え方 |
|---|---|---|
| 0 | 0 | 揺れるだけ（ぶつかったときの既定値） |
| 3 | 1 | 演出なし |
| **4** | 4 or 5 | **倒れる演出（プレイヤーが右にいるときの向き）。`obj[364]=1`** |
| **5** | 6 or 7 | **倒れる演出（逆向き）。ただし木の上部が右にずれたままフェードアウトする** |

`obj[364] = 1` が倒木フラグ。`unk_592394(obj, X, Y, ±2)` が倒れる方向を判定する。

**【追記 / F-41】** `kind` 4/5 の選択は**レコードの `flags` bit1** で行われている
（`FieldObj_FinalizeRecord` の `0x5A1110`-`0x5A111C`）。
自前で 4 か 5 を決め打ちすると向きが固定される。ゲームが決めた bit を読むこと。
モデル名は `Item_GetFieldObjDef(obj+100)[12]` を索引に 22B テーブルから引く。

**【訂正 / F-40】** 当初「`kind=5` だと赤いバラの見た目が出る」と書いたが誤り。
赤いバラは `kind` とは無関係で、`FieldObj_FellObject` の引数 `a2` が空だったことが原因。
また「`kind=4` では切り株の当たり判定が消える」も、実際にはレコード枯渇 (F-39) の
副作用だった。`kind` は倒れる演出の**向きと種別のみ**を決める。

---

