---
id: ACNL-F0181
aliases:
- F-139
title: 'F-139: ResFont→CMAP→batch quad の実機経路を確認 — `HIGH`（経路・引数・構造）'
summary: 2026-08-28、Remote GDB を停止／再開し、文字更新中の同一呼び出しを breakpoint で採取した。
date: '2026-08-28'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7616360
- 7616604
- 5066412
- 5066696
- 5066632
- 5066688
- 5067032
- 5080196
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9137-9165
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-139: ResFont→CMAP→batch quad の実機経路を確認 — `HIGH`（経路・引数・構造）

2026-08-28、Remote GDB を停止／再開し、文字更新中の同一呼び出しを breakpoint で採取した。
実機で観測した値は次の通り。

- `0x743768` (`nwfont_ResFont_MapCharToGlyph`) に `tid=219` で停止。`R0=0x3302ABE0`
  （17×24 ResFont）、`R1=0x904A`（Unicode「遊」）。終端 `0x74385C` で `R0=0x0A01`
  （glyph index 2561）を返し、ResFont `+0x14/+0x16` は `0x904A/0x0A01` に更新された。
  CMAP の入力・出力・キャッシュ更新が静的実装と一致する。
- `0x4D4EAC` (`nwfont_CharWriter_EmitGlyphQuad`) に同じ `tid=219` で停止。`R0=0x0000FC70`
  （writer）、`R1=SP=0x0FFFFB10`（glyph record）。record は raw sheet `0x318B2A80`、
  glyphWidth=4、cellHeight=24、sheet=128×128、format=0x0B、descriptor=`0x319BEB70`。
  `writer+0x44=0x32D3A6F0` が非零であり、`a1+0x44 != 0` の batch 分岐を実際に選択した。
- batch 終端 `0x4D4FC8` で count が増え、生成 instance `0x32D3A770` は 44 bytes。
  末尾 descriptor は `0x319BEB70`、座標・UV・色の並びは静的 `0x4D4F88`〜`0x4D4FC0`
  の store 順と一致する。従ってこの表示経路では `0x4D5118`→`0x4D8484` の即時 texture
  setup は呼ばれない。
- 5秒の通常走行後も4フォントの descriptor table（154/3/3/1 entries）の handle
  フィールドは全て0。今回の batch 経路だけでは texture handle の遅延 materialize は観測
  されず、後段の描画 submit／別カテゴリ経路に残る。

**根拠**: 入口・終端 breakpoint の PC/thread/register、停止中の `dbg_read_memory` による
ResFont/CMAP/glyph/descriptor/batch buffer の実値、及び `code.bin.i64` の同一命令列・store
順。これにより F-130/F-131/F-134/F-137 のうち CMAP と batch 経路は `HIGH` に昇格するが、
`0x4D8484` の GPU upload/bind 時点は未観測のため F-137 の backend 部分は引き続き
`MEDIUM` とする。

---

