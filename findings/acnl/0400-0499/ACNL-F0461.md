---
id: ACNL-F0461
aliases:
- IDA-opus-5.5-F037
title: '建物の影の表は一覧 0x67CC と同じ番号で並び、場面を作るときにしか作られない（2026-09-25、HIGH: 静的＋実機のクラッシュ時の値）'
summary: '場面を作るとき `BsShadowMapMgr_CreateResources 0x264C08` → `sub_265544`: `*(mgr+100) = sub_76EA84(StrcMgr)`（= `*(StrcMgr+0x67CC)`、一覧 0x67CC の数）。1 件ずつ `sub_6D9E58(StrcMgr, &model, i)`（一覧[i] の vt+156）から影のコマンドを作り、表 `dword_94A458` に {番地, 語数}（8 B）で並べる。'
date: '2026-09-25'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2509832
- 7793508
- 2511928
- 9344080
- 9344092
- 2500664
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1347-1356
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F037: 建物の影の表は一覧 0x67CC と同じ番号で並び、場面を作るときにしか作られない（2026-09-25、HIGH: 静的＋実機のクラッシュ時の値）

- 場面を作るとき `BsShadowMapMgr_CreateResources 0x264C08` → `sub_265544`: `*(mgr+100) = sub_76EA84(StrcMgr)`（= `*(StrcMgr+0x67CC)`、一覧 0x67CC の数）。1 件ずつ `sub_6D9E58(StrcMgr, &model, i)`（一覧[i] の vt+156）から影のコマンドを作り、表 `dword_94A458` に {番地, 語数}（8 B）で並べる。コマンドは影のヒープ（mgr+24）から借りる。
- 毎フレーム `sub_262698`（g3d FuncNode の描画コールバック）: `i < *(mgr+100)` かつ `表[i].語数 != 0` の間 `sub_76EB48(StrcMgr, i)` を呼ぶ。`sub_76EB48` は `i < *(StrcMgr+0x67CC)` のときだけ一覧[i] を取り、それ以外は 0 を返す。その 0 を検査しないまま `LDR R1,[R0]` を実行する（0x76EB64）。
- 表を作り直すのは `CreateResources` と `DestroyResources 0x265438` だけで、どちらも場面の読み込み時（vtable 0x8E9450 / 0x8E945C）に呼ばれる。`DestroyResources` が返すのは表の先頭と影のヒープ全体。1 件ずつのコマンドは個別には返さない。
- もう 1 本の表 `off_94A450`（`sub_260BB4`）は `mgr+92 / mgr+96` で回る地形側の表で、一覧 0x67CC とは関係ない。
- 実機（利用者報告「橋を消したら SIGSEGV」、2026-09-25）: PC 0x76EB64、LR 0x262838、R1 = i = 2、R2 = 一覧の数 = 2。`off_94A44C` = mgr = 0x3309C410、`mgr+100` = 3、表 0x30F9CDA8 の 3 件はいずれも語数 100。gohan の KillVisual が一覧 0x67CC から 1 件抜いたのに、影の表を 3 件のまま残したため。
- gohan の直し（PublicWorks `DropShadowEntry`、実機未確認）: 一覧 0x67CC から i 番目を抜くときに表の i 番目も抜き、`mgr+100` を 1 減らす。あとから一覧へ足した建物（i >= mgr+100）には影の表が無いので、影は出ないが落ちもしない。
- 反証条件: 表を詰めたあとも同じ PC で落ちる／消していない建物の影が消える、または別の位置に出る（→ 影のコマンドが一覧の番号以外の何かと結び付いている）。

