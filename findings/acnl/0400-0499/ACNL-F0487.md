---
id: ACNL-F0487
aliases:
- IDA-opus-5.5-F046
title: 'ソフトウェアキーボードのキーの「次の入力までの待ち」の正体（2026-09-26、MEDIUM: 静的のみ（逆アセンブル＋成果物の照合）。実機未確認）'
summary: 利用者の指示「ゲーム内のキー入力で、一度入力してから次に入力できるまでの短い待ちを無くす」の下調べ（gohan で対応、下記）。
date: '2026-09-26'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5232560
- 5764932
- 11339312
- 5766664
- 5234440
- 9424992
- 5189224
- 5195420
- 5205352
- 5219348
- 5202532
- 5202672
- 5204620
- 5233096
- 9425648
- 5229548
- 5229392
- 5766784
- 9798044
tags:
- keyboard
supersedes: []
source: IDA:work/FINDINGS.md:1973-1995
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F046: ソフトウェアキーボードのキーの「次の入力までの待ち」の正体（2026-09-26、MEDIUM: 静的のみ（逆アセンブル＋成果物の照合）。実機未確認）

利用者の指示「ゲーム内のキー入力で、一度入力してから次に入力できるまでの短い待ちを無くす」の下調べ（gohan で対応、下記）。

- **部品の更新** `gui_UpdateButtons 0x4FD7B0`(flags)（唯一の呼び出し元 = BsSkb の calc `0x57F744`、1 回/フレーム）:
  最初に `byte_9580E6`（忙しい）= 0、部品の一覧（番兵 `0xAD0630`、次 = [節]、部品 = 節 − 4。Vapecord の CUSTOMKEY）のどれかの **+12（押さえている）** が立っていれば 1。
  `(flags & 0x107) == 0` かつ `dword_95819C == 0` なら各部品の vt+8 を呼ぶ。忙しくなければ十字キーなどの事象（`off_958124` = `BsSkb_OnKeyEvent 0x57FE08`、4/5/6）も出す。
- 部品の vt+8 = `gui_ButtonEx_Update 0x4FDF08`（11 クラスが共有）: **+20（有効）かつ（+12 または 忙しくない）** のときだけ、状態 +16 で vt+0x28/+0x2C/+0x30/+0x34/+0x38 へ。
- **字のキー = `gui::InputButton`**（vtbl `0x8FD060`。作るのは 4 種のキー配列の組み立て `0x4F2E68` / `0x4F469C` / `0x4F6D68` / `0x4FA414` だけ）:
  - 状態 0 `0x4F6264`: まず +12 を落とす。タッチの「押した瞬間」（`sub_520D4C(0x8000)` = 入力の +4 の立ち上がり）かつ当たり判定内なら、押すアニメ、**+12 = 1・忙しい = 1**、状態 1、**事象 1（= 字の入力）**。
  - 状態 1 `0x4F62F0`: 離れるか外れたら音（+88）、離すアニメ（`sub_4FE1E8(b,2)`: 段 2 の組が空なら段 0 の組を逆向きに）、状態 2。
  - 状態 2 `0x4F6A8C`（EditAreaEx / TchOnButtonSp / EditArea と共有）: +281 が 0 なら `gui_Button_AnimsDone 0x4FD9C8`(b,2)（段 2 のアニメ +64 と +144 の 5 本がどれも再生中（+0x14 == 1）でない）が真で状態 0。
    InputButton の記述子（`sub_4FDD8C` で 0 埋め、組み立てが入れるのは段 0 = `n0s1` の組 +104 と段 4 = `i0` の組 +184 だけ）では段 2 が空 → **1 フレームで抜ける**。
  - → 離したフレームを N とすると、N+1 は状態 2、N+2 は状態 0（ここで +12 が落ちるが、忙しいはフレームの頭で計算済み）。**N+1・N+2 の 2 フレームは他のキーが更新されず、その間の「押した瞬間」は失われる**
    （押した瞬間しか見ないので、指を置いたままでは後から入らない）。同じキーも N+1 は受け付けない。30fps で約 67ms。これが待ちの正体と見る。
- **繰り返しキー = `gui::RepeatInputButton`**（vtbl `0x8FD2F0`、作るのは同じ 4 関数）: 状態 1 `0x4FCBEC` で離すと直接状態 0（+12 は次のフレームの状態 0 `0x4FCB50` で落ちる）→ 1 フレーム止まる。
- ほかの待ち（`BsSkb_OnKeyEvent` → `BsSkb_HandleModeKeys 0x57FE80` → キー配列 vt+0x10）に時間の条件は見当たらない。
- **対応（gohan）**: `0x4FD7B0` を MITM で包み、元の処理の前に、InputButton の状態 2 は `0x4FD9C8`(b,2) が真のときだけ状態 0 へ、状態 0 の InputButton / RepeatInputButton の +12 を落とす
  （＝ゲームが次の 2 フレームでやることの前倒し。条件 flags & 0x107 / `0x95819C` も写す）。成果物の逆アセンブルで番地・オフセット（+12/+16/+281、節 − 4）と呼び出し（R1 = 2）を確認。
- 反証条件: 実機で待ちが残る（→ 別の待ちがある）、同じキーの連打で押下の見た目が崩れる、字が二重に入る、長押しの繰り返しや Enter・濁点・ケータイの連打が変わる。
- IDB: `gui_UpdateButtons` / `gui_ButtonEx_Update` / `gui_InputButton_State0_Idle` / `_State1_Held` / `gui_Button_State2_WaitRelease` / `gui_Button_AnimsDone` /
  `gui_Button_PlayAnim` / `gui_RepeatInputButton_State0_Idle` / `_State1_Held` / `g_guiButtonsBusy` を命名・注記。

