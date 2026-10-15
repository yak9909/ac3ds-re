---
id: ACNL-F0440
aliases:
- IDA-gpt-6-sol-F008
title: 送信者の動作中に下位種別12が拒否される送信ゲート（2026-10-04、静的MEDIUM／回避未検証）
summary: 利用者の2台では座標同期がホスト・ゲストの両方向で成立し、拒否は送信者本人の歩行・アクション中に起きる。受信相手の動作状態には依存しないとの訂正を優先する。個別宛先の`NetTransfer_SendSegments 0x616E10`は`NetTransfer_CanQueueForPeer 0x61849C`の拒否で0を返す。同関数は`enforcePeerMasks=1`なら相手別4マスクを検査し、0ならその4条件だけ省く。接続可能性とpeer転送枠のbusy検査は両モ
date: '2026-10-04'
category: network
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 6385168
- 6390940
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:231-234
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F008: 送信者の動作中に下位種別12が拒否される送信ゲート（2026-10-04、静的MEDIUM／回避未検証）

利用者の2台では座標同期がホスト・ゲストの両方向で成立し、拒否は送信者本人の歩行・アクション中に起きる。受信相手の動作状態には依存しないとの訂正を優先する。個別宛先の`NetTransfer_SendSegments 0x616E10`は`NetTransfer_CanQueueForPeer 0x61849C`の拒否で0を返す。同関数は`enforcePeerMasks=1`なら相手別4マスクを検査し、0ならその4条件だけ省く。接続可能性とpeer転送枠のbusy検査は両モードで残る。どの条件が歩行で落ちたかは未測定。gohanには通常モードが失敗してマスク省略モードが通るときだけ一片を1回試す変更を用意したが、実機成功は未確認。根拠・反証条件・IDBの7関数renameとコメントは[coord_sync_action_reject_20261004.md](evidence/network/coord_sync_action_reject_20261004.md)。

