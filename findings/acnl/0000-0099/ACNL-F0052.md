---
id: ACNL-F0052
aliases:
- F-14
title: F-14 フィールドアクションの実行経路 — `HIGH`
summary: スコップのアクション決定から掘削レコード登録までの全経路が判明した。
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5866052
- 5867144
- 10150236
- 5867104
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:870-929
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-14 フィールドアクションの実行経路 — `HIGH`

スコップのアクション決定から掘削レコード登録までの全経路が判明した。

```
FieldObj_ResolveDigAction (0x598244)
 └ 0x598688  BL Player_StartFieldAction(actionID, &対象item, &結果item,
                                        &g_EmptyItem, X, Y, 0,0,0,0,0)
     └ 18B キュー(0x9AE15C, 18B×4) の空きスロットへ格納
     │    [0..3]=対象item  [4..7]=結果item  [8..11]=item2(空)
     │    [12]=X  [13]=Y  [14]=actionID  [15]=使用中フラグ(1)
     │    [17]= a7..a11 から合成したビットフィールド
     ├ actionID == 16 のときは [15]=2 にするだけで終了（遅延）
     └ それ以外は同期的に:
          unk_59FA6C(rec)           22B レコードをスタック上に初期化
          sub_59EBE8(rec, slot, 0)  18B → 22B 変換
          sub_59E8F8(rec)           rec[13] のビット[5:2] でケース分岐
```

`sub_59EBE8(rec22, slot18, caseNo)` の対応:

| 22B レコード | 由来 |
|---|---|
| `rec[0..11]` | `slot[0..11]`（3 アイテム） |
| `rec[12]` | `actionID * 4 \| (unk_305F6C() & 3)` — 上位6bitがアクションID、下位2bitがプレイヤー index |
| `rec[13]` | `caseNo * 4` — `sub_59E8F8` のケース番号。第3引数がそのまま入る |
| `rec[14]` | `slot[17]`（フラグ） |
| `rec[18]` | `unk_2F75CC()` = 自プレイヤー番号 |
| `rec[19]` | `slot[12]` = X |
| `rec[20]` | `slot[13]` = Y |

`sub_59E8F8` の case 3 が掘削の実行:

```
FieldObj_ApplyDigRecord(rec[12] >> 2,   // actionID
                        rec[12] & 3,    // playerIdx
                        rec, rec+4, rec+8,  // 3 アイテム
                        rec[19],        // X
                        rec[20],        // Y
                        rec[18],        // 自プレイヤー番号
                        rec[14],        // フラグ
                        rec + 15)       // &rec[15]
```

`Player_StartFieldAction` は `sub_59EBE8` を caseNo=0 で呼ぶので、入口は常に
case 0 = `sub_59EC9C`。`sub_59EC9C` は条件に応じて `rec[13]` を 4 か 8 に
書き換えて `sub_59E8F8` を再帰呼び出しする。

**根拠**: `Player_StartFieldAction` / `sub_59E8F8` / `sub_59EBE8` / `sub_59EC9C`
/ `FieldObj_ApplyDigRecord` の decompile と、`0x598660`-`0x598688` の assembly。

**未確認**: case 3 へ実際に遷移させる経路（`sub_59E878` / `unk_59F3D8` /
`unk_59EE44` のいずれかが `rec[13]` を 3 に書くと思われるが未読）。

**含意**: `Player_StartFieldAction` を呼べば、引数組み立て・プレイヤー番号・
フラグ・レコード管理をすべてゲーム本来の処理が行う。複数マスを掘るために
`FieldObj_ApplyDigRecord` を直接呼ぶ必要はない。

---

