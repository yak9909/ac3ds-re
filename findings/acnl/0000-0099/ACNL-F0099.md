---
id: ACNL-F0099
aliases:
- F-61
title: 'F-61: `REFERENCES/CHEATS/drop.cpp` の「host drop」の正体'
summary: 'confidence: **HIGH**（静的解析。素の命令・分岐先・Vapecord の表が三方で一致）'
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5897380
- 5897340
- 5891508
- 5891548
- 3131580
- 3192876
- 7722916
- 5891880
- 5897612
- 5897260
- 5892244
- 5891792
- 5860652
- 5860884
- 5890520
- 5894888
- 5895980
- 5890492
- 5893276
- 5893700
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:3687-3816
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-61: `REFERENCES/CHEATS/drop.cpp` の「host drop」の正体

confidence: **HIGH**（静的解析。素の命令・分岐先・Vapecord の表が三方で一致）

### 結論

**通信プレイ中に、ホストでないクライアントへホストの処理経路を通させるパッチ群。**
9 箇所すべてが「自分がホストか / この動作は誰のものか」を見る**条件分岐の固定**で、
`drop`（`DROPM`）とは別物。

### 1. まずアドレスの版

**この 7 行は日本語版アドレス**。1 行目の `USA0x0059FCA4` とは出所が違う。

- Vapecord `Addresses.hpp` の `HOST1`-`HOST9` の**JPN 列（index 4）と全一致**
- USA 列には 1 つも存在しない
- JPN のダンプで全部 `0A00xxxx` = `BEQ` としてデコードでき、
  パッチ値が**変位を保ったまま条件だけ変えている**
  （`0A000010→EA000010` / `0A000022→EA000022` / `0A00002D→EA00002D` /
  `0A000003→EA000003` / `0A000004→EA000004`）。5 命令の変位一致は偶然では起きない

一方コメント中の `//bypass check in 0x59FC7C` は **USA** の `Item_PlaceItem`
（`PLACEITEMOFFSET`、JPN `0x59E5B4`）。**同一ファイル内で版が混ざっている。**

裏付け: `DROPM` は USA `0x59FCA4` = USA PlaceItem `0x59FC7C` + `0x28`、
JPN `0x59E5DC` = JPN PlaceItem `0x59E5B4` + `0x28`。オフセットまで一致する。

### 2. 前提となる述語（本解析で命名）

| addr | 名前 | 中身 |
|---|---|---|
| `0x2FC8BC` | `Net_IsMultiplayer` | `vc_GETPLAYER2(net) > 1`（参加人数 2 人以上） |
| `0x30B82C` | `Net_IsHost` | `Net_GetLocalPlayerIndex(net) == 0` |
| `0x75D7A4` | `Net_GetLocalPlayerIndex` | 接続中なら `*(u8*)(net+78440)`、でなければ 0 |

`Net_IsHost` の根拠は、ガードが崩れた側で
`Net_SendPacket(58, **0**, rec, 22)`（`Item_PlaceItem` 0x59E728）＝
**プレイヤー 0 宛に送る**こと。つまり 0 番＝ホスト。
呼び出し元 30 件以上の汎用述語で、drop 専用ではない（F-55 の見分け方）。

### 3. 9 箇所の内訳

| ラベル | JPN | 素の値 | パッチ | 効果 |
|---|---|---|---|---|
| `DROPM` | `0x59E5DC` | `0A000004` | `EA000004` | **別物**。下記 §5 |
| `HOST1` | `0x59FD8C` | `0A00002C` | NOP | ロック生成を**常に全員へ同報** |
| `HOST2` | `0x59FC2C` | `0A00002C` | NOP | ロック解除を**常に全員へ同報** |
| `HOST3` | `0x59E894` | `0A000010` | `EA000010` | 常に自前実行 |
| `HOST4` | `0x59E6D0` | `0A000003` | `EA000003` | 常に自前実行 |
| `HOST5` | `0x596D2C` | `0A00001D` | NOP | 常に自前実行（汎用関数、作者も「unnecessary?」） |
| `HOST6` | `0x596E14` | `0A000025` | NOP | 同上 |
| `HOST7` | `0x59E1D8` | `0A00003B` | NOP | 常に自前実行 |
| `HOST8` | `0x59F2E8` | `0A000022` | `EA000022` | 木のアイテム落下を自前実行 |
| `HOST9` | `0x59F72C` | `0A00002D` | `EA00002D` | 木の果実落下を自前実行 |

