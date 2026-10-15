---
id: ACNL-F0070
aliases:
- F-32
title: F-32 CTRPF の空ページ `0x01E81000` は実行可能 — `HIGH`
summary: CTRPluginFramework が起動時に確保する空メモリページ。
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1582-1610
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-32 CTRPF の空ページ `0x01E81000` は実行可能 — `HIGH`

CTRPluginFramework が起動時に確保する空メモリページ。

```
0x01E80000 = NOP NOP NOP NOP / LDR PC,[PC,#-4] / 0x0700DD7C / NOP NOP
0x01E81000 - 0x01E81FFF = 全部ゼロ (4096B = 1024 命令)
0x01E82000 以降 = 0xFF (未マップ)
```

`0x01E80000` に CTRPF が置いたトランポリン（`LDR PC,[PC,#-4]` + ジャンプ先）が
**実際に動いている**ため、同じマッピング内のこのページも実行可能と判断し、
土しぶきケーブ（19 命令）を置いて**実機で動作を確認した**。

**意義**: `.text` 内の死にコードを探す制約から解放される。1024 命令は破格。

**注意**:
- CTRPF が後からフックを追加すると使われる恐れがある
- **`.code` の一部ではないので `code.ips` には含められない**。
  恒久化するなら `.text` 内へ移す必要がある
- ゲーム再起動で消えるのは他のメモリパッチと同じ

**比較**: `0x08001000` 付近のゼロ領域は**使ってはいけない**。
`0x08000000` に "HPXE" シグネチャと自己参照ポインタがあり、
動的メモリアロケータの管理領域だった。割り当てられれば上書きされ、
ヒープなので実行権限も無い公算が高い。

---

