# Ghidra-gpt-sol-5.6-F039 — 風船ドロップ再設計（独立二系統検証後）

Status: **design only**。この文書ではAR payloadを作成しない。

対象: ACNL JPN v1.5 / CTRPluginFramework Action Replay。  
基準実装: **Ghidra-gpt-sol-5.6-F032 hardware-verified**。

## 1. 目的

Ghidra-gpt-sol-5.6-F032で実機確認済みの以下を壊さず、残っている「completionを早く返しすぎる」問題だけを修正する。

- 選択したinventory Itemが風船から落ちる。
- 0x21系のfalling-present visualだけが表示される。
- 着地後、同じItemがfieldへ残る。
- Player state 0x16を維持する。
- inventory UIが正常に成功完了する。

Ghidra-gpt-sol-5.6-F034〜Ghidra-gpt-sol-5.6-F037で試したnative DropData統合は採用しない。

## 2. 再解析で確定した処理系の分離

### 2.1 Inventory UI completion

`BsMenuItem_DropStart @ 0x19AD30` は `Player_DropItem @ 0x596084` のreturnを `BsMenuItem+0xD8` に保存し、`-1` だけ即失敗とする。UI側に `0..3` の範囲検査はない。

`BsMenuItem_DropWait @ 0x19AF8C`:

```text
result = DropQueue_PollAndFinalize(handle)
0/1 -> wait
2   -> stock success: inventory source消去 / icon refresh / UI state advance
3   -> stock failure
```

UIが必要とするのは「opaque completion token + poll result contract」である。

### 2.2 Normal inventory drop

stock:

```text
Player_DropItem
  -> Drop_FindTargetTile
  -> Item_PlaceItem(type 0x0A)
       -> DropData allocate
       -> State=1
       -> FieldAction record build
       -> FieldAction dispatch
  -> native handle 0..3
```

`Item_PlaceItem @ 0x59E5B4` はqueue allocator APIではない。slot確保直後にnormal-drop FieldActionを開始する。custom balloonでcompletion token確保だけに使ってはいけない。

### 2.3 Natural AcBalloon landing

ModuleVillage terminal処理はmain `BalloonPresent_TryLandAndPlace @ 0x598BEC` を呼ぶ。

valid landing:

```text
FieldAction_RegisterActive(type 0x21)
FieldAction_InitRecord
BalloonPresent_BuildRecord(type 0x21)
FieldAction_SendOrDispatch
BalloonPresent_CreateAtTile
```

inventory DropDataはallocateしない。

従って以下は別lifecycleである。

1. inventory DropData/UI completion
2. normal drop FieldAction 0x0A
3. natural balloon FieldAction 0x21

## 3. 二系統検証で見つかった旧説明の矛盾

旧記録には次の2つが共存していた。

- Ghidra-gpt-sol-5.6-F025系: terminal A4 reactionはcustom state helper return後に発生した、という説明。
- Ghidra-gpt-sol-5.6-F027系: `BalloonPresent_TryLandAndPlace` はcustom state helper内で同期発火した、という説明。

しかしraw `ModuleVillage.cro` terminal routine file `0x19BA8` の同一invocation内の順序は:

```text
0x19C08 / 0x19C2C / 0x19C94 / 0x19CC4
    BL import 0xDE8 -> main 0x598BEC  // landing attempt
...
0x19CDC
    BL import 0xDF8 -> main 0x5C5A30 // Player A4 reaction
0x19CE8
    BL import 0x240                   // terminal cleanup側
return
```

「landingはhelper内だがA4だけhelper後」という因果説明には依存できない。

実機事実そのものは維持する。

- exact custom AcBalloon identity guardでA4抑止は成功した。
- state setter呼出し前にactor identityをpre-armするとcustom landing識別が成功した。

Ghidra-gpt-sol-5.6-F039ではterminalがstate setterから同期実行されるか後のupdateで実行されるかを**設計条件にしない**。

## 4. 設計不変条件

state setterを呼ぶ**前**に:

```text
shared+0x60 = exact custom AcBalloon*
shared+0x68 = 0                       // falling object未生成
shared+0x6C = 1                       // synthetic completion WAIT
```

その後にのみ `AcBalloon_SetState(actor,1)` を呼ぶ。

terminalが同期でも遅延でも同じ状態から処理される。

## 5. synthetic completion state

