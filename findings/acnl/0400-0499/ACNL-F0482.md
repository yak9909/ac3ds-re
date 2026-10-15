---
id: ACNL-F0482
aliases:
- IDA-opus-5.5-F051
title: '村のマスにアイテムを置く・消す手順（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 2 は実機未確認）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。マップエディター（gohan Issue #16）の配置・削除モードのため。'
date: '2026-09-27'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7317544
- 9789428
- 9735772
- 5888636
- 3131728
- 5891508
tags:
- map
supersedes: []
source: IDA:work/FINDINGS.md:1864-1877
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F051: 村のマスにアイテムを置く・消す手順（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 2 は実機未確認）

解析ソフト: IDA / 解析モデル: opus-5.5。マップエディター（gohan Issue #16）の配置・削除モードのため。

- 消す = **Field_DeleteItemAt 0x6FA828(x, y, 部屋データ)**。空でなければ、分類 122 なら別の記録（sub_5B9434）、ほかは TownBase+401762 へ記録（sub_1B262C）、
  `Field_SetItemAtWorldXY(部屋データ, &ItemToPlace 0x955FF4, x, y, 0)` で空を書き、fgobj（`sub_59CEC0` = `*(0x948E5C + 0x14)` = off_948E70 が非 0）なら
  **Field_MarkDirty 0x59DA7C(x, y, 1)** へ末尾分岐（IDA-opus-5.5-F005）。ItemToPlace はファイル上 0（実行時に空アイテムが入ると推定、LOW）。
- 書く = **Field_SetItemAtWorldXY 0x2FC950(部屋データ, &item, x, y, 0)**: マス → エーカー（sub_6A6468、x>>4）→ 範囲検査 sub_747728（部屋データ +0..+C）→
  エーカーの枠 +32 + 12 × (ax + ay × 幅) → sub_57B100 がデバッグ入出力中・プレイヤーの通信状態（sub_606CB0 x 4）を見てから Item_Copy。成功で 1。
- gohan の置き方は消し方と同じ形（書いてから fgobj があれば Field_MarkDirty）。通信の同期はしない（ROTATION の PlaceItem 0x59E5B4 系とは違う）。
- 長押しの閾値: ゲームのチップ Select 状態（CRO 0xB429BC）のリテラル 0x41C00000 = 24.0（F050 と同じ）。

反証条件: 置いたアイテムが上画面に出ない・高さがおかしい（MarkDirty では足りない）、消したアイテムの記録が翌日に悪さをする。

