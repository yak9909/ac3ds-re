---
id: ACNL-F0359
aliases:
- F-331
title: 'F-331（2026-09-07）: トグル実行のライフサイクル連携'
summary: 利用者の設計：ホットキーで ON/OFF を切り替えるとトグル式の有効無効も
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21729-21751
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-331（2026-09-07）: トグル実行のライフサイクル連携

利用者の設計：ホットキーで ON/OFF を切り替えるとトグル式の有効無効も
切り替わる。有効中は関数を常に実行し、ホットキーの ON/OFF 挙動は関数内で
作る。必要なチートだけ有効にすることで他の暴発を防ぐ。トグル式の構成は
「有効時に一回」「有効時に常に」「無効時に一回」の 3 関数。

### 用意した窓口（`Includes/GuiMenu.hpp` の `ToggleHandlers`）

- `OnEnable(int index)` — 無効→有効に変わったフレームに 1 回。
- `OnTick(int index, u16 heldMask)` — 有効な間は毎フレーム（約16ms）。
  `heldMask` は `HotkeyBit` マスクの水準。ON/OFF 挙動はここに書く。
- `OnDisable(int index)` — 有効→無効に変わったフレームに 1 回。
- `SetToggleHandlers()` で登録（写しを取る。`nullptr` で解除）。
  いずれもメニュースレッドから呼ばれる。短く・止めないこと。
- 駆動は `Update()` で、有効状態（`applied`）の遷移を見る。
  メニューの開閉によらず、チート ON 中は常に回る。
  起動時点で有効な項目では `OnEnable` を誤発しない（現状態で初期化）。
- `Notify` / `NotifyRed` は tick 内からも呼べる（連発に注意）。

使い方の例は `GuiMenu.hpp` の注記を参照。検証器 2 種 0 件、ビルド済み。
ケーブ不変。**実機の目視は未確認**（既定動作は不変のため影響は限定的）。

