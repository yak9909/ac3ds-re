---
id: ACNL-F0679
aliases:
- Ghidra-gpt-sol-5.6-F038
- G-F038
title: inventory completionはnative DropDataではなく非同期synthetic handle 4で十分
summary: '**確度: HIGH（UI/FieldAction構造はGhidra独立静的確認、handle 4成功経路はGhidra-gpt-sol-5.6-F032実機確認）。Ghidra-gpt-sol-5.6-F038実装自体は未実機。**'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 1682736
- 1683340
- 5860484
- 1478152
- 5871636
- 5876712
- 5848680
tags:
- inventory
supersedes: []
source: Ghidra:work/FINDINGS.md:2190-2216
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F038: inventory completionはnative DropDataではなく非同期synthetic handle 4で十分

**確度: HIGH（UI/FieldAction構造はGhidra独立静的確認、handle 4成功経路はGhidra-gpt-sol-5.6-F032実機確認）。Ghidra-gpt-sol-5.6-F038実装自体は未実機。**

Ghidra-gpt-sol-5.6-F034〜Ghidra-gpt-sol-5.6-F037で前提にしていた「custom balloonもnative DropData slotを持つべき」を撤回する。

Ghidra 12.1.3でJPN v1.5 bytesを再構築して再decompileした結果:
- `BsMenuItem_DropStart @ 0x19AD30` は `Player_DropItem` returnを単に `this+0xD8` へ保存し、-1だけ即失敗とする。
- `BsMenuItem_DropWait @ 0x19AF8C` はその値を `0x596C84` へ渡し、0/1なら待機、2なら成功、3なら失敗へ進む。
- UI側はtokenが0..3のnative slot indexであることを検証しない。
- Ghidra-gpt-sol-5.6-F032では実際にsynthetic handle 4 + 0x596C84入口hookでUI成功完了が実機確認済み。

従ってGhidra-gpt-sol-5.6-F032の唯一のcompletion欠陥は `handle 4 -> 常時2` で成功を早出ししていたこと。native queue統合ではなく:
- custom開始後 `syntheticStatus=1`
- `0x596C84(4)` はstatus 1中は1を返す
- exact custom visualの着地で `0x168E08 -> 0x599814` 完了後にstatus 2
- 次pollで2を返してstatus 0へclear
- `0x59ABE8` の同期生成失敗はstatus 3
とすれば、BsMenuItem自身の待機stateが二重dropを防ぐ。

`FgObjPresent_Update @ 0x593E68` のmode 1はvisual cleanupのみでfield persistenceを行わないため、native queue案のようにmode-1 cleanupまでinventory completionを遅延する必要もない。

custom-success pathでは `Item_PlaceItem`, `FieldAction_QueueToRecord`, `FieldAction_Dispatch`, normal action 0x0A updaterを呼ばない。実操作はhardware-verified Ghidra-gpt-sol-5.6-F032を維持する。

根拠: `docs/drop_pipeline_reanalysis.md`, `work/evidence/drop_pipeline_reanalysis_20260916.md`, scoped Ghidra export `acnl_jpn_v15_drop_reanalysis_gf038_delta.xml/.bytes`。


