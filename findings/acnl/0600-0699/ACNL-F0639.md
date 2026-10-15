---
id: ACNL-F0639
aliases:
- Ghidra-gpt-sol-5.6-F001
- G-F001
title: 村を通過する電車は位置状態を持つ `AcStrcTrain` オブジェクトである
summary: '**確度: MEDIUM（複数の独立した静的証拠。実機インスタンス未観測）**'
date: '2026-09-19'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: Ghidra
addresses: []
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:7-20
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F001: 村を通過する電車は位置状態を持つ `AcStrcTrain` オブジェクトである

**確度: MEDIUM（複数の独立した静的証拠。実機インスタンス未観測）**

更新版 `ModuleOutdoor.cro` に `AcStrcTrain` クラス、`AcStrcTrain::Allocator`、`Strc/sobj/sobj_train/sobj_train.bcres` が存在する。RTTI/内部relocationを復元すると継承は `AcStrcTrain -> UtlBase<AcStrc> -> AcStrc`。

`AcStrcTrain` 固有vtable処理で、インスタンス `this+0x14/+0x18/+0x1C` の3連続値を一組としてコピー・引数渡ししている。更新処理（CRO file offset `0xC800`）は `this+0x14 += this+0x40` を毎更新行い、初期化処理（`0xC4FC`）は進行方向に応じて `+0x14` と `+0x40` を初期化する。従って `+0x14..+0x1C` は3成分の位置ベクトル相当、`+0x40` は移動軸の更新量/速度相当と判断できる。

`0xBB30` でも `+0x14/+0x18/+0x1C` を `+0x334/+0x338/+0x33C` へ3成分まとめて複製し、そのベクトルを後続処理へ渡す。

**未確認:** `+0x14/+0x18/+0x1C` の各軸がX/Y/Zのどれに対応するか、ワールド座標かローカル座標か、村内で走行中の実インスタンスアドレスと実測値は未確認。従って「+0x14=X」とはまだ命名しない。

根拠: `work/evidence/train_object_20260915.md`。

