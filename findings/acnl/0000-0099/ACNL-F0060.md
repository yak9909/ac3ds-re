---
id: ACNL-F0060
aliases:
- F-22
title: F-22 隣マスが掘れない原因は対象アイテムの照合 — `HIGH`
summary: 複数マス掘りで隣マスに穴が空かず、かつキューが詰まる原因は**同一**だった。
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5893276
- 5896240
- 3139088
- 6968284
- 3141176
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1169-1242
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-22 隣マスが掘れない原因は対象アイテムの照合 — `HIGH`

複数マス掘りで隣マスに穴が空かず、かつキューが詰まる原因は**同一**だった。

### 判定経路

```
Player_StartFieldAction
  → FieldAction_Dispatch case0 → FieldAction_Case0 (0x59EC9C)
      → FieldAction_CanApply(rec)          (0x59F830)
          item = Field_GetItemAtXY(mapmgr, rec[19]=X, rec[20]=Y, rec[14]&1)
          if (!item) return 0
          switch (rec[12] >> 2)            // actionID
            case 0x13 (=19 掘る):
              return Item_SameId(item, rec)   (0x2FE610)
```

`Item_SameId` は 8 命令:

```
LDRH R0, [R0]          ; そのマスの実アイテム ID
LDRH R1, [R1]          ; レコードの対象アイテム ID (rec[0..1])
BIC  R0, R0, #0x8000
BIC  R1, R1, #0x8000
CMP  R0, R1
MOVEQ R0, #1
MOVNE R0, #0
BX   LR
```

**そのマスの実アイテム ID と、レコードに記録された対象アイテム ID が一致するか**を見る。

### 何が起きていたか

ケーブは `Player_StartFieldAction` の a2（対象アイテム*）に
**中心マスのアイテムポインタ**をそのまま渡していた。隣マスの実際の中身とは
一致しないため `Item_SameId` が 0 を返し、`FieldAction_CanApply` が 0、
`FieldAction_Case0` の条件が false になって `rec[13] |= 8` → case 2 →
`slot[15] = 3` で滞留する。

**穴が空かないこと**と**スロットが解放されず 3 回で詰まること**が、
これ 1 つで両方説明できる。

### 実機での裏付け

ケーブ内 `BL` の直後で停止させて観測:

```
R0 = 0                     ← スロット取得は成功している
slot0  X=60 Y=22 action=19 item1=0x009E(穴) [17]=0x00
       [15] = 3            ← case 2 = 不成立
```

引数・座標・`[17]` はすべて正しいのに `[15]=3` に落ちる。
中心マスは `[15]=2`（case 1 = 成立）になる。差は対象アイテムだけ。

### 修正

隣マスの実アイテムを取り直して a2 に渡す:

```
BL   Field_GetMapManager        ; 0x6A53DC
MOV  R1, X+1 / MOV R2, Y / MOV R3, #0
BL   Field_GetItemAtXY          ; 0x2FEE38 → R0 = 隣マスの item*
CMP  R0, #0 / BEQ skip          ; マップ範囲外なら何もしない
MOV  R1, R0                     ; a2 = 隣マスの実アイテム
```

同じマスのものを比較するので必ず一致する。

**含意**: v1 が `Field_GetItemAtXY` を呼ぼうとしていたのは方向として正しかった。

---

