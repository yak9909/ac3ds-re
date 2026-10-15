---
id: ACNL-F0117
aliases:
- F-79
title: 'F-79: 実画面生成成功の同期点は `Menu_PollOpen -> UiScreen_OpenById` の戻り'
summary: 'confidence: **HIGH**（`Menu_PollOpen` disassemblyと実機pending残留を照合）、'
date: '2026-08-24'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7147688
- 7147860
- 5409888
- 7168824
- 7168096
- 7170744
- 6037356
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:4970-4997
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-79: 実画面生成成功の同期点は `Menu_PollOpen -> UiScreen_OpenById` の戻り

confidence: **HIGH**（`Menu_PollOpen` disassemblyと実機pending残留を照合）、
**LOW**（constructor戻り版の実機結果は確認待ち）

`Menu_PollOpen` (`0x6D10A8`) はmenuId `0x7C`をscreenIdへ変換し、`0x6D1154` で
`UiScreen_OpenById` (`0x528C60`) を呼ぶ。戻り値が非0なら画面生成成功で、0ならopen state 3を
1へ戻す。lower-menu updateが停止する前に必ず通り、かつ要求のキュー成功ではなく実体生成成功を
直接判定できる同期点である。

`PATCHES/cave_catalog_inventory_tabs_out.py` を再改訂した。`0x6D6338` ではpendingと同時に
その場のR4 lower-menu managerをprivate storageへ保存する。`0x6D1154` のcall-compatible wrapperは
stock `UiScreen_OpenById` を先に呼び、戻り値非0・pending=1・保存manager非nullのときだけ
`State_Change(manager+20, sub_6D6A98, 0)` を行う。stock戻り値は保存してそのままcallerへ返す。
退場完了hookはpendingと保存managerを両方消し、従来どおり終了待機へ接続する。

前版後のstock復旧を確認し、constructor戻り版を設置した。`0x6D6060` はstockのまま、
`0x6D6338` / `0x6D1154` / `0x6D6AB8` の3 hook、cave全域、pending=0、保存manager=0を
読戻した。breakpoint 0件を確認してContinue済み。画面結果は確認待ち。

実装は `PATCHES/cave_catalog_inventory_state16.py`。hookは両版とも
`0x5C1F6C: EB025D3A -> EB62FD63 (BL 0x01E81500)`。第2版caveは20バイトで、
`PUSH {R4,LR}; MOV R0,#0; BL vc_CFUNCTION; MOV R0,#0; POP {R4,PC}`。
PC相対命令を移設せず、stackを8バイト整列のまま公式関数を呼ぶ。install前に実機と
`code.bin.i64` のanchor、breakpoint 0件、cave全ゼロを照合し、設置後もhook/caveを読戻した。

---

