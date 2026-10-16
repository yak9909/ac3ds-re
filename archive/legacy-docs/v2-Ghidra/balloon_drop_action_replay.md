# 通常ドロップを風船経由に置換するCTRPF Action Replay

対象: ACNL JPN v1.5 / CTRPluginFramework Action Replay。

現行コード: `artifacts/action_replay/acnl_jpn_v15_balloon_drop.txt`

## Ghidra-gpt-sol-5.6-F012 現行設計

### 1. Player_DropItem hook

`0x596188` のstock `BL Item_PlaceItem` を `BL 0x838200` に置換。

custom可能条件:
- BsVillageBalloonMgrあり
- 現在AcBalloonなし
- ActorFactory成功

成功時:
- target tileからballoon position生成
- AcBalloon生成
- shared pageへItem/world tile/impact Vec3保存
- state 1を同期実行
- `r0=4` をreturn

ここで `4` はsynthetic completion handle。stock `Item_PlaceItem` のhandleは0..3なので衝突しない。

custom不可/生成失敗時:
- 元register/stack/LRを復元
- `BX Item_PlaceItem`
- stock `Item_PlaceItem(type=0x0A,...)` へtail-call

`BLX Item_PlaceItem -> BX LR` は使用しない。tail-callなのでstock関数は直接 `Player_DropItem+0x108` へreturnする。

### 2. custom landing

`0x598BEC BalloonPresent_TryLandAndPlace` の先頭を `B 0x838330` に置換。

armed=1のcustom AcBalloonだけ:
```
BalloonPresent_CreateAtTile(
    shared Item*,
    shared worldX,
    shared worldY,
    shared impact Vec3*,
    0
)
```
を直接call。

armed=0の自然風船はstock prologueを実行して `0x598BF0` へ戻る。

### 3. inventory completion

Ghidra-gpt-sol-5.6-F010で、BsMenuItemは `Player_DropItem` returnを `this+0xD8` に保存し、
`FieldAction_PollAndFinalize @ 0x596C84`
がstatus 2を返すまで待つことを確認した。

Ghidra-gpt-sol-5.6-F012は `0x596C84` を `B 0x8383C0` に置換。

（疑似C を省略。原本は _local/legacy-src/…）

これによりcustom dropではFieldAction slotを一切allocate/改変せず、BsMenuItemだけstock success-completionへ進む。

status 2後、stock BsMenuItemが:
- selected slotをg_EmptyItemへ変更
- slot iconをrefresh
- drag/drop UI stateをadvance

する。

## Ghidra-gpt-sol-5.6-F011 crash correction

Ghidra-gpt-sol-5.6-F011は `Item_PlaceItem(type=0x10)` をcompletion tokenに使用していたが、実機でdrop瞬間にcrash。

crash_dump_00000008:
- data abort
- PC `0x59E624`
- FAR `0x11`
- r4 `0`
- r5 `0x31F50688`

`0x59E624` は `Item_PlaceItem` 内 `LDRB r1,[r4,#0x11]`。正常なFieldAction entry pointer/indexになっていない。

またGhidra-gpt-sol-5.6-F011 stubは `BLX Item_PlaceItem -> BX LR` でcaller LRを失う静的バグもあった。

そのためtype 0x10方式は完全廃止。

## code cave

- `0x838200-0x83832F`: spawn/fallback
- `0x838330-0x83837F`: landing
- `0x838380-0x8383BF`: state helper
- `0x8383C0-0x8383D7`: completion poll hook
- `0x8383D8-0x8383FF`: unused
- next known allocation: `0x838400`

payload:
- size `0x1D8` = 472 bytes
- SHA-256 `9ecc906c807c162fb7ccecc3b31a8b1d5a99a8d944a790d7e22ddfe9751131d7`

hooks:
- `0x596188 = EB0A881C` → `0x838200`
- `0x598BEC = EA0A7DCF` → `0x838330`
- `0x596C84 = EA0A85CD` → `0x8383C0`

stock restore:
- `0x596188 = EB002109`
- `0x598BEC = E92D4FF3`
- `0x596C84 = E92D4FF0`

## 実機確認項目

1. drop時にcrashしない
2. 風船→プレゼントが1個生成
3. 元Itemがinventoryから消える
4. drag iconが解放される
5. inventoryが継続操作可能
6. Player state `0x16 -> 0x06` が残るか

Ghidra-gpt-sol-5.6-F012は静的検証済み、実機未検証。


## Ghidra-gpt-sol-5.6-F013: inventory-open中のPlayer state保持

Ghidra-gpt-sol-5.6-F012で持ち物側のcompletionは実機上正常化したが、custom balloon drop後にPlayer state `0x16 -> 0x06` が残った。

stock inventory dropではこの遷移は起きないため、custom balloon lifecycle中だけstate 6へのgeneric normalizationを抑止する。

### guard arm

既存dead cave `0x838080` にwrapperを置く。

custom actor state helperを呼ぶ直前:
- `MENU_FLAGS @ 0x949D68` を読む
- bit `0x08` (menu-open lifetime) がsetなら
- `shared+0x1C = 1`

その後、従来のAcBalloon state helper `0x838380` を呼ぶ。

### Actor_SetState hook

`Actor_SetState @ 0x64C688` の先頭を `B 0x8380C0` に置換。

hook条件:

（疑似C を省略。原本は _local/legacy-src/…）

これによりcustom drop後もメニューが開いている間だけ `0x16 -> 0x06` を拒否する。

メニューが正規に閉じてbit 0x08が落ちるとguardをclearし、それ以降のstate transitionはstock処理へ戻す。

### diagnostic

`shared+0x20` に、最後に抑止した `Actor_SetState` caller LRを保存する。

必要なら実機でこの値を読み、直接callerが:
- `0x64BDFC`
- `0x672F40`
- その他

のどれかを確定できる。

### cave / hooks

guard cave:
- `0x838080-0x8380B7`: guard-arm wrapper
- `0x8380C0-0x838117`: Actor_SetState guard

既存balloon cave:
- `0x838200-0x8383D7`

hooks:
- `0x64C688 = EA07AE8C` → `0x8380C0`
- `0x83810C = EAF8515E` → stock continuation `0x64C68C`
- `0x8382E4 = EBFFFF65` → wrapper `0x838080`

OFF restores `0x64C688 = E92D5FF0` and clears shared guard/LR slots.

Ghidra-gpt-sol-5.6-F013 is statically validated and hardware re-test is pending.


## Ghidra-gpt-sol-5.6-F014: enable直後crashとguard cave再配置

Ghidra-gpt-sol-5.6-F013初版では、旧Ghidra XMLのallocation noteにある「dead cave / NOP化済み / 参照なし」を根拠に `0x838080-0x838137` を再利用した。

しかし実機ではARを有効化した瞬間、drop操作なしでcrashした。

crash_dump_00000009:
- exception = data abort
- PC = `0x566E04`
- LR = `0x8380AC`
- r0 = `0`
- r10 = `0`
- FAR = `0`

`0x8380AC` は旧guard wrapperがAcBalloon state helperから戻る位置。正規custom drop経路ならspawn caveがshared baseを `r10=0x01E81000` に保持しているはずだが、dumpでは `r10=0`。さらにユーザーはdropしていない。

従って、`0x838080` はXML export時点ではdeadでも、実機runtimeでは別の既存経路/patchから使用されている。

### 新配置

guardロジックは維持し、既存allocationの間にある未使用gapへ移設:

- `0x838400-0x838423`: 既存textbox cave
- `0x838424-0x83845B`: Ghidra-gpt-sol-5.6-F013 guard-arm wrapper
- `0x83845C-0x838463`: padding
- `0x838464-0x8384BB`: Actor_SetState guard
- `0x8384BC-0x8384FF`: unused
- `0x838500-`: 既存replacement strings

`0x838424-0x8384BB` は再確認済み:
- initialized main imageからのARM B/BL target 0件
- initialized image内aligned direct pointer 0件
- Ghidra allocation map上の既存割当 0件

updated branches:
- `0x8382E4 -> 0x838424`: `EB00004E`
- `0x83844C -> 0x838380`: `EBFFFFCB`
- `0x64C688 -> 0x838464`: `EA07AF75`
- `0x8384B0 -> 0x64C68C`: `EAF85075`

hashes:
- relocated guard block: `e3c9f2dd07c3cc4fd6a5c4961e2c691a832fd1a21a90bde44dc6afb44d3e1077`
- modified main balloon block: `4e59739939afcaedd53612a348f8b8707e163b238061899b1b8071c89f4dd00f`
- concatenated: `eb815cc9f2ba683285c507022c60bdba1873a78783cdba08f0fccabca2038bcb`

`0x838080-0x838137` は今後custom caveとして使用しない。


## Ghidra-gpt-sol-5.6-F015: state guardをActorFactory前へ前倒し

Ghidra-gpt-sol-5.6-F014移設版はenable直後crashを解消したが、custom drop後のPlayer state `0x16 -> 0x06` は残った。

再監査すると、旧guardは遅すぎた。

旧順序:

```
GET_PLAYER
ActorFactory_CreateByTypeId
shared Item/Vec3保存
guard arm
AcBalloon state 1
```

このためActorFactory中にPlayer state resetが起きる場合、guardはまだ0であり `Actor_SetState` hookを素通りする。

### 新順序

```
GET_PLAYER wrapper
  -> stock GET_PLAYER
  -> shared.guard = 0
  -> player != 0
  -> player->currentState == 0x16
  -> MENU_FLAGS & 0x08
  -> shared.guard = 1
return Player*

ActorFactory_CreateByTypeId
AcBalloon setup
AcBalloon state 1
```

`GET_PLAYER @ 0x5C27D8` 自身はPlayer current stateを読むが変更しないため、この位置でarmすればcustom path内の最初の外部副作用処理であるActorFactoryより前を確保できる。

### 新guard cave

既存textbox caveとreplacement-string storageの間:

