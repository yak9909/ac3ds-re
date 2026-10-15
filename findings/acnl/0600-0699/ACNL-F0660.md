---
id: ACNL-F0660
aliases:
- Ghidra-gpt-sol-5.6-F022
- G-F022
title: AcBalloon terminal dropがPlayer state 0xA4 reactionを明示要求し、desired=0x06へ戻る
summary: '**確度: HIGH（実機trace＋ModuleVillage.cro＋main static call chainが一致）。**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 9959068
- 6052400
- 6828244
- 6604424
- 6052404
tags:
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:874-978
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F022: AcBalloon terminal dropがPlayer state 0xA4 reactionを明示要求し、desired=0x06へ戻る

**確度: HIGH（実機trace＋ModuleVillage.cro＋main static call chainが一致）。**

Ghidra-gpt-sol-5.6-F021 traceの実機値:
- caller LR = `0x00BFCCE0`
- requested state = `0xA4`
- current state = `0x16`
- desired state = `0x06`
- previous state = `0x06`
- Player* = `0x33099E3C`
- r2 = `0x0097F69C`
- r3 = 0
- MENU_FLAGS = `0x081C`

したがって最初のstate lossはdirect `0x16 -> 0x06` ではなく **`0x16 -> 0xA4`**。

### CRO caller特定

IDA branchの `ModuleVillage.cro` をCRO relocation table込みで解析。

main helper `0x5C5A30` のstatic export tagは `0x4C5A300`。ModuleVillage anonymous import index 314がこれをimportし、import stub literal:
- CRO file `0xDFC`
- stub entry `0xDF8`

へresolveされる。

stub `0xDF8` へのARM branch xrefはCRO内で一意:
- call file `0x19CDC`
- LR file `0x19CE0`

実機LRとの差:
```
0x00BFCCE0 - 0x00019CE0 = 0x00BE3000
```
なので、実機ModuleVillage load baseは `0xBE3000`。callsite runtimeは `0xBFCCDC` でtraceと完全一致。

### terminal drop内の命令

ModuleVillage file `0x19BA8` 近傍のterminal drop処理で、Item生成/落下処理後:

```
0x19CD4  MOV   r0,#0x240
0x19CD8  LDRSB r0,[r4,r0]     ; AcBalloon+0x240 parameter
0x19CDC  BL    import_stub_0xDF8
0x19CE0  MOV   r0,r4
```

import stubはmain `0x5C5A30`。

### main側call chain

`0x5C5A30`:
- local Playerを取得
- AcBalloon由来paramをr1へ保持
- `0x6830D4` へtail-branch

`0x6830D4`:
- Player state context/helperを取得
- AcBalloon由来paramをcontext+0x0Eへ保存
- r2=context
- r3=0
- **r1=0xA4**
- `Actor_SetState @ 0x64C688` へtail-branch

従ってstate `0xA4` はAcBalloon terminal dropがPlayerへ要求するreaction stateと判断できる。

trace時点でdesired `player+0x1AB=0x06`、previous=0x06なので:
```
menu open: current=0x16, desired=0x06, previous=0x06
AcBalloon terminal drop: 0x16 -> 0xA4
subsequent desired/current sync: 0xA4 -> 0x06
```
が観測症状を説明する。

### Ghidra-gpt-sol-5.6-F022修正

custom balloon helperはstate1を同期callする間だけ `shared+0x0C=1` にしている。

main `0x5C5A30` をhookし:
```
if (shared.armed == 1)
    return;        // custom inventory balloon: skip Player A4 reaction

// natural balloon / all stock cases
original PUSH {r4,lr}
continue 0x5C5A34
```

とする。

これにより:
- custom inventory dropだけA4 reactionを発生させない
- 自然風船はarmed=0なのでstock Player reaction維持
- Actor_SetState全体をhookしない
- inventory/menu state machineへ一般的な副作用を入れない

guard cave:
- `0x838424-0x838443`, 0x20 bytes
- hook `0x5C5A30 -> 0x838424`: `EA09CA7B`
- stock continuation `0x838438 -> 0x5C5A34`: `EAF6357D`

根拠: `docs/inventory_menu.md`、`docs/balloon_drop_action_replay.md`、`work/evidence/inventory_menu_20260915.md`、`work/evidence/balloon_drop_ar_20260915.md`。


