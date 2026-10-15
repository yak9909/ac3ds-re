---
id: ACNL-F0356
aliases:
- F-330
title: 'F-330（2026-09-07）: OFF 通知の縁を帯より暗い赤に'
summary: 利用者の指摘：OFF の縁が帯と同じ赤だった。ON は帯（`#63e4a4`）より
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21652-21664
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-330（2026-09-07）: OFF 通知の縁を帯より暗い赤に

利用者の指摘：OFF の縁が帯と同じ赤だった。ON は帯（`#63e4a4`）より
暗い縁（`#4f6c5b`）なので、OFF も同様にする。

`kColDangerEdge`（`#6c4f5b`）を追加。`#4f6c5b` の R と G を入れ替えた
同系色で、くすんだ暗さは保って赤 dominant にした。
`AddNotice(..., red)` で帯 `kColDanger`・縁 `kColDangerEdge` にする。
プレビュー側（`app.js` の `drawNotice`）も無効時は赤の縁で描く。
検証器 2 種 0 件、ビルド済み。ケーブ不変。

実機では OFF 通知の縁が帯より暗い赤なことを見る。

