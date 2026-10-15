---
id: ACNL-F0361
aliases:
- F-335
title: 'F-335（2026-09-07）: 複数パッチ切替と押し続け移動の再設計'
summary: 利用者の壁抜け（複数アドレス×複数値）・座標移動（ホットキー＋押下方向へ
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21775-21805
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-335（2026-09-07）: 複数パッチ切替と押し続け移動の再設計

利用者の壁抜け（複数アドレス×複数値）・座標移動（ホットキー＋押下方向へ
連続移動）・移動方式切替（リスト：十字キー/Cパッド/スライドパッド）の
仕様を受け、振る舞い 2 種に分解して再設計した。

### 分解

- **縁切り替え型**（壁抜け）：押下の立ち上がりで反転する。効果記述は
  関数側の表＋2 関数（`IsActive`/`SetActive`）で持ち、メニューは
  発火条件（有効＋閉鎖中）・読取検証の調停・通知だけやる。
- **押し続け型**（座標移動）：`OnTick` の `held` マスクで判定し、
  毎フレーム少量ずつ動かす。方式切替のリスト値は `ItemValue()` で読む。

### 入れたもの（`Includes/GuiMenu.hpp`）

- `TogglePatch`（番地・大きさ・有効値・既定値）＋
  `PatchListIsActive`（全一致で真）／`PatchListSetActive`
  （書換＋`FlushMemory`）。壁抜けは表＋2 行の関数で足りる。
  不正要素は判定＝偽・書込＝飛ばし。既定値の自動保持は無い（禁止のまま）。
- `IsVisible()` — 下画面パッド等を直接読む効果用。開いている間は
  動かさないこと（`held` は開閉中 0 だが直接読みは素通しのため）。
- 用法スケッチ（ヘッダ注記）：3 方式の読み方まで書いた。
  十字キー＝`held` の方向 bit／Cパッド＝`hidKeysHeld()` の
  `KEY_CSTICK_*`（libctru に実在を確認。アナログ読みは無い）／
  スライドパッド＝`hidCircleRead()`（実在を確認。遊びを切る）。
  直接読み方式だけ `IsVisible()` で閉塞する。

検証器 2 種 0 件、ビルド済み。ケーブ不変。
**実機の目視は未確認**（関数側の登録が無いため新経路は未実行）。

