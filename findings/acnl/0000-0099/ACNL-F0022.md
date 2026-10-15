---
id: ACNL-F0022
aliases:
- F-392
title: 'F-392: しずえスキップの通常フック化（2026-09-09）'
summary: '**MEDIUM。** フリーズ原因と修正後生成物は静的に確定。修正版の実機確認は未実施。'
date: '2026-09-09'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5555236
- 5555240
tags:
- hook
supersedes: []
source: v1:RE/FINDINGS.md:188-208
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-392: しずえスキップの通常フック化（2026-09-09）

**MEDIUM。** フリーズ原因と修正後生成物は静的に確定。修正版の実機確認は未実施。

- 利用者がF-391版で自前メニューをONにすると、メニュー表示時に画面が停止し、音は継続した。
- CTRPF `HookManager.cpp`ではMITM wrapperがcallbackへ直接分岐し、callback側が
  `HookContext::OriginalFunction()`を呼ぶ契約。F-391の`OnFrame`は元関数を呼ばずreturnした。
  したがって`Framework_ProcOneFrame`の残りが毎フレーム実行されないことが停止原因。
- 独立した生成物確認では、`Hook::InitializeForMitm`がflags=8、通常の`Hook`コンストラクタが
  flags=3 (`USE_LR_TO_RETURN | EXECUTE_OI_BEFORE_CB`)を設定する。F-391 `OnFrame`にも
  original呼出は存在しなかった。
- `ShizueSkip::Install`を`g_hook.Initialize(0x0054C424, OnFrame)`へ修正。通常フックは
  素の先頭命令`0xE92D4070`を実行してcallback後に`0x0054C428`へ復帰する。
- ビルド前検証は専用検査、描画/仕様/ケーブ、キーボード10,943遷移/15場面、
  Simulator 49/49、ARM構文がすべてPASS。クリーンビルドと成果物検査もPASS。
- リンク後`ShizueSkip::Install+0x58` (`0x0700B1F0`)は
  `BL 0x0701F554 Hook::Initialize`。`InitializeForMitm`は`0x0701F570`で呼ばれていない。
- 修正版成果物は846,115 bytes、SHA-256
  `cc1d416aebd09a2bb52fc0da22a5f0a6225f0d2f5cad04287b481a1b2a6a1e9c`。
  **実機未確認。F-391成果物は使用禁止。**

