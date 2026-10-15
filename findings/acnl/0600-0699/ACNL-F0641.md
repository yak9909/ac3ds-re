---
id: ACNL-F0641
aliases:
- Ghidra-gpt-sol-5.6-F003
- G-F003
title: 村の風船は `AcBalloon` Actorで、生成・破裂・プレゼント配置を既存経路から制御できる
summary: '**確度: HIGH（静的実装経路を複数箇所で確認）。チートとしての実機実行は未確認。**'
date: '2026-09-19'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 5746172
- 9735636
- 9735644
- 5868524
- 5897340
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:41-63
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F003: 村の風船は `AcBalloon` Actorで、生成・破裂・プレゼント配置を既存経路から制御できる

**確度: HIGH（静的実装経路を複数箇所で確認）。チートとしての実機実行は未確認。**

更新版 `ModuleVillage.cro` に `BsVillageBalloonMgr` と `AcBalloon : UtlBase<Actor>` が存在する。自然生成manager更新（CRO file `0x1688`, text-relative `+0x1508`）は、本体 `ActorFactory_CreateByTypeId (0x57ADFC)` を `(typeId=0x00F1, manager, variant, &position, 0)` の形で呼ぶ。

本体global:
- `0x948DD4` = `BsVillageBalloonMgr_InstancePtr`
- `0x948DDC` = `AcBalloon_InstancePtr`

`AcBalloon` constructionが後者へselfを書き、teardownで0へ戻すため、stock subsystemは基本的に同時1 AcBalloon Actorを前提とする。

variantは少なくとも `0=通常`, `1=銀`, `2=金`, `3=空飛卵`。撃墜後の最終dropは `AcBalloon` state 1に集約される。内部state切替関数は CRO file `0xD304`（code/text-relative `+0xD184`）。通常はstate 0、銀はstate 2、金はstate 4で開始し、残存風船数が0になるとstate 1へ遷移する。

state 1のdrop処理（CRO file `0x19BA8`）は本体 `BalloonPresent_TryLandAndPlace (0x598BEC)` を呼び、Item IDは通常 `0x2036`、銀 `0x3362`、金 `0x3363`、イベント `0x211B`。

`0x598BEC` は着地点と周囲候補を検査し、FieldAction type `0x21` を登録して `fgobj_ObjectPresent` を生成・配置する。通常Dropperのdrop type `0x0A` / `0x59FC7C` とは別経路。

**チート実装案（MEDIUM）:** ModuleVillageロード中、manager != 0、AcBalloon singleton == 0を確認し、type `0x00F1` で対象マス上空へ生成。1 update以上初期化を通した後、`AcBalloon_SetState(actor,1)` を呼ぶ。任意Itemにする場合は `BalloonPresent_TryLandAndPlace` のItem引数を、そのcheat生成分の1回だけ差し替えるhookを使う。この方式なら既存の破裂・落下・FieldAction・despawnを維持できる。

根拠: `docs/balloon_spawn_drop.md`、`work/evidence/balloon_spawn_drop_20260915.md`。


