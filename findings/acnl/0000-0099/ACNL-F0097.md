---
id: ACNL-F0097
aliases:
- F-59
title: F-59 FOXXY 時間変更チートの残り 2 パッチ — 演出をメニュー姿勢に差し替えている — `HIGH`
summary: F-58 で未解析だった `0x6563A8` と `0x670A48` を解明した。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6644648
- 6752840
- 7158964
- 7152792
- 6650032
- 6758224
- 6862204
- 6644492
- 8664628
- 6853140
- 6654568
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:3481-3551
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-59 FOXXY 時間変更チートの残り 2 パッチ — 演出をメニュー姿勢に差し替えている — `HIGH`

F-58 で未解析だった `0x6563A8` と `0x670A48` を解明した。

### 全 4 パッチの内訳

| # | USA | JPN | 素の値 | 有効時 | 意味 |
|---|---|---|---|---|---|
| 1 | `0x6D3CB4` | `0x6D2498` | `MOV R0,#0x4A` | `#0x2E` | **MenuID 持ち物欄③ → 日付変更**（F-58） |
| 2 | `0x6578B0` | `0x6563A8` | `MOV R1,#23` | `#26` | **アニメ `putaway_wait1` → `menu_think1`** |
| 3 | `0x671F50` | `0x670A48` | `MOV R1,#0x42` | `#6` | **状態 66（拾い上げ）→ 状態 6（中立）** |
| 4 | `0x68B57C` | 未特定 | `MOV R1,#6` | `#6` | **有効時も無効時も同じ値＝死んだ行** |

### #2 — アニメの差し替え

```c
PlayerAction_PutAwayWait (0x65630C):
    if (player[2245] & 0x20) { ...; Actor_PlayAnim(player, 208 /*swim_get_wait1*/, ...); }
    return Actor_PlayAnim(player, 23, 1, 0, 1);   // ★0x6563A8 の即値
```

| ID | 名前 |
|---|---|
| 23 (`0x17`) | `putaway_wait1` — 道具をしまう待機 |
| 26 (`0x1A`) | **`menu_think1`** — メニュー操作中の「考える」待機 |

### #3 — 【重要】これは**状態 ID** であってアニメ ID ではない

```
670a3c  BL   vc_COORDOFFSET
670a44  MOV  R2, R6
670a48  MOV  R1, #0x42          ← ★書き換え対象
670a50  BL   Actor_SetState     ← ★Actor_PlayAnim ではない
```

`Actor_SetState` は `g_ActorStateTable` (`0x843634`, stride `0x1C`) を引く。
**アニメ表で引くと `cracker_setoff1` という無関係な名前が出る**（一度そう誤読した）。

| state | エントリ | 内容 |
|---|---|---|
| 66 (`0x42`) | `ActorState66_PickupGet_Enter` (`0x689214`) | `Actor_PlayAnim(38 = pickup_get1)` で**拾い上げ演出**、座標をセットして Y を -1.0 |
| 6 | `0x658A68` | 手持ちアイテムのフラグ (`this+2245/2247/2248`) をクリアして**中立状態へ戻す** |

`0x658A68` は `PUSH {R4-R7,LR}` で始まる**真の関数先頭**だが、
**IDA は直前の `sub_658A20` と併合している。**
（`sub_658A20` が `POP {R4-R6,LR}` + NOP でフォールスルーするため。
CLAUDE.md の「関数先頭の後方走査は誤検出する前提で使う」がそのまま出た）

### まとめ — 4 パッチの役割分担

```
#1  「穴に埋める」動作が開くメニューを  持ち物欄③ → 日付変更  に差し替え
#2  その間の待機アニメを              しまう待機 → メニュー考え中  に差し替え
#3  拾い上げ演出の状態へ入るのをやめ    中立状態へ戻す
#4  死んだ行
```

**つまり #1 が機能そのもので、#2/#3 はプレイヤーの見た目を
「メニューを開いている姿」に整えるための調整。**
アイテムを拾い上げるモーションのまま日付変更ウィンドウが開くのを防いでいる。

### 教訓

- **即値の書き換えを見たら、その即値が「どの関数の何番目の引数か」を必ず確認する。**
  同じ `MOV R1,#imm` でも `Actor_PlayAnim` ならアニメ ID、
  `Actor_SetState` なら状態 ID で、引くテーブルが違う（F-59 で一度誤読した）
- チートの複数パッチには**主役と脇役がある。**
  機能の本体は 1 つで、残りは見た目の辻褄合わせや死んだ行のことがある

---

