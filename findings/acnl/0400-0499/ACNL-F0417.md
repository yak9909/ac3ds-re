---
id: ACNL-F0417
aliases:
- IDA-gpt-6-F013
title: T015の再実機訂正（2026-10-13）
summary: GPT-6/idalib、MEDIUM。pocket singleton0x9499ECをLoadStep/Disposeと原STRで照合。screen list先頭だけの取得を修正。trash cleanupはsource有効又はtarget drag可を音条件とするため、消去icon更新/非drag trashの組合せでは音が抑制される。成功時一度明示再生する。
date: '2026-10-13'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:10-15
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F013: T015の再実機訂正（2026-10-13）

- GPT-6/idalib、MEDIUM。pocket singleton0x9499ECをLoadStep/Disposeと原STRで照合。screen list先頭だけの取得を修正。trash cleanupはsource有効又はtarget drag可を音条件とするため、消去icon更新/非drag trashの組合せでは音が抑制される。成功時一度明示再生する。
- Aはnode StartDecideだけではBAC完了通知が来ない。本物のDecide→StateDecideAnim→wait cleanupを使い、即取得の完了を二重要求せず青を戻す。ROM index43=たべる/action16、15=じめんにおく/action0をdispatch ARM stride8/PMFと照合。index12/action15はにがすでありeat15仮説を却下。2checkboxはnative dispatch/重複排除を使う。
- フォント生成667codes/58source欠字0、元656/欠字10literal。2chat項目をkeyboardフォルダへ移設。根拠work/evidence/gohan_inventory_ui_followupとinventory_ui_followup_design.md。DB5func/global/14注記/PMF型+Enum/3prototype保存・close所有0。PC/公式XML進捗はSESSIONを正とし、GPU/音/実機成功へ昇格しない。

