---
id: ACNL-F0582
aliases:
- IDA-gpt-6-sol-F001
title: 通信パケット種別番号 `0x00`～`0x84` の受信表（2026-10-03、MEDIUM/一部LOW）
summary: 対象は日本語版更新 `artifacts/update/exefs/code.bin`（SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`）。解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。`Net_DispatchPackets 0x627718` は6バイトヘッダの種別を `0x85` と比較し、`off_875B4C[種別]` から受信ハンドラを
date: '2026-10-03'
category: network
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6453016
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4381-4388
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-sol-F001: 通信パケット種別番号 `0x00`～`0x84` の受信表（2026-10-03、MEDIUM/一部LOW）

対象は日本語版更新 `artifacts/update/exefs/code.bin`（SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`）。解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。`Net_DispatchPackets 0x627718` は6バイトヘッダの種別を `0x85` と比較し、`off_875B4C[種別]` から受信ハンドラを選ぶ。原本バイナリとIDBの全133ポインタ、比較命令を照合PASS。`0x00` と `0x5F` は空処理、ほかは受信処理を持つ。ただし送信呼出しが見つからない番号もあり、「有効な送信に使われる」とは限らない。

送信側の種別定数は90番号で確認。`0x33`～`0x36` は定数ではなく `byte_87BE48[player & 3]` から選ばれ、原本4バイトと受信側の `PlayerState_ApplyRemotePacket` が対応する。`0x3A` はフィールド操作22バイト、`0x4A`/`0x4B` はゲスト手紙と結果、`0x81`/`0x82` は掲示板投稿と削除。`0x41` はさらにサブ種別0～36を内包するため、種別番号だけで行動を一意に決められない。全133行の受信動作・ハンドラ・確度は [docs/topics/network_packets.md](../docs/topics/network_packets.md)。

根拠: `work/evidence/network/packet_handlers_ida.json`（IDA受信側）、`packet_senders_ida.json`（定数指定送信側）、`packet_table_verify.json`（原本生バイナリの独立照合）、`tools/patches/verify_packet_catalog.py`。ゲーム内の用途を断定できない行はLOWと明示。旧 `reference/old_project/RE/FINDINGS.md` F-55 の `0x47` 送信起点は現行版で再発見できず未解決。反証条件は別ビルドで異なる受信表、送信時に未追跡の型選択、実機トレースでの別用途。実機への適用・Resumeは行っていない。

