---
id: ACNL-F0485
aliases:
- IDA-opus-5.5-F048
title: 'ゲームの「持ち物に入れる」は 0xFD 以下の ID を写し替え、空に写しても成功を返す／没アイテムを隠す分岐（2026-09-27、MEDIUM: 静的＋利用者の実機報告と整合。修正版は実機未確認）'
summary: '利用者の実機報告（F047 の版）: ポケットアイテムで 0xFF 以下などが入らないのに「入れました」と出た。'
date: '2026-09-27'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 3286156
- 7050648
- 7048884
- 7485560
- 7485632
- 3286300
tags:
- inventory
supersedes: []
source: IDA:work/FINDINGS.md:1937-1952
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F048: ゲームの「持ち物に入れる」は 0xFD 以下の ID を写し替え、空に写しても成功を返す／没アイテムを隠す分岐（2026-09-27、MEDIUM: 静的＋利用者の実機報告と整合。修正版は実機未確認）

- 利用者の実機報告（F047 の版）: ポケットアイテムで 0xFF 以下などが入らないのに「入れました」と出た。
- 原因（静的）: `Inventory_WriteSlotChecked 0x32248C` → `Item_NormalizeForPocket 0x6B9598` → **`Item_RemapFieldIdForPocket 0x6B8EB4`**:
  ID ≤ 0xFD のとき、分類 11〜17・20・27・28 と ID 0xC9 は (ID−159)+表の基底（範囲外は 0x7FFE）、それ以外は `ItemToPlace`（空）へ写す。
  続く判定は空（0x7FFE）を通すので、空を書いて 1 を返す → 何も入らないのに成功。報告と整合する。
- `Inventory_GetSlot 0x723878`: 枠が空でなく、かつ `sub_768FFC`（ID の 0x6000 が 0x4000、または記録 +1 bit 0x10 = 持てる）が偽なら
  `ItemToPlace`（空）を返す。その分岐が **`0x7238C0` BEQ（0x0A000001）**。公開チート「没アイテムをポケットに表示する」は ここを NOP
  （`REFERENCES/CHEATS/player.txt`、Adios / ROTATION の Main.cpp も同じ 1 語）。呼び元 78 か所。
  もう 1 つの公開チート「拾った没アイテムが持ち物欄に入る」は `0x32251C` を `MOV R0,#1`（`Item_NormalizeForPocket` の結果を潰す）。
- ゲームの空き判定（`Inventory_FindEmptySlot` / `Inventory_AddToFirstEmpty`）は「持てない物が入った枠」も空とみなす → 没アイテムを上書きする。
- gohan（f390466）: ポケットアイテムは ID をそのまま、生の中身が空（`Item_IsEmpty`）の最初の枠へ書く（印 +64+枠 = 0）。アイコンは F047 の `vc_LOADICON`。
  没アイテム表示（Issue #15）= `0x7238C0` を NOP（`PatchListSetActive`）、切り替えで持ち物を開いていれば 16 枠のアイコンを作り直す。成果物の逆アセンブルで確認。
- 反証条件: 修正版で 0xFD 以下が入らない、没アイテム表示で見えない、表示中に落ちる。
- IDB: `Item_RemapFieldIdForPocket` 命名、2 か所に注記。

