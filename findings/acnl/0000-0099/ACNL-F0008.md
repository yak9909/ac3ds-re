---
id: ACNL-F0008
aliases:
- F-404
title: 'F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11）'
summary: 利用者が独立swkbd_probe.3gxを配置しACNLを再起動。新規header/生成コードアンカーを照合、Suspend/bp0を確認してmailboxに1要求を設定。5秒の自動Suspend付きResume後、state2/failure0。5,242,880 bytesを確保して全域write/readback成功、内蔵辞書2,045,891 bytesと圧縮.code 471,668 bytesのOpen/GetSize/全体Read/CRC32一致/Close/
date: '2026-09-11'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1273956
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:51-55
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11）

利用者が独立swkbd_probe.3gxを配置しACNLを再起動。新規header/生成コードアンカーを照合、Suspend/bp0を確認してmailboxに1要求を設定。5秒の自動Suspend付きResume後、state2/failure0。5,242,880 bytesを確保して全域write/readback成功、内蔵辞書2,045,891 bytesと圧縮.code 471,668 bytesのOpen/GetSize/全体Read/CRC32一致/Close/handle解放がすべて成功。buffer free完了、ログ書出しも成功。現在Suspend/PC0x00137064、command0、試験buffer保持なし。hardware_result.jsonを保存。3gx側で予定の検証容量を確保できた。エンジン本体はまだ実行していない。次は展開・再配置・実行権限と実機候補取得。詳細DOCS/system_keyboard_plugin_probe.md。


