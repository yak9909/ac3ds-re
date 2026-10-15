---
id: ACNL-F0447
aliases:
- IDA-opus-5-F014
title: 外部 nw4c ヘッダとの照合。実測は全て一致し、引数の解釈を2点訂正（2026-09-21、HIGH、静的＋実機照合）
summary: '解析ソフト: IDA / 解析モデル: opus-5。利用者提供の [SMBNext/nsmb2-headers](https://github.com/SMBNext/nsmb2-headers)'
date: '2026-09-21'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1474008
- 4814904
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:571-646
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F014: 外部 nw4c ヘッダとの照合。実測は全て一致し、引数の解釈を2点訂正（2026-09-21、HIGH、静的＋実機照合）

解析ソフト: IDA / 解析モデル: opus-5。利用者提供の [SMBNext/nsmb2-headers](https://github.com/SMBNext/nsmb2-headers)
（New Super Mario Bros. 2 の部分ヘッダ。`include/nw/gfx/` に nw4c のクラス定義）と
[mk7re/nw4c](https://github.com/mk7re/nw4c) を読み、**本ビルドの実測値と1件ずつ突き合わせた**。

**扱い**: 別タイトル・別ビルドなので、**ヘッダからは「メンバの宣言順と名前」だけを採り、
オフセットは全てこちらの実測を正とした**。ヘッダ中のコメントにある番地（例 `0x00167DD8`）は
NSMB2 のもので、**本ビルドでは一切使えない**。

### 一致した（こちらの実測 → 正式名）

| こちらの実測 | nw4c の正式名 |
|---|---|
| `AnimBinding` `[3]/[4]` | `m_AnimGroups`（`ut::MoveArray<AnimGroup*>`） |
| 同 `[7]/[8]`（私が「スロット配列」と呼んだ） | `m_AnimObjects`（`ut::MoveArray<AnimObject*>`） |
| 同 `[10]`（私が「行長」と呼んだ） | **`m_AnimObjectCountPerGroup`** |
| `AnimGroup+0x08`（`+16`にメンバ数、`+32`に phase） | `m_ResAnimGroup` |
| 同 `+0x1C`（ノードへの戻り） | `m_SceneNode` |
| 同 `+0x24/+0x28`・`+0x34/+0x38`・`+0x44/+0x48`（各18要素） | `m_TargetObjectIndicies` / `m_TargetObjects` / `m_TargetPtrs` |
| `sub_48A844` が呼ぶ `group[24]`（`+0x60`） | **`m_PreEvaluateCallback`**（`bool(*)(AnimGroup*,int)`） |
| `node+0x28` | `SceneNode::m_AnimBinding` |
| `node+0x4C` | `TransformNode::m_Transform`（CalculatedTransform の行列） |
| `node+0x8C` | **`m_WorldMatrix`** |
| `node+0xBC` | `m_CalculatedTransform` の行列 |
| `node+0x148` / `+0x14C` | **`Model::m_MaterialAnimGroup` / `m_MaterialAnimBindingIndex`** |
| `node+0x1EC` | `Model::m_MaterialActivator` |
| CGFX 辞書スロット 9 / 10 | `m_SkeletalAnimsDicCount` / `m_MaterialAnimsDicCount` |

`node+0x4C`/`+0x8C`/`+0xBC` の三つ組は、`sub_497F4C` が `+124/128/132` に `1.0f`・`+136` に 2049、
`+236/240/244` に `1.0f`・`+248` に 2049 を書いていたことと厳密に整合する
（CalculatedTransform ＝ 行列48B ＋ scale 12B ＋ flags 4B）。
`TransformNode` のメンバを順に積むと **ちょうど `0x148` から `Model` のメンバが始まる**。

### 訂正1: 第5引数は「材質のコピーマスク」ではない

`Model::Description` は `u32 bufferOption` を持ち、`BufferOption` の enum に
**`MULTI_FLAG_ANIMATABLE_MATERIAL`** がある。したがって
**a5 = `bufferOption`**（`model+0x188` はこれ）。IDA-unknown-F023 の「材質のコピーマスク」は不正確。

### 訂正2: アニメ機構を有効にするのは a5 ではなく a6（要検証）

`SceneNode::Description` は
`bool isFixedSizeMemory` / **`bool isAnimationEnabled`** / `s32 maxCallbacks` / `s32 maxChildren` /
**`s32 maxAnimObjectsPerGroup`** を持つ。

- **a7 = `maxAnimObjectsPerGroup`** — IDA-opus-5-F011 の「a7＝1グループあたりのスロット数」を裏付け
  （a7=3 で `m_AnimObjectCountPerGroup` が 3 だった）。
- **a6 = `isAnimationEnabled`** と見られ、**`AnimBinding` を作るのはこちらの可能性が高い**。

**IDA-opus-5-F009 の「第5引数がアニメ機構を作る」は、a5/a6/a7 を同時に `(0,0,1)→(0x834,1,3)` と
変えた A/B の結果であって、3つを分離していない。** ヘッダの語義からは a6 が本命なので、
F009 のこの部分は**未分離**として扱う。検証法は `(0, 1, 3)` で作って `node+0x28` が埋まるかを見ること（T011）。

### その他の名前

- ノード vtable slot 3 `0x00497838` = **`TransformNode::UpdateTransform(WorldMatrixUpdater*, SceneContext*)`**。
  `UpdateAll` が渡す第2引数は `SceneUpdater+0x40` の WorldMatrixUpdater、第3引数は **SceneContext**
  （私が「scene」と書いていたもの）。その `[3]/[4]` がノード配列、`[59]/[60]` が AnimBinding 配列。
- `node+52` は `SceneNode::m_PreUpdateSignal` で、`+8` がそのコールバック配列
  （こちらもプレイヤーも 0 個だったのはそのため）。

### 未採用・要注意

- `nsmb2-headers` に `SkeletalModel.h` / `SceneUpdater.h` / `AnimEvaluator.h` は無い。
  `node+0x228`/`+0x22C` が `SkeletalModel` の骨アニメ欄だという結論は**こちらの逆アセンブル由来のまま**で、
  外部資料の裏付けは無い（ただし `Model` の `m_XxxAnimGroup` / `m_XxxAnimBindingIndex` の並びとは整合）。
- `mk7re/nw4c` は小規模（`gfx` に `Camera.hpp` と `TransformNode.hpp` と `res/` のみ）で、今回は追加情報なし。
- マテリアルアニメのメンバ22個が何かは**まだ不明**。一般の CGFX 資料はテクスチャの
  scale/rotate/translate や差し替えを挙げるが、**本ビルドで確かめていないので採用しない**。
- **ACNL 専用の資料を発見**: [captainsouthbird/CGFXModel](https://github.com/captainsouthbird/CGFXModel)
  （ACNL の villager 編集）。別タイトルのヘッダより優先して当たる価値がある（T012）。

反証条件: `(0, 1, 3)` でも `AnimBinding` ができない（なら a5 が効いている）、
本ビルドのクラス配置が NSMB2 と部分的に違う欄がある。

