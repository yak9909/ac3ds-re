---
id: ACNL-F0101
aliases:
- F-63
title: 'F-63: `REFERENCES/CHEATS/drop.txt` の「host drop」— `drop.cpp` にない 6 行'
summary: 'confidence: **HIGH**（静的解析。素の命令・分岐先・Vapecord の表・ID 一覧が整合）'
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5891548
- 5897380
- 7485632
- 1684996
- 1685744
- 1685976
- 1687180
- 1687472
- 7485560
- 7485524
- 2555244
- 2555304
- 1685424
- 1684452
- 1685752
- 1687196
- 1687204
- 5869252
- 5897584
- 5897596
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4023-4170
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-63: `REFERENCES/CHEATS/drop.txt` の「host drop」— `drop.cpp` にない 6 行

confidence: **HIGH**（静的解析。素の命令・分岐先・Vapecord の表・ID 一覧が整合）

### 結論

`drop.txt` の `[host drop]` は **`drop.cpp` の 10 行（F-61 の通信層）+ 6 行の追加**。
追加分は通信ではなく **持ち物メニューの可否判定を外す**もの。

**★2 層構成。**「ホストとして自分で実行する」(F-61) だけでは足りず、
そもそも**メニューに「おく」「うめる」が出ない**ので、UI 側のゲートも外している。

なお `drop.txt` 側は `DROPM` が `0x59E5DC`（JPN）で、
`drop.cpp` の `USA0x0059FCA4` と違い**全行が日本語版アドレス**。

### 1. 追加 6 行

| addr | 素の値 | 場所 | 効果 |
|---|---|---|---|
| `0x7238C0` | `0A000001` | `Inventory_GetSlot` | 常に実スロットを返す |
| `0x19B604` | `0A00000C` | `ItemMenu_UpdateActionFlags` | 可否フラグ `v13` を常に 1 |
| `0x19B8F0` | `E3500000` | `ItemMenu_Build` | `Item_CanPlant` の **CMP を潰す** |
| `0x19B9D8` | `1A000012` | `ItemMenu_Build` | カテゴリ限定を外す |
| `0x19BE8C` | `0A000011` | `ItemMenu_Build` | `sub_767930` を飛ばす |
| `0x19BFB0` | `0A000017` | `ItemMenu_Build` | `Item_CanPlaceHere` を飛ばす |

全部 `E1A00000`（NOP）に置換。**6 行中 5 行は分岐潰し、1 行だけ比較潰し**。

### 2. 新しく特定した関数

| addr | 名前 | 根拠 |
|---|---|---|
| `0x723878` | `Inventory_GetSlot` | `vc_GET_ITEM`(`0x723854`) が `sub_2FB900() + 27600` を渡す。16 枠 |
| `0x26FD6C` | `Item_CanPlant` | Vapecord `PLANT2`。`!IsEmpty && sub_5B3CD4() && sub_76BD4C(item)` |
| `0x26FDA8` | `Item_CanPlaceHere` | Vapecord `DROP2`。部屋フラグ 8/4 と `sub_769FB4(item)` |
| `0x19B7B0` | `ItemMenu_Build` | 判定ごとに `MOV R0,#ID / MOV R2,#種別 / BL sub_5E284C` を並べる (MEDIUM) |
| `0x19B3E4` | `ItemMenu_UpdateActionFlags` | 3 つの可否を `+24256` の `+125/+429/+733` に書く (MEDIUM) |

### 3. ★`sub_598EC4` の正体が判明（TODO-15 解決）

`0x19BE8C` を NOP にした直後の飛び先が `BL sub_598EC4` だった。中身は:

```
持ち物の vc_GETCATEGORIE != 17 なら 0
向き判定・探索順テーブルは Drop_FindTargetTile と同じ
★ただし v11 = 1 から v11 < 4 まで = 足元を除いた隣接 3 マスだけ
Field_GetItemAtXY のマスが Item_IsId(item, 158) であること
FieldAction_FindActive == -1（未ロック）かつ到達判定
```

**`158` = `0x9E` = `Hole`（穴）** — `REFERENCES/IDS/.../All_ACNL_Items.txt` で確認。
よって **`Drop_FindAdjacentHole` = 「隣接する穴を探す」判定**で、
持ち物メニューに「うめる」を出すかどうかを決めている。

**★F-62 との衝突:** 「ドロップ15x15」は `g_DropOffsetTable` を 225 エントリ化するが、
`Drop_FindAdjacentHole` は `+9` 前提のまま。**両方を同時に当てると壊れる。**

### 4. ★`0x19B8F0` は「持ち物が空のとき」にしか効かない

