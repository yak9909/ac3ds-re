---
id: ACNL-F0617
aliases:
- IDA-opus-5.5-F101
title: 'ACNL の品番 → モデル名の表と、HHD との品物の突き合わせ（2026-10-06、MEDIUM〜HIGH: 静的 2 本 + ROM の実データ）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。T022 の下調べ。'
date: '2026-10-06'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7767388
- 8830328
- 5460032
- 5149472
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:4795-4804
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F101: ACNL の品番 → モデル名の表と、HHD との品物の突き合わせ（2026-10-06、MEDIUM〜HIGH: 静的 2 本 + ROM の実データ）

解析ソフト: IDA / 解析モデル: opus-5.5。T022 の下調べ。
- ACNL: 番号 = (品番 & 0x7FFF) − 0x2000（`vc_READSTACK` 0x76855C、< 0x172B）→ モデル名 = `g_ItemModelNameTable` 0x86BD78[番号]（`ItemParam_GetModelName` 0x535040 → `ItemModel_BuildPath` 0x4E9320 が "Item/Model/%s.bcres"）。
- HHD（IDA-opus-5.5-HHD-F012）も同じ式・同じ名前の付け方（Item/Model/%s.bch）だが、**品番そのものはずれている**（int_fru_apple: HHD 0x2012 / ACNL 0x2018）。品番では突き合わせられず、モデル名で突き合わせる。
- 床だけ名前が違う: HHD floor_X / ACNL carpet_X または carpet_floor_X。
- `tools/hhd/match_items.py` の結果（work/evidence/hhd_decorate/item_match.{json,tsv}）: HHD のモデル名つき 5,904 件のうち ACNL にもあるもの 4,800 件（HHD のアイコンあり 4,756 件）、HHD のみ 1,104 件（rug 245・hobj 188・roof 96 など HHD 専用の部屋/外観パーツ）。
  同じモデル名の ACNL 品番が複数あるもの 1,410 件（int_orgel 91 本の曲違い、リメイクの色違いなど）→ 名前の文字列でも突き合わせる必要がある（未）。
- IDB: 0x86BD78 を g_ItemModelNameTable（const char *[5931]）、0x76855C にコメント。

