---
id: ACNL-F0185
aliases:
- F-159
title: 'F-159: コードケーブに使える領域は `0x01E82000` で終わる — `HIGH`（実機で読み書き検証）'
summary: '`0x01E82000`-`0x01E821FF` は **128 ワードすべて `0xFFFFFFFF`**、'
date: '2026-08-28'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9510-9536
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-159: コードケーブに使える領域は `0x01E82000` で終わる — `HIGH`（実機で読み書き検証）

`0x01E82000`-`0x01E821FF` は **128 ワードすべて `0xFFFFFFFF`**、
`0xDEADBEEF` を書いても読み戻すと `0xFFFFFFFF` のまま = **未マップ**。

したがってケーブに使えるのは **`0x01E81000`-`0x01E81FFF` の 4KB 1 頁だけ**。

この boot での使用状況（F-155a より、一度実行した番地は同じ boot で再利用しない）:

| 番地 | 用途 |
|---|---|
| `0x01E81500` 付近 | `cave_own_funcnode.py`（CAVE/STUB/HOLDER/COUNTER/TEMPLATE） |
| `0x01E81600` | `cave_textbox.py` MYSTR |
| `0x01E817F0` / `0x01E81800`-`0x01E81BFF` | `cave_textbox.py` のログリングバッファ |
| `0x01E81C00` | F-157 第 1 版（色のみ）— 実行済み |
| `0x01E81D00` | F-159 第 3 版（テーブル駆動）— 実行済み |
| `0x01E81E00` | F-157 第 2 版（トレース付き）— 実行済み |
| `0x01E81E80` | F-158 第 2 版（位置 X）— 実行済み |
| `0x01E81F80` | 観測スロット LOG |

**改版のたびに新しい番地が要るので、1 セッションで作れるケーブの数に上限がある。**
枯れてきたら 3DS を再起動して頁を白紙に戻すこと。
本スクリプトのようにパラメータをテーブル化しておけば、
コードを書き換えずにデータだけ更新でき、番地を消費しない。

---

