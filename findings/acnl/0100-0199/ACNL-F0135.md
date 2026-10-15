---
id: ACNL-F0135
aliases:
- F-97
title: 'F-97: `GpuCmd_GetProperty` と、自前コマンド追加の定石'
summary: 'confidence: **MEDIUM**（getter の switch を逆コンパイルで直接確認。**静的解析のみ**、F-101 で訂正）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1212124
- 5105652
- 1396812
- 9890456
- 1212620
- 1291940
- 1388544
- 1531904
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5646-5705
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0139"]
---
## F-97: `GpuCmd_GetProperty` と、自前コマンド追加の定石

confidence: **MEDIUM**（getter の switch を逆コンパイルで直接確認。**静的解析のみ**、F-101 で訂正）

### `GpuCmd_GetProperty`(`0x127EDC`)

**当初「コマンド領域の予約 API」と読んだのは誤り。単なる getter だった。**
`switch (id - 512)` で管理オブジェクトの各フィールドを返す。

| id | 返すもの |
|---|---|
| 512 | `mgr[11]` |
| 513 | 現在の mgr かつ `byte_AD98D1` |
| 514 | 現在オフセット（`mgr[3]` も更新） |
| 515 | `mgr[8]` GX キューに積んだ数 |
| 516 / 517 | `mgr[2]` / `mgr[7]` |
| 518 | `mgr[1]` バッファ基底 |
| 519 | `mgr[0]` |
| **520** | **`g_GpuCmdPtr`** |
| 521 / 522 | `mgr[4]` / `mgr[10]` 処理済み数 |
| 523 | `mgr[6]` GX キュー基底 |
| 524 | 現エントリの型（`784 + type`） |
| 525 | 現エントリの addr / size |

### ★ゲーム自身が使っているコマンド追加手順

```c
GpuCmd_GetProperty(520, &ptr);   // ptr = 現在位置
*ptr   = value;
ptr[1] = header;                 // reg | (mask<<16) | ...
...
GpuCmd_Advance(bytes);           // g_GpuCmdPtr += bytes
```

実例: `sub_4DE7F4`(`0x4DE7F4`)、`sub_15504C`(`0x15504C`)。

制約:
- `g_GpuCmdEnd`(`0x96EA98`) を超えない（ゲーム側も毎回検査）
- `GpuCmd_SplitAndSubmit`(`0x1280CC`) が走る**前**に積む
- GPU に見せるメモリは `GSPGPU_FlushDataCache`(`0x13B6A4`) が必要

### ★描画ループの入口はまだ特定できていない

`GpuCmd_SplitAndSubmit` の呼び出し元を辿ると
`sub_16A130`(`0x2224`) → `sub_15504C` → `sub_1534A8` → `sub_4DE7F4` という
単一の鎖になるが、**これが毎フレームの描画とは確認できていない。**

`sub_15504C` は 19 スロットをビットマスクで選び、
`sub_22BD1C(p, n, n, 1,0,0, 10, 0, 0x10000, 0)` で
正方形テクスチャらしきものを作る（n は 64/128/256/512/1024 に丸め）。

**★近所の `sub_14A9C8` が YUV→RGB(F-94) なので、
`0x153000`-`0x176000` は画像コーデック側の疑いがある。**
「GPU コマンドを使っている＝描画ループ」と決めつけないこと。

`nn::gr` の状態フラッシュ側は別系統:
`sub_121E2C`(`0xCA4`) → `sub_11EB68` → `sub_11CE64` → `sub_11C7CC`(`0x4A4`)。

---

