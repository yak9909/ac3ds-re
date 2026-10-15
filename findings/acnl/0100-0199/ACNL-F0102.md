---
id: ACNL-F0102
aliases:
- F-64
title: 'F-64: FOXXY の `pseudoType0x21` と、FOXXY 用 USA→JPN 変換'
summary: 'confidence: **HIGH**（仕組みとアドレス対応）/ **LOW**（画面上の見た目）'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5849088
- 5910528
- 5893592
- 5899424
- 5898176
- 5892344
- 5907188
- 5901356
- 5861716
- 5855884
- 5869740
- 5863908
- 5897340
- 5891508
- 5914624
- 5860556
- 5896240
- 5896332
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4171-4346
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-64: FOXXY の `pseudoType0x21` と、FOXXY 用 USA→JPN 変換

confidence: **HIGH**（仕組みとアドレス対応）/ **LOW**（画面上の見た目）

### 0. ★副産物: FOXXY の USA→JPN は `−0x16C8`（この帯域限定）

FOXXY は USA 専用で地域変換を持たない（F-57）。Vapecord の表に載っていない
アドレスも多いが、**`0x594000`-`0x5A3000` の帯では差分が一定**だった。

- Vapecord の表でこの帯域に入る 51 件のうち **50 件が `0x16C8`**（残り 1 件 `CLEARLOCKED` のみ `0x2C44`）
- **バイト単位の裏取り**: FOXXY が解除時に書き戻す `0xEB000019` が
  JPN `0x59EDD8` の素の値と完全一致した

これで表に無いアドレスも引ける（**使うときは必ず命令を目で確認すること**）:

| FOXXY (USA) | JPN | 正体 |
|---|---|---|
| `0x5A04A0` | `0x59EDD8` | `BL FieldAction_TreeDropItem`（フック位置） |
| `0x59FFC0` | `0x59E8F8` | `FieldAction_Dispatch` |
| `0x5A22F4` | `0x5A0C2C` | actionID の分岐本体（FOXXY 名 `DropIDSwitch`） |
| `0x597154` | `0x595A8C` | `Player_BeginFieldObjAction` |
| `0x5990AC` | `0x5979E4` | `Drop_FindTargetTile` |
| `0x59FC7C` | `0x59E5B4` | `Item_PlaceItem` |

### 1. `dropPkt` は 22 バイトで、本解析の読みと一致

`Includes/Game.hpp:121` の構造体が **F-44 / F-61 の読みを独立に裏付けた**。

| FOXXY | offset | 本解析 |
|---|---|---|
| `replaceID` / `placeID` / `showID` | +0 / +4 / +8 | item1 / item2 / item3 |
| `combinedDropIDPlayerIndex` | +12 | `a1[12]`（actionID = `>>2`、playerIdx = `&3`） |
| `processFlags` | +13 | `a1[13]` |
| `paramFlags` | +14 | `a1[14]` = F-44 の `Flags` |
| `flags` | +15 | `a1[15]` |
| `roomID` / `wX` / `wY` | +18 / +19 / +20 | `a1[18]` / `a1[19]` / `a1[20]` |

**合計 22 バイト = `Net_SendPacket(58, dest, rec, 22)` のサイズと一致。**

### 2. ★`FieldAction_Dispatch` の分岐キーは actionID ではない

F-61 で名前は付けたが中身を詰めていなかった点の訂正。

**分岐は `processFlags`(`a1[13]`) の bit2-5**（0-9）で、actionID とは別物。

```
0 -> FieldAction_Case0
3 -> FieldObj_ApplyDigRecord(actionID = a1[12]>>2, ...)
4 -> FieldAction_ClearActive
7 -> ★bit2-5 を 3 に直して再入 → その後 Net_SendPacket(58, 4, a1, 22)
     ＝「自前で実行し、かつ全員に同報」という正規の経路
8 -> FieldAction_RegisterActive
```

FOXXY は `processFlags` に **オンラインなら `0x1C`（bit2-5 = 7）**、
オフラインなら `0x0C`（= 3）を入れる。
つまり**他プレイヤーにも見せるための正規ルートを使っている**。

### 3. 仕組み

`PlaceItemWrapper(ID = 0x21, ...)` のときだけ:

1. `0x59EDD8`（`BL FieldAction_TreeDropItem`）を NOP にしてから
   CTRPF の `Hook` を張り、`pseudoType0x21` へ飛ばす
2. `PlaceItem` には **ID `0xF`** を渡す
   （`FieldAction_Case0` は actionID ∈ {8,9,14,15} で木の落下経路に入り、
   9 と 15 は `FruitTree` を見ずに直接 `TreeDropItem` を呼ぶ。だから必ずフックに来る）
3. フック内で:
   - **2 つ目のレコード**を作る。`actionID = 0x21`（`0x84 >> 2`）、
     `replaceID = showID = 0x71`、`placeID` は元の `placeID`、座標は元の目標マス
     → `FieldAction_Dispatch` へ流す
   - **元のレコードを書き換える**。座標を**自分の足元**に、
     `replaceID = 0x71`、`placeID` = 足元にあるアイテム、
     `showID` = 元の `placeID`、`paramFlags = 0x8`
   - `flags` に **相対変位**を詰める: `((dx+4)&0xF) | (((dy+4)&0xF)<<4)`
4. フックから戻ると、書き換わった元レコードが通常経路を続行する

