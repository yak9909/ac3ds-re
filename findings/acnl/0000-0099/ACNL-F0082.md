---
id: ACNL-F0082
aliases:
- F-44
title: F-44 `Item_PlaceItem` (0x59E5B4) — 資料と逆コンパイルが完全一致 — `HIGH`
summary: '出典: `REFERENCES/TEXTS/drop_method.txt`。**実機の逆コンパイルと行単位で一致した。**'
date: '2026-09-08'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5891508
- 10150236
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2159-2233
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-44 `Item_PlaceItem` (0x59E5B4) — 資料と逆コンパイルが完全一致 — `HIGH`

出典: `REFERENCES/TEXTS/drop_method.txt`。**実機の逆コンパイルと行単位で一致した。**
従来 `Player_StartFieldAction` と呼んでいたもの。実名は `ACNL_Item::PlaceItem`。

```c
int __fastcall Item_PlaceItem(
        int   DropType,          // アクションID (14/15/16/18/19/26/28 など)
        void *ItemToReplace,     // 置き換え元（木そのもの）
        void *ItemToPlace,       // 置き換え先（切り株・切断竹）★
        void *ItemToShow,        // 表示用。伐採経路では g_EmptyItem
        u8    wX, u8 wY,
        char  IsInside,          // 屋内か
        char  PlayerSide,        // AcPlayer+0x2E (s16) > 0 ★倒れる向き
        char  FruitTree,
        char  CrashTree,         // ★倒すか。従来 R6 と呼んでいたもの
        char  HitCount);         // 打撃数
```

空きスロットを `g_DropDataTable`（`0x9AE15C`, 18B × 4）から探し、
**満杯なら `-1` を返す**（`while (State) { if (++Slot >= 4) return -1; }`）。

### `Flags`（`+17`）のビット定義

```c
Flags = (CrashTree << 5) & 0x20      // bit5
      | (FruitTree << 2) & 0x1C      // bit2-4
      | (PlayerSide << 1) & 2        // bit1
      | IsInside                     // bit0
      | (HitCount << 6);             // bit6-7
```

**これが F-41 / F-42 を独立に裏付けた。** 実測した `Flags = 0xE2` を分解すると:

| bit | 名前 | 値 | 一致する自前の観測 |
|---|---|---|---|
| 0 | `IsInside` | 0 | 屋外 |
| 1 | `PlayerSide` | **1** | 終端処理が `kind=5` を選ぶ = **倒れる向き**（F-41） |
| 2-4 | `FruitTree` | 0 | — |
| 5 | `CrashTree` | **1** | `flags & 0x20` が成立し `a2 = ItemToPlace`（F-41） |
| 6-7 | `HitCount` | **3** | ケーブが打撃カウンタに書いた 3（F-42） |

つまり:

- `FieldObj_FinalizeRecord` が読む `flags & 0x20` は **`CrashTree`**
- `kind` 4/5 を分ける `flags` bit1 は **`PlayerSide`**、出どころは `AcPlayer+0x2E` の符号
- レコードの `item1` は **`ItemToPlace`**

**「倒れる向きが `PlayerSide` で決まる」は資料には書かれていない**（資料では `Unk1`）。
こちらの実測で意味が確定した分。

### その他

- `DropType == 16` のときだけ `State = 2` にして即時実行しない
  （資料の `DROPTYPE_HIT_BELL_ROCK`）
- 他プレイヤーがいてホストでないときは `sub_623F80(58, 0, rec, 22)` で送信。
  資料の `netgame::NetGameMgr::SendPacketToPlayer(PLAYER_PACKET_DROP, ..., 0x16u)` と
  サイズ `0x16 = 22` まで一致

### 構造体 `DropData`（18 バイト）

| off | 資料の名前 | 従来の呼び方 |
|---|---|---|
| +0 | `ItemToReplace` | item0 |
| +4 | `ItemToPlace` | item1 |
| +8 | `ItemToShow` | item2 |
| +12 | `wX` | X |
| +13 | `wY` | Y |
| +14 | `DropType` | actionID |
| +15 | `State` | state |
| +16 | — | スロット番号 |
| +17 | `Flags` | flags |

---

