---
id: ACNL-F0320
aliases:
- F-296
title: F-296 (HIGH・実機) — ★借りた領域を返せる。**確保 → 解放 → 再確保の往復を実機で成立**
summary: F-295 で `nw::lyt` のヒープから 64KB 借りたが、**返す手段が無かった**。
date: '2026-09-04'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4951280
- 5675860
- 5675844
- 5625880
- 5624868
- 4951316
- 9892176
- 5075316
- 5075344
- 10186752
- 4603428
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:18845-18902
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-296 (HIGH・実機) — ★借りた領域を返せる。**確保 → 解放 → 再確保の往復を実機で成立**

F-295 で `nw::lyt` のヒープから 64KB 借りたが、**返す手段が無かった**。
アロケータ vtable の +0x0C を静的に特定し、実機で往復させて確定した。

### 関数

| 番地 | 中身 |
|---|---|
| `0x004B8CF0` | `nw::lyt AllocMemory(size, align)` — `off_96F150` → `vtable+0x08` を尾呼び |
| `0x00569B54` | `ssys::ma::Allocator::Alloc(this, size, align)` — `R1 = size + align` にして `heap->vtable[0x18]` を尾呼び |
| **`0x00569B44`** | **`ssys::ma::Allocator::Free(this, ptr)`** — `heap->vtable[0x1C]` を尾呼び |
| `0x0055D818` | ヒープ側 alloc |
| `0x0055D424` | ヒープ側 free。**`CMP R1,#0 / BXEQ LR`** で null 安全 |

**`Alloc` と `Free` は完全に対称。** どちらもポインタを素通しし、
ヘッダの付け外しをしない。だから **`Alloc` が返した番地をそのまま `Free` へ渡せばよい。**
`nw::lyt` 側に `AllocMemory` に対応する `FreeMemory` ラッパは無い
（`0x4B8D14` はもうペイン工場）ので、**`0x569B44` を直接呼ぶ。**

呼び方は `R0 = *(0x0096F150)`（アロケータ）、`R1 = 返す番地`。

### 解放の手順（この順序でないと危ない）

1. **描画を止める** — `build_pane_tree.py MODE="detach"`。
   ノードの `+0x20`（root Pane）を 0 にし、`+0x11D`（記録要求）を 1 にする。
   `nwlyt_DrawPaneTreeToCurrentList`（`0x4D7174`）は `0x4D7190` で
   **`*(layout+0x20) == 0` なら cursor を素通しして何も積まない**ので、
   これだけでゲームがオブジェクトを歩かなくなる。
2. **1 回記録させる** — Resume して 3 秒。`+0x108`（記録長）が
   `0x38E0 → 0` になる。**コミット済みの列が空になるまで解放しない。**
   止めただけでは前フレームの記録が毎フレーム再生され続ける。
3. **解放** — `alloc_lyt_heap.py MODE="free"`。`Render_FrameEnd` の一発ケーブ。
   スロットが 0 でなければ `Free` を呼び、**スロットを 0 にして二重解放を防ぐ**。
4. **ケーブを外す** — `MODE="uninstall"`。

### 実機での裏取り（独立した 2 つの結果）

| 見たもの | 結果 |
|---|---|
| スロット `0x009B7000` | `0x32EB0F60` → **`0`** |
| PC / 挙動 | `0x00463E24`（正常なゲームコード）。フォルトなし |
| **解放後の再確保** | **`0x32EB0F60`（同一番地）** — 空きリストへ戻っている証拠 |

そのあと `build` → `enable` でメニューを組み直し、
**74 枚が元通り描かれた**（記録長 `0x38D0`）。往復しても壊れない。

★再確保しただけでは描けない。**ヒープの free が空きリストのリンクを
領域内へ書き込む**ので、`build` で組み直すこと。

### 追加した手段

- `PATCHES/alloc_lyt_heap.py` に `MODE="free"`（17 語のケーブ、事前監査つき）
- `PATCHES/build_pane_tree.py` に `MODE="detach"`（描画だけ止める。vtable は触らない）

`disable` は vtable を旧ケーブ `CAVE_Q` へ戻してしまうので、
**解放の前段には `detach` を使う**こと。

