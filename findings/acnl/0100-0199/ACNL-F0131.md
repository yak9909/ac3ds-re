---
id: ACNL-F0131
aliases:
- F-93
title: 'F-93: ドロップの可否判定は 2 段。F-65 コード B が無効だった理由'
summary: 'confidence: **HIGH**（実機で検証。コード A・B の結果が予測と一致／不一致を確定させた）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5857412
- 1463368
- 5896240
- 1463568
- 1463580
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5338-5464
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-93: ドロップの可否判定は 2 段。F-65 コード B が無効だった理由

confidence: **HIGH**（実機で検証。コード A・B の結果が予測と一致／不一致を確定させた）

### 実機結果

| コード | 内容 | 結果 |
|---|---|---|
| A `00596178 E3A00021` | 通常ドロップの種別を `0x21` に | **何も起きない**（予測どおり） |
| B `0059F8B0 0059FA58` | 種別 `0x0A` の `FieldAction_CanApply` を無条件許可に | **変化なし**（★予測が外れた） |

コード A は F-65 の予測どおり。`0x21` は `sub_5A0C2C` に case が無く配置処理が走らない。

### ★コード B が効かなかった理由: 判定が 2 段だった

`Player_DropItem`(`0x596084`) の流れ:

```c
if (!Drop_FindTargetTile(&x, &y, ...)) return -1;   // ←★ゲート1
Item_PlaceItem(10, ..., x, y, ...);                  //   その後 ゲート2
```

| | 関数 | 役割 |
|---|---|---|
| **ゲート1** | `Drop_FindTargetTile` → **`Field_CanPlaceItemAt`(`0x165448`)** | **どのマスを選ぶか** |
| **ゲート2** | `FieldAction_CanApply`(`0x59F830`) | 選ばれたマスの検証 |

`Field_CanPlaceItemAt` の中身:

```c
result = Item_IsEmpty(tile);   /* 0x165510  BL Item_IsEmpty (EB065D83) */
if (!result) return result;    /* 0x16551C  空でなければ 0 */
```

**ゲート1 が空マスしか返さないので、ゲート2 の `Item_IsEmpty` は
通常経路では絶対に失敗しない。** だからコード B は単独では何も変えない。

**コード B は「二重ロックの 2 つ目」で、必要だが十分ではなかった。**

### ★「物を重ねて置ける」の 1 行目を読み落としていた

F-65 で「コード B は `drop.txt` の『物を重ねて置ける』が既にやっていること」と書いたが、
**あのチートの 1 行目 `00165510 E1A00000` を勘定に入れていなかった**。
実際の構成は:

```
00165510 E1A00000     ← ゲート1（Field_CanPlaceItemAt の Item_IsEmpty）★これが本体
0059F8B0 0059FA58     ← ゲート2、種別 0x0A
0059F8B4 0059FA58     ← 種別 0x0B
0059F8B8 0059FA58     ← 種別 0x0C
0059F8BC 0059FA58     ← 種別 0x0D
0059E6D0 EA000003     ← HOST4  （F-61）
0059E894 EA000010     ← HOST3
0059FC2C E1A00000     ← HOST2
0059FD8C E1A00000     ← HOST1
```

CLAUDE.md の「チートの実装を読むときはメニュー項目の全体を読む」(F-58) と
「値を使う側ではなく値を決める側を疑う」を、まさに両方踏んだ。

### 逆向きも成立しない

ゲート1 だけ外してゲート2 を素のままにすると、
`Drop_FindTargetTile` が占有マスを返した後 `FieldAction_CanApply` の
種別 `0x0A` = `Item_IsEmpty` で弾かれ、`FieldAction_Case0` の
`if (CanApply && FindActive == -1)` が不成立になる。**両方必要。**

### `Field_CanPlaceItemAt`(`0x165448`)

`(wX, wY, roomID, mode, checkPlayers)`。呼び出し元 6 件は全部ドロップ系:
`Drop_FindTargetTile` / `FieldAction_TreeDropItem` / `FieldAction_TreeDropFruit` /
`sub_596C2C` / `sub_598BEC` / `sub_5A1268`。

**`0x165510` を NOP にすると 6 経路すべてに効く**ので、
木の果実・アイテム落下も占有マスに落ちるようになる。

### F-93 追記: 木の落下だけがゲート1 単独で効く理由（実機確認済み）

`00165510 E1A00000` を当てた実機で
**木の果実・アイテム落下が占有マスに落ちるようになったことを確認。**

これは二段ゲート説の裏付けになる。`FieldAction_CanApply` の種別別判定を見ると:

| 種別 | ゲート2 の判定 | 空マス判定 |
|---|---|---|
| `8` | `Item_SameId` + FruitTree | なし |
| `9` / `0xF` | `Item_SameId` | なし |
| `0xE` | `Item_SameId` + `g_TreeHitCounts` | なし |
| **`0x0A`（通常ドロップ）** | **`Item_IsEmpty`** | **あり** |

木の落下が使う actionID は `FieldAction_Case0` の分岐から `{8, 9, 0xE, 0xF}`。
**どれもゲート2 に空マス判定を持たない**ので、
`Field_CanPlaceItemAt`（ゲート1）が唯一の関門だった。
→ `0x165510` の NOP だけで即座に効く。

通常ドロップ `0x0A` はゲート1・ゲート2 の両方に空マス判定があるので 2 行必要。
**観測結果がこの非対称性をそのまま示している。**

### F-93 確定: 二段ゲートを実機で完全に確認

| 段階 | コード | 実機結果 |
|---|---|---|
| ゲート2 のみ | `0059F8B0 0059FA58` | **変化なし** |
| ゲート1 のみ | `00165510 E1A00000` | **木の果実・アイテム落下が占有マスへ**（通常ドロップは不可） |
| **両方** | 上の 2 行 | **通常ドロップでも重ね置き可** |

**二段ゲート説はこれで確定。**

- ゲート1 `Field_CanPlaceItemAt`(`0x165448`) … どのマスを**選ぶ**か
- ゲート2 `FieldAction_CanApply`(`0x59F830`) … 選ばれた後の**検証**

木の落下（actionID `8/9/0xE/0xF`）はゲート2 に空マス判定が無いため
ゲート1 だけで効き、通常ドロップ（`0x0A`）は両方に空マス判定があるので 2 行必要 ——
**3 通りの観測がこの非対称性をそのまま裏付けた。**

得られた原則:

> **「判定が 1 箇所だ」と仮定しない。**
> 対象を*選ぶ*処理と、選ばれた対象を*検証*する処理は別に置かれていることがある。
> 片方だけ外して「効かない」ときは、もう一方を探す。

`drop.txt`「物を重ねて置ける」が 1 行目に `00165510` を置いていたのは
この構造を作者が把握していたから。**F-65 でその 1 行を読み落としたのが原因だった**
（CLAUDE.md「チートの実装を読むときはメニュー項目の全体を読む」F-58 の再発）。

---

