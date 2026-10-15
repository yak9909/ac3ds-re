---
id: ACNL-F0078
aliases:
- F-40
title: F-40 赤いバラの正体 — `FieldObj_FellObject` の `a2` が空だと `a1` から ID を流用する — `HIGH`
summary: '**衝突経路で「赤いバラの見た目をしたオブジェクト」が倒木演出中ずっと表示され、'
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5873948
- 5902744
- 5880752
- 9789428
- 5880516
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1824-1895
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-40 赤いバラの正体 — `FieldObj_FellObject` の `a2` が空だと `a1` から ID を流用する — `HIGH`

**衝突経路で「赤いバラの見た目をしたオブジェクト」が倒木演出中ずっと表示され、
演出のフェードアウトと同時に切り株へ切り替わる**現象の原因。

### 関数シグネチャ

```c
FieldObj_FellObject(item *a1, item *a2, int X, int Y, int a5, int kind, int fx)
```

- `a1` = 切り倒す対象のアイテム（木本体）
- **`a2` = 切り倒した後に残すアイテム（切り株など）**

### 分岐

```c
result = FieldObj_SpawnFallActor(v39, v41, v42, kind, v36);   // 0x59A11C 倒木アクター
if (result) {
    if (Item_IsEmpty(a2)) {                       // ★a2 が空のとき
        v18 = *(__int16 *)Item_GetFieldObjDef(a1);   // a1 の定義先頭 2 バイトを ID に流用
        if (v18 >= 0xFE) v18 = 0;
        Item_Copy(&v37, Item_InitWithId(&v36, v18));
    } else {
        Item_Copy(&v37, a2);                      // ★正しい経路
    }
    ...
    *(_DWORD *)v25 = &unk_901F4C;                 // 2 体目のアクター（残るもの）の vtable
    unk_58FB40(v25, &v37, v41, v42, 0);
}
```

`Item_GetFieldObjDef(a1)` の先頭 2 バイトは**アイテム ID ではなくフィールドオブジェクト定義の
別フィールド**であり、それを ID として解釈した結果が `0x00B2`/`0x00FA` 相当の見た目になっていた。

### 斧経路と衝突経路の実測差分（breakpoint で両方を観測）

| 経路 | 呼び出し元 | `a1` | `a2` | `kind` |
|---|---|---|---|---|
| **斧** | `0x5A1198` | ID `0x002B`（木） | **ID `0x0014`（切り株）** | **4** |
| **ぶつかる** | `0x59BBB0` | ID `0x002B`（木） | **`0x955FF4` = `g_EmptyItem`（ID `0x7FFE`）** | **0** |

**衝突経路と斧経路では `FieldObj_FellObject` の呼び出し元そのものが違う。**

衝突経路の呼び出し元 `0x59BAC4`（`PUSH {R4-R9,LR}`）の末尾:

```
0059BB94  ADD  R4, SP, #4
0059BB98  STR  R9, [SP]           ; a5
0059BB9C  LDR  R1, loc_59BBC4     ; ★a2 = 0x955FF4 (g_EmptyItem) を literal から固定で読む
0059BBA0  MOV  R3, R6             ; Y
0059BBA4  MOV  R2, R5             ; X
0059BBA8  MOV  R0, R8             ; a1
0059BBAC  STM  R4, {R7,R9}        ; [SP+4]=kind  [SP+8]=fx
0059BBB0  BL   FieldObj_FellObject
0059BBC4  DCD  0x00955FF4         ; literal = g_EmptyItem
```

`a2` は**この経路では常に空で固定**されている。元々この経路は木を倒すためのものではなく、
「残すものが決まっていない」状態で呼ばれることを前提にしている。

### 結論

**`FieldObj_FellObject` の内部（`0x59A11C` など）をフックしても `a2` は直せない。**
引数は既に渡された後だからである。**呼び出し元 `0x59BBB0` をフックする必要がある。**

**教訓**: 「渡された値を使う側」ではなく「値を決める側」を疑う。
ユーザーの指摘（「a1 の ID を渡す部分ではなく、渡された値を用いて
オブジェクトを召喚する処理が正しくないのでは」）がそのまま正解だった。

---

