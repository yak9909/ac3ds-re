---
id: ACNL-F0371
aliases:
- F-345
title: 'F-345（2026-09-07）: 手紙は **2 つの大きな塊**を要る — 借りっぱなしでは通せない'
summary: '**confidence: HIGH**（実機の停止位置・オブジェクトの中身 + `sub_1FC55C` の逆コンパイル）'
date: '2026-09-07'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 3128228
- 2082444
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:22360-22432
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-345（2026-09-07）: 手紙は **2 つの大きな塊**を要る — 借りっぱなしでは通せない

**confidence: HIGH**（実機の停止位置・オブジェクトの中身 + `sub_1FC55C` の逆コンパイル）
F-344 の直し（借用 0x50000）を入れても**同じ場面で落ちた**。前より先へは進んでいる。

### 2 回目の停止

```
PC = 0x002FBBA4  Mem_Copy の中   R0(コピー先) = 0   R2 = 0x1FFE0
LR = 0x001FC68C  sub_1FC55C の中（1 回目と同じ関数）
```

`item::ResLoader`（`0x33132CD4`）を読むと **今度は成功している**:
`buf(+0xEC) = 0x32FCE580` / 状態 3 / `Item/Model/letter_shic.bcres` 131,456 B。

落ちたのは**その次**。`sub_1FC55C` を読むと:

```c
v8 = sub_4A5F90(v83, v4);          // v83 = { 256, 256, 1, ... } の画像を作る
                                   // v4 = sub_5691E4() = dword_96FC40 = 0x32C46038
                                   //      その +4 = 0x32C45F78 = ★nw::lyt の ExpHeap
v13 = (v8+56 の相対オフセット);      // 画像データへの相対参照
v17 = (v13+12 の相対オフセット);      // ★0 だったので v17 = nullptr
if (v17 - v6 <= 0 || ... ) sub_31C538();   // ← memcpy。コピー先が null のまま
```

**256 x 256 x 2 バイト = 131,072 B = 0x20000** で、落ちた `Mem_Copy` の大きさと一致。

### 手紙が nw::lyt ヒープに要求する量

| 何 | 大きさ |
|---|---|
| `Item/Model/letter_shic.bcres` | 131,456 B（0x20180） |
| 256x256 のテクスチャ（便箋の絵） | 131,072 B（0x20000） |
| **合計** | **262,528 B** |

### ★借りっぱなしでは不可能

```
ヒープ総量                3,866,624 B
手紙の場面でゲームが使う量  3,376,620 B
手紙の 2 つの塊              262,528 B
--------------------------------------
借りてよい上限（余裕ゼロ）    227,476 B
```

| 構成 | 配置 | 判定 |
|---|---|---|
| いま（通知 5・借用 0x50000） | 255,616 B | **入らない** |
| 通知 2 件まで削った F-342 の版 | 231,552 B | **入らない** |

**削っても通らない。借りっぱなしをやめるしかない。**

### ★GPU に見せる必要があるのは「アトラスだけ」

`DOCS/ctrpf_plugin.md` §4: プラグインヒープ（`new`）は **PA=0 で GPU に見せられない**。
だが自前 GUI の持ち物のうち **GPU が読むのはアトラスの画素だけ**:

| 持ち物 | 誰が読むか | GPU 可視が要るか |
|---|---|---|
| アトラス（32,768 B） | GPU（テクスチャ） | **要る** |
| Picture / Pane / Material | CPU（`Layout_RecordPaneTree`） | 不要 |
| フォント資源（ResFont/CWDH/CMAP） | CPU（`MapCharToGlyph`） | 不要 |
| バッチ（コマンド語） | CPU（`CopyToCommandBuffer` が `Mem_Copy`） | 不要 |

★バッチは**フラグ 0（Mem_Copy 経路）**にしてあるので `RangeCacheOp` を通らない
（`BuildCommandStream` 末尾の `if ((batch+0x09) & 2)` に入らない）。

→ **アトラス以外をプラグイン側のメモリへ移せば、借用は約 33 KB で済む。**
  そのとき手紙の場面の空きは 490,004 − 33,000 = 約 457,000 B で、262,528 B は楽に入る。

---

