---
id: ACNL-F0764
aliases: []
title: "0x4EDC74 はアニメの再生速度（1 回の更新で進めるフレーム量）を設定する"
summary: "0x4EDC74(anim, rate) は AnimEvaluator の +64 に float を書く。+64 は 0x49BB0C が「1 回の更新で現在フレームに足す量」として読む（0 なら更新しない、初期値 1.0）。再生速度の設定。"
date: 2026-11-11
category: render
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses:
  - 0x4EDC74
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: sonnet-5.5
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x4EDC74 は `void Anim_SetRate(void *anim, float rate)`（rate は VFP s0 渡し）。アニメ（g3d::MaterialAnim など、vtable+8 が内部の AnimEvaluator を返す物）の +64 に、1 回の更新で進めるフレーム量を書く。確度 MEDIUM（独立した静的根拠が 3 つ。実測は無い）。

## 根拠

- 0x4EDC74: `VMOV S16,S0; LDR R1,[R0]; LDR R1,[R1,#8]; BLX R1; VSTR S16,[R0,#0x40]`。vtable+8 で内部オブジェクトを引き +64 へ s0 を書く。
- 読み手 0x49BB0C: `+64`（`VLDR S0,[R0,#0x40]`）が 0 なら何もしない。0 でなければ `S2 = (+56) + (+64)` を +76 の評価関数（引数 +80）で評価し、`+60 = +56`、`+56 = 新しい値`、`+88 = 1`。つまり +64 は現在フレームに毎回足す量。
- 初期化 0x490D80: `+64 = 1.0f`（0x3F800000）、`+56 = +60 = +68 = 0`。既定の速度が 1.0 と読める。
- 呼び出し側 0x227020: ビルド後に `Anim_SetFrame(0.0)`（0x2272D0）→ `sub_4EDC74(1.0)`（0x2272DC）。スケルタルも同じ並びで、「フレーム 0、速度 1.0」の初期化に当たる。
- 0x4911EC（AnimBinding_EvaluateAndApply から呼ばれる）は +56 と +64 を保存済みの値と比べ、変わっていれば再評価する。+64 が評価の入力として扱われている。
- 旧版 gohan の `AnimSetRate`（`void (*)(void*, float)`）と同じ番地・同じ形。

## 反証条件・未確認点

- +64 を「時間の倍率」ではなく別の意味で読む経路が見つかれば、結論は誤り。0x49BB0C を呼ぶ vtable の位置（どのクラスの何番か）は未特定。
- 実機で rate を変えて再生が速くなることは測っていない。
- 名前は旧版 gohan の `AnimSetRate` ではなく `Anim_SetRate` を使う（docs/naming.md の `<Subsystem>_<Verb><Object>`）。
