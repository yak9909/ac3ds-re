---
id: ACNL-F0284
aliases:
- F-261
title: 'F-261: ★★★★★Layout の初期化 `sub_5685A4` に「自前リストの正しい作り方」が全部書いてある — `HIGH`（静的のみ）'
summary: F-260 の実装を静的に検証する過程で見つけた。**私の実装には致命的な誤りが 2 つあった。**
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9420548
- 5075768
- 5075572
- 5075512
- 5075412
- 8609792
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:15418-15511
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-261: ★★★★★Layout の初期化 `sub_5685A4` に「自前リストの正しい作り方」が全部書いてある — `HIGH`（静的のみ）

F-260 の実装を静的に検証する過程で見つけた。**私の実装には致命的な誤りが 2 つあった。**

### `sub_5685A4`（Layout の生成）が示す正規の手順

```c
*(_DWORD *)(L + 0x114) = 0;         // 状態無効化フラグ
*(_BYTE  *)(L + 0x11C) = 1;         // ★allowNoSplit = 1
GpuCmd_GetProperty(519, &save);
sub_121B34(1, L + 0x100);           // = nngxGenCmdlists。未使用 id を作って L+0x100 へ
GpuCmd_SelectList(*(L + 0x100));
*(_DWORD *)(L + 0x118) = qCount;
sub_121988(qCount, 1);              // = nngxCmdlistStorage。バッファと GX キューを確保
GpuCmd_SelectList(save);
```

### 誤り 1: `Layout+0x11C`（allowNoSplit）を 0 のままにしていた

`GpuCmd_ReplayRecordedListRange` の第 7 引数がこれである。

```c
if (a7) { ... sub_2F858C(g_GpuCmdPtr); g_GpuCmdPtr += (a3 - v19) & ~3; }  // ★本体をコピー
else    { for (...a5 件...) フラグを立てるだけ }                          // ★コピーしない
```

**0 だと記録した本体がコピーされず、何も描かれない。** 本物の Layout は 1。

### 誤り 2: マネージャの base/size を手で書いていた（GX キュー配列が無い）

`sub_121988(size, qCount)` は現在選択中のマネージャに対して:

```c
古いバッファがあれば off_96EAA8 で解放
v9 = off_96EAA4(0x10000, 261, id, size + 28 * qCount);  // 1 回の確保で両方
mgr[1] = v9;            // base
mgr[2] = size;          // 容量
mgr[6] = v9 + size;     // ★GX キューの配列（バッファの直後）
mgr[7] = qCount;        // ★キューの件数
Mem_ZeroFill(v9 + size, 28 * qCount);
g_GpuCmdPtr = base;  g_GpuCmdEnd = base + size;
```

**`mgr[6]` を 0 のままにすると `GpuCmd_SplitAndSubmit` が
`v0[6] + 28 * v0[8]` ＝ アドレス 0 付近へ書いて落ちる。**
id も `sub_121B34` が `dword_96EAAC` を増やしながら未使用のものを配るので、
100/101 のような決め打ちは不要（かつ危険）。

### ★`drawctx` は `Drawer` そのもの＝ `mgr + 0x364`

`DrawBegin1` の実体（Drawer vtable `+0x10` = `sub_4D7274`）は `a1+1684 / +1688 / +1692 /
+1696 / +1698` を触る。これは我々が drawctx として使っている構造そのものである。
実機の値でも `mgr 0x32FF5F88 + 0x364 = 0x32FF62EC` = 捕獲していた drawctx と一致した。

したがって **`DrawCtx_FlushBatch` のフックで drawctx を捕まえる必要はない**。
捕まらないフレームで描けなくなる原因の一つがこれだった。

### Drawer の vtable（`vtbl_nw_lyt_Drawer` = `0x008FBF04`）

| スロット | 実体 | 役割 |
|---|---|---|
| `+0x0C` | `0x004D7338` | **DrawBegin1**。`g_GpuCmdPtr` を渡して `+0x10` を呼び、戻り値を書き戻す |
| `+0x10` | `0x004D7274` | 実体。`drawctx+1684/1688/1692 = 0`、`+1696 = 1`、`+1698 = 6`、`TextBox_UpdateDrawState(ctx, cur, 0, 0)`、`sub_4D72C4` |
| `+0x14` | `0x004D7238` | **DrawEnd1**。同様に `+0x18` を呼ぶ |
| `+0x18` | `0x004D71D4` | 実体。`drawctx+36 != 0` なら `DrawCtx_FlushBatch`、続けて `sub_4D7204` |

- `DrawBegin` が **`drawctx+1692`（UV セット数）を 0 に戻す**（F-207 の値）
- `DrawEnd` が**溜まっているバッチを自動で流す**
- **記録の経路に `GpuCmd_SplitAndSubmit` は出てこない**（`sub_4D72C4` は生のコマンド語を
  カーソルへ直接書く）。したがって記録中に GX キューのエントリは作られない

### 実装（`PATCHES/cave_node_record.py`）と IDA での検証

登録ケーブに「一度だけ自前リストを作る」処理を入れ、記録ケーブからは base/size の
手書きを削除した。`drawctx` は `mgr+0x364` から求める。F-256 のゲートは撤去した。

**実機には一切適用していない。** 生成語を静的 IDB の `.text`（ファイル実体のある領域）へ
一時的に書き込み、IDA に逆アセンブルさせて確認し、元のバイト列へ戻した
（`idb_save` はせず、読み戻しで復元を確認）。ケーブの基準を `0x836000` 台にして
生成し直すことで `BL` の飛び先も IDA が正しい関数名で解決した。

IDA が解決した呼び出し: `GpuCmd_GetProperty` / `sub_121B34` / `GpuCmd_SelectList` /
`sub_121988` / `GpuCmd_SelectList` / `ssys_ma_lyt_LayoutMgr_AddLayout`。
契約フィールドの書き込み `STR R2,[R1,#0x114]` / `[R1,#0x118]` / `STRB R2,[R1,#0x11C]` /
`STRB R2,[R1,#0x11D]` も意図通り。

### ★逆アセンブルで見つけて直した不具合（F-260 から継続）

登録ケーブで `R3`（リストの tail）が prev/next の検査で上書きされ、
**雛形の複製が永久に実行されない**状態だった。`MOV R12,R3` で退避して解決。
机上では気付けなかった。

---

