---
id: ACNL-F0002
aliases: []
title: 2026-09-12 普通チャットの入力所有者・日本語フォント・候補表示
summary: 通常gohanへ候補列挙を追加。BsMenuChatの所有者照合、ゲーム日本語フォント154シート対応、stock Batch容量、threadJoinの正のtimeoutの扱いを[トピック](../project_v2/docs/topics/chat_kanji.md)へ集約。根拠 `project_v2/work/evidence/chat_kanji/`。字形/幅は全65536コードポイントで元ARMと一致。リンク済み変換候補17/6/143/3/1件が原本と一致し、
date: '2026-09-12'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags:
- chat
- font
supersedes: []
source: v1:RE/FINDINGS.md:7-10
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## 2026-09-12 普通チャットの入力所有者・日本語フォント・候補表示

通常gohanへ候補列挙を追加。BsMenuChatの所有者照合、ゲーム日本語フォント154シート対応、stock Batch容量、threadJoinの正のtimeoutの扱いを[トピック](../project_v2/docs/topics/chat_kanji.md)へ集約。根拠 `project_v2/work/evidence/chat_kanji/`。字形/幅は全65536コードポイントで元ARMと一致。リンク済み変換候補17/6/143/3/1件が原本と一致し、frontend24ケースPASS。実機での統合表示は未確認（MEDIUM、エミュレーションをHIGHへ昇格させない）。

