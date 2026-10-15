---
id: ACNL-F0375
aliases:
- F-349
title: 'F-349（2026-09-07）: Simulatorの文字・数値キーボードをCTRPFへ移植'
summary: '**confidence: MEDIUM（ソース照合とホスト試験。実機未確認）**。'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:22606-22648
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-349（2026-09-07）: Simulatorの文字・数値キーボードをCTRPFへ移植

**confidence: MEDIUM（ソース照合とホスト試験。実機未確認）**。
詳細・再現・実機確認項目: **`DOCS/keyboard.md`**。

今回の利用者指示で、F-321時点のキーボード保留を解除した。
`GuiKeyboard.hpp/cpp`に固定容量の入力状態と描画を実装し、`GuiMenu`へ接続。
配列は元Simulatorの`textKeyLayout()`を実行して`GuiKeyboardLayout.h`へ生成する。

### 移植範囲

- 通常/小型のかな・カナ・QWERTY。カーソル位置への挿入/削除、8文字上限、濁点/半濁点/小字、Caps/Shift、確定/取消、フェード。
- DEC/HEX/小数、符号、削除、上下限。メニューのfloatは1/10単位の整数へ戻す。
- タッチの水準から立ち上がりを作り、押しっぱなしで二重入力しない。十字キー/A/Bも使える。
- 通常の数値確定は編集値だけ更新。ホットキー経由は確定時に適用値も更新。取消はどちらも変えない。
- 名前変更はSimulatorと同じUIサンプル。ゲームのプレイヤー名への書き込みは実装していない。

### 容量・描画

F-347の単純な2枚重ねでは、不透明な縁が半透明の内地の背景になる。
F-323と同じ**重ならない5矩形**の枠を採用。角丸は既存GUIと同じ矩形枠。
`oIdx`と矩形/文字の代入キャストを**u16**へ。`oKind`は0/1なのでu8を維持。

下Picture336・文字76スロット、plugin置き場0x70000（配置401,664 B）、
下LIST_SIZE0x2D000。**アトラス借用0x9000と通知5件は維持**。
全枠を使った記録の保守見積もり124,224 Bは安全弁147,456 B以内。

### 独立した検証と成果物

1. **C++対元Simulator: 10,943入力遷移で状態と確定結果が全一致**。
2. **実C++の描画呼出を捕獲**した15場面で、字形欠け/画面外/文字枠不足/予算超過0。
   PNGはプラグインの実アトラスから描画し目視も確認。
3. 既存移植8群/仕様v3/費用式23点/生成配列、Simulator48テスト、タッチと過大入力保護、
   実3DSヘッダーのARM構文検査をすべて通した後にビルド。
4. `gohan.elf`の再リンク、キーボード処理のシンボル、3gxの更新とSHA-256を確認。

`PATCHES/build_keyboard_plugin.py`が検証成功とソースSHA一致を条件にmakeを呼ぶ。
最初はMSYS2の`/tmp`権限で失敗したため、workspace内の一時フォルダと`make -j1`へ変更して成功。
**実機へは未適用。** ログ/PNG/JSON/SHAは` scratchpad/keyboard_port_qa/`。
実機確認済みの戻り先は引き続き`BACKUP/plugin_full_20260907_f346/`。

---

