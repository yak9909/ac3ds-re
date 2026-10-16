# 持ち物画面（BsMenuItem）とPlayer stateの解析

対象: ACNL JPN v1.5。2026-09-15時点のGhidra/XML/bytes静的解析と実機観測。

## 結論

持ち物画面は、少なくとも2つの独立したstate machineで成立している。

1. 下画面UI側: `BsMenuItem` / `BsMenuTab` と `MENU_FLAGS (0x949D68)`
2. Player側: `Actor_SetState (0x64C688)` と `player+0x1A9` のcurrent state

実機で観測された「下画面の持ち物欄は表示されたまま、Player stateだけ `0x16 -> 0x06`」は、この2系統が同期を失った状態と一致する。

Ghidra-gpt-sol-5.6-F008版でBalloonPresentのFieldAction前半をバイパスしても症状が変わらなかったため、FieldAction type `0x21` は少なくとも単独の原因ではない。現時点では、カスタムAcBalloon生成/state遷移のどこかがPlayer側のgeneric state-normalization条件を成立させている可能性があるが、callerは未確定。

## BsMenuItem open/close

### `BsMenuItem_OpenEnter @ 0x199F9C`

`MENU_FLAGS` を読み、bit `0x10` をclear、bit `0x08` をsetしてopen開始状態にする。

### `BsMenuItem_OpenUpdate @ 0x199F44`

`this+0x1EC0` のopen process完了を待つ。完了時にbit `0x800` をclear、bit `0x10` をsetし、UI内部stateを `0x815E8C` で進める。

### `BsMenuItem_CloseEnter @ 0x19AB74`

`0x68E6E4` をcallし、bit `0x20` をclearしてclose processを開始、`this+0x1E9B = 1` とする。

### `BsMenuItem_CloseUpdate @ 0x19AAC0`

close process完了後にbits `0x08|0x10` をclearし、cleanup後に `0x815E8C` でUI内部stateを進める。

つまり、Player stateを変更しただけではBsMenuItemは閉じない。

## Lower-menu controller

`BsMenuTab_LowerMenuSwitchUpdate @ 0x6D6060` はbit `0x08` をopen-handshakeとして監視し、bit `0x10` を待ってlower-screen child UIを有効化する。

`BsMenuTab_LowerMenuSwitchEnter @ 0x6D62AC` は選択lower-tabを決定し、`Menu_RequestOpen @ 0x6D1330` へmenu IDを渡す。

`BsMenuTab_WaitMenuEndUpdate @ 0x6D7194` はbit `0x08` が立っている間menu終了待ちを続け、bit `0x08` が落ちた後にbit `0x20` をsetしてreturn-flowを開始する。

## Player state machine

`Actor_SetState @ 0x64C688` の命令列から:
- `player+0x1A9` = current state
- `player+0x1AA` = previous state

を確認した。state descriptor table baseは `0x843634`、1 entry = `0x1C` bytes。

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

`0x16 -> 0x06` は単なるflag変更ではなく、Player actor側のstate lifecycle切替である。

## stock持ち物drop経路

`FUN_0019AD30 @ 0x19AD30` は:

1. `this+0xCC` から選択slotを取得
2. `vc_GET_ITEM @ 0x723854` でItem*取得
3. action可能条件を検査
4. `Player_DropItem @ 0x596084` をcall
5. returnを `this+0xD8` に保存
6. failure (`-1`) なら `this+0xDC = 0x2E`
7. successなら `0x68E6E4` とUI内部transition (`0x815E8C`) を実行

この関数に `Actor_SetState` callはない。

`Player_DropItem @ 0x596084` 本体にも `Actor_SetState` callはない。通常dropの最終配置は `Item_PlaceItem(type=0x0A,...)`。

従ってstock inventory dropはPlayer state `0x16` を維持したまま成立する設計である。

## Inventory slot

`vc_GET_ITEM @ 0x723854` -> `Inventory_GetSlot @ 0x723878` はslot index < 16を検査し、4-byte strideでItemを返す。無効slot/itemなら `g_EmptyItem @ 0x955FF4` を返す。

## state 0x06への直接遷移候補

main static codeで `Actor_SetState(player, 6, ...)` を直接呼ぶ箇所として少なくとも:
- `0x64BDFC` in `FUN_0064BBC8`
- `0x672F40` in `FUN_00672CAC`

を確認した。

前者はgeneric field/input/safety判定後、後者は `player+0x1AB` 等を使うstate-normalization処理中にstate 6へ戻す。ただし今回の実機 `0x16 -> 0x06` がどちらから発生したか、またはindirect call経由かは未確定。

## 操作不能の説明

