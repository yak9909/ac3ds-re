---
id: ACNL-F0014
aliases:
- F-400
title: '最新 F-400: 再配置のPC試験成功・テーブル同梱を避ける方針'
summary: 利用者はSD/3gxへテーブルをリソース同梱する方式を避けたいと指定。
date: '2026-09-10'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:86-96
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## 最新 F-400: 再配置のPC試験成功・テーブル同梱を避ける方針

利用者はSD/3gxへテーブルをリソース同梱する方式を避けたいと指定。
内蔵辞書RomFSとSWKBD ExeFS .codeを実行時にRAMへ読む方式を候補とし、実機権限は未検証。
52箇所の観測絶対参照を全件idalib xrefで照合。callback3個と合わせ移設し、
元VAをunmapして0x04100000/0x06100000から候補列が一致。未修正コピーは旧19094Cで停止。
これはPCでの再配置可能性の確認。全経路閉包/学習/異なる版の対応は未完。
DOCS/system_keyboard_relocation.md、probe_relocated_engine.pyとf400証拠JSON参照。
今回実機アクセス/ビルド/SD/3gx変更なし。次は全参照の静的網羅と内蔵タイトル読取り権限の確認。


