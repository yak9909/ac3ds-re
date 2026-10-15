---
id: ACNL-F0266
aliases:
- F-243
title: 'F-243: CSEQ バイトコードの命令表を確定（ラベル境界一致 100.00%） — `HIGH`'
summary: '`SOUND/cseq.py`。引数長は推測せず、**CSEQ が自前で持つ 33,344 個の `LABL` オフセットが'
date: '2026-09-01'
category: sound
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:14270-14308
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-243: CSEQ バイトコードの命令表を確定（ラベル境界一致 100.00%） — `HIGH`

`SOUND/cseq.py`。引数長は推測せず、**CSEQ が自前で持つ 33,344 個の `LABL` オフセットが
命令境界に落ちるか**で決めた（ラベルは必ず命令境界なので、これは命令表そのものの検定になる）。
`python SOUND/cseq.py fit` で再現できる。

**結果: ラベル区間 33,319 中 33,318 (100.00%)、復号失敗ゼロ。**

### ★「未知の命令」を追う前に、既知の命令の引数長を疑う

最初は 99.43% で、未知 opcode `0x98` `0x8C` `0x92` `0x99` `0x8F` … が 171 件残っていた。
**これらは実在しない。** `0xF0`（拡張命令）の **sub `0xE0` だけ引数が 1 バイト短い**のに
一律で読んでいたため、そこから先が全部ずれて別のバイトを opcode と誤認していた。
sub 別に測ると:

| sub | 引数 2 バイト | 引数 3 バイト |
|---|---|---|
| `0xE0` | **99.5%** | 2.1% |
| `0x80` / `0x81` / `0x86` | — | **100%** |

1 箇所直しただけで未知 opcode は全部消え、一致率は 100.00% になった。
**この誤りは音にも出ていた**（`SE_MU_CTRL_GRID_*` が雑音になっていた）。

### 命令表の要点

- `0x00-0x7F` note（opcode がキー、u8 velocity, varint length）
- `0x80` wait / `0x81` prg（varint）
- `0x88` opentrack（u8 + **u24 ビッグエンディアン**）/ `0x89` jump / `0x8A` call（u24 BE）
- `0xA0-0xA5` **接頭辞**。次の命令の引数の読み方を変える:
  `random`/`variable` は本体の**最後の引数を置換**、`time` 系は**後ろに追加**、`if` は追加なし。
  重ねられる（実際に出るのはほぼ `A2 A1` = if + variable）
- `0xC0-0xCF` / `0xD0-0xDF` u8、`0xE0-0xE7` s16
- `0xF0` 拡張命令 `sub, u8, s16`（**sub `0xE0` のみ最後が u8**）
- `0xB1` は u8 1 個のみ（`0xB0-0xBF` の他は u8+s16）。
  ラベル境界では区別できないが、`d0(attack) b1 00 d1(decay) d2(sustain) d3(release)` の
  四つ組が揃うのは 1 バイト読みだけ（387 箇所）。confidence: MEDIUM

**ファイル全体はリトルエンディアンなのに `u24` だけビッグエンディアン**なので注意。

