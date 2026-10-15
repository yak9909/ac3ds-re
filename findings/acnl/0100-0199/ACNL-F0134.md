---
id: ACNL-F0134
aliases:
- F-96
title: 'F-96: コマンドリストの終端・提出経路と GX API 一式'
summary: 'confidence: **MEDIUM**（型値と引数位置を直接確認。**静的解析のみ**、F-101 で訂正）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1212620
- 1239000
- 1273612
- 9890456
- 1268044
- 1268096
- 1268064
- 1268128
- 1291940
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5580-5645
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-96: コマンドリストの終端・提出経路と GX API 一式

confidence: **MEDIUM**（型値と引数位置を直接確認。**静的解析のみ**、F-101 で訂正）

### 全体の流れ

```
描画コード → g_GpuCmdPtr に (値,ヘッダ) を積む
  → GpuCmd_SplitAndSubmit(0x1280CC)  終端を付けて GX キューへ type=1
  → GxQueue_Dispatch(0x12E7D8)       28B エントリを型で振り分け
  → GX_SetCommandList(0x136F0C)      0x20B の GX コマンドを GSP 共有メモリへ
  → sub_13B5AC                       GSP へ送信
```

### `GpuCmd_SplitAndSubmit`(`0x1280CC`)

末尾に必ず積む 4 コマンド:

| 値 | ヘッダ | reg |
|---|---|---|
| 0 | `0x0008025E` | `0x25E` PRIMITIVE_CONFIG |
| 1 | `0x000F0111` | `0x111` FRAMEBUFFER_FLUSH |
| 1 | `0x000F0110` | `0x110` EARLYDEPTH_CLEAR |
| **`0x12345678`** | `0x000F0010` | `0x010` **終端マーカー** |

`0x12345678` → reg `0x010` は 3DS 標準のコマンドリスト終端。

その後 GX キューへ:
```c
entry = mgr[6] + 28 * mgr[8];
entry[0] = 1;                    // SetCommandList
entry[4] = mgr[1] + mgr[5];      // アドレス
entry[8] = mgr[3] - mgr[5];      // サイズ
mgr[5] = mgr[3];  ++mgr[8];
```

各書き込みは `g_GpuCmdPtr < g_GpuCmdEnd`(`0x96EA98`) の境界検査つき。

### ★GX API 一式（`GxQueue_Dispatch` の switch）

| type | addr | 名前 |
|---|---|---|
| 0 | `0x13594C` | `GX_RequestDma` |
| 1 | `0x136F0C` | `GX_SetCommandList` |
| 2 | `0x135980` | `GX_SetMemoryFill` |
| 3 | `0x135960` | `GX_SetDisplayTransfer` |
| 4 | `0x1359A0` | `GX_SetTextureCopy` |

**3DS の GX コマンド列挙そのもの。** テクスチャ転送・バッファクリア・
フレームバッファ変換は全部ここを通る。

`GX_SetCommandList(addr, size, flushFlag, flags)` はスタック上に 0x20B の
GX コマンド構造体を組み、先頭バイトに **5(SetCommandListFirst) / 1(SetCommandList)**
を入れて `sub_1372B8` → `sub_13B5AC` で GSP へ。

### 描画に使うときの足がかり

- **自前コマンドを割り込ませる**なら `GpuCmd_SplitAndSubmit` より前に
  `g_GpuCmdPtr` へ積む（`g_GpuCmdEnd` を超えないこと）
- **テクスチャを送る**なら `GX_SetTextureCopy`、
  **クリア**なら `GX_SetMemoryFill`、
  **画面転送**なら `GX_SetDisplayTransfer`
- GPU に渡すメモリは事前に `GSPGPU_FlushDataCache`(`0x13B6A4`, F-94) が必要

---

