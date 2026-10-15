---
id: ACNL-F0569
aliases:
- IDA-unknown-F013
- V2-F013
title: しずえ画面「準備中」の仕事はSvProc種別4、中で日替わり処理と寝癖（2026-09-17、HIGH）
summary: ModulePlSelect case0の記述子this+632（flags 0x24000942、+32 sub_5254C0）はsub_2388BCがthis+0x16Cへ入れ、talk driverはthis+0x168（vtbl 0x8F46D8→TalkSaveTask_Step 0x237868）を毎フレーム叩く（旧「this+632を叩く」を訂正）。StepがSvProc_StartThread 0x3046C0で「SvProc Thread」を作り、ProcT
date: '2026-09-17'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9389784
- 2324584
- 1767112
- 8951160
- 2147976
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4281-4286
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F013: しずえ画面「準備中」の仕事はSvProc種別4、中で日替わり処理と寝癖（2026-09-17、HIGH）

ModulePlSelect case0の記述子this+632（flags 0x24000942、+32 sub_5254C0）はsub_2388BCがthis+0x16Cへ入れ、talk driverはthis+0x168（vtbl 0x8F46D8→TalkSaveTask_Step 0x237868）を毎フレーム叩く（旧「this+632を叩く」を訂正）。StepがSvProc_StartThread 0x3046C0で「SvProc Thread」を作り、ProcThread_Run 0x1AF6C8→SaveProcess_Execute 0x1D3C38が+32を呼んだ後g_SvProcTypeTable 0x889578[((flags&0x3C0)>>6)-1]=[4] SvProcType4_Prepare 0x5CC724を実行。そこからSave_RunDayChangeWithPlayers→Save_RunDayChange→Town_OnDayChange→Save_PlayersOnDayChange→Player_OnDayChange→Player_ApplyAbsenceBedHead 0x20C688（選択中プレイヤーの不在15日以上で髪型16/33。0x20C6D8が寝癖付かないのNOP先）。
利用者の推測「寝癖付かないは準備中部分を書き換えている」を静的に裏付けた。含意: しずえスキップはcase0を走らせないので日替わり処理・受信ボックス取り込みを飛ばす可能性（別経路で補われるか未確認、実機比較が必要）。IDBに13関数と表を命名。反証条件: 実機で準備中にSaveProcess_Executeの種別4が走らない。根拠work/evidence/prepare_screen/README.md。
実機（2026-09-17、利用者）: しずえスキップ（case0を飛ばす）で寝癖と郵便ポストのメールが一緒に起きなくなることを確認。静的な経路と一致するのでHIGH（「準備中の日替わり処理に寝癖・郵便が含まれ、しずえスキップで飛ぶ」まで）。

