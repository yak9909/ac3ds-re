---
id: ACNL-F0510
aliases:
- IDA-opus-5.5-F021
title: 家の足元は名前表に無い → ゲームが読み込み済みの足元を使う／0x05 は属性を書き換えない（F019・F020 の訂正）（2026-09-24、HIGH（実機の占有＋静的））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「住民の家の UnitCursor が 1x1」「ベンチの周りは物を置ける。花を植えられるは物を置けるの十分条件」。'
date: '2026-09-24'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1775392
- 5401620
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2411-2423
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F021: 家の足元は名前表に無い → ゲームが読み込み済みの足元を使う／0x05 は属性を書き換えない（F019・F020 の訂正）（2026-09-24、HIGH（実機の占有＋静的））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「住民の家の UnitCursor が 1x1」「ベンチの周りは物を置ける。花を植えられるは物を置けるの十分条件」。

- 住民の家（例 id 0x0B、(69,28)）は `Building_GetName` の表に名前が無い → gohan が `Strc/data/<名>.bin` を引けず 1 マスにしていた。
  実機の占有マップ（層 1）では外周込み 5x4＋下段 3 マス = `hobj_npchouse_XX.bin` の形。ゲームは型番号からファイルを決める（`Building_GetFootprintByCategory`）
  → 名前の無い id は描画スレッドで `Building_GetFootprint 0x1B1720(x, y, id)` を呼び、ゲームが読み込み済みの足元を写す（gohan `c2aab70`）
- 住民の家の衝突判定（花を植えられない）= 本体 3x3 のうち戸口（下段中央 0x31）を除く 8 マス
- **F019/F020 の訂正**: 「byte_957D32 & 2 は外周 0x05 を置けないとする」は誤読。`Structure_StampFootprint 0x526C14` は
  **コード 5 のマスだけ属性バイトを書き換えない**（default 分岐で v20 == 5 のとき LOBYTE(v34) = v20 を飛ばす）ので、0x05 のマスは元の地面の属性のまま。
  表で 0x05 を引く意味は無い。利用者の「花を植えられる ⇒ 物を置ける」とも矛盾しない
- 移動モード: 何も選んでいないとき、カーソルを合わせた建物を白・合成度合い 50 で光らせる（利用者指示）

