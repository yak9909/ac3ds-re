---
id: ACNL-F0619
aliases:
- IDA-opus-5.5-F103
title: ACNL の「かざる」の部品と、データだけ書いたときの振る舞い（2026-10-06、静的 + 実機 2 回。置く部品は実機未確認）
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。'
date: '2026-10-06'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 10152452
- 5891508
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4819-4832
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F103: ACNL の「かざる」の部品と、データだけ書いたときの振る舞い（2026-10-06、静的 + 実機 2 回。置く部品は実機未確認）

解析ソフト: IDA / 解析モデル: opus-5.5。
- **実機 試験 1**（gohan なし）: 部屋のマップ = [0x9AEA04] → 区画 +32（家の中は 1 個。12 B: +4 床の層 / +8 家具の上の層）→ 品物 = 層 + z*64 + x*4（16x16、4 B = 品番 + 旗。旗の上位 2 ビット = 向き。0x7FFE 空き、0x7FFC 大きな家具の占有）。
  床の層の椅子 1 個を 0x7FFE に書いた → **画面の椅子は消えず触れもした。家を出入りすると消えた**（利用者）。データと家具のオブジェクトは別。
- **実機 試験 2**: `Item_PlaceItem` 0x59E5B4 の操作 0xA（落とす）で椅子 → 葉っぱの見た目で足元に落ち、アニメの後に見えなくなり、そのマスには置けなくなった。家を出入りすると正面向きの椅子になっていた（利用者）。**「かざる」とは別の経路**。
  （試験 2 の「目の前」は sub_762D80 + sub_317090 で、実際は足元のマスだった。CTRPF のメニューを開いている間はゲームが止まるので、メニューの処理の中で結果を待つ作りは誤り）
- **「かざる」の部品**（静的、MEDIUM）: ポケットの品物を家の中で出す `sub_19AD30` → 家の中は `sub_1A003C`:
  `sub_690D24(記録, 品物, 1)`（GetPlayerObject の +20 位置・+46 向き）→ `sub_691AD4`（場所探し。大きさ ItemParam+23&0xF、向き 4 通り、プレイヤーのマスの周りの型）→
  **1 マスの試し `sub_6920CC(記録, x, z, 向き, 品物, 層, プレイヤー x, z, 向き, 型)`**（大きさと向きの全マスが空き・置ける・プレイヤーのマスと重ならない等。0 = 置ける。記録 12 B = 品物 / +4 x / +5 z / +6 向き / +7 層 / +8 旗）
  → 0 なら `sub_68FA84(記録)` = `g_BsFtrMgr` の下へ `Actor_SpawnByProfile` で家具のオブジェクト（その場で出る）→ `sub_4E7580`（特定の品物の記録）→ ポケットから消す（sub_2BFE8C）。
  戻り 1 = 場所が無い（メッセージ 14）。
- 試験 3 用 gohan work/furniture-test（置く = 自前の輪の探索 + sub_6920CC + sub_68FA84、消す = 一番近い家具へ Item_PlaceItem 操作 6）。結果待ち。