- `0x838424-0x83847B`: GET_PLAYER + early guard arm
- `0x83847C-0x838483`: padding
- `0x838484-0x8384DF`: Actor_SetState guard
- `0x8384E0-0x8384FF`: unused
- `0x838500-`: existing replacement strings

更新命令:

- `0x838270: EB00006B` → BL `0x838424`
- `0x838274: E1A00000` → NOP
- `0x8382E4: EB000025` → BL state helper `0x838380`
- `0x64C688: EA07AF7D` → B `0x838484`

Actor_SetState stock continuationは `LDR pc,=0x64C68C` を使用する。

### static validation

`0x838424-0x8384E3`:
- initialized main-image ARM B/BL target 0件
- aligned direct pointer 0件
- known allocation 0件

hashes:
- guard block: `888c90a30e2d121b9794d4c44fb51334f532cb864a53b724382a16d3e8b84e67`
- main cave: `5fcbadb1449c4d7a316df1a8dd46fd47fb9e2685f1d9a7654d037ba61f6cf368`
- combined: `ead098d3dc8144ce4fc4a0a5e69bfc357b2764369b2ad52da240bcb92b10a7e2`


## Ghidra-gpt-sol-5.6-F016: menu-open state invariantを直接守る

Ghidra-gpt-sol-5.6-F015 early-arm版でも実機ではstate 0x16 -> 0x06が残ったため、custom shared guardは廃止した。

stock menu lifecycleを再確認すると:

- `BsMenuItem_CloseUpdate @ 0x19AAC0` はclose animation/process完了後に `MENU_FLAGS` bits `0x08|0x10` をclearする。
- `BsMenuTab_WaitMenuEndUpdate @ 0x6D7194` はbit `0x08` がsetの間はreturn flowへ進まず、clear後にclose/return request bit `0x20` をsetする。

したがってmenu-open bit 0x08が立っている間はPlayer current state 0x16を維持し、bit 0x08が落ちた後はstate 6への遷移を許可するのが自然な不変条件。

### Actor_SetState hook

`0x64C688` を `0x838424` へbranch。

（疑似C を省略。原本は _local/legacy-src/…）

custom guard flagには依存しない。

### direct-write scan

main .textをARM命令としてscanし、即値 `#0x1A9` への `STRB` は22箇所。

Player state-machine側で明確なruntime state writeは:
- `0x64C79C` — `Actor_SetState` のcurrent-state write
- `0x68D7C4` — Player初期化処理

後者はconstructor/init系なので、通常drop時の0x16->0x06説明にはなりにくい。

### cave

- `0x838424-0x838473`: menu-open state guard
- `0x838470-0x8384FF`: unused
- `0x838500-`: existing replacement strings

hook:
- `0x64C688 = EA07AF65`

hashes:
- guard `2995fa6ffaf19ca981d2d74b73f2c986363a708cc549c0898be1138e1a235936`
- main cave `9ecc906c807c162fb7ccecc3b31a8b1d5a99a8d944a790d7e22ddfe9751131d7`
- combined `7cd41fcf4282683bdc14d20a0e05a92d2c04be7fc8244d80e1f699238deb6c97`


## Ghidra-gpt-sol-5.6-F019: state suppressionを外した診断build

Ghidra-gpt-sol-5.6-F016までのstate抑止では原因transitionを特定できなかったため、現行ARは診断build。

`Actor_SetState @ 0x64C688` は `0x838424` へbranchし、最初の「menu-open中・current=0x16・requested!=0x16」をshared pageへ記録した後、stock `0x64C68C` へ復帰する。

stateを止めたり書き戻したりはしない。

trace:
- `0x01E81020`: caller LR
- `0x01E81024`: requested state
- `0x01E81028`: old current
- `0x01E8102C`: desired (+0x1AB)
- `0x01E81030`: marker
- `0x01E81034`: previous (+0x1AA)
- `0x01E81038`: Player*
- `0x01E8103C`: r2
- `0x01E81040`: r3
- `0x01E81044`: MENU_FLAGS

trace E-block:
- address `0x838424`
- size `0x80` bytes
- executable/literal bytes `0x7C`
- final `0x04` bytes are padding
- SHA-256 (0x80 bytes): `dfb9fbf244e129760658371a936627d9693e447f40eff0a6a857c3d09b0b3d6c`

AR enable時にtrace領域を0clearする。


## Ghidra-gpt-sol-5.6-F022: Player state 0xA4 reactionだけをcustom dropで抑止

実機traceにより、custom drop後のPlayer state lossは:
```
0x16 -> 0xA4 -> 0x06
```
と確定。

最初の`0xA4`要求はModuleVillage AcBalloon terminal drop:
- CRO file `0x19CDC`
- runtime `0xBFCCDC`（load base `0xBE3000`）
- imported main helper `0x5C5A30`

main helper chain:
```
0x5C5A30
  -> GET_PLAYER
  -> 0x6830D4
       -> state context param setup
       -> Actor_SetState(player,0xA4,...)
```

custom dropではstate helperが同期実行中のみ`shared+0x0C=1`。

そのため`0x5C5A30`を:
（疑似C を省略。原本は _local/legacy-src/…）
にhookする。

guard cave:
- `0x838424-0x838443`
- `0x5C5A30 = EA09CA7B` -> `0x838424`
- `0x838438 = EAF6357D` -> `0x5C5A34`

自然風船はarmed=0なのでstock A4 reactionが残る。

Actor_SetState診断hookは削除。

Ghidra-gpt-sol-5.6-F022 reaction guard binary SHA-256: `cc5f5296ea8afaa3304fee79071cf118b097a5effadc95ae698d8262f846ed6c` (0x20 bytes).


## Ghidra-gpt-sol-5.6-F023: Ghidra-gpt-sol-5.6-F022後に残る 0x16 -> 0x06 のcallerを直接記録

Ghidra-gpt-sol-5.6-F022実機再試験でもcustom drop直後にPlayer current stateが0x06へ遷移した。Ghidra-gpt-sol-5.6-F022はAcBalloon terminal dropの0xA4 reactionだけを抑止するため、残る0x06の発生源を別途特定する。

現行診断版はGhidra-gpt-sol-5.6-F022の0x5C5A30 hookを維持しつつ、Actor_SetState @ 0x64C688を観測hookへ変更する。

条件:
- current [r0+0x1A9] == 0x16
- requested r1 == 0x06

一致時のみ:
- shared+0x20 = caller LR
- +0x24 = requested
- +0x28 = current
- +0x2C = desired [Player+0x1AB]
- +0x30 = marker 0x06F1A57E
- +0x34 = previous [Player+0x1AA]
- +0x38 = Player*
- +0x3C = r2
- +0x40 = r3
- +0x44 = MENU_FLAGS snapshot

state遷移自体は抑止しない。元prologueを実行済みの状態で0x64C68Cへ復帰する。

trace cave:
- 0x838444-0x8384BB
- payload 0x78 bytes
- SHA-256 b8f198c50fe74d827dc3a6e919de7ac982499462f44137ec4ed3b603fda71234

hook:
- 0x64C688 -> 0x838444 = EA07AF6D
- OFF restore = E92D5FF0

静的collision再検証:
- main .text ARM B/BL target into 0x838444-0x8384BB: 0
- initialized .text/.rodata/.data aligned direct pointer into same range: 0

trace領域はAR側でclear/0固定しない。marker 0x06F1A57Eで今回の記録を識別する。


## Ghidra-gpt-sol-5.6-F024: Actor_SetState無条件hit + state 0x16 first-departure trace

Ghidra-gpt-sol-5.6-F023実機結果:
- shared 0x01E81020..0x44に記録なし
- したがって「current=0x16 && requested=0x06」の直接遷移は観測されていない

Ghidra-gpt-sol-5.6-F024ではhook到達と遷移条件を分離する。

Actor_SetState @ 0x64C688 hookは毎回:
- shared+0x48: hit counter++
- +0x4C: last requested
- +0x50: last current
- +0x54: last caller LR
- +0x5C: unconditional marker 0x24F1A57F

さらに current==0x16 && requested!=0x16 の最初のdeparture候補で:
- +0x20 caller LR
- +0x24 requested
- +0x28 current
- +0x2C desired
- +0x30 marker 0x16F1A57F
- +0x34 previous
- +0x38 Player*
- +0x3C r2
- +0x40 r3
- +0x44 MENU_FLAGS
- +0x58 Ghidra-gpt-sol-5.6-F022 armed flag (shared+0x0C)

trace cave:
- 0x838444-0x8384E3
- payload 0xA0 bytes
- SHA-256 a83f85c2309d46f90e7e1089b89c273dfad1f0642832cb8013a01fe3cf07b5f5

static collision:
- ARM B/BL target into cave: 0
- initialized aligned direct pointer into cave: 0

Interpretation:
- +0x5Cが出ない: Actor_SetState hook自体が実行されていない/適用されていない
- +0x5Cは出るが+0x30が出ない: state 0x16からのdepartureがActor_SetState経由で観測されていない
- +0x30が出る: +0x24 requested と +0x20 LR が実際の最初のdeparture


## Ghidra-gpt-sol-5.6-F025: custom AcBalloon* identityでterminal A4だけ抑止

Ghidra-gpt-sol-5.6-F024実機trace:
- caller LR = 0xBFCCE0
- requested = 0xA4
- current = 0x16
- desired = 0x06
- previous = 0x0D
- Player* = 0x33099E3C
- MENU_FLAGS = 0x081C
- hit counter = 0x06
- last requested/current/LR = 0xA4 / 0x16 / 0xBFCCE0
- Ghidra-gpt-sol-5.6-F022 armed flag (shared+0x0C) = 0

これによりGhidra-gpt-sol-5.6-F022 failure reasonが確定した。
shared+0x0CはAcBalloon state helperの同期実行中だけ1で、helper return後すぐ0になる。
一方、terminal-dropの0xA4 requestはその後にModuleVillage 0xBFCCDC -> import thunk -> main 0x5C5A30として発生するため、+0x0Cでは識別できない。

