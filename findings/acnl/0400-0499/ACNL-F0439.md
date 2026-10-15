---
id: ACNL-F0439
aliases:
- IDA-gpt-6-sol-F009
title: 下位送信のBusyは未確認フレーム数、F008待機中拒否の再検証（2026-10-04、静的＋利用者実測）
summary: F008試作で待機中にも`Net=1 Busy=1`が持続し、旧版では同じ接続内で複数回送信できたと利用者が確認。送信バッチ`0x62710C`は管理`+156+peer`のbyteを+1、受信下位ヘッダ低2bitの処理`0x62A0B4`は負deltaで減らす。これは未確認フレーム数であり、F008の「転送枠使用中」だけの解釈を訂正。`SendSegments`も同じゲートを呼ぶため、同じ瞬間の値1なら旧通常送信も失敗する。新事前呼出しが値1を作った証拠はなく、版差/タイミ
date: '2026-10-04'
category: network
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 6451468
- 6463668
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:227-230
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F009: 下位送信のBusyは未確認フレーム数、F008待機中拒否の再検証（2026-10-04、静的＋利用者実測）

F008試作で待機中にも`Net=1 Busy=1`が持続し、旧版では同じ接続内で複数回送信できたと利用者が確認。送信バッチ`0x62710C`は管理`+156+peer`のbyteを+1、受信下位ヘッダ低2bitの処理`0x62A0B4`は負deltaで減らす。これは未確認フレーム数であり、F008の「転送枠使用中」だけの解釈を訂正。`SendSegments`も同じゲートを呼ぶため、同じ瞬間の値1なら旧通常送信も失敗する。新事前呼出しが値1を作った証拠はなく、版差/タイミングとACK状態を追加測定する。旧通常送信を最初に呼ぶgohan診断版と4枠Tx/Ack表示を作成。IDBに関係5関数のrename、部分構造体2件、型/コメントを保存。根拠/反証条件は[coord_sync_unacked_20261004.md](evidence/network/coord_sync_unacked_20261004.md)。

