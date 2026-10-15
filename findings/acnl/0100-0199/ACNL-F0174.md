---
id: ACNL-F0174
aliases:
- F-136
title: 'F-136: atlas flush wrapper の同一視を撤回 — `MEDIUM`（呼び出し規約）/ `LOW`（command 名）'
summary: 再監査で、従来 `0x143718` を `GSPGPU_FlushDataCache`、`0xFFFF8001` を「flush command」と
date: '2026-08-24'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1324824
- 1330244
- 2031746
- 1330300
- 1291940
- 1291996
- 1320648
- 9097752
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:8977-9002
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-136: atlas flush wrapper の同一視を撤回 — `MEDIUM`（呼び出し規約）/ `LOW`（command 名）

再監査で、従来 `0x143718` を `GSPGPU_FlushDataCache`、`0xFFFF8001` を「flush command」と
記述していた点は過剰だったと判明した。独立に命令列と定数を確認すると:

- `0x143718` は `dword_8AD218`（値 `0xFFFF8001`）を読み、`sub_1372C8()` が返す
  `&dword_9778CC`、raw address、size を `0x144C44` へ渡す。
- `0x144C44` は TLS IPC buffer の header `0x001F0082`（`0x144C7C`）を設定し、
  `v5[4]=a2`、`v5[1]=addr`、`v5[2]=size` の後に `SVC 0x32` を実行する。
- 既知の `0x13B6A4` は同じ SVC 形式だが header `0x00080082`（`0x13B6DC`）であり、
  `0xFFFF8001` はその process handle 引数として `sub_136ED8` から渡される。

従って `0xFFFF8001` は command ID ではなく process handle 値である。また `0x143718`
の `0x001F` request が flush / invalidate / その他の range cache operation のどれかは、
この静的コードだけでは確定できない。atlas 初期化 (`0x1426C8`) が raw sheet 範囲を
渡す事実は残るが、関数名は `nwgfx_GspGpu_RangeCacheOp_1F` として確度を下げ、既知の
`GSPGPU_FlushDataCache` API (`0x13B6A4`) との同一視をしない。

**根拠**: `0x143718`/`0x144C44` と `0x13B6A4` の full assembly、`int_convert` による
`2031746 → 0x1F0082`、`524418 → 0x00080082`、`dword_8AD218` の IDB 値
`0xFFFF8001`、および atlas/非 atlas 両経路の caller xref。なお `0x143718` (0x2C bytes)、
`0x144C44` (0x38 bytes)、`0x144C7C`、`0x8AD218` も `code_runtime.elf.i64` と byte-for-byte
一致しており、これは command の**存在とビルド対応**を裏付けるが、command 名までは確定しない。

---

