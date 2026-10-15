---
id: ACNL-F0063
aliases:
- F-25
title: F-25 レコードを積んでも反映されない — 反映側は 1 マスしか見ない — `HIGH`
summary: 'v5（`0x59E9CC` = `BL FieldObj_ApplyDigRecord` をフックし X+1 で再度呼ぶ）の実測:'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5892556
- 5899072
- 5899096
- 10150468
- 10150446
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1339-1375
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-25 レコードを積んでも反映されない — 反映側は 1 マスしか見ない — `HIGH`

v5（`0x59E9CC` = `BL FieldObj_ApplyDigRecord` をフックし X+1 で再度呼ぶ）の実測:

レコード配列をクリアして 1 回掘った結果、**残ったのは 1 件だけ、しかも X=64（隣マス）**。
中心 (63,24) は無い。これは以下を意味する:

| マス | 登録 | 反映 | レコード |
|---|---|---|---|
| 中心 | OK | **処理された**（穴が空く） | 解放されて消える |
| 隣 | OK | **処理されない** | `[17]=2` で残る |

つまり `FieldObj_ApplyDigRecord` は隣マスでも**正しく登録される**。
`sub_5A0318(X, Y, pNo)` は 3 つすべてを厳密に照合する（`0x5A0340`-`0x5A0358`）ので
互いのキャンセルでもない。

**反映側がボトルネックだった。**

`[17]=2` のレコードを地面へ反映する処理はいずれも
`sub_5A0318(X, Y, pNo)` で**呼び出し元が指定した 1 マス**を引くだけ:

| 関数 | 引数 | actionID 19 |
|---|---|---|
| `sub_5991CC(X, Y)` | 座標指定 | switch 対象外（case 11/28/0 のみ） |
| `sub_5956B8(X, Y)` | 座標指定 | 対象外（case 11 のみ） |
| `sub_5A166C(X, Y, pNo)` | 座標指定 | キャンセル専用 |
| `sub_5A1954()` | なし | 全レコードのリセット |

レコードをいくら積んでも、プレイヤーの状態機械が指定した 1 マス以外は反映されない。
**以前 11 件溜まっていたのは「毎回、隣マスの分だけが残る」ため。**

**危険**: `FieldObj_ApplyDigRecord` の空きスロット検索は
`v12 == -1`（32 件満杯）のチェックが無く、`0x9AE244 - 22 = 0x9AE22E` へ
範囲外書き込みを行う。レコードが解放されずに溜まると 32 回でクラッシュする。

---

