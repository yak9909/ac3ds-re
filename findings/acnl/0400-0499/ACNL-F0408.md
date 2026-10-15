---
id: ACNL-F0408
aliases:
- F-381
title: 'F-381（2026-09-08）: 診断フラグを戻しフルビルドへ。メニュー非表示の説明'
summary: 利用者の指摘の通り、`kDiagNoHooks=true` の間は A1/A2 を入れないため
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 2621493
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:24294-24305
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-381（2026-09-08）: 診断フラグを戻しフルビルドへ。メニュー非表示の説明

利用者の指摘の通り、`kDiagNoHooks=true` の間は A1/A2 を入れないため
自前ノードが再生されずメニューは表示されない。
スレッドは起動したまま（g_visible=1）なので入力遮断は効き、
ボタン不通・タッチのみ操作可になる。Select での開閉も見えないまま動く。

`kDiagNoHooks` を false に戻し、フルビルド（A1/A2＋しずえ＋入力＋
F-375 修正）へ復帰。検証器 0 件。診断目的は達した：
A1/A2 なしでも RenderTop+0x0C で head 不正（`0x280035`）の停止が起きる
＝挿入路では説明できない。残る軸は入力フック・メニュースレッド・
Enable 時確保・素の遷移バグ。素の反復と、有効系の順次復帰で分ける。
