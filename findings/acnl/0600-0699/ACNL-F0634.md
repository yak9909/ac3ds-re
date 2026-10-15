---
id: ACNL-F0634
aliases:
- IDA-gpt-6.1-sol-F008
title: 'しばらく使うとフリーズする原因 — 読み込みのヒープの枯渇（2026-10-08、実測 + 静的: MEDIUM）'
summary: '測定: 親（sonnet-5.5、ida-pro-mcp、固まった状態）。静的洗い出しと修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix5）。根拠 **work/evidence/t022_freeze_20261008/README.md**、**work/evidence/t022_catalog_fix5/report.md**。gohan 89a636e。'
date: '2026-10-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 8065336
- 9894976
- 9754184
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:5017-5026
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F008: しばらく使うとフリーズする原因 — 読み込みのヒープの枯渇（2026-10-08、実測 + 静的: MEDIUM）

測定: 親（sonnet-5.5、ida-pro-mcp、固まった状態）。静的洗い出しと修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix5）。根拠 **work/evidence/t022_freeze_20261008/README.md**、**work/evidence/t022_catalog_fix5/report.md**。gohan 89a636e。
- 固まった場所（実測）: ゲームのメイン処理（tid 0xDA）が 0x7B1138（GX キューの旗 byte_AD98D1 が 0 になるまで無期限に待つループ）で止まり、再開しても変わらない。提出済みの最後の描画命令列（0x3229D7C0、0x19930 B）は PICA の書式として最後まで整合し、テクスチャの番地もすべて範囲内（アイコン枠 0x22EC3000〜 を含む）。描画命令の器は余裕あり（s_grid 0x4580 / 0x18000）。
- **読み込みのヒープ（[[0x96FC40]+4]、ExpHeap、全体 3,866,624 B）の空きが 22,420 B**（窓は開いたまま）。窓 1 つで 1.22 MB を使い、窓完成直後の余白が 35 KB、家具を出すごとに数 KB 減る。fix4 の「窓を常駐」で 1.2 MB が返らなくなっていた。
- 結論（MEDIUM）: ヒープの枯渇 → ゲーム側の確保の失敗 → GPU 完了待ちで停止、が筋。どの確保が失敗したかは未特定（LOW）。
- Codex fix5 の修正（静的）: アイコン枠・DARC のコピーの所有権を atomic に、格子アニメの返却、低余白で非表示の窓を返す、枠が尽きたら Spawn 前に拒否、テント項目を家具リストへ統合、診断用の変数。
  訂正（Codex）: Chip の Out 0xB4304C は資源を解放せず、Dtor 0xB4355C まで保持。[0x94D648] は NetGameMgr 本体でなく SingletonDisposer へのポインタ（F007 の周辺訂正と同じ）。
- 次: 窓のヒープ使用を減らす（Codex t022_catalog_fix6）。

