---
id: ACNL-F0444
aliases:
- IDA-opus-5-F011
title: 自前資源のマテリアルアニメを生成し、自前instanceへ結線できた（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**自分で読み込んだ `UnitCursor.bcres` のアニメを、'
date: '2026-09-21'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1798700
- 5662696
- 3242076
- 5160524
- 9423988
- 5159956
- 5178112
- 9436920
- 1231948
- 7657648
- 5625128
- 5168280
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:342-409
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F011: 自前資源のマテリアルアニメを生成し、自前instanceへ結線できた（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。**自分で読み込んだ `UnitCursor.bcres` のアニメを、
自分で作った instance へ結線するところまで実機で通した。**

手順（park は `0x001B722C`、call guard 経由）:

| 段 | 呼ぶもの | 結果 |
|---|---|---|
| 1 | `0x005667E8(allocr_D)` → `0x0031785C(allocr_D, 0x4000, parent, name)` | **アニメ専用ヒープ** `0x31010C70` |
| 2 | **`0x004EBE4C(MA)`** = `g3d::MaterialAnim` 構築子 | vtable `0x8FCC74`、`+4=2`、`+12` に HeapAllocator |
| 3 | `0x004EBC14(MA, nodeHolder, CANM, allocr_D, 0)` | **戻り値 1**。`+16` ヒープ `0x31010D18`、**`+8` アニメ本体 `0x31010DC0`** |
| 4 | `0x004F0300(nodeHolder, MA, 0)` | `AnimBinding` の行1・スロット0 に `0x31010DC0` が入った |

CANM の実行時番地は **資源先頭 + ファイル内オフセット**（`UnitCursor` = `res+0x1148`、
`UnitCursorNG` = `+0x1358`、`UnitCursorRotate` = `+0x161C`）。3つとも実機で `CANM` を確認。
**CANM は magic がオブジェクト先頭**にあり、CMDL のように `obj+4` ではない。

### 第7引数はスロット数だった

`AnimBinding` の行長は **3** で、`ModelInstance_Create` に渡した第7引数 `3` と一致し、
`UnitCursor.bcres` のマテリアルアニメ本数 3 とも一致する。行番号は `node+0x14C` = 1。
**IDA-opus-5-F009 の「第7引数はスロット数ではない」は不正確だった**ので訂正する。
`sub_1C25E8` が `a7=1` でスロット0へ結線できていたのは、**1本しか使わないから行長1で足りていた**だけ。
正しくは「**a5 がアニメ機構を作るかどうか、a7 が1行あたりのスロット数**」。

### 専用ヒープの実測（2026-09-21）

マテリアルアニメ1本の消費は **1,132 バイト**（`0x4000` のヒープの残りが 15,252 B）。
`g3d::MaterialAnim_BuildFromRes` は `sub_566700` で子ヒープを**実使用量へ縮める**ので、
子ヒープ自身の空きは 0 になる。測るときは**親側**（渡したアロケータのヒープ）を見る。

つまり専用ヒープは **2 呼び出し**（`HeapAllocator_Ctor 0x005667E8` → `Heap_CreateNamed_0 0x0031785C`）で、
**4 KiB もあれば 3 本入る**。今回の `0x4000` は 14 倍の過大。
**解明（2026-09-21、訂正）**: instance ヒープは小さすぎたのではない。
**1回目の失敗した試行（素の `AnimEvaluator`）が、同じ instance ヒープの中に子ヒープを作って
そのまま残していた**。レジスタ復元で復旧したので解放されていない。実機の `EV+16` に
生きた `sead::ExpHeap`（`0x30C51E7C`、vtable `0x008FFEF8`）が残っているのを読み取りだけで確認した。
2回目はその残骸で空きを食われ、`sead_ExpHeap_TryCreate 0x0012CC4C` が
`v11 <= 0xA8`（168 B 以下）で null を返したか親の `alloc` に失敗した。

したがって**正しい教訓は「アニメには大きなヒープが要る」ではない**:

- `g3d::MaterialAnim_BuildFromRes` は親の **最大空きブロック全体**を子ヒープとして取り
  （`sead::ExpHeap::getMaxAllocatableSize 0x0074D8B0` = vtable slot16）、成功後に
  `sub_566700` → `sead::ExpHeap::adjust 0x0055D528`（vtable slot5）で**余りを親へ返して縮む**。
  よって **1つのヒープから N 本を順に作れる**（各回 約1,132 B だけ残る）。12体構成の前提が立つ。
- **失敗した build は親を汚染する**。子ヒープが残り、親の空きが消える。
  レジスタ復元だけの復旧では巻き戻らないので、**失敗後は別のアロケータを使うか子ヒープを解放する**。
- **失敗は黙って 0 を返す**ので、`Heap_CreateNamed_0` の戻り値と `MaterialAnim+16` を必ず確認する。
- 子ヒープは **168 バイト以下では作れない**（`TryCreate` の `v11 <= 0xA8` で null）。

### まだ動かしていない

結線までで、**フレームを進めていないので見た目は変わっていない**。
**訂正（2026-09-21）**: VFP は再生には要らない。**`sub_4EDC98 0x004EDC98` が毎フレームの進行**で、
**引数は整数1個**。ゲームの全アクタ（`sub_1AB2E4` `sub_227020` `sub_227CFC` ほか12箇所以上）が
これを呼んでいる。中身は「vtable slot2 で内部 evaluator を引き、`+76` の関数を `+80` を引数に呼び、
`+60=+56`（前回値）、`+56=+68`（次値）、`+88=1`（更新印）」。
`sub_4EDC74`（VFP s0）は**任意フレームへの seek 用**であって再生には不要。
したがって「call guard に VFP を足す」「AnimFrameController を直接書く」はどちらも不要。
今回の instance は姿勢を与えていないので画面には出していない。

根拠: `events.jsonl` の `animheap_*` / `matanim_ctor2` / `matanim_build2` / `matanim_bind`、
`sub_4EBE4C` / `sub_4EBC14` / `sub_4F0300` の逆アセンブル、結線後のメモリ読み出し。
反証条件: 別のスロット番号で書けない、`+20` が 0 のままで評価時に落ちる、
行長 3 が a7 ではなく資源のアニメ本数で決まっている（a7 を変えて確かめる）。

