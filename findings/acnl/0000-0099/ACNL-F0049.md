---
id: ACNL-F0049
aliases:
- F-11
title: F-11 岩・構造物は cat10 経路の末端で脱落 — `HIGH`
summary: 対象 ID 153（cat10）は `0x59836C` で cat10 経路へ分岐し、
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5866348
- 5866616
- 5866888
- 5867144
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:829-845
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-11 岩・構造物は cat10 経路の末端で脱落 — `HIGH`

対象 ID 153（cat10）は `0x59836C` で cat10 経路へ分岐し、
`unk_767D80` と `unk_2FE984` が両方 0 を返して
`0x598478 : BEQ 0x598588`（アクション16 = 何も起きない）へ落ちていた。

**根拠**: breakpoint `0x598688` で `R0 = R4 = 16`、対象 ID 153、
結果アイテム 153（158 になっていない）を観測。定義テーブル実読で cat10 を確認。

これにより「パッチしたのに効かない」の原因が **I-cache ではなく未解析経路**だと確定。

`0x598478` を掘る経路へ転送すると、**構造物だけでなく岩も掘れるようになった**（実機）。
岩も cat10 と見られる。`REFERENCES/IDS/DropID (maybe).txt` の
`0x12 = 岩を砕く` が cat10 のアクション 18 に対応するという解釈とも整合する（未確定）。

---

