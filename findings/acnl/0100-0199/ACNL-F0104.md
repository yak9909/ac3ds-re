---
id: ACNL-F0104
aliases:
- F-66
title: 'F-66: オンライン髪型変更は虫取り網アクションから美容室状態 `0xB9` への迂回'
summary: 'confidence: **MEDIUM**（独立した複数の静的経路で一致。実機・通信相手を使った動的検証は未実施）'
date: '2026-09-08'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6826388
- 6826732
- 6826528
- 6826688
- 6826600
- 6826636
- 6826676
- 6826656
- 8667764
- 6721048
- 8669808
- 6779628
- 6780272
- 6827896
- 6848036
- 6828472
- 6838072
- 6863352
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4406-4489
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-66: オンライン髪型変更は虫取り網アクションから美容室状態 `0xB9` への迂回
confidence: **MEDIUM**（独立した複数の静的経路で一致。実機・通信相手を使った動的検証は未実施）

対象は `REFERENCES/CHEATS/player.txt` の「見た目変更(オンライン)」節。
4 命令のパッチ先はすべて `PlayerAction_TryBugNetSwing` (`0x682994`-`0x682AEC`) に入る。

### 虫取り網アクションの改変

| addr | 元命令 | ON | 意味 |
|---|---|---|---|
| `0x682A20` | `BEQ 0x682AC0` | `NOP` | `[player+0x174]` bit1 の準備判定を迂回 |
| `0x682A68` | `BNE 0x682AC0` | `NOP` | 道具種別 `4`（虫取り網）の判定を迂回 |
| `0x682A8C` | `BNE 0x682AB4` | `NOP` | 状態遷移直前の虫取り網再判定を迂回 |
| `0x682AA0` | `MOV R1,#0x70` | `MOV R1,#0xB9` | `Actor_SetState` の遷移先を差し替える |

通常は状態 `0x70`（記述子 `0x844274`）へ入り、enter `0x668E18` が
アニメ 102 `net_swing1` を再生する。チート時は同じアクション入口から
状態 `0xB9`（記述子 `0x844A70`）へ入る。
呼び出し元は `PlayerAction_DispatchTop` (`0x6772EC`) 内の `0x677570`。

### 状態 `0xB9` は見た目変更の正規状態

正規の開始関数 `Player_StartAppearanceChange` (`0x682F78`) も、
`vc_GETANIMINST(player)` の返すパケットへ次を詰めて `Actor_SetState(player,0xB9,packet,0)` を呼ぶ。

| packet off | 内容 | 範囲 |
|---|---|---|
| `+14` | 髪型 | `0x00`-`0x21`（34 種） |
| `+15` | 髪色 | `0x00`-`0x0F`（16 色） |
| `+16` | 目の色 | `0x00`-`0x05`（6 色） |
| `+17` | 見た目用 Item 4B | — |
| `+21` | 補助フラグ | — |

状態記述子のコールバック:

| descriptor off | addr | 名前 | 役割 |
|---|---|---|---|
| `+00` | `0x687E24` | `PlayerState_AppearanceChangeEnter` | ローカル時の位置合わせ後、アニメ 237 `barber_set1` |
| `+08` | `0x6831B8` | `PlayerState_AppearanceChangeUpdate` | scratch 値を検査し、プレイヤーの見た目へ適用 |
| `+10` | `0x685738` | `PlayerState_AppearanceChangeSyncLocal` | ローカルプロフィールへ反映 |
| `+18` | `0x68B9F8` | `PlayerState_AppearanceChangeSyncRemote` | 受信パケットから相手プロフィールへ反映 |

update は `player+0x8CA/+0x8CB/+0x8CC` を髪型・髪色・目色として読み、
範囲内なら `player+0x942/+0x944/+0x948` へ適用して見た目を再構築する。
`+0x8CD` は 4B Item、`+0x8D1` は補助フラグ。このため従来の
`+0x8CA/+0x8CB = 対象マス X/Y` は全状態共通の意味ではなく、**状態別 scratch 領域**である。

local sync は `vc_PSOFFSET(playerNo)` のプロフィールレコードへ髪型 `+4`、髪色 `+5`、
目色 `+7`、Item `+10` を反映する。remote sync も受信パケット `+14/+15/+16/+17` から
同じ更新を行う。これがチート名の「オンライン」に対応する同期経路であり、
単なるローカル表示値の書き換えではない。

### Gateway の `0x060D0600` は髪型値ではなく状態キック

```
offset = 0x33000000;
if (*(u32*)0x33099F84 != 0xFFFFFFFF)
    offset += 0x12C;
if (keyMask & 0x100)
    *(u32*)(offset + 0x99FE4) = 0x060D0600;
```

`0x33099E3C` をプレイヤー基準とすると、選択先は
`player+0x1A8` (`0x33099FE4`) または `player+0x2D4` (`0x3309A110`)。
通常側では little endian の 4 バイト `[00,06,0D,06]` となり、
`Actor_SetState` の書き込みから `player+0x1A9 = 現在状態 6`、
`player+0x1AA = 直前状態 13` と確認できる。状態 6 は neutral/wait、状態 13 は movement。
`+0x1A8/+0x1AB`、分岐基準 `player+0x148`、代替先 `+0x2D4` の厳密な役割は未確定。

重要: [Nanquitas の CTRPF Action Replay コード型資料](https://gist.github.com/Nanquitas/d6c920a59c757cf7917c2bffa76de860)
のキー定義では `DD000000 00000100` は **R** であり A ではない。
配布文の「Aボタン」はゲーム側の通常アクション入力を指す可能性が高いが、
状態キックと A 入力の順序は実機で確認が必要。少なくとも AR 行そのものを
「A ボタン条件」と解釈してはいけない。同じ `0x060D0600` は `drop.txt` にもあり、
髪型固有データではなく再利用されるプレイヤー状態キックである。

### 安全性

状態 `0xB9` の `+18` はリモート受信処理に実際に接続されている。
不正な値や中途半端な復元は通信相手の一時プロフィール表示まで波及しうるため、
未検証のまま野良オンラインで使うべきではない。OFF の 4 命令は元バイトと一致する。

---

