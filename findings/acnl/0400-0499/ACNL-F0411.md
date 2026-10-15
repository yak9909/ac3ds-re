---
id: ACNL-F0411
aliases:
- F-386
title: 'F-386: 内蔵SWKBDの漢字確定文字を共有メモリから回収（2026-09-09）'
summary: F-384のパッチを残したまま通常チャットを再度開き、利用者が `漢字テスト` を入力して
date: '2026-09-09'
category: text
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 9890554
- 1273956
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:24350-24371
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-386: 内蔵SWKBDの漢字確定文字を共有メモリから回収（2026-09-09）

F-384のパッチを残したまま通常チャットを再度開き、利用者が `漢字テスト` を入力して
右ボタンで確定した。利用者はゲームへ正常復帰したと報告した。再Suspend後の読み取りでは
state=3、run count=2、CreateMemoryBlock/Prepare/Start=0、sender=`0x401`、actual size=`0x400`、
wake reason=2、received handle=0、shared-handle close result=0だった。

`SwkbdResult=2` は2ボタン構成の右ボタン（confirm）と一致した。text offset=0、length=5
UTF-16単位で、共有ページ先頭10 bytesは `22 6F 57 5B C6 30 B9 30 C8 30`。厳密な
UTF-16LEデコード結果は利用者の入力と同じ `漢字テスト` だった。境界検査は
offset/lengthが共有ページ`0x1000` bytes内かつ設定上限32 UTF-16単位以内であることを確認した。

ゲーム側APT状態`0x0096EAFA`は0、PC=`0x00137064`、breakpoint 0。chat/frame hookと
ケーブSHA-256も適用時から不変だった。結果コードと共有ページという独立した2つの結果が
利用者の操作報告と整合するため、**通常チャットから起動した内蔵SWKBDで漢字変換後の確定文字を
安全に回収できる**ことをHIGHで確定する。

この戻り値が示すのは確定文字だけである。未確定の候補一覧、候補順位、文節境界は0x400-byte
戻り設定および共有ページには含まれなかったため、SWKBD実行中の候補生成・描画・辞書参照を
別途観測する必要がある。一次記録は
`SYSTEM_KEYBOARD/evidence/native_chat_first_confirm.json`。

