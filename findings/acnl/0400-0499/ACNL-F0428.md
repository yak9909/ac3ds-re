---
id: ACNL-F0428
aliases:
- IDA-gpt-6-F003
title: chat listの決定と時刻窓からのfield復帰（2026-10-12）
summary: 担当 GPT-6 / IDA（idalib）、更新原入力SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ARM32LE/imagebase0。native assembly、source、既存F036/F062を照合。確度MEDIUM、新修正版実機未確認。
date: '2026-10-12'
category: text
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1771160
- 7148336
tags:
- chat
supersedes: []
source: IDA:work/FINDINGS.md:91-98
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F003: chat listの決定と時刻窓からのfield復帰（2026-10-12）

- 担当 GPT-6 / IDA（idalib）、更新原入力SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ARM32LE/imagebase0。native assembly、source、既存F036/F062を照合。確度MEDIUM、新修正版実機未確認。
- SelectBase_WaitCalc 0x1B0698 は決定旗を消し、indexが同じ再決定はindexの変化から検出できない。native IsDecidedを元計算前に読むvt[24]ラップが必要。GameList十字の即通知は公共事業のpreview用なのでchat上だけfocus移動へ限定する。
- native BACはTouch state0xACF6E0のcurrentとprevious（+26）を使い、40Bの履歴/座標が必要。chat上のlist native updateの間だけraw40Bを差し込んで全bytesを戻し、背後UIは既存入力遮断を維持する。利用者が背後「とじる」への入力漏れと訂正したことが修正の前提。
- 時刻窓Update0x28C5C0の終了はUiScreen破棄のみ。要求0x6D1330→poll0x6D10A8はfield hidden bit4を待つ。nativeタブMenuOut0x6D4E5Cはidle/empty0x6D1074の後でMapSyncTabsInへ移る。直接要求のcallerはこのfield lifetimeも保持する必要がある。新owner4を使い終了後だけ返す。
- DBへMenu_IsIdleAndEmpty/BsMenuTab_MenuOutUpdateの2rename、前者bool(void)型、確認した20概念の根拠commentを保存/読戻し/close（所有0）、公式XML/全bytes/hash PASS（44209functions/32995symbols）。既存実名を保持、Register/Unregister list primitiveや周辺の実class名・比較screenの意味は未確定としてrenameしない。根拠work/evidence/gohan_chat_lists_fix、設計docs/topics/chat_lists_fix_design.md。

