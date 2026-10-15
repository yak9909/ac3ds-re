---
id: ACNL-F0007
aliases:
- F-405
title: 'F-405 解決: キャッシュ処理中のクラッシュ、再起動で一時変更解除'
summary: Plugin/crash_dump_00000004.dmpのPC0xFFF2B3F8はMCR p15,0,R1,c7,c10,1。R1=FAR=0x061BE000が試験arenaと一致し、DFSR0x805はsection translation fault/write。ARM11 core1、SVC mode、保存プロセスsocket/TID0x0004013000002E02。ダンプ解析とidalibの保存命令列を照合（HIGH）。他コアの異なるアドレス空間が原因とい
date: '2026-09-11'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:47-50
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-405 解決: キャッシュ処理中のクラッシュ、再起動で一時変更解除

Plugin/crash_dump_00000004.dmpのPC0xFFF2B3F8はMCR p15,0,R1,c7,c10,1。R1=FAR=0x061BE000が試験arenaと一致し、DFSR0x805はsection translation fault/write。ARM11 core1、SVC mode、保存プロセスsocket/TID0x0004013000002E02。ダンプ解析とidalibの保存命令列を照合（HIGH）。他コアの異なるアドレス空間が原因というdispatch仮説はLOW、svc0x91/0x93のどちらかは不明。ユーザー再起動後に旧cave/controlゼロ、元vtable、mailbox idleを確認した。F-405を再実行しない。以前の「結果未回収」は解消済み。pending_state.jsonに解決を記録し、旧記録はpending_state_before_resolution.jsonに保存。

