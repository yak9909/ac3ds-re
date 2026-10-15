---
id: ACNL-F0309
aliases:
- F-284
title: F-284 (HIGH) — 自前 GUI（F-283 版）のクラッシュ `PC=0x839004` は「.text のゼロ埋めを NOP スライドして飛び出した」結果
summary: '**根拠**（静的。`idalib-mcp` / `code.bin.i64`）'
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8622084
- 8622080
- 1798800
- 1798804
- 5664248
- 8617984
- 8611584
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:17808-17860
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-284 (HIGH) — 自前 GUI（F-283 版）のクラッシュ `PC=0x839004` は「.text のゼロ埋めを NOP スライドして飛び出した」結果

**根拠**（静的。`idalib-mcp` / `code.bin.i64`）

1. `get_bytes` で `0x839000` 以降を読むと `4B 2D 2D 2D 23 00 1E 1E 01 00 00 00 B0 01 00 00 …`
   という**データ表**。`.text` の実行可能領域はここより手前で終わっている。
   - `0x839000` = `0x2D2D2D4B` … cond=`0010`(CS)。報告の `CPSR=0x00000010` は **C=0** なので**空振り**
   - `0x839004` = `0x1E1E0023` … cond=`0001`(NE)。**Z=0 で成立**。bits27-24=`0xE` = コプロセッサ命令
     → **未定義命令例外**。これが `PC=0x839004` の正体。
2. ゼロ語 `0x00000000` は `ANDEQ R0,R0,R0`。**Z=0 のとき何もしない＝ NOP。**
   つまり `0x838xxx` のゼロ埋めを延々と滑って `.rodata` へ出た。
3. `insn_query` で `0x1B7290 = BL ssys_ma_lyt_LayoutMgr_RenderTop`、次が `0x1B7294`。
   報告の `LR=0x1B7294` は **`BL RenderTop` 以降 `BL`/`BLX` が 1 本も実行されていない**ことを意味する。
4. `R0` は RenderTop が受け取った LayoutMgr のまま。`R3=0x3F7B2EDF` / `R12=0xBE45B566` は
   **CAVE_A1 の 2・3 命令目（`LDR R3,=LOG` / `MOV R12,#0`）が書くはずの値ではない。**
   → **`0x566DF8` の `B 0x838950` を踏んだ直後には、既にゼロを滑っていた。**

**同時に否定されたこと**

`/CTRPF_OwnGui.txt` は `上ノード list=41 記録長=1072 バイト` /
`下ノード list=42 記録長=1072 バイト` を記録している。
**組み込み直後は両画面ともコマンドリストを作れて記録もできていた**ので、
「`LIST_SIZE = 0x10000` が大きすぎて `nngxCmdlistStorage` の確保に失敗した」という
前セッションの最有力仮説は**誤り**。

**まだ確定していないこと（原因の特定）**

「誰がケーブ領域をゼロにしたか」。候補は `Sources/OwnGui.cpp` の 2 箇所だけ。
- `Disable()`（`RemoveHooks()` → 100ms → ゼロ埋め。順序は正しいが
  **ゲームが Pause 中だと 100ms が無意味**、かつ `Process::Patch` の戻り値を見ていない）
- `Enable()` の `InstallHooks()` 失敗時クリーンアップ
  （**既にフックが入っていると「素ではない」で失敗し、生きたフックを残してケーブを全消しする**。
  `Enable()` に `if (g_enabled) return true;` のガードが無い）

詳細と次手順は `scratchpad/MEMO_f284_crash.md`。

**★ IDA でケーブを検証するときの注意（このセッションで判明）**

`code.bin.i64` では **`0x838200` 以降は未マップ**。`get_bytes` はゼロを返すが実体は無く、
`patch` が `Address not mapped: 0x838950` を返して判明した。
`0x838000` は実コード、`0x839000` は `.rodata` なので**セグメントの穴**（ファイルに無いパディング）。
実機では RX として実在する。
→ **ケーブの逆アセンブル検証は、マップ済みの空き（例 `0x836700`）へ
全ケーブを同じ量だけ平行移動して書き込み、相対オフセットを保ったまま行う。**
ゲーム関数への `BL` は移動量ぶんずれるので手で足し戻して照合し、検証後は元へ戻す。

**`.text` 内のゼロ隙間（NOP スライドの入口。どこへ落ちても `0x839004` で死ぬ）**

`0x838810`–`0x838950` / `0x838AAC`–`0x838AB0` / `0x838BF8`–`0x838C00` /
`0x838C2C`–`0x838CB0` / `0x838CD8`–`0x838CE0` / `0x838CE8`–`0x839000`

---

