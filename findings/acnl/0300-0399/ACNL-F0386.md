---
id: ACNL-F0386
aliases:
- F-358@v1:RE/FINDINGS.md:23291
title: 'F-358（2026-09-08）: `BsFgProc::Setup` の正体 — `fgobj::Proc` のセットアップ段（＋しずえ会話スキップの下調べ）'
summary: 'confidence: **MEDIUM〜HIGH（静的のみ）**。**この作業中デバッガは切断されていた**（`is_debugger_on()==False`）。'
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9223460
- 9445596
- 9200960
- 9216808
- 9379720
- 9380992
- 5880832
- 3242076
- 2154496
- 1049600
- 5884276
- 9445608
- 3110348
- 9769786
- 9769785
- 5976820
- 9769787
- 8925992
- 8927477
- 2101768
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23291-23379
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-358（2026-09-08）: `BsFgProc::Setup` の正体 — `fgobj::Proc` のセットアップ段（＋しずえ会話スキップの下調べ）

confidence: **MEDIUM〜HIGH（静的のみ）**。**この作業中デバッガは切断されていた**（`is_debugger_on()==False`）。
実機は 1 バイトも触っていない。詳細は `scratchpad/MEMO_f358_bsfgproc_and_boot.md`。

### 1. `BsFgProc` = RTTI 名 `fgobj::Proc`

| | |
|---|---|
| TypeInfo | `0x008CBD24`（`N5fgobj4ProcE`） |
| vtable | `0x009020DC`（16 スロット） |
| 継承 | `fgobj::Proc` -> `Base`(`0x008C6540`) -> `oml::framework::Process`(`0x008CA328`) |

`ScBoot`(`0x008F1F88`) / `ScStage`(`0x008F2480`) も同じ `Base` を継承し、
**vtable のスロット割りが一致する**（スロット 4/5/10/14 が同一番地）。`Proc` は「処理の単位」の共通基底。

★**Fg = foreground object**。隣接文字列が `fg_hole_sand` / `fg_crack_soil` / `fg_wrapping` /
`fg_soldout` / `BsFgObject` / `Fg/Bcres/FgObjAnim.bcres`。落とし物・穴・ひび・マイデザ・包装を持つ。

### 2. `BsFgProc::Setup` は 2 つのものを指す

**(a) ヒープの名前** — `fgobj_Proc_CreateHeaps`（`0x0059BC00`）が `Heap_CreateNamed`(`0x0031785C`) で作る:

| 格納先 | 名前 | 大きさ（屋外 / それ以外） |
|---|---|---|
| `this+0x14` | **`BsFgProc::Setup`** | `0x1E000`(122,880) / `0xDC00`(56,320) |
| `this+0x1C` | `BsFgProc::Resource` | `0x20E000`(2,154,496) / `0x100400`(1,049,600) |
| `this+0x45C` | `BsFgProc::MyDsnMgr` | `0x19800`(104,448)。屋外のときだけ |

分岐は `byte_948E5F = Room_HasFlags(4, 現在の部屋)` = **屋外か**（F-56 の表と一致）。

**(b) 仮想関数 `Setup()`** = **`fgobj_Proc_Setup`（`0x0059C974`）**、vtable スロット 3。

```
byte_948E5E = Room_HasFlags(8, 部屋)   // 屋内か
byte_948E5F = Room_HasFlags(4, 部屋)   // 屋外か
fgobj_Proc_CreateHeaps(this)           // ★上の 3 ヒープ
if (!sub_599490 || !sub_599A64) return 3;      // 3 = まだ（次フレーム再入）
"Fg/Bcres/FgObjAnim.bcres" を読む（段階 7 -> 8 -> 9 -> 10。段階は this+0x45B8）
item 13223 のマイデザ用モデルを 4 x 10 = 40 個
リスト初期化・マップ範囲・FuncNode 登録
return 2;                                      // 2 = 完了
```

★**戻り値 2=完了 / 3=継続の「段階つき Setup」= フィールド読み込み（「準備中」）の 1 ステップ**。
**しずえの会話とは無関係。** 呼び出し元は vtable 経由の 1 か所（`0x009020E8`）のみ。

### 3. しずえ会話スキップの下調べ（★ここから先は仮説）

`Room_GetCurrentId`(`0x002F75CC`) は **`g_CurrentRoomId`（`0x0095133A`、1 バイト）**を読むだけ（F-55）。

| 部屋 | 内部名 | 意味 |
|---|---|---|
| `0x00` | `Village` | 村 |
| **`0x5E`** | **`Title`** | タイトル画面 |
| `0x5F` | `VillagePrologue` | 初回の駅到着 |
| `0x60` / `0x61` / `0x62` | `Save` / `Load` / `Format` | セーブ・終了・黒画面 |
| **`0x63`** | **`PlayerSelect`** | **しずえのスポットライト／村の読み込み ★目的の場面** |
| `0x9C` | `UpdateSelect` | 電車のしずえ用プレイヤー選択 |

★**この表がこのビルドに合うことを独立に確認**: `sub_605BF4` に `Room_GetCurrentId() == 94`(=`0x5E`)、
`sub_7552B8` は 92,93,94,96,97,98,99,152,156 をまとめて弾く（表の Sequence/Cutscene 行と一致）。

| 番地 | 意味 |
|---|---|
| `0x0095133A` | **現在の部屋 ID**（`0xA5`=165 は「部屋なし」） |
| `0x00951339` | **直前の部屋 ID**（`Room_ClearCurrentId 0x005B32F4` が退避） |
| `0x0095133B` | もう 1 つの部屋バイト（遷移先？未確定） |
| `0x00883328` | `g_RoomFlagTable`（F-56） |
| `0x008838F5` | 部屋 -> 種別の表（`sub_5B33A8` が引く。165 エントリ） |
| `0x00201208` | `dFieldFactory_Create(heap, roomId)`。部屋 ID で switch し Builder 9 種から選ぶ |

**未確定**: 部屋 `0x63` の中の進行（しずえ登場 -> 会話 -> 「はじめる」 -> 村の読み込み）を
誰が回しているか。`state::Base<T>` の 110 クラスに該当が無く、
`script::FlowEngine` / `libms::FlowNode*`（会話スクリプト）の線が濃い。
部屋遷移の要求は `sub_605BF4` の `word_94A3D0`（`0xFFFF`=要求なし）らしいが未確定。

★**部屋 ID の直接書き換えは非推奨**（「現在部屋 ID の偽装は全システムへ波及する」と既出）。
狙うのは**会話フローを終わらせる側**であって部屋 ID の詐称ではない。

### 4. 実機で測ること（デバッガを繋ぎ直してから）

1. `0x00951338`〜`0x0095133C` を **タイトル / プレイヤー選択 / しずえ会話中 / 準備中 / 村に出た直後**の
   5 点で読む -> 遷移の実際の並びが確定する
2. しずえ会話中に `0x0059C974` へ bp -> ヒットしなければ「村の読み込みはまだ」の裏取り
3. 「はじめる」を選んだ瞬間の `word_94A3D0`（`0x0094A3D0`）の変化を見る

---

