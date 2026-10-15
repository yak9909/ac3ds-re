---
id: ACNL-F0302
aliases: []
title: リテラル参照の値まで検証する道具を追加した
summary: '`PATCHES/verify_literals.py`。`audit_node_cave.py` は'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 10161664
- 9942860
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:17043-17088
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## リテラル参照の値まで検証する道具を追加した

`PATCHES/verify_literals.py`。`audit_node_cave.py` は
「参照先がリテラル領域に入っているか」しか見ないが、こちらは
`Asm` のラベル表と突き合わせて **その LDR が本当に意図した定数を読んでいるか**を出す。

```
CAVE_Q  389 語  リテラル 27 本   リテラル検査 OK
CAVE_P  35 語 / CAVE_A1 87 語 / CAVE_A2 82 語 / CAVE_N 11 語 / CAVE_M 7 語 / CAVE_F 10 語  すべて OK
リテラル異常 合計 = 0 件
```

死語（誰も参照していないリテラル）も報告する。現在 `CAVE_Q` に 2 本:

- `TABP`（`0x009B0E00`）— スプライト表の先頭。今は `.bss` の `LOG` 経由で読むので不要
- `TEXBLK`（`0x0097B74C`）— `RESTORE_TEX = True` のときだけ使う

### `Asm.lit` に二重定義の検出を入れた

`assemble()` のラベル表は**後の定義で上書き**されるので、
同じ名前を違う値で 2 回定義すると**静かに間違った定数を読む**。

```python
def lit(self, label, value):
    既存に同名があれば: 値が違えば RuntimeError / 同じならまとめる
```

実際に `CAVE_Q` が `CMDPTR` と `CMDEND` を 2 回ずつ定義していた（値は同じ）。
まとめた結果 391 → 389 語。**値が違う二重定義は 1 件も無かった。**

### 現行（未適用）

```
CAVE_Q=0x838200(389) CAVE_P=0x838820(35)  CAVE_V=0x8388B0(44)
CAVE_A1=0x838960(87) CAVE_A2=0x838AC0(82) CAVE_N=0x838C10(11)
CAVE_M=0x838C40(7)   CAVE_B=0x838C60(12)  CAVE_U=0x838C90(12)
CAVE_F=0x838CC0(10)  CAVE_T=0x838CF0(2)    末尾 0x838D00（余り 768 バイト）
```

`CAVE_Q` 全 362 コード語を IDA で逆アセンブルし、
入口（`MOV R4,R0` / `STR R4,[R12,#0xF4]`）、全 BL（10 件）、全 BLX（2 件）、
エピローグを確認した。復元後は `NCCH/exefs/code_runtime.bin` と 6 点で一致。
監査 0 件、リテラル検査 0 件。

---

