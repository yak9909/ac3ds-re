---
id: ACNL-F0571
aliases:
- IDA-unknown-F007
- V2-F007
title: 木と家具の共通モデル生成・姿勢設定（2026-09-14、MEDIUM）
summary: 木を含むfieldオブジェクトはItem_GetFieldObjDef→def+0xC→manager+0x414の22-byte shape表→名前+5→0x5992D4→0x4A5F20→0x58EEC0→0x4F048C。家具も同じModelInstance_Createに到達する。holder経由のtranslation/matrix/scaleと破棄入口を特定・命名。Create返値成功だけではholder+4非nullを保証しない。
date: '2026-09-14'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5870292
- 4874016
- 5828288
- 5178508
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:4294-4298
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F007: 木と家具の共通モデル生成・姿勢設定（2026-09-14、MEDIUM）

木を含むfieldオブジェクトはItem_GetFieldObjDef→def+0xC→manager+0x414の22-byte shape表→名前+5→0x5992D4→0x4A5F20→0x58EEC0→0x4F048C。家具も同じModelInstance_Createに到達する。holder経由のtranslation/matrix/scaleと破棄入口を特定・命名。Create返値成功だけではholder+4非nullを保証しない。
独立12領域のIDA bytesと入力codeが一致し、Capstone ARM・RTTI・計算を照合。任意モデル配置の実機成功を主張しない。木ID・生成オプション・共有状態の続報はIDA-unknown-F009–F011。GPU寿命は未確定。詳細docs/topics/models3d.md、根拠work/evidence/models3d/。