6 行で唯一、分岐ではなく **`CMP R0,#0` を潰している**。
後続 `BEQ`(`0x19B8F8`) は `Item_CanPlant` 内の**残留フラグ**を使うことになる。
終了経路ごとに追うと:

| `Item_CanPlant` の終了経路 | 戻り値 | 残留 Z | CMP を消すと |
|---|---|---|---|
| `Item_IsEmpty` 成立 | 0 | **Z=0** | **本来飛ぶはずが通る（挙動が変わる）** |
| `sub_5B3CD4() == 0` | 0 | Z=1 | 元と同じ |
| `sub_76BD4C` 経由 | 0/1 | 戻り値と一致 | 元と同じ |

**3 経路中 2 経路では残留フラグが偶然 CMP の結果と一致するため何も変わらない。**
実質「持ち物が空のスロットでも植える系の項目を出す」だけの行。

CLAUDE.md の「1 チートの全行が必要とは限らない」（F-49）の実例。

### 5. 効いていない可能性がある点

`0x19BE8C` を外しても、その先の `BEQ`(`0x19BE9C`-`0x19BEA4`) は**パッチされていない**ので、
`Drop_FindAdjacentHole` 自体は依然としてゲートのまま。
つまり「隣に穴が無ければ項目は出ない」は維持される。

### 6. IDA へ反映済み

`0x598EC4` `0x723878` `0x26FD6C` `0x26FDA8` `0x19B7B0` `0x19B3E4` をリネームし、
追加 6 行すべてに素の値つきコメントを入れた。

### 7. 未確認

- 実機未検証（静的解析のみ）
- `sub_5E284C` がメニュー項目追加であることは状況証拠（MEDIUM）
- `sub_767930` / `sub_769FB4` / `sub_5B3CD4` / `sub_76BD4C` の中身は未調査

### F-63 追記: 実ゲームへの影響（静的解析からの推論）

**★実機未検証。以下は分岐構造から導いた推論。**

#### オフライン（1 人）では 16 行中 9 行が不発

通信層 9 行（HOST1-9）は**すべて `Net_IsMultiplayer()` の分岐の内側**にあり、
その分岐自体はパッチされない。逆アセンブルで確認:

```
0x59FD70  BL Net_IsMultiplayer
0x59FD7C  BEQ loc_59FE44        ← パッチされない。オフラインはここで抜ける
0x59FD80  BL Net_IsHost
0x59FD8C  BEQ loc_59FE44        ← HOST1。ここを NOP
```

HOST3/4/5/6/7/8/9 も同じ形（`Net_IsMultiplayer` の分岐が手前にある）。
**オフラインでは元から自前実行なので、これらは何も変えない。**

したがってオフラインで効くのは:

- **`DROPM`(`0x59E5DC`)** — 待ち行列 4 枠を無視して常にスロット 0
- **UI 6 行** — 本来出ない「おく」「うめる」がメニューに出る

#### メモリ安全性は保たれる

`Inventory_GetSlot` の**範囲チェックは別分岐**でパッチ対象外:

```
0x723888  CMP R1, #0x10
0x723890  BCS loc_7238CC     ← 範囲外はここで弾かれる。パッチされない
0x7238C0  BEQ loc_7238CC     ← パッチ対象はこちらだけ
```

添字 16 以上は従来どおり `&ItemToPlace` が返る。**OOB にはならない。**
パッチが効くのは「添字は正当だが `Item_IsEmpty || sub_768FFC` に落ちるスロット」だけ。

#### 想定される不具合

| 由来 | 想定される症状 |
|---|---|
| `DROPM` のスロット 0 上書き | 処理中のレコードを潰す。演出が途中で消える、置いたはずのものが出ない。F-42 で実際にキュー詰まりを経験している |
| UI ゲート外し | メニューには出るが実処理側の判定は残るので「選んでも何も起きない」が多いはず |
| HOST3/4/7/8/9（配置を送らない） | 自分の画面にだけ出て**他プレイヤーには見えない**。デシンク |
| HOST1/2（ロックだけ同報） | 他人の `g_FieldActionActive`(32 枠) を消費させる。アイテム本体は送られないので、他人からは「一瞬ロックされて何も起きないマス」 |
| ホスト偽装 | 本物のホストと権限が二重になる。同じマスへの操作が競合しうる |

**★用途はオンラインで他人の村に自由に物を置くこと**と考えられる。
オフラインで使っても `DROPM` と UI 以外の意味はない。

#### 併用の注意

「ドロップ15x15」(F-62) と同時に当てると `Drop_FindAdjacentHole` が壊れる。
`host drop` の `0x19BE8C` はその関数へ**わざと進ませる**パッチなので、相性が悪い。

---

