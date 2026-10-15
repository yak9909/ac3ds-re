---
id: ACNL-F0180
aliases:
- F-142
title: 'F-142: EmitGlyphQuad は会話外 UI でも共有される — `HIGH`（実機）'
summary: 会話を開いていない状態で `0x4D4EAC` に software breakpoint を置くと実際に停止した。
date: '2026-08-24'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5066412
- 5068852
- 5068680
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9119-9136
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-142: EmitGlyphQuad は会話外 UI でも共有される — `HIGH`（実機）

会話を開いていない状態で `0x4D4EAC` に software breakpoint を置くと実際に停止した。
停止時の値は `R0=0x0FFFFC58`（TextWriter）、`R1=0x0FFFFAF8`（glyph record）、
`LR-4=0x4D5834`、`writer+0x3C=0x3302ABE0`（17×24 ResFont）、`writer+0x40=0`、
`writer+0x44=0x32D0721C`（batch buffer）、raw sheet=`0x3187CA80`、
descriptor=`0x319BE954`、scale X/Y=`1.0` だった。

従って `nwfont_CharWriter_EmitGlyphQuad` は会話専用ではなく、時計など別の UI 文字も
同じ `nwfont_CharWriter_DrawGlyphAndAdvance` (`0x4D5788`) から共有する。また、この実例は
`writer+0x44 != 0` の batch 分岐であり、`writer+0x40` を即時描画用 context として使わない。
この writer の `+0x44` を 0 にして即時経路へ強制するのは、`+0x40==0` のため null
context 参照になり危険である。即時描画の動的検証には、別の有効 context を持つ writer を
先に捕捉しなければならない。

**根拠**: 実機停止時の PC/register、停止中メモリ読み出し、`0x4D4EAC` の静的分岐条件。
breakpoint は読み出し前に削除済みで、ゲームメモリへの書込みは行っていない。