synthetic handleはGhidra-gpt-sol-5.6-F032と同じ `4`。

`shared+0x6C`:

- `1` = WAIT
- `2` = SUCCESS
- `3` = FAILURE

0は通常運用では不要。次のcustom開始時に必ず1で上書きする。

status 2/3をpoll時に0clearしない。BsMenuItemが同じhandleを再度pollしても結果が変化しないようterminal stateとして保持する。

## 6. custom start

Ghidra-gpt-sol-5.6-F032 spawn pathを維持する。

前提:

- `BsVillageBalloonMgr* @ 0x948DD4 != NULL`
- `AcBalloon* @ 0x948DDC == NULL`
- stock `Player_DropItem` がtarget tileを解決済み
- `ActorFactory_CreateByTypeId` 成功

ActorFactory契約:

```text
r0 = 0xF1
r1 = BsVillageBalloonMgr*
r2 = 0
r3 = Vec3*
stack arg #5 = 0
```

`0x57ADFC` はstack arg #5を `0x947FEC` へstageし、後段が非zero時にpointerとしてdereferenceする。Ghidra-gpt-sol-5.6-F037 crashで0x0Aを入れたことがfault原因だった。ここは変更禁止。

ActorFactoryがNULLならstatusをarmせずstock `Item_PlaceItem` fallbackへ戻る。

ActorFactory成功後、state setter前に§4の3値をarmする。

## 7. custom landing

`0x598BEC` hookはexact actor identityだけをcustom処理する。

```text
if incoming r4 != shared+0x60:
    stock BalloonPresent_TryLandAndPlace
else:
    BalloonPresent_CreateAtTile(
        shared+0x04 Item*,
        shared+0x08 X,
        shared+0x00 Y,
        shared+0x10 impact Vec3*,
        0)
```

full natural 0x21 FieldAction bodyはcustom actorでは実行しない。

### 7.1 visual生成成功の証明

`BalloonPresent_CreateAtTile @ 0x59ABE8` はmanager/availabilityを確認し、`FgObjPresent_SpawnFalling @ 0x593D0C` がNULLでない場合だけ `0x59AC50` へ到達する。

Ghidra-gpt-sol-5.6-F032 capture hookは `0x59AC50` でexact object pointerを `shared+0x68` へ保存する。

従ってterminal landing attempt後:

```text
shared+0x68 != 0  <=> custom falling object生成成功を観測済み
```

## 8. terminal A4 reaction guardをfailure判定にも利用する

raw ModuleVillage terminal orderではlanding attemptの後にcustom A4 reaction callsite `LR=0xBFCCE0` が来る。

exact actor + exact LR一致時:

```text
shared+0x60 = 0

if shared+0x68 == 0:
    shared+0x6C = 3
else:
    shared+0x6C remains 1

return without Player A4 reaction
```

これで `0x59ABE8` に追加return hookを入れず、既存identity guard位置で同期landing failureを確定できる。

この判定はterminal内部のlanding -> A4順序だけに依存する。state setterとの同期/非同期関係には依存しない。

## 9. handle 4 poll

`DropQueue_PollAndFinalize @ 0x596C84` はstockでは最初にhandleからDropData addressを計算するため、handle 4は必ず入口で捕捉する。

```text
if handle != 4:
    stock 0x596C84
else:
    return shared+0x6C
```

WAIT=1 / SUCCESS=2 / FAILURE=3 がそのままBsMenuItem contractと一致する。pollはstatusを書き換えない。

### 9.1 WAIT stranded対策

正常path:

- terminal前: `+0x60=actor`, `+0x68=0`, status=1
- terminal成功後〜impact前: `+0x60=0`, `+0x68=fallingObject`, status=1

terminal landing失敗は§8でstatus=3になる。

「actorがterminalへ到達せず異常破棄される」具体的pathは未確定なので推測timeoutは導入しない。実機で再現した場合だけteardown pathを追加解析する。

## 10. falling objectはshared Item lifetimeから独立する

`FgObjPresent_SpawnFalling @ 0x593D0C` はobject生成後 `0x58FB40` を呼ぶ。

`0x58FB40`:

```asm
MOV r11,r1
...
ADD r0,r0,#0x64
BL  0x2FC878
```

Itemをobject+0x64へcopyする。positionもobject+0x40/+0x44/+0x48へ保持される。

