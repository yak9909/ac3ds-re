---
id: ACNL-F0513
aliases:
- IDA-opus-5.5-F018
title: 親ヒープ *(0x94CC48) の空きは 484 KB。UnitCursor とプレビューを並べると足りない／駅・役場のプレビュー名（2026-09-24、HIGH（実機の読み取り）／MEDIUM（名前、静的））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「切り替えが重い・UnitCursor がすぐ消えた・無限ロードするモデルがある」、実機 Suspend 中に gohan の変数を読んだ。'
date: '2026-09-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9751624
- 9751656
- 9789324
- 3126100
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:2458-2472
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F018: 親ヒープ *(0x94CC48) の空きは 484 KB。UnitCursor とプレビューを並べると足りない／駅・役場のプレビュー名（2026-09-24、HIGH（実機の読み取り）／MEDIUM（名前、静的））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「切り替えが重い・UnitCursor がすぐ消えた・無限ロードするモデルがある」、実機 Suspend 中に gohan の変数を読んだ。

- 親ヒープ `*(0x94CC48)`（sead::ExpHeap、15,433,728 B）: **空き 484,520 B（3 塊、最大 463,772 B）**。建物用の親 `*(0x94CC68)` は 607,948 B（1 塊）
- 当時の gohan: UnitCursor 40 体（8x5）× 8 KB＋予備＋資源 32 KB ≒ 376 KB、プレビュー（駅）≒ 243 KB → 合わせると空きを超える
- グリッドカーソルは `Failed / kNotInVillage` で止まっていた（部屋 id は 0、シーンの所有者も有効）。組み直しの AllocHeaps で一瞬の条件落ちに当たったと推定（LOW）
- 無限ロードに見えた種類は 0x54 `sobj_stationA`: `Strc/sobj/sobj_stationA/Textures/season00/season00.bcres` が無い（大きさ 0 → プレビュー無し）。
  `PwpPreview_LoadSlot` は役場 0x50 を `sobj_officeA%02d`（番号 = 庭 +401848 の u16 & 3、sub_6CA35C）、駅 0x54 を `sobj_stationA%02d`（ビット 8〜9、sub_6CA378）、
  0x4F を `sobj_reset_cls` で読む。庭 = `*(0x955F8C)`（vc_D_GARDEN 0x2FB354 がそのまま返す）
- 切り替えが重かったのは gohan の RomfsIndex::ReadFile が 1 回ごとに更新タイトル（媒体 3 通り）と base を開き直していたため

対策（gohan `84f7047`）: UnitCursor 6 KB/体・初期 24 体、プレビューのインスタンス 32 KB、**どちらも親ヒープに 128 KB を残せないときは作らない**、
アーカイブを開いたまま使い回す、駅・役場・0x4F の名前、止まった UnitCursor の通知と組み直し。

