---
id: ACNL-F0656
aliases:
- Ghidra-gpt-sol-5.6-F018
- G-F018
title: stock inventory dropはPlayer stateを変更しない。state 0x16はmenu open時に明示設定される
summary: '**確度: HIGH（main .textのcall chainを入口からcompletionまで静的追跡）。**'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 6037256
- 6039512
- 6789704
- 6657116
- 1682736
- 7485524
- 1682988
- 5857412
- 6874852
- 1688776
- 9742464
- 1726044
- 5863908
- 5891508
- 5896812
- 5893096
- 5892344
- 5860484
- 2546460
- 1684324
tags:
- menu
- inventory
- player
supersedes: []
source: Ghidra:work/FINDINGS.md:585-740
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F018: stock inventory dropはPlayer stateを変更しない。state 0x16はmenu open時に明示設定される

**確度: HIGH（main .textのcall chainを入口からcompletionまで静的追跡）。**

ユーザー指示に基づき、AR側から逆算せず、持ち物画面のdrag/dropからPlayerへ行われる操作をstock経路で再解析した。

### 1. menu open時にPlayer state 0x16を明示設定

`FUN_005C1F08 @ 0x5C1F08`:
- local Playerを `GET_PLAYER @ 0x5C27D8` で取得
- `player+0x1A9` を読む
- current stateが `0x16` なら何もしない
- それ以外では `0x679A48` の後に `FUN_0065945C @ 0x65945C` をcall

`FUN_0065945C` はhelper/contextを準備後、tail-callで:

```
Actor_SetState(player, 0x16, helper, 0)
```

を実行する。

従ってPlayer state `0x16` は実際に持ち物/下画面menuを開く際に設定されるPlayer stateである。

### 2. inventory drag/drop callbackはPlayer_DropItemを呼ぶだけ

`FUN_0019AD30 @ 0x19AD30`:
- `this+0xCC` のselected slotを読む
- `vc_GET_ITEM @ 0x723854` でItem*取得
- action可否を検査
- `0x19AE2C`: `Player_DropItem @ 0x596084`
- return handleを `this+0xD8` へ保存
- success時 `FUN_0068E6E4 @ 0x68E6E4`
- BsMenuItem state tableを+0x60へ進め、次handler `0x19C4C8` を設定

このcallbackにはPlayer pointer取得、`Actor_SetState`、`player+0x1A9/+0x1AB` writeは無い。

### 3. success直後の0x68E6E4はPlayerではなくcamera系

`FUN_0068E6E4` はglobal `0x94A880` をdereferenceし、存在すれば `0x1A565C` へtail-call。

XML上 `0x94A880` はcamera系globalとして既知。 `0x1A565C` は:
- object+0xF0 -> +0xF3 copy
- +0x136 clear
- +0x1B2 flags処理

を行う。

Player current/desired stateへのaccessはない。

### 4. Player_DropItemはPlayer stateを書かない

`Player_DropItem @ 0x596084` は:
- Item/network/field条件検査
- `Drop_FindTargetTile @ 0x5979E4`
- Item temp copy
- stock最終処理 `Item_PlaceItem(type=0x0A,...)`

を行う。

`Actor_SetState` callも `player+0x1A9/+0x1AB` writeも無い。

`Drop_FindTargetTile` はlocal Playerを取得するが、Player側について確認できるのは:
- `player+0x2E` read
- `player+0x14` を位置/衝突系helperへ渡す
などのtarget tile計算用readであり、state writeは無い。

### 5. stock FieldAction作成/dispatchにも直接Player state操作なし

`Item_PlaceItem @ 0x59E5B4` はFieldAction slotをallocateし、recordを構築して:
- `FieldAction_InitRecord @ 0x59FA6C`
- `FieldAction_QueueToRecord @ 0x59EBE8`
- `FieldAction_Dispatch @ 0x59E8F8`

を通す。

この直列経路でPlayer pointer取得、`Actor_SetState`、`+0x1A9/+0x1AB` accessは確認できない。

従ってstock inventory dropのfield placementはPlayer stateを直接変更する処理ではない。

### 6. drop completionもinventory/UIだけを更新

stock success後のhandler `FUN_0019C4C8 @ 0x19C4C8` は:
- `this+0xD8` handleを `FieldAction_PollAndFinalize @ 0x596C84` でpoll
- status 2でselected inventory slotを `g_EmptyItem` へ変更
- `0x26DB1C` でslot icon refresh
- `0x19B364` のUI処理
- `0x815E8C` でBsMenuItem local state遷移
- `0x117AD0` へtail branch

を行う。

ここにもPlayer state操作は無い。

### 7. stock Player stateの不変条件

以上からstockの持ち物dropは:

```
menu open:
    Actor_SetState(Player, 0x16)

drag/drop:
    Playerはtarget tile計算でreadされるだけ
    Player_DropItem / Item_PlaceItem
    FieldAction completion
    inventory slot clear / UI refresh

menu remains open:
    Player state 0x16を維持
```

という構造。

したがってcustom balloon drop後のstate 0x06はstock inventory dropの一部ではなく、**custom-only AcBalloon lifecycleが導入した副作用**。

### 8. direct 0x16->0x06抑止が効かなかった理由の有力経路

`Actor_SetState` はcurrent state更新後に `FUN_0067A2C8 @ 0x67A2C8` をcallする。この関数は条件により `player+0x1AB`（desired/target state）を書き換える。

`FUN_00672CAC @ 0x672CAC` はcurrent/desired synchronizer:
- desired `player+0x1AB` を読む
- current != desiredなら `Actor_SetState(player, desired,...)`
- desiredが特殊値 `>=0xEB` の場合はcurrent !=6なら `Actor_SetState(player,6,...)`

を実行する。

従って実際のcustom経路が:

```
0x16 -> intermediate state X
       ↓
desired state更新
       ↓
X -> 0x06
```

なら、Ghidra-gpt-sol-5.6-F013..G-F016の「current==0x16 && new==0x06だけ抑止」は捕捉できない。

このモデルは、複数のdirect-0x06 guardが実機で効かなかった事実と整合する。

### 次の決定的検証

menu-open中、`Actor_SetState` 入口で **current==0x16から離れる最初のtransitionを、new stateに関係なく記録**する。

記録候補:
- `shared+0x20` = caller LR
- `shared+0x24` = requested new state
- `shared+0x28` = current state
- `shared+0x2C` = desired state (`player+0x1AB`)

これでcustom balloon処理が最初にPlayerをどのstateへ遷移させているかを確定できる。

根拠: `docs/inventory_menu.md`、`work/evidence/inventory_menu_20260915.md`。


