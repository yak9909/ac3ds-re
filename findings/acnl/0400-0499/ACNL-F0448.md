---
id: ACNL-F0448
aliases:
- IDA-opus-5-F015
title: ModelInstance_Create の a5/a6/a7 を実機で分離（2026-09-21、HIGH、実機A/B/C）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-F014 の仮説を実機で検証。'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:647-681
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F015: ModelInstance_Create の a5/a6/a7 を実機で分離（2026-09-21、HIGH、実機A/B/C）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-F014 の仮説を実機で検証。
**同じ `UnitCursor` 資源に対し、引数だけを変えた4体**を作って比較した。

| instance | (a5, a6, a7) | `bufferOption` `+0x188` | `m_AnimBinding` `+0x28` | `m_MaterialAnimGroup` `+0x148` | `m_AnimObjectCountPerGroup` |
|---|---|---|---|---|---|
| book | (0, 0, 1) | 0 | **0** | **0** | — |
| cursorB | (0, 0, 1) | 0 | **0** | **0** | — |
| cursorC | (0x834, 1, 3) | **0x834** | 0x30C513CC | 0x30C51C10 | 3 |
| **cursorE** | **(0, 1, 3)** | **0** | **0x310152AC** | **0x3101565C** | **3** |

**確定（3つとも分離できた）**:

- **a5 = `Model::Description::bufferOption`**。`model+0x188` にそのまま入る（0x834→0x834、0→0）。
- **a6 = `SceneNode::Description::isAnimationEnabled` が `AnimBinding` と `AnimGroup` を作る。**
  a5 が 0 でも a6=1 なら両方できる。**IDA-opus-5-F009 の「第5引数がアニメ機構を作る」は誤りで、訂正する。**
- **a7 = `maxAnimObjectsPerGroup`**。`AnimBinding::m_AnimObjectCountPerGroup` に入る（3→3）。

`m_VisibilityAnimGroup` `+0x150` も a6 で作られる（cursorE で `0x31015568`）。
これが F013 で「行0・メンバ1・phase 0 の未使用グループ」と書いたものの正体。

### 安全上の注意（3gx では a5 も要る）

**`bufferOption = 0` でアニメを結線して走らせてはいけない。** `BufferOption` の enum には
`MULTI_FLAG_ANIMATABLE_MATERIAL` があり、これが**そのインスタンス専用の書き換え可能な材質**を
用意する。0 のままだと材質は共有のままなので、適用段（`AnimBinding_EvaluateAndApply`）が
**ゲーム自身が使う共有 `ResMaterial` へ書き込む恐れがある**。
実際ゲームの `AcObjUnitCursor` は `0x834` を渡している。
**したがって実用の組み合わせは `(0x834, 1, 3)`**: a6 で機構を作り、a5 で自前の材質を持たせる。
cursorE は**結線も描画もしていない**（危険なので試していない）。反証条件: `bufferOption=0` でも
専用材質が用意される経路がある。

根拠: `events.jsonl` の `t011_*`、4体の `+0x188` / `+0x28` / `+0x148` / `+0x1EC` の読み出し。

