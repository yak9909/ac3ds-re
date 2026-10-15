---
id: ACNL-F0585
aliases:
- IDA-gpt-6-sol-F004
title: Pretendoの公表したACNL RCE対策は `0x81` 掲示板パケット（2026-10-04、MEDIUM）
summary: 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。Pretendo Nimbusの[公開ソース](https://github.com/PretendoNetwork/nimbus/blob/fc2d813412a6
date: '2026-10-04'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1590452
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4417-4422
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F004: Pretendoの公表したACNL RCE対策は `0x81` 掲示板パケット（2026-10-04、MEDIUM）

解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。Pretendo Nimbusの[公開ソース](https://github.com/PretendoNetwork/nimbus/blob/fc2d813412a6e0ff652663c32f181891c346ad68/plugin/Sources/patches.cpp) は `acnlPacket0x81Handler` の受信長を `0x1AC` 以下へ制限する。そのフック用8バイトは当該原本の `0x1844B4` に一意に一致し、通常6バイトヘッダの `off_875B4C[0x81]` も同関数を指す。

受信 `sub_1844B4`（IDB名 `NetPkt81_BbsAddPost`）は `0x1AC` バイトのスタック領域を取り、`Mem_CopyBytes3(SP,payload,size)` を長さ検査なしで呼ぶ。掲示板に追加した後、ホストなら同じ `0x81` で他相手に中継する。したがって修正対象は長い掲示板投稿によるスタック範囲外コピーであり、先行F003の**下位転送種別12 (`0x0C`)** の町外コピーとは別経路。Pretendoのパッチは下位 `0x0C` を検査しない。ただし `0x81` での実機RCE成立過程と、下位 `0x0C` の実機配送・悪用可能性は未検証であり、パッチの対象外というだけで安全性/危険性を確定しない。根拠は `work/evidence/network/pretendo_rce_comparison_20261004.md`（Pretendo一次ソース＋IDA assembly＋原本パターン/表ポインタ）。反証条件: 対象ビルドのパターンが別受信関数へ一致する、実際の通信層で `0x81` の長さを必ず `0x1AC` 以下へ制限する、特定の動画が別脆弱性を解説している。利用者の追加指示を受け、今回判明した関数15件・変数/表4件のrename、Enum3件、型2件、関数シグネチャと根拠コメントを主IDBへ保存し、再読込で確認。実機試験なし。

