---
id: ACNL-F0027
aliases:
- F-364
title: 'F-364: ACNLの内蔵キーボード起動候補経路・APT/GSP契約・ABIの検証（2026-09-08）'
summary: '**confidence MEDIUM。** `code.bin.i64`の静的解析、停止中実機の読み取り、原本ARMの局所実行。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 4717536
- 4715504
- 1224976
- 4756820
- 4711568
- 4711724
- 1638400
- 4713344
- 1224720
- 4390976
- 1200500
- 1250696
- 1703936
- 1224840
- 1226472
- 9926672
- 1220208
- 1220256
- 4643576
- 4632684
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:312-348
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-364: ACNLの内蔵キーボード起動候補経路・APT/GSP契約・ABIの検証（2026-09-08）

**confidence MEDIUM。** `code.bin.i64`の静的解析、停止中実機の読み取り、原本ARMの局所実行。
SWKBDの実機起動成功ではない。ビルド・実機書込み・関数呼出し・再開なし。

- 第一候補は既存ゲームAPT管理を利用する方法。`0x0047FBE0` Prepare、`0x0047F3F0` Start、
  `0x0012B110` Wait。Startの4引数はappId/params/size/sharedHandle。
  キーボード用はappId `0x401`、パラメータ`0x400`、別途共有メモリハンドル。
- `0x0012B110`は6引数のAAPCS。第五引数handle outはSP+0、s64 timeoutはSP+8/+12。
  SP+4は整列穴。既存`0x00489554`のARM STRD/受信関数と局所実行で独立照合。
  生APT command `0xA`/`0xB`/`0xC`をSDKの2/3/4へ変換。SwkbdResultとは別。
- Start側にVRAM保存`0x0047E490`→`0x0047E52C`（GSP IPC `0x00190000`）、
  キャプチャ受渡し`0x0047EB80`、GSP解放`0x0012B010(0)`がある。
  Wait側はNotifyToWait `0x00430040`、受信、GSP再取得`0x0012B010(1)`、
  VRAM復元`0x00125174`→`0x00131588`（IPC `0x001A0000`）等を条件付きで実行。
  公式libctru apt/gspgpuソースのIPC語・順序と照合。
- APTセッションは`0x0012B088`でmutex待ち/open、`0x0012B6E8`でclose/ゼロ化/unlock。
  `[0x00977810]=0`だけで未初期化と判断しない。低位IPC直呼びではこの契約が欠ける。
- Startエラーは`0x00129E70`→`0x00129EA0`→`err:f`へ進む。
  単なるResult返却とは扱えない。失敗時の回収・呼出し文脈は未確定。
- 実機read-only: ARM32、imagebase表示0、state=-1、bp=0。
  PC `0x0046DAF8` / SP `0x31F468C0` / LR `0x0046B06C` / PSR `0x60000010`。
  6関数先頭16バイトがIDBと一致。caller appId=`0x300`、role下位3ビット=0、
  mutex非0・現APTセッション0・timeout定数-1/0。mapping APIは空で、新規配置の安全性は未確認。
- **原本ARM IPC18ケース**（成功/サービスエラー/SVCエラー）と既存caller ABIが一致。
  OS/GPU等はモック。起動成功やエラー復旧のテストではない。
- パラメータ構造体32bitレイアウト`0x400`、55 UTF-16単位の共有データ`0x1000`を
  libctruヘッダ/ソースと照合して生成。初期値「かんじ」、予測有効、callback/学習入出力なし。
  いずれも未適用の検証用データ。
- CTRPF原作者ソースのKeepThreadはSWAP時のhook unmap/restore・サウンド解放を行う。
  キーボード起動時に本機でSWAPが発生するかは未観測。参考版Pauseの画面取得/フレーム停止とも
  協調が必要。任意のプラグインスレッドからの同期呼出しを安全と断定しない。

成果物:`DOCS/system_keyboard_launch.md`、`SYSTEM_KEYBOARD/{verify_launch_abi,prepare_launch_fixture,read_launch_state}.py`。
根拠:`SYSTEM_KEYBOARD/evidence/launch*.json`、`verification_launch_abi.json`、`launch_fixture/`。
静的IDBへ8関数命名・4型修正・4コメント、保存済み。一時メモ:`scratchpad/MEMO_20260908_swkbd_launch.md`。

