---
id: ACNL-F0237
aliases:
- F-212
title: 'F-212: ★★★★★マテリアルには名前と定数色が入っている — `HIGH`（実機）'
summary: 自前スプライトが「たまに別の色を拾う」症状の正体。
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12790-12822
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-212: ★★★★★マテリアルには名前と定数色が入っている — `HIGH`（実機）

自前スプライトが「たまに別の色を拾う」症状の正体。

| オフセット | 内容 |
|---|---|
| `+0x10` | 定数色（中立なら `0`） |
| `+0x14` 〜 `+0x2C` | 定数色（中立なら `0xFFFFFFFF`） |
| `+0x38` 〜 | **ASCII の名前**（`P_base_00` など） |
| `+0x4D` | `Material_EmitState` が最初に読むバイト |

実機で採取した 4 例:

| アドレス | 名前 | `+0x10` | `+0x14` | 判定 |
|---|---|---|---|---|
| `0x32C96428` | `P_base_00` | `0` | `FFFFFFFF` | 中立 |
| `0x32EE500C` | `P_list_arrow_00` | `0` | `FFFFFFFF` | 中立 |
| `0x32D83158` | `P_crsl_00` | `00FFFFFF` | **`FF6077FF`** | ★色付き（カーソル） |
| `0x32D1E0C8` | `W_msg_00` | `0` | **`007D4040`** | ★色付き（メッセージ枠） |

拾っていた色は**カーソルの色**だった。
`+0x10 == 0 && +0x14 == 0xFFFFFFFF && +0x18 == 0xFFFFFFFF` を条件に加えて解決。

**★名前が読めるので、マテリアルは今後アドレスではなく名前で語れる。**
デバッグ時は `+0x38` から 24 バイトを読むこと。

実機での確認（ユーザー報告）:

> 常に真っ白で、常に最前面です。


---

