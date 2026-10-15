---
id: ACNL-F0486
aliases:
- IDA-opus-5.5-F047
title: '持ち物へアイテムを入れるゲーム自身の処理と、持ち物画面のアイコンの作り直し（2026-09-26、MEDIUM: 静的＋実機実績のある外部実装と独立一致。gohan の実装は実機未確認）'
summary: ポケットアイテム（gohan.md §17.5）の下調べ。資料の ID 一覧に頼らず、ゲーム自身の処理を使う（2026-09-17 の利用者判断）。
date: '2026-09-26'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2882772
- 3285932
- 3286156
- 7050648
- 6613220
- 7484932
- 3127552
- 11178316
- 3132340
- 8947964
- 2546460
- 1704468
- 9987328
- 7150712
- 9327136
- 1798684
tags:
- inventory
supersedes: []
source: IDA:work/FINDINGS.md:1953-1972
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F047: 持ち物へアイテムを入れるゲーム自身の処理と、持ち物画面のアイコンの作り直し（2026-09-26、MEDIUM: 静的＋実機実績のある外部実装と独立一致。gohan の実装は実機未確認）

ポケットアイテム（gohan.md §17.5）の下調べ。資料の ID 一覧に頼らず、ゲーム自身の処理を使う（2026-09-17 の利用者判断）。

- **`Inventory_AddItem 0x2BFCD4`**(持ち物, &アイテム, 印, 図鑑登録): `Inventory_AddToFirstEmpty 0x3223AC` → 16 枠を 0 から見て最初の空き（`Item_IsEmpty`、
  または中身が「持てない」もの）へ `Inventory_WriteSlotChecked 0x32248C`。書く前に `Item_NormalizeForPocket 0x6B9598`（特殊 ID の写像のあと
  `ItemParam_GetRecord` の記録 +1 bit 0x10 が要る。空 0x7FFE も通す）が偽なら書かずに 0。書いたら 持ち物+64+枠 = 印（記録 +2 bit7 なら 2）。
  図鑑登録が真なら `sub_6EEA70`(持ち物+80, …)。今のプレイヤーの持ち物なら条件付きで `sub_24B920`(save+8888, 32, 1)。
  呼び元 24 か所。プレイヤーが拾うとき: `sub_6554B8` → `vc_WRITEITEM 0x64E8E4`(player, &item) → ここ（図鑑登録 = 特定の部屋の特定の分類でなければ 1）。
- `Inventory_FindEmptySlot 0x723604`: 上と同じ判定で最初の空き枠（無ければ −1）。`Save_GetCurrentPlayer 0x2FB900`: `*0xAA914C`（セーブの読み書き中は null）。
  持ち物 = プレイヤー + 27600（0x6BD0、16 x 4 B。旧 F-63 の `sub_2FB900()+27600` と一致）。`Item_InitWithId 0x2FCBB4` の追加初期化（表 0x8888FC の 2 本）は +2 の u16 だけを書く。
- **アイコン**: `vc_LOADICON 0x26DB1C`(格子, 枠) が今のプレイヤーの持ち物の枠からアイコンを作り直す（空なら消す）。持ち物画面の中では格子 = BsMenuItem + 7872（0x1EC0）:
  (1) `BsMenuItem_Ctor 0x1A0214` が `sub_270110(this+7872)` で作る (2) ゲームは枠を書いたあと `vc_LOADICON(this+7872, 枠)`（`sub_199550` / `sub_199AFC` など）
  (3) Vapecord の実機で動いているコード（`Inventory::ReloadIcons`: `*(InvMenu+0xC) + 0x1EC0`、メニュー番号 0 のとき）と独立に一致。
  下画面の画面 = `*(*(0x986500) + 0xC)`（`Menu_GetScreenMenuId 0x6D1C78` が +0x24 をメニュー番号として読む）。
- gohan の実装（gohan f43f2bc）: `Inventory_AddItem(持ち物, &item, 0, 0)`、画面の vtable が `BsMenuItem`(0x8E5220) で番号 0 のときだけ `vc_LOADICON`。
  ゲームのスレッド（`0x1B721C` のフレームフック）から。成果物の逆アセンブルで引数・オフセット・リテラルを確認。
- 反証条件: 実機で入らない・別の枠に入る・持てない物が入る・持ち物画面のアイコンが変わらない／乱れる・落ちる。
- IDB: 上の 7 関数を命名、4 か所に注記。

