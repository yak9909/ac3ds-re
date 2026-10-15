---
id: ACNL-F0651
aliases:
- Ghidra-gpt-sol-5.6-F013
- G-F013
title: custom balloon drop中のinventory state 0x16→0x06をmenu-open guardで抑止する
summary: '**確度: MEDIUM（静的検証済み、実機未検証）。**'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: Ghidra
addresses:
- 6602236
- 6762304
- 9739624
- 6604424
- 6604428
tags:
- menu
- inventory
supersedes: []
source: Ghidra:work/FINDINGS.md:349-402
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F013: custom balloon drop中のinventory state 0x16→0x06をmenu-open guardで抑止する

**確度: MEDIUM（静的検証済み、実機未検証）。**

Ghidra-gpt-sol-5.6-F012でinventory completion契約は実機上正常化し、連続dropも可能になった。一方、custom balloon drop後にPlayer current stateが依然 `0x16 -> 0x06` へ遷移する。

静的に `Actor_SetState(player,6,...)` の直接callsiteとして少なくとも:
- `0x64BDFC`
- `0x672F40`
を確認しているが、実機でどちらが発火しているかは未確定。

Ghidra-gpt-sol-5.6-F013では原因callerを限定せず、custom drop中かつ下画面メニューがopenの間だけ `Actor_SetState` 入口で遷移を抑止する。

shared page:
- `+0x1C`: inventory-state guard
- `+0x20`: 最後に抑止した `Actor_SetState` caller LR（診断用）

custom actor state helperを呼ぶ直前、`MENU_FLAGS @ 0x949D68` のbit `0x08` がsetならguard=1。

`Actor_SetState @ 0x64C688` hook:
- guard != 1 → stock
- menu-open bit 0x08 == 0 → guard clearしてstock
- new state != 6 → stock
- current state != 0x16 → stock
- それ以外 → LRをshared+0x20へ保存し、`r0=1` でreturnしてstate transitionを実行しない

従って抑止範囲は「custom balloon dropでguardが立っている」「menuがまだopen」「0x16→0x06」の組合せだけ。

メニューが正規に閉じてbit 0x08が落ちれば、次のActor_SetState callでguardをclearし、通常のstate transitionをそのまま通す。

既存のdead cave `0x838080-0x838137` は添付XMLでNOP化済み・参照なしと確認されており、Ghidra-gpt-sol-5.6-F013で:
- `0x838080-0x8380B7`: guard-arm wrapper
- `0x8380C0-0x838117`: Actor_SetState guard hook
として再利用。

hooks:
- `0x64C688 -> 0x838464`: `EA07AF75`
- stock continuation: `0x8384B0 -> 0x64C68C`: `EAF85075`
- custom helper wrapper: `0x8382E4 -> 0x838080`: `EBFFFF65`

wrapper cave SHA-256:
`4c348767f7aa76d0218a302d3a0a5dc701c6ae00db85f6b219ab18664c13cb79`

main balloon cave SHA-256:
`83a15c55008d8c4f312de60e28d1f0a5aa835ff15f1fc4cee9b279acf06aa0d5`

combined two-cave SHA-256:
`cf60fa8b93498982cd976137db5068de4d27dea881512a256b9af0a96eae0aa0`

**実機確認項目:** state 0x16が維持されるか、inventory継続操作、メニューを閉じた後に通常stateへ戻れるか。

根拠: `docs/balloon_drop_action_replay.md`、`docs/inventory_menu.md`、`work/evidence/balloon_drop_ar_20260915.md`。


