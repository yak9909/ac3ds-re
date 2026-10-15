---
id: ACNL-F0410
aliases:
- F-385
title: 'F-385: 通常チャットから内蔵SWKBDの起動・キャンセル復帰に成功（2026-09-09）'
summary: F-384を適用した実機で通常チャットを開くと、内蔵ソフトウェアキーボードが起動した。
date: '2026-09-09'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 9890554
- 1273956
tags:
- chat
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:24334-24349
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-385: 通常チャットから内蔵SWKBDの起動・キャンセル復帰に成功（2026-09-09）

F-384を適用した実機で通常チャットを開くと、内蔵ソフトウェアキーボードが起動した。
キャンセル後に再Suspendして読み取った値は、state=3、run count=1、
CreateMemoryBlock/Prepare/Start=0、sender=`0x401`、actual size=`0x400`、wake reason=2、
received handle=0、shared-handle close result=0だった。`SwkbdResult=1` は2ボタン構成の
左ボタン（cancel）と一致し、text offset=`0xFFFFFFFF`、length=0、共有ページ全ゼロだった。

ゲーム側APT状態 `0x0096EAFA` は0へ戻り、素の `BsSkb` 子 `0x32E143E0` も残っている。
PC=`0x00137064`、breakpoint 0、ケーブのSHA-256も適用時から不変。したがって、
**ACNLの通常チャット入口から、ACNL既存APT管理を使って内蔵SWKBDを安全に起動し、
キャンセル後にゲームへ復帰できる**ことを動的観測まで含めてHIGHで確定する。

確定入力とUTF-16結果の回収は次の試験。候補一覧そのものは今回の戻りデータには含まれない。
一次記録は `SYSTEM_KEYBOARD/evidence/native_chat_first_cancel.json`。

