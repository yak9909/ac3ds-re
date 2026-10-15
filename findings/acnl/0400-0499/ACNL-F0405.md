---
id: ACNL-F0405
aliases:
- F-378
title: 'F-378（2026-09-08）: 実行構成がどのビルドとも一致しない'
summary: 実機値（チートON・メニューOPEN・タイトル待機・正常待機PC）：
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24251-24265
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-378（2026-09-08）: 実行構成がどのビルドとも一致しない

実機値（チートON・メニューOPEN・タイトル待機・正常待機PC）：
A1/A2 素 / shizueフック入り / 入力フック入り / g_visible=1。

- gate ビルドなら A1/A2 も入るはず。diag ビルドなら sh も入らないはず。
  どちらとも一致しない。`RemoveHooks()` の唯一の呼び出し元は
  `Disable()` で、そこを通れば sh・入力も外れる。説明がつかない。
- `InstallHooks()` が失敗すれば `Enable()` が失敗しメニューは起動しないが、
  メニューは起動している（g_visible=1）。よって A1/A2 は入ってから
  誰かに外されたことになる。心当たり： セッション共有中の他エージェントの
  書き込み（00BE6Bxx 混線の実績あり）、利用者の手動操作、SD 差し替えの齟齬。
- この状態でのクラッシュ判定はできない（構成自体が壊れている）。
  正手順： SD の 3gx を特定→再起動→全語の素を確認→ON→全語を確認→試験。

