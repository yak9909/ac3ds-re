---
id: ACNL-F0412
aliases:
- F-387
title: 'F-387: SWKBD実機の表示候補キャッシュ位置と読取器（2026-09-09）'
summary: '**confidence: MEDIUM（SWKBD原本の静的解析2経路＋オフラインfixture。実機値は未取得）。**'
date: '2026-09-09'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1800064
- 1061324
- 1087852
- 1122260
- 1420080
- 1123024
- 1147344
- 1144764
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:24372-24392
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-387: SWKBD実機の表示候補キャッシュ位置と読取器（2026-09-09）

**confidence: MEDIUM（SWKBD原本の静的解析2経路＋オフラインfixture。実機値は未取得）。**
SWKBDの`[0x001B7780]`がアプリオブジェクトを指す。入力変更経路
`0x1031CC`→`0x10996C`→`0x111FD4`と、表示キャッシュ構築経路
`0x15AB30`→`0x1122D0`→`0x1181D0`→`0x1177BC`を突き合わせた。

- 変換対象長/文字列: `app+0x6958C` / `app+0x69590`（UTF-16LE、112 bytes）
- 変換入力: `app+0x69600`（UTF-16LE、112 bytes）
- 表示候補: `app+0x69670`から112 bytes×最大12件
- 全候補数/選択index/表示件数: `app+0x69BB0/+0x69BB4/+0x69BB8`
- 候補cacheのindex順: `(selected+i)%total`

`read_live_candidates.py`はSWKBDプロセスを候補表示中にSuspendした状態からだけ読む。
原本SHA-256、関数6領域、件数上限、NUL終端、UTF-16、入力長を検証する。対象への書込み、
Resume、breakpoint操作はない。オフライン検証器は元ARM 8語、12候補fixture、index折返し、
異常系5件を検査してPASSした。

画面用cacheなので実機の表示順取得には適するが、画面外の候補と文節境界を含むとは扱わない。
一次記録:`SYSTEM_KEYBOARD/evidence/verification_live_candidate_reader.json`。

