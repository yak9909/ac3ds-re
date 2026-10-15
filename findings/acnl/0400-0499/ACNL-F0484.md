---
id: ACNL-F0484
aliases:
- IDA-opus-5.5-F049
title: 'アイテムの名前とアイコンの決まり方、没アイテムの割り出し（2026-09-27、MEDIUM: 静的＋ROM の実データ。Ghidra-gpt-sol-5.6-ITEM-T011 と独立一致。gohan の名前差し替えは実機未確認）'
summary: '**名前** `ItemName_ResolvePhrase 0x56D274`(phrase, &item, a3): phrase を空に（vt+28）→ 通常の ID は `STR_Item_name` の (ID&0x7FFF)−0x2000 番'
date: '2026-09-27'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5689972
- 9455956
- 9634808
- 6275908
- 2854572
- 5460240
- 8858692
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1916-1936
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F049: アイテムの名前とアイコンの決まり方、没アイテムの割り出し（2026-09-27、MEDIUM: 静的＋ROM の実データ。Ghidra-gpt-sol-5.6-ITEM-T011 と独立一致。gohan の名前差し替えは実機未確認）

- **名前** `ItemName_ResolvePhrase 0x56D274`(phrase, &item, a3): phrase を空に（vt+28）→ 通常の ID は `STR_Item_name` の (ID&0x7FFF)−0x2000 番
  （件数より小さいときだけ）、特殊な種類は別処理で組む → それでも空なら `script::WordRes {0x904954, "???"(0x9303F8), 0x3FFFFFFF}`
  （`script_WordRes_Ctor 0x5FC344`）を vt+20 で入れる。呼び元 5 か所。
- **ROM の名前表** `Script/Str/STR_Item_name.umsbt`（更新版 192,528 B / 基本版 145,696 B）: 先頭の表 {u32 0x30, u32 大きさ} の後に MSBT 1 本。
  区画は ATR1 と TXT2 だけ（LBL1 なし）、件数 5931 = 0x172B（Ghidra の記録の表の件数と一致）。名前あり 5825、空 106
  （`tools/items/dump_item_names.py`）。
- **アイコン** `ItemIconWidget_SetItem 0x2B8EAC`: `ItemParam_GetIconBaseName 0x535110`（記録 +0 の u16 → 表 0x872C44 の 507 件、記録が無ければ `icn_000`）
  + ".bclim" をアクセサ（this+304）+12 から取り、`P_itemIcon` の material の TexMap（+52）へ。取れなければ `icn_000.bclim`。
  ROM の `Layout/ItemWin/item_icon.arc`（DARC）の BCLIM は 419 枚中 416 枚が 32x32・ETC1A4（書式 11）。
- **没アイテム**（`tools/items/diff_hidden_items.py`）: 利用者の全アイテム表（`Item.h` の PDF、`inputs/hidden_items/`）5520 件のうち、ROM に名前の無いもの 332 件
  = 表より下（0x0005〜0x00FF）251 / 表の中で名前が空 76 / 表より上（ラッピングの形 0x4037 など）5。PDF の名前は漢字表記なので 2262 件で ROM と表記が違う（別物ではない）。
  PDF に無い ID が 637 件（名画 0x3109〜0x312F と 0x34CE〜0x3725。ROM には名前がある = 通常アイテム）。
  漢字名・かな名の全文字が `Font/Garden_msg_size16.bcfnt` の CMAP にある（`tools/items/export_hidden_items.py` が検査）。
- 利用者の没アイテム用 PNG 86 枚は 64x64 RGBA8。32x32 の単純な 2 倍拡大ではない。`icon_map.txt` が指す 5352・5353 の PNG は無い。
- gohan（9a40fe1）: 自前表示 = `0x56D274` を MITM でフックし、没アイテムなら表の漢字名の WordRes を入れる。名前の窓口 `ItemNames`
  （通常は ROM を実行時に読む、没アイテムは内蔵の表 `HiddenItemTable.h`）。成果物の逆アセンブルで WordRes と vt の順を確認。
- 反証条件: 自前表示で名前が変わらない・化ける・落ちる、通常アイテムの名前が ROM と違う。
- IDB: 5 関数を命名、2 か所に注記。

