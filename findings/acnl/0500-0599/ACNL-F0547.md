---
id: ACNL-F0547
aliases:
- IDA-opus-5-F001
title: モデルのクラスは資源が決める。ゲーム内のCMDLは2種類しかない（2026-09-20、MEDIUM、静的）
summary: '解析ソフト: IDA / 解析モデル: opus-5。対象 `artifacts/update/exefs/code.bin`（VA=file+0x100000）。'
date: '2026-09-20'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1048576
- 5178508
- 4776784
- 7561560
- 4895344
- 9420032
- 4811068
- 9418824
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:4052-4069
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F001: モデルのクラスは資源が決める。ゲーム内のCMDLは2種類しかない（2026-09-20、MEDIUM、静的）

解析ソフト: IDA / 解析モデル: opus-5。対象 `artifacts/update/exefs/code.bin`（VA=file+0x100000）。
`ModelInstance_Create 0x004F048C` → `sub_48E350 0x0048E350` → `sub_736158 0x00736158` のswitchは
**呼び出し側の引数ではなく資源のtypeInfo語（ResModel+0）**で生成器を選ぶ。したがって任意bcresに対して
クラスを指定することはできない。romfs 1,907ファイルに現れるCMDLは `0x40000012` →
`nwgfx_Model_Create 0x004AB270` ＝ `nw::gfx::Model`（node vtable `0x008FBD00`、**953個**）と
`0x40000092` → `sub_49693C 0x0049693C` ＝ `nw::gfx::SkeletalModel`（node vtable `0x008FB848`、**379個**）の
**2種類だけ**。クラス名はvtable−4のTypeInfo→+4のマングル名（`N2nw3gfx5ModelE` /
`N2nw3gfx13SkeletalModelE`）から読んだもので、switchの見た目からの推定ではない。TypeInfoの基底欄より
SkeletalModelはModelの派生。個数は `CMDL` マジックの生走査とCGFXモデル辞書の走査という**独立2経路**で
一致した。実機で描画に成功した `fg_treeA_4` は `0x40000012`、不可視だった `UnitCursor` は `0x40000092`。

根拠: `tools/models3d/model_preflight.py --survey`（2経路一致を自身で表明する）、
`work/evidence/models3d/live_20260919/resource_snapshot.json` の `type`。
反証条件: DLC/更新で別のtypeInfoを持つCMDLが入る、switchのどれかの腕へ別経路から到達する。
未確認: SkeletalModel側を実機で描いた例はまだ無い。

