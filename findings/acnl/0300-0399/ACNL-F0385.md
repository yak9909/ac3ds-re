---
id: ACNL-F0385
aliases:
- F-359
title: 'F-359: 内蔵漢字変換候補取得の目的・共有辞書候補・ゲーム内APT起動経路（2026-09-08）'
summary: 調査目的は3DS本体内蔵のかな→漢字変換辞書・変換候補の取得。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: LOW
tool: IDA
addresses:
- 4718892
- 1572928
- 4718440
- 1966212
- 9926672
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23246-23290
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-359: 内蔵漢字変換候補取得の目的・共有辞書候補・ゲーム内APT起動経路（2026-09-08）

### 目的の訂正（利用者の明示）

調査目的は3DS本体内蔵のかな→漢字変換辞書・変換候補の取得。
自前メニューへ組み込む目的は一切なく、gohan.3gxの設計に依存させない。
依頼されていない用途を推測で前提にしない指示をAGENTS.md/CLAUDE.mdにも記録した。
利用者の知り合いには、とび森で内蔵キーボードを安全に呼んだ実績がある。具体的経路は不明。

### 公開APIと候補一覧の区別

libctru `swkbd.h` と `swkbd.c` の共有メモリコピー方向・コールバック経路を照合。
`swkbdInputText`は入力文字列の返却、`swkbdSetFilterCallback`は送信文字列の検査。
`swkbdSetDictionary`は呼出し元→キーボードの追加辞書指定であって内蔵辞書の取得ではない。
学習データの入出力も内蔵辞書本体・確定前の全候補一覧と同一視しない。
公開APIに候補一覧取得は見つからないが、内部の候補配列/辞書から取得できないとは結論しない。

### 辞書資源の候補（LOW、実体未確認）

3dbrewタイトル一覧のJPN列:
- 内蔵キーボード本体: `0x000400300000C002` (`swkbd`)
- 日本語共有辞書: `0x0004009B00011902` (`JA_small/32`)

出典: https://www.3dbrew.org/w/index.php?title=Title_list
上位/下位IDの結合はPythonで計算。実機版情報・内容・読み込み元はまだ照合していない。
作業フォルダ内の名前/拡張子検索では両タイトルのダンプは見つからず、保存先を利用者に問い合わせ中。

### とび森のAPT経路（MEDIUM、静的）

- `0x0048012C` = `APT_PrepareToStartLibraryApplet_Ipc`。IPCヘッダー`0x00180040`。
- `0x0047FF68` = `APT_StartLibraryApplet_Ipc`。IPCヘッダー`0x001E0084`。
  R0=appId/R1=buffer/R2=size/R3=shared handle。逆コンパイラの`__int64`を信用せずARM命令で照合。
- APTハンドル`[0x00977810]`は、サービス名`APT:A`/`APT:U`を選択する`sub_120610`の取得先。
- `sub_47FBE0`→Prepare、`sub_47F3F0`→Start。
  共通caller `sub_489554`はID **`0x406`（エラー表示）**、サイズ`0xF80`を渡し、`sub_12B110`で受信/待機する。
- 独立照合: 本作のARM命令による全IPC語配置とlibctru `apt.c`の同コマンド実装が一致。
  同じヘッダー値を使う別サービス候補`sub_468604`をAPTと混同しなかった。
- 低位2関数を命名、5箇所へ根拠コメントを付けて`code.bin.i64`を保存した。
- **ライブラリアプレット起動経路は存在するが、内蔵キーボード`0x401`での安全な起動・復帰は未確認。**
  エラー表示のIDだけを変更する方法は採用しない。適合する構造体・共有メモリ・呼出し文脈を調べる。

詳細は `DOCS/system_keyboard.md`。ビルド・実機書き込み・再開は行っていない。

---

