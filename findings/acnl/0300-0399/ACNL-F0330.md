---
id: ACNL-F0330
aliases:
- F-306
title: F-306 (HIGH・実機) — ★★★TextWriter 直呼びで描けた。TextBox の DrawSelf を通さない
summary: F-301 で「TextBox は必須ではない」と結論した経路を実機で成立させた。
date: '2026-09-06'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4948832
- 5067156
- 8290120
- 5072240
- 7589476
- 5070000
- 5067800
- 5067276
- 4947436
- 4947168
- 4947776
- 9942868
- 9942900
- 9942932
- 5069592
- 8291464
- 9945268
- 8622080
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:19805-19931
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-306 (HIGH・実機) — ★★★TextWriter 直呼びで描けた。TextBox の DrawSelf を通さない

F-301 で「TextBox は必須ではない」と結論した経路を実機で成立させた。
自前 Pane の **vtable スロット 26（DrawSelf）を自前ケーブ**にし、
ケーブが `TextWriter` / 標準 TextBatch を直接回す。

### A. ケーブが呼ぶ 9 関数（全部 idalib で引数を確定）

| 番地 | 契約 |
|---|---|
| `0x004B8360` | `FlushBatch(R0=drawctx, R1=cursor) -> cursor` |
| `0x004D5194` | `ResetBatch(R0=writer)` … `batch+4=0 / +8=0 / +0x1C=0` |
| `0x007E7F48` | `DrawString(R0=writer, R1=UTF-16, R2=文字数)` |
| `0x004D6570` | `BuildCommandStream(R0=drawctx, R1=writer)` |
| `0x0073CE64` | `BuildMatrix(R0=pane, R1=*(drawctx+0x66C))` |
| `0x004D5CB0` | `EmitStatePrefix(R0=drawctx, R1=cursor) -> cursor` |
| `0x004D5418` | `ExpandCornerColors(R0=desc)` |
| `0x004D520C` | `CopyToCommandBuffer(R0=desc, R1=cursor, R2=drawctx) -> cursor` |
| `0x004B7DEC` | `UpdateDrawState(R0=drawctx, R1=cursor, R2=0, R3=1) -> cursor` |

提出の順序は `TextBox_EmitBatchToGpuCommands 0x4B7CE0` の assembly をそのまま写した:

```
語数(batch+0x1C)==0 なら cursor を返す
drawctx+0x6A2=4 / +0x6A0=1 / +0x6A1=1
BuildMatrix(pane, *(drawctx+0x66C))
drawctx+0x25=3
cursor = EmitStatePrefix(drawctx, cursor)
desc+0x44 = batch → ExpandCornerColors(desc)
cursor = CopyToCommandBuffer(desc, cursor, drawctx)
desc+0x44 = 0
cursor = UpdateDrawState(drawctx, cursor, 0, 1)
```

★`UpdateDrawState` の第 3 引数が 0 のとき `0x4B7F40` へ飛び、
3 つの大域（`0x97B754`/`0x97B774`/`0x97B794`）を 0 にしてから
第 4 引数が非 0 なら `TextDraw_EmitStateSuffix` を呼んで `cursor+0x18` を返す。

### B. ★TextWriter のひな型 25 語を**全語**確定（推測ゼロ）

`sub_4D5B18 (0x4D5B18)` と `sub_7E8488 (0x7E8488)` の全ストアを読み取った:

```
+00=0  +04..+18=0xFFFFFFFF  +20=0(byte)  +24=+28=1.0  +2C..+38=0.0
+3C=+40=+44=0  +48=0 +49=0xFF  +4C=FLT_MAX  +50=+54=0  +58=4  +5C=0
+60=0x0097C0B4（既定 TagProcessor）
```

→ **`sub_7E8488` を呼ばずに、ひな型を丸ごと用意して 25 語コピーすれば同じ状態になる。**
我々が変えるのは **+18/+1C 色・+20 諧調・+24/+28 倍率・+3C フォント・
+44 バッチ・+4C 折り返し幅・+5C 整列** の 8 欄だけ。

★**writer の +08..+14（4 隅色）は即時経路専用**で、バッチ経路では
`BuildCommandStream` が `TextDraw_BuildFourCornerColors` で作り直す。
だから writer に `ExpandCornerColors` を掛ける必要はない。

