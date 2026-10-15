---
id: ACNL-F0275
aliases:
- F-252
title: 'F-252: 2D レイアウトの描画は「1 本のリストを画面ごとに 2 回再生」する — `HIGH`（静的。動的照合は未実施）'
summary: '> **★F-253 で大幅に訂正した。単体で読まないこと。** リストは 1 本ではなく 2 本（`mgr+0x04`=上画面 / `mgr+0x10`=下画面）、'
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1798596
- 5664248
- 1798884
- 5673648
- 5673344
- 1260132
- 5672856
- 5667776
- 5074064
- 5669596
- 5669736
- 5670280
- 5670260
- 5664356
- 5664304
- 5664324
- 5664344
- 1048576
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:14668-14806
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0276", "ACNL-F0295"]
---
## F-252: 2D レイアウトの描画は「1 本のリストを画面ごとに 2 回再生」する — `HIGH`（静的。動的照合は未実施）

> **★F-253 で大幅に訂正した。単体で読まないこと。** リストは 1 本ではなく 2 本（`mgr+0x04`=上画面 / `mgr+0x10`=下画面）、
> パスは 3 本（`0x400` 上左目 / `0x410` 上右目 / `0x401` 下）、下画面の投影は 320x240 である。
> 「下画面が 0.8 倍なのは投影幅 400 のせい」という F-208 との一致は**偶然であり、取り下げた**。
> 以下のうち、パスの対応と `LayoutList_SetDisplay` の構造・`Layout+0x134` の役割はそのまま正しい。


`REFERENCES/TEXTS/render.txt`（gokiro 氏）を設計の参考として読み、**本作 JPN 無印の
`code.bin.i64` 側で独立に検証した**。外部ログを仕様として採用してはいない。

### 画面パスの正体（render.txt と一致）

| 我々の名前 | 実体 | 根拠 |
|---|---|---|
| `Frame_DrawPass1024` (`0x1B71C4`) | **上画面パス** | `ssys_ma_lyt_LayoutMgr_RenderTop(0x566DF8)` を呼ぶ |
| `Frame_DrawPass1040` (`0x1B72E4`) | **下画面パス** | `ssys_ma_lyt_LayoutMgr_RenderBottom(0x5692B0)` を呼ぶ |

`1024` / `1040` はレイアウト構造体のオフセットではなく **display トークン**である。
`0x400 = 1024`（NN_GX_DISPLAY0 = 上）、`0x410 = 1040`（NN_GX_DISPLAY1 = 下）。
同じ値が `Render_DrawScene0` / `Render_DrawScene1` の引数にも渡っている。

```
RenderTop(mgr)    : (*(mgr+4 の vtable +0x08))(mgr+4)   ← RecordChildren
                    SetDisplaySize(mgr, 0x190, 0xF0)
                    LayoutList_SetDisplay(mgr+4, 0x400)
RenderBottom(mgr) : SetDisplaySize(mgr, 0x190, 0xF0)
                    LayoutList_SetDisplay(mgr+4, 0x410)
                    sead_List_UnlinkAll(mgr+4)
```

### ★1 本のリストしかない（render.txt との相違点）

`ssys_ma_lyt_LayoutMgr_CreateInstance(0x569180)` は
`mgr+0x00 = vtbl_LayoutMgr`、`mgr+0x04 = vtbl_LayoutList`、`mgr+0x10 = vtbl_LayoutList`
と 2 本の `LayoutList`（各 12 バイト = vtable / head / tail）を埋め込む。
しかし `mgr+0x10` は `sub_566F44` が `vtbl_ssys_ma_lyt_TexBufList` へ差し替える派生であり、
**テクスチャバッファ用**である。

`RenderTop` も `RenderBottom` も `mgr+4` を使う（`ADD R0,R4,#4` を逆アセンブラで確認）。
`ssys_ma_lyt_LayoutMgr_GetInstance(0x133A64)` は `dword_96FC38` を返すだけなので、
両パスの `mgr` は同一である。したがって **ACNL の Layout 用リストは `mgr+4` の 1 本だけ**。
render.txt の `m_LayoutListTop` / `m_LayoutListBottom` という 2 本構成とはここが異なる。
外部資料は構造の説明としては有用だが、**番地・構成は本作で取り直すこと**。

ノードは `+4 = prev`、`+8 = next`。`sead_List_UnlinkAll` は
下画面パスの最後にリスト全体を空にする。すなわち **Layout の登録はフレームごとの一時的なもの**で、
F-238 / F-239 の「固定 id・固定 heap ポインタで対象を選んではいけない」という結論の
構造的な裏付けになる。

**未解決**: 静的にはリストが 1 本なのに、F-205 は「パスごとに最後の Layout が違う」と実測した。
したがってノードは 2 パスの間に足されるか外されるかしている。**その追加経路はまだ特定していない。**
リストが両パスで同一なら全 Layout が両画面に出るはずで、実機の見た目と矛盾する。
この矛盾が解けるまで「上下の描き分けはリストで決まる」と結論しない。

### 上下で投影は同じ。下画面が 0.8 倍になる理由（F-208 と独立に一致）

