---
id: ACNL-F0325
aliases:
- F-301
title: F-301 (HIGH・静的のみ) — ★F-300 の訂正。**TextBox は必須ではない。**文字描画の本体は `TextWriter`
summary: 利用者の指摘を受けて詰め直したところ、F-300 の
date: '2026-09-04'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4959608
- 4960744
- 5067276
- 5066412
- 4947168
- 4947188
- 4947272
- 4947276
- 4947280
- 7589840
- 1254128
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:19256-19362
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-301 (HIGH・静的のみ) — ★F-300 の訂正。**TextBox は必須ではない。**文字描画の本体は `TextWriter`

利用者の指摘を受けて詰め直したところ、F-300 の
「フォントを流用しても TextBox は自前で要る」は**言い過ぎだった**。

### 見落としていたこと

**1. `TextBox` は文字を描く機械ではない。設定を運ぶ Pane にすぎない。**

`nwlyt_TextBox_ConfigureTextWriter`（`0x4BAD78`）が TextBox から読むのは **7 欄だけ**:

| TextBox | → TextWriter | 意味 |
|---|---|---|
| `+0xE0` | `+0x3C` | Font |
| `+0xEC` | `+0x54` | 行間 |
| `+0xF0` | `+0x50` | 字間 |
| **`+0x48`（Pane の幅）** | `+0x4C` | 折り返し幅 |
| `+0xF4` | `+0x60` | TagProcessor（0 なら既定のまま） |
| `+0xFC`/`+0xFD` | `+0x5C` | 整列 |
| `+0xD8`/`+0xDC` | `+0x18`/`+0x1C` | 上下の色 |

**全部ただの値。** TextBox を経由せず TextWriter へ直接書けばよい。

**2. `sub_7E7F48(writer, UTF-16 文字列, 文字数)` が独立した入口。**
呼び出し元は 2 つだけで、どちらも TextBox の中（`RebuildBatchWriter` と
`nwlyt_TextBox_DrawText`）。だが関数自体は TextBox を引数に取らない。

**3. 描画経路は 2 本ある。前回は片方（バッチ）しか見ていなかった。**
**`nwlyt_TextBox_DrawText`（`0x4BB1E8`）が即時経路**で、バッチを使わず
`writer+0x40` の文脈へ直接積む。

**4. TextWriter の初期化は 1 回の呼び出しで済む。**
`sub_7E8488(writer)`:
```
sub_4D5B18(writer)                     ; CharWriter の初期化
writer+0x60 = &dword_0097C0B4          ; ★既定の TagProcessor（大域。自前で用意しなくてよい）
writer+0x4C = 0x7F7FFFFF (FLT_MAX)     ; 折り返しなし
writer+0x58 = 4 / +0x5C = 0 / +0x50 = 0 / +0x54 = 0
```

**5. `TextBatch_CopyToCommandBuffer`（`0x4D520C`）は記述子とバッチだけで呼べる。**
`TextBox_EmitBatchToGpuCommands` も TextBox も通さなくてよい。
記述子は約 `0x4A` バイトの平のデータ:

| 記述子 | 中身 |
|---|---|
| `+0x00`/`+0x04` | 色 2 つ（Material の `+0x10`/`+0x14` 相当） |
| `+0x18`/`+0x1C` | 上下の色 |
| `+0x20` | 諧調フラグ（0 or 2） |
| `+0x44` | **バッチ**（呼んだあと 0 に戻す） |
| `+0x49` | α（Pane の `+0xB5` 相当） |

**6. バッチを設定すれば `writer+0x40`（RectDrawer 文脈）は一度も読まれない。**
`EmitGlyphQuad`（`0x4D4EAC`）は `writer+0x44` が非 0 なら
44 バイトの記録を積んで即 return する。**RectDrawer は要らない。**

### したがって — TextBox 抜きの最小経路

```
自前 Pane の DrawSelf(pane, cursor, DrawInfo, drawctx):
  1. drawctx[36] != 0 なら cursor = DrawCtx_FlushBatch(drawctx, cursor)
  2. writer(0x64 バイト) に sub_7E8488(writer) で既定値
  3. writer+0x3C = フォント / +0x44 = バッチ / +0x18,+0x1C = 色
     +0x2C,+0x30 = 位置 / +0x24,+0x28 = 倍率 / +0x4C = 折り返し幅
  4. sub_7E7F48(writer, UTF-16, 文字数)          → バッチへグリフ記録
  5. TextBatch_BuildCommandStream(drawctx, writer, ...)  → コマンド列を作る
  6. 0x4A バイトの提出記述子を組む（色・α・+0x44 = バッチ）
  7. cursor = TextBatch_CopyToCommandBuffer(記述子, cursor, drawctx)
```

**TextBox も Material も要らない。**

### ★逆に判明した障壁 — 完成品の TextBox を使うほうが面倒

`TextBox_EmitBatchToGpuCommands`（`0x4B7CE0`）は 5 番目の引数（**DrawInfo**）から
`*(DrawInfo + 0x80)` を読み、そこを作業オブジェクトとして使う
（`+0xF8` が提出記述子、`+0x13C` がバッチの置き場）。

```
0x4B7CE0  PUSH {R4-R9,LR} / SUB SP,#0xC
0x4B7CF4  LDR R4,[SP,#0xC+arg_0]     ; 第 5 引数
0x4B7D48  LDR R0,[R4,#0x80]          ; ★DrawInfo+0x80
0x4B7D4C  ADD R4,R0,#0xF8            ; 提出記述子
0x4B7D50  STR R7,[R0,#0x13C]         ; バッチを置く
```
（呼び出し側 `0x73CFD0 STR R6,[SP]`、R6 = 入口の R2 = DrawInfo で確認）

- **`nw::lyt::DrawInfo` のコンストラクタ（`0x1322F0`）は `+0x80` を 0 に初期化する**
- **実機のタイトル画面のレイアウトでも `DrawInfo+0x80` = `0x1C`（ポインタではない）**
  → このレイアウトは TextBox を描けない
- 自前ノードの DrawInfo（node+0x30）も当然 0

つまり **TextBox をそのまま使うなら、この作業オブジェクトを別途用意する必要がある。**
「コードを 1 語も書かずに TextBox を置くだけ」とはいかない。

### 訂正後の結論

| | 必要なもの | 自前コード |
|---|---|---|
| **TextWriter 直呼び** | writer 0x64 + バッチ + 記述子 0x4A + フォント | **ケーブ 1 本**（上の 7 手順） |
| **TextBox** | TextBox 0x108 + Material 80 + バッチ + フォント + **`DrawInfo+0x80` の作業オブジェクト** | 0 語（ただし作業オブジェクトの素性が未確定） |

**どちらも成立する。TextBox は必須ではない。**
容量はどちらもバッチ（1 文字 356〜377 バイト）が支配するので大差ない。

★すべて静的解析のみ。実機では未検証。

