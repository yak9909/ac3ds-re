---
id: ACNL-F0020
aliases:
- F-394
title: 'F-394: callback境界のレジスタ保存でF-393を修正'
summary: '**HIGH（利用者が自前メニュー復帰・しずえスキップ成功を実機確認）。**'
date: '2026-09-10'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:160-177
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-394: callback境界のレジスタ保存でF-393を修正

**HIGH（利用者が自前メニュー復帰・しずえスキップ成功を実機確認）。**
報告: 「復帰しました。しずえスキップも問題なく動作しました。」
全操作・日付またぎ・反復試験を網羅したという意味ではない。
通常Hookから直接C++へ入る構成を変更し、
ShizueSkipCallback.sがr0-r12/lr、CPSRフラグ、FPSCR、d0-d15を保存・復元する。
192 bytesを追加使用し、C++呼出時の8-byte整列を保持。元PUSHのスタックも検証した。
実機採取CTRPF wrapperと旧F-392 ELFのPC実行でOFF時R0=0を再現できた。
新ASMの破壊耐性試験と、リンク済みTickのOFF/対象外/待機/準備不足/発火/準備済みを
同じwrapperから実行し、一般レジスタ・浮動小数点・フラグ・SP/LR・復帰先を照合してPASS。
外部APIはモックであり、実機の画面遷移やセーブ処理の検証ではない。
Installのcallbackリテラルは0x0700B7F0、そこからBL 0x0700AFF8 ShizueSkipTick。
専用事前試験、ARM構文、統合、描画移植/仕様検査をPASS後クリーンビルドした。
成果物846,070 bytes、SHA-256
`157c3159aff40fa54168ed53faa11dfe09941f424d16f1d0e5a1c79a01d77095`。
再現スクリプトPATCHES/verify_shizue_hook_registers.py、結果scratchpad/shizue_hook_qa/。

