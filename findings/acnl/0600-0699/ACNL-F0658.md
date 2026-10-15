---
id: ACNL-F0658
aliases:
- Ghidra-gpt-sol-5.6-F020
- G-F020
title: shared page書込み可否とActor_SetState hook到達を分離診断
summary: '**確度: HIGH（既存風船経路＋診断hook静的検証）。**'
date: '2026-09-19'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses: []
tags:
- hook
supersedes: []
source: Ghidra:work/FINDINGS.md:786-831
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F020: shared page書込み可否とActor_SetState hook到達を分離診断

**確度: HIGH（既存風船経路＋診断hook静的検証）。**

`0x01E81000` page自体は既存Ghidra-gpt-sol-5.6-F012風船経路でCPUから書込み済み:
- +0x00 worldY
- +0x04 Item
- +0x08 worldX
- +0x10..+0x18 impact Vec3
をspawn hookがSTRし、landing hookが同じ値を読んで実機で正常dropしている。

従ってGhidra-gpt-sol-5.6-F019の `+0x20..+0x44` が0のままでも、page全体がread-only/unmappedとは考えにくい。

Ghidra-gpt-sol-5.6-F020では診断を3段階に分離:

1. **AR engine write sentinel**
   - enable時に `0x01E81060 = 0xC0DEC0DE`
   - これが見えればAR direct writeは成功

2. **Actor_SetState hook CPU-write**
   - hook入口ごとに `+0x48` counter++
   - `+0x4C` last LR
   - `+0x50` last requested
   - `+0x54` last current
   - `+0x58` last desired
   - `+0x5C` last MENU_FLAGS
   - これらは条件なしで毎回更新

3. **first current=0x16 transition**
   - MENU_FLAGS条件は外した
   - current==0x16 && requested!=0x16 && marker==0 の最初の1回を +0x20..+0x44へ保存
   - +0x30 marker=1

この結果:
- +0x60も0 → AR direct write自体が見えていない/読み方の問題
- +0x60 sentinel、+0x48=0 → Actor_SetState hook未到達
- +0x48>0、+0x30=0 → Actor_SetStateは動くがcurrent=0x16から離れるtransitionは通っていない。+0x1A9 direct write等を疑う
- +0x30=1 → +0x20/+0x24で最初のstate-loss caller/stateを確定

trace hook cave:
- `0x838424-0x8384BB` 0x98 bytes
- SHA-256 `79e4235361e58523aaa6d9a71275d40f45da43c5f21bf085496fadf782899a8f`

根拠: `docs/inventory_menu.md`、`work/evidence/inventory_menu_20260915.md`。


