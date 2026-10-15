---
id: ACNL-F0086
aliases:
- F-48
title: F-48 静的 IDB を idalib-mcp で常用する — `HIGH`
summary: '`code_runtime.bin` (F-46) を **最小の ARM ELF ヘッダで包んで** idalib-mcp に読ませた。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1048576
- 1067340
- 3125430
- 5870028
- 5870016
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2529-2582
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-48 静的 IDB を idalib-mcp で常用する — `HIGH`

`code_runtime.bin` (F-46) を **最小の ARM ELF ヘッダで包んで** idalib-mcp に読ませた。

| 項目 | 値 |
|---|---|
| 入力 | `NCCH/exefs/code_runtime.elf`（`code_runtime.bin` + ELF ヘッダ 0x1000） |
| IDB | `NCCH/exefs/code_runtime.elf.i64` |
| セッションID | `acnl` |
| imagebase | `0x100000`（ELF の `PT_LOAD` で明示） |

### なぜ ELF で包むのか

生の `.bin` はヘッダが無く、**headless ではプロセッサとロードアドレスを決められない**。
ELF32 / LE / `EM_ARM` / `PT_LOAD(p_vaddr=0x100000, p_offset=0x1000)` を被せるだけで
IDA が自動で ARM・base `0x100000` として読む。生成手順は `make_elf.py`。

### デバッグ IDB との違い

| | デバッグ IDB（ida-pro-mcp） | 静的 IDB（idalib-mcp） |
|---|---|---|
| 逆アセンブル | 接続ごとに破棄。`ida_restore.py` で復元 | **永続** |
| `xrefs_to` | **空を返す**（未解析のため） | **使える** |
| メモリ読み | GDB 経由で 77-150KB/s、30 秒タイムアウト | ローカル。制限なし |
| 実行時の値 | 見える | ダンプ時点で固定 |
| 関数境界 | 手動で `add_func` | **自動解析済み** |

**広域走査・xref 探索・関数境界の確定は静的 IDB でやる。**
実行時の値やパッチの効果を見るときだけデバッグ IDB を使う。

### 自前のブルートスキャンより `xrefs_to` が正確

`Item_IsFlowerCategory` の呼び出し元を、`code_runtime.bin` を Python で走査して
ARM の `BL` だけ数えたら 7 件だったが、**`xrefs_to` は 9 件**を返した。
`0x10494C` と `0x2FB0B6` が **Thumb** からの呼び出しで、ARM のエンコードしか
見ていないスキャンが取りこぼしていた。

**自作スキャンは「そのエンコードしか見ていない」ことを忘れると静かに間違える。**
静的 IDB があるなら `xrefs_to` を使う。

### 注意

- **`xrefs_to` の結果をそのまま全部読まない。** `Item_GetId` は 261 件あり、
  一覧を丸ごと受け取るとコンテキストを大量に消費する。件数だけ欲しいときは
  `limit` を小さくして `xref_count` を見る。
- 関数境界がデバッグ IDB 側の記録と食い違うことがある
  （`0x5991CC` と記録していたものが静的 IDB では `0x5991C0` 始まり）。
  **静的 IDB の自動解析のほうを疑わず、両方を突き合わせること。**
- 静的 IDB にも `ida_restore.py` の名前を反映済み（関数 73 件、型 6 件、コメント 14 件）。
  `ida_restore.py` は **ida-pro-mcp 用**なので、idalib 側へは
  `rename` / `type_apply_batch` / `set_comments` のバッチで入れる。

---

