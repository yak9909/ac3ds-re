---
id: ACNL-F0077
aliases:
- F-39
title: F-39 【危険】レコード枯渇で範囲外書き込み → SIGSEGV — `HIGH`
summary: セッション4 で**実際にクラッシュした**（`got SIGSEGV signal, exc.code b`）。
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10150468
- 10150446
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1803-1823
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-39 【危険】レコード枯渇で範囲外書き込み → SIGSEGV — `HIGH`

セッション4 で**実際にクラッシュした**（`got SIGSEGV signal, exc.code b`）。

`FieldObj_ApplyDigRecord` の空きスロット検索には満杯チェックが無い（F-25 で指摘済み）:

```c
v12 = 0;
while (byte_9AE255[22 * v12]) { if (++v12 >= 32) { v12 = -1; break; } }
v13 = 22 * v12 + 0x9AE244;      // v12 == -1 → 0x9AE22E へ範囲外書き込み
```

衝突フックから毎回 `FieldObj_ApplyDigRecord` を呼ぶ設計にしたところ、
レコードが消化されずに 32 件を超えて落ちた。

**教訓**: レコードを登録する改造では、**必ず消化・解放されることを実機で確認する**。
`0x9AE244` の使用中件数を定期的にダンプすれば早期に気づける。
兆候として「切り株の当たり判定が消える」等の異常が先に出ていた。

---

