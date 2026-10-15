---
id: ACNL-F0015
aliases:
- F-399
title: '最新 F-399: 画面・APTなしのエンジン実行をPCで確認'
summary: 初期化から全候補列挙までOS mockなし。原本data/BSSをRO化しても17/6件一致。
date: '2026-09-10'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1687296
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:97-107
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## 最新 F-399: 画面・APTなしのエンジン実行をPCで確認

初期化から全候補列挙までOS mockなし。原本data/BSSをRO化しても17/6件一致。
data/BSSを除去し0x1B8000の静的表1ページだけ保持しても一致。全除去は0x19BFA8で停止。
idalibの0x19BF00→0x1B8FD0参照と対応。書込みは独立context/stack/io/辞書poolのみ。
実機保存候補との照合6試験PASS。原本は絶対jump table/定数pointer/VFPを使用。
3DS上の独立モジュール化は有力だが、再配置・実行領域・RAM/ABI/時間の検証が必要。
今回実機接続/ビルド/3gx変更なし。DOCS/system_keyboard_engine_only.mdと
SYSTEM_KEYBOARD/audit_engine_only.py、evidence/f399_engine_dependencies.jsonを参照。


