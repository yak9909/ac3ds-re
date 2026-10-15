---
id: ACNL-F0353
aliases:
- F-327
title: 'F-327（2026-09-07）: 要望 R6a（縁も赤に）・R6b（適用時の通知を両方抑制）'
summary: '**confidence: MEDIUM**（検証器 2 種 0 件 + プレビュー + ビルド。'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21562-21591
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-327（2026-09-07）: 要望 R6a（縁も赤に）・R6b（適用時の通知を両方抑制）

**confidence: MEDIUM**（検証器 2 種 0 件 + プレビュー + ビルド。
**実機の目視は未確認**。ケーブ不変）

利用者に確認してもらった結果：Y 入力待ちの取消・無効は正常、
同時開きも問題なし。タッチパネルは対象外のまま（十字キーで完結する設計。
HID タッチの配管が別途要るので、要れば新規タスク）。

### R6a：無効時の赤を縁にも適用

`Notice` に `border` を追加し、`AddNotice(..., red)` で帯と縁を
ともに `kColDanger`（`#e5484d`）にする。通常は帯 `kColAccent`・
縁 `kColPanelEdge` のまま。

### R6b：メニュー適用時（X・全適用・ダイアログ確定）の通知を出さない

利用者と確認のうえ**有効・無効の両方を抑制**した。`ApplyItem()` は
値の反映だけ行う。オンオフとその通知は関数側（ホットキー実行側）が持つ。
語尾定数（`kMsgEnabledSuffix` / `kMsgDisabledSuffix`）は関数側が使うため
残してある。ホットキー発動時の `ACTION` 通知・セーブ実行・リスト選択の
通知はそのまま。

### 実機で確かめること

1. X 適用・全適用で通知が出ないこと（黄色→通常色の変化はする）。
2. 無効適用の通知も出ないこと。
3. 将来の関数側通知で赤の帯・縁が出ること（現状は出す側が無いため
   目視できず。`右下通知をテスト` は緑のまま）。

