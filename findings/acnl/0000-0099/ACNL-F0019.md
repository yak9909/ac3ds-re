---
id: ACNL-F0019
aliases:
- F-395
title: 'F-395: UI単文節経路と直接連文節APIの区別'
summary: MEDIUM。UI caller 0x10996Cは111FD4(ctx,1,text,0,0,55)を呼ぶが、最下層1145ACの
date: '2026-09-10'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:149-159
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-395: UI単文節経路と直接連文節APIの区別

MEDIUM。UI caller 0x10996Cは111FD4(ctx,1,text,0,0,55)を呼ぶが、最下層1145ACの
R3は1（1121F8で即値指定）。135988の単文節分岐へ入り、直接55と動作が異なる。
原本UI wrapperをPCで実行した4入力で確認。mutexのみモック。結果recordとgetter出力一致。
ctx=app+8、文節record=app+0x36890、u16件数=app+0x37B7Aをwriter/readerで照合。
旧実機「かんじ」はmode0・予測17・文節0。editorの変換対象区間は
start=[editor+0x14]-[editor+0x24]-[editor+0x28]、length=[editor+0x28]で、
入力取得と描画側で独立一致。全文の自動文節一覧と同一視しない。
詳細DOCS/system_keyboard_phrase_state.md、再現SYSTEM_KEYBOARD/verify_ui_phrase_route.py。