Ghidra-gpt-sol-5.6-F025はboolean timing guardを廃止し、custom生成したAcBalloon actor identityを使う。

### custom actor pointer保存

AcBalloon state helper 0x838380:
- 旧 0x8383B4: STR r2,[r10,#0] (worldY cleanup)
- 新 0x8383B4: MOV r0,r4

これによりhelperはAcBalloon*をr0で返す。
shared worldYは次回custom dropで必ず上書きされ、armed=0の間はlanding hookで参照されないため、旧cleanupは不要。

spawn cave:
- 旧 0x8382E8: NOP
- 新 0x8382E8: STR r0,[r10,#0x60]

したがってstate helper return直後に custom AcBalloon* を shared+0x60へ永続化する。

### 0x5C5A30 identity guard

ModuleVillage側terminal-dropは:
- 0xBFCCD8: LDRSB r0,[r4,#0x240]
- 0xBFCCDC: BL import thunk
- LR = 0xBFCCE0

import thunkはLDR pc形式なので、main 0x5C5A30入口でも:
- LR = 0xBFCCE0
- incoming r4 = AcBalloon*

が保持される。

Ghidra-gpt-sol-5.6-F025 guardは0x838424で:
1. shared+0x60のcustom AcBalloon*を読む
2. incoming r4と比較
3. LRが0xBFCCE0か比較
4. 両方一致した場合だけshared+0x60をclearしてBX lr
5. 不一致ならstock PUSH {r4,lr}を実行して0x5C5A34へ戻る

従って自然風船や他callerの0x5C5A30はstockのまま。

guard cave:
- 0x838424-0x83845F
- payload 0x3C bytes
- SHA-256 8f2d585a49623abdb1fde21283721f83ce05ba6dfe99c56a4a216a8930b1befd

hook:
- 0x5C5A30 = EA09CA7B -> 0x838424
- stock continuation branch from 0x838450 = EAF63577 -> 0x5C5A34

Actor_SetState diagnostic hookは削除し、0x64C688はstock E92D5FF0へ戻す。

Ghidra-gpt-sol-5.6-F025 scoped Ghidra export:
- acnl_jpn_v15_balloon_identity_delta.xml SHA-256 d9ad99ff21528834e563357b007586074159f933ea7437f334399017a31182c3, size 18991
- companion bytes SHA-256 441d9b800f745565410214f1fb628e8bb3cd06ed7ac760e22892776b951ba418, size 44

### Ghidra-gpt-sol-5.6-F025 hardware validation — SUCCESS

実機確認:
- custom balloon drop succeeds
- Player state remains 0x16 through the drop
- Ghidra-gpt-sol-5.6-F024で観測した terminal A4 reaction はGhidra-gpt-sol-5.6-F025 actor-identity guardで抑止できた

従ってGhidra-gpt-sol-5.6-F025の以下は実機で成立:
- custom AcBalloon*をshared+0x60へ保存
- ModuleVillage terminal reaction helper 0x5C5A30入口で incoming r4 と shared+0x60 を比較
- LR=0xBFCCE0も一致したcustom actorだけPlayer state 0xA4 reactionをskip
- natural balloon / other callerはstock path

Ghidra-gpt-sol-5.6-F025は hardware-validated とする。

## Ghidra-gpt-sol-5.6-F026: terminal landingをcustom AcBalloon identityで識別し、元Inventory Itemをpayloadにする

Ghidra-gpt-sol-5.6-F025実機成功後、fieldへ落ちるItemがなお 0x2036 のプレゼント（中身ランダム）だった。

原因:
- Player_DropItem hookでは actual inventory Item* から4-byte Itemを読み、shared+0x04へ保存済み
- しかし従来landing hook 0x598BEC は shared+0x0C == 1 のときだけcustom pathへ入る
- Ghidra-gpt-sol-5.6-F024で判明した通り、このarmed flagはstate helper return後に0へ戻る
- ModuleVillage terminal dropはその後に実行されるため、landing hookはstock pathへ流れる
- stock ModuleVillage terminal dropはdefault variantでItem 0x2036を構築し BalloonPresent_TryLandAndPlaceへ渡す
- そのため実機ではランダムプレゼントになる

ModuleVillage terminal-drop Ghidra disassembly:
- function entry 0xBFCBA8 でAcBalloon*をr4へ保持
- default Item path: 0xBFCC08 BL 0xBE3DE8
- variant 2/1/3も同importを 0xBFCC2C / 0xBFCC94 / 0xBFCCC4 からcall
- function後半 0xBFCCD8 LDRSB r0,[r4,#0x240] までr4はAcBalloon*のまま
- import 0xBE3DE8 はmain BalloonPresent_TryLandAndPlace @ 0x598BEC

したがってmain 0x598BEC入口でもincoming r4でcaller AcBalloon*を識別できる。

Ghidra-gpt-sol-5.6-F026 landing hook:
- shared = 0x01E81000
- if r4 == shared+0x60(customAcBalloon*) then custom path
- BalloonPresent_CreateAtTile receives Item* = shared+0x04
- worldX = shared+0x08, worldY = shared+0x00, impact Vec3 = shared+0x10
- otherwise execute stock BalloonPresent_TryLandAndPlace

変更命令:
- 0x838334: LDR r2,[r12,#0x0C] -> LDR r2,[r12,#0x60] (E59C2060)
- 0x838338: CMP r2,#1 -> CMP r4,r2 (E1540002)
- 0x83833C BNE stock は不変
- custom pathの0x838350 ADD r0,r12,#4以降は既存のまま

shared+0x04は Player_DropItem @ 0x596188 hook入口で:
- r2 = actual inventory Item*
- LDR r6,[r2]
- STR r6,[shared,#4]
として4-byte Item全体をcopyしている。
従ってitem IDだけでなくItem metadataも元持ち物の値を保持する。

自然風船はr4がshared+0x60と一致しないためstock Item選択を維持する。
custom actor identityはterminal landing後もGhidra-gpt-sol-5.6-F025 A4 guardで使い、A4 skip時にclearする。

### AR text completeness correction

Ghidra-gpt-sol-5.6-F025先頭guard E-blockは E0838424 0000003C (60 bytes) で、payload末尾が単独 00000000 1word行になっていた。
CTRPFのコードテキスト行は2word形式で扱うため不完全。

Ghidra-gpt-sol-5.6-F026では:
- block length 0x40
- final padding 00000000 00000000
へ修正。

全AR code lineを 8hex + 8hex の2word形式で再検査済み。

hashes:
- identity/reaction guard E payload 0x40: 43765ecdd5930943099b3aac2c9daf29d152f47b8dbe354e88464e84cf3fecf7
- main balloon cave 0x1D8 (inventory-item landing identity版): 7976029b7f4290c86a4aaf32b3e91c0c3cc7ee8b133f72731fdcca8ffea38a15
- combined: 6e37be11d1cc66cc323867915f0f15117a0c0ee5c2ec6b076b8bfb4a8de749cb

Ghidra scoped export:
- XML acnl_jpn_v15_balloon_inventory_item_delta.xml size 21817 SHA-256 b606806a91dbdde7a5b4776001e7f36649e88f71380c13c395fb6aa585ded3a8
- bytes companion size 576 SHA-256 81e13c44bd4e05c21ea2b853a21851ed3059444e39ba422ba75ad077d4ec1d22

Hardware validation pending:
- dropped present contains the exact inventory Item/ID selected for drop
- Player state remains 0x16
- inventory slot clears and UI remains interactive
- natural balloon payload behavior remains stock

## Ghidra-gpt-sol-5.6-F027: landing identityをstate helper内でpre-arm

Ghidra-gpt-sol-5.6-F026 hardware result:
- custom balloon経路にならず、通常ドロップへfallbackした

再監査で原因を特定。

Ghidra-gpt-sol-5.6-F026ではcustom AcBalloon*をshared+0x60へ保存する命令が:
- spawn cave 0x8382E8
- AcBalloon state helper 0x838380からreturnした後
に置かれていた。

しかしBalloonPresent_TryLandAndPlace @ 0x598BECはAcBalloon state transitionの実行中に同期的に呼ばれる。
従来のshared+0x0C armed方式でlanding overrideが成立していたこと自体も、この順序を示す。

従ってGhidra-gpt-sol-5.6-F026のlanding時点ではshared+0x60がまだ未設定で:
- incoming r4 == shared+0x60 が不一致
- custom landing pathへ入らない
- stock BalloonPresent_TryLandAndPlaceへfallback
となっていた。

### Ghidra-gpt-sol-5.6-F027 fix

state helper内、AcBalloon state setterをBLXする前に:
- r4 = custom AcBalloon*
- STR r4,[r10,#0x60]
を実行する。

具体的にはhelper:
- old MOV r2,#1 ; STR r2,[r10,#0x0C]
- new STR r4,[r10,#0x60] ; NOP
へ変更。

Ghidra-gpt-sol-5.6-F026以降landing判定はshared+0x0Cを使わないため、armed=1設定は不要。
helper後半のshared+0x0C clearは残し、旧値を確実に0へ戻す。

landing同期call時点:
- shared+0x60 = custom AcBalloon*
- ModuleVillage caller r4 = same AcBalloon*
となるためidentity判定が成立する。

helper return後のspawn cave STR r0,[r10,#0x60] も残し、subsequent terminal A4 reaction guard用にidentityを再確認保存する。
helperはreturn直前にr0=r4としているため同一pointer。

### ABI revalidation

ModuleVillage AcBalloon_TerminalDrop_CRO @ 0xBFCBA8:
- entry MOV r4,r0
- item path call BL 0xBE3DE8 at 0xBFCC08/2C/94/C4
- r4 remains AcBalloon* through these calls
- later 0xBFCCD8 LDRSB r0,[r4,#0x240]
- 0xBFCCDC reaction helper call

Main BalloonPresent_TryLandAndPlace @ 0x598BEC decompile confirms formal ABI is two arguments:
- r0 = impact/position pointer
- r1 = Item*
so r2 is not an incoming formal argument。

Ghidra-gpt-sol-5.6-F027 therefore keeps landing comparison:
- LDR r2,[shared,#0x60]
- CMP r4,r2
and on match passes shared+0x04 inventory Item to BalloonPresent_CreateAtTile.

Ghidra export:
- XML acnl_jpn_v15_balloon_inventory_item_timing_delta.xml
- size 23251
- SHA-256 6c394eeef7444a2d9bad634b2a9b354c7000dcbd8ed163a2ed24775e6102365d
- bytes size 576
- bytes SHA-256 81e13c44bd4e05c21ea2b853a21851ed3059444e39ba422ba75ad077d4ec1d22

Hardware validation pending.

## Ghidra-gpt-sol-5.6-F028: custom Item substitutionをstock landing persistence経路へ戻す

Ghidra-gpt-sol-5.6-F027 hardware result:
- dropped item visual matches the selected inventory Item
- Player state 0x16 remains preserved
- however the falling Item disappears after landing instead of remaining on the ground

原因:
- Ghidra-gpt-sol-5.6-F027 custom landing bypasses BalloonPresent_TryLandAndPlace body
- it directly calls BalloonPresent_CreateAtTile @ 0x59ABE8
- this creates/activates the falling fgobj_ObjectPresent visual
- but skips the stock success path that registers and dispatches the persistent field action

Ghidra stock BalloonPresent_TryLandAndPlace @ 0x598BEC confirms the persistent success path:
- 0x598D4C: FieldAction_RegisterActive(type=0x21, tile, context, 1)
- 0x598D58: FieldAction_InitRecord
- 0x598D7C: BalloonPresent_BuildFieldActionRecord(record, Item*, x, y, ...)
- 0x598D88: FieldAction dispatch/send
- 0x598DA0: BalloonPresent_CreateAtTile(Item*, x, y, impact, 0)

Thus 0x59ABE8 alone is only the falling-present object creation side of the stock landing operation; persistence requires the preceding FieldAction/record chain.

### Ghidra-gpt-sol-5.6-F028 design

Do not directly call 0x59ABE8 for custom balloons.
Instead, hook the entry of BalloonPresent_TryLandAndPlace only to substitute its Item argument:

- incoming r0 = impact/position pointer
- incoming r1 = stock ModuleVillage Item* (normally Item 0x2036 for default balloon)
- incoming r4 = AcBalloon* retained by the ModuleVillage caller

At cave 0x838330:
- load shared base
- load shared+0x60 custom AcBalloon*
- compare incoming r4
- if equal, set r1 = shared+0x04 (captured original inventory Item)
- execute original prologue PUSH {r0,r1,r4-r11,lr}
- branch to stock continuation 0x598BF0

Natural balloons do not match the custom actor identity, so their original r1 Item remains unchanged.

Relevant patch words:
- 0x838330 E59FC040  LDR r12,=0x01E81000
- 0x838334 E59C2060  LDR r2,[r12,#0x60]
- 0x838338 E1540002  CMP r4,r2
- 0x83833C 028C1004  ADDEQ r1,r12,#4
- 0x838340 E92D4FF3  original BalloonPresent_TryLandAndPlace prologue
- 0x838344 EAF58229  B 0x598BF0

This keeps:
- Ghidra-gpt-sol-5.6-F027 pre-armed custom AcBalloon identity
- Ghidra-gpt-sol-5.6-F025 terminal A4 reaction suppression
- synthetic inventory completion handle 4
while restoring stock field-placement persistence.

Ghidra export:
- XML acnl_jpn_v15_balloon_landing_persistence_delta.xml
- size 25055
- SHA-256 8fafb1b3c2049208f51d94ba70459dd95482e781ff9ead0e5c330e9987c18d16
- bytes size 576
- bytes SHA-256 81e13c44bd4e05c21ea2b853a21851ed3059444e39ba422ba75ad077d4ec1d22

Hardware validation pending:
- selected inventory Item falls from balloon
- Item remains on ground after landing
- source inventory slot clears once
- Player state remains 0x16
- inventory remains interactive
- natural balloon behavior stays stock

## Ghidra-gpt-sol-5.6-F029: direct falling visualを維持し、impact時だけground itemを確定

Ghidra-gpt-sol-5.6-F028 hardware result:
- custom balloonではなく通常ドロップになった
- drop後inventory completionが解放されず、下画面が操作不能になった

Ghidra-gpt-sol-5.6-F028は撤回する。full stock BalloonPresent_TryLandAndPlaceを戻す方式は、custom側のsynthetic completion handle 4とstock FieldAction type 0x21を二重に走らせ、custom inventory lifecycleと競合する。

### Ghidra-gpt-sol-5.6-F027の成功部分

Ghidra-gpt-sol-5.6-F027では:
- selected inventory Itemの見た目で風船から落下した
- Player state 0x16を維持した
- synthetic handle 4でinventory/UI completionを維持できた

失敗は着地後にvisualが消える点だけだった。

### fgobj_ObjectPresent着地処理

`FgObjPresent_Update @ 0x593E68` を追跡すると、mode 0のfalling presentは最初の着地時に:
- 0x590EA0をcall
- 0x593F4Cでobject+0x146へmode 1を書込
- 後続mode 1処理でvisual objectを削除
する。

このupdate自体はpersistent ground Itemを生成しない。従ってGhidra-gpt-sol-5.6-F027は正しいfalling visualだけが存在し、着地後に消えるのが構造上の動作だった。

### stock ground-item finalizer

`0x5A155C` を `FieldAction_FinalizeGroundItem` と同定。
このroutineはaction-entry-like構造を受け取り:
- 0x168E08でfield/tile data更新
- 0x59DA7Cでtile/object occupancy更新
- 0x59A4A0でpersistent ground fgobj生成
を行う。

実際に参照するentry field:
- +0x00 shown/empty Item
- +0x04 actual Item
- +0x0C flags
- +0x0E tile X
- +0x0F tile Y
- +0x15 player id

### Ghidra-gpt-sol-5.6-F029 design

Ghidra-gpt-sol-5.6-F027のdirect balloon falling pathとsynthetic completionを復元した上で、custom falling objectだけを捕捉する。

`BalloonPresent_CreateAtTile @ 0x59ABE8` 内:
- r6はItem*を保持
- custom pathではr6 == shared+0x04
- 0x593D0Cが作ったfgobj_ObjectPresent*は0x59AC48後のr1

0x59AC50をhookし、r6 == shared+0x04の時だけr1をshared+0x68へ保存する。

次に0x593F4Cをhookし:
- original `STRB r0,[r4,#0x146]`を実行
- new mode == 1
- r4 == shared+0x68
の時だけ一度:
- shared+0x68をclear
- synthetic entryをshared+0x80に構築
- actual Item = falling object+0x64
- X/Y = saved shared+0x08/+0x00
- player id = 0x2F75CC
- `FieldAction_FinalizeGroundItem @ 0x5A155C`をcall
する。

その後stock FgObjPresent_Update @ 0x593F50へ戻る。

これによりfull stock balloon FieldAction type 0x21を起動せず、Ghidra-gpt-sol-5.6-F027で正常だったinventory completion/UI releaseを維持したまま、visual impactの瞬間に地面Itemだけ確定する。

### caves / hooks

- capture cave 0x8383D8-0x8383F7 (0x20 bytes)
- impact cave 0x838464-0x8384F3 (AR E-block 0x90 bytes including padding)
- 0x59AC50 -> 0x8383D8 = EA0A75E0
- 0x593F4C -> 0x838464 = EA0A9144
- OFF restore 0x59AC50 = E5980014
- OFF restore 0x593F4C = E5C40146

Static collision:
- existing ARM B/BL target into both new cave ranges: 0
- initialized aligned direct pointers into both ranges: 0

AR E-block audit:
- 0x838424 length 0x40: exact
- 0x838464 length 0x90: exact
- 0x838200 length 0x1D8: exact
- 0x8383D8 length 0x20: exact
- all payload lines are complete 2-word CTRPF lines

Ghidra export:
- acnl_jpn_v15_balloon_impact_persistence_delta.xml
- size 25832
- SHA-256 5801d08e4973ab13afed1d0bb348794752c5f3070dd4d0cd8ef6943b2853c28e
- bytes size 1237
- bytes SHA-256 bb113b4c6e2d1913677f11745df79ba2698603e0c2e780cc99cc6d67f09b6087

Hardware validation pending:
- selected Item falls from balloon
- after visual impact the same Item remains on the ground
- inventory slot/drag state releases normally
- Player state remains 0x16

## Ghidra-gpt-sol-5.6-F030: action 0x12誤用を撤回し、stock action 0x0Aでimpact定着

Ghidra-gpt-sol-5.6-F029 hardware result:
- selected inventory Itemの見た目で風船から落下
- 着地後は依然として消滅
- 着地時に岩破壊のようなeffectが発生
- user hypothesis: drop/action ID 0x12

この0x12仮説は静的解析で確認できた。

`FieldAction_DispatchGroundOperation @ 0x5A06D4` のjump table:
- operation byte = record+0x10
- case 0x12 -> 0x5A0BEC -> BL 0x5A155C
- case 0x0A -> このdispatcherではdefault/no-op arm

従ってGhidra-gpt-sol-5.6-F029が直接呼んだ0x5A155Cはgeneric ground finalizerではなく、operation 0x12専用handlerだった。
hardwareで見えた岩破壊様effectは、この誤った0x12 handler実行と整合する。

### normal drop action 0x0A

`FieldActionType0A_GroundDropUpdate @ 0x5A0C2C` を復元。
record+0x11 == 1 かつ operation +0x10 が0x0A/0x22の時:
- local player idをrecord+0x15と照合
- player/network index record+0x0DからPlayer positionを取得
- `GroundItem_SpawnPersistentFgObj @ 0x59A4A0` を record+0x08 Item, tile X/Yでcall
- 成功時に必要条件ならtile state更新
- record+0x11 = 2

`FieldAction_CreateOperationRecord @ 0x5A16B0` からlayoutも確認:
- +0x00/+0x04/+0x08 = 4-byte Item fields
- +0x0C = flags
- +0x0D = player/network index
- +0x0E/+0x0F = tile X/Y
- +0x10 = operation type
- +0x11 = state
- +0x15 = player id

### Ghidra-gpt-sol-5.6-F030

Ghidra-gpt-sol-5.6-F027/Ghidra-gpt-sol-5.6-F029の成功部分は維持:
- direct falling-present visual
- custom fgobj capture at 0x59AC50
- synthetic inventory completion handle 4
- Player state 0x16 preservation

着地hook 0x593F4Cでcustom falling objectがmode 0->1になる最初の1回だけ:
- transient recordを shared+0x80 に構築
- Item shared+0x04をrecord+0x04/+0x08へcopy
- flags=0
- current player/network indexを0x305F6Cで取得し+0x0D
- saved worldX/worldYを+0x0E/+0x0F
- +0x10=0x0A
- +0x11=1
- player idを0x2F75CCで取得し+0x15
- `FieldActionType0A_GroundDropUpdate @ 0x5A0C2C` を直接call

stock FieldAction slot/poolは新規allocateしないため、inventory側synthetic completionとの競合を避ける。
`0x5A155C` / action 0x12は完全に不使用。

Impact cave:
- 0x838464-0x8384EB
- executable 0x84 bytes + 4-byte padding
- E-block length 0x88
- binary SHA-256 a228d276acb1f022a3994a09f2699ae1833262cf5a81140948fa7bd2c097aa77 (executable 0x84)
- existing B/BL targets into cave: 0

Ghidra export:
- acnl_jpn_v15_balloon_action0a_persistence_delta.xml
- size 34004
- SHA-256 a4b6a5b2e2229fe0009cdd7aad1615f8f216dc40ec52c66045714261370b8a14
- companion bytes size 4481
- bytes SHA-256 6a9acf6d2ef4e7aa0d2fa54b6e64272b8b242115db23d74701d771ac9d939a59

Hardware validation pending:
- selected Item still falls from balloon
- rock-destruction-like effect is gone
- same Item persists on ground
- lower-screen UI releases
- Player state remains 0x16

## Ghidra-gpt-sol-5.6-F031: Player-origin updaterを外し、balloon impact位置からpersistent ground objectを生成

Ghidra-gpt-sol-5.6-F030 hardware result:
- バグ/操作不能はない
- しかしcustom balloon dropではなく、通常ドロップとして見える

原因は`FieldActionType0A_GroundDropUpdate @ 0x5A0C2C`のdecompileで確定。
このupdaterはoperation 0x0Aを処理する際:
- record+0x0DからPlayerを取得
- Player+0x14/+0x18/+0x1Cをlocal Vec3へcopy
- Yへstock offsetを加える
- そのPlayer位置Vec3をfifth argumentとして`GroundItem_SpawnPersistentFgObj @ 0x59A4A0`へ渡す

従ってGhidra-gpt-sol-5.6-F030はballoon impact後に、Player位置を始点とした通常drop objectをもう一度生成していた。

`FgObjPresent_Update @ 0x593E68`も再decompile。
`0x593F4C`は:
- current Yがground target `object+0x140`以下になった後
- mode 0 caseで`FUN_00590EA0`を実行した直後
- mode byte `object+0x146`を1へ変更する
実際のground-contact transitionであることを再確認。

### Ghidra-gpt-sol-5.6-F031

Ghidra-gpt-sol-5.6-F030のoperation record / 0x5A0C2C callを完全撤去。
custom falling objectが0x593F4Cへ到達した最初の1回だけ:
- shared+0x68 custom falling-object identityを確認
- identityをclear
- Item* = shared+0x04
- tile X = shared+0x08
- tile Y = shared+0x00
- flag = 0
- fifth argument = `fallingObject+0x40` (impact時のcurrent Vec3)
- `GroundItem_SpawnPersistentFgObj @ 0x59A4A0`を直接call

これによりstock FieldAction state machineもoperation 0x0A updaterも通さず、persistent ground objectの生成primitiveだけを使用する。
開始位置はPlayerではなくballoon visualの着地点なので、通常drop animationを再生成しない。

maintained:
- Ghidra-gpt-sol-5.6-F027 direct balloon falling visual
- shared+0x04 original inventory Item
- custom fgobj capture at 0x59AC50
- synthetic completion handle 4
- Player state 0x16 preservation
- custom AcBalloon terminal A4 suppression

Impact cave:
- 0x838464-0x8384C3
- E-block 0x60 bytes
- direct BL at 0x8384A8 -> 0x59A4A0 (`EBF587FC`)
- existing main-image B/BL targets into cave: 0
- initialized aligned pointers into cave: 0

AR E-block audit:
- 0x838424: 0x40 exact
- 0x838464: 0x60 exact
- 0x838200: 0x1D8 exact
- 0x8383D8: 0x20 exact
- malformed/incomplete lines: 0

Ghidra-gpt-sol-5.6-F031 exchange:
- XML `acnl_jpn_v15_balloon_direct_ground_spawn_delta.xml` size 21158 SHA-256 a9a472d4b8c1a03e6cbe2bdbe2d0ea3772a66a76ca75170ef430895d0b6971ac
- bytes size 2409 SHA-256 5df78c7a0520caf66b933b2af90ca0e3ad00a419c4fb20c827fa9b72fb5a92f7

Hardware validation pending:
- still falls from balloon
- no second normal-drop animation
- ground Item remains after impact
- lower screen stays interactive
- Player state stays 0x16

## Ghidra-gpt-sol-5.6-F032: 0x0A visual生成を外し、stock post-visual field commitだけ再利用

Ghidra-gpt-sol-5.6-F031 hardware result:
- custom balloon 0x21の落下挙動は正常
- selected inventory Itemの見た目も正常
- しかし着地後は定着せず消滅
- 着地時に0x21由来の着地animationと0x0A由来の着地animationが同時再生され、二重表示に見える
- animation終了後、定着直前で消えるように見える

この観測でGhidra-gpt-sol-5.6-F031の誤認を修正。

### stock action 0x0A caseを命令単位で分離

`FieldActionType0A_GroundDropUpdate @ 0x5A0C2C` のcase 0x0A targetは `0x5A0E08`。

case 0x0Aでは:
- 0x5A0E90..0x5A0EB0: Player位置から開始Vec3を作り、`0x59A4A0`をcall
- 0x5A0EB0: `BL 0x59A4A0`
- success後 0x5A0EC0: current player id取得 (`0x2F75CC`)
- 0x5A0ECC: local/authority gate (`0x2F75E4(8,id)`)
- 0x5A0EDC..0x5A0EF8: X/Y, flags, player id, Item*を構成して `0x168E08`
- 0x5A0EFC..0x5A0F04: same X/Yで `0x599814`
- 0x5A0F94: record stateを2へ

従って`0x59A4A0`はpersistent field commitそのものではない。
Ghidra-gpt-sol-5.6-F031 hardwareで0x21 visualと同時に0x0A landing animationが出たことからも、`0x59A4A0`はoperation 0x0A側のdrop/landing visual constructorであることが実機確認された。

persistent field data側はその後段:
- `FieldTile_CommitItem @ 0x168E08`
- `FieldTile_RefreshAfterCommit @ 0x599814`
である。

### Ghidra-gpt-sol-5.6-F032

Ghidra-gpt-sol-5.6-F031のimpact hookから `0x59A4A0` callを完全撤去。

custom `fgobj_ObjectPresent` が `FgObjPresent_Update @ 0x593E68` のground-contact transition `0x593F4C` に到達した最初の1回だけ:
- shared+0x68 custom falling object identityを確認してclear
- fifth arg = Item* `shared+0x04`
- r0 = saved tile X `shared+0x08`
- r1 = saved tile Y `shared+0x00`
- r2 = flags 0
- r3 = current player id from `0x2F75CC`
- `FieldTile_CommitItem @ 0x168E08`
- then `FieldTile_RefreshAfterCommit @ 0x599814` with same X/Y
- stock `FgObjPresent_Update+0xE8 (0x593F50)`へ復帰

これにより:
- 0x21 falling/landing visualは1本だけ残す
- 0x0A visualを新規生成しない
- operation 0x0A/0x12 state machineを起動しない
- stock 0x0Aがvisual生成成功後に行うfield data確定だけを再利用する

Impact cave:
- 0x838464-0x8384E7 executable 0x84 bytes
- E-block 0x88 bytes (4-byte padding含む)
- payload SHA-256 `19c489e8952ec952f4ea94401665e0cc3c52ebfb3533cbeddde3626be9535f8c`
- caveは0x838500 replacement stringsより前に収まる

Ghidra annotations:
- 0x59A4A0 -> `GroundItem_SpawnDropVisual`
- 0x168E08 -> `FieldTile_CommitItem`
- 0x599814 -> `FieldTile_RefreshAfterCommit`
- 0x5A0C2C comment updated with split 0x0A path
- 0x593E68 comment updated with Ghidra-gpt-sol-5.6-F032 impact commit

Ghidra-gpt-sol-5.6-F032 exchange:
- XML `acnl_jpn_v15_balloon_field_commit_delta.xml` size 32069 SHA-256 `4cbb9cac1987701f822fc2c421c317672a6c7f7d02d72cddc674f583bacc4662`
- bytes size 2522 SHA-256 `15432816dee3d936dbe541369ea2793a277e7fa06fb4d241e50efd4f159cc339`

Hardware validation pending:
- 0x21 balloon landing animationだけが再生される
- 0x0A由来の二重animationが消える
- impact後に同じItemがfield tileへ定着する
- lower screen remains interactive
- Player state remains 0x16

### Ghidra-gpt-sol-5.6-F032 hardware validation — SUCCESS

実機確認:
- custom balloon/0x21 landing animationのみ再生され、Ghidra-gpt-sol-5.6-F031で発生した0x0A由来の二重表示は消失
- selected inventory Itemが風船から落下
- impact後、そのItemがfield tileへ正常に定着
- lower-screen UIは正常に解放され操作可能
- Player state 0x16を維持

従ってGhidra-gpt-sol-5.6-F032の`FieldTile_CommitItem @ 0x168E08 -> FieldTile_RefreshAfterCommit @ 0x599814`だけを0x21 impact時に実行する設計はhardware-validatedとする。

## Ghidra-gpt-sol-5.6-F033: custom falling objectをbusy tokenにしてdrop queueをlock

Ghidra-gpt-sol-5.6-F032 hardware success後の残課題:
- synthetic completion handle 4によりinventory UIは早期に解放される
- custom balloon/drop animation中でも次のinventory dropを開始できる
- 2回目dropがshared Item/worldX/worldY等を更新し、同じ場所への重複dropを起こし得る

既存のshared+0x68は`BalloonPresent_CreateAtTile @ 0x59ABE8`で生成されたexact custom `fgobj_ObjectPresent*`を保持し、Ghidra-gpt-sol-5.6-F032 impact hook `0x593F4C`でground-contactした最初の1回にclearされる。

このlifetimeはqueue lockにそのまま利用できる:
- custom falling object生成前: shared+0x68 == 0
- falling/drop animation中: shared+0x68 != 0
- ground impact/field commit開始: shared+0x68をclear

### precheck cave

既存drawing cave終了0x8381D7とballoon main cave開始0x838200の間のgap:
- `0x8381D8-0x8381F7`
- static ARM B/BL target into range: 0
- initialized aligned direct pointer into range: 0

payload:
- `0x8381D8 LDR r12,=0x01E81000`
- `0x8381DC LDR r12,[r12,#0x68]`
- `0x8381E0 CMP r12,#0`
- `0x8381E4 MVNNE r0,#0`  // -1
- `0x8381E8 BXNE lr`
- `0x8381EC B 0x838200`
- literal/padding at 0x8381F0/0x8381F4

`Player_DropItem @ 0x596084`内のstock Item_PlaceItem callsite hook:
- old `0x596188 EB0A881C -> 0x838200`
- new `0x596188 EB0A8812 -> 0x8381D8`

busy時は`r0=-1`で元callerへ即returnする。
BsMenuItem stock callbackは-1だけをimmediate failureとして扱うため:
- 2回目Itemを消費しない
- completion handle待機stateへ入らない
- stock Item_PlaceItem fallbackを実行しない
- shared drop coordinates/Itemを上書きしない

not busy時は0x838200へbranchし、Ghidra-gpt-sol-5.6-F032のhardware-validated custom balloon pathをそのまま実行する。

### lock/unlock timing

lock setに専用writeは不要。
`shared+0x68`はcustom falling object生成時に同期的に設定され、Player_DropItemがsynthetic handle 4を返すより前に有効になる。

unlockはGhidra-gpt-sol-5.6-F032 impact hookがexact custom objectのground contactを検出した時の既存:
`MOV r6,#0 ; STR r6,[shared,#0x68]`
を利用する。

従ってuser inputから見たlock windowは、custom falling object生成完了からground impactまで。

Ghidra-gpt-sol-5.6-F033 Ghidra scoped export:
- XML `acnl_jpn_v15_balloon_queue_lock_delta.xml` size 26593 SHA-256 `0007605911aac0b1859c96a56548bd7e7a9a21bddb7981c4741a4469713b1e39`
- bytes size 1237 SHA-256 `0fd2ad6fbe827e157db4cb62331a691b2d414118db1a44b2f35ed1e5f683aa66`

Hardware validation pending:
- 1個目のcustom balloon drop中に2個目をdropしても2個目はfieldへ出ない
- 2個目inventory Itemは残る
- UI lock/操作不能にならない
- 1個目impact後は次のdropを正常に開始できる

## Native drop queue re-audit (post Ghidra-gpt-sol-5.6-F032)

User correction accepted: ACNL already owns the drop queue; adding a second custom busy lock before fully understanding the native lifecycle was the wrong integration direction.

Address clarification:
- 0x955FF4 = ItemToPlace (4-byte empty/sentinel Item), not the queue base.
- native four-slot queue = g_DropDataTable @ 0x9AE15C, 0x12 bytes x 4.
- g_FieldActionActive @ 0x9AE1A4 and g_DigRecordArray @ 0x9AE244 are separate structures.

DropData layout (IDA comment + JPN instruction audit):
- +00 ItemToReplace
- +04 ItemToPlace
- +08 ItemToShow
- +0C wX
- +0D wY
- +0E DropType
- +0F State
- +10 SlotIndex
- +11 Flags

Native State lifecycle:
- 0 = free
- Item_PlaceItem 0x59E5B4 allocates first free slot and sets 1
- FieldAction_Dispatch 0x59E8F8 case 1/2 sets the originating slot to 2/3
- 2 = success completion pending consumption
- 3 = failure completion pending consumption
- 0x596C84 polls by returned slot index and, for ordinary DropType 0x0A, consumes 2/3 then clears DropType/State back to 0

The slot index is propagated through FieldAction_QueueToRecord @ 0x59EBE8 via DropData+0x10 into processFlags low two bits, which is how completion packets address the correct queue slot.

Inventory menu contract:
- FUN_0019AD30 stores Player_DropItem return in BsMenuItem+0xD8.
- FUN_0019AF8C polls 0x596C84(handle).
- 0/1 -> wait.
- 2 -> inventory source slot removal + UI refresh/advance.
- 3 -> error path.
Thus the native DropData queue is also the inventory UI completion token.

IDA vc_DROPM comment at 0x59E5DC explicitly documents that the old rapid-drop cheat bypasses the State scan and always overwrites slot 0, destroying an in-flight record. This independently confirms the intended queue protection semantics.

Impact on current balloon design:
- Ghidra-gpt-sol-5.6-F032 remains HW VERIFIED for visual/state/persistence.
- synthetic handle 4 is the reason a second local inventory drop can start early: its 0x596C84 special case returns 2 immediately and bypasses native State=1.
- Ghidra-gpt-sol-5.6-F033 custom shared+0x68 busy lock is RETIRED as the future integration direction.
- current AR restored to hardware-verified Ghidra-gpt-sol-5.6-F032 baseline.
- next integration must allocate/use a real DropData slot, keep State=1 during balloon flight, set that same slot to 2 only after Ghidra-gpt-sol-5.6-F032 impact+field commit, and let stock 0x596C84 free it and release the UI. Failure should use State=3.
- no new queue implementation is introduced by this analysis.

## Ghidra-gpt-sol-5.6-F034: native DropData queue integration

Ghidra-gpt-sol-5.6-F032 remains the hardware-verified visual/persistence baseline. Ghidra-gpt-sol-5.6-F033's independent busy flag is retired.

### Key integration point

Stock `Item_PlaceItem @ 0x59E5B4` is now allowed to run normally through native DropData allocation and initialization.

At `0x59E6A4`, immediately after:
- first free `g_DropDataTable @ 0x9AE15C` slot is selected,
- three Item values are copied,
- X/Y/DropType/Flags are stored,
- `State=1` is written,

but before the normal FieldAction record is constructed, Ghidra-gpt-sol-5.6-F034 intercepts only the inventory caller.

The discriminator is the saved LR in the Item_PlaceItem frame:
- prologue pushes r0-r3,r4-r11,lr and subtracts 0x1C,
- saved LR is therefore `[sp+0x4C]`,
- inventory Player_DropItem callsite `0x596188` returns to `0x59618C`.

Only when:
- saved LR == 0x59618C, and
- DropData.DropType == 0x0A,

does the custom balloon path run. Otherwise execution resumes stock at `0x59E6A8`.

Queue-full handling remains entirely stock: if all four DropData entries are nonzero, Item_PlaceItem returns -1 before the custom intercept is reached.

### Native handle

The selected DropData pointer is saved at custom shared+0x6C.

No synthetic handle is returned.

On custom success the cave branches directly to the stock Item_PlaceItem epilogue `0x59E70C`, which returns the real native slot index in r0.

Consequences:
- BsMenuItem+0xD8 stores slot 0..3,
- stock `DropQueue_PollAndFinalize @ 0x596C84` sees State=1 while the balloon is active,
- lower-screen inventory stays in its normal wait state,
- another local inventory drop cannot start through the same menu action,
- no independent custom queue lock is needed.

The old `0x596C84(handle==4)->2` hook is removed and `0x596C84` is fully stock.

### Visual/persistence path

Ghidra-gpt-sol-5.6-F032 behavior is preserved:
- custom AcBalloon identity guard,
- selected inventory Item used for the falling present,
- only 0x21 balloon landing visual,
- impact field commit via `FieldTile_CommitItem @ 0x168E08`,
- tile refresh via `FieldTile_RefreshAfterCommit @ 0x599814`,
- Player state 0x16 retention via the terminal A4 guard.

The exact custom falling-object capture moved from cave 0x8383D8 to 0x838308.

### Completion timing

Ghidra-gpt-sol-5.6-F032 used shared+0x68 only until first impact. Ghidra-gpt-sol-5.6-F034 keeps the exact custom falling-object pointer through mode 0 -> mode 1.

At `FgObjPresent_Update @ 0x593E68`:
- mode 0 ground contact stores mode=1 at `0x593F4C`,
- Ghidra-gpt-sol-5.6-F032 field commit still runs there,
- shared+0x68 is intentionally not cleared at impact.

On the next mode-1 update, stock dispatch reaches `0x593F34`.

Ghidra-gpt-sol-5.6-F034 hooks `0x593F34` and, only when r4 == shared+0x68:
- loads the exact native DropData pointer from shared+0x6C,
- writes `State=2` to entry+0x0F,
- clears shared+0x6C and shared+0x68,
- executes the original `MOV r0,#1`,
- resumes stock at `0x593F38`.

This means queue completion is delayed until the falling-present visual enters its stock cleanup mode, rather than being reported immediately at request time or at initial impact.

Stock `0x596C84` then consumes State=2, performs ordinary type-0x0A completion semantics, clears the DropData slot back to State=0, and returns success to BsMenuItem.

### Failure/fallback

If the custom eligibility checks fail, the hook resumes stock `Item_PlaceItem` before FieldAction construction.

If custom AcBalloon creation fails after native slot allocation:
- shared+0x6C is cleared,
- execution resumes stock at 0x59E6A8,
- the already initialized native slot continues through the normal drop path.

Thus there is no stranded custom State=1 slot on the known spawn-failure path.

### Cave map

- 0x8381D8-0x838307: native-slot custom interceptor (0x130 bytes)
- 0x838308-0x838327: custom falling-object capture (0x20)
- 0x838330-0x83837F: custom BalloonPresent landing hook (0x50)
- 0x838380-0x8383BF: custom AcBalloon state helper (0x40)
- 0x8383C0-0x8383EF: native DropData completion hook (0x30)
- 0x838424-0x838463: terminal A4 reaction guard
- 0x838464-0x8384EB: impact field commit
- 0x838400-0x838423 remains untouched

### Hooks

ON:
- 0x596188 remains stock `BL Item_PlaceItem` = EB002109
- 0x59E6A4 -> 0x8381D8 = EA0A66CB
- 0x598BEC -> 0x838330 = EA0A7DCF
- 0x59AC50 -> 0x838308 = EA0A75AC
- 0x593F34 -> 0x8383C0 = EA0A9127
- 0x593F4C -> 0x838464 = EA0A9144
- 0x5C5A30 -> 0x838424 = EA09CA7B
- 0x596C84 is stock; synthetic poll hook removed

OFF restores:
- 0x59E6A4 = E1A0000D
- 0x593F34 = E3A01000
- plus the previously known Ghidra-gpt-sol-5.6-F032 restores.

### Static validation

- all AR payload lines are complete 2-word lines,
- every E-block encoded word count equals its declared byte length,
- all direct branch targets were recomputed from the final cave addresses,
- synthetic handle-4 compare/poll code is absent,
- Player_DropItem's stock BL to Item_PlaceItem is present.

Hardware validation pending:
- first inventory drop uses the 0x21 balloon visual and persists,
- source inventory Item remains present while State=1/in flight,
- a second drop cannot begin through the inventory UI during flight/landing,
- on mode-1 cleanup, State becomes 2, source Item is removed once, UI releases,
- a subsequent drop after completion works normally,
- no duplicate 0x0A landing visual,
- Player state remains 0x16.

## Ghidra-gpt-sol-5.6-F035: stock inventory-call signature for native queue interception

Ghidra-gpt-sol-5.6-F034 hardware result:
- behavior regressed to an ordinary normal drop, matching the visible result previously seen in Ghidra-gpt-sol-5.6-F030
- no crash or UI lock was reported
- therefore the custom branch at the post-allocation Item_PlaceItem intercept was not being selected on hardware, or it fell back before custom balloon creation

Static re-audit:
- Item_PlaceItem prologue is `STMDB sp!,{r0-r11,lr}; SUB sp,sp,#0x1C`
- saved LR is indeed `[sp+0x4C]`
- Player_DropItem calls Item_PlaceItem at `0x596188`, nominal LR `0x59618C`
- despite that static layout, LR-based discrimination did not work as a reliable hardware selector and is retired

IDA already documents a stronger stock signature for ordinary inventory drop:
`Player_DropItem -> Item_PlaceItem(0x0A, g_EmptyItem, ItemToPlace, ItemToShow, ...)`

At the callsite:
- 0x596178 = MOV r0,#0x0A
- 0x596180 = LDR r1,[pc,#0x24]
- literal 0x5961AC = 0x00955FF4
- 0x596188 = BL Item_PlaceItem

Inside Item_PlaceItem, after its push/sub frame:
- saved original r0 is [sp+0x1C]
- saved original r1 is [sp+0x20]
- saved original r2 is [sp+0x24]
- saved original r3 is [sp+0x28]

Ghidra-gpt-sol-5.6-F035 therefore changes only the custom-selector predicate:
- old: saved LR [sp+0x4C] == 0x59618C
- new: saved original r1 [sp+0x20] == 0x955FF4
- still require DropData.DropType(+0x0E) == 0x0A
- existing Ghidra-gpt-sol-5.6-F032 inventory-context globals and custom spawn/fallback behavior remain unchanged

All native queue behavior from Ghidra-gpt-sol-5.6-F034 is retained:
- stock Item_PlaceItem allocates one of four DropData slots
- queue full still returns -1 in stock code
- native slot remains State=1 during custom balloon flight/landing
- Ghidra-gpt-sol-5.6-F032 impact field commit remains unchanged
- exact slot becomes State=2 only after fgobj_ObjectPresent mode-1 cleanup at 0x593F34
- stock DropQueue_PollAndFinalize consumes State=2, removes inventory source once, clears slot to State=0, and releases UI
- synthetic handle 4 remains removed

AR cave change is only two words:
- 0x8381D8: E59D004C -> E59D0020
- literal 0x8382F4: 0x0059618C -> 0x00955FF4

Hardware validation pending.

## Ghidra-gpt-sol-5.6-F036: native DropData allocation from the Ghidra-gpt-sol-5.6-F032 callsite context

Hardware results leading here:
- Ghidra-gpt-sol-5.6-F034: ordinary normal drop
- Ghidra-gpt-sol-5.6-F035: unchanged ordinary normal drop
- both versions moved AcBalloon creation into Item_PlaceItem after native DropData allocation
- changing the post-allocation selector from saved LR to saved original r1==0x955FF4 did not change hardware behavior

Conclusion:
- the selector was not the material problem
- moving the custom balloon spawn into Item_PlaceItem's post-allocation execution context was the regression
- Ghidra-gpt-sol-5.6-F032's hardware success depended on executing the custom spawn from the Player_DropItem callsite context at 0x596188

### Ghidra-gpt-sol-5.6-F036 split design

The stock queue allocation and the custom visual creation are now split.

At Player_DropItem 0x596188:
- the hook enters a new high-page cave at 0x838E00
- SP is left untouched before calling stock Item_PlaceItem, so all seven stack arguments remain exactly stock
- the same Ghidra-gpt-sol-5.6-F032 eligibility globals are checked: 0x948DD4 must be nonzero and 0x948DDC must be zero
- if not eligible, the cave tail-jumps to stock Item_PlaceItem with LR still 0x59618C

For an eligible inventory drop:
- save original return LR in shared+0x78
- set transient allocator-arm shared+0x70=1
- BLX stock Item_PlaceItem @ 0x59E5B4

At Item_PlaceItem 0x59E6A4:
- hook now points to a tiny allocator-stop cave at 0x838F98
- no caller signature, no balloon spawn, no coordinate work occurs here
- if shared+0x70==0: execute original MOV r0,sp and resume stock 0x59E6A8
- if armed: save exact DropData* r4 at shared+0x6C and return through stock epilogue 0x59E70C before FieldAction construction
- native slot scanning, queue-full -1, Item copies, X/Y, DropType, Flags and State=1 all remain stock

Back in the 0x838E00 callsite cave:
- clear shared+0x70
- preserve the real native slot index at shared+0x74
- world X/Y are read from the original Player_DropItem stack arguments
- the selected Item is read from Player_DropItem's local Item copy at original sp+0x28
- the same Ghidra-gpt-sol-5.6-F032 Vec3 construction and AcBalloon spawn path is executed
- custom helper at 0x838380 is unchanged
- return to 0x59618C with r0 = the real native slot index

Thus the queue is stock, but AcBalloon creation is again performed from the same caller context that was hardware-verified in Ghidra-gpt-sol-5.6-F032.

### Failure behavior

If native queue is full:
- stock Item_PlaceItem returns -1
- Ghidra-gpt-sol-5.6-F036 returns that same -1 to Player_DropItem/BsMenuItem

If custom AcBalloon spawn fails after native slot allocation:
- exact DropData.State is changed to 3
- the real slot index is returned
- stock DropQueue_PollAndFinalize handles the error/finalization path

### Completion

The Ghidra-gpt-sol-5.6-F034/Ghidra-gpt-sol-5.6-F035 native completion path is retained:
- custom falling object remains exact identity at shared+0x68
- Ghidra-gpt-sol-5.6-F032 impact commit 0x168E08 -> 0x599814 is unchanged
- after mode-1 visual cleanup at 0x593F34, exact DropData* shared+0x6C receives State=2
- stock 0x596C84 consumes success, removes the source inventory Item once, clears the slot to State=0, and releases UI
- synthetic handle 4 remains absent

### Cave layout

Existing low caves are preserved:
- 0x838308-0x838327 custom falling-object capture
- 0x838330-0x83837F BalloonPresent landing substitution
- 0x838380-0x8383BF AcBalloon helper
- 0x8383C0-0x8383EF native queue completion
- 0x838424-0x838463 terminal A4 guard
- 0x838464-0x8384EB Ghidra-gpt-sol-5.6-F032 impact field commit

New high caves:
- 0x838E00-0x838F93 callsite/native-allocation bridge (0x194 bytes)
- 0x838F94 left as padding separation
- 0x838F98-0x838FC3 allocator-stop cave (0x2C bytes)

This leaves 0x838500-0x838DFF (0x900 bytes) untouched for the previously reserved replacement-string area.

Static original-image audit for 0x838E00-0x838FC4:
- ARM B/BL targets into range: 0
- aligned direct 32-bit initialized pointers into range: 0
- source image is part of the known executable zero-fill page after .text

Hooks:
- 0x596188 -> 0x838E00 = EB0A8B1C
- 0x59E6A4 -> 0x838F98 = EA0A6A3B
- existing Ghidra-gpt-sol-5.6-F032/Ghidra-gpt-sol-5.6-F034 landing/capture/completion/state hooks retained
- stock 0x596C84 remains unhooked

Hardware validation pending.

## Ghidra-gpt-sol-5.6-F037: Ghidra-gpt-sol-5.6-F036 crash-dump root cause and ABI-safe bridge

Hardware:
- Ghidra-gpt-sol-5.6-F036 crashed immediately when starting the inventory drop.
- crash dump: `crash_dump_00000010.dmp`
- SHA-256: `c350a6c97074e160f46bae592007ca3c8620c70866f0202075be9941b27df128`

Crash-dump register block (r0-r15 beginning at file offset 0x28):
- r0 = 0x009AE160
- r1 = 0x00000000
- r2 = 0x00003B68
- r3 = 0x00000001
- r4 = 0x009AE15C
- r5 = 0
- r6 = 0x52
- r7 = 0x35
- r8-r11 = 0
- r12 = 0x0059E5B4
- sp = 0x0FFFFD28
- lr = 0x0059E618
- pc = 0x002FC878
- cpsr = 0x10

Instruction correlation:
- `0x59E60C LDR r1,[sp,#0x24]`
- `0x59E610 ADD r0,r4,#4`
- `0x59E614 BL 0x2FC878`
- return LR = `0x59E618`
- `0x2FC878 LDRH r2,[r1]`

At the fault:
- r4 = 0x9AE15C = DropData slot 0 base
- r0 = 0x9AE160 = slot0 +4 = ItemToPlace destination
- r1 = 0 = source Item* passed to ItemID::Write
- therefore the crash is a NULL source dereference inside stock Item copy

The dump also contains `0x838E38`, the instruction immediately after Ghidra-gpt-sol-5.6-F036's BLX Item_PlaceItem, confirming the call originated from the new high cave.

Root cause:
- Ghidra-gpt-sol-5.6-F036 entered the high cave with the correct stock Item_PlaceItem ABI:
  r0=0x0A, r1=0x955FF4, r2=actual Item*, r3=shown Item*
- but eligibility code reused/clobbered r1/r2/r3 before BLX Item_PlaceItem
- Item_PlaceItem therefore received invalid argument registers
- this is an ABI-preservation bug in Ghidra-gpt-sol-5.6-F036, not a native DropData queue design failure

### Ghidra-gpt-sol-5.6-F037 fix

Before any eligibility logic:
- save original r0/r1/r2/r3 to shared+0x7C/+0x80/+0x84/+0x88
- save original LR to shared+0x78

Before BLX stock Item_PlaceItem:
- restore all original r0-r3 exactly
- do not alter SP, so all stock stack arguments remain at their original locations

Before calling stock:
- copy world X/Y from original stack into shared+0x08/+0x00
- copy the full Item from original r2 Item* into shared+0x04
- this removes later dependence on Player_DropItem stack-frame offsets

After native slot allocation:
- save returned slot index at shared+0x74
- reconstruct exact DropData* as `0x9AE15C + slot*0x12` and store at shared+0x6C
- no longer depend on Item_PlaceItem's transient r4 value being exported by the hook

During custom balloon construction:
- preserve all callee-saved registers r4-r11 plus LR around the custom path
- Ghidra-gpt-sol-5.6-F032 coordinate/Vec3/AcBalloon logic is then run from the original 0x596188 callsite context

Allocator-stop hook:
- moved to 0x838FD0
- armed: jump to stock Item_PlaceItem epilogue 0x59E70C before FieldAction construction
- unarmed: execute original MOV r0,sp and resume 0x59E6A8

Failure paths:
- native queue full returns the real stock -1
- custom spawn failure marks the exact native DropData.State=3 and returns its real handle for stock failure finalization

Queue completion/persistence remains unchanged:
- Ghidra-gpt-sol-5.6-F032 impact field commit 0x168E08 -> 0x599814
- exact native DropData.State=2 after mode-1 cleanup at 0x593F34
- stock 0x596C84 consumes/clears the slot and releases inventory UI
- synthetic handle 4 remains absent

### Ghidra-gpt-sol-5.6-F037 cave boundaries

- main bridge: 0x838E00-0x838FCF, 0x1D0 bytes
- allocator-stop: 0x838FD0-0x838FF7, 0x28 bytes
- highest written address is below 0x839000 .rodata start

Static AR audit:
- all E-block byte counts exact
- malformed lines: 0
- 0x596188 -> 0x838E00
- 0x59E6A4 -> 0x838FD0
- synthetic 0x596C84/handle-4 hook absent

## Drop/balloon pipeline re-analysis after Ghidra-gpt-sol-5.6-F037

Current implementation status:
- Ghidra-gpt-sol-5.6-F032 is restored as the current AR baseline because it is the last hardware-verified implementation for visual/persistence/state.
- Ghidra-gpt-sol-5.6-F034/Ghidra-gpt-sol-5.6-F035 are retired: they regressed to normal drop by mixing custom balloon with Item_PlaceItem/normal FieldAction lifecycle.
- Ghidra-gpt-sol-5.6-F036/Ghidra-gpt-sol-5.6-F037 are retired: both violated hidden call contracts while trying to bridge native queue through stock Item_PlaceItem.

Critical corrections:
1. Item_PlaceItem has two responsibilities: native DropData allocation and immediate normal FieldAction dispatch. These must not be coupled for custom balloon.
2. Natural balloon-present landing uses a separate 0x21 FieldAction/active-table path and does not allocate a four-slot DropData handle.
3. 0x57ADFC is not balloon-specific. Static scan finds 105 direct BL callers. It stages r3 and caller stack arg#5 into 0x947FE8/0x947FEC before generic creation.
4. crash_dump_00000011 proves Ghidra-gpt-sol-5.6-F037 violated that contract: pc=0x57AF18, r2=0x947FE8, r1=0xA. The constructor dereferenced 0x947FEC==0xA. Ghidra-gpt-sol-5.6-F032 correctly supplied stack arg#5=0.
5. DropQueue_PollAndFinalize 0x596C84 State=1 is a pure wait. For ordinary DropType 0x0A, State=2 follows generic clear and returns 2; it does not replay Item_PlaceItem.

Design selected for next implementation:
- use the native g_DropDataTable slot only as inventory UI completion token;
- reserve a free 0x12-byte slot directly at the Ghidra-gpt-sol-5.6-F032 0x596188 context;
- do not call Item_PlaceItem / FieldAction_QueueToRecord / FieldAction_Dispatch;
- keep the exact Ghidra-gpt-sol-5.6-F032 custom balloon spawn and impact persistence path;
- return the real native slot index to BsMenuItem;
- keep State=1 while balloon visual is active;
- after exact custom falling-present mode1 cleanup, set that slot State=2;
- let stock 0x596C84 clear it and let BsMenuItem run normal success handling.

Detailed design is in docs/drop_pipeline_reanalysis.md.
No new AR has been assembled from this design yet.


## Ghidra-gpt-sol-5.6-F039 design freeze — AR組立前の独立二系統検証

Ghidra-gpt-sol-5.6-F038をさらに独立再検証した結果、実装方向はsynthetic handle 4のまま維持するが、timing前提を修正する。

重要な訂正:
- 旧Ghidra-gpt-sol-5.6-F025/Ghidra-gpt-sol-5.6-F027の「state helperとの同期タイミング」説明は相互に矛盾するため撤回。
- raw ModuleVillage terminal file 0x19BA8で直接確定できるのは `0x598BEC landing attempt -> 0x5C5A30 A4 reaction -> cleanup` の順序。
- Ghidra-gpt-sol-5.6-F039はstate setterとの同期/遅延を仮定しない。

AR実装時の固定設計:
1. state setter前に custom AcBalloon* (+0x60), falling pointer=0 (+0x68), synthetic WAIT=1 (+0x6C) をarm。
2. helper return後のactor pointer再保存を撤去。
3. handle 4 pollは+0x6Cを直接返す。1=wait, 2=success, 3=failure。
4. 0x59AC50 captureはvisual生成成功marker。
5. exact A4 guard時に+0x68==0ならstatus=3。
6. exact impactで0x168E08 -> 0x599814の後だけstatus=2、続いて+0x68 clear。
7. mode-1 cleanupは待たない。falling object自身がItem/positionを保持する。
8. Item_PlaceItem/native DropData/normal FieldActionはcustom-success pathへ再導入しない。

具体設計・cave layoutは `docs/balloon_drop_gf039_design.md`。  
独立検証証拠は `work/evidence/balloon_drop_dual_verification_20260916.md`。

**この節ではAR payloadを作成しない。current ARはGhidra-gpt-sol-5.6-F032のまま。**


## Ghidra-gpt-sol-5.6-F039 implementation

Current AR is now Ghidra-gpt-sol-5.6-F039:
`artifacts/action_replay/acnl_jpn_v15_balloon_drop.txt`.

Changes from hardware-verified Ghidra-gpt-sol-5.6-F032:
1. state helper pre-arms exact AcBalloon identity, synthetic WAIT=1, and clears falling-object identity before the state transition;
2. the post-helper actor re-save is removed;
3. handle 4 poll returns persistent status 1/2/3 instead of immediate success;
4. exact terminal guard publishes failure if no falling object was captured;
5. exact impact commits `0x168E08 -> 0x599814`, clears object identity, then publishes SUCCESS=2 last.

No native DropData allocation or normal FieldAction path was reintroduced.

Static validation is complete. Hardware result is pending. During the first validation pass, do not disable the AR while a synthetic handle-4 operation is active.


## Ghidra-gpt-sol-5.6-F039 hardware result

**SUCCESS.**

The asynchronous synthetic-completion implementation behaves as intended on hardware. Ghidra-gpt-sol-5.6-F039 is now the current hardware-verified AR baseline.
