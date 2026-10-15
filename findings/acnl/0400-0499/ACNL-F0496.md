---
id: ACNL-F0496
aliases:
- IDA-opus-5.5-F035
title: 'プラグインから GPU 可視メモリを確保できた＝Luma の svcControlMemoryUnsafe で SYSTEM 領域から空き番地へ貼る（2026-09-25、HIGH: 実機 2 回＋Luma の公式ソース）'
summary: '**★採用しない（2026-09-25、利用者の判断）**: 他の CFW・エミュレータで使えず、Old 3DS で通るかも分からないため、自前 GUI は従来のゲームのヒープ借用へ戻した'
date: '2026-09-25'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2297396
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2146-2167
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F035: プラグインから GPU 可視メモリを確保できた＝Luma の svcControlMemoryUnsafe で SYSTEM 領域から空き番地へ貼る（2026-09-25、HIGH: 実機 2 回＋Luma の公式ソース）

- **★採用しない（2026-09-25、利用者の判断）**: 他の CFW・エミュレータで使えず、Old 3DS で通るかも分からないため、自前 GUI は従来のゲームのヒープ借用へ戻した
  （gohan ed1ffb4 = afd4c74 / 28a80da の revert。GUI のコードは 39e7f2d と同一）。知見（Luma の Unsafe の性質・HOME の通知の仕組み）は記録として残す。
  `Sources/Debug/LinearAllocTest.cpp` の試験（旧 CTRPF メニュー）は調査用として残っている。

- 旧 F-163（svcControlMemory の LINEAR は OutOfMemory）を訂正・拡張。試験は gohan `Sources/Debug/LinearAllocTest.cpp`（旧 CTRPF メニュー「GPU可視メモリ(linear/VRAM)を検証」）。
- **svcControlMemory / Luma svcControlMemoryEx(0xA2)** の MEMOP_ALLOC_LINEAR は **APP / SYSTEM / BASE の全領域・全サイズで 0xD86007F3**。
  svcGetSystemInfo(0): APP 使用 0x7C00000（割り当て 0x7200000 を超える）/ SYSTEM 使用 0x1566000（割り当て 0x63F5000、空き約 78MB）/ BASE 使用 0x195A000（割り当て 0x2000000）。
  → 断られる理由は領域の空きではなく**プロセスの資源上限**（推定、MEDIUM）。
- **Luma svcControlMemoryUnsafe(0xA3)**（`k11_extension/source/svc/ControlMemoryUnsafe.c`）は資源上限を見ず `kAlloc(fcram, pages, region)` し、**addr0 へ貼る**（出力 = addr0）。
  addr0 = 0 だと番地 0 に貼ってしまう（1 回目の試験）。PA = kvAddr + 0x40000000。解放（MEMOP_FREE）で物理メモリも返る（使用量で確認）。
- **実機（2 回目）**: svcQueryMemory でたどったメモリ配置の空き区画 `0x10003000`（〜0x11000000 が空き。共有メモリを貼る区画）へ
  Unsafe(ALLOC_LINEAR | REGION_SYSTEM, 0x40000) → 成功、**PA 0x28C32000**（svcConvertVAToPA。libctru の osConvertVirtToPhys は 0）、読み書き OK、
  SYSTEM 使用量 0x1567000 → 0x15A7000 → 解放後 0x1567000（漏れ無し）。
- **利用者の実機確認（gohan afd4c74、自前 GUI のアトラスを自前確保）**: 描画・OFF/ON・場面転換・手紙は全部 PASS（GPU は読めている）。
  **ただし持ったまま HOME へ行くと HOME メニューが落ちた**（menu 0004003000008202、addr 0x00230E34、0xD8C3FBF3 = Application/OutOfResource/OutOfMemory）。
  Unsafe は資源上限の勘定の外で SYSTEM 領域を使うため（推定、HIGH に近い: Luma は HOME のためにプラグインのメモリを SD へ退避する仕組みまで持つ）。
  対処: New 3DS では Luma が HOME_ENTER / HOME_EXIT を送り返事を待つ（plgloader.c）。CTRPF は起動時に notifyHomeEvent を 1 にし（pluginInit.o __entrypoint）、
  KeepThreadMain で「利用者のコールバック → PLGLDR__Reply」の順に呼ぶ。gohan は HOME_ENTER で返し、HOME_EXIT で取り直してアトラスを移す（RelocateAtlas）。
- 未確認: GPU が実際に読めるか（PA は FCRAM なので読めるはず）、長く持ったまま場面を切り替えても安全か、書いた後のキャッシュ（svcFlushProcessDataCache が要る見込み）。

