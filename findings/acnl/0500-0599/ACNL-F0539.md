---
id: ACNL-F0539
aliases:
- IDA-opus-5-F020
title: 姿勢を直接書くだけでは描かれない。骨格の更新が要る（2026-09-21、HIGH、実機。**F017 の訂正**）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**利用者の指摘（「UnitCursor が画面内に描画されていない」）から判明した。**'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5166996
- 5165036
- 5178508
- 5159956
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3723-3775
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F020: 姿勢を直接書くだけでは描かれない。骨格の更新が要る（2026-09-21、HIGH、実機。**F017 の訂正**）

解析ソフト: IDA / 解析モデル: opus-5。**利用者の指摘（「UnitCursor が画面内に描画されていない」）から判明した。**

### 症状

`many_instances.py` で作った12体は、**毎フレーム 12 submit / 12 advance / 24 apply が計器に出ていて、
ゲームも 30.67fps で無傷なのに、画面には1体も出ていなかった**。
尺を 1.0 → 4.0 → 12.0 と上げても、加算合成のせいでもなく、**本当に描かれていなかった**。

### 原因

`many_instances.py` は姿勢を**直接書き込み**で付けていた。`node+0x4C` / `+0x8C` / `+0xBC` へ
同じ 48 B を書き、`node+0x88 |= 0x800` を立てる。これは `TransformNodeHolder_SetMatrix3x4 0x4ED794`
が残す姿と一致する。**しかしゲームはその後 `TransformNodeHolder_UpdateWorldAndSkeleton 0x4ECFEC` も呼ぶ**。

こちらは node の行列だけでなく**骨格オブジェクトの骨ごとの配列も埋める**。
実測（カーソル0、骨1本）: `0x4ECFEC` を1回呼ぶと骨格 `skel+0x2C`（64 B）の **32 B** と
`skel+0x3C`（48 B）の **30 B** が変わった。呼ぶ前はそこが未初期化のままで、
**メッシュに有効な変換が無いので何も描かれない**。

`UnitCursor` は骨1本だが `type 0x40000092` ＝ SkeletalModel なので、この経路を通る。

### 直し方と費用

**1体につきゲーム呼び出しは3回**になる（2回ではない）:

```
ModelInstance_Create          0x004F048C
g3d_MaterialAnim_BuildFromRes 0x004EBC14
UpdateWorldAndSkeleton        0x004ECFEC   <- これが抜けていた
```

`many_instances.update_begin()` / `update_step()` を足した。
**`repose()` のあとにも毎回呼ぶ必要がある**（骨の行列は node の世界行列から導かれるため）。

実機で12体に対して呼んだところ、**その場で全部が画面に出た**。
画像 `cursor0_updated_top.png`（1体だけ直した状態。画面いっぱいの縞）、
`twelve_visible_top.png`（12体・尺3.0）、`twelve_spread_top.png`（12体・尺2.0で広げたもの）。
直す前の対照は `cursors_only_scale12_top.png`（尺12.0でも**何も出ていない**）。

### なぜ気づけなかったか

- 計器（submit 数）は「submit したか」しか測っていない。**描かれたかは測っていない。**
- `check()` は参照インスタンスと**node の欄**を突き合わせていたが、**骨格側は見ていなかった**。
- 唯一の視覚確認手段だった Chokistream がこの間止まっていて、古いフレームを返していた。
  その古いフレームにはゲーム自身が作った `cursorC` の縞が写っており、**自分の12体だと誤読した**。
- 一方 `arbitrary_model.py` 経由の本・カブトムシは `0x4ECFEC` を呼んでいたので普通に出ていた。
  **「出た方」と「出ない方」の差分を取っていれば早く気づけた。**

反証条件: 骨を持たない `nw::gfx::Model`（`0x40000012`）なら直接書き込みだけで出る可能性。
`book` は `0x4ECFEC` を呼んでいるので未検証。

