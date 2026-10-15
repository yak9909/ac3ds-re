---
id: ACNL-F0542
aliases:
- IDA-opus-5-F008
title: 骨・アニメの構造。node+0x228 は AnimGroup で、F029 の2語の正体（2026-09-21、HIGH、静的＋実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**アニメを結線するには instance 側に「アニメ枠」が要る。**'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2256928
- 5159956
- 5178112
- 5160956
- 5164316
- 11172244
- 9424104
- 9418824
- 9418312
- 9420236
- 4811068
- 4812372
- 4812376
- 4895344
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3886-3943
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F008: 骨・アニメの構造。node+0x228 は AnimGroup で、F029 の2語の正体（2026-09-21、HIGH、静的＋実機）

解析ソフト: IDA / 解析モデル: opus-5。**アニメを結線するには instance 側に「アニメ枠」が要る。**
`ModelInstance_Create` はその枠を作らず 0 で初期化するだけなので、`(0, 0, 1)` で作った instance には
アニメを一切結べない（結線関数は**失敗しても何も言わずに戻る**）。

### 資源側: 種別は CGFX の辞書スロットで決まる

CGFX の DATA ヘッダは `res+0x1C` から (個数, オフセット) の対が 16 個並ぶ。したがって
**`res+100` = スロット9の個数 = 骨アニメ、`res+108` = スロット10 = マテリアルアニメ**。
ゲーム自身 `sub_227020 0x00227020` がこの 2 語を見て経路を分けている。
romfs 全体で `CANM` は 1,539 個。`humanAnimCommon.bcres` は骨アニメ 403・マテリアルアニメ 414、
`UnitCursor.bcres` は**マテリアルアニメ 3 本のみ**（`UnitCursor` / `UnitCursorNG` / `UnitCursorRotate`）、
`book.bcres` はアニメ無し。**注意: `CANM` の `obj+0` は typeInfo ではない**（浮動小数のデータ）。
種別は辞書スロットで判定する。

### 経路が 2 本ある

| 種別 | 生成 | 結線 | 必要な欄 |
|---|---|---|---|
| マテリアル | `0x004EBC14`（ヒープ名 `"MaterialAnim::build"`） | `0x004F0300(instance, anim, slot)` | **`node+0x148`** 非0、行 `node+0x14C` |
| **骨** | `0x004EBFFC`（ヒープ名 `"SkeletalAnim::build"`。**instance を引数に取る**） | `0x004ECD1C(instance, anim)` | **`node+0x228`** 非0、行 `node+0x22C` |

どちらも書き込み先は `node+0x28` の表の `[行 * 行長 + スロット]`。
**枠が 0 なら黙って何もしない**ので、戻り値では成否が分からない。

### 実機の実物（プレイヤーの SkeletalModel）

`[0x00AA7994]` のプレイヤー内に `TransformNodeHolder`（vtable `0x008FCCE8`）が 1 つあり、
その node `0x306AD3C8`（vtable `0x008FB848`）は:

- `node+0x28` = `0x306AD65C`、vtable `0x008FB648` = **`nw::gfx::AnimBinding`**（RTTI）。
  `[3]/[4]` が行の begin/end（1 行）、`[7]/[8]` がスロット配列、**`[10]` = 行長 = 1**。
  `0x4ECD1C` はここの `[7] + 4*(行*行長)` へアニメを書く。実機では `0x306AD6B4` に `0x306AE3E8`。
- `node+0x228` = `0x306AD91C`、vtable `0x008FBDCC` = **`nw::gfx::AnimGroup`**（RTTI）。
  `+0x1C` は node への戻りポインタ、`+0x24/+0x28`・`+0x34/+0x38`・`+0x44/+0x48` が
  **18 要素の並行配列 3 本**（アニメ対象＝骨などのメンバ表）。
- `node+0x148` = 0（このプレイヤーはマテリアルアニメを結んでいない）。

**これで IDA-unknown-F029 の 2 語が完全に説明できた。** `node+0x228`/`+0x22C` は
**骨アニメの結線欄**であって可視性とは無関係。IDA-opus-5-F005 で「0/−1 のまま描けた」ことと矛盾しない。
`nwgfx_SkeletalModel_Create 0x0049693C` は `0x496E54/0x496E58` で必ず `+0x22C = -1`・`+0x228 = 0` と置く。

### 次の一手（未検証の仮説）

`ModelInstance_Create` の第5引数（これまで「材質コピーマスク」と呼んでいた値）が
**AnimGroup を作るかどうかを決めている**可能性が高い。根拠: 木（アニメ無し）は `0`、
ゲームの `AcObjUnitCursor`（マテリアルアニメ3本）は **`0x834`** で、第7引数も `3`（＝スロット数か）。
検証法: `UnitCursor` を `(0x834, 1, 3)` で作り直し、`node+0x148` が非 0 になるかを見る。
なればマテリアルアニメを結線して実機で動かせる。ならなければ AnimGroup は別段が作っている。

根拠: `sub_227020` / `sub_4EBC14` / `sub_4EBFFC` / `sub_4F0300` / `sub_4ECD1C` / `sub_497F4C` /
`nwgfx_Model_Create 0x004AB270` / `nwgfx_SkeletalModel_Create` の逆アセンブル、
vtable `0x008FB648` `0x008FBDCC` の RTTI、実機のプレイヤー instance 読み取り、
`code.bin` 全域の変位 0x148/0x14C/0x228/0x22C ストア走査。
反証条件: 第5引数を変えても `node+0x148` が 0 のまま、AnimGroup を作る別経路がある、
`node+0x28` の表を後から差し替えられる。

