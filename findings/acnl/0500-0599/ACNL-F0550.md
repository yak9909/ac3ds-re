---
id: ACNL-F0550
aliases:
- IDA-gpt-6-astra-F002
title: 木1体の専用材質で透明度変更（2026-09-20、HIGH）
summary: '解析ソフト: IDA / 解析モデル: gpt-6-astra。ゲームのcopy関数0x4ADD44(mask0x800)で専用ResMaterialを作りMaterial+80をredirect。SimpleMaterialActivator0x4A17B8はMaterial+8のみを読むので、それだけでは無効。このinstanceのRTTI/vtable4slotを複製しActivateだけgeneric0x49C08Cへ替えると、constant-alpha RGB b'
date: '2026-09-20'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4906308
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4112-4117
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-astra-F002: 木1体の専用材質で透明度変更（2026-09-20、HIGH）

解析ソフト: IDA / 解析モデル: gpt-6-astra。ゲームのcopy関数0x4ADD44(mask0x800)で専用ResMaterialを作りMaterial+80をredirect。SimpleMaterialActivator0x4A17B8はMaterial+8のみを読むので、それだけでは無効。このinstanceのRTTI/vtable4slotを複製しActivateだけgeneric0x49C08Cへ替えると、constant-alpha RGB blendで255/128/0の不透明/半透明/消失を実見した。元TEV/alpha testを保持し葉の切抜きを維持。shared resource hashは不変、OFFで元source/vtableを復元。一般の半透明材質へのalpha乗算や奥行きソートは未確認。

根拠: `work/evidence/models3d/alpha_screen_20260920/` の `generic_activate_asm.json`、`copy_asm.json`、`generic{128,0,255}.png`、`reboot1/final_restored_state.json`。詳細 [alpha_screen_plan](../docs/topics/alpha_screen_plan.md)。**旧IDA-unknown-F024の「描画状態はコード側に無い」「DrawMesh末尾がMTOBを流すだけ」は不正確。MaterialActivatorが材質コマンドを別途emitする。** メッシュのdraw listだけから現在のblendを断定しない。反証条件: 別activator/材質でこのsourceを読まない、元資源が変わる、alpha変更で他instanceも変化する。

