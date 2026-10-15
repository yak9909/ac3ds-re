---
id: ACNL-F0246
aliases:
- F-221
title: 'F-221: ★★ゲームのアロケータから取れるのは 0x4000 まで — `HIGH`（実機）'
summary: グリフアトラスを 256x128 LA4（32KB）にしようとして `Alloc(0x8000, 0x80)` を試したが
date: '2026-09-01'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:13254-13272
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0319"]
---
## F-221: ★★ゲームのアロケータから取れるのは 0x4000 まで — `HIGH`（実機）

グリフアトラスを 256x128 LA4（32KB）にしようとして `Alloc(0x8000, 0x80)` を試したが
**0 が返る**（4 秒走らせても同じ）。`Alloc(0x4000, 0x80)` は成功する。

```
g_GfxAllocator = 329A4820   heap = 329A4778
heap +0x20 = 0x39800（総量らしき値）
```

したがってグリフアトラスは **128x128 LA4 = 16KB = 8x8 セルが 256 個**で組む。
256 字あれば ASCII 95 字 + かな約 100 字 + 漢字数十字は入る。

足りなくなったら **テクスチャの基点もチャンクごとに .bss から読む**ようにして、
0x4000 のページを複数枚使えばよい（未実装）。


---

