---
id: ACNL-F0637
aliases:
- IDA-gpt-6.1-sol-F011
title: 家具のチップと窓が読み込みヒープを共有する問題 — 基準の見直しと、アイコン枠を描画命令用ヒープへ（2026-10-09、実測 + 静的 MEDIUM、実機未確認）
summary: '測定: 親（sonnet-5.5、通知が出た後の停止状態）。調査・修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix8、枠切れで一度停止して再開）。根拠 **work/evidence/t022_heap_20261009/README2.md**、**work/evidence/t022_catalog_fix8/report.md**。gohan 6ca7158。'
date: '2026-10-09'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5673460
- 9894972
- 9894976
- 1170040
- 6383136
- 9457572
- 9436920
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:5049-5060
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F011: 家具のチップと窓が読み込みヒープを共有する問題 — 基準の見直しと、アイコン枠を描画命令用ヒープへ（2026-10-09、実測 + 静的 MEDIUM、実機未確認）

測定: 親（sonnet-5.5、通知が出た後の停止状態）。調査・修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix8、枠切れで一度停止して再開）。根拠 **work/evidence/t022_heap_20261009/README2.md**、**work/evidence/t022_catalog_fix8/report.md**。gohan 6ca7158。
- 実測: 総空き 985,996 B、窓の消費 593,120 B、窓完成後 392,876 B が基準 393,216 B（384 KiB）に 340 B 不足。チップ（Chip_Setup）が 1 個 5,616 B を永続消費（約 48 個で 270 KB）。リークではなくゲームの仕様。
- 共有の確認（Codex、MEDIUM）: ゲーム自身の Editor_CreateChips 0xB3CC08 も追加のチップも同じ Chip_Setup 0xB43160 → Chip_BuildLayoutAndAnimations 0xB420C4 を通る。0x5691F4 が同じ 2D_UI_Heap を [0x96FC3C]+4 と [0x96FC40]+4 へ設定。命令の器 1,280 B は別ヒープ（graphic::MemoryMgr の a1[5]）。読み込みヒープ側の内訳は合成実行で 5,404 B（実測 5,616 B との差 212 B は未解決）。
  ゲーム上限（チップ 112）まで出したときの窓を開いた状態の空きは約 164〜174 KB（移設なし）、アイコン移設ありで約 262〜272 KB（試算）。
- 修正: (1) 読み込みヒープの基準を総空き / 連続とも 128 KiB へ（F010 の 384 / 128 KiB から）。(2) **利用者の判断（2026-10-09）で採用**: アイコン枠 98,304 B を graphic::MemoryMgr の a1[5]（FCRAM の ExpHeap、全体 7,008,256 B、空き約 714 KB、GPU の命令の器の割り当て先。0x11DA78 / 0x616620）から末尾側で確保。確保前に総空き 256 KiB + 窓の命令予定分 + 確保費用、連続 128 KiB を要求、確保後と窓の構築後にも検査、不足なら読み込みヒープへフォールバックまたは窓を開かない。ヒープの種類（vtable 0x904FA4 / 0x8FFEF8）を照合してから触る。
  診断: s_graphicHeap* の前後記録と毎秒リングに a1[5] の空きを追加。通知は「品を出して不足 / 描画の空き不足」とチップの数・残り / 必要。
- 親の懸念: a1[5] は GPU 描画命令の器で、不足すると描画が止まる危険（F008 の GX 待ちの原因候補）。利用者は「フリーズしたら利用者から修正を依頼」と判断して採用。反証条件: a1[5] の空きが 256 KiB を保った状態でも描画が止まる、または窓を開いた状態の家具追加が止まる。
- IDB: 主 IDB に命名 4・部分型・コメント、ModuleIndoor にコメント 6（ID は親が F011 に置換: 主 12+4、Indoor 6）。
- 追記（2026-10-09 実機 decor_catalog12）: 全項目 PASS（家具 70 個以上でも窓が開く、描画は止まらない）。

