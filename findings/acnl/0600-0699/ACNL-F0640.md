---
id: ACNL-F0640
aliases:
- Ghidra-gpt-sol-5.6-F002
- G-F002
title: パチンコ弾はPlayer内の固定3スロットで管理される
summary: '**確度: MEDIUM（複数の独立した静的証拠。実機メモリ観測は未実施）**'
date: '2026-09-19'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: Ghidra
addresses:
- 6686480
- 6709012
tags:
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:21-40
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F002: パチンコ弾はPlayer内の固定3スロットで管理される

**確度: MEDIUM（複数の独立した静的証拠。実機メモリ観測は未実施）**

パチンコ弾は独立したActorを毎回newする構造ではなく、Playerインスタンス内に埋め込まれた **3個の固定projectile slot** を再利用する。

`SlingshotProjectile_FireReset (0x660710)` は装備item IDにより発射数を決める。通常/レンタル=1、銀 `0x3362`=2、金 `0x3363`=3。

各slotのstrideは `0x8C`。現在座標は `Player+0x118C/+0x1190/+0x1194 + slot*0x8C`、速度ベクトルは `+0x1180/+0x1184/+0x1188 + slot*0x8C`。active bitは `Player+0x12C8` のbit 0..2。

`SlingshotProjectile_UpdateAll (0x665F14)` はslot 0..2を固定上限で走査し、各slotについて独立に `position += velocity`、衝突更新、描画transform更新を行う。従って金の3発は3本とも別々のXYZ状態を持つ。

連射時は新しい論理Actorを追加するのではなく、既存slotの座標・速度を発射位置へ再初期化する。同時に旧描画instanceを解除し、汎用描画poolから再取得する。

発射リセットはPlayer state `0xA2` のanimation markerで呼ばれる。飛翔更新は通常Player updateから独立して継続するため、軌道そのものはモーションデータではない。

stockコードの同時上限は **1 Player Actorあたり3発**。

根拠: `docs/slingshot_projectiles.md`、`work/evidence/slingshot_projectiles_20260915.md`。

