---
id: ACNL-F0570
aliases:
- IDA-unknown-F012
- V2-F012
title: 店の営業時間判定は店・用途ごとに複製、共通の入口なし（2026-09-17、MEDIUM）
summary: 時刻はDate_GetRaw 0x2FB3A4（&0xACF6B0を返すだけ、466 caller）の[1]>>24、条例はsub_7585A0（[garden+0x621CF] bit1）/sub_7585C4。判定はShopHours_*（IDB命名済み）に複製され、多くはCRO（ModuleDowntown/Outdoor/Indoor/Shop/NpcDt/Club）から匿名インポートで直接呼ばれる。ShopsAlwaysOpenの9語は9関数の「0を返す出口」で関数
date: '2026-09-17'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 3126180
- 3183608
- 7414760
- 7432288
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4287-4293
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F012: 店の営業時間判定は店・用途ごとに複製、共通の入口なし（2026-09-17、MEDIUM）

時刻はDate_GetRaw 0x2FB3A4（&0xACF6B0を返すだけ、466 caller）の[1]>>24、条例はsub_7585A0（[garden+0x621CF] bit1）/sub_7585C4。判定はShopHours_*（IDB命名済み）に複製され、多くはCRO（ModuleDowntown/Outdoor/Indoor/Shop/NpcDt/Club）から匿名インポートで直接呼ばれる。ShopsAlwaysOpenの9語は9関数の「0を返す出口」で関数ごと1語が下限、減らせない（gohan.md店24時間オープン）。
時間帯は逆コンパイルと独立にUnicornで全時刻×条例を実行して一致（tools/patches/shop_hours.py→hours.json）。店名はVapecordラベルと、呼出し側の引数オフセット（garden+0x668A0 Re-Tail、+0x622EC Ables、+0x66730 Redd。Vapecord構造体注記と一致）による。
9語が触らない同種判定: ShopHours_ReTail_InHours 0x3093F8（Re-Tailの時間帯だけ。sub_112104〈住民の外出先5の可否、IsOpenと併用〉とModuleShopの条件分岐case0）、ShopHours_Ables_IsOpen2 0x7123E8（Ables版と挙動が全時刻一致。使用はsub_1120B8〈住民の外出先21の可否〉のみ。別関数である理由はLOW）、ShopHours_Redd_InHours 0x716860（Redd版から品の状態・playerフラグを除いた時間帯だけ。ModuleIndoorで「sub_70C58C（オフライン&&Nookling閉店…）なら!InHours」。用途LOW）。ほか看板/BGM等の番号を返すsub_70FDD8/71BC24/71DBCC/717088（推定LOW）。
住民の外出先（villager+0x250F）が閉店中の店なら状態を戻すsub_69D848がこれらを参照（LOW）。反証条件: 実機で店の開閉と上記関数の戻り値が食い違う。根拠work/evidence/shop_open/（README.md・callers.json・hours.json）、tools/patches/shop_open_callers.py・cro_call_context.py・shop_hours.py。

