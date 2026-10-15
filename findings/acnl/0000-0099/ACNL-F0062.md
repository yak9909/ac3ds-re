---
id: ACNL-F0062
aliases:
- F-24
title: F-24 キューに積んでも実行段階は 1 マスしか処理しない — `HIGH`
summary: 'F-22 の修正でケーブは正しく動くようになった。実機で確認できたこと:'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5904048
- 5892560
- 5867144
- 5892556
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1269-1338
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-24 キューに積んでも実行段階は 1 マスしか処理しない — `HIGH`

F-22 の修正でケーブは正しく動くようになった。実機で確認できたこと:

```
18B キュー        : 4 スロットとも [15]=2 (case 1 = 成立)   ← 前回は [15]=3 (不成立)
進行中アクション  : [0] X=70 Y=29    [1] X=71 Y=29  ← X+1、ケーブが出した隣マス
                    [2] X=70 Y=28    [3] X=70 Y=27
```

**隣マスの要求は `Item_SameId` を通過し、`FieldAction_RegisterActive` にも登録される。**
ユーザー報告の「隣を掘ろうとすると前振り動作のみで掘れない」は、
`FieldAction_FindActive` が既存エントリを見つけて弾いていたためで、
登録自体は成功していた証拠でもある。

### しかし穴は空かない

`FieldObj_ApplyDigRecord` (`0x5A16B0`) に breakpoint を置き、1 回掘って観測:

```
1 回目: actionID=19 playerIdx=0 item0=0x7FFE(空) item1=0x009E(穴)
        X=68  Y=27  pNo=0 flags=0  a10=0x0FFFFC57 (スタック上)
        LR = 0x59E9D0  → FieldAction_Dispatch の case 3 から
```

**その後 12 秒待っても 2 回目の呼び出しは来ない。**

つまり:

| 段階 | 中心マス | 隣マス |
|---|---|---|
| キュー登録 | OK | OK |
| `FieldAction_CanApply` (`Item_SameId`) | OK | **OK**（F-22 修正の成果） |
| `FieldAction_RegisterActive` | OK | OK |
| `slot[15]` | 2 (case1) | 2 (case1) |
| **case 3 → `FieldObj_ApplyDigRecord`** | **到達** | **到達しない** |

`slot[15]=2` から case 3 へ進める処理は、**プレイヤーの状態機械が
「今掘っているマス」1 つに対してしか行わない**と考えられる。
キューに積んだだけでは実行段階に進まない。

これは `[15]=2` のスロットが解放されない理由でもある（F-19 の枯渇）。

### 含意 — フック位置を変える必要がある

`0x598688` は**アクション決定 → キュー登録**の段階なので、
ここで複数マスを積んでも実行段階が 1 マスしか消化しない。
余ったスロットが滞留してキューを枯渇させるだけで、逆効果になる。

**次の方針**: `FieldObj_ApplyDigRecord` の**呼び出し元**
（`LR = 0x59E9D0` から `BL` は `0x59E9CC`）をフックし、
X+1 でもう一度 `FieldObj_ApplyDigRecord` を呼ぶ。
ここは実際に地面を書き換える段階で、判定はすべて通過済み。

引数はすべて判明している:

```
FieldObj_ApplyDigRecord(actionID, playerIdx, item0*, item1*, item2*,
                        X, Y, playerNo, flags, &rec[15])
  R0=actionID  R1=playerIdx  R2=item0*  R3=item1*
  [SP+0]=item2*  [SP+4]=X  [SP+8]=Y  [SP+12]=playerNo
  [SP+16]=flags  [SP+20]=&rec[15]
```

**未確認**: `sub_5A0C2C`（`FieldObj_ApplyDigRecord` の末尾で実際の適用を行う）が
対象アイテムの照合をしていないか。している場合は隣マスの実アイテムを
`Field_GetItemAtXY` で取り直す必要がある（F-22 と同じ対処）。

---

