---
id: ACNL-F0446
aliases:
- IDA-opus-5-F013
title: アニメの適用段は sub_48A844。画面で動いた（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**F012 で欠けていた「適用」段を特定し、実機で絵が変わった。**'
date: '2026-09-21'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4761668
- 4786200
- 9418512
- 4814904
- 4814900
- 4784116
- 4784200
- 9420032
- 9418824
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:492-570
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F013: アニメの適用段は sub_48A844。画面で動いた（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。**F012 で欠けていた「適用」段を特定し、実機で絵が変わった。**

### 適用段

**`sub_48A844(AnimBinding, phase)` 0x0048A844** が、結線済みアニメを評価して対象へ書き込む本体。
引数は `node+0x28` の `nw::gfx::AnimBinding` と phase。中身は実測した AnimBinding の配置と一致する:
`a1[3]/[4]` が行ごとの `AnimGroup` 配列、`a1[7]` がアニメのスロット配列、`a1[10]` が行長。
行ごとに `*(group+8)+32` の **phase バイト**が引数と一致したときだけ、その行の全スロットについて
アニメの vtable **slot 6** を呼んで評価し、`sub_742A9C` で結果を書き込む。

ゲームは `SceneUpdater::UpdateAll 0x00490818`（vtable `0x008FB710` の slot 5）からこれを
**phase 0 → ノード走査 → phase 1** の順で呼ぶ。**こちらの instance はシーンのノード一覧に
入っていないので一度も呼ばれなかった**、というのが F012 で絵が変わらなかった理由。

潰した候補（いずれも違った）: `SceneNode::Update 0x00497838`（vtable slot 3。ワールド行列と子の再帰）、
ノード vtable **slot 10 は `bx lr` の空実装**（Model / SkeletalModel / TransformNode とも `0x00497834`）、
`SceneUpdater` の slot 6/7（`0x0048FFF4` / `0x00490048` → `sub_7E4FFC` は**描画キューの構築**）、
`AnimBinding` の vtable（破棄2スロットのみ）、`g3d::MaterialAnim` の残りスロット（破棄系）、
ノード `+52` の updater 一覧（**こちらもプレイヤーも 0 個**）。

### phase は種別ではなく行ごとのタグ

| | groups | 行長 | 行 | phase | members |
|---|---|---|---|---|---|
| こちらの `UnitCursor` | 2 | 3 | **1** | **1** | 22（`m_UnitCursor` のアニメ可能欄） |
| 同 行0（未使用） | | | 0 | 0 | 1 |
| ゲームのプレイヤー（骨） | 1 | 1 | 0 | **1** | 18（骨） |

**「phase 0 = マテリアル、1 = 骨」ではない。** 行ごとのタグなので、**両方を呼ぶ**のが安全。

### 実機の結果

ケーブに適用パスを2本（phase 0 と 1）足した。計器: runs 46 / advances 46 / **applies 92** / submits 92。
applies が 92 = 46 × 2 phase × **結線のある1体**で、binding を持たない本は正しく飛ばされている。

`step = 0` で要求フレームを 0 / 50 / 100 に固定して撮り直すと:

| 領域 | 適用前 f000→f050 | **適用後 f000→f050** |
|---|---|---|
| カーソルの縞（右） | 0.05% | **42.92%** |
| カーソルの縞（左） | 0.00% | **69.13%** |
| 空の芝生（対照） | 2.33% | **0.00%** |

対照の芝生が 0% なので場面は静止しており、**変化はカーソルだけ**。

**動いているのは色ではなく模様の位置**（利用者の指摘で測り直して確定）。
縞を横切る走査帯（y 165..205）の輝度プロファイルで明帯を数えると:

| | 明帯の中心 | 平均輝度 |
|---|---|---|
| f000 | 145.5 / 196.0 / 278.5 / 313.0（**4本**） | 122.1 |
| f050 | 113.5 / 145.5 / 197.5 / 289.5 / 319.0（**5本**） | 119.1 |
| f100 | 113.0 / 143.0 / 190.5 / 280.0 / 316.5（**5本**） | 118.9 |

**本数と位置が変わる一方、平均輝度はほぼ同じ**。UV スクロールのような模様の移動であって、
色の脈動ではない。**当初「黄色→黄緑」と書いたのは誤り**で、模様がずれて芝生と重なる位置が
変わったのを色変化と取り違えていた。数値 `applied_stripe_bands.json`。
**メンバ22個の内訳は IDA-opus-5-F016 で確定した**（自前資源の直接解読）。
`UnitCursor` が実際に駆動するのは `MaterialColor.Constant0` / `Constant1` と
**`TextureCoordinators[1].Translate`** の3つで、**模様の移動と色変化の両方**が起きている。

画像 `applied_f000/f050/f100_top.png`、画素差分 `applied_frame_diff.json`。
**注意**: 「本」を対照に置いた領域は縞と重なるので対照にならない。空き地を使うこと。

### 毎フレームの契約（3gx 向けにまとめ）

1体につき毎フレーム **4 呼び出し**:
`Anim_SetFrame(anim, s0=要求フレーム)` → `sub_48A844(binding, 0)` → `sub_48A844(binding, 1)` →
`TransformNodeHolder_Submit(holder, 0)`。12体なら 12 + 24 + 24 + 12 = **72 呼び出し/フレーム**
（Unicorn の `twelve_with_anim` で確認）。ケーブは 656 B @ `0x838600`。

根拠: `sub_48A844` / `sub_490818` / `sub_497838` / `sub_7E4FFC` の逆アセンブル、
vtable `0x008FB710` `0x008FBD00` `0x008FB848` のスロット、実機の AnimBinding・AnimGroup の読み出し、
`events.jsonl` の `anim_apply_enable`、画像3枚と画素差分。
反証条件: phase を両方呼ばなくても動く、シーンへ繋げば `sub_48A844` を直接呼ばずに済む、
別の資源でメンバ数や phase が違う。

