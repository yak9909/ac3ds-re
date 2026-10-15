---
id: ACNL-F0567
aliases:
- IDA-unknown-F015
- V2-F015
title: 日替わり処理の成長・郵便・「アイテム消えない」の中身（2026-09-18、MEDIUM）
summary: Field_GrowUp 0x104B54 のコールバックを romfs Fg/Param/Fg.bin（16B×254、tools/fg_param_dump.py、旧実測カテゴリ7件一致）と IDS のアイテムIDで特定。苗の成長 Field_GrowUpSaplings 0x2FD778→Field_GrowUpAdvanceStage（+6の次段階、最大4段）、無効な位置（外周・草地以外・周囲障害物・密集）の苗は Field_GrowUpWiltSapling 0x3
date: '2026-09-18'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1067860
- 3135352
- 3234320
- 1137488
- 1141264
- 1134944
- 1136136
- 1138812
- 1136052
- 3142020
- 2412240
- 3201172
- 7317672
- 7317544
- 5403468
- 5401620
- 3131728
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4272-4275
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F015: 日替わり処理の成長・郵便・「アイテム消えない」の中身（2026-09-18、MEDIUM）

Field_GrowUp 0x104B54 のコールバックを romfs Fg/Param/Fg.bin（16B×254、tools/fg_param_dump.py、旧実測カテゴリ7件一致）と IDS のアイテムIDで特定。苗の成長 Field_GrowUpSaplings 0x2FD778→Field_GrowUpAdvanceStage（+6の次段階、最大4段）、無効な位置（外周・草地以外・周囲障害物・密集）の苗は Field_GrowUpWiltSapling 0x315A10 等で枯れ姿ID1〜5。竹 Field_GrowUpBambooSpread 0x115B50（item+2下位3bitのカウンタ、周囲15マスへ埋まった竹の子0x200D、近くの竹0本80%/1〜3本40%/4本以上0%）。岩 Field_GrowUpSpawnRock 0x116A10（0x400付きの岩が無ければ草地へ0x98+rand5を1個）。花が枯れる Field_GrowUpWiltFlower 0x115160（Fg+0xE %/日、条例bit4で無効）、交配 Field_GrowUpBreedFlower 0x115608、基本18色の自然発生 Field_GrowUpSpawnFlower 0x11607C。埋没: 化石0x202Aを4個まで・落とし穴0x209Fを1個 Field_GrowUpBuryItem 0x1155B4。ほかラフレシア・ジェイコブズラダー・タンポポ・キノコ（11月）・蜂/お金の木。各段の乱数は日付＋町で初期化。郵便: Mail_Deliver 0x2FF184。準備中では SvProcType4_Prepare が日替わりの後に Mail_SP_First/Housing/Gardening を直接送り、日替わり内で季節NPC（Player_OnDayChangeNpcMail 0x24CED0）・つねきち・住民（Villager_SendMail 0x30D894）の手紙。Vapecord「アイテム消えない」: パッチ 0x6FA8A8 は Field_DeleteItemAt 0x6FA828 の削除を止める（日替わり内の呼び出し: 公共事業完成区画・家の目印・Town_DayChangeGrassAndStructures→Structure_StampAll(1,0)→建物の足元）、パッチ 0x52734C は Structure_StampFootprint 0x526C14 の大物削除、フック 0x2FC950（Field_SetItemAtWorldXY、旧vc_NEVER_WILT_FUNC）は苗が枯れる5か所で ID+1 を置く＝枯れずに成長。3部品とも日替わり処理内の処理を止める（利用者の推測と一致）が、パッチ1/2 の関数は日替わり以外（sub_5C9C24 等）からも使う。外周で木を消す Field_GrowUpClassifyTile の直接書き込みは対象外。IDB 43関数命名。LOW: byte_A0EAFC の意味、ctx+22697 が雨か、岩フラグの意味、フック5か所の JPN 対応。反証条件: 実機で準備中を飛ばしても岩・竹・花・埋没物が翌日変化する。根拠 work/evidence/prepare_screen/growup.md。

