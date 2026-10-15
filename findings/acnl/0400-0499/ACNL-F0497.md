---
id: ACNL-F0497
aliases:
- IDA-opus-5.5-F034
title: 'ゲームの SVC は 32 種類・745 か所（2026-09-25、HIGH: 命令語＋逆アセンブル、名前は libctru と 3dbrew の 2 資料で一致）'
summary: 再現 `tools/svc/scan_svc.py` → `work/evidence/svc/svc_sites.json`。文書 `docs/topics/svc.md`。
date: '2026-09-25'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1273956
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2168-2174
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F034: ゲームの SVC は 32 種類・745 か所（2026-09-25、HIGH: 命令語＋逆アセンブル、名前は libctru と 3dbrew の 2 資料で一致）

- 再現 `tools/svc/scan_svc.py` → `work/evidence/svc/svc_sites.json`。文書 `docs/topics/svc.md`。
- 多いのは 0x32 SendSyncRequest 392・0x23 CloseHandle 164・0x28 GetSystemTick 81・0x24 WaitSynchronization 43（SDK のインライン展開）。
- `0x137064` は WaitSynchronization（待機中スレッドの PC。ここで止まっているとき bp を付けた直後の continue が失敗した）。
- 応用案（計測・ポインタ検査・スレッド同期・スレッド停止・LINEAR 確保）は未検証。

