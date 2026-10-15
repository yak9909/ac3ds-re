---
id: ACNL-F0226
aliases:
- F-201
title: 'F-201: F-200 の検証。**1 件の訂正と、GPU ハングの静的な説明** — 静的解析'
summary: F-200 を疑って再検証した。**ユーザーの指示「confidence HIGH でも信用しきらない」に従う。**
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5173620
- 5173676
- 9328728
- 9328732
- 9328736
- 9328716
- 9328720
- 9328724
- 8063528
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12337-12416
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-201: F-200 の検証。**1 件の訂正と、GPU ハングの静的な説明** — 静的解析

F-200 を疑って再検証した。**ユーザーの指示「confidence HIGH でも信用しきらない」に従う。**

### 1. アセンブリで裏付けが取れたもの

| 主張 | 検証 | 結果 |
|---|---|---|
| `Frame_DrawPass1024` のシーン呼び出し順 | 逆アセンブル | **分岐なしの直列。順序確定** |
| `Render_DrawScene0/1` の引数が 1024 | `MOV R0, #0x400` | **確定** |
| 再生が `if(a1==1024)` の外 | `4EF0A4 CMP R0,#0x400` / `4EF0A8 BNE -> 0x4EF174`、再生は `0x4EF1AC` | **確定。両パスで走る** |
| `Frame_EndDrawPass1024` が描画の最後 | 直後は `CMP R4,#1` と排他処理だけ | **確定** |

### 2. ★訂正 — 「xref 1 件だからフレームに 1 回」は成り立たない

`Frame_DrawPass1024` / `1040` の参照は**データ 1 件ずつ**（`0x8E5858` / `0x8E585C`）で、
**関数ポインタ表**から呼ばれる（`0x8E5860` が NULL 終端）。

```
0x8E584C: 001B6B84
0x8E5850: 00560184
0x8E5854: 001B7090
0x8E5858: 001B71C4   Frame_DrawPass1024
0x8E585C: 001B72E4   Frame_DrawPass1040
0x8E5860: 00000000   終端
```

**xref の数からは呼び出し回数を導けない。**

ただし独立した裏付けがある。`Render_FrameEnd` は `Frame_DrawPass1040` の 1 か所からのみ
呼ばれ、実測でフレームフラグが **4 秒で約 120 回 = 30 fps** と一致していた。
よって **`Frame_DrawPass1040` はフレームに 1 回**。
表の最終要素なので**ディスパッチャもフレームに 1 回**回っており、
`Frame_DrawPass1024` も 1 回と考えられる（**表からの推論。直接の証拠ではない**）。

### 3. ★★GPU ハングの静的な説明が見つかった

**`GpuCmd_SplitAndSubmit` の呼び出し元は、カーソル由来の値を呼び出しをまたいでキャッシュする。**

`GpuCmd_ReplayRecordedListRange`（`0x7B0A28`）:

```c
v14 = g_GpuCmdPtr;                    // ★呼び出し前にキャッシュ
v15 = g_GpuCmdPtr - mgr[1];
mgr[3] = v15;
if (mgr[5] != v15) {
    GpuCmd_SplitAndSubmit();          // ← ここでフックが発火
    ...
    *v14 = 0; v14[1] = 524894;        // ★古い v14 に書く
    g_GpuCmdPtr = (int)(v14 + 2);     // ★★古い値でカーソルを巻き戻す
}
```

**フック内で `g_GpuCmdPtr` を進めると、戻った呼び出し元が古い値でカーソルを巻き戻し、
私たちが書いたデータの上にパディングコマンドを書く。** コマンド列が壊れて GPU が止まる。

`Render_DrawSceneIndexed` も同様で、`SplitAndSubmit` の直後に
`GpuCmd_CommitListAndCaptureDelta` で範囲を記録するため、
私たちの追記分がシーンの記録範囲に誤って計上される。

**したがって `GpuCmd_SplitAndSubmit` をフックしてカーソルを動かしてはいけない。**
これは F-197 と今回の 2 回のハングを両方説明する。

### 4. 手順上の誤り — ツールを取り違えた

検証の途中で**デバッガ側（ida-pro-mcp）で静的 IDB を読もうとし、
全部 `0xFF` の結果を得た**。3DS が再起動中で実機メモリが読めなかっただけ。
そのまま結論に使えば誤読していた。

**静的解析は idalib-mcp、実行時の値は ida-pro-mcp。**
`CLAUDE.md` の「読むと全部 `0xFF` は未マップの徴候」がここでも効いた。

### 5. まだ推測のままのもの

- 1024 / 1040 と上画面 / 下画面の対応
- `Frame_EndDrawPass*` の時点でどの画面のフレームバッファが束縛されているか
- ディスパッチャがフレームに 1 回であること（表からの推論）

---

