---
id: ACNL-F0026
aliases:
- F-372
title: 'F-372: ACNL既存APTの実行文脈候補と失敗分岐のPC検証（2026-09-08）'
summary: '**MEDIUM、実機アクセスなし。** 利用者が既存APT経路を第一候補に指定し、実機操作を保留。'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2420496
- 6087308
- 6084976
- 6087324
- 6085056
- 3452420
- 11401288
- 3450364
- 1281328
- 1271052
- 5818268
- 5818288
- 9890554
- 1220208
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:286-311
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-372: ACNL既存APTの実行文脈候補と失敗分岐のPC検証（2026-09-08）

**MEDIUM、実機アクセスなし。** 利用者が既存APT経路を第一候補に指定し、実機操作を保留。
`DOCS/system_keyboard_launch.md`末尾に呼出し契約・試験手順と残件。

- idalib/code.bin.i64のxref: `0x0024EF10`→`0x005CE28C`→`0x005CD970`。
  `0x005CE29C`が既存ErrEulaMgr callback実行の呼出し位置で、独立要求の受付位置候補。
  ErrEulaMgrの`+28/+32`はmember-function pointer。`+20/+24`は別経路。
  正確な実行スレッドは未観測。任意のCTRPFスレッドで安全とはしない。
- `0x005CD9C0`は`0x0034AE04(0x00ADF848)`の取得成功時だけアプレット起動。
  取得関数のTLS所有者/再帰カウント、下位`0x0034A5FC`のLDREX/STREXを確認。
  解放は`0x00138D30`→`0x0013650C`。静的assemblyと原本callerの成功/失敗実行を照合。
- `0x0058C79C(0)`は管理オブジェクトのbit `0x4`経路、`0x0058C7B0`はbit `0x8`優先で
  次にbit `0x4`を調べる。既存状態があれば無条件の開始/終了ペアでは保存を保証しない。
- Prepareは最初に遷移byte`0x0096EAFA=4`とし、最終失敗時にも同関数内で戻さない。
  Prepare/Startの3種類の再試行Resultは10ms待ち、回数上限なし。
- StartはVRAM保存/capture関数の負の戻り値をその場で判定せず、起動IPCへ進む。
  callee内部のエラー処理まで無視しているという意味ではない。
  最終Start IPC失敗はfatal入口`0x00129E70`へ。そこで局所実行を止め、正常復帰を仮定しなかった。
- **原本ARM33ケースPASS**: Prepare12、Start8、Wait9、既存caller4。
  `SYSTEM_KEYBOARD/verify_acnl_lifecycle.py`、`evidence/verification_acnl_lifecycle.json`。
  OS/GPU/サービス/ロック等のcalleeはモック。実機起動、実際の排他や復旧の証明ではない。
- 根拠:`evidence/acnl_prepare_static.json`/`acnl_prepare_context.json`。
  AST検査、静的IDBコメント4件保存。ビルド・実機操作・プラグイン組込みなし。
- 残件: スレッド/常駐配置、周辺状態保持、Prepare/Startの失敗回収、異常通知と共有メモリ寿命。

