---
id: ACNL-F0384
aliases:
- F-358
title: 'F-358: 3DS内蔵ソフトウェアキーボードのAPIとCTRPFの条件（2026-09-08）'
summary: 詳細・出典・次の確認順は **`DOCS/system_keyboard.md`**。
date: '2026-09-08'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:23227-23245
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-358: 3DS内蔵ソフトウェアキーボードのAPIとCTRPFの条件（2026-09-08）

詳細・出典・次の確認順は **`DOCS/system_keyboard.md`**。

- libctruの公式例と手元ソースを独立に照合。`swkbdInit` / `swkbdInputText` が文字/テンキーを扱い、
  `aptLaunchLibraryApplet(APPID_SOFTWARE_KEYBOARD = 0x401)` で内蔵アプレットを起動する。
  日本語本体で漢字入力には `SWKBD_PREDICTIVE_INPUT` が必要。出力はUTF-8。
- libctruのAPTは専用受信スレッドと状態を持ち、起動時に画面/GSP権限を受け渡す。
  CTRPF原作者の初期化ソースに `aptInit` はなく、ローカルのライブラリにもその参照はない。
  **通常homebrewの例をそのまま使えるとは未確認**。ゲームのAPTとの接続・復帰検証が必要。
- `code.bin.i64` / idalibで `sub_21C24C` の `UiScreen_OpenById(0x23E)` と、
  `sub_57D444` の `Layout/Swkbd/*.arc` 選択・呼び出しを逆コンパイル/命令で照合。
  BsSkbはゲームの画面管理を使う経路。OSアプレット利用の証拠として混同しない。
  全内部経路でOSアプレットを使わないことまで証明してはいない。
- **confidence: MEDIUM**（複数の静的証拠。プラグインからの内蔵キーボード起動は動的未確認）。
- 進捗確認で `verify_plugin_port_v2.py` 8群・異常0件、キーボード `--preflight` 成功。
  HANDOFFの容量を現行ソース・検証器で照合し訂正（文字上69/下76、Picture上74/下336・計410）。
- 今回はビルド・実機書き込み・再開なし。調査メモと取得ソース/SHA-256をscratchpadへ保存。

