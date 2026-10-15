---
id: ACNL-F0094
aliases:
- F-56
title: F-56 `ACNL_ID_Lists-master` との照合 — 4 件確定・1 件は資料側が誤り — `HIGH`
summary: Vapecord 作者による ID 一覧 `REFERENCES/IDS/ACNL_ID_Lists-master` と、
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8925992
- 8781744
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:3222-3314
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-56 `ACNL_ID_Lists-master` との照合 — 4 件確定・1 件は資料側が誤り — `HIGH`

Vapecord 作者による ID 一覧 `REFERENCES/IDS/ACNL_ID_Lists-master` と、
本解析で扱ってきたテーブルを突き合わせた。

### アイテム ID — 全部一致し、推定が 1 件確定した

`All_ACNL_Items.txt` は `7FFE Empty` から始まる（= `g_EmptyItem`）。

| ID | 資料 | 本解析での扱い |
|---|---|---|
| `0x0014` | **cedar stump** | 切り株 ✓ |
| `0x0021` | **cut bamboo (growing 3)** | 切断竹 ✓ |
| `0x002B` | **cedar** | 「木」→ **正確には杉** |
| `0x0039` | **bamboo** | ユーザーがぶつかった木 = 竹 ✓ |
| `0x009E` | **Hole** | 「ID158 は穴と**推定**」(F-28) → **確定** |
| `0x00B2` | **red roses** | 「赤いバラの見た目」(F-40) ✓ |
| `0x00FA` | **broken red flower** | 「同じ見た目の未使用アイテム」✓ |

### F-47 のカテゴリが全部「花の種類」だった

| cat | ID 範囲 | 実名 |
|---|---|---|
| 11 | `0x9F`-`0xA5` (7) | チューリップ |
| 12 | `0xA6`-`0xAB` (6) | パンジー |
| 13 | `0xAC`-`0xB1` (6) | コスモス |
| 14 | `0xB2`-`0xB9` (8) | **バラ**（`0xB2` = red roses） |
| 15 | `0xBA` (1) | 金のバラ |
| 16 | `0xBB`-`0xBD` (3) | カーネーション |
| 27 | `0xBE`-`0xC3` (6) | ユリ |
| 28 | `0xC4`-`0xC7` (4) | スミレ |
| 17 | `0xC8` (1) | ジェイコブスラダー |
| 20 | `0xCA`-`0xCB` (2) | タンポポ / 綿毛 |
| 19 | `0xCE`-`0xF7` (42) | **枯れた花** |

**対象外なのは `0xC9` 四つ葉のクローバー / `0xCC` 雑草 / `0xCD` ラフレシア。**
つまり「走って踏むと壊れるのは花だけで、雑草や四つ葉は壊れない」。
`Item_IsFlowerCategory` という命名が結果的に正しかった。

`FieldObj_PlayPlantEffect` の範囲 `ID - 159 < 89` も、
**`0x9F`(red tulips) - `0xF7`(Jacob's ladder wilted) の 89 個**とぴったり一致する。

### 部屋フラグの bit の意味が確定した

`Room_IDS.txt` の Outdoor/Indoor 分類と `g_RoomFlagTable` (`0x883328`) を照合:

| bit | Outdoor 23 件中 | Indoor 94 件中 | 意味 |
|---|---|---|---|
| 1 | 21 | 0 | **屋外** |
| 2 | 21 | 0 | **屋外** |
| 3 | 0 | 94 | **屋内** |
| 5 | **1** | 0 | **村(Town) のみ** — 部屋 ID `0x00` ただ 1 つ |

- `FieldObj_TrampleAt` の `Room_HasFlags(4, ...)` = **屋外か**
- `FieldObj_ResolveAxeAction` の `Room_HasFlags(32, ...)` = **村か**

bit2 の無い Outdoor は Wii U 連携ミニゲーム 2 部屋だけ（`flags=0x08000000`）。

### パーティクル

`g_PlantEffectTable` の値（`0x177` `0x179` `0x17B` `0x176` `0x178` `0x172` `0x175` …）は
`Particle_IDs(1).txt` で**すべて "Flowers"** に当たる。用途と一致。

### 【重要】アニメーション ID は**資料側が誤り**

| ID | 資料 (`Animation_IDs.txt`) | ゲーム自身の名前 (`g_AnimNameTable`) |
|---|---|---|
| 71 | Player vanishes | **`scoop_swing1`** |
| 72 | Close door | **`scoop_swing_wait1`** |
| 73 | Shovel use | `scoop_dig1` |
| 74 | Shovel use | `scoop_hane1` |
| 75 | Shovel hits nothing | `scoop_suka1`（空振り）**← ここだけ一致** |
| 76 | Shovel hits something strong | `scoop_stump1` |
| 77 | Shovel hits something strong | `scoop_get1` |
| 78 | Shovel swing | `scoop_putaway1` |
| 79 | Shovel dig | `scoop_bury1` |

**本解析の値は `g_AnimNameTable` (`0x85FFB0`) をメモリから読んだもので、
ゲーム自身が持っている名前**。実機でも検証済み。**こちらが正。**

資料は実機を動かして見た目で付けたラベルなので、
`scoop_swing1` を「Player vanishes」と取り違えている。

### この資料の評価

- **アイテム ID / 部屋 ID / パーティクル ID は信頼できる**。
  本解析の推定を確定させ、カテゴリに実名を与えた
- **アニメーション ID は信頼できない**。ゲーム内の名前テーブルが正
- **「より正確な可能性が高い」は分野による。** 一次情報（ゲーム内のテーブル・文字列）が
  取れるものは常にそちらが上。資料は一次情報が取れない領域でこそ効く

---

