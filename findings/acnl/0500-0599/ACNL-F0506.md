---
id: ACNL-F0506
aliases:
- IDA-opus-5.5-F025
title: 地形のマス情報は 10 バイト（角の高さ 4 個＋属性）で、足元データと同じ形／橋の四角の外周は必ず端のマス（2026-09-24、MEDIUM（静的＋romfs 全 24 本）。実機の見た目は未確認）
summary: '**地形の高さ**: `Field_GetGroundHeightAtWorld 0x6C69C0` -> `sub_6C6A60` -> `sub_6A8C80`。区画ブロック + 28 から'
date: '2026-09-24'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7104960
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2338-2348
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F025: 地形のマス情報は 10 バイト（角の高さ 4 個＋属性）で、足元データと同じ形／橋の四角の外周は必ず端のマス（2026-09-24、MEDIUM（静的＋romfs 全 24 本）。実機の見た目は未確認）

- **地形の高さ**: `Field_GetGroundHeightAtWorld 0x6C69C0` -> `sub_6C6A60` -> `sub_6A8C80`。区画ブロック + 28 から
  1 マス 10 バイト（行 160 バイト、`sub_75D024` の索引 `+0x1C + 160*(y&15) + 10*(x&15)`）。
  +0/+2/+4/+6 の u16 が 4 隅（下位 5 ビット x 8 = 高さ。`sub_75CFE4`/`75CFF4`/`75D004`/`75D014` の `LSL#27; LSR#24`）、
  +9 の bit6 が平らの印（`sub_75D044`）。**Strc/data の足元データ（16x16x10 = 2,560 バイト、+8 = 属性）も同じ形**。
- **橋の足元の四角**: romfs の `fobj_bridge_*`（24 本）すべてで、板（属性 0x17/0x18）は属性 0 以外の外接の四角の外周に来ない。
  外周は端（0x33・0xA0 など）。→ 橋の「岸の高さ」＝四角の中の地面の最大、として gohan のカーソルとカメラに使う
  （ゲームの建て方 = 地面 + 32（F024 以前の SpawnHeight）は川の中の基点を前提にしていて、陸の上だと 1 マス高い。利用者の報告）。
- 反証条件: 実機で、川の上の橋のカーソルが岸より低い／高く出る場合（四角が岸へ届かない川幅、崖際など）。

