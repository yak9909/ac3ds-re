---
id: ACNL-F0362
aliases:
- F-336
title: 'F-336（2026-09-07）: 試験2項目へ効果配線（通知確認用）'
summary: 利用者の要望：テスト用の無敵モード・壁抜けに通知を入れること。
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21806-21841
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-336（2026-09-07）: 試験2項目へ効果配線（通知確認用）

利用者の要望：テスト用の無敵モード・壁抜けに通知を入れること。

### 実装（`WireTestEffects()`）

- `Initialize()` の `BuildTree()` 直後に、label 検索で両項目の番号を
  引き、`ToggleEffectFuncs`（試験変数の反転だけ）を登録する。
- **ゲームメモリには触らない**。通知経路の確認と実チートの雛形用。
  実チートはこの形を写す（`IsActive`＝読取判定、`SetActive`＝書込。
  メモリ型は `PatchListIsActive`/`PatchListSetActive`）。
- 不要になれば `WireTestEffects()` ごと消す。

### 試験手順

1. 無敵モード（または壁抜け）に Y でホットキーを設定→X で適用。
2. A で ON→X で適用（有効化）。
3. メニューを完全に閉じる（閉じる確認が出たら適用を選ぶ）。
4. ホットキー押下→有効通知（題・本文＝項目名）。再押下→無効通知（赤）。
   どれかが出なければ F-335 前回答の 5 条件（登録・束縛適用・有効・
   完全閉鎖・完全一致）を上から当たる。

検証器 2 種 0 件、ビルド済み。ケーブ不変。

---

---

> ★**改番（2026-09-07）**: ここから 4 件は当初 F-327〜F-330 と名乗っていたが、
> 別エージェントがプラグイン側で同じ番号（F-323〜F-336）を先に使っていたため、
> **F-337〜F-340 へ振り直した**。対応は F-327→F-337 / F-328→F-338 /
> F-329→F-339 / F-330→F-340。古い番号で書かれた記述を見たら文脈で判別すること
> （共有バッチ・TextWriter・記録量の話ならこちら、メニューの見た目・通知・
> トグルの話ならプラグイン側）。`scratchpad/MEMO_f326_textwriter_migration.md` は
> FINDINGS 番号を持たない（移行の検討メモ）。

