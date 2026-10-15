---
id: ACNL-F0610
aliases:
- IDA-opus-5.5-F094
title: gohan のリソースを sdmc:/gohan に（2026-10-06、設計 + 静的検査。実機未確認）
summary: '解析モデル opus-5.5。利用者の依頼: 没アイテムのアイコン・名前表・HHD の arc を SD の gohan フォルダから読む。名前表は人が読める形で、タイトル ID ごと（ローカライズ）。'
date: '2026-10-06'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4727-4734
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F094: gohan のリソースを sdmc:/gohan に（2026-10-06、設計 + 静的検査。実機未確認）

解析モデル opus-5.5。利用者の依頼: 没アイテムのアイコン・名前表・HHD の arc を SD の gohan フォルダから読む。名前表は人が読める形で、タイトル ID ごと（ローカライズ）。
- ゲームのアイテムアイコンは `Layout/ItemWin/item_icon_tex.arc`（DARC、`timg/icn_NNN.bclim`、各 1,064 B = ETC1A4 32x32 1,024 B + CLIM 見出し 0x28: `CLIM FFFE 0014 02020000 全長 1` / `imag 0x10 幅 高さ 書式 11` / データ長）。自前のアイコンも同じ形の arc（`timg/<番号>.bclim`）にした。
- 描画は変えない（`ItemIconWidget_SetItem` の後で `P_itemIcon` の TexMap を差し替え、GPU から読める借用ヒープのキャッシュへ写す）。arc の利点は標準の形・道具で見られること・3gx から外れること（3gx −105,056 B）。ゲームの arc 読み込み（ArcResAccReader）でゲームのヒープに常駐させる案は、ヒープを常に約 90 KB 使うので採らない。
- 並び: `sdmc:/gohan/common/hidden_item_icons.arc`、`sdmc:/gohan/<TID16>/hidden_items.tsv`（UTF-8 TSV: id, icon, kana, name）、`sdmc:/gohan/<TID16>/hhd_charcreate.arc`。生成: `tools/items/export_hidden_icons.py`（読み直して一致を検査）/ `export_hidden_items.py` / `tools/hhd/build_hhd_arc.py`。gohan work/sd-resources a83ceac。
- 検査: gohan の解析手順を Python に写して生成物に当てた → 絵 75 枚（見出しの検査を通過）・表 332 件（重複なし）・参照する絵 77 種のうち無いのは 5352・5353（以前と同じ）。

