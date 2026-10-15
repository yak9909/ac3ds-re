---
id: ACNL-F0584
aliases:
- IDA-gpt-6-sol-F003
title: 下位種別12の受信に町サイズ上限がない（2026-10-04、MEDIUM）
summary: '解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。通常送信 `sub_61FE5C` は町全量 `0x71880` Bで止まるが、非ホスト受信 `sub_187030` は先頭4Bオフセットが `>=0x10EA` なら '
date: '2026-10-04'
category: network
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4411-4416
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F003: 下位種別12の受信に町サイズ上限がない（2026-10-04、MEDIUM）

解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。通常送信 `sub_61FE5C` は町全量 `0x71880` Bで止まるが、非ホスト受信 `sub_187030` は先頭4Bオフセットが `>=0x10EA` なら `Save_GetTownBase()+(offset-0x10EA)` を計算し、**町境界を検査せず** `Mem_CopyBytes3` でコピーする。町末尾との比較はコピー後の完了判定である。したがって通常送信関数とは別に細工した下位種別12が届く場合、相手の書込み可能な仮想メモリを町外まで上書きする余地がある。対象端末のTownBase値、配送とメモリ権限の確認が必要で、実機成功は未確認。

これは相手のROM/ExeFSファイルを変更する処理ではない。比較用IDA loaderは `.text` をREAD|EXECとしており、通常の `memcpy` が読取り専用のコードページへ書けるとは言えない。現在bootの実機マップは未測定。また、種別12の受信経路は `Field_RebuildAttributes` / `Building_RebuildOccupancy` を呼ばないため、範囲外書込みが成立してもそれだけで再構築関数は起動しない。実行時の属性/占有データを正確に直接置き換える別案は理論上あり得るが未設計。IDA assemblyと原本命令/SHA、loader権限と `Mem_CopyBytes3` のストアを独立照合。根拠・反証条件は `work/evidence/network/town_transfer_oob_20261004.md`。実機通信・書込み・Resume、DB変更なし。

