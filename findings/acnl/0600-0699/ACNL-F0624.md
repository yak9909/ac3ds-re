---
id: ACNL-F0624
aliases:
- IDA-opus-5.5-F107
title: 'HHD と ACNL の品の名前での突き合わせと、ACNL の Item.bin のカテゴリ（2026-10-07、MEDIUM: 静的 + ROM の実データ）'
summary: '解析ソフト: IDA（capstone で code.bin を直接）/ 解析モデル: opus-5.5。T022 の品の対応（F101 の「曖昧な 1,410 件」）。'
date: '2026-10-07'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5460360
- 10560364
- 3132260
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4905-4916
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F107: HHD と ACNL の品の名前での突き合わせと、ACNL の Item.bin のカテゴリ（2026-10-07、MEDIUM: 静的 + ROM の実データ）

解析ソフト: IDA（capstone で code.bin を直接）/ 解析モデル: opus-5.5。T022 の品の対応（F101 の「曖昧な 1,410 件」）。
- ACNL の品のパラメータ: romfs Item/Param/Item.bin。`ItemParam_GetRecord` 0x535188 = [0xA1236C+4] + 番号 × 30（`RSB r0,r0,r0,LSL#4` → `ADD r0,r1,r0,LSL#1`）、番号 < 0x172B。カテゴリ = 記録 +10 の 1 バイト（`vc_GETCATEGORIE` 0x2FCB64、0x9B 以上は 0）。
  照合: ファイルの記録の 0x23C9 / 0x23CA（〜のかべ）= 3、0x23EC / 0x23ED（〜じゅうたん）= 4 = `HouseRoom_SetWallpaper` / `SetFlooring` が確かめる種類（F106）と一致。ファイルは 5,931 × 30 + 22 B（末尾 22 B は未確認）。
- HHD の品名: romfs Script/Str/STR_Item_name.umsbt を tools/items/dump_item_names.py --romfs で書き出せる（work/cache/hidden_items/hhd_item_names.tsv、5,790 件に名前）。
- 名前の一致: モデル名で 1 対 1 の 3,390 件のうち名前が同じ 3,278 件、違う 112 件（HHD で改名された壁紙・床紙など）。
- T022 のリスト（上段 01 / 04）に出る品のうち ACNL 側が複数の 578 件: 名前で 1 件に決まる 40、名前の一致が 0 件 1、**同じ名前の品番が 2 つ 537**:
  - 服 446 件: カテゴリ 6（0x2495〜0x2681、493 件）とカテゴリ 147（0x34CE〜0x36BA、493 件）の対。147 側は値段 0・+0x19 = 0x5D・+0x1B = 2。
  - K.K. の曲 91 件: カテゴリ 47（0x212B〜0x2185）と 49（0x2189〜0x21E3）の対（ほかにカテゴリ 50 の 91 件 0x21E7〜）。49 側は +0x19 = 0x5D・+0x1B = 2。
  - 仮説（LOW）: 147 / 49 が「部屋に置いた形」。かざるで服・曲を置くときにゲームが部屋へ書く品番をコードで確かめるまで、どちらを置くかは決めない。

