---
id: ACNL-F0489
aliases:
- IDA-opus-5.5-F044
title: '文字の挿入・削除・選択・確定、キーの経路、チャットの送信、入力欄の「未確定」と「選択」の飾り（2026-09-25、MEDIUM: 静的のみ。実機未確認）'
summary: F043 の続き。かな入力のコンポジションと漢字変換（利用者の依頼）の土台。
date: '2026-09-25'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5380904
- 5382356
- 5383624
- 5383916
- 5379836
- 5380836
- 5383736
- 5382596
- 5193260
- 5199212
- 5199444
- 5199524
- 5199584
- 5199780
- 5210476
- 5205012
- 5226760
- 8721416
- 5760812
- 5766664
tags:
- chat
supersedes: []
source: IDA:work/FINDINGS.md:2043-2064
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F044: 文字の挿入・削除・選択・確定、キーの経路、チャットの送信、入力欄の「未確定」と「選択」の飾り（2026-09-25、MEDIUM: 静的のみ。実機未確認）

F043 の続き。かな入力のコンポジションと漢字変換（利用者の依頼）の土台。

- **挿入** `TextManager_InsertChar 0x521B28`（旧 vc_WRITEFUNC）(tm, 字, 位置, ローマ字モード): 字 1/2/3 = カーソル直前の字の濁点・半濁点・小書き変換（表 `sub_4DA1C0`、tm+148 が 0 のとき）。ローマ字モード ≠ 0 なら未確定分 [cursor−tm+36, cursor) に字を足して `sub_4D9A2C` でかなへ変換し直す。普通の挿入: `sub_521244`(LineManager=tm+4) で入るか判定 → memmove → 文字数 +8 を増やす → 字を置く → ローマ字モードなら **tm+36++** → カーソル tm+20 を進める。満杯なら 0 を返しエラー音。
- **削除** `TextManager_DeleteRange 0x5220D4`（旧 vc_DELETEFUNC）(tm, 位置, 字数): 未確定の字数 tm+36 を、消した範囲と [cursor−tm+36, cursor) の重なりだけ減らす。カーソルも詰める。
- **選択**: tm+28 = 選択の起点、**tm+32 = 選択中（byte）**、tm+20 = カーソル。範囲は [min(+28,+20), max)。`TextManager_DeleteSelection 0x5225C8` が消して選択を解く（+32=0, +28=カーソル, +144=−1）。→ **ゲームの入力欄は選択を持つ**（F043 の「+24 が選択の起点らしい」は誤り。+24 は別の欄で −1 に戻されるだけ）。
- **Backspace** `TextManager_Backspace 0x5226EC`(tm, 無音): 選択があれば選択を消す、無ければ cursor−1 を 1 字消す。**未確定を確定しない**（DeleteRange が tm+36 を減らす）。
- **入力の入口** `TextManager_InputChar 0x5216FC`(tm, 字, ローマ字モード, 結合): 全キー配列が通る。ローマ字モード 0 なら先に `TextManager_FinishRomajiPending`（＝未確定を確定）。選択中なら選択を置き換える。空白（0x20 / 0x3000）は確定。**字 10（Enter）: 未確定 > 0 なら確定して音を鳴らして戻る（改行も送信もしない）**、未確定 0 なら vc_KEYENTER（改行可）のときだけ改行を挿入。
- `TextManager_CommitPending 0x521AE4`(tm, 選択を解く) = 携帯配列とローマ字の途中を確定。`TextManager_SetText 0x522638`(tm, 文字列, 長さ) は全欄を初期化（文字列 0 で全消去）。`TextManager_InputCellPhoneKey 0x5221C4` = 携帯配列の複数回押し。
- **キー配列の処理**（各 vtable の +0x10）: gui::GridKeySet `0x4F3E2C` / **gui::KanaKeySet `0x4F556C`**（字は `InputChar(tm, 字, 0, 0)` = 0x4F5654 と 0x4F56A4 の BL。**ローマ字モードが常に 0 なので、かなには未確定が無い**。Backspace 0x4F56E0、濁点キー 1/2/3 は 0x4F57A4）/ gui::QwertyKeySet `0x4F816C`（ローマ字モード = dword_AD0548: 0 英字 1 ひらがな 2 カタカナ。切り替えは `gui_QwertyKeySet_SetRomajiMode 0x4F6C14`、0 にすると確定）/ gui::CellPhoneKeySet `0x4FC108`。キーの種類は表 dword_8905C4（かな）/ dword_8908C4（qwerty）/ dword_8902C4（grid）の 12 B 行の先頭。
- **キーボード本体** = BsSkb（名前は状態機械の文字列 "BsSkb"、表 0x851408 の 28 状態。dword_94A654 に自身）。組み立て `BsSkb_InitStep 0x57E72C`: キー配列の種類 dword_AD0544（0 qwerty / 1 kana / 2・3 grid / 4 cell）で swkbd_*.arc を読む。キー配列は BsSkb+4416（+1388 も）。キーの事象 `BsSkb_OnKeyEvent 0x57FE08`（sub_4FD728 で登録）→ モード切替 `BsSkb_HandleModeKeys 0x57FE80` → キー配列 vt+0x10。
- **チャットの送信**: BsSkb の下のボタンは dword_AD0144 で 1/2/3 個（チャットは 2 個 = +1420）。`BsSkb_Wait_Calc 0x57B778`（状態 #4 wait）: 2 個のボタンの結果 1 → +4580 = 2 と `TextManager_CommitPending(tm,1)`（**送信の前に未確定を確定**）→ `BsSkb_ReturnWait_Calc 0x57D720` → `vc_CALLCHAT(1, +4580)`。vc_CALLCHAT は byte_9580E1 と dword_AD0278 に書くだけ。チャット側 `sub_193764`（表 0x848BC8 の Wait）が 2 を見て `ChatWindow_Send_Calc 0x1938EC` → 閉じるアニメ（BsSkb+1396 の +20 == 2）の後 vc_SUBMIT_CHAT → SetText(tm,0,−1)。結果 0 → CALLCHAT(1,1) = 閉じる。
- **入力欄の飾り**（チャット = lyt::TextAreaOneLineChat、vtable 0x8FD6D0 の +8 = `lyt_TextAreaOneLine_UpdateText 0x505A08`。手紙など = `lyt_TextArea_UpdateText 0x509F44`。部品の作成は `sub_5091D8` の P_decorArea / DecorCursor）:
  - 行ごとの +460 / +476 = **未確定の範囲 [cursor−tm+36, cursor)**（ローマ字の未確定の飾り）。
  - 行ごとの +492 / +508 = **選択の範囲**（tm+32 のとき）。
  - +524 / +528 = 携帯配列の途中（tm+132 のとき cursor−1 の 1 字）。+440 / +448 = カーソル。
  - 字ごとの送りは writer+80（+1576+80）を足して x を進め、飾りの位置 = 範囲の最初の字の x、幅 = 範囲の最後の字までの x の差。
- **設計への帰結**: tm+36 を立てれば、**ゲーム自身の飾り（未確定の範囲）・Enter での確定・送信前の確定・Backspace での縮み・カーソル移動での確定**がそのまま効く。かなのキーは InputChar(…,0,…) で毎回確定させるので、そこだけ変える必要がある。
- 反証条件: 実機で tm+36 を立ててもかなの範囲に飾りが出ない／Enter キー（字 10）がチャットで送信になる／Backspace で未確定の字数が合わなくなる。
- IDB: 上の関数を命名・注記（vc_WRITEFUNC / vc_DELETEFUNC は Vapecord のラベルを注記に残して改名）。

