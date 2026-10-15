---
id: ACNL-F0397
aliases:
- F-370
title: 'F-370（2026-09-08）: クラッシュ再発。犯人は呼び出し元の this=NULL'
summary: 前回と同じ PC=`0x0054C438`（`LDR R0,[R4,#0x148]`）だが今回は R4=`0x0`。
date: '2026-09-08'
category: system
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 5555256
- 5556296
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24062-24086
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-370（2026-09-08）: クラッシュ再発。犯人は呼び出し元の this=NULL

前回と同じ PC=`0x0054C438`（`LDR R0,[R4,#0x148]`）だが今回は R4=`0x0`。
部屋は `0x63` のまま。遷移要求は `0xFFFF`（なし）。
フック語は入ったまま。利用者の切り分け： 項目ON/OFFは無関係、
自前メニューONが相関する。

### スタックが無罪を証明した

SP の退避域： 保存R4=`0x32939880`（正常ヒープ）、保存LR=`0x0054C848`
（`Framework_MainLoop`。正常経路）。つまり入口R4は正常で、
+0x04 `MOV R4,R0` のあと +0x14 までに R4 が `0x0` になった。
+0x04〜+0x14 で R4 を書くのは +0x10 の分岐だけだが実体は
R1/R3 しか触らない（再確認済み）。コールバックは +0x04 より前で
復元済み。よって**入口 R0（＝呼び出し元が渡した this）が NULL**。
前回は `0x18`。ゼロ/小値が変動する。

### 結論と残課題

自前コールバックのレジスタ破壊では説明できない（+0x04 が洗い直す）。
`MainLoop` 側の framework ポインタが遷移途中で NULL/ゴミになっている。
フック存在自体・チートON状態・他エージェント・素の遷移バグの
切り分けが要る。E1（チートOFF で同遷移）が最優先。
項目OFFでもフックは入ったままなので、発火の有無とは独立の軸。

