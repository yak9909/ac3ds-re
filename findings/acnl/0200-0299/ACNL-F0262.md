---
id: ACNL-F0262
aliases:
- F-241
title: 'F-241: lifecycle trace の block-copy emitter は loader Layout を破損する — `HIGH`（生成命令＋実機レジスタ＋破損メモリ）'
summary: '`probe_loader_submit_lifecycle.py` の F-240 emitter は安全ではなかった。`LOG=0x009B3000` 自体は'
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10170368
- 9946984
- 5664304
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:14068-14092
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-241: lifecycle trace の block-copy emitter は loader Layout を破損する — `HIGH`（生成命令＋実機レジスタ＋破損メモリ）

`probe_loader_submit_lifecycle.py` の F-240 emitter は安全ではなかった。`LOG=0x009B3000` 自体は
`code.bin.i64` の segment survey で `.bss` (`0x97C768..0xAF2694`, RW) にあるため、`.text` への
書込みが原因ではない。

共通 emitter の raw ARM 命令は `LDMIA R2,{R0-R3}` の直後に
`STMIA R1!,{R0-R3}` を置いていた。replay stage の第2 word は Layout pointer であるから、LDM 後の
`R1` は本来の ring 宛先ではなく `0x3225A2B4` になった。さらに base register `R1` 自身も STM の
register list に含まれる。実機 SIGSEGV 時の `PC=0x838E60`、`R1=0x3225A2C4`、`R2=0x1A` は、
第一 STM が Layout 宛てに 16 byte 書いたあと、`ADD R2,#0x10` が loader id `0x0A` を `0x1A` にした
値と整合する。停止中に読むと Layout 先頭は実際に
`[0x3225A2B4..+0x0C] = {1, 0x3225A2C4, 0x0A, 0}` だった。

したがって再生 Layout の vptr を含む先頭が失われ、後続の stock
`LayoutList_SetDisplay(0x566E30)` でも不正 Layout pointer を介した SIGSEGV が起きた。unknown な
旧 `+4/+8/+C` を推測で直すことはしない。hook を stock に戻し、PC を cave epilogue に移す試行後も
heap 破損は残ったため、再起動が唯一安全な復旧である。

uninstall script の内部 verify と独立 read-back の両方で hook stock、cave zero、LOG zero を確認した。
この script の install path は再適用禁止とする。次回は block-copy を使わず、source と destination を
異なる register に固定した 1 word `STR` trace から再設計する。

---

