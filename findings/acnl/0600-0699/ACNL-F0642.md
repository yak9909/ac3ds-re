---
id: ACNL-F0642
aliases:
- Ghidra-gpt-sol-5.6-F004
- G-F004
title: 通常ドロップをAcBalloon経由へ置換するAR実装
summary: '**確度: MEDIUM（ARM/ABIは静的確認。現行cave移設版は実機未検証）**'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: Ghidra
addresses:
- 5857672
- 5868524
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:64-81
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F004: 通常ドロップをAcBalloon経由へ置換するAR実装

**確度: MEDIUM（ARM/ABIは静的確認。現行cave移設版は実機未検証）**

`Player_DropItem+0x104 (0x596188)` の最終 `BL Item_PlaceItem` をhookし、target tile中心へ `AcBalloon` を生成する。生成成功時はshared pageへ元Item/impact Vec3を保存し、同一game-thread内で `SetState(actor,1)` を同期callする。landing path `0x598BEC` はarmed中だけshared Vec3/Itemへ差し替える。

Ghidra-gpt-sol-5.6-F007で旧cave配置が既存描画caveと衝突していたことが判明したため、現行配置は:
- spawn `0x838200-0x83832F`
- landing `0x838330-0x838353`
- helper `0x838354-0x838393`

hook:
- `0x596188: EB0A881C` = BL `0x838200`
- `0x598BEC: EA0A7DCF` = B `0x838330`

根拠: `docs/balloon_drop_action_replay.md`、`work/evidence/balloon_drop_ar_20260915.md`。


