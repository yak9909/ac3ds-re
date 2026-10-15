---
id: ACNL-F0449
aliases:
- IDA-opus-5-F016
title: アニメが何を動かすかは資源から読める。UnitCursor は色定数2本とUV平行移動（2026-09-21、HIGH、静的）
summary: '解析ソフト: IDA / 解析モデル: opus-5。外部資料（[captainsouthbird/CGFXModel](https://github.com/captainsouthbird/CGFXModel)）は'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:682-733
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F016: アニメが何を動かすかは資源から読める。UnitCursor は色定数2本とUV平行移動（2026-09-21、HIGH、静的）

解析ソフト: IDA / 解析モデル: opus-5。外部資料（[captainsouthbird/CGFXModel](https://github.com/captainsouthbird/CGFXModel)）は
**ACNL 対象だがアニメは明示的に非対応**（「villager のアニメは共通・外部」）で、この件には使えなかった。
代わりに**自前の `UnitCursor.bcres` を直接解いた**。外部資料より確度が高い。

### ResAnimGroup の配置（`AnimGroup::m_ResAnimGroup` が指す先）

| off | 内容 |
|---|---|
| `+0x08` | 名前への相対オフセット（`"MaterialAnimation"` / `"VisibilityAnimation"`） |
| `+0x10` | **メンバ数**（実機で読んだ 22 / 1 と一致） |
| `+0x14` | **メンバ DICT への相対オフセット** |
| `+0x20` | **phase**（マテリアル群=1、可視性群=0。実機の読みと一致） |

`UnitCursor` の `MaterialAnimation` 群の22メンバ（＝**動かしうる欄の一覧**）:

- `MaterialColor.Emission / Ambient / Diffuse / Specular0,1 / Constant0..5`（11個、kind `0x08000000`）
- `TextureMappers[0,1].Sampler.BorderColor`（kind `0x02000000`）
- `TextureMappers[0,1].Texture`（差し替え。kind `0x20000000`）
- `FragmentOperation.BlendOperation.BlendColor`（kind `0x04000000`）
- **`TextureCoordinators[0,1].Scale / .Rotate / .Translate`**（6個、kind `0x80000000`）

`VisibilityAnimation` 群の唯一のメンバは `IsBranchVisible`。
**これが IDA-opus-5-F013 で「行0・メンバ1・phase 0 の未使用グループ」と書いたものの正体。**

### CANM が実際に駆動するメンバ

CANM の配置: `+0x04` 版数、`+0x08` 名前、`+0x10` **ループ旗**、`+0x14` **フレーム数(float)**、
`+0x18` メンバ数、`+0x1C` メンバ DICT への相対オフセット。

| アニメ | ループ | フレーム数 | 駆動するメンバ |
|---|---|---|---|
| `UnitCursor` | 1 | **150.0** | `MaterialColor.Constant0` / `Constant1` / **`TextureCoordinators[1].Translate`** |
| `UnitCursorNG` | 1 | 150.0 | `MaterialColor.Constant0` / `Constant1` |
| `UnitCursorRotate` | 0 | **3.0** | `TextureCoordinators[1].Rotate` |

**`+0x14` の 150.0 は、実機で読んだ evaluator の `inner+72 = 150.0` と一致する**ので、
build が CANM を正しく読んだことの独立な裏付けにもなる。旧 IDA-unknown-F024 の
「UnitCursor ループ150 / NG ループ150 / Rotate ワンタイム3」もこれで裏付けられた。

### F013 の表現の訂正

画面で動いていたのは **`TextureCoordinators[1].Translate` による模様のスクロールと、
`MaterialColor.Constant0/1` の色変化の両方**。
利用者の指摘（「色ではなく位置が動いている」）は正しく、明帯の本数と位置が変わって平均輝度が
ほぼ同じだったのは Translate の寄与。ただし**色も同時に動いている**ので、
F013 で「色ではない」と言い切ったのも行き過ぎだった。両方が正しい。

根拠: `artifacts/update/romfs/Ftr/Chip/UnitCursor.bcres` の直接解読（実機不要・再現可能）。
反証条件: DICT の解釈違い、kind 語の意味が別、別資源で配置が異なる。

