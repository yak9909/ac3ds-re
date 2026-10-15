---
id: ACNL-F0304
aliases:
- F-279
title: 'F-279: 検証道具を全ケーブに広げ、死語を 1 本落とした — `HIGH`'
summary: '`build_v` / `build_pass` / `build_t` は生の語列を返すので、'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10161408
- 10161664
- 9942860
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:17175-17224
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-279: 検証道具を全ケーブに広げ、死語を 1 本落とした — `HIGH`

### `verify_literals.py` が `Asm` 由来でないケーブも見るようにした

`build_v` / `build_pass` / `build_t` は生の語列を返すので、
これまで「Asm 由来でないので飛ばす」と出るだけだった。**そこが盲点になっていた。**

生の語列でも PC 相対 LDR は復号できるので、
「参照先がケーブ内か」「末尾のリテラル領域か」「何を読むか」を出すようにした。

結果:

| ケーブ | PC 相対 LDR | 参照先 | 値 |
|---|---|---|---|
| `CAVE_V` | 1 本 | 語 43/43（末尾） | `0x009B0D00` = `LOG` |
| `CAVE_B` | 1 本 | 語 11/11（末尾） | `0x009B0D00` = `LOG` |
| `CAVE_U` | 1 本 | 語 11/11（末尾） | `0x009B0D00` = `LOG` |
| `CAVE_T` | 0 本 | — | リテラル境界は無関係 |

**3 本とも末尾のリテラルから `LOG` を読んでいるだけで、問題は無かった。**
盲点は塞いだので `Asm` 化の必要性は下がった（`INSTALL_PROBES=False` で入れてもいない）。

### 死語 `TABP` を削除

`verify_literals.py` が検出した「誰からも参照されていないリテラル」2 本のうち、
`TABP`（`0x009B0E00`、スプライト表の先頭）は
表の位置を `.bss` の `LOG` 経由で読むようになったので不要。削除して `CAVE_Q` は 389 → 388 語。

`TEXBLK`（`0x0097B74C`）は `RESTORE_TEX = True` のときだけ使うので残す。

### 検証

- 監査: 総異常 0 件・重なりなし・余り 784 バイト
- リテラル検査: **全 11 ケーブで異常 0 件**
- IDA: リテラルが 1 本減って全 LDR のオフセットがずれるので、
  入口（`MOV R4,R0` / `STR R4,[R12,#0xF4]`）と
  エピローグ（`LDR R4,=LOG` / `LDR R4,[R4,#0xF4]` → `Commit` → `STRB [R4,#0x11D]`）を
  空き `.text` へ相対位置ごと当てて確認。復元後 `code_runtime.bin` と一致

### ケーブ配置（F-279 時点。現行・未適用）

```
CAVE_Q=0x838200(388) CAVE_P=0x838810(35)  CAVE_V=0x8388A0(44)
CAVE_A1=0x838950(87) CAVE_A2=0x838AB0(82) CAVE_N=0x838C00(11)
CAVE_M=0x838C30(7)   CAVE_B=0x838C50(12)  CAVE_U=0x838C80(12)
CAVE_F=0x838CB0(10)  CAVE_T=0x838CE0(2)    末尾 0x838CF0（余り 784 バイト）
```

---

