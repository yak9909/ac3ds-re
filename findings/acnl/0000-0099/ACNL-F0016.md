---
id: ACNL-F0016
aliases:
- F-398
title: 'F-398: 関数型辞書の登録でPC候補列が実機保存値に一致（HIGH）'
summary: 0x18CDDCの日本語分岐はslot7=0x19BECC、8=0x19C334、9=0x16B890を登録。
date: '2026-09-10'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1687244
- 1688372
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:108-117
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-398: 関数型辞書の登録でPC候補列が実機保存値に一致（HIGH）

0x18CDDCの日本語分岐はslot7=0x19BECC、8=0x19C334、9=0x16B890を登録。
idalib assembly/decompileと二つの実機appの36-byte entriesが一致。
旧Probeに登録を足すだけで14→17件/1→6件、順序と文字列が実機保存値に一致。
0x1181D0は初期50件超で追加検索し、「か」143件・「し」195件をPC取得。
F-397のUI段階差という仮説を撤回。詳細DOCS/system_keyboard_full_candidates.md。
検証器verify_full_candidates.pyとevidence/f398_full_candidates.json。新規実機操作なし。


