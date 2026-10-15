---
id: ACNL-F0459
aliases:
- IDA-opus-5.5-F002
title: 消した・動かした建物の当たり判定が残る理由と、再起動なしで直す 2 関数（2026-09-23、HIGH（静的））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の実機検証:「Vapecord で設置した建物には当たり判定があった。'
date: '2026-09-23'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2375848
- 2369656
- 2368012
- 9789324
- 2369860
- 3125064
- 6082124
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1281-1335
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F002: 消した・動かした建物の当たり判定が残る理由と、再起動なしで直す 2 関数（2026-09-23、HIGH（静的））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の実機検証:「Vapecord で設置した建物には当たり判定があった。
元々ある建物を削除したり自分の位置へ移動させた場合は衝突判定の更新にゲームの再起動が必要」。

### 1. なぜ残るか

- Vapecord の消す・動かすは**セーブの建物表だけ**を書き換えて部屋を読み直す。
- 当たり判定は区画ごとの**属性ブロック**（16x16 マス x 10 B = 2,560 B、建物の足元データと同じ形）に
  書かれている。建物の足元を押す処理（`Structure_StampFootprint`）は**足すだけ**で、
  消えた建物の属性を地形へ戻す処理は部屋の読み直しでは走らない。
- 建物の「実行時リスト」に見えた `dword_AB1DF4` / `AB1DF8` は `VillageBook` / `EventBook` クラスで、
  コンストラクタは vtable を置くだけ（`Building_CreateManagers 0x2440A8`）。**状態を持たない窓**なので、
  押し直せば毎回セーブの表をそのまま読む。古いのは属性と占有の側だけ。

### 2. 直す関数（どちらも引数なし）

| 関数 | 中身 | ゲーム自身の使用 |
|---|---|---|
| **`Field_RebuildAttributes 0x242878`** | 村の 6x7 区画それぞれへ**区画本来の地形属性を 2,560 B 複写**して素に戻し、砂浜・川べりの値を補正、最後に `Structure_StampAll(0,0)` | code.bin からは 0 件。**`ModuleIndoor.cro` と `ModulePrologue.cro` がインポートして呼ぶ** |
| **`Building_RebuildOccupancy 0x24220C`** | 占有マップ 4 層を消してから VillageBook / EventBook / AB1E00 の全建物を書き直す | code.bin の **15 か所**が呼ぶ常用処理 |

`Field_RebuildAttributes` の中身は全部フィールドのデータ書き換え（区画の復元 `sub_6A889C(…, 2560)`、
砂浜・川べりの属性値 20/22 → 50/128 の補正 `sub_6F9250`、灯台などの位置計算 `sub_6A64F8`、押し直し）で、
資源の読み込みや描画には触らない。

`ModuleIndoor` が使うのは、家の増築で家の足元が変わったときと推定（未確認）。
**「建物の足元が変わったときに当たり判定を作り直す」という今回の用途そのもの。**

### 3. gohan への実装（実機未確認）

`Sources/Cheats/PublicWorks.cpp`。表を書き換えたあと、描画スレッドで
`Field_RebuildAttributes` → `Building_RebuildOccupancy` → 部屋の読み直し（Vapecord と同じ引数）。
表の位置はコードで裏を取った: `Save_GetTownBase` = `[0x955F8C] + 0x80`、設置関数は `TownBase + 0x4BE00` を
`sub_5CCE4C` へ渡し、それが `+8` から 4 B x 56 を走査し `+4` の数を増やす — Vapecord の `ACNL_BuildingData`（garden + 0x4BE80）と一致。
**消す・動かすは公共事業（0x90〜0xFB）だけ**。役場や店を誤って消さないため。
マイデザインの看板・顔出し看板（0xDC / 0xDD）は看板表も要るので今回は断る。
`tools/strc/verify_publicworks.py` が焎き込んだ 11 関数すべてを「ゲームが呼んでいる（BL か CRO インポート）」
「関数の入口として解読できる」で検査（27/27 PASS）。

根拠: `acnl_jpn_v15_annotated.i64` の `0x242878` / `0x24220C` / `0x242944` / `0x2440A8` / `0x2FAF48` / `0x5CCE4C`、
CRO インポートの走査（`segOff = 0x01428780`）、Vapecord `GameStructs.hpp` の `ACNL_BuildingData`。
反証条件: 実機で消した建物の場所にまだぶつかる、区画の「本来の属性」が別の変更（道や橋）を消してしまう。

### 4. 実機の結果（2026-09-23、利用者。**これで HIGH＝静的＋実機**）

1. 消した場所を**歩いて通れるようになった**
2. 動かした場合、**古い場所は通れ、新しい場所でぶつかる**
3. 置かれているアイテムなどは消えずに残っている

さらに利用者の観察: **当たり判定は設置・移動・削除の直後に更新されており、部屋の読み直しで変わるのは
公共事業の描画だけ**。読み直しは見た目のためだけに要る（見た目を即時に出せれば不要。IDA-opus-5.5-T001）。
このあと利用者の指示で対象を公共事業だけから**全建物**へ広げた（役場・店・家も。
マイデザインの看板 0xDC/0xDD は Vapecord と同じく看板表 garden+0x4BF70（0x878 B × 8）も書き換える）。

