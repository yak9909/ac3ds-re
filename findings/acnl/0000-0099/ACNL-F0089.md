---
id: ACNL-F0089
aliases:
- F-51
title: F-51 フェードの正体は `FaderColor`、`FaderMoment` に差し替えれば消える — `HIGH`
summary: F-50 で「`0x568BF8` が唯一の調整点」と書いたが、**フェードには効かない。**
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5671928
- 5412236
- 1798036
- 1798048
- 1798060
- 6966992
- 9750092
- 6967988
- 1798124
- 6315072
- 6315708
- 6520848
- 6521536
- 7704436
- 7704644
- 1869544
- 5658872
- 5658608
- 9221872
- 9438284
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2749-2854
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-51 フェードの正体は `FaderColor`、`FaderMoment` に差し替えれば消える — `HIGH`

F-50 で「`0x568BF8` が唯一の調整点」と書いたが、**フェードには効かない。**
ユーザーの「ウィンドウを開くときのフェードが残る」という指摘は正しかった。

### なぜ `g_UiAnimRate` がフェードに効かないのか

```
Fade_Init (0x52958C)
  UiAnim_Load(this+952,  "fade_In_Fade.bclan",  layout)
  UiAnim_Load(this+992,  "fade_Out_Fade.bclan", layout)
  UiAnim_Load(this+1112, "fade_kind.bclan",     layout)
  UiAnim_Load(this+1032, "fade_in_L.bclan",     layout)
  UiAnim_Load(this+1072, "fade_out_L.bclan",    layout)
      -> UiAnim_Init: this+16 = g_UiAnimRate    ★コピー
```

**`Fade_CreateSingletons` / `Wipe_CreateSingletons` / `Fader_CreateAll` は
起動時に 1 度だけ、`0x1B6F94` / `0x1B6FA0` / `0x1B6FAC` の連続呼び出しで実行される。**

`UiAnim_Init` はそのとき `g_UiAnimRate` を**値としてコピー**するので、
**後から `0x568BF8` を書き換えても既存のフェードには反映されない。**
メニューのレイアウトは開くたびに作り直されるので新しいレートを拾う。
「メニューは速くなったのにフェードだけ残る」現象はこれで説明できる。

**F-50 の「唯一の調整点」は「開くたびに作られるもの」に限った話だった。訂正する。**

### フェーダの構造

`Fader_CreateAll` (`0x6A4ED0`) が起動時に 9 個作り `g_FaderRegistry` (`0x94C64C`) へ:

| # | 種別 | 画面 | 色 |
|---|---|---|---|
| 1 | `FaderColor` | 上 | 黒 |
| 2, 3 | `FaderColor` | 上 | 白 |
| 4 | `FaderWipe` | 上 | — |
| **5** | **`FaderMoment`** | 上 | — |
| 6 | `FaderColor` | 下 | 黒 |
| 7, 8 | `FaderColor` | 下 | 白 |
| **9** | **`FaderMoment`** | 下 | — |

`Fader_SetKind(topKind, bottomKind)` (`0x6A52B4`) が種別 → レジストリの引き当て:

```
kind 0 -> [4] FaderWipe        kind 1 -> [1]/[6] FaderColor 黒
kind 2 -> [5]/[9] FaderMoment  ★フェードなし
kind 4 -> [2]/[7] FaderColor 白
kind 5 -> [3]/[8] FaderColor 白(flag1)
```

呼び出し元 7 箇所と渡す値（実測）:

| 呼び出し | kind | |
|---|---|---|
| `0x1B6FEC` | (1, 1) | **起動時の既定 = 黒フェード** |
| `0x605C40` / `0x605EBC` | オブジェクトのフィールド由来 | スクリプト系 |
| `0x638010` / `0x6382C0` | (0, 3) | `FaderWipe` |
| `0x758F74` / `0x759044` | **(2, 2)** | **素で既にフェードなし** |

### `FaderMoment` は待ちゼロ

```c
FaderMoment_Update (0x1C86E8):
  if (state == 2) { state = 1; flags |= 1; Fade/Wipe を即座に隠す; return 1; }
  if (state == 3) { state = 0; flags |= 2;                        return 1; }
```

**ゲーム自身が「フェードなし」の実装を持っている。** それを選ばせるだけでよい。

### 修正

```
006A52B8 E3A05002   ; MOV R5,R0 -> MOV R5,#2   上画面
006A52C4 E3A04002   ; MOV R4,R1 -> MOV R4,#2   下画面
```

`Fader_SetKind` の先頭で引数を握り潰す。呼び出し元 7 箇所すべてに効く。

### 【重要】誤りやすい点 — 使われていない「20 フレーム」

`ssys::co::FaderBase` のコンストラクタ (`0x5658F8`) は

```
0056590C  MOV R1, #0x14      ; 20
00565914  STR R1, [R0,#8]    ; this+8 = 20（フレーム数）
```

を実行し、`FaderBase_Update` (`0x5657F0`) が `this+12` を `this+8` まで数える。
**いかにもフェードの尺に見えるが、これは到達しない。**

- 派生は `FaderColor` / `FaderMoment` / `FaderWipe` の 3 つだけ
  （`TypeInfo` の base が `ssys::co::FaderBase` = `0x8CB6F0` のものを全走査して確認）
- **3 つとも vtable の `+0x18`（Update）を上書きしている**
- `FaderBase` の vtable (`0x90044C`) を参照するのは自身の ctor だけ = 素の
  `FaderBase` は生成されない
- `FaderBase_Update` への参照も vtable の 1 件のみ

`Fader_SetDurationAndStart` (`0x565320`) が `fader+8 = 引数` を書き
（`0x6382CC` は `FadeStart(20)` を渡す）、いかにも尺に見えるが、
`FaderColor_Update` は `Fade_IsIdle` を待つだけで `this+8` を読まない。

**「それらしい定数」を見つけた時点で満足せず、到達可能かを確かめること。**
今回は vtable の上書き状況と派生クラスの全列挙で否定できた。

---

