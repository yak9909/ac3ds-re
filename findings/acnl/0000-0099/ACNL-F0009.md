---
id: ACNL-F0009
aliases:
- F-403
title: F-403完了・F-404 3gx検証へ移行（2026-09-11）
summary: 最新はDOCS/system_keyboard_plugin_probe.md。全辞書2,045,891 bytesの実機取得と全bytes/SHA照合、6辞書個別照合が完了。一時handle/buffer/wrapperは全復元済み。エンジン実機実行は未実施。
date: '2026-09-11'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1368952
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:56-61
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-403完了・F-404 3gx検証へ移行（2026-09-11）

最新はDOCS/system_keyboard_plugin_probe.md。全辞書2,045,891 bytesの実機取得と全bytes/SHA照合、6辞書個別照合が完了。一時handle/buffer/wrapperは全復元済み。エンジン実機実行は未実施。
System/lyt heapの空きは小さいが、全heapの調査は未完。利用者の指定で3gx側メモリを検証する。現行pluginの総枠5 MiBは実機headerと一致、Lumaは10 MiB設定に対応。独立のPlugin/SwkbdProbeで5 MiBの一時確保・内蔵FS読取り・全解放を検証予定。10 MiBの実機確保は未確認。辞書SD/3gx同梱や自前メニュー統合はしない。gohan正常版を維持。最終読取りstate=-1/PC0x0014E378。