実機症状は:
- BsMenuItem側: `MENU_FLAGS 0x08/0x10` が維持され、lower screen UIはopen扱い
- Player側: current stateが `0x16` から `0x06` へ遷移済み

という不整合と一致する。

正規のBsMenuItem close sequenceを通っていないためUIは残る。一方Playerはinventory用state lifecycleを離れているため、入力/イベントの前提が崩れ、画面だけ残って操作不能になると判断できる。

## 次の決定的な確認

`Actor_SetState @ 0x64C688` の入口で old=`0x16` / new=`0x06` の場合だけLRを記録すれば、遷移callerを1回の実機試験で確定できる。

候補が `0x64BDFC` / `0x672F40` ならその条件を逆解析する。別LRなら、そのcallerを新たに解析する。


## Ghidra-gpt-sol-5.6-F010: drop完了tokenとinventory slot解放

ユーザー実機観測を再整理すると、問題の主症状はPlayer state変更そのものではなく:

- 足元へドラッグ&ドロップするとfield側dropは実行される
- 元Itemが持ち物slotから消えない
- ドラッグ中のItem iconがdrop直前位置で停止する
- そのままBsMenuItemが操作不能になる

である。

静的解析では、この症状を直接説明できる完了待ち経路が確認できた。

### Player_DropItemの戻り値はboolではない

`Player_DropItem @ 0x596084` は最後に `Item_PlaceItem @ 0x59E5B4` をcallし、そのreturnをそのまま返す。

`Item_PlaceItem` は `g_FieldActionSlots @ 0x9AE15C` の4 entryからfree slotを探す。

- entry count = 4
- entry stride = `0x12`
- action type = entry+`0x0E`
- status = entry+`0x0F`
- free = status 0
- allocation時 status = 1
- return = slot index `0..3`
- free slotなし = `-1`

したがって `Player_DropItem` の非負returnは「成功フラグ」ではなく、後続処理が監視するFieldAction handle/indexである。

### BsMenuItemはreturn handleを保存して待つ

`FUN_0019AD30`:
- `0x19AE2C`: `Player_DropItem(item)`
- `0x19AE34`: returnを `this+0xD8` に保存
- return == -1だけ失敗扱い
- 非負ならdrop後の待機stateへ遷移

`FUN_0019AF8C` はその待機stateで:

```
handle = this->field_D8;
status = FieldAction_PollAndFinalize(handle); // 0x596C84
```

を毎update実行する。

### status 2になるまでItemは持ち物から消えない

`0x596C84` はhandleから:

```
entry = 0x9AE15C + handle * 0x12;
status = entry[0x0F];
```

を取得する。

`FUN_0019AF8C` の処理:
- status 0/1: 何も完了処理をせずreturnし、次frameも待機
- status 3: error `0x1D` を設定してUI transition
- status 2: 成功完了処理へ進む

status 2時、通常Itemでは `0x19B034` で:

```
Inventory_SetSlot(
    inventory,
    selectedSlot,
    g_EmptyItem,   // 0x955FF4
    0,
    1
);
```

相当の処理を `0x2BFE8C` 経由で行う。

その内部 `0x322550` は実際に:

```
inventory[selectedSlot] = newItem; // 4-byte Item copy
```

を行う。

続いて:
- `0x19B0F8 -> 0x26DB1C`: 選択slotのItem icon/表示を再読込
- `0x19B110 -> 0x815E8C`: BsMenuItem内部stateを次へ遷移

まで進む。

つまり「Itemを持ち物から消す」「ドラッグ表示を更新する」「UIロックを抜ける」は、drop call直後ではなく、FieldAction handleがstatus 2になった後に実行される。

### 現行balloon ARの契約違反

現行ARのspawn hookはcustom balloon処理成功時に `r0=1` を固定returnしている。

しかしその経路では `Item_PlaceItem` を実行していないため、FieldAction slot 1をallocateしていない。

そのためBsMenuItemは:

```
this+0xD8 = 1;
status = FieldAction_PollAndFinalize(1);
```

として、custom dropとは無関係なslot 1を永久に監視する。

通常、slot 1がfreeならstatusは0なので:
- inventory slotをg_EmptyItemへ変更しない
- slot iconを更新しない
- BsMenuItem stateを進めない

という状態になる。

これは実機の「fieldにはdropされたが、元Itemが残り、ドラッグ位置でiconが固まり、操作不能になる」症状と完全に一致する。

### Player state 0x16 -> 0x06について

このcompletion-handle不整合だけで、Item残留とUI freezeは直接説明できる。

