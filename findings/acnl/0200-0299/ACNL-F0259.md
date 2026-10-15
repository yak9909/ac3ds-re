---
id: ACNL-F0259
aliases:
- F-234
title: 'F-234: ロード画像は上画面で id 8 の後に replay される Layout id 10 — `HIGH`（静的＋実機＋リソース同定）'
summary: ユーザーがロード画像を目視した状態で Suspend し、再開すればロードが終わる条件だったため、
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5908424
- 5669864
- 5669596
- 9379668
- 1185468
- 11376832
- 11376900
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:13869-13970
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-234: ロード画像は上画面で id 8 の後に replay される Layout id 10 — `HIGH`（静的＋実機＋リソース同定）

ユーザーがロード画像を目視した状態で Suspend し、再開すればロードが終わる条件だったため、
事前監査した一回限りの低レベル trace を入れ、上画面パス末尾 `0x5A27C8` に software
breakpoint を置いて一度だけ再開した。breakpoint はヒット直後に削除し、trace も stock へ復元した。

### 1. ロード画像表示中の実 replay 順

`GpuCmd_ReplayRecordedListRange` の引数と caller を、パス印とともに記録した結果:

```
seq 0: pass 1 / list id 8  / length 0x180 / LR=0x5683E8
seq 1: pass 1 / list id 10 / length 0x2C0 / LR=0x5683E8
```

両方とも `Layout_ReplayRecordedList` (`0x5682DC`) からの replay であり、
**ロード中の上画面は id 8 の後に id 10 を replay する。** 現行方式が id 8 の記録末尾へ
UI 画像（スプライト）を追加しても、後続の id 10 に覆われ得る。

### 2. id 10 が現在のロード画像であることの独立確認

trace とは別に、停止中のスタックに残った Layout 候補を調べた。`0x0FFFFE08` から
`0x3225A2B4` を得て、次を確認した。

- vptr `0x008F1F54 = vtbl_Layout`
- 幅・高さ `400.0 x 240.0`
- `Layout+0x100=10`, `+0x104=0`, `+0x108=0x2C0`, `+0x10C=0`
- id 8 の next が id 10、id 10 の prev が id 8、id 10 の next は 0
- 直接到達する文字列に `RootPane`, `N_All`, `P_bg`, `G_loop`
- texture `tc_load_01.bclim`〜`tc_load_03.bclim`
- animation `load_wait_kind.bclan`
- archive `Layout/common/save_wait.arc`

これは低レベル trace と独立した、オブジェクト・リンク・リソースによる同定である。
したがって id 10 は、停止時に実際に見えていたロード画像 Layout である。

### 3. Drawer fingerprint の訂正

静的 `code.bin.i64` では、replay 前に
`sub_4B8C34(Drawer, Layout+0x30, 0)` が呼ばれる。その下の `sub_4D6C90` は
`sub_148D30` で `Layout+0x34` の 16 word / `0x40` bytes を `Drawer+0x34` へコピーするが、
続けて先頭 word を `Drawer+0x30` へ移し、`Drawer+0x34` を `0x013F02C1` で上書きする。

従って照合条件は raw `0x40` bytes equality ではなく:

```
Drawer+0x30 == Layout+0x34
Drawer+0x38..+0x70 == Layout+0x38..+0x70
Drawer+0x34 == 0x013F02C1
```

である。この変換後 fingerprint も id 10 Layout と停止中 Drawer で一致した。
以前の raw `0x40` bytes scan の不一致は Layout 解放の証拠にしない。

### 4. id 10 の記録リスト容量と主リスト容量

`GpuCmd_SelectList` (`0x1216BC`) の静的な検索式は
`0x00AD98C0 + ((id & 0x1F) << 2) + 0x1C` で bucket を選び、manager `+0x40` を
exact id まで辿る。id 10 の bucket はスクリプト計算で `0x00AD9904`。

ロード中の実機値:

```
id 10 manager = 0x327AE21C
base          = 0x327AE270
size          = 0x1000
offset        = 0x2C0
record end    = 0x327AE530
manager end   = 0x327AF270
remaining     = 0xD40
```

Layout 側の id / start / length / capacity hint も `10 / 0 / 0x2C0 / 0x1000` で一致する。
id 10 へ相乗りすればロード画像より後に小さな表示を置ける可能性はあるが、残量 `0xD40` のため
19チャンク級の全メニューの容量問題は解消しない。

一方、同じ上画面パス末尾の主リストは:

```
base      = 0x3229D0C0
ptr       = 0x3229E370
end       = 0x3239D0C0
used      = 0x12B0
remaining = 0xFED50
```

だった。従って**全GUIの次候補は引き続き `0x5A27C8` 入口の主リスト**である。
ただし stock は通常 submit せず、Drawer の投影も直前 Layout 依存なので、まず1枚だけの
自然提出版を試し、描かなかった場合だけ明示 Split 版を別に A/B する。

### confidence の根拠と限界

- 静的: replay 引数、Drawer 変換、list manager 検索式を `code.bin.i64` の assembly で確認
- 動的1: ロード画像表示中の低レベル replay 列 `id 8 → id 10`
- 動的2: 停止中 Layout の vtable・リンク・記録値・ロード専用リソース名・Drawer fingerprint
- 容量: manager と Layout の二経路で一致

以上は根本原因の同定を `HIGH` とする根拠だが、**tail へ追加したUI画像が自然提出されるかは未検証**。
ここは F-234 から推測で昇格させない。

---

