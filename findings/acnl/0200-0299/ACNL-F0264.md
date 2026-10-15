---
id: ACNL-F0264
aliases:
- F-236
title: 'F-236: Layout record-list のバッファ本体は安全に差し替える必要がある — `MEDIUM`（静的＋ゼロ長実機経路）'
summary: 外部会話ログ `REFERENCES/TEXTS/render.txt` は「描画コマンド追加・順番変更・コマンド
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5664416
- 5670612
- 8062612
- 5669596
- 1185468
- 5670768
- 3128204
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:14134-14181
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-236: Layout record-list のバッファ本体は安全に差し替える必要がある — `MEDIUM`（静的＋ゼロ長実機経路）

外部会話ログ `REFERENCES/TEXTS/render.txt` は「描画コマンド追加・順番変更・コマンド
バッファ拡張」の三要素を挙げている。ただし二次資料なので仕様として採用せず、ACNL 自身の
`code.bin.i64` と停止中実機で照合した。

### 静的な二経路の根拠

- RTTI の `ssys::ma::lyt::LayoutList` vtable にある `0x566EA0` は、`list+4` から
  各 node の `+8` を辿り、node vtable `+0x14` を呼ぶ。この slot は Layout 側の
  `Layout_RecordPaneTree(0x5686D4)` であり、LayoutList の「子 Layout を記録する
  ループ」と分かる。役割名を `ssys_ma_lyt_LayoutList_RecordChildren` として IDB へ反映した。
- `Layout_RecordPaneTree` は `Layout+0x100` の list を選び、Pane tree を記録してから
  `GpuCmd_CommitListAndCaptureDelta(0x7B0694)` を呼ぶ。一方
  `Layout_ReplayRecordedList(0x5682DC)` が記録範囲を後から再生する。外部ログの
  record/replay 構造と一致するが、ここで得た結論はゲーム内 assembly が根拠である。

`GpuCmd_SelectList(0x1216BC)` は未知 id に対して 0x44-byte の manager header を作るだけで、
`manager+4`（buffer base）と `manager+8`（capacity）を割り当てない。したがって
capacity 値だけを増やすのは buffer 外書込みを招く。さらに、記録途中の `0x568770` では
`manager+0x0C` がまだ Commit 前の古い offset である。コピーすべき長さは
**`g_GpuCmdPtr - manager->base`** である。

### 実機の限定プローブ

新規 `PATCHES/probe_layout_record_buffer_extend.py` は、現在の title 上画面 Layout id `0x10`
だけを対象に、`0x568770`（`nwlyt_DrawPaneTreeToCurrentList` の直後、DrawEnd/Commit 前）で
以下を行う。描画コマンドと submit は追加しない。

1. live cursor から書込み済み byte 数を検査・算出する。
2. `g_GfxAllocator` の `Alloc(size, align)` で 0x4000 bytes / align 0x80 を確保する。
3. ゲームの `Mem_Copy(0x2FBB8C)` で既存の記録済み bytes だけをコピーする。
4. manager base/size と `g_GpuCmdPtr/g_GpuCmdEnd` を同一ケーブ内で整合する値へ更新する。

適用前に branch、literal、67-word cave、BSS、breakpoint 0 件、対象 manager の
`base/capacity/offset` を機械監査する。最初の監査では semantic NOP を `MOV R0,R0` と
取り違えず、静的 bytes と実機 read-back の双方で `0x568770=0xE320F000` を確定し、復元値を
修正した。

1200 ms の予約付き走行で hook は一度通り、id 0x10 manager は
`base 0x327B4A70 -> 0x329D8500`、`capacity 0x1000 -> 0x4000` へ置換された。
この標本は `used=0` / committed offset 0 だったため、**allocator/repoint のゼロ長経路だけ**が
確認済みである。非ゼロ `Mem_Copy`、replay 後の見た目、他画面の最終 Layout、全メニュー量は
未確認であり HIGH に上げない。hook/cave/LOG は直後に撤去済みで、置換済み buffer は
in-flight GX request を危険にさらさないため reboot まで保持する。

---

