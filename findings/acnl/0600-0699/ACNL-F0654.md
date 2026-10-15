---
id: ACNL-F0654
aliases:
- Ghidra-gpt-sol-5.6-F016
- G-F016
title: custom guard依存を廃止し、menu-open中の0x16→0x06を直接抑止する
summary: '**確度: MEDIUM（静的検証済み、実機未検証）。**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: Ghidra
addresses:
- 6604700
- 6870980
- 1682112
- 7172500
- 6604424
- 6604428
tags:
- menu
supersedes: []
source: Ghidra:work/FINDINGS.md:520-569
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F016: custom guard依存を廃止し、menu-open中の0x16→0x06を直接抑止する

**確度: MEDIUM（静的検証済み、実機未検証）。**

Ghidra-gpt-sol-5.6-F015 early-arm版でも実機ではdrop後にPlayer stateが0x06へ遷移した。したがってcustom shared guardのarm timingだけでは説明できない。

本体.textをARM命令パターンで全scanし、即値offset `#0x1A9` への `STRB` は22箇所確認した。このうちPlayer state-machine領域で通常state遷移に使われるのは:
- `0x64C79C` in `Actor_SetState`
- `0x68D7C4` in Player初期化/constructor系
が明確。後者はcurrent/previous state初期化とdesired state=6の設定であり、通常drop時のruntime transition経路ではない。

またstock menu close:
- `BsMenuItem_CloseUpdate @ 0x19AAC0` がclose完了後に `MENU_FLAGS` bits 0x08|0x10をclear
- `BsMenuTab_WaitMenuEndUpdate @ 0x6D7194` はbit 0x08がclearされるまでreturn flowへ進まない

ため、menuが開いている間のcurrent 0x16 -> requested 0x06を拒否し、bit 0x08が落ちた後はstock transitionを許可する設計がstate-machine semanticsと整合する。

Ghidra-gpt-sol-5.6-F016ではshared+0x1C guardを廃止。

`Actor_SetState @ 0x64C688` hook:
- `MENU_FLAGS & 0x08 == 0` -> stock
- requested state `r1 != 6` -> stock
- current state `[r0+0x1A9] != 0x16` -> stock
- 上記3条件成立時のみ:
  - caller LRを `shared+0x20` に記録
  - `r0=1` でreturn
  - state transitionを実行しない

stock pathは元prologue `PUSH {r4-r12,lr}` を実行し、literal PC loadで `0x64C68C` へ復帰。

guard cave:
- `0x838424-0x838473` (0x50 bytes; final word is padding)
- `0x838470-0x8384FF` unused
- `0x838500-` existing replacement strings

hook:
- `0x64C688 -> 0x838424`: `EA07AF65`

balloon/synthetic-completion caveはGhidra-gpt-sol-5.6-F012へ戻し、custom guard wrapperは削除。

hashes:
- guard cave: `2995fa6ffaf19ca981d2d74b73f2c986363a708cc549c0898be1138e1a235936`
- main balloon cave: `9ecc906c807c162fb7ccecc3b31a8b1d5a99a8d944a790d7e22ddfe9751131d7`
- concatenated: `e9a7c2bde901378b807e13f86519cefaf75d82a6fca85238fa4848cdc2651433`

**実機未確認:** drop後state 0x16維持、menu close後0x06への正常復帰。

根拠: `docs/balloon_drop_action_replay.md`、`work/evidence/balloon_drop_ar_20260915.md`。