**★NOP と「無条件分岐化」が混在するのは、分岐先が箇所ごとに逆だから**であって
意図は 1 つ。

- `BEQ` の飛び先が**自前実行側**（HOST3/4/8/9）→ 無条件分岐にして常に自前実行
- `BEQ` の飛び先が**依頼・送信側**（HOST5/6/7）→ NOP にして落ちさせ自前実行
- `BEQ` が**同報ブロックを飛ばす**（HOST1/2）→ NOP にして常に同報

典型形（HOST7, `0x59E1BC`-）:

```
BL Net_IsMultiplayer ; 通信中でなければ loc_59E1DC（自前実行）
BL Net_IsHost
BEQ loc_59E2CC       ; ★ホストでなければ「ホストへ依頼」側へ ← ここを NOP
loc_59E1DC: BL FieldAction_Dispatch
```

HOST1/2 だけ向きが逆に見えるが、この送信は**ホストの義務**
（`Net_SendPacket(58, 4, …)`、dest 4 = 全員、生成 0x20 / 解除 0x24）。
ホストを騙る以上、ロックの生成・解除を他クライアントへ告知しないと整合が崩れる。

### 4. 木の 2 本（HOST8 / HOST9）の裏取り

作者ラベルは「item tree drop」「fruit tree drop」。
どちらも `FieldAction_Case0`(`0x59EC9C`) からのみ呼ばれ、分岐条件は

```
FruitTree = (rec[14] << 27) >> 29        // ★F-44 の Flags の bit2-4
  FruitTree == 2      -> FieldAction_TreeDropItem  (0x59EE44, HOST8)
  FruitTree == 1 or 4 -> FieldAction_TreeDropFruit (0x59F3D8, HOST9)
```

**F-44 で確定済みの `Flags` ビット割り当てと一致する**ので、
ラベルは作者の主観ではなく実際の区別だと確認できた。

### 5. `DROPM` は host drop ではない

`drop.cpp` 1 行目の素の `drop` チート。`Item_PlaceItem` の**空きスロット探索**:

```
while (g_DropDataTable[i].State) { if (++i >= 4) return -1; }
```

`0x59E5DC` はこのループの脱出 `BEQ`。`EA000004` で無条件化すると
**占有状態を無視して常に `i = 0` を使う** = 4 枚の待ち行列を実質無効化し、
連続ドロップを可能にする。

**★副作用: 処理中のレコードを上書きして潰す。**
F-42 でキューが詰まった件と同じテーブルなので、併用時は注意。

### 6. IDA へ反映済み

| addr | name |
|---|---|
| `0x2FC8BC` | `Net_IsMultiplayer` |
| `0x30B82C` | `Net_IsHost` |
| `0x75D7A4` | `Net_GetLocalPlayerIndex` |
| `0x59E878` | `FieldAction_SendOrDispatch` |
| `0x59FBB0` | `FieldAction_ClearActive` |
| `0x59EE44` | `FieldAction_TreeDropItem` |
| `0x59F3D8` | `FieldAction_TreeDropFruit` |

`g_FieldActionActive`(`0x9AE1A4`) のレイアウトも確定（STRB 列 `0x59FD5C`-`0x59FD68`）:
**`+0 wX / +1 wY / +2 playerNo / +3 flags / +4 actionID`、5B × 32、
空きの印は `+2 playerNo == 165 (0xA5)`。**
`g_DropDataTable`(`0x9AE15C`, 18B × 4) とは別テーブル。

### 7. 未確認

- 実機で当てたときの挙動は未検証（静的解析のみ）
- `sub_596C84`（HOST5/6 の包含関数）の正体。呼び出し元 8 件以上の汎用処理
- ホストを騙る以上、**同じ部屋の他プレイヤーの整合性に影響する**。
  オンラインで使えば相手側の状態を壊しうる

---

