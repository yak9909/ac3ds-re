---
id: ACNL-F0541
aliases:
- IDA-opus-5-F017
title: 同じモデル・アニメ12体の同時描画。実機で30.67fpsを維持し、submit先は溢れない（2026-09-21、HIGH、静的＋実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T010。'
date: '2026-09-21'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5178508
- 5159956
- 9424104
- 5165064
- 9423988
- 9438524
- 5160524
- 5178112
- 5426648
- 5166640
- 4810984
- 4895260
- 4820768
- 8276800
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:3804-3885
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F017: 同じモデル・アニメ12体の同時描画。実機で30.67fpsを維持し、submit先は溢れない（2026-09-21、HIGH、静的＋実機）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T010。
3gx へ十数体を組み込む前提（利用者指定）で、**同一モデル・同一アニメを12体**同時に生成・結線・描画した。

### 1体あたりの生成費用は「ゲーム呼び出し2回」で足りる

`tools/models3d/many_instances.py`。instance 生成 `0x4F048C` と アニメ構築 `0x4EBC14` の**2回だけ**呼び、
残りは**このセッションで全欄を観測済みの状態の直接書き込み**にした。

| 部位 | 方法 | 根拠 |
|---|---|---|
| instance holder | 16 B 書き込み（`0x8FCCE8`, 0, 0, 0） | `0x4ED008` の残す姿を全欄観測 |
| `g3d::MaterialAnim` | 32 B 書き込み（`0x8FCC74`, 2, 0, `0x90053C`, 0…） | `0x4EBE4C` の残す姿を全欄観測 |
| 姿勢 | 48 B を `node+0x4C` / `+0x8C` / `+0xBC` へ、`node+0x88 |= 0x800` | `SetMatrix3x4` の結果と一致。**ただしこれだけでは足りない — IDA-opus-5-F020 で訂正** |
| 曲面変換 | float32 で自前計算 | 下記のとおり実機と照合 |
| 結線 | `slots + 4*(0 + index*per_group)` へ `*(anim+8)` | `0x4F0300` の式をそのまま写した |

**ビルド後の `MaterialAnim+4` は 1**（コンストラクタが置く 2 ではない）。
12体すべてが、ゲームが端から端まで作った参照インスタンス（`cursorC` / node `0x30C51138`）と
**vtable・binding・`bufferOption 0x834`・`m_MaterialAnimBindingIndex 1`・`per_group 3`・
MaterialAnim の全8語の形が一致**した（`many_instances.check()`）。

### 曲面変換の自前計算は実機と一致（角度は完全一致）

`0x52CDD8` に同じ入力を渡した実機の答えと突き合わせた。
**角度 23822 は完全一致**、位置は最大 `0.0057` 単位差（相対 1.5e-5）で、これは
ゲーム側の三角関数と Python `math` の差。描画位置としては同一とみなせる。

### 実機の結果

| 項目 | 4体 | 12体 |
|---|---|---|
| 1500ms あたりの hook 実行 | 46 | **46** |
| 実効 fps | 30.67 | **30.67** |
| submit / フレーム | 4 | **12** |
| advance / フレーム | 4 | **12** |
| apply / フレーム | 8 | **24** |

**12体でもフレーム落ちが測れない**（実機の上限が30fps）。2回繰り返して同じ値。
Unicorn の `twelve_with_anim` の予測（12/24/12）と実機が一致した。

> **★訂正（同日）**: この時点の12体は**毎フレーム submit されていたが、画面には1体も出ていなかった**。
> 原因は姿勢付けの手抜きで、`TransformNodeHolder_UpdateWorldAndSkeleton` を呼んでいなかったこと。
> 詳細と直し方は **IDA-opus-5-F020**。上の計器の値そのものは正しい（submit は実際に起きていた）。

### submit 先は溢れない（静的に確定。実機で余裕も確認）

`TransformNodeHolder_Submit 0x4ED630` → node vtable スロット4（`+0x10`）
（SkeletalModel `0x4968E8` / Model `0x4AB21C`）→ traverser vtable スロット7（`+0x1C`）＝ `0x498F20`。
`0x498F20` は配列3本へ積む（`ctx+8` / `ctx+56` / `ctx+232`。3本目は `node+0x28`（binding）が非0のときだけ）。

`nwut_Array_PushBack 0x7E4B40` と `0x498F20` 内の手書き push は**どちらも、満杯かつ
成長不可（フラグ `& 0xC0000000 != 0x40000000`）なら「何も書かずに 0 を返す」**。
境界を越えて隣へ書く経路は無い。

実機（boot2、村の屋外）: 3本とも **容量1024・成長不可**、使用は 34 / 11 / 15。
12体を毎フレーム足しても余裕は990以上。

**注意**: 3本目（`ctx+232`）に積まれる条件が `m_AnimBinding != 0` なので、
**アニメを結んだ instance は submit するだけでこの配列にも載る**。用途は未解明（IDA-opus-5-T013）。

### 画像は未取得（**この時点では Chokistream の映像が止まっていた**）

> **★その後（同日）**: 映像は復旧し、撮れるようになった。そして**12体は本当に見えていなかった**
> （利用者の指摘で判明）。原因は IDA-opus-5-F020。以下はその時点の記録として残す。

計器は上記のとおりだが、**12体が画面に見えることの画像証拠は取れていない**。
`capture_chokistream.ps1` が返す PNG が Resume を2回挟んでも **sha256 まで同一**
（`25fcb833…5390e`。`many04_top.png` / `many12_on_top.png` / `many12_off_top.png` の3枚）で、
窓の内容が更新されていない。[dynamic_observation](../docs/dynamic_observation.md) が
「映像用JFrameに対する PrintWindow 経路は Image Sequence と未照合」と警告していた件に当たる。
**この3枚を描画の証拠に使わないこと。**
したがって「4体が描けている」と一度書いたのは誤りで、あれは古いフレームだった（同日中に訂正）。

根拠: `tools/models3d/many_instances.py`、`work/evidence/models3d/arbitrary_20260920/many_state.json`、
`events.jsonl` の `many_enable_stage_a` / `many_enable_stage_b` / `many_repose` / `many_reenable`、
`0x498F20` `0x7E4B40` `0x4968E8` の逆アセンブル、実機の traverser context `0x329ABEF0` 読み出し。
反証条件: 別の部屋で traverser の容量が違う、体数を増やすと配列が成長可へ変わる、
画像を取ったら12体が見えない。