Player state `0x16 -> 0x06` が同じ原因の二次効果か、AcBalloon lifecycle側の独立した副作用かはまだ未確定。したがって、今後はまずFieldAction completion contractを正常化し、その後もstate遷移が再現するかを再評価する。

### 修正方針候補

ARは固定値1を返してはいけない。stock BsMenuItemが期待する有効なcompletion handleを返す必要がある。

静的には `Item_PlaceItem` のaction type `0x10` はslotをallocateした直後にstatusを2へ設定し、dispatchを行わずhandleを返す特殊経路を持つ。この経路を「field配置を行わないcompletion token」として利用できる可能性がある。

ただしtype 0x10の他用途・副作用はまだ実機未確認なので、現時点では修正ARへは反映していない。


## Ghidra-gpt-sol-5.6-F011実装への反映

Ghidra-gpt-sol-5.6-F010のcompletion contractに基づき、balloon ARを修正した。

旧:
```
custom drop成功
-> return 1
```

新:
```
custom開始前:
    FieldAction 4 slotsにfree entryがあるか確認
    無ければstock dropへfallback

custom balloon / falling present生成

custom成功後:
    元のItem_PlaceItem引数を復元
    Item_PlaceItem(type=0x10, ...)をcall
    -> valid FieldAction handle (0..3)
    -> entry statusは即2
    -> normal dispatchなし
    -> handleをBsMenuItemへreturn
```

これによりBsMenuItemの `this+0xD8` には実在するcompletion handleが入り、`BsMenuItem_DropWaitUpdate` はstockと同じstatus-2成功経路へ進める。

期待される結果:
- selected slotがg_EmptyItemへ置換
- drag icon再読込/消去
- BsMenuItem内部stateが進行
- inventory input lockが解除

Player state `0x16 -> 0x06` は、このcompletion修正後も再現する場合に限って独立問題として追跡する。


## Ghidra-gpt-sol-5.6-F018: stock drag/drop時のPlayer操作

### menu open

`FUN_005C1F08 @ 0x5C1F08` はlocal Playerを取得し、`player+0x1A9` を確認する。

current stateが`0x16`でなければ:
```
FUN_0065945C(player)
    -> helper/context準備
    -> Actor_SetState(player, 0x16, helper, 0)
```

したがって`0x16`は持ち物/下画面menu open時のPlayer stateとして明示的に使用される。

### drag/drop callback

`FUN_0019AD30`:
1. selected slot `this+0xCC`
2. `vc_GET_ITEM`
3. action validation
4. `Player_DropItem`
5. FieldAction handle -> `this+0xD8`
6. success時 `0x68E6E4`
7. BsMenuItem state tableを次handler `0x19C4C8` へ進める

Player state writeは無い。

### success-side 0x68E6E4

`0x68E6E4` はglobal `0x94A880` のobjectを取得して `0x1A565C` へtail-callする。

`0x1A565C` はそのobjectの:
- +0xF0 -> +0xF3
- +0x136 clear
- +0x1B2 flag processing

を行う。Player current/desired state accessは無い。

### Player_DropItem

`Player_DropItem @ 0x596084`:
- Item/field/network check
- `Drop_FindTargetTile`
- Item copy
- `Item_PlaceItem(type=0x0A,...)`

Player state setter/writeなし。

`Drop_FindTargetTile` はPlayerから向き/位置系値をreadしてtarget tileを求めるが、Player stateを書かない。

### stock FieldAction

`Item_PlaceItem` はFieldAction slotを作り、`FieldAction_InitRecord` / `FieldAction_QueueToRecord` / `FieldAction_Dispatch` を通す。

この直列経路には直接Player pointer取得、`Actor_SetState`、`player+0x1A9/+0x1AB` accessを確認していない。

### completion

通常のdrop success handler `0x19C4C8` はhandle status 2で:
- selected inventory slot -> g_EmptyItem
- slot icon refresh
- BsMenuItem UI処理
- local state transition

を行う。Player state操作は無い。

### 結論

stockでは:
```
menu open        : Player -> state 0x16
inventory drop   : Player stateは変更しない
menu open継続   : state 0x16を維持
```

よってcustom balloon後のstate 0x06はinventory drop仕様ではない。

### なぜdirect 0x16->0x06 guardが効かない可能性があるか

`Actor_SetState` はcurrent state更新後に `FUN_0067A2C8` をcallし、条件により`player+0x1AB` desired stateを書き換える。

`FUN_00672CAC` はcurrent/desiredを同期し、desiredがcurrentと異なる場合は別の`Actor_SetState`を起こす。desiredが特殊値`>=0xEB`ならstate 6へ正規化する。

