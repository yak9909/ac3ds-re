---
id: ACNL-F0010
aliases:
- F-402
title: 'F-402 最終: 内蔵code全体Read・バイト同一性・cleanup確認（HIGH）'
summary: code kind2で読んだ471668bytesが提供NCCH内.codeと完全一致。SHA09e684ca41504af96b6548f42e8a2a159f07d3865ca7077e1d4f8356b98ec14e、ExeFSエントリhashとも一致。ctrtool再展開770048bytesは従来解析対象SHAa0b78005b0a99116ca703bc9b7625ce1b0f2d4cc45f66fc6fb9ab8a34244d4f0と一致。NCCHheader署
date: '2026-09-11'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5174116
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:62-66
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-402 最終: 内蔵code全体Read・バイト同一性・cleanup確認（HIGH）

code kind2で読んだ471668bytesが提供NCCH内.codeと完全一致。SHA09e684ca41504af96b6548f42e8a2a159f07d3865ca7077e1d4f8356b98ec14e、ExeFSエントリhashとも一致。ctrtool再展開770048bytesは従来解析対象SHAa0b78005b0a99116ca703bc9b7625ce1b0f2d4cc45f66fc6fb9ab8a34244d4f0と一致。NCCHheader署名FAIL表示は別途記録し、署名真正性までは主張しない。辞書は先頭256byteとサイズの確認まで。
code Close/Releaseとgame heap Freeが完了。一時wrapper/code/scratchはbackupへ完全復元、既存launcher/chat維持。最終ACNL Suspend/PC0x004EF364/bp0。デバッガtimeoutは手動Suspend後に回復し、保留処理を二重送信せずcleanupした。全結果evidence/f402_step/code_verified.json/final_restored.json等。エンジンの実機実行は未実施。

