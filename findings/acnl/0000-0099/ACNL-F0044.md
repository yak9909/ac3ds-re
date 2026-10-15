---
id: ACNL-F0044
aliases:
- F-06
title: F-06 アニメ再生速度は VFP の S1 — `HIGH`
summary: '`Actor_PlayAnim` (`0x0068D0EC`) の引数:'
date: '2026-09-08'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6869228
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:738-750
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-06 アニメ再生速度は VFP の S1 — `HIGH`

`Actor_PlayAnim` (`0x0068D0EC`) の引数:
`R0`=actor, `R1`=animID, `S0`=開始フレーム, `S1`=**再生速度**(通常 1.0), `S2`=ブレンド(5.0)。

`S1` の `1.0f` リテラルの上位ハーフワードを 16bit 書換で倍率を変えられる
(`3F80`=1.0x, `4000`=2.0x …)。

**根拠**: assembly（各呼び出し直前の `VLDR S1, =1.0`）+ 実機での書換検証。
アドレス一覧は `DOCS/shovel_speed.md`。

---

