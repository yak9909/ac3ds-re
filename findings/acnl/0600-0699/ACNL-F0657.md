---
id: ACNL-F0657
aliases:
- Ghidra-gpt-sol-5.6-F019
- G-F019
title: menu-open中にstate 0x16から離れる最初のActor_SetStateを記録する診断AR
summary: '**確度: HIGH（hook構造/ABI静的検証。実機値取得待ち）。**'
date: '2026-09-19'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 6604424
- 6604428
tags:
- menu
supersedes: []
source: Ghidra:work/FINDINGS.md:741-785
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: superseded
consolidated_into: ''
duplicate_of: ''
superseded_by: ACNL-F0659
---
## Ghidra-gpt-sol-5.6-F019: menu-open中にstate 0x16から離れる最初のActor_SetStateを記録する診断AR

**確度: HIGH（hook構造/ABI静的検証。実機値取得待ち）。**

Ghidra-gpt-sol-5.6-F018でstock inventory drop自体はPlayer stateを変更せず、custom balloon pathがstate lossを導入していることを確認した。これまでのguardは `0x16 -> 0x06` を直接想定していたが、`Actor_SetState` 後処理とdesired-state同期により `0x16 -> X -> 0x06` の可能性がある。

Ghidra-gpt-sol-5.6-F019ではstate抑止を完全に外し、`Actor_SetState @ 0x64C688` の入口で以下を満たす**最初の1回だけ**記録する:

- `MENU_FLAGS & 0x08 != 0`
- current `player+0x1A9 == 0x16`
- requested `r1 != 0x16`
- trace marker `shared+0x30 == 0`

記録後はmarker=1とし、transition自体はstock処理へそのまま通す。

shared trace map:
- `0x01E81020`: caller LR
- `0x01E81024`: requested new state (r1)
- `0x01E81028`: old current state (+0x1A9)
- `0x01E8102C`: desired state (+0x1AB)
- `0x01E81030`: trace marker (0/1)
- `0x01E81034`: previous state (+0x1AA)
- `0x01E81038`: Player*
- `0x01E8103C`: Actor_SetState r2
- `0x01E81040`: Actor_SetState r3
- `0x01E81044`: MENU_FLAGS snapshot

hook cave:
- `0x838424-0x83849F`: trace hook body + literals
- `0x8384A0-0x8384A3`: explicit padding in AR E-block
- `0x8384A4-0x8384FF`: unused
- `0x838500-`: existing replacement strings

`Actor_SetState` hook:
- `0x64C688 -> 0x838424`: `EA07AF65`

trace hook first executes the stock prologue `PUSH {r4-r12,lr}`, then inspects/records using saved callee registers, and finally `LDR pc,=0x64C68C` to resume the untouched stock function body.

AR activation clears all trace slots `+0x20..+0x44` before installing hooks.

**実機で必要な値:** 1回custom dropした直後の `0x01E81020..0x01E81044`。特にLRとrequested stateで最初のstate-loss callerを確定できる。

根拠: `docs/inventory_menu.md`、`work/evidence/inventory_menu_20260915.md`。