したがってcustom pathが:
```
0x16 -> intermediate X
desired変更
X -> 0x06
```
なら、過去の「old=0x16/new=0x06だけ抑止」では捕捉できない。

次に観測すべきものは、menu-open中に0x16から離れる**最初のrequested stateとcaller LR**。


## Ghidra-gpt-sol-5.6-F019: first transition trace

stock drop解析から、次に必要なのは「最終的に0x06になった時」ではなく、menu-open中にPlayerが最初に0x16から離れる瞬間の特定。

現行診断ARは `Actor_SetState @ 0x64C688` を観測専用hookする。

条件:
```
MENU_FLAGS & 0x08
&& current == 0x16
&& requested != 0x16
&& trace_marker == 0
```

成立時だけ以下を保存:
- +0x20 caller LR
- +0x24 requested state
- +0x28 current state
- +0x2C desired state
- +0x30 marker=1
- +0x34 previous state
- +0x38 Player*
- +0x3C r2
- +0x40 r3
- +0x44 MENU_FLAGS

その後はstock `Actor_SetState+4` へ復帰するため、state遷移は一切抑止しない。

これにより `0x16 -> X -> 0x06` のXとそのcallerを1回の実機dropで確定できる。


## Ghidra-gpt-sol-5.6-F020: shared page / hook到達の三段階診断

`0x01E81000` pageは既存の風船drop経路でCPU書込みに成功しているため、`+0x20..`が0でもpage全体が書込不可とは判断しない。

現行診断:
- `+0x60 = 0xC0DEC0DE`: AR engine direct-write sentinel
- `+0x48`: Actor_SetState hook entry count
- `+0x4C`: last caller LR
- `+0x50`: last requested state
- `+0x54`: last current state
- `+0x58`: last desired state
- `+0x5C`: last MENU_FLAGS

first transition traceは`MENU_FLAGS`条件を外し、
```
current == 0x16
requested != 0x16
marker == 0
```
だけで`+0x20..+0x44`へ保存する。

結果の読み方:
- sentinelなし: direct AR write/read issue
- sentinelあり、entry count 0: Actor_SetState hook未到達
- entry count >0、marker 0: 0x16から離れる処理はActor_SetStateを通っていない
- marker 1: first transitionを捕捉


## Ghidra-gpt-sol-5.6-F021: traceをAR自身が消していた問題の修正

Ghidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020では、診断用に`0x01E81020..`を0へ初期化する通常writeをONコードへ置いていた。

CTRPFの通常writeはコード有効中に繰り返し適用されるため、CPU hookが値を書いてもすぐ0に戻る。このため過去のtrace=0は「hook未到達」を意味しない。

現行方式:
- trace領域はAR側から一切clearしない
- Actor_SetState hook実行時に`+0x48=0xA57A7E01`
- last LR/requested/current/desired/MENU_FLAGSを`+0x4C..+0x5C`
- current=0x16かつrequested!=0x16なら`+0x30=0x16F1A57E`と`+0x20..+0x44`へcontext保存

初期値/marker=0に依存しないため、AR連続実行と競合しない。

`+0x60=0xC0DEC0DE`のみ、trace領域外のdirect-write sentinelとして常時書込を維持する。


## Ghidra-gpt-sol-5.6-F022: state 0x06の前段はAcBalloon terminal dropのPlayer state 0xA4 reaction

実機trace:
- LR `0xBFCCE0`
- requested `0xA4`
- current `0x16`
- desired `0x06`
- previous `0x06`

ModuleVillage.croのrelocation/importを逆引きすると:
- runtime base `0xBE3000`
- callsite runtime `0xBFCCDC`
- CRO file `0x19CDC`
- LR file `0x19CE0`

このcallsiteはAcBalloon terminal drop `file 0x19BA8` 内。

直前:
```
MOV   r0,#0x240
LDRSB r0,[r4,r0]       // AcBalloon+0x240
BL    import_stub_0xDF8
```

stub `0xDF8` はmain `0x5C5A30` をimportする。

main:
`0x5C5A30` -> local Player取得 -> tail `0x6830D4`

`0x6830D4`:
- state context取得
- param -> context+0x0E
- `r1=0xA4`
- `Actor_SetState`へtail branch

従ってcustom風船がinventory stateを壊す原因は、風船drop時のstock Player reaction state A4。

desiredは0x06のままなので:
```
0x16 -> 0xA4 -> 0x06
```
となる。

### Ghidra-gpt-sol-5.6-F022 fix

custom state1同期call中はshared+0x0C=1なので、`0x5C5A30`のみhook:

（疑似C を省略。原本は _local/legacy-src/…）

Actor_SetState全体はhookしない。

自然風船はarmed=0なのでstock reactionを維持する。
