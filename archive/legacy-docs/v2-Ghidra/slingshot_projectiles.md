# パチンコ弾の固定スロット・座標・生成上限

## 結論

パチンコの玉は「射撃モーションだけで表示位置が決まる飾り」ではない。Player Actor内に固定確保されたprojectile slotが座標・速度・衝突・描画状態を保持し、飛翔中は毎フレーム更新される。

ただし、各発を独立Actorとしてheapに追加していく方式でもない。**Playerごとに3 slot固定**であり、次の射撃は同じslotを再初期化する。

確度: **MEDIUM**（複数静的証拠、実機未観測）。

## 発射数

`SlingshotProjectile_FireReset (0x00660710)`:

| 装備 | item ID | 使用slot数 |
|---|---:|---:|
| レンタル/通常 | `0x3360/0x3361` | 1 |
| 銀 | `0x3362` | 2 |
| 金 | `0x3363` | 3 |

関数内のcountはdefault 1、silverで2、goldで3になる。発射loopはこのcount分だけslot 0から初期化する。

## 3発はそれぞれ座標を持つ

slot strideは `0x8C`。

| 内容 | slot 0 | slot 1 | slot 2 |
|---|---:|---:|---:|
| velocity XYZ | `+0x1180/+0x1184/+0x1188` | `+0x120C/+0x1210/+0x1214` | `+0x1298/+0x129C/+0x12A0` |
| position XYZ | `+0x118C/+0x1190/+0x1194` | `+0x1218/+0x121C/+0x1220` | `+0x12A4/+0x12A8/+0x12AC` |
| collision | `+0x1140` | `+0x11CC` | `+0x1258` |
| visual handle | `+0x1198` | `+0x1224` | `+0x12B0` |

active maskは `Player+0x12C8` のbit 0..2。

`SlingshotProjectile_UpdateAll (0x00665F14)` は必ず `slot=0; slot<3; slot++` で走査し、active slotごとに

```
position.x += velocity.x
position.y += velocity.y
position.z += velocity.z
```

を行い、衝突状態と描画transformもそのslotのpositionで更新する。

したがって金の3発は「1個の座標から3個描画している」のではなく、**3発それぞれが独立した位置状態を持つ**。

## 連射時に前の弾が消える理由

発射処理は新規slotを追加せず、slot 0..N-1へ発射時の位置・速度を再書込みする。

さらに各slotで

1. `FUN_002e67d4(slot.visual)` — 前の描画インスタンスを解除/無効化
2. `FUN_002078d8(slot.visual, 0x213, slot.position, ...)` — 汎用描画プールから表示インスタンスを再取得

を実行する。

従って観察される「直前の弾が消えて新しい弾が出る」は二層に分かれる。

- 論理projectile: **同じ固定slotの座標・速度を書き換えて再利用**
- 描画instance: **旧instanceを解除し、新しい/再利用されたpool instanceへ再バインド**

独立Actorが射撃ごとに積み上がる実装ではない。

## モーションとの関係

Player state `0xA2`:

- enter `0x0067ABFC`: shoot animation `0x57` を開始
- update `0x0066D02C`: `AnimSlot_CrossedMarker(...,0)` 到達時に `SlingshotProjectile_FireReset` を呼ぶ

つまり **発射タイミングは射撃モーションに同期**している。

一方、飛翔更新 `SlingshotProjectile_UpdateAll` は通常Player update `0x00654640` のitem category `0x12` 分岐から呼ばれる。射撃state終了後もprojectile slotは独立して更新されるため、弾の軌跡そのものがモーションデータに結び付いているわけではない。

## 最大数

stockコードはactive bitを3個しか扱わず、update loopも固定で3回。したがって **1 Player Actorあたり同時最大3発**。

金を連射してもslot 0..2を再初期化するため、6発・9発と蓄積しない。

オンライン等でPlayer Actorが複数存在する場合のゲーム全体上限は今回未確認。この「3」は1 Actor内部のslingshot subsystem上限。
