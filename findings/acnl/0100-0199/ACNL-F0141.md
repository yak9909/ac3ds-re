---
id: ACNL-F0141
aliases:
- F-103
title: 'F-103: ★GX キューを実機で直接読み、1 フレームの構成を観測'
summary: 'confidence: **HIGH**（静的 + 動的。TODO-48）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6172-6252
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-103: ★GX キューを実機で直接読み、1 フレームの構成を観測

confidence: **HIGH**（静的 + 動的。TODO-48）

### 手法: breakpoint を使わない

CLAUDE.md「**高頻度実行箇所に breakpoint を置くとゲームがフリーズする**」。
GX 関数は毎フレーム 12 回＝秒 700 回超なので bp は不適。

代わりに **GX キューの中身をメモリから直接読んだ**。
`mgr[6]` に 28 (0x1C) バイト × `mgr[8]` 件が並ぶので、
**実際に使われている type バイトをそのまま観測できる。**

### 観測結果（id=1 のマネージャ、12 件 = 1 フレーム分）

```
[ 0] type=1 SetCommandList   +4=3229D0C0 +8=00000020 +12=0
[ 1] type=2 MemoryFill       +4=1F181200 +8=0000FFFF +12=00020000
[ 2] type=1 SetCommandList   +4=3229D0E0 +8=00005440 +12=0
[ 3] type=1 SetCommandList   +4=32677600 +8=00026070 +12=2
[ 4] type=1 SetCommandList   +4=322A2520 +8=00002090 +12=0
[ 5] type=3 DisplayTransfer  +4=1F000000 +8=324C71D0 +12=01A00100
[ 6] type=1 SetCommandList   +4=322A45B0 +8=00000290 +12=0
[ 7] type=1 SetCommandList   +4=32677600 +8=00026070 +12=2
[ 8] type=1 SetCommandList   +4=322A4840 +8=00002090 +12=0
[ 9] type=3 DisplayTransfer  +4=1F000000 +8=325DB350 +12=01A00100
[10] type=1 SetCommandList   +4=322A68D0 +8=00012490 +12=0
[11] type=3 DisplayTransfer  +4=1F00C000 +8=32563290 +12=01A00100
```

### 確定したこと

- **28 (0x1C) バイトのストライドが実機で成立**（きれいに復号できた）
- **type 1 / 2 / 3 が実際に発火**。F-100 の静的同定と一致
- `SetCommandList` の `+4` = アドレス、`+8` = サイズ
- **`[0]` が `mgr[1]`(基底) + サイズ `0x20`** = 新フレーム冒頭の小さなリスト。
  もう一方のマネージャ（構築開始直後）も
  **`SetCommandList(0x20)` + `MemoryFill` の 2 件だけ**で、
  **フレーム開始時の定型パターン**だと分かる
- `[2][4][6][8][10]` は `0x322Axxxx` = **id=1 のバッファ内**（基底 `0x3229D0C0` + 1MB）。
  `GpuCmd_SplitAndSubmit` が刻んだ断片
- **`[3]` と `[7]` は `0x32677600`（バッファ外）を `flags=2` で 2 回提出**。
  毎フレーム同じアドレス・同じサイズ `0x26070` なので
  **事前に構築された固定コマンドリスト**とみられる

### アドレス帯から読める意味

- **`MemoryFill` の宛先 `0x1F181200` は VRAM 帯（`0x1F000000`-）**
  → **フレームバッファのクリア**という読みが裏付けられた
- **`DisplayTransfer` は src が VRAM (`0x1F000000` / `0x1F00C000`)、
  dst が linear heap (`0x32xxxxxx`)**
  → **VRAM から表示用バッファへの転送**
- **1 フレームに DisplayTransfer が 3 回**。
  src が `0x1F000000` ×2 と `0x1F00C000` ×1 なので、
  **上画面（左右 2 枚）＋下画面**の構成と整合する（推測）
- `+12 = 0x01A00100` は 3 件とも同じ。`w | (h<<16)` 形式なら
  下位 `0x0100`=256 / 上位 `0x01A0`=416。**画面サイズとの対応は未確定**

### 確度の内訳（CLAUDE.md 準拠）

| 項目 | 確度 |
|---|---|
| type 1 `SetCommandList` | **HIGH**（静的 + 実機で発火を観測） |
| type 2 `MemoryFill` | **HIGH**（同上。宛先が VRAM であることも確認） |
| type 3 `DisplayTransfer` | **HIGH**（同上。VRAM→linear heap を確認） |
| type 0 `RequestDma` | **MEDIUM**（静的のみ。このフレームでは発火せず） |
| type 4 `TextureCopy` | **MEDIUM**（静的のみ。このフレームでは発火せず） |
| 28 バイトストライド | **HIGH** |
| 上下画面の対応 | **LOW**（アドレス帯からの推測） |

### 自前描画への含意

- **フレームは `SetCommandList(0x20)` + `MemoryFill`（クリア）で始まる**
- 本体のコマンドは `SetCommandList` で**数回に分けて**提出される
- **`0x32677600` のような外部の固定コマンドリストも混ぜられる**
  → 自前のコマンド列を別バッファに用意して
  `GX_SetCommandList` で流す手も原理的には可能
- 描画結果は VRAM に出て、最後に `DisplayTransfer` で表示用へ運ばれる

---