### C. ケーブ（75 語 = 0x12C バイト）

```
DrawSelf(R0=pane, R1=cursor, R2=DrawInfo, R3=drawctx):
  1. drawctx[0x24] != 0 なら FlushBatch（Picture は drawctx に溜まるだけ。F-301）
  2. 制御+0x10（dirty）が立っていれば:
       ひな型 25 語 -> 作業域へコピー / ResetBatch / DrawString / BuildCommandStream
       dirty = 0
  3. batch+0x1C == 0 なら何も積まずに cursor を返す
  4. 上の提出手順
  5. 新しい cursor を返す
```

### D. ★実機へ入れる前にやった検証

1. **`.text` の空きをゼロ連続で機械測定**した。
   空き `0x838018-0x838200` / **`0x838534-0x838810`** / `0x838CE8-0x839000`。
   ★当初 `0x838810` を空きと決めつけたが**既存ケーブ（`E92D500F`）が入っていた**。
   採用は `0x838540`（前後を既存ケーブに挟まれ、`0x839000` の端から遠い）。
2. **事前監査**（全 LDR のリテラル参照先・全 BL の宛先が許可 9 関数・全分岐がケーブ内）→ 異常 0
3. **objdump で逆アセンブル** → 全 BL が意図どおりに解決
4. **輪へ繋がずに実機へ書き**、**デバッガの逆アセンブラで実機のバイトを確認**
   （75 語すべて設計と一致）。ケーブは誰からも参照されないので走らない
5. 領域の重なり検査（`batch_size(n)` を単一の生成元から取る）

### E. ★★事故 — `import` 経路の `sys.exit()` で IDA を 2 度落とした

`textwriter_cave.py` の末尾に

```python
if MODE == "asmdump":
    sys.exit(main_asmdump())
```

と書いたため、`textwriter_apply.py` が `import` した瞬間にこれが走り、
**`SystemExit` が ida-pro-mcp のリクエストハンドラごと落とした**。
CLAUDE.md に明記されている既知の罠を 2 回踏んだ。

**対処**: 入口を `if __name__ == "__main__":` で塞いだ。
**import される側のスクリプトは、モジュール階層で `sys.exit()` を通してはいけない。**

★併せて **`importlib.reload()`** を入れた。IDA の Python は一度読んだモジュールを
掴み続けるので、編集が反映されず古い定義で動く。

### F. 実機の結果 — オフラインの予測と一致

| | 実機 | 予測 |
|---|---|---|
| バッチ件数 | **15 / 15** | 全文字 |
| 構築済み / dirty | 1 / 1→**0** | ケーブの再構築が走った |
| コマンド語数 | 254 / 上限 1224 | — |
| 下画面の記録長 | **0x5A30** | — |
| writer 作業域 | font/batch/倍率 2.00/整列 0x111/TagProc 0x97C0B4 | ひな型どおり ✔ |
| 記録[0] 'T' UV | `(0.2578,0.8047)-(0.2969,0.7500)` | idx=52 U=33 V=25 ✔ |
| 字の大きさ / 送り | 幅 10.0 / 高 −14.0 / X=−90.0 | 5×2 / 7×2 / advance 6×2 ✔ |

**画面に「TEXTWRITER 0123」が自前フォントで表示された。**

### G. TextBox 方式との比較（実測）

| | TextBox（F-305） | TextWriter 直呼び（F-306） |
|---|---|---|
| 自前コード | **0 語** | **75 語** |
| 必要な追加データ | TextBox 0x108 + Material 0x50 | vtable 複製 0x110 + ひな型 0x64 + 作業域 0x64 + 記述子 0x50 + 制御 0x20 |
| `DrawInfo+0x80` の作業オブジェクト | **要る**（`LayoutMgr+0x1C`） | **要らない** |
| 再構築の制御 | TextBox の dirty 任せ | **自前**（制御+0x10） |
| バッチ（1 文字 ~356B） | 同じ | 同じ |

**どちらも成立する。** TextWriter 直呼びの利点は
`DrawInfo+0x80` に依存しないことと、再構築の契機を自分で決められること。

