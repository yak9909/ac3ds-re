---
id: ACNL-F0481
aliases:
- IDA-opus-5.5-F052
title: '持ち物の選択窓（ItemSelectWindow）と模様替えの範囲の枠（CollectChip）の作り（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 は実機未確認）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。マップエディターの範囲選択（利用者の決定: 案 B）のため。'
date: '2026-09-27'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2861232
- 2862220
- 9753300
- 9753324
- 9753348
- 9753372
- 9753396
- 2859120
- 2857504
- 2858268
tags:
- inventory
- map
supersedes: []
source: IDA:work/FINDINGS.md:1849-1863
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F052: 持ち物の選択窓（ItemSelectWindow）と模様替えの範囲の枠（CollectChip）の作り（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 は実機未確認）

解析ソフト: IDA / 解析モデル: opus-5.5。マップエディターの範囲選択（利用者の決定: 案 B）のため。

- **ItemSelectWindow**（code.bin、持ち物で「置く・捨てる」を出す窓）: 組み立て **0x2BA8B0**（itm_slct_win.bclyt、コマンド 0x3700、優先度 0x9F、
  in/out_itm_nm と in/out_slct_win を読む）、行の結線 0x2BAC8C（ButtonActionControl に 6 行。行の部品名の表 0x94D2D4 B_cntnts_0X /
  0x94D2EC T_slct_cntnt_0X / 0x94D304 N_slct_cntnt_0X / 0x94D31C P_undrLine_0X / 0x94D334 G_msg_0X。行の音 0x10003C3）、開く 0x2BA070
  （MENU_FLAGS・手カーソル・音 0x10003C4）。**大きさ 0x2B9A20**: 文字のある行だけ出し、幅 = 文字箱の幅の最大 + 15（行の B_cntnts の幅）、
  枠 W_slct_00 の幅 = + 30、高さ = T_slct_cntnt_00 の高さ × 行数 + 11（最小 32）、行の x = −幅/2 − 枠の x + 15。置き場所 0x2B9D1C（画面に収める）。
  W_slct_00 の基準点は上端中央（origin 1）、行は上端から 20 ずつ下。
- **CollectChip**（ModuleIndoor、範囲の枠 cip_group_00）: 組み立て CRO 0xB0AD88（コマンド 0x1000。W_Group_00 / P_Start_00 / P_End_00 / B_Group_00）、
  更新 0xB0ABF8（枠 = 始点と指の中点、大きさ |差| + 10.0（VLDR リテラル 0x41200000）、P_End = 指）、確定 0xB5923C（当たり判定の四角が枠と重なるチップを選ぶ）。
  Neutral 0xB0AAF0 = 押して枠を始め、離して確定（音 0x100051D。F053 で訂正）。
- チップの長押し: Select 状態 0xB429BC の `CMP R1,#6`（6 フレーム）と 24.0（F050）。

