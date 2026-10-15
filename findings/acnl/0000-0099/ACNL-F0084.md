---
id: ACNL-F0084
aliases:
- F-46
title: F-46 実機イメージ `code_runtime.bin` を吸い出した — `HIGH`
summary: '`dump_code.py` で実行中プロセスから吸い出した。**`NCCH/exefs/code_runtime.bin`、10,485,760 バイト。**'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1048576
- 9308782
- 9308826
- 9789428
- 10485760
- 11172244
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2315-2382
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-46 実機イメージ `code_runtime.bin` を吸い出した — `HIGH`

`dump_code.py` で実行中プロセスから吸い出した。**`NCCH/exefs/code_runtime.bin`、10,485,760 バイト。**

| 項目 | 値 |
|---|---|
| 範囲 | VA `0x00100000` - `0x00B00000` |
| 対応 | **`VA = ファイルオフセット + 0x100000`（検証済み）** |
| 取得条件 | ゲーム再起動直後、**パッチ・ケーブをすべて外した素の状態** |

### 検証

アンカー **17 件すべて一致**（旧 `code.bin` は 6 件中 2 件しか無く base も食い違っていた）。
命令だけでなく、RTTI のポインタ連鎖と文字列も一致した:

```
VA 0x8E0A6E -> "N5fgobj11ObjectSwingE"
VA 0x8E0A9A -> "N5fgobj11ObjectTimerE"
VA 0x955FF4 -> 0x00007FFE   (g_EmptyItem)
```

**F-43 の RTTI 手法がこのファイル単体で使える。** 実機接続なしでクラス名を引ける。

### 範囲の根拠

`0x1000` 単位でマップ状況を実測した:

| 範囲 | 状態 |
|---|---|
| `0x100000` - `0xA00000` | `.text` / `.rodata` / `.data` |
| `0xA00000` - `0xB00000` | マップ済み。ほぼゼロ（`.bss`）。`g_PlayerObjects`(`0xAA7994`) を含むのでダンプに入れた |
| `0xB00000` - `0xB10000` | **未マップ**（ここで打ち切り） |

### `.code` の外にもマップ領域がある（未同定）

| 範囲 | 内容 |
|---|---|
| `0xB10000` - `0xBD0000` (768KB) | 未調査 |
| `0xBF0000` - `0xC40000` (320KB) | `0xC00000` は ARM コード。`0xC10000` は高エントロピー |
| `0xC50000` - `0xC60000` (64KB) | 未調査 |

CTRPF / Luma 側のものか、ゲームの別セグメントかは**未確認**。
本解析で扱ってきた関数はすべて `0xA00000` 未満なので、当面は影響しない。

### 注意 — ファイルイメージとは別物

- `.data` は**起動後の値**。初期値ではない。
  今回は再起動直後に吸ったので比較的素に近いが、保証はない
  （実際 `g_PlayerObjects[0]` は `0` = プレイヤー未生成の状態で入っている）
- `.bss` 相当はファイルには存在しないものが実行時の内容で入っている
- **パッチ・ケーブを当てたまま吸うと焼き付く。** 今回は吸う前に 14 箇所すべてが
  素の値であることを確認してから開始した

### IDA への読み込み

新規に開くときの設定:

| 項目 | 値 |
|---|---|
| processor | ARM little endian |
| ROM start address / Loading address | `0x00100000` |
| 32bit / ARMv6K (ARM11) | |

これで逆アセンブルが IDB に残り、実機接続なしで解析できる。
`ida_restore.py` の関数定義・リネームもそのまま適用できる。

---

