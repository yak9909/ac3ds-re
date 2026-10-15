---
id: ACNL-F0572
aliases:
- IDA-unknown-F009
- V2-F009
title: 木の実体とSeason資源を原本照合（2026-09-17、MEDIUM）
summary: 更新Fg.binのItem0x26→shape0x25→base FgShape.binのfg_treeA_4。strideは元ARMの索引コードで決定。全23 Season00..22のモデル辞書と自身の名称が一致し、type0x40000012・mesh/material各1。ctrtool展開済み25資源を独立RomFS parserで原本bytesと照合PASS。base展開全体は10753/12938のPARTIAL、updateは4150/4150完了であり、全展
date: '2026-09-17'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4299-4302
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F009: 木の実体とSeason資源を原本照合（2026-09-17、MEDIUM）

更新Fg.binのItem0x26→shape0x25→base FgShape.binのfg_treeA_4。strideは元ARMの索引コードで決定。全23 Season00..22のモデル辞書と自身の名称が一致し、type0x40000012・mesh/material各1。ctrtool展開済み25資源を独立RomFS parserで原本bytesと照合PASS。base展開全体は10753/12938のPARTIAL、updateは4150/4150完了であり、全展開成功と混同しない。根拠tree_assets.json、inspect_tree_assets.py。

