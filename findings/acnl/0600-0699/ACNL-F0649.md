---
id: ACNL-F0649
aliases:
- Ghidra-gpt-sol-5.6-F011
- G-F011
title: type 0x10 completion token案は実機クラッシュで棄却
summary: '**確度: HIGH（crash_dump_00000008＋静的再監査）。**'
date: '2026-09-19'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 5891620
- 10150236
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:261-289
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F011: type 0x10 completion token案は実機クラッシュで棄却

**確度: HIGH（crash_dump_00000008＋静的再監査）。**

Ghidra-gpt-sol-5.6-F011はcustom成功後に `Item_PlaceItem(type=0x10,...)` を呼び、status=2の正規FieldAction handleを返す設計だった。

実機ではdrop瞬間にdata abort:
- PC=`0x59E624`
- FAR=`0x11`
- r4=`0`
- r5=`0x31F50688`

`0x59E624` は `Item_PlaceItem` 内の `LDRB r1,[r4,#0x11]`。正常なslot allocationならr4は `0x9AE15C` 内、r5は0..3であるため、この実行状態は破綻している。

さらに静的再監査でfallback/call stubが:

```
LDR r12,=Item_PlaceItem
BLX r12
BX  lr
```

となっており、BLXでhook callerのLRを上書きするためreturn path自体が不正だったことも判明した。

従ってGhidra-gpt-sol-5.6-F011実装は全面的に廃止する。

根拠: `work/evidence/balloon_drop_ar_20260915.md`。


