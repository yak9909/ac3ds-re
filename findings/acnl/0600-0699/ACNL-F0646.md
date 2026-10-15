---
id: ACNL-F0646
aliases:
- Ghidra-gpt-sol-5.6-F008
- G-F008
title: カスタム風船drop中にinventory Player stateが0x16→0x06へ遷移する
summary: '**確度: HIGH（実機挙動）。旧FieldAction原因仮説は棄却。**'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 5876712
tags:
- inventory
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:132-146
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F008: カスタム風船drop中にinventory Player stateが0x16→0x06へ遷移する

**確度: HIGH（実機挙動）。旧FieldAction原因仮説は棄却。**

Ghidra-gpt-sol-5.6-F007移設版は実機でクラッシュせず、通常dropから風船生成→プレゼント落下まで成功した。

ただし持ち物画面を開いたままdropすると、Player current stateが `0x16 -> 0x06` に遷移し、下画面の持ち物UIは表示されたまま操作不能になる。

FieldAction type `0x21` の登録/dispatchを省略し、`BalloonPresent_CreateAtTile (0x59ABE8)` を直接呼ぶGhidra-gpt-sol-5.6-F008試作でも同じ症状が再現した。従って **FieldAction経路は少なくとも単独原因ではない**。旧「FieldActionがstateを壊す」という原因帰属は棄却する。

現行ARは調査用として残すが、次の修正はGhidra-gpt-sol-5.6-F009でPlayer/menu state同期経路を特定してから行う。

根拠: `docs/inventory_menu.md`、`work/evidence/inventory_menu_20260915.md`。


