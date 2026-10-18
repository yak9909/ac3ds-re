# 風船生成・撃墜DROP・任意Item配置

## 結論

村を飛ぶ風船は `ModuleVillage.cro` の `AcBalloon` Actorである。自然生成、パチンコ弾とのcollision、破裂state、プレゼントの落下/地面配置が分離されている。

この構造を利用し、**通常ドロップ対象マスの上空へ風船を生成し、初期化後すぐ破裂させ、任意Itemを既存の風船プレゼント経路で配置するチートは実装可能**と判断する。

静的解析の確度はHIGH。実機でのcheat実行は未検証。

## 生成

`BsVillageBalloonMgr` の自然生成updateは ModuleVillage CRO file `0x1688`（code segment relative `+0x1508`）。

生成直前のARM:
```asm
ldr  r0, [literal]        ; -> main 0x8813A6
ldrb r2, [r4,#0x595]     ; variant
add  r3, sp, #4           ; Vec3 position
ldrh r0, [r0]             ; typeId = 0x00F1
mov  r1, r4               ; BsVillageBalloonMgr*
str  0, [sp]              ; fifth arg
bl   ActorFactory_CreateByTypeId
```

main:
`ActorFactory_CreateByTypeId = 0x57ADFC`

したがって自然生成call shapeは概ね:
（疑似C を省略。原本は _local/legacy-src/…）

### singleton

- `*(BsVillageBalloonMgr**)0x948DD4`
- `*(AcBalloon**)0x948DDC`

`AcBalloon` ctorが `0x948DDC` へselfを書き、destructor/cleanupが0へ戻す。stock systemはcurrent balloonを1本のglobalで管理するため、cheatも `0x948DDC != 0` の間は追加spawnしない方が安全。

## variant

`AcBalloon` の内部variant getterに対する分岐とdrop選択から:

| variant | 意味 | 最終Item |
|---:|---|---:|
| 0 | 通常 | `0x2036` プレゼント(毎回違う) |
| 1 | 銀 | `0x3362` 銀のパチンコ |
| 2 | 金 | `0x3363` 金のパチンコ |
| 3 | イベント | `0x211B` 空飛卵 |

銀/金は同一Actor内で2/3個の風船partを持つ。

## state machineと安全な即破裂

AcBalloon内部state setterは ModuleVillage CRO file `0xD304`。CRO code segmentはfile `0x180`から始まるため、code/text-relative offsetは **`+0xD184`**。

この関数へのdirect callを6箇所確認:
`0x19714, 0x198BC, 0x19A98, 0x1A104, 0x1A810, 0x1A838`。

初期state:
- 通常: 0
- 銀: 2
- 金: 4

銀/金の中間stateは残存balloon part数に応じて次stateを選び、0個になった場合はいずれも **state 1** へ遷移する。従って生成済みActorを自然な最終破裂/dropへ送る最短経路は:

```c
AcBalloon_SetState(balloon, 1);
```

ただしctor完了直後の同一call stackで実行せず、少なくとも1 update通してmodel/collision/state初期化を完了させる。

### state 1 drop

CRO file `0x19BA8` はvariantに応じたItemを作り、impact XYZとともにmain `0x598BEC` へ渡し、その後cleanupへ進む。

## プレゼント配置

main `0x598BEC = BalloonPresent_TryLandAndPlace`。

処理:
1. impact XYZをworld tileへ変換。
2. 対象tileの配置可否を検査。
3. 必要なら周囲候補も探索。
4. `FieldAction_RegisterActive(0x21, x, y, room, 1)`。
5. `BalloonPresent_BuildFieldActionRecord (0x59EB3C)`。
6. `BalloonPresent_CreateAtTile (0x59ABE8)`。
7. 内部で `FgObjPresent_SpawnFalling (0x593D0C)` が0x148 bytesの `fgobj_ObjectPresent` を生成。

これは既存Dropperの `DropType=0x0A` / `PlaceItem 0x59FC7C` とは別系統。

## 任意Item化する推奨設計

単にstate 1へ送るだけでは、Itemはvariant由来の固定値になる。任意Itemを落とすには、自然な処理を破壊しない **one-shot Item override** が適する。

推奨:
1. 村/ModuleVillageロード中であることを確認。
2. `mgr = *(void**)0x948DD4` が非NULL、`*(void**)0x948DDC == NULL` を確認。
3. 通常Dropperと同じ対象world tileを決定。
4. tile中心X/Zと地形高＋風船高度からVec3を作る。自然spawn helper（CRO file `0x12388`）も参考にする。
5. `ActorFactory_CreateByTypeId(0xF1,mgr,0,&pos,0)`。
6. 1 update待つ。
7. `0x598BEC` 入口にone-shot overrideをarmする。次の風船drop callだけparam2の `Item*` を希望Itemへ差替え、直後に解除。
8. ModuleVillage text baseから `+0xD184` のstate setterを解決し、`SetState(balloon,1)`。

これにより破裂effect、自然なpresent落下、FieldAction登録、Actor cleanupをstockコードへ任せられる。

### なぜ0x598BECを直接呼ぶだけではないか

`0x598BEC(position,item)` を直接呼べばItem配置自体は可能だが、AcBalloonの破裂effect/state/despawnが別途必要になる。見た目とlifetime整合性を保つなら、state 1＋one-shot overrideの方が安全。

## 注意点

- CRO file offsetをruntime absolute addressとして使わない。state setterは code/text-relative `+0xD184` としてロード済みModuleVillageのtext baseから解決する。
- `0x598BEC` は周囲候補へずらす場合がある。厳密に指定tileへ置きたい場合は事前に配置可能判定を行い、不可ならspawnを中止する。
- online同期は未検証。FieldAction/network recordを通るため、まずofflineで確認する。
- stock singletonを尊重し、自然風船が存在中はcheat balloonを重ねない。
