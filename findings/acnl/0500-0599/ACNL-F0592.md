---
id: ACNL-F0592
aliases:
- IDA-opus-5.5-F076
title: '実行時のテクスチャ差し替えと性別の読み方を実機で確認（2026-10-05、HIGH: 静的 + 実機）'
summary: 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。T013 段 3（gohan work/hhd-charcreate 4c6db33、3gx fda07ad4…d0c5）。
date: '2026-10-05'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2854572
- 4937796
- 4954160
- 11172244
- 3140448
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4489-4500
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F076: 実行時のテクスチャ差し替えと性別の読み方を実機で確認（2026-10-05、HIGH: 静的 + 実機）

解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。T013 段 3（gohan work/hhd-charcreate 4c6db33、3gx fda07ad4…d0c5）。

- テクスチャの差し替え: `ItemIconWidget_SetItem 0x2B8EAC` と同じ手順（`nwlyt_ArcResourceAccessor_GetTexture 0x4B5844`(出力 20 B, holder+12, 名前) →
  材質+52 が指す TexMap の [0..3] に写し [4] の書式ビット 0xF00 だけ入れ替え → `nwlyt_TexMap_UpdateGpuRegs 0x4B9830` → 材質+0x4D bit2 を落とす）で、
  自前の DARC の絵（目 24・髪 32）を実行時に入れ替えられる。利用者の目視で目・髪の一覧の絵が正しく切り替わった（ALL PASS）。
- 性別: プレイヤー [0xAA7994] の +428（プレイヤー番号）→ `0x2FEB60`（プロフィール）→ +21946 の bit0。**0 = 男の子・1 = 女の子** として目の絵を選び、
  利用者の目視で「性別と対応している」→ 読み方が実機で一致（利用者のキャラの値そのものは未記録）。
- 髪のページ送り（N_All を 8 フレームで 276 滑らせて絵を入れ替え）も PASS。滑る長さは HHD のコードから未確認（仮の値）。
- 利用者指示（同日）: 髪型は男女の区別なく 4 ページ（1〜2 = 男の子 B00〜15、3〜4 = 女の子 G00〜15）。タッチペンでのスクロールにも後で対応する。

