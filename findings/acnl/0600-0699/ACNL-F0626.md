---
id: ACNL-F0626
aliases:
- T022
title: T022 カタログの生成器（Codex 依頼 t022_catalog_arc、gpt-6.1-sol xhigh、2026-10-07。打ち切り。記録 ID なし = 道具と生成物）
summary: 'tools/hhd/make_catalog_arc.py → work/cache/hhd/catalog/hhd_catalog.arc（5 レイアウト・373 アニメ・57 テクスチャ、構造検査 PASS）、tools/hhd/make_icon_bank.py → hhd_icons.bin（3,723 品。**ETC1A4 3,465 品と ETC1 258 品が混在**: 4,096 B に揃えた版と原本の形の版を作成。ETC1 に不透明のアルファを足す方式の採否'
date: '2026-10-07'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags:
- catalog
supersedes: []
source: IDA:work/FINDINGS.md:4929-4932
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## T022 カタログの生成器（Codex 依頼 t022_catalog_arc、gpt-6.1-sol xhigh、2026-10-07。打ち切り。記録 ID なし = 道具と生成物）
- tools/hhd/make_catalog_arc.py → work/cache/hhd/catalog/hhd_catalog.arc（5 レイアウト・373 アニメ・57 テクスチャ、構造検査 PASS）、tools/hhd/make_icon_bank.py → hhd_icons.bin（3,723 品。**ETC1A4 3,465 品と ETC1 258 品が混在**: 4,096 B に揃えた版と原本の形の版を作成。ETC1 に不透明のアルファを足す方式の採否は未定）、catalog_manifest.json（gohan 用のペイン名・アニメ・当たり）。
- designer で 6 場面を描画（work/evidence/t022_catalog_arc/comparisons.json）。配置・形は HHD のスクショに近いが画素一致は未達（タブの縞の位相・名前の文字や影など）。最後のタブ絵の補正の後の再描画・再比較と report.md は未実施（打ち切り）。