従ってimpact後に次のcustom dropがshared Item/X/Yを上書きしても、旧visualのmode-1 cleanupは壊れない。

pool table literalは `0x98447C`、count literalは `0x226`。

## 11. impact / persistence / SUCCESS publication

exact falling objectだけ処理する。

Ghidra-gpt-sol-5.6-F032と同じ:

```text
mode 0 -> 1 ground contact
    -> get local player id
    -> FieldTile_CommitItem @ 0x168E08
    -> FieldTile_RefreshAfterCommit @ 0x599814
```

completion publicationは:

```text
0x168E08 return
0x599814 return
shared+0x6C = 2
shared+0x68 = 0
resume stock FgObjPresent_Update
```

commit/refreshより前にstatus=2を出してはいけない。

## 12. mode-1 cleanupを待たない理由

`FgObjPresent_Update @ 0x593E68` mode 1:

```text
0x58ED68(object,0)
0x67BBF0()
return 1
```

field Item persistenceを実行しない。visual object自身がItem/positionを所有するため、completion pointはmode-1 deletionではなく **0x168E08 -> 0x599814完了後** とする。

## 13. 0x168E08のfailure semantics

`FieldTile_CommitItem @ 0x168E08` は内部gateを持ちbool successを返すAPIではない。

stock action 0x0A updaterもvisual生成成功後:

```text
0x168E08(...)
0x599814(...)
...
record.state = 2
```

と進み、0x168E08 returnをsuccess判定に使わない。

Ghidra-gpt-sol-5.6-F039もstock completion semanticsを踏襲する。初回実機検証scopeは **offline/local**。online/network同期は未検証。

## 14. Player state A4 guard

Ghidra-gpt-sol-5.6-F025 hardware-verified identity guardを維持する。

```text
incoming r4 == shared+0x60
LR == 0xBFCCE0
```

一致時のみA4 reactionをskip。natural balloon/other callerはstock。

Ghidra-gpt-sol-5.6-F039では同時に§8のfalling-object生成結果を確定する。

## 15. custom-success pathから除外する関数

- `Item_PlaceItem @ 0x59E5B4`
- `FieldAction_QueueToRecord @ 0x59EBE8`
- `FieldAction_Dispatch @ 0x59E8F8`
- full custom `BalloonPresent_TryLandAndPlace` body
- `FieldActionType0A_GroundDropUpdate @ 0x5A0C2C`
- `0x5A155C` action 0x12 handler
- `0x59A4A0` normal-drop visual constructor

custom operation本体はGhidra-gpt-sol-5.6-F032 hardware-verified pathのみ維持する。

## 16. 実装時の最小差分

1. state helper: state setter前に `+0x60 actor / +0x68 0 / +0x6C 1` をarm。
2. spawn cave: helper return後の `STR r0,[+0x60]` を撤去。setter return valueへidentityを依存させない。
3. poll hook: handle 4を即2ではなく `shared+0x6C` へ変更。
4. A4 guard / impact hook:
   - A4 guard: `+0x68==0`ならstatus3。
   - impact: commit+refresh後status2、その後+0x68 clear。

## 17. 検証順序

1. drop開始後 status=1。
2. handle=4 poll中、落下中は1。
3. 落下中はsource Itemが残る。
4. BsMenuItem wait中は2個目dropを開始できない。
5. exact falling objectが+0x68へ入る。
6. A4 guard時、+0x68!=0ならstatus=1のまま。
7. Player state 0x16維持。
8. ground contactで0x168E08が1回。
9. 続けて0x599814が1回。
10. その後だけstatus=2。
11. 次pollで2、source Itemが1回だけ消える。
12. UI解放。
13. 次のdrop開始可能。
14. landing生成を故意に失敗させるとA4 guard時+0x68==0、status=3、source Item維持。
15. natural balloonはstock挙動。

## 18. 実装配置案

```text
0x8381D8-0x8381F3  new: terminal outcome helper (0x1C)
0x8381F4-0x8381FF  padding
0x838200-0x83832F  existing spawn/fallback
0x838330-0x83837F  existing custom landing
0x838380-0x8383BF  revised state helper
0x8383C0-0x8383D7  revised synthetic poll
0x8383D8-0x8383F7  existing falling-object capture
0x838400-0x838423  existing textbox cave — touch禁止
0x838424-0x838463  revised A4 identity guard
0x838464-0x8384F3  revised/expanded impact commit block
0x8384F4-0x8384FF  spare
0x838500-             existing replacement strings — touch禁止
```

