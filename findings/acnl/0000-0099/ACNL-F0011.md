---
id: ACNL-F0011
aliases:
- F-402@v1:RE/FINDINGS.md:67
title: F-402 実機結果更新
summary: ACNLから内蔵辞書のOpen/Size2045891/先頭256byte Read/Close/Releaseが成功。読取りsampleは提供NCCHの0x1200と一意一致（HIGH:静的経路と実測）。SWKBD codeはkind1OpenがE0E046BE、kind2 .codeはOpen/Size471668成功。先頭256byte ReadはE0C046F9、全体471668byte Readは成功。FSのRead返信byte数も471668。全bytes同一性は
date: '2026-09-11'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:67-71
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-402 実機結果更新

ACNLから内蔵辞書のOpen/Size2045891/先頭256byte Read/Close/Releaseが成功。読取りsampleは提供NCCHの0x1200と一意一致（HIGH:静的経路と実測）。SWKBD codeはkind1OpenがE0E046BE、kind2 .codeはOpen/Size471668成功。先頭256byte ReadはE0C046F9、全体471668byte Readは成功。FSのRead返信byte数も471668。全bytes同一性はまだ未検証。DOCS/system_keyboard_native_fs.mdとf402_step各JSON参照。
code全体Read後のClose確認中にデバッガ照会タイムアウト。heap buffer0x32DFC000/475136bytesとcode handle0x568054のcleanup、および一時wrapper復元が未確認。状態はRE/STATE.md先頭優先。OS追加RAM確保はD86007F3 OutOfMemory、試験用に既存game heapを利用した。最終エンジン設計の依存条件としない。

