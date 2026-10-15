---
id: ACNL-F0645
aliases:
- Ghidra-gpt-sol-5.6-F007
- G-F007
title: balloon ARの旧code caveが既存描画caveと衝突していた
summary: '**確度: HIGH（添付Ghidra XMLの既存allocation map＋crash_dump_00000007＋ユーザー実機挙動）。**'
date: '2026-09-19'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 8618004
- 8622080
- 3131512
- 5891596
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:100-131
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F007: balloon ARの旧code caveが既存描画caveと衝突していた

**確度: HIGH（添付Ghidra XMLの既存allocation map＋crash_dump_00000007＋ユーザー実機挙動）。**

添付 `acnl_jpn_v15.xml` の `0x00838014` コメントには、zero-fill gap `0x838018-0x839000` 内の既存割当が記録されている:

- `0x838080-0x838137`: dead cave
- `0x838140-0x8381D7`: 描画発行cave
- `0x838400-0x838423`: textbox cave
- `0x838500-`: replacement strings

旧balloon ARは `0x838018-0x8381AB` を使用し、特に `0x838140-0x8381AB` が既存描画発行caveと重複していた。AR enable時点でE patch codeがこの領域を上書きするため、ユーザーがdrop操作をしなくても既存cave実行時に異常制御フローへ入る。

crash_dump_00000007:
- PC=`0x2FC878`
- LR=`0x59E60C`
- FAR=`0x3A`
- `Item_PlaceItem` saved LR=`0x838128`
- entry r1=`0x3A`

`0x2FC878` は4-byte Item copyの `ldrh r2,[r1]` であり、直接faultは無効Item pointer。dropしていないのに旧cave内 `0x838128` から `Item_PlaceItem` が呼ばれていることは、enable時cave衝突と整合する。

修正版は既存allocationの空白 `0x8381D8-0x8383FF` を再検証し、その内部の `0x838200-0x838393` に移設した。この範囲について:
- main .text ARM B/BL参照 0件
- initialized .text/.rodata/.data 内の4-byte直接ポインタ 0件
- 既存allocation map上の割当 0件

**重要:** 旧コードを有効化したプロセスでは既存描画caveが破壊済み。OFFコードでは元内容を復元できないため、新版試験前にゲームを完全再起動する。

根拠: `docs/balloon_drop_action_replay.md`、`work/evidence/balloon_drop_ar_20260915.md`。