### 18.1 0x8381D8 gap再監査

fresh bytes全体を再走査:

- initialized `.text` からのARM B/BL target: 0
- initialized `.text/.rodata/.data` のaligned direct pointer: 0
- XML allocation mapではdrawing cave `0x838140-0x8381D7` 直後の未割当gap
- current Ghidra-gpt-sol-5.6-F032 ARはこのrangeを書かない

最終AR生成時にも再監査する。

### 18.2 revised state helper

既存0x40 bytes内に収める。

```asm
PUSH {r4,lr}
MOV  r4,r0
LDR  r12,[r4]
LDR  r12,[r12]
LDR  r3,=0xE6CC
SUB  r12,r12,r3
STR  r4,[r10,#0x60]
MOV  r2,#1
STR  r2,[r10,#0x6C]
MOV  r2,#0
STR  r2,[r10,#0x68]
MOV  r1,#1
BLX  r12
MOV  r0,r4
POP  {r4,pc}
.word 0xE6CC
```

旧 `shared+0x0C` cleanupを撤去。spawn caveのhelper return後 `STR r0,[r10,#0x60]` はNOPへ変更。

### 18.3 terminal outcome helper

A4 guard exact matchから、`r12=shared` を保持してbranch:

```asm
LDR   r3,[r12,#0x68]
CMP   r3,#0
MOVEQ r3,#3
STREQ r3,[r12,#0x6C]
MOV   r3,#0
STR   r3,[r12,#0x60]
BX    lr
```

0x1C bytes。

### 18.4 revised poll

既存0x18-byte caveに収める。

```asm
CMP   r0,#4
LDREQ r12,=<shared>
LDREQ r0,[r12,#0x6C]
BXEQ  lr
PUSH  {r4-r11,lr}
B     0x596C88
```

### 18.5 revised impact block

既存blockを0x88から最大0x90へ拡張し、0x838500より前に収める。

順序:

```text
exact-object check
PUSH registers
prepare Item* stack arg
local player id
0x168E08
0x599814
status = 2
fallingObject = 0
restore
resume 0x593F50
```

現在Ghidra-gpt-sol-5.6-F032の `fallingObject=0` はcommit前なので、Ghidra-gpt-sol-5.6-F039では必ずcommit後へ移動する。

## 19. 採用判断

> **実操作はGhidra-gpt-sol-5.6-F032のまま。completionだけをhandle 4の非同期3状態にする。同期時系列を仮定せず、観測済みactor/object identityで進める。**

独立二系統解析の共通部分だけから構成する。


## 20. Implementation result

Ghidra-gpt-sol-5.6-F039 candidate AR has now been assembled from this design.

Implementation detail refined during assembly:
- after `0x168E08 -> 0x599814`, clear `shared+0x68` first;
- publish `shared+0x6C = 2` **last**.

This is slightly stronger than the earlier prose ordering because a concurrent/next UI observation can only see SUCCESS after the exact falling-object identity has already been released.

Final cave layout:
```text
0x8381D8-0x8381FF  terminal outcome + synthetic poll helper
0x838200-0x8383D7  existing main block with revised state/poll
0x8383D8-0x8383F7  existing Ghidra-gpt-sol-5.6-F032 falling-object capture
0x838424-0x838463  revised A4 identity guard
0x838464-0x8384EB  revised impact commit/completion
```

Static implementation audit passed:
- source stock hook words match JPN v1.5 raw bytes
- E-block lengths exact
- E-block overlap 0
- all hook/internal ARM branch targets exact
- initialized .text ARM B/BL targets into cave ranges: 0
- aligned initialized pointers into cave ranges: 0
- highest written cave address 0x8384EB
- reserved 0x838500+ area untouched

Detailed implementation evidence:
`work/evidence/balloon_drop_gf039_implementation_20260916.md`

Hardware validation remains pending.


## 21. Hardware validation

**SUCCESS.**

Hardware behavior matched the design:
- async WAIT persisted during flight;
- the selected Item used the custom balloon visual;
- persistence completed at impact;
- source inventory completion occurred afterward;
- inventory UI recovered normally;
- Player state behavior remained correct.

Ghidra-gpt-sol-5.6-F039 is promoted from static candidate to the current hardware-verified baseline.
