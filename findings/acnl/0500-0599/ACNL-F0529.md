---
id: ACNL-F0529
aliases:
- IDA-opus-5.5-F001
title: 公共事業は ID → 名前 1 つでモデルと足元が引ける。設置関数は見た目を作らない（2026-09-23、静的）
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。（旧表記 `IDA-opus-5-F039`、次の TODO は `IDA-opus-5-T026`〜`T028`。担当モデルを取り違えていたのを 2026-09-23 に訂正。番号は再利用しない）'
date: '2026-09-23'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2368984
- 2368756
- 5401620
- 5401100
- 6064964
- 9787136
- 1775392
- 7118432
- 11262484
- 11267648
- 11283564
- 11311768
- 11317232
- 4833420
tags:
- building
- model
supersedes: []
source: IDA:work/FINDINGS.md:3049-3117
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F001: 公共事業は ID → 名前 1 つでモデルと足元が引ける。設置関数は見た目を作らない（2026-09-23、静的）

解析ソフト: IDA / 解析モデル: opus-5.5。（旧表記 `IDA-opus-5-F039`、次の TODO は `IDA-opus-5-T026`〜`T028`。担当モデルを取り違えていたのを 2026-09-23 に訂正。番号は再利用しない）

利用者の依頼「公共事業設置のプレビュー（半透明モデル＋当たり判定を UnitCursor で囲む）」
のための前提調査。実機は使っていない。

### 1. 設置関数がやっていること（HIGH、静的＋Vapecord の呼び出し方と一致）

Vapecord `Building.cpp` の `PlaceBuildingUpdateCollisions` = `Address(0x2425D8)`（USA）。
`Addresses.hpp` の JPN 列は **`0x2424F4`**。IDB の `vc_PLACEBUILDING` と一致。中身:

1. `Structure_StampFootprint 0x526C14({x,y}, id, 1, 1)` — 足元のフィールド属性を書き、アイテムを消す
2. `sub_5CCE4C(TownBase + 310784, id, x, y)` — セーブの建物表へ登録、スロットを返す
3. `Building_WriteOccupancy 0x526A0C(1, x, y, id, slot)` — 占有レイヤへスロット番号を書く

**見た目の実体（3D モデル）を作る処理は含まない。** だから Vapecord はこのあと
`Game::ReloadRoom` で部屋を読み直している。利用者の言う「設置しても画面遷移しないと見えない」
はこの形からそのまま説明できる。属性と占有は書かれるので、**当たり判定は即時に付く可能性が高い**
（実機未確認）。残るのは「見た目を即時に作る」側。

### 2. ID → 名前 → モデル・足元（HIGH）

`Building_GetName 0x5C8B44`: `id < 0xFC` なら `*(0x955700 + 4*id)`。基点と刻み幅はこの添字計算から確定。
`0xFC` は空き（Vapecord `kEmptyBuildingId` と一致）。名前が決まれば:

- モデル `Strc/{fobj,sobj,dobj}/<名>/<名>.bcres`（code.bin の書式文字列）
- 足元 `Strc/data/<名>.bin`

**公共事業は `fobj_*`**（ID 0x90〜0xFB、108 件。ベンチ・噴水・街灯・橋など）。
`sobj_*` は交番・駅・看板など、`dobj_*` は店。
**108 件すべてでモデルと足元が存在することを生の RomFS で確認**（`tools/strc/catalog_buildings.py`）。

### 3. 足元データの形（HIGH、コードとデータの両方から）

`Strc/data/*.bin` は**すべて 2,560 B = 16×16 マス × 10 B**。
コード側（`Structure_StampFootprint` / `Building_WriteOccupancy`）の添字が「1 行 160 B・1 マス 10 B」で一致。

- **基点は (行 7, 列 7) = 建物の (x, y)**。列 = x、行 = y。
  実例: `sobj_plan_fence_2x1` は (7,7)(7,8) — +x へ伸びる。`1x2` は (6,7)(7,7) — −y へ伸びる。
- **byte 8 = そのマスへ書くフィールド属性コード**。単純な「当たり／余白」ではない:
  柵は 0x02（本体）＋ 0x31（周囲 1 マス）、街灯は 0x04（中心）＋ 0x05、
  橋は 0x17/0x18/0x33/0xA0、花壇は 0x31/0xAB。全建物で 43 種類の値が出る。
- byte 9 は全マス 0x40、byte 0–7 は柵のつながりらしき値（未解明）。

**ゲームが実際に書くのは byte 8 が非 0 のマス**（`Building_WriteOccupancy` は 0 と 0xA1 だけ飛ばす）。
プレビューで囲む範囲はこの「書き込まれるマス」とするのが正確。
例: ベンチ 4×3（12 マス）、街灯 3×3、噴水 5×5、ピラミッド 5×5、橋 6×4。
**どの属性コードが通行不可かはゲームの属性表で決まるので、まだ決めていない（IDA-opus-5.5-T003）。**

### 4. 足元の出どころ

`Building_GetFootprint 0x1B1720(x, y, id)` → `Building_GetFootprintByCategory 0x6C9E60(id)` が建物の種類で分岐し、
`ldr r0, =<.bss の資源オブジェクト>; b <共通の取得>` の形の関数群へ落ちる
（`0xABDA14` / `0xABEE40` / `0xAC2C6C` / `0xAC9A98` / `0xACAFF0` など）。つまり実行時に romfs から読んだもの。
建設中の予定地（`garden+451236..451251`）に一致するときだけ別のテンプレートを返す。

### 5. 既にある部品

- **半透明**: IDA-gpt-6-astra-F002（実機成功、HIGH）。instance 専用に材質を複製し、
  Activate を汎用 `0x49C08C` へ差し替えて constant alpha。gohan には未移植。
- **任意モデルの表示**: モデルビューア（F035〜F038、一覧作成まで実機確認）。
- **マスの敷き詰め**: グリッドカーソル（F032〜F034、実機完成）。1 マス = world 32、マス中心へ丸める。

根拠: `acnl_jpn_v15_annotated.i64` の `0x2424F4` / `0x526C14` / `0x526A0C` / `0x1B1720` / `0x6C9E60` / `0x5C8B44`、
Vapecord `src/core/game_api/Building.cpp` と `include/core/infrastructure/Addresses.hpp` の PLACEBUILDING / D_GARDEN 行、
`tools/strc/romfs_read.py`、`tools/strc/catalog_buildings.py`（`work/evidence/strc/building_catalog.json`）。
反証条件: 実機で設置直後に当たり判定が付かない、足元の基点が (7,7) でない建物がある。

