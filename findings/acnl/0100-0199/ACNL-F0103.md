---
id: ACNL-F0103
aliases:
- F-65
title: 'F-65: 通常ドロップの入口と、種別を変える AR コード'
summary: 'confidence: **HIGH**（静的解析。チートの復元値と逆コンパイルが一致）/ 実機未検証'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5857412
- 5857656
- 5857364
- 5863196
- 5896332
- 5896368
- 5896380
- 5896792
- 5896548
- 5896372
- 5896532
- 5896376
- 5896460
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4347-4405
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-65: 通常ドロップの入口と、種別を変える AR コード

confidence: **HIGH**（静的解析。チートの復元値と逆コンパイルが一致）/ 実機未検証

### 通常ドロップは `Player_DropItem`(`0x596084`)

```c
if (!Drop_FindTargetTile(&v8, &v9, IsInside, 0, IsId)) return -1;
...
return Item_PlaceItem(10, g_EmptyItem, ItemToPlace, item, v8, v9, IsInside[0], 0,0,0,0);
```

**第 1 引数 `10` = `0x0A` がドロップ種別**で、即値は **`0x596178`**（`E3A0000A`）。
対になる `0x596054` は `sub_595FEC` 側で素は `E3A0000C`（`0x0C` = 花植える）。

裏取り: `drop.txt`「ドロップタイプ」の「普通」エントリが
`0x596054 E3A0000C` / `0x596178 E3A0000A` を書き、**実バイナリの素の値と一致**。
FOXXY も USA `0x59771C`（= JPN `0x596054`）に `Process::Write8(DropType)` している。

### 種別の意味が確定した（TODO-23 の一部）

`drop.txt`「ドロップタイプ」のホットキー表記と `sub_5A0C2C` の case が一致:

| 値 | チートの表記 | `sub_5A0C2C` |
|---|---|---|
| `0x0A` | ドロップ | case 0xA（音 16778582 + `sub_59A4A0`） |
| `0x0B` | スコップ | case 0xB（音 16778582 + `sub_59AFD8`） |
| `0x0C` | 花植える | case 0xC（音 16778798 + `sub_599FBC`） |
| `0x0D` | マイデザ | case 0xD（音 16779596 + `sub_59A038`） |
| `0x0F` | 置いても見えない | case なし |

### ★種別表の索引は「種別 − 1」

F-64 で「索引 0x00-0x21」と書いたが正確には
**`0x59F88C` から 34 エントシ、索引 = 種別 − 1、種別は `1`-`0x22`**。

検算（`drop.txt`「物を重ねて置ける」が `0x59F8B0`-`0x59F8BC` を `0x59FA58` に向ける）:

- `0x59F8B0` = 索引 9 = 種別 `0x0A`、素 `0x59F964`
- `0x59F8B4` = 索引 10 = 種別 `0x0B`、素 `0x59F954`
- `0x59F8B8` = 索引 11 = 種別 `0x0C`、素 `0x59F964`
- `0x59F8BC` = 索引 12 = 種別 `0x0D`、素 `0x59F964`

逆コンパイルの分類（`0xA`/`0xC`/`0xD` は `Item_IsEmpty`、`0xB` は `Item_SameId`）と一致。
種別 `0x21` → 索引 32 → `0x59F90C` = **`0x59FA58`（無条件で 1）** も一致。

ハンドラ: `0x59F954` = `Item_SameId` / `0x59F964` = `Item_IsEmpty` /
**`0x59FA58` = 無条件で 1**（Vapecord ラベル `DVAL`）。

### ★「物を重ねて置ける」の正体

種別 `0x0A`-`0x0D` の判定を `0x59FA58` に向け替えて
**空マス判定を外している**だけ。つまり
**種別 `0x21` の「無検証」を、演出を保ったまま通常ドロップに移植したもの**。

AR コードは `DOCS/ar_codes.md` に記載。

---

