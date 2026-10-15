---
id: ACNL-F0360
aliases:
- F-334
title: 'F-334（2026-09-07）: 効果の実体を関数登録に直す'
summary: 利用者の指摘：`RegisterToggleEffect` という名前にアドレスや有効値を
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21752-21774
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-334（2026-09-07）: 効果の実体を関数登録に直す

利用者の指摘：`RegisterToggleEffect` という名前にアドレスや有効値を
持たせるのはおかしい。関数の方で制御すべき。
あわせて、既定値は必ず明示値にし、初回書込値の自動保持は
全てにおいて絶対にしないこと（禁止）。

### 変えたところ（F-333 のデータ登録を置き換え）

- `RegisterToggleEffect(int index, const ToggleEffectFuncs *funcs)` —
  `{IsActive, SetActive}` の振る舞いを登録する。両方必須。
  写しを取る。解除は `UnregisterToggleEffect`。
- 発火（閉鎖中・有効中の押下）で `IsActive()` → 反転 `SetActive(!active)`
  → 通知（題はチート名。無効側は赤）。読取検証・再同期の筋は同じ。
- 既定値の自動保持は構造的に入らない。外す値は常に関数側の明示値
  （`SetActive` 内で書くもの）であり、メニューは読んだ値を既定値として
  保存しない。コードにも禁止を注記した。
- `SetActive` 内の書換には `FlushMemory()` を呼ぶこと（公開のまま）。
- `ToggleEffectActive()` は `IsActive()` に委譲（未登録は false）。

検証器 2 種 0 件、ビルド済み。ケーブ不変。
**実機の目視は未確認**（登録する関数側が無いため発火経路は未実行）。

