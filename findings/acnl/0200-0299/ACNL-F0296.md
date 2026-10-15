---
id: ACNL-F0296
aliases: []
title: '`SET_PROJECTION` を廃止した'
summary: 上の 3 番で、**ビューポートは各パスが `RecordChildren` の後・`SetDisplay`（replay）の前に
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 8622080
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16581-16608
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## `SET_PROJECTION` を廃止した

上の 3 番で、**ビューポートは各パスが `RecordChildren` の後・`SetDisplay`（replay）の前に
主リストへ直接出している**ことが確定した。したがって

- そのパスの全 replay に先行してビューポートが入っている
- 我々の投影行列（ノード `+0x34`）は同じ寸法（上 400x240 / 下 320x240）から作ってある

ので、記録の中で `SetDisplaySize` を呼ぶ必要はまったくない。

さらにこれは **`LOG_DISP`（実行時に捕獲した display トークン）に依存していた最後の箇所**
だった。落としたことで、記録の内容は**実行時の観測値に一切依存しなくなった**。

`CAVE_Q` は 400 → 387 語。監査: 総異常 0 件・重なりなし。余り 784 バイト。

### ケーブ配置（F-272 時点。現行）

```
CAVE_Q=0x838200(387) CAVE_P=0x838810(35)  CAVE_V=0x8388A0(44)
CAVE_A1=0x838950(87) CAVE_A2=0x838AB0(82) CAVE_N=0x838C00(11)
CAVE_M=0x838C30(7)   CAVE_B=0x838C50(12)  CAVE_U=0x838C80(12)
CAVE_F=0x838CB0(10)  CAVE_T=0x838CE0(2)    末尾 0x838CF0 / 上限 0x839000（余り 784 バイト）
```

**未適用。実機へは入れていない。**

---

