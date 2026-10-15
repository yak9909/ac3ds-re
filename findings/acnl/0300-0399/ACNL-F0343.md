---
id: ACNL-F0343
aliases:
- F-315@v1:RE/FINDINGS.md:20997
title: 'F-315 追記: 1 度目のクラッシュについて（原因は未確定）'
summary: 同じ構成（借用 `0x50000` + `LIST_SIZE 0x10000`）が **2 回目は問題なく動いた**。
date: '2026-09-06'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 10161408
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:20997-21018
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-315 追記: 1 度目のクラッシュについて（原因は未確定）

同じ構成（借用 `0x50000` + `LIST_SIZE 0x10000`）が **2 回目は問題なく動いた**。
1 度目との違いは **`CAVE_N` から `SVC 0x54`（`svcFlushProcessDataCache`）を外したこと**だけ。

1 度目は吐き出し先を `.bss (0x009B0D00, 0x100)` に向けていた。
利用者が報告した `LR = 0xFFF0BA00`（カーネル領域）は SVC 内での例外と整合するが、
**再現していないので断定しない。**

★教訓として確かなこと:
- **アトラスが無いのに毎フレーム SVC を撃つ理由が無かった。**
  必要のない副作用を持つケーブを「とりあえず元のまま」入れない。
- **1 度に 3 つ（`LIST_SIZE`・借用量・フックの追加）を変えた**ので切り分けられなかった。
  2 回目は 1 つずつ入れて、各段で読み出して確認した。

★**利用者の指摘のとおり、1 度目は idalib での逆アセンブル検証を飛ばしていた。**
  ただし後から検証したところ、**適用した命令列は以前に実機で動いた版と 1 語も違わず**、
  差分はリテラル 3 語だけだった（`0x8000→0x10000` x2、`0x20000→0x50000`）。
  つまり**この手順を踏んでいても捕まえられなかった**。手順違反であることは変わらない。

---