**`0x71` = `tree (item)`**（`REFERENCES/IDS/.../All_ACNL_Items.txt` で確認）。

### 4. ★`0x21` はゲームに存在しない actionID

`sub_5A0C2C`(`0x5A0C2C`) の case は **`0xA` / `0x22`（共用）/ `0xB` / `0xC` / `0xD`** だけ。
`0x21` は **`default:` に落ち、`state = 2`（完了）を入れるだけ**。

念のため `0x594000`-`0x5A4000` を走査したが **`CMP Rn,#0x21` は 1 件もない**
（`0x22` は `0x596CCC` に 1 件）。**本当に未使用の ID。**

ただし `FieldObj_ApplyDigRecord` は登録前に
`FieldObj_FindRecord` → `FieldObj_RevertRecord` で
**そのマスの既存レコードを取り消して巻き戻す**。
`0x21` は「何もしないが、マスの既存処理を潰して即完了するレコード」として働く。

### 5. 何が「面白い」のか

- **ゲームが持っていない動作 ID を作り、正規のディスパッチャに通している。**
  未使用 ID が `default:` で安全に完了する設計を突いている
- **`flags`(+15) に相対変位を詰められる**ことを利用している。
  ドロップレコードの形式が「記録された座標からのオフセット配置」を
  表現できることを示す
- **`processFlags` の case 7 を使って他プレイヤーにも同報させている。**
  F-61 の host drop が同報を潰す方向だったのと対照的で、
  こちらは**正規の「実行して全員に伝える」経路に乗せている**

### 6. 未確認（LOW）

- **画面上どう見えるかは未検証。** 2 つのレコードの合成結果は静的には追い切れない
- 目的は `0x71` = tree と actionID 0xF（木の落下系）から
  **「離れた場所の木に何かを落とさせる／木を絡めた配置をする」**あたりと推測されるが、
  **推測の域を出ない**
- `state = 2` になったレコードを後段で処理するものがあるかは未調査

### ★F-64 訂正: `0x21` は「存在しない ID」ではなく「検証なし・演出なしの正規枠」

上の §4 で「`0x21` はゲームに存在しない actionID」と書いたが**誤り**。
`sub_5A0C2C` の switch だけを見て一般化してしまった。

#### 一次情報: ドロップ種別は 0x00-0x21 の 34 エントリ

**`FieldAction_CanApply`(`0x59F830`) の中、`0x59F88C` に
`rec[12] >> 2`（ドロップ種別）で引く 34 エントリのジャンプテーブルがある。**
索引は `0x00`-`0x21` で、**`0x21` が種別の上限**。
Vapecord ラベル `DADD` はこのテーブル先頭で、
FOXXY は `main.cpp:50` で 34 エントリ全部を自前ハンドラで埋めている。

つまり**ドロップ種別は 0x21 までの正規の列挙値**。

#### `case 0x21` は「無条件で許可」

`FieldAction_CanApply` の各ケースは何かを検証するが、`0x21` だけ違う:

| 種別 | 判定 |
|---|---|
| 1-5 | 埋まっていない && `Item_SameId` |
| 6,7,9,0xB,0xF,0x11-0x13,0x1B-0x1F | `Item_SameId` |
| 8, 0xE | `Item_SameId` + FruitTree / `g_TreeHitCounts` の打撃カウンタ |
| 0xA,0xC,0xD,0x1A,0x22 | `Item_IsEmpty`（空マスでないと不可） |
| 0x14-0x19 | `Item_SameId` + `Item_IsBuriedFlag` |
| 0x20 | `Item_IsBuriedFlag` + `Item_SameId` |
| **0x21** | **`return 1`。全検証を飛ばす唯一の種別** |
| default | 0 |

#### 一方 `sub_5A0C2C` では演出がない

`sub_5A0C2C` の case は効果音と配置関数を選ぶ = **「ドロップの演出」の決定**:

```
0xA / 0x22  Sound 16778582 + sub_59A4A0
0xB         Sound 16778582 + sub_59AFD8 + sub_5C24A8
0xC         Sound 16778798 + sub_5A0594 + sub_599FBC
0xD         Sound 16779596 + sub_59A038
default     state = 2 を入れるだけ（音も演出もなし）
```

`0x21` はここに case が無く default に落ちる。

#### まとめると

**`0x21` = 「置く条件を一切問わず、演出も出さない」ドロップ種別。**
検証を通すのに使えるが、配置そのものは行わない。
だから FOXXY は実配置を種別 `0xF` にやらせ、`0x21` のレコードは別に注入している。
これが `pseudo`（＝種別 0x21 を騙る）という名前の意味。

#### これは「ドロップ方法を変える」類か → **はい**

- FOXXY の `DropType` は**利用者がメニューで選ぶ値**（既定 `0xA`、`DropType = index + 1`）
- ゲーム側もドロップ種別を 0x00-0x21 の列挙として持ち、
  `sub_5A0C2C` で**種別ごとに効果音と配置関数を切り替えている**
- `drop.txt` の「掘ってドロップ」「植える動作でドロップ」「回転ドロップ」
  「岩砕いてドロップ」等は、この種別を差し替えるチート群と考えられる
  （個々の対応付けは未確認）

`0x21` はその列挙の末尾にある**特権枠**で、
「どこにでも・何の上にでも・音も演出もなく置ける」原始的な手段になっている。

---

