---
id: ACNL-F0627
aliases:
- IDA-gpt-6.1-sol-F003
title: '服・ワンピース・K.K. の曲を部屋に置くときの品番（2026-10-07、MEDIUM: 静的 2 経路）'
summary: '解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_pair_ids.md、アプリサーバー経由）。採番・照合・記録は親（opus-5.5）。根拠 **work/evidence/t022_pair_ids/report.md**。主 IDB に命名 13 関数・2 表、型 19、構造体 2、カテゴリの Enum、コメント 58（ID '
date: '2026-10-07'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1704052
- 6891736
- 5693224
- 7051592
- 7048408
- 7051924
- 7051948
- 9765924
- 8300176
- 9766092
- 8316248
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4933-4943
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F003: 服・ワンピース・K.K. の曲を部屋に置くときの品番（2026-10-07、MEDIUM: 静的 2 経路）

解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_pair_ids.md、アプリサーバー経由）。採番・照合・記録は親（opus-5.5）。根拠 **work/evidence/t022_pair_ids/report.md**。主 IDB に命名 13 関数・2 表、型 19、構造体 2、カテゴリの Enum、コメント 58（ID は親が F??? → 本 ID に置換、件数一致）。
- 床に「へやにかざる」とき、ゲームは**元の品番（服 = カテゴリ 6、ワンピース = 7、曲 = 47）のまま** 12 B の配置記録・家具・部屋のマップに書く（0x1A0074 の分岐、0x6928D8 の写し、0x56DF28 のマップ書き込み）。
- 「カベにかける」ときだけ 0x6B9948 → **0x6B8CD8** で 6 → 147 / 7 → 148 / 47 → 49 へ写す。0x6B8CD8 は「カテゴリの中の位置」を保って変換先のカテゴリの先頭へ足す汎用の写し替え（sub_5349DC(カテゴリ) = {先頭の品番, 件数}）。拾うと 0x6B9A94 → 0x6B9AAC で 6 / 7 / 47 へ戻る。
  親の照合（opus-5.5）: 0x6B8CD8 の命令（Item.bin +10 のカテゴリの比較 → 位置 = 品番 − 先頭 → 先頭 + 位置）。差 0x1039 / 0x5E はカテゴリの先頭の差と一致（F107）。
- → **T022 のリストは床に置くので 6 / 7 / 47 側**（tools/hhd/export_catalog_table.py の PAIR_PICK）。書き出した表の品のカテゴリ: 服 6 = 346、ワンピース 7 = 100、曲 47 = 91、147 / 148 / 49 は 0 件。
- 家具の生成の表（記述子 12 B）から、服 = AcFtrCloth（0x950424 → 0x7EA690）、曲 = AcFtrMusicJacket（0x9504CC → 0x7EE558）。派生 CRO の描画は未確認。
- 未確定: +0x1B の意味、実機の往復。反証条件: 通常の配置で壁用の品番が保存される観測。
- 追記（T022 カタログの生成器、2026-10-07 18:33、Codex t022_catalog_arc2 = gpt-6.1-sol xhigh）: 親の途中指示（turn/steer）で arc を上段タブ用 hhd_catalog_top.arc（19,240 B）と窓用 hhd_catalog.arc（517,032 B）に分割、manifest に所属を記載し両 arc の全参照を検査。アイコンの束は 3,723 品すべて 4,096 B の ETC1A4（ETC1 の 258 品は HHD の角の丸い型抜きのアルファを足し、色のブロックは保持）。designer の 6 場面を再比較（画素一致は未達: 文字の影・縞の位相・投影の差）。根拠 work/evidence/t022_catalog_arc/report.md。

