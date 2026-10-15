---
id: ACNL-F0173
aliases:
- F-135
title: 'F-135: `code.bin.i64` と `code_runtime.elf.i64` の独立照合 — `HIGH`（同一バイト列・アドレス）/ `MEDIUM`（実機での意味づけ）'
summary: 前回の「確定」を、別 IDB と別経路で再監査した。`code_runtime.elf.i64` は実機から取得した
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5079112
- 5066412
- 1320648
- 1317704
- 5079584
- 5080196
- 9423532
- 5079552
- 4934412
- 5429228
- 4934428
- 5429248
- 1320744
- 5076288
- 5067032
- 4934324
- 5429068
- 1048576
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:8931-8976
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-135: `code.bin.i64` と `code_runtime.elf.i64` の独立照合 — `HIGH`（同一バイト列・アドレス）/ `MEDIUM`（実機での意味づけ）

前回の「確定」を、別 IDB と別経路で再監査した。`code_runtime.elf.i64` は実機から取得した
コードダンプを ELF 化した照合用 IDB であり、ライブ GDB のプロセスそのものではない。
両 IDB を同時に開き、同じ VA の raw bytes を比較した結果は次の通りだった。

| VA | 比較長 | 差分バイト数 |
|---:|---:|---:|
| `0x4D8048` (CFNU/CFNT parser) | 440 (`0x1B8`) | **0** |
| `0x4D4EAC` (EmitGlyphQuad) | 740 (`0x2E4`) | **0** |
| `0x1426C8` (descriptor loop) | 144 (`0x90`) | **0** |
| `0x141B48` (descriptor init) | 64 (`0x40`) | **0** |
| `0x4D8220` (sheet-table size) | 404 (`0x194`) | **0** |
| `0x4D8484` (texture parameters) | 144 (`0x90`) | **0** |

さらに、次の独立した証拠も一致した。

- `0x8FCAAC` の ResFont vtable 128 bytesと、`0x4D8200` の `CFNU/FINF/CFNT/CMAP/TGLP`
  文字列領域は両 IDB で byte-for-byte 一致した。
- parser の xref は両 IDB とも `0x4B4B0C` / `0x52D7EC` の2件、sheet-table size は
  `0x4B4B1C` / `0x52D800` の2件、descriptor 初期化は `0x142728` / `0x4D7540` の2件、
  texture parameter は `0x4D5118` の1件だった。
- 2つの呼び出し側 (`0x4B4AB4`, `0x52D74C`) を両 IDB で逆コンパイルし、parser →
  `20 * sheet_count` 確保 → `SetGlyphSheetTable` という流れが同じであることを確認した。

このため、**この6関数の命令列・関数境界・同一ビルド上の VA 対応に矛盾はなく**、F-133/F-134 の
分岐記述を撤回する反例も見つからなかった。一方、runtime IDB の metadata は imagebase
`0x100000` と表示されるが、実際のコード名前空間は `0x4D...` で静的 IDB と同じだった。
`0x5D...`（`+0x100000`）を問い合わせると別領域になるため、照合時は同じ VA を使う。

ただし、これは「実機ライブで parser/descriptor/handle 分岐をその瞬間に実行した」証拠ではない。
このセッションでは `ida-pro-mcp` の `py_eval` / GDB メモリ読み取り endpoint が公開されておらず、
実機の live `ResFont*`、descriptor `+0/+0x08`、lazy handle の生成時点は未確認のままである。
従って確度を次のように分離する。

| 主張 | 確度 | 根拠 |
|---|---|---|
| 6関数の VA・命令列・分岐・サイズが実機ダンプと一致 | **HIGH** | raw bytes 6領域、xref、逆コンパイルの独立照合 |
| TGLP offset、descriptor 0x14-byte layout、immediate/batch の静的解釈 | **MEDIUM** | 上記静的証拠。実行時 descriptor 値は未採取 |
| 自前 callback が既存 descriptor/handle をそのまま再利用できる | **LOW** | live pointer/所有権/後段 submit 未確認 |

次回 `ida-pro-mcp` が利用できる状態で、`scratchpad/dump_glyph_atlas.py` を停止中の実機に
対して実行し、上表の MEDIUM/LOW を一文字・一フォントから昇格または反証する。

---

