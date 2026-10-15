---
id: ACNL-F0355
aliases:
- F-328
title: 'F-328（2026-09-07）: 関数側連携の窓口（トグル実行は利用者が持つ）'
summary: '**confidence: MEDIUM**（検証器 2 種 0 件 + ビルド。**実機の目視は未確認**。'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21624-21651
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-328（2026-09-07）: 関数側連携の窓口（トグル実行は利用者が持つ）

**confidence: MEDIUM**（検証器 2 種 0 件 + ビルド。**実機の目視は未確認**。
ケーブ不変。振る舞いの既定値は不変）

利用者の方針：トグル式の有効無効切替＋通知は関数側で実装する。
メニューは現状維持で、必要な窓口だけ用意することになった。

### 用意した窓口（`Includes/GuiMenu.hpp`）

- `SetHotkeyHandler(handler)` — 登録するとチェック項目の発動時に
  内蔵の `ACTION` 通知の代わりに `handler(項目番号)` を呼ぶ。
  handler はメニュースレッドから呼ばれる（短く・止めないこと）。
  未登録なら従来通り（有効中のみ `ACTION` 通知）。
- 状態の読み書き：`ItemCount` / `ItemLabel` / `ItemValue` /
  `ItemApplied` / `SetItemApplied`（値と適用値をまとめて反映・通知なし）/
  `ItemHotkey` / `ItemAppliedHotkey` / `FormatItemHotkey`。
  項目番号は `BuildTree` から変わらない。単語単位の読み書き。
- `Notify` / `NotifyRed`（赤）— 別スレッドから呼べる。
  `GuiNotification::NotifyRed` からも呼べる。
- ホットキーマスク bit の公開 enum `HotkeyBit`
  （`HB_ZL`〜`HB_START`。表示順＝Simulator の `HOTKEY_BUTTON_ORDER`）。
  内部 enum との二重定義をやめ、公開側へ一本化した。

### 実機で確かめること

既定値（ハンドラ未登録）の振る舞いが F-327 から変わらないこと。

