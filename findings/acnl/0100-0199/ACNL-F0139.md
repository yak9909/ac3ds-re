---
id: ACNL-F0139
aliases:
- F-101
title: 'F-101: CLAUDE.md 準拠での再精査 — confidence の系統的誤り'
summary: 'confidence: **MEDIUM**（本項自体も静的解析のみ）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5939-6024
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-101: CLAUDE.md 準拠での再精査 — confidence の系統的誤り

confidence: **MEDIUM**（本項自体も静的解析のみ）

**CLAUDE.md を条文ごとに照合して自分の記述を点検した結果。**

### 1. ★最大の誤り: confidence の付け方が定義に反していた

CLAUDE.md:

| 記号 | 条件 |
|---|---|
| `HIGH` | **静的解析と動的観測の双方**で確認 |
| `MEDIUM` | 複数の静的証拠から推定 |

**F-94 から F-100 まで 7 件すべてを `HIGH` と書いていたが、
どれも実機観測をしていない。全部 `MEDIUM` が正しい。**

7 件とも `MEDIUM` に訂正した。実機で観測できたものから順に上げる。

これは「動いた／動かない」を確かめずに確度を主張していたということで、
ドロップ解析（F-93）で実機検証によって二段ゲートが判明した経緯と対照的。
**描画側はまだ一度も実機を通していない。**

### 2. `REFERENCES/` の扱いを誤っていた

CLAUDE.md:「`REFERENCES/` と `NCCH/` は**一次情報ではない**。裏取りするまで `LOW`」

`registers.h` / `gspgpu.h` は `REFERENCES/CTRPF PROJECTS/FOXXY/Includes/` 配下、
つまり FOXXY 同梱の ctrulib であって一次情報ではない。
F-99 でこれを「正解」として扱ったのは行き過ぎ。

**代わりにゲーム側コードとの内部整合で裏を取った:**

| reg / 名前 | 整合する観測 |
|---|---|
| `0x149` `LIGHT0_CONFIG` | コードが `16 * i + 65865` と **`0x10` 刻み**で書く＝ライト別ブロックと一致 |
| `0x010` `FINALIZE` | 提出直前の**最後の 1 命令**として `0x12345678` を書く |
| `0x111` / `0x110` | FINALIZE 直前に値 1 で連続して書かれる |
| `0x2C0` / `0x2C1` | CONFIG 直後に DATA を `extra=0xB` の一括転送、値の bit31（連続書き込み）も立つ |

**名前は依然 `REFERENCES` 由来だが、使われ方は矛盾しない。**

### 3. 新たに見つかった読み違い: `mgr[9]` と `mgr[10]` の混同

`GpuCmd_GetProperty` の id 522 を「処理済み数」と書いたが、
**`mgr[9]` と `mgr[10]` は別のカーソル**だった。

- `GxQueue_Dispatch`: `mgr[9]` を進める（処理カーソル）。
  ループ条件は `dword_AD98D4 + mgr[10] > mgr[9]`
- `GpuCmd_GetProperty` case 12/13: `mgr[10]` をキューの参照 index に使う

**`mgr[10]` の役割は未確定**として記録し直した。

### 4. 表記規則（CLAUDE.md「16 進なら必ず `0x` を付けて書く」）

十進と 16 進が混在して紛らわしい箇所を補記した:
`28 (0x1C)` バイト / `512 (0x200)` / `520 (0x208)` / `784 = 0x310` /
`24 (0x18)` バイト。

### 5. 「SDK と対象固有ロジックを分離する」（CLAUDE.md）

明示していなかったので `DOCS/rendering.md` 冒頭に追記:

**描画解析で扱っているのは全部 SDK / ライブラリのコード**
（`sead` / `nw4c` / `nn::gr` / GSP）で、**ACNL 固有のロジックではない。**
他の 3DS タイトルにもほぼそのまま当てはまる反面、
「ACNL の解析」としての価値は間接的。

### 6. 「LOW は rename せず」への適合

今回 rename したものはいずれも複数の静的証拠がある `MEDIUM` 相当で、
`LOW`（仮説）を rename したものは無い。ただし
`nwgfx_SimpleMaterialActivator_Activate` の「Activate」、
`sead_GfxMemoryMgr_InitBuffers` の「InitBuffers」は
**メソッド名部分が推測**なので、その旨をコメントに残してある。

### 7. 今回の巡回で誤りが出なかったもの

`g_GpuCmdPtr` / `g_GpuCmdEnd` / `GpuCmd_Advance` /
`GpuCmd_SplitAndSubmit` の終端 4 コマンドの構成 /
GX 5 本の type バイト / `Copy24Bytes` / RTTI の継承関係 /
GSP スタブの IPC ヘッダ分解。

---

