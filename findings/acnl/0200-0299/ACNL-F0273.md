---
id: ACNL-F0273
aliases:
- F-250
title: 'F-250: 未設定の変数に対する比較が 712 件を無音にしていた — `HIGH`（全件バッチで確認）'
summary: '全件バッチ（3,960 件）で 712 件が「ノート 0」になった。`SEQ_BGM_DJ01_HS_SANBIKA` を追うと:'
date: '2026-09-01'
category: sound
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:14588-14615
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-250: 未設定の変数に対する比較が 712 件を無音にしていた — `HIGH`（全件バッチで確認）

全件バッチ（3,960 件）で 712 件が「ノート 0」になった。`SEQ_BGM_DJ01_HS_SANBIKA` を追うと:

```
 86: varBF [1, -32512]     flag = (var1 <= -32512) -> 偽
100: jump/if [131]         ★flag が偽なので無視 -> 曲が始まらない
```

- **`0xBF` は必ず `var1` に対する比較で、`var1` を設定するシーケンスは 1 つも無い。**
  ゲーム側が外から入れる値なので、0 と決めつけると分岐が落ちて曲ごと消える
- 第 2 引数は全 3,494 箇所で先頭バイトが 0x80 以上。そのため
  **varint(128〜142) と BE s16(-32512〜) は同じ長さ**になり、
  `cseq.fit()` はどちらでも 100.00%。**長さでは解釈を決められない**

対処は解釈の断定ではなく方針: **未設定の変数を参照する比較では `flag` を触らない**
（未設定変数を使う命令を見送る既存の扱いと揃えた）。`synth.UNSET_CMP_NEUTRAL`。

効果: ノート 0 が **712 → 526 件**。K.K. の曲 **186 件が復活**。
残り 526 件のうち **489 件は `SE_MELODY`**（村メロ＝旋律が外部データ）、
ほかは `SE_SYS_SILENT` / `SE_MU_CTRL_*` / `SE_DJ_CTRL_*` など音符を持たない制御用。

**修正で出力が変わるのは 186 件だけ**（＝無音だった BGM）で、既存の 3,248 件は
1 件も変わらないことを、修正前後のボイス列比較で確認した。
そのため全件を回し直さず、`render.py --names=FILE` を足して差分だけ出した。

---

