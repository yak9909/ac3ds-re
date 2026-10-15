---
id: ACNL-F0575
aliases:
- IDA-unknown-F008
- V2-F008
title: resource描画属性・scene番号・画面を区別（2026-09-14、MEDIUM）
summary: 0x317BD0の旧名ModelInstance_SetRenderLayerは誤解を招く。0x58E978のcallerは資源lookup結果を渡した後でinstanceを作り、関数内も相対辞書を変更する。ResModel_SetRenderLayerへ改名。共有資源を個別instanceの設定として変更しない。
date: '2026-09-14'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4311-4315
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F008: resource描画属性・scene番号・画面を区別（2026-09-14、MEDIUM）

0x317BD0の旧名ModelInstance_SetRenderLayerは誤解を招く。0x58E978のcallerは資源lookup結果を渡した後でinstanceを作り、関数内も相対辞書を変更する。ResModel_SetRenderLayerへ改名。共有資源を個別instanceの設定として変更しない。
Render_DrawScene2はBsShadowMapMgrの存在でgateされ、描画先/状態の切替と復元を伴う。0x264C08とRTTI/vtableを照合し、旧「無条件のscene 2」を訂正。これは本件用の空きプレビュー枠ではなく、resource内layer値とも別。旧資料は参照専用として保持し、現行IDBへ根拠コメントを追加。詳細と反証/未確定条件はdocs/topics/models3d.md。

