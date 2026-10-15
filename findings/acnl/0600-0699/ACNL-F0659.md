---
id: ACNL-F0659
aliases:
- Ghidra-gpt-sol-5.6-F021
- G-F021
title: trace領域をARで0固定していたためGhidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020 traceは観測不能だった
summary: '**確度: HIGH（AR実行モデルと現行コードの直接確認）。**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses: []
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:832-873
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F021: trace領域をARで0固定していたためGhidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020 traceは観測不能だった

**確度: HIGH（AR実行モデルと現行コードの直接確認）。**

Ghidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020ではAR本体に:
```
01E81020 00000000
...
01E8105C 00000000
```
を置いていた。CTRPFの通常writeはコード有効中に継続適用されるため、CPU hookがtrace値を書いても次のAR更新で0へ戻される。

従って「+0x20..+0x44が0のまま」という実機結果から、hook未到達やpage書込不可を推論することはできなかった。

Ghidra-gpt-sol-5.6-F021でtrace領域へのAR-side clearを全面廃止。

初期値に依存しない診断方式へ変更:
- `shared+0x48 = 0xA57A7E01`: Actor_SetState hookが1回でも実行されたことを示すmagic
- `shared+0x4C`: last caller LR
- `shared+0x50`: last requested state
- `shared+0x54`: last current state
- `shared+0x58`: last desired state
- `shared+0x5C`: last MENU_FLAGS

current==0x16 && requested!=0x16を観測した場合:
- `shared+0x30 = 0x16F1A57E`
- `+0x20..+0x44` にtransition contextを保存

markerの事前clearは不要で、matching transitionごとに最新値へ上書きする。

`shared+0x60 = 0xC0DEC0DE` はtrace領域外のAR direct-write sentinelとして継続使用。これは常時writeでも問題ない。

trace hook:
- `0x838424-0x8384B3`
- size `0x90`
- SHA-256 `ffdb386d701b2e0f4a38052aab2d2acd80129527d618db1def0e82f052008fc3`

**重要:** Ghidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020でtrace領域が0だった実機結果は無効。Ghidra-gpt-sol-5.6-F021以降のbuildで再取得が必要。

根拠: `docs/inventory_menu.md`、`work/evidence/inventory_menu_20260915.md`。


