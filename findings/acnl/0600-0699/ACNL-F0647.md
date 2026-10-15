---
id: ACNL-F0647
aliases:
- Ghidra-gpt-sol-5.6-F009
- G-F009
title: 持ち物画面はBsMenuItem UI stateとPlayer state 0x16の二重state machineで成立する
summary: '**確度: HIGH（添付Ghidra XML/bytesの独立静的解析＋実機state観測）。state 0x16→0x06のcallerだけ未確定。**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 9739624
- 1679260
- 1679172
- 1682292
- 1682112
- 7168096
- 7172500
- 6604424
- 8664628
- 8665244
- 6851060
- 6865556
- 6841280
- 6816112
- 8664796
- 8066088
- 6856536
- 6819192
- 6768576
- 7485524
tags:
- inventory
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:147-213
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F009: 持ち物画面はBsMenuItem UI stateとPlayer state 0x16の二重state machineで成立する

**確度: HIGH（添付Ghidra XML/bytesの独立静的解析＋実機state観測）。state 0x16→0x06のcallerだけ未確定。**

### UI側

`MENU_FLAGS = 0x949D68` をBsMenuItem/BsMenuTabが共有する。

- `BsMenuItem_OpenEnter @ 0x199F9C`: bit 0x10 clear、bit 0x08 set。
- `BsMenuItem_OpenUpdate @ 0x199F44`: open処理完了後にbit 0x10 set。
- `BsMenuItem_CloseEnter @ 0x19AB74`: close要求bit 0x20をclearしてclose処理開始。
- `BsMenuItem_CloseUpdate @ 0x19AAC0`: close完了後にbits 0x08|0x10をclear。
- `BsMenuTab_LowerMenuSwitchUpdate @ 0x6D6060`: bit 0x08/0x10をlower-menu handshakeとして消費。
- `BsMenuTab_WaitMenuEndUpdate @ 0x6D7194`: bit 0x08が落ちるまで待ち、その後bit 0x20をsetしてreturn flowへ進む。

このUI lifecycleはPlayer state byteとは独立している。

### Player側

`Actor_SetState @ 0x64C688` の命令列から:

- `player+0x1A9` = current state
- `player+0x1AA` = previous state

を確認。state descriptor table baseは `0x843634`、strideは `0x1C`。

state `0x16` descriptor @ `0x84389C`:
- enter `0x6889F4`
- update `0x68C294`
- exit `0x6863C0`
- event `0x680170`

state `0x06` descriptor @ `0x8436DC`:
- enter `0x7B1428`
- update `0x689F58`
- exit `0x680D78`
- event `0x6747C0`

従って0x16→0x06はinventory UI flagの変更ではなく、Player側の正式なstate transitionとして扱うべきである。

### stock inventory drop

`FUN_0019AD30` は `this+0xCC` の選択slotから `vc_GET_ITEM @ 0x723854` でItem*を取得し、`0x19AE2C` で `Player_DropItem @ 0x596084` を直接呼ぶ。成功後は `0x68E6E4` とUI-local transition `0x815E8C` を進めるだけで、`Actor_SetState` を直接呼ばない。

`Player_DropItem` 本体にも `Actor_SetState` callはなく、stock最終配置は `Item_PlaceItem(type=0x0A,...)`。

従って **通常の持ち物dropはPlayer state 0x16を維持したまま成立する**。

### 操作不能の説明

実機症状は:
- BsMenuItem側: MENU_FLAGS 0x08/0x10が残り、UIはopen扱い
- Player側: current stateだけ0x06へ遷移

というstate desynchronizationと一致する。正規 `CloseEnter -> CloseUpdate` を通らないため下画面は残り、Playerだけinventory用state lifecycleを離れる。

main static codeで `Actor_SetState(player,6,...)` の直接callは少なくとも:
- `0x64BDFC` in `FUN_0064BBC8`
- `0x672F40` in `FUN_00672CAC`

を確認したが、今回どちらが発火しているかは未確定。

**次の決定的検証:** `Actor_SetState` 入口で old=0x16 / new=0x06 の場合だけLRを記録する。これで1回の実機dropからstate reset callerを確定できる。

根拠: `docs/inventory_menu.md`、`work/evidence/inventory_menu_20260915.md`、`artifacts/exchange/ghidra/acnl_jpn_v15_inventory_delta.xml`。


