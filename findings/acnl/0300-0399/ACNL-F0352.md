---
id: ACNL-F0352
aliases:
- F-326
title: 'F-326（2026-09-07）: 実機報告の不具合1件と要望 R1〜R5'
summary: '**confidence: MEDIUM**（検証器 2 種 0 件 + プレビュー + ビルド。'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21499-21561
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-326（2026-09-07）: 実機報告の不具合1件と要望 R1〜R5

**confidence: MEDIUM**（検証器 2 種 0 件 + プレビュー + ビルド。
**実機の目視は未確認**。ケーブ不変）

利用者の実機報告（段 6/段 7 の確認）への対応。

### 不具合：ACTION 項目のホットキーが適用待ちにならない

`IsDirtyItem()` が ACTION を一律に除外していたため、UI テストの
上/下画面リストにホットキーを設定しても X が何もせず、
適用（`appliedHotkey` へ反映）できなかった。ホットキー発動側
（`FireHotkeyItem` → `RunAction`）は出来ていたので、設定だけ届かない形。

直し：フォルダ以外は値・ホットキーどちらの差分でも適用待ちにする。
ACTION は値を持たないのでホットキー差分だけ効く。行の黄色表示・
下帯の件数・閉じる確認ダイアログも自動で追従する。

### 要望 R1：下画面リストの dim にフェードイン・アウト

dim（`kColDim`）が即時表示だった。リスト自身の `OverlayAmount` で
αを掛けるようにした（1 行変更）。

### 要望 R2：トグル式はホットキーで切り替えない

チェックのホットキー発動は値の切り替えをやめ、有効中（`applied != 0`）の
押下だけ `ACTION` + 項目名の通知を出す（状態は変えない）。
無効中の押下は何もしない。将来チート固有の実行関数を配線する場所として
`FireHotkeyItem()` に注記した。現状は値がゲームへ届く仕組み自体が無い
（メニューは UI 状態の段階）ので通知のみ。

### 要望 R3：通知回数の表示を廃止

`DrawNotices()` で題に `id` を付けなくなった（`CHEAT ENABLED 3` をやめる）。
`Notice.id` の欄は残してある。

### 要望 R4：無効時のアクセントを赤に

`Notice.accent` を追加し、`AddNotice(..., red)` で決める。
無効適用だけ `kColDanger`（`#e5484d`）。プレビュー側（`app.js` の
`drawNotice`）も題が `CHEAT DISABLED` で始まるとき赤になるよう足した。

### 要望 R5：通知の形式（題:項目名 / 本文:項目名+語尾）

適用時は題＝項目名、本文＝項目名＋語尾（`kMsgEnabledSuffix` /
`kMsgDisabledSuffix`）。語尾を変えたければこの 2 定数だけ直す。
`verify_plugin_port_v2.py` の群 5 に例外を 1 件追加した
（`を無効にしました` は Simulator に無いデバイス先行文）。

### タッチパネルについて

未実装ではなく**対象外**。メニューは十字キー操作で完結する設計で、
入力待ちの無効・取消も X/B ボタンでできる（A/全離しで決定）。
タッチを読むには HID タッチの配管が別途要る。要れば新規タスクにする。

### 実機で確かめること

1. UI テストの上/下画面リストにホットキーを設定→黄色→X 適用→
   閉じて押すとリストが開くこと。
2. 下画面リストの dim がフェードすること。
3. チェックのホットキーで値が変わらず、有効中のみ通知が出ること。
4. 通知の題・本文・赤アクセント（無効時）。回数表示が無いこと。