`SetDisplaySize` の引数は**両画面とも `0x190, 0xF0` = 400 x 240**（逆アセンブラで確認）。
投影が 400 幅なのに下画面の実フレームバッファは 320 幅なので、

```
上画面 1 単位 = 400/400 = 1.0 px      縦 240/240 = 1.0 px
下画面 1 単位 = 320/400 = 0.8 px      縦 240/240 = 1.0 px
```

これは F-208 で実機の目盛りから測った「横 0.8 / 縦 1.0」と**独立に一致する**。
座標系の食い違いは Layout ごとの性質ではなく、**画面ごとの固定倍率**だった可能性が高い。

> ### ★★★【F-272 による訂正】この小節は**二重に誤り**である
>
> **(1) 値が誤り。** 下画面パス `ssys_ma_lyt_LayoutMgr_RenderBottom`（`0x568F98`）は
> `SetDisplaySize(0x140, 0xF0)` = **320x240** を使う。両画面 400 ではない。
> 当時 3 本目のパスに印を付けていなかったための取り違えである（F-253 で訂正済み）。
>
> ```
> RenderTop        (0x566DF8) SetDisplaySize(400,240) → SetDisplay(mgr+4,    0x400)
> RenderTopRightEye(0x5692B0) SetDisplaySize(400,240) → SetDisplay(mgr+4,    0x410)
> RenderBottom     (0x568F98) SetDisplaySize(320,240) → SetDisplay(mgr+0x10, 0x401)
> ```
>
> **(2) 機序が誤り。** `SetDisplaySize` が出すのは**ビューポート**であって投影行列ではない。
> 投影は **各 Layout の `+0x28` / `+0x2C`（幅・高さ）**から
> `ssys_ma_lyt_Layout_SetupProjectionMatrix`（`0x567BC0`）が作り、
> `Layout+0x34` の 16 語として保持され、**replay 時**に
> `nwlyt_Drawer_EmitProjectionUniform`（`0x4D6C90`）が uniform index 0 へ流す
> （F-265 / F-266）。
>
> **正しい説明**: 旧経路の「横 0.8 / 縦 1.0」は、相乗り先の Layout 自身の `+0x28` が 400
> だったからである。320 幅のビューポートで `320/400 = 0.8`、高さは両方 240 なので `1.0`。
> **F-208 の見出し「レイアウトごとに投影が違う」がそのまま正しい機序**であり、
> 「画面ごとの固定倍率」ではない。
>
> F-208 が実測した id 15 のレイアウト（`+0x28 = 320`）が
> 「等方 1 単位 = 1px・原点は画面中央」になることも、同じ式から出る。

### `Layout+0x134` は画面フィルタではない

`Layout_ReplayRecordedList(0x5682DC)` の `0x568368` 以降:

```
LDR    R0,[R4,#0x108]     記録長
CMP    R0,#0 ; BLE 0x568588      0 なら再生せず return（F-240）
LDR    R0,[R4,#0x134]     display トークン
CMP    R0,#0x400 ; CMPNE R0,#0x410
LDRBEQ R1,[R4,#0x320] ; CMPEQ R1,#1
BEQ    0x568574           → Layout+0x124 の float を S17 へ（0x400 側は符号反転）
```

すなわち display は**立体視／画面別オフセットの符号**を決めるだけで、
**再生するかどうかは決めない**。`GpuCmd_ReplayRecordedListRange` の引数も
`Layout+0x100=id / +0x104=start / +0x108=length / +0x10C=aux` で display を含まない。

### ★注入点の第一候補: `LayoutList_SetDisplay` の出口 `0x566E64`

```
0x566E30 PUSH {R4-R6,LR}     R5 = display（0x400 / 0x410）
0x566E44 loop: STR R5,[R4,#0x134] / LDR R0,[R4] / LDR R1,[R0,#8] / BLX R1
0x566E58       LDR R4,[R4,#8] / CMP R4,#0 / BNE loop
0x566E64 POP  {R4-R6,PC}     ★唯一の出口
```

`0x566E64` に着いた時点で、**その画面の全 Layout の再生が終わっている**。
`R5` は callee-saved で入口以降変更されないため、ここで **上下の区別がそのまま取れる**
（ユーザー要件の「上画面と下画面に描画する区別」に直接対応する）。

この位置の利点は 3 つあり、`HANDOFF_CHEATMENU.md` §2 の未解決 3 件に対応する:

1. 積む先が Layout の記録リスト（容量 `0x1000` 級）ではなく**主リスト**（F-234 で
   容量 `0x100000` / 使用 `0x12B0` を実測）なので、F-232 の容量超過が構造的に起きない。
2. 全 Layout の後なので、ロード画像 Layout（F-234 の id 10）にも覆われない。
3. 座標系が候補 Layout ごとに変わらず、直前の `SetDisplaySize` で決まる 400x240 に固定される。

**これはまだ仮説である。** F-235 で `Frame_EndDrawPass1024` の主リスト末尾に積んだときは
画面更新が止まった。`0x566E64` は Layout 再生列の内側なので状況は異なるが、
実機で確かめるまで安全とは言わない。ida-pro-mcp が再接続でき次第、
**まず読み取り専用で** 出口到達回数・`R5`・主リストの `g_GpuCmdPtr` / `g_GpuCmdEnd` を採取する。

---

