---
id: ACNL-F0615
aliases:
- IDA-opus-5.5-F099
title: 'ゲームのカタログのプレビューは 2 枠を交互に使い、替えた前の枠は 1 フレーム後にすぐ壊す（2026-10-06、MEDIUM: 静的）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。'
date: '2026-10-06'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2259004
- 2259940
- 2260220
tags:
- catalog
supersedes: []
source: IDA:work/FINDINGS.md:4776-4783
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F099: ゲームのカタログのプレビューは 2 枠を交互に使い、替えた前の枠は 1 フレーム後にすぐ壊す（2026-10-06、MEDIUM: 静的）

解析ソフト: IDA / 解析モデル: opus-5.5。
- `PwpPreview_Update` 0x22783C: 表示中の枠 a1[564] を Scene_SubmitNode で出したあと、もう片方の枠にインスタンスが残っていれば同じ呼び出しの中で壊す（0x227BE4〜: アニメの解放、ModelInstance_Destroy x2、ホルダー sub_2F7330 x3、sub_536008）。前の枠が最後に出されたのは前のフレームなので、**替えてから 1 フレームで解放**しており、数フレームの待ちは無い。
- 次のモデルは空いている枠へ読む（PwpPreview_LoadSlot 0x227CFC）。表示中のモデルを出したまま次を読む二重化。
- gohan の BuildingPreview の片付けの 4 フレーム待ちは、ゲームより長い安全側の値（根拠は記録が無い）。
- IDB: 0x227BE4 にコメント。

