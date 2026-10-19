---
id: ACNL-F0719
aliases: []
title: "既定TagProcessorは起動時の相対初期化表から構築される"
summary: "既定のchar/wide TagProcessorはstartから起動時の相対オフセット表を巡回して初期化される。TextWriterのコンストラクタはwide既定オブジェクトを参照するだけである。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # 静的な生産側と独立した消費側。実機なし
tool: IDA
addresses: [0x00100000, 0x001019D8, 0x0093ECC8, 0x0079B70C, 0x002FE9E4, 0x0097C0B0, 0x0097C0B4, 0x007E8488]
tags: ["font"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x79B70Cを `nwfont_InitDefaultTagProcessors`、0x1019D8を `Runtime_RunStaticInitializers`、相対表の該当語を `kDefaultTagProcessorsInitializerOffset` と命名した。これは通常のTextBox描画時に初めて行う初期化ではなく、実行入口からの起動処理である。確度 MEDIUM：入口命令・相対表原本・走査側、独立したguard/初期化・TextWriter消費が一致。実機なし。

## 根拠

- `_local/builds/acnl_jpn_v15/ida/work/100/primary.txt` のstartは0x100010で0x1019D8をBLXし、その後0x10001Cでアプリケーションの初期設定0x11C7CCへ進む。
- 0x1019D8は[0x93E7CC,0x93EF94)のword列を前から巡回。各語の値をその語自身のアドレスへ足し、BLXする（0x1019E4..EA）。絶対関数ポインタ表ではない。
- 該当語0x93ECC8の原本値は0xFFE5CA44。32bit加算で0x79B70Cとなる。原本と計算は `_local/builds/acnl_jpn_v15/ida/work/100/primary-index.json` と `_local/builds/acnl_jpn_v15/ida/work/100/calculations.json`。
- 0x79B70Cはchar版guard/オブジェクト0x97C0A8/ACの処理に続き、0x79B750..64でwide guard0x97C0B0のbit0とStaticGuardAcquireを検査。0x79B774..80で0x97C0B4へ0x8FCA24を書き込む。
- 0x2FE9E4の実体は `if (*guard) return 0; *guard=1; return 1;`。guardを書き込むのはこの取得処理であり、vptr書込みより前。末尾0x11C124はno-opへ転送するので、guardを後でreleaseする呼出しと解釈しない。
- 0x7E8488のTextWriter ctorは+60へ0x97C0B4そのものを保存し、guard取得/既定vptr保存を行わない。TextBox_RebuildBatchWriter 0x4BAFB0はこのctorを呼び、通常の描画経路で先に初期化を行う別処理を持たない。

## 反証条件・未確認点

- 起動完了後の通常経路の静的な到達順。guardやvptrが外部から書換えられた場合、別の再初期化を保証しない。最初の実TextBox描画時刻/スレッドは未測定。
- acquireの名称は既存を維持したが、命令からは同期ロックや並列安全性は導けない。
