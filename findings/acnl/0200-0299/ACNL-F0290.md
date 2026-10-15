---
id: ACNL-F0290
aliases:
- F-267
title: 'F-267: 雛形の複製を廃止した。写し元依存が実装から消えた — `HIGH`（静的のみ）'
summary: F-259 の実装は、本物の Layout から `+0x28` の 20 語（`0x50` バイト）を写して雛形にしていた。
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8611820
- 8611824
- 8611828
- 8611832
- 8611864
- 8611584
- 8622080
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:15975-16041
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-267: 雛形の複製を廃止した。写し元依存が実装から消えた — `HIGH`（静的のみ）

F-259 の実装は、本物の Layout から `+0x28` の 20 語（`0x50` バイト）を写して雛形にしていた。
F-264〜F-266 でその 20 語の意味が全部割れたので、複製が不要になった。

| 語 | 意味 | 誰が読むか | 現在 |
|---|---|---|---|
| `+0x28` / `+0x2C` | 幅・高さ（float） | scissor（F-262）と投影（F-266）の両方 | **F-264 で自前** |
| `+0x30` | DrawInfo 先頭語 | **再生経路のどこからも読まれない** | 放置 |
| `+0x34`〜`+0x74` | 投影行列 16 語 | `nwlyt_Drawer_EmitProjectionUniform`（F-265） | **F-266 で自前** |

`+0x30` が読まれないことの根拠:
`nwlyt_Drawer_BeginLayoutReplayState(drawer, this+0x30, 0)` は
第 3 引数 `a3 = 0` を drawer vtable `+0x10` へ渡し、DrawInfo のポインタは
`nwlyt_Drawer_EmitProjectionUniform(drawer, cursor, DrawInfo + 4)` にしか使わない。
`Layout_ReplayRecordedList` の他の参照は `+0x100`〜`+0x11C`、`+0x124`、
`+0x134`、`+0x138`〜`+0x148`、`+0x320` であって `+0x30` は無い。

**これで「その boot で最初にリスト末尾だったレイアウトが何か」という不定要素が
実装から完全に消えた。** `scratchpad/MEMO_f260_verify.md` の未検証項目 5 は解消。

`+0xF8` は「雛形を写したか」から**「寸法と投影を入れたか」**へ意味替えした。
記録要求のゲート（`+0xF8` が立っているときだけ `+0x11D` を立てる）は形を変えていない。

### ★全体を IDA で通して見つけたバグ（実機には入れていない）

`BL ssys_ma_lyt_Layout_SetupProjectionMatrix` は当然 `R0`-`R3` / `R12` を壊す。
呼び出しの後、`R1`（ノード）は取り直していたが **`R0`（mgr）を取り直していなかった**。
その直後の `ssys_ma_lyt_LayoutMgr_AddLayout(mgr, node, screen)` に、
`R0` = `SetupProjectionMatrix` の戻り値（= ノード+0x34 のポインタ）が渡っていた。

```
0x8367ec BL   ssys_ma_lyt_Layout_SetupProjectionMatrix
0x8367f0 LDR  R0, =MGRP        ← 追加
0x8367f4 LDR  R0, [R0]         ← 追加
0x8367f8 LDR  R1, =NODE
...
0x836818 BL   ssys_ma_lyt_LayoutMgr_AddLayout
```

**部分だけを逆アセンブルしていたら見逃していた。** 生成器を変えたら
**ケーブ 1 本を丸ごと IDA に通す**こと。監査スクリプトは分岐先とリテラルしか見ないので、
レジスタの生存区間は見つけられない。

### 検証

上下とも全 87 / 82 語を空き `.text`（`0x836700`）へ当てて逆アセンブルし、
`PUSH` から戻りの `B` まで全命令を確認した。分岐先はすべてケーブ内か命名済みのゲーム関数。

- 上（A1）: 戻り `B loc_566DFC`（`RenderTop`+4）、`AddLayout` の `R2 = 0`
- 下（A2）: 戻り `B loc_568F9C`（`RenderBottom`+4）、`AddLayout` の `R2 = 1`

復元後のバイト列は `NCCH/exefs/code_runtime.bin` と完全一致。監査: 総異常 0 件・重なりなし。

### ケーブ配置（F-267 時点。現行）

```
CAVE_Q=0x838200(382) CAVE_P=0x838800(35)  CAVE_V=0x838890(44)
CAVE_A1=0x838940(87) CAVE_A2=0x838AA0(82) CAVE_N=0x838BF0(11)
CAVE_M=0x838C20(7)   CAVE_B=0x838C40(12)  CAVE_U=0x838C70(12)
CAVE_F=0x838CA0(10)  CAVE_T=0x838CD0(2)    末尾 0x838CE0 / 上限 0x839000（余り 800 バイト）
```

**未適用。実機へは入れていない。**

---

