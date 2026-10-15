---
id: ACNL-F0515
aliases:
- IDA-opus-5.5-F016
title: 設置プレビューはゲーム自身の公共事業プレビューと同じ 3 資源で組める／衝突判定の「一回り小さい」形（2026-09-23、MEDIUM（静的。実機未確認））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の指示「配置モードでプレビューが表示されていない」「衝突判定のサイズは一回り小さい方（ベンチ 4x3 ではなく 2x1）」。'
date: '2026-09-23'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2260220
- 2258356
- 2258392
- 3242328
- 7104960
tags:
- building
supersedes: []
source: IDA:work/FINDINGS.md:2491-2505
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F016: 設置プレビューはゲーム自身の公共事業プレビューと同じ 3 資源で組める／衝突判定の「一回り小さい」形（2026-09-23、MEDIUM（静的。実機未確認））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の指示「配置モードでプレビューが表示されていない」「衝突判定のサイズは一回り小さい方（ベンチ 4x3 ではなく 2x1）」。

- 建物のモデル `Strc/{fobj,sobj}/<名>/<名>.bcres` は**テクスチャを持たない**（例: fobj_bench_log のモデル 7,224 B、テクスチャ `Textures/season00.bcres` 21,888 B は別ファイル）
- `PwpPreview_LoadSlot 0x227CFC`（F003）の組み立て: モデル holder・テクスチャ holder（season00 固定）・LUT holder（fobj は `Strc/fobj/lut/Lut_fieldobj.bcres`、sobj は `Strc/sobj/lut/Lut_sobj.bcres` と推定。
  文字列はこの関数の直前 0x2275B4/0x2275D8）を読み、`G3dResHolder_Setup(モデル, ヒープ, 0, 1)` → `(モデル, ヒープ, LUT, 1)` → `(テクスチャ, ヒープ, 0, 1)` → `(モデル, ヒープ, テクスチャ, 1)`。
  `G3dResHolder_Setup 0x317958` の第 3 引数は別の holder（その +8 の資源で参照を解決する = ResGraphicsFile::Setup(allocator, other)）
- gohan `BuildingPreview` はこの順をそのまま使い、mask 0x834（汎用の書き出し関数・材質本体はインスタンスごとの写し）で 1 体作り、写しのフラグメント設定を定数アルファのブレンドにする。
  資源が揃うのは fobj 全部と sobj の大半（154 種。欠け: sobj_officeA/stationA/BBS_CD/hnw_rent/RVcar00/01）
- 高さは実際の生成と同じ `PublicWorks::SpawnHeight`（地面 0x6C69C0、橋は +32）に一本化
- 衝突判定の形: 足元データの「属性を書くマス」の**外接の四角を上下左右 1 マスずつ縮めた内側**（縮めて残らなければそのまま）。
  ベンチ 4x3→2x1、街灯 3x3→1x1、噴水 5x5→3x3、南北の橋 4x6→橋板 2x4（`verify_building_editor.py` で照合）。
  属性コードで決める方法（0x05 = 周囲など）は通行可否の表（T003）が未解明なので採らなかった

