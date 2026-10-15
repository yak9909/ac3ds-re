---
id: ACNL-F0442
aliases:
- IDA-opus-5-F009
title: アニメ機構は ModelInstance_Create の引数で作られる（**a5 ではなく a6。IDA-opus-5-F015 で確定**）（2026-09-21、HIGH、実機A/B）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**同じ資源・同じモデルで第5引数だけ変えた対照実験**を実機で行った。'
date: '2026-09-21'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1844712
- 9418556
- 9419492
- 9419228
- 9418312
- 9420236
- 4789456
- 9424328
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:239-284
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F009: アニメ機構は ModelInstance_Create の引数で作られる（**a5 ではなく a6。IDA-opus-5-F015 で確定**）（2026-09-21、HIGH、実機A/B）

解析ソフト: IDA / 解析モデル: opus-5。**同じ資源・同じモデルで第5引数だけ変えた対照実験**を実機で行った。
`UnitCursor` の資源はすでに読み込み済みのものを再利用し、instance だけ作り直した。

| 欄 | `(0, 0, 1)` | **`(0x834, 1, 3)`** |
|---|---|---|
| `node+0x28` `nw::gfx::AnimBinding` | `0` | **`0x30C513CC`** |
| `node+0x148` マテリアル `AnimGroup` | `0` | **`0x30C51C10`** |
| `node+0x14C` 行 | `0` | **`1`** |
| `node+0x228` 骨 `AnimGroup` | `0` | `0` |
| `node+0x22C` 行 | `-1` | `-1` |
| `node+0x1EC` activator | 非0 | 非0 |

**骨側が 0 のままなのは正しい**: `UnitCursor.bcres` は辞書スロット10（マテリアル）に3本持つだけで、
スロット9（骨）は空だから。つまり AnimGroup は**引数と資源の両方**で決まる。

**第7引数について（IDA-opus-5-F011 で訂正）**: ここでは「スロット数ではない」と書いたが、
実際には **a7 = 1行あたりのアニメスロット数**だった。`sub_1C25E8 0x001C25E8` が `a7 = 1` で
済んでいるのは1本しか結線しないため。**a5 が機構を作るか、a7 がスロット数**が正しい。
この関数は手本として最良で、`res+100`（スロット9の個数）→ `res+104`（そのオフセット）で骨アニメを取り、
`res+112`（スロット10のオフセット）の辞書から名前 `"milk_round"` でマテリアルアニメを引いている。
**これで IDA-unknown-F023 の「a5＝材質コピーマスク」という理解を訂正する**: a5 は
少なくともアニメ機構の生成も決めている。

### アニメ本体のクラスと構築子

RTTI で確定: `AnimEvaluator` vtable **`0x008FB73C`**、`TransformAnimEvaluator` **`0x008FBAE4`**、
`BaseAnimEvaluator` `0x008FB9DC`、`AnimBinding` `0x008FB648`、`AnimGroup` `0x008FBDCC`
（後ろ2つは実機のプレイヤー instance の実測と一致）。

**`sub_491450(obj, allocatorHolder)` が `AnimEvaluator` の構築子**（`0x004914D0` で vtable を置く）。
`+4` に allocatorHolder、`+12/+16` がヒープ用アロケータ枠（`sub_4EBC14` が
`Heap_CreateNamed_0(obj+12, …)` で使う）、`+48` に `AnimFrameController`、`+52` に `AnimFrame`、
`+64`/`+72` が `1.0f`、`+76` に既定の評価関数 `sub_4D3EFC`。**+112 まで書くので 116 バイト以上**。

**注意**: 実機でプレイヤーに結線されている evaluator（`0x306AE3E8`）の vtable は **`0x8FCDC8`** で、
`TransformAnimEvaluator` ではない派生クラスだった（`+0x10`〜`+0x1C` に 0x208 間隔の4本、
`+0x24` に 18＝AnimGroup のメンバ数）。**ブレンド用の派生**と見られる。
単一アニメなら素の `AnimEvaluator` で足りるはずだが、**これは未検証の仮説**。

根拠: 実機A/B（`events.jsonl` の `animtest_*`）、`sub_1C25E8` / `sub_491450` の逆アセンブル、
`code.bin` 全域の RTTI 走査、プレイヤー instance の実測。
反証条件: 別の資源で第5引数 0 でも AnimGroup ができる、`0x834` 以外の値でも同じ、
素の `AnimEvaluator` では `sub_4EBC14` の vtable slot6 が失敗する。

