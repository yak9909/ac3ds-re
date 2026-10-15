---
id: ACNL-F0068
aliases:
- F-30
title: F-30 掘る動作のエフェクトは 3 系統 — `HIGH`
summary: 状態 79 (`ShovelState_DigUpdate` = `0x65BC7C`) がアニメ ID で分岐して出す。
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6667388
- 6667564
- 6667608
- 6667652
- 6667756
- 7742068
- 6747524
- 6869476
- 2426108
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1490-1546
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-30 掘る動作のエフェクトは 3 系統 — `HIGH`

状態 79 (`ShovelState_DigUpdate` = `0x65BC7C`) がアニメ ID で分岐して出す。

```c
v10 = *(u16*)(actor + 548);       // 現在のアニメID
if (v10 == 73) { ... }            // scoop_dig1  = 掘る
if (v10 == 76) { ... }            // scoop_stump1 = 切り株
```

アニメ 73（通常の掘る）の経路:

| 呼び出し | アドレス | 内容 |
|---|---|---|
| `Effect_DigDirt(actor, X, Y, 0)` | `0x65BD2C` | **土しぶき** |
| `Effect_ScoopScrape(actor, pos, a3, 0)` | `0x65BD58` | **地面抉れ** |
| `Actor_PlaySound(actor, 16778777, 1)` | `0x65BD84` | **サウンド**（パーティクルではない） |

`0x65BDEC`（`Effect_ScoopScrape` の a4=2）は**アニメ 76 = 切り株専用**で、
通常の掘る動作では実行されない。

### `Effect_DigDirt` (`0x762274`) — 土しぶき

```c
unk_6A6364(v9, X, Y);                   // マス座標 -> ワールド座標
if (unk_6C4D0C(v9, 0) == 22)            // 地面種別 22 = 砂
    unk_764074(actor, 0, 0, flag ? 353 : 352, v9);
else                                     // 土など
    unk_764074(actor, 0, 0, flag ? 354 : 351, v9);
```

**X, Y を引数に取る**ので任意のマスへ出せる。地面種別で自動的に切り替わる。

### `Effect_ScoopScrape` (`0x66F584`) — 地面抉れ

```c
if (unk_6C4D0C(pos, 0) != 22)
    return sub_65D970(actor, pos, a3, a4);
return unk_4EA990(actor+412, 0, pos, v10, 11401328, 1,
                  "t_scoop_sand", dword_947F24[a4]);
```

こちらは**ワールド座標 `pos`** を取る（`Field_XYToWorld` で作る）。

### `Actor_PlaySound` (`0x68D1E4`)

```c
if (!(actor[0x66] >> 5 & 1)) {
    Sound_Play(actor + 1516, soundID);   // 0x2504FC -> unk_6B3884
    if (flag) actor[0x173] |= 6;
}
```

**アクターに紐づくサウンド再生**。座標指定はできない。

---

