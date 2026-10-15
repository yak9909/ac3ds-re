---
id: ACNL-F0505
aliases:
- IDA-opus-5.5-F026
title: '橋のカーソルの高さの出どころ（川の判定・ゲームの橋の置き方・岸の高さ）（2026-09-24、HIGH（川の判定: 静的＋実機の地形）／MEDIUM（岸＝最寄りの陸）。gohan へは未実装）'
summary: '**背景**: F025（足元の四角の地面の最大）は、四角が全部川の中だと川底の高さになり、カーソルとカメラが上下した（利用者の実機確認）。'
date: '2026-09-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7100768
- 7720388
- 6083568
- 6083908
- 7202508
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2320-2337
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F026: 橋のカーソルの高さの出どころ（川の判定・ゲームの橋の置き方・岸の高さ）（2026-09-24、HIGH（川の判定: 静的＋実機の地形）／MEDIUM（岸＝最寄りの陸）。gohan へは未実装）

- **背景**: F025（足元の四角の地面の最大）は、四角が全部川の中だと川底の高さになり、カーソルとカメラが上下した（利用者の実機確認）。
  利用者の実機の Suspend 状態（カーソル (79,36)、配置モード、橋 w_e、高さの四角 x77-82 y34-37）での高さは 112。
  gohan 変数の読み取り: `work/evidence/strc/bridge_height.json`（`tools/strc/probe_bridge_height.py`。3gx と gohan.elf の .text 8 語一致）。
- **地面の高さの算法（静的、逆アセンブル）**: `sub_6A8C80` = 平らの印（マス +9 bit6、`sub_75D044`）なら 1 隅目、でなければ 4 隅の最大。
  隅 = u16 の下位 5 ビット x 8。区画 = `*(room+36) + 2588*(ax + ay*幅)`（`sub_7520D8`、room = `dword_9AEA04[0]`、幅 = room[2]-room[0]+1 = 7）。
- **地形の実測**（`tools/strc/probe_terrain_tiles.py`、`work/evidence/strc/terrain_tiles_x74-86_y30-42.json` / `terrain_tiles_x50-62_y52-62.json`）:
  陸 14（=112）、川底 10（=80）、川は平ら。岸の角の斜めのマスは平らでなく 14。
- **川の判定（ゲームの関数）**: `Field_TileHasWaterAt 0x6C5960`（旧 sub_6C5960）= 属性コード（`FieldTile_GetAttr 0x75CDC4` = マス +8）を
  `FieldAttr_SplitParts 0x5CD3F0`（unk_956748 + 8*code）で 4 部分に分け、[0] か [2] が `FieldAttr_WaterKind 0x5CD544`（byte_957936）!= 0。
  code.bin の表で計算した水のマスが、実機の 2 か所の地形で川の範囲と一致（岸の角の斜めのマスも水になる）。
- **ゲームの橋の置き方**: `BsStrcMgr_SpawnStructures` 0x6DE6CC = 基点の地面 + 32.0（flt_6DE560）。実物の橋 y=112 = 川底 80 + 32。
  ただし**読み込み後の地形は橋の足元で書き換わっている**（床 16=128、端 15=120）。置いた時点では川底を読んでいた。
- **岸の高さの候補（数値を持たないもの）**: 基点が水でなければその地面、水なら**最寄りの水でないマスの地面**。2 か所の川で両岸とも 14（=112）で、
  実物の橋の y とも一致。ゲームの +32 は、基点が川底（水・平ら）のときだけ正しい（陸では 1 マス高い）。
- 反証条件: 海・滝・河口・崖の段の境にある川で、最寄りの陸の高さが岸の高さと違う例。すでに橋がある場所（地形が床の高さ）。

