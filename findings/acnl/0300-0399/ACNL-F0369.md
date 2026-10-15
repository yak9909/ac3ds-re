---
id: ACNL-F0369
aliases:
- F-343
title: 'F-343（2026-09-07）: 空いた容量で通知を Simulator と同じ 7 件にした'
summary: '**confidence: HIGH**（検証器 8 群が異常 0 件 / ビルド成功。★実機での目視はこれから）'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:22209-22261
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-343（2026-09-07）: 空いた容量で通知を Simulator と同じ 7 件にした

**confidence: HIGH**（検証器 8 群が異常 0 件 / ビルド成功。★実機での目視はこれから）
前提: F-342 第 1 段（器を詰めて 207,296 B 空けた）
退避: `BACKUP/plugin_full_20260907_f342/`（F-342 段階・実機で動作確認済み）

### 決めたこと（利用者の判断）

| 項目 | 決定 |
|---|---|
| 空いた容量の使い道 | **通知を 2 -> 7 件**。借用 `kBorrowBytes` は 0x6C000 のまま（ゲームへは返さない） |
| 記録リストの上限 | **上画面 `LIST_SIZE` 0x20000 -> 0x28000**（nngx から +32,768 B。空きは 1,220,172 B） |

### 通知 1 件の実費（ソースから数えた）

`DrawNotices` は 1 件につき `Frame1px`（矩形 5 枚）+ 縁の帯 1 枚 + 文字 2 本。

```
矩形 6 枚 + 文字スロット 2 本（題 <=24 字 / 本文 <=16 字）= 領域 10,144 B / 記録 4,470 B
```

### 変更

| ファイル | 変更 |
|---|---|
| `Sources/GuiMenu.cpp` | `kNoticeMax` 2 -> **7** |
| `Sources/GuiV2.cpp` | `kTopSlotCaps` に 16 字 x5 と 24 字 x5 を追加（上 63 -> **73 本**） |
| `Sources/GuiV2.cpp` | ★**矩形の枠を画面ごとに分けた**。`kMaxRectTop` 86 / `kMaxRectBot` 56 / `kMaxRectAll` 142。`RectsOf(screen)` を新設し `FillRect` / `MaxRects` / 不可視化の範囲 / `picBase` が使う |
| `PATCHES/export_gui_v2.py` | `kGuiListSizeTop` 0x20000 -> **0x28000**（`GuiCavesV2.h` は再生成） |
| `PATCHES/verify_plugin_port_v2.py` | 群 4 に上下の枠の検査、群 6 を画面ごとの枠へ |

### ★踏んだ落とし穴

`kMaxRect` を 56 -> 86 にしたら**下画面**の検査が落ちた。
通知は上画面にしか出ないのに、枠が上下共通だったので
**下画面の記録の最悪値が 29,184 B となり `LIST_SIZE 0x8000` の 80%（26,214 B）を超えた**。
→ 枠を画面ごとに分けて解決（下は 56 のまま）。Picture も 30 枚ぶん節約できた。

### 結果

| | 前（F-342） | 後（F-343） |
|---|---|---|
| 文字スロット | 上 63 / 下 11 | **上 73** / 下 11 |
| 矩形の枠 | 上下とも 56 | **上 86** / 下 56 |
| 配置 | 231,552 B（借用の 52.3%） | **271,616 B（61%）** |
| 上画面の記録（最悪） | 84,848 B / 0x20000 の 64.7% | **103,728 B / 0x28000 の 79%** |
| 下画面の記録（最悪） | 23,064 B / 0x8000 の 87% | 変わらず 23,064 B（87%） |
| 通知 | 2 件 | **7 件（Simulator と同じ）** |

`python PATCHES/verify_plugin_port_v2.py` -> 総異常 0 件。`make` -> `gohan.3gx` 更新。

---

