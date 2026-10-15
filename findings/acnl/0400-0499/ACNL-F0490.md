---
id: ACNL-F0490
aliases:
- IDA-opus-5.5-F043
title: '文字入力（チャット・手紙・掲示板共通）の sys::TextManager の欄とカーソル・未確定の扱い（2026-09-25、MEDIUM: 静的のみ。実機未確認）'
summary: 漢字変換の候補欄とかな入力のコンポジション（利用者の依頼）の下調べ。取っ掛かりは AnimalBytes `Sources/ACNL/Chat.cpp`（入力欄の UTF-16 = [0x958108]、文字数 = [0x958114]+8）。
date: '2026-09-25'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9797896
- 9797908
- 5385576
- 9427636
- 9427604
- 11338048
- 5382176
- 5216876
- 5380464
- 5382356
- 5383352
- 9424912
- 9425136
- 9425536
- 9424868
- 9425748
- 9425980
- 9424792
- 9426640
- 5185536
tags:
- chat
supersedes: []
source: IDA:work/FINDINGS.md:2065-2077
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F043: 文字入力（チャット・手紙・掲示板共通）の sys::TextManager の欄とカーソル・未確定の扱い（2026-09-25、MEDIUM: 静的のみ。実機未確認）

漢字変換の候補欄とかな入力のコンポジション（利用者の依頼）の下調べ。取っ掛かりは AnimalBytes `Sources/ACNL/Chat.cpp`（入力欄の UTF-16 = [0x958108]、文字数 = [0x958114]+8）。

- `TextInput_CreateTextManager 0x522D68`（キーボード入力の初期化）が sys::TextManager（160 B、vtbl 0x8FDAB4）を作って [0x958114] に置く。同時に sys::LineManager（136 B、vtbl 0x8FDA94）。設定は大域 0xAD0140..（最大字数 word_AD0160、vc_KEYENTER、vc_NUMBERS、vc_KEYAT）。
- TextManager の欄: +4 LineManager 側の状態（sub_521084 が位置を計算して +16 へ）、+8 文字数、+12 最大字数、+16 UTF-16 バッファ、**+20 カーソル位置**、+24 選択の起点らしき値（初期値 -1。`TextManager_SetCursor` が -1 に戻す）、+28 カーソルの控え、+32 旗、**+36 ローマ字の未確定の字数**、+40 余りの字数、**+132 携帯電話配列の複数回押しの途中**、+144 = -1。
- `TextManager_SetCursor 0x522020`(tm, 位置, 選択を消す, 控え): 途中の入力を確定 → 位置を [0, 文字数] に収めて +20 へ。入力欄に触れると `gui_EditArea_TouchSetCursor 0x4F9A6C` が当たり判定（文字欄 vt+20）で位置を出して呼ぶ → **入力欄にはカーソルがあり、タッチで動かせる**。
- `TextManager_FinishRomajiPending 0x521970`: ローマ字の未確定（+36 > 0）を確定する。カーソルの直前が N / n なら「ん」（dword_AD0548 == 2 のときは「ン」）にする。最大字数を超えた分は `vc_DELETEFUNC 0x5220D4`（1 字削除）で消す。→ **ゲームのローマ字の「未確定」は、打った英字をバッファに置いたまま字数を数えておく仕組み**。かな入力（KanaKeySet）には相当する欄が無い（未確認）。
- `TextManager_FinishCellPhonePending 0x5224B8`: 携帯電話配列の複数回押しの途中（+132）を確定する。
- キーボードの GUI クラス（RTTI）: gui::KanaKeySet 0x8FD010 / QwertyKeySet 0x8FD0F0 / CellPhoneKeySet 0x8FD280 / GridKeySet 0x8FCFE4 / KeySet 0x8FD354 / Key・NrmKey・MulKey・TglKey、gui::EditArea 0x8FD43C / EditAreaEx 0x8FCF98、lyt::TextAreaOneLineChat 0x8FD6D0。[0x958114] の参照は 161 か所（GUI 0x4F2000..0x50B000、TextManager 0x521000..、0x57B000.. は未確認）。
- 未解析: 文字の挿入の関数、選択（+24）の使われ方、送信（Enter）の処理、かなキーの押下から挿入までの経路、文字欄の描画位置（未確定部分の下線を引くため）。
- 反証条件: 実機で +20 がカーソルと連動しない／+36 がローマ字入力中に増えない。

