---
id: ACNL-F0170
aliases:
- F-132
title: 'F-132: 非整数倍率が右端の不均一さを生む — `HIGH`'
summary: F-131 の折り返しを除くため `T_time_0` の pane width を 40.0px にした状態で、同じ
date: '2026-08-24'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:8784-8809
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-132: 非整数倍率が右端の不均一さを生む — `HIGH`

### 動的比較

F-131 の折り返しを除くため `T_time_0` の pane width を 40.0px にした状態で、同じ
7px fallback glyph（CWDH `glyphWidth=6`, `advance=7`）について要求サイズだけを比較した。

| 条件 | 横/縦倍率 | 目視結果 |
|---|---:|---|
| `18 x 24`、NEAREST | `18/7`、`24/7` | 2文字は一行。ただし右端に1〜3px程度の不均一さが見える |
| `14 x 14`、NEAREST | `2`、`2` | 2文字は一行。右端の欠け・不均一さが改善し、字形自体に異常なし |

フォント、CWDH、文字列、pane width、filter（両flag OFF）は比較中に変更していない。
変更したのは TextBox `+228/+232` の要求サイズだけである。整数2倍で症状が改善したため、
右端の1〜3pxはメモリ上のbuffer越境や `glyphWidth` の不正参照ではなく、`18/7` の
非整数倍率を最近傍補間でラスタライズした際の端部境界・丸めの見え方が主因と判断する。

`glyphWidth=6` と `cellWidth=7` の差によるadvance余白は依然として存在するが、整数倍率では
その余白が不自然な欠けとして現れない。従って、CWDHを改変して `glyphWidth=7` にする
パッチは現時点では不要であり、stock資源を維持するのが安全である。

**根拠**: 静的 assembly（F-131 の quad/advance 計算）と、同一実機起動での
`18 x 24` / `14 x 14` A/B 目視比較。filter・font・pane幅を固定した一変数試験。

---

