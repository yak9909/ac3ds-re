---
id: ACNL-F0587
aliases:
- IDA-gpt-6-sol-F006
title: 屋外XYZを下位 `0x0C` で書くための条件と副作用（2026-10-04、静的MEDIUM／実用性LOW）
summary: 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版無印＋更新、原本SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。利用者指定の屋外XYZ `0x33099E50` は2026-09-18のgohan実機記録と、別日のプレイヤー実体 `0x33099E3C` に対する静的 `+0x14` が一致する。前回答の「実体の位置が不明」はこの屋外
date: '2026-10-04'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 9789324
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4427-4434
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F006: 屋外XYZを下位 `0x0C` で書くための条件と副作用（2026-10-04、静的MEDIUM／実用性LOW）

解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版無印＋更新、原本SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。利用者指定の屋外XYZ `0x33099E50` は2026-09-18のgohan実機記録と、別日のプレイヤー実体 `0x33099E3C` に対する静的 `+0x14` が一致する。前回答の「実体の位置が不明」はこの屋外観測では訂正する。ただし相手端末・別boot・屋内での同一番地は未確定。

`Save_GetTownBase` は実行時の `[g_GardenSaveBasePtr 0x955F8C]+0x80` を返すため、相手のこの値がなければ、片内オフセットからXYZ宛先を確定できない。利用者は未測定と回答。さらに町外のXYZ宛先は `NetTransfer12_ReceiveTownChunk` の**コピー後の転送完了分岐も毎回通り**、4人分のセーブ処理、ready flag、通信状態 `+552`/`+78493` を更新する。したがって、範囲外コピーが可能という静的結論だけでは継続的な位置同期チートの実用性を証明できない。受信側で基点・実体・roomを読取り、完了分岐の実機影響と通信配送を小さく検証する必要がある。

根拠・反証条件・IDB注釈は `work/evidence/network/coord_sync_oob_20261004.md`。主IDBに確定したポインタ表・グローバル・関数をrename/型/コメントとして保存。未確定のセーブ後処理3関数は理由を記してコメントのみ。XML交換物を更新し構文/参照/hash検証PASS（44,198関数・32,708シンボル）。実機への送信・書込み・Resumeなし。

