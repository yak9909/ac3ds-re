---
id: ACNL-F0175
aliases:
- F-137
title: 'F-137: `SetGlyphTextureParams` の引数は decompiler 表示より多く使われる — `MEDIUM`'
summary: '`0x4D8484` の逆コンパイル表示では `0x7ABDBC` 呼び出しの引数が省略され、texture'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5080196
- 8043964
- 5067032
- 8045256
- 8044412
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9003-9031
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-137: `SetGlyphTextureParams` の引数は decompiler 表示より多く使われる — `MEDIUM`

`0x4D8484` の逆コンパイル表示では `0x7ABDBC` 呼び出しの引数が省略され、texture
parameter の state 設定だけに見える場合がある。これは call prototype/Hex-Rays 表示の
簡略化であり、引数が無視されている根拠にはならない。呼び出し元と本体の assembly を
独立に追うと、次が確認できる。

- `0x4D5118` の直前で `R0 = glyph+0x08` (sheet width)、`R1 = glyph+0x0A` (sheet height)、
  `R2 = glyph+0x10` (texture format)、`R3 = glyph+0x00` (raw sheet address) を設定して
  `BL 0x4D8484` する。
- `0x4D8484` は `R2` を switch selector として複数の format case を分岐し、`R3` を raw
  data として保持し、width/height/format/raw と filter/wrap 用の値を stack/register に
  pack したうえで `BL 0x7ABDBC` する。
- `0x7ABDBC` は他経路からも呼ばれる generic texture setup dispatcher で、
  後続の `0x7AC2C8` / `0x7ABF7C` が GPU texture parameter state を設定する。

したがって、この経路は「filter flags だけを設定する関数」ではなく、glyph sheet の
format・寸法・raw address に依存した texture setup と wrap/filter state 設定をまとめて
行う、と読むのが妥当である。ただし `0x7ABDBC` の backend が実際にどの時点で GPU へ
upload/bind するか、format enum の各値、live で渡される値は未観測であり、ここから
「GPU upload 完了」までは断定しない。

**根拠**: `0x4D5118`→`0x4D8484` の全引数レジスタ、`0x4D8484` の format switch と
`0x7ABDBC` call の assembly、`0x7ABDBC` の複数 caller/xref。`code_runtime.elf.i64` との
raw bytes 一致は F-135 で確認済みだが、live descriptor/handle と SVC/GPU side effect は
未確認である。従って役割の確度は `MEDIUM` に留める。

---

