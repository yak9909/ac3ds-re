---
id: ACNL-F0076
aliases:
- F-38
title: F-38 「揺すると木を切る」パッチと通常経路 — `HIGH`
summary: '`Player_BeginFieldObjAction` (`0x595A8C`) の mode 分岐:'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5855884
- 5855968
- 5855972
- 5855980
- 5856024
- 5856012
- 5856028
- 5856556
- 5856600
- 5856020
- 5856036
- 5864852
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1759-1802
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-38 「揺すると木を切る」パッチと通常経路 — `HIGH`

`Player_BeginFieldObjAction` (`0x595A8C`) の mode 分岐:

```
0x595AE0  BL   FieldAction_FindActive        ; (X, Y, 165)
0x595AE4  CMN  R0, #1
0x595AEC  BEQ  loc_595B18                    ; ★-1（進行中アクション無し）なら 0x595B18 へ
...
0x595B0C  BEQ  loc_595B34                    ; mode 0（通常は到達しない）
0x595B1C  BEQ  loc_595B90                    ; ★通常経路の mode 0 判定
0x595D2C  → B sub_597CE0                     ; 斧/木のアクション決定
0x595D58  → B FieldObj_ResolveDigAction      ; スコップ
```

**通常は `FieldAction_FindActive` が -1 を返すので `0x595B18` へ飛ぶ。**
`0x595B0C` は使われない経路であり、そこを書き換えても効果がない（実機で確認）。

`0x595B1C` を `BEQ 0x595D2C` (`0A000082`) にすると mode 0 が
`FieldObj_ResolveAxeAction` へ流れ、**揺すると木が切れる**ようになる。

`REFERENCES/CHEATS/trees.txt` の「木を揺するだけで切れる」が
`0x595B0C`/`0x595B14` を NOP にし `0x595B1C`/`0x595B24` を書き換えるのは、
この通常経路を捕まえるため。**チートの行を「不要」と切り捨てると必要な行を落とす。**

関連パッチ:
- `0x597D94` (`BGT` → `NOP`) — 1 回で切り倒す（`trees.txt` 由来、実機確認）

---

**【重要な訂正 / F-42】上記 2 つのパッチはどちらも使ってはいけない。**

- `0x595B1C` を書き換えると **A ボタンで「揺する」だけでも木が倒れる。**
  `0x595B24` を見れば分かるとおり **`mode 1` は素で `FieldObj_ResolveAxeAction` へ行く**ので、
  伐採判定を呼びたいだけなら mode 0 を潰す必要はまったくない。
- `0x597D94` を NOP にすると **斧まで一撃になる。**
  そのマスだけ一撃にしたいなら、打撃カウンタ `dword_9AE504` の 2 bit を
  直接立てればよい（F-42）。

**この 2 行を `trees.txt` から採ったまま検証せずに使い続けたのが遠回りの原因だった。**
チートの行は「その機能が実現する」ことしか保証しない。**副作用は自分で確かめる。**

---

