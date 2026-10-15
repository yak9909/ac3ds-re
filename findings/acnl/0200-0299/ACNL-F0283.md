---
id: ACNL-F0283
aliases:
- F-260
title: 'F-260: F-259 の設計を実装し、IDA の逆アセンブルで検証した（実機未適用） — `HIGH`（静的のみ）'
summary: '`PATCHES/cave_node_record.py`。`cave_node_draw.py` を複製し、F-259 の設計を載せた。'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5669596
- 8609792
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:15356-15417
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-260: F-259 の設計を実装し、IDA の逆アセンブルで検証した（実機未適用） — `HIGH`（静的のみ）

`PATCHES/cave_node_record.py`。`cave_node_draw.py` を複製し、F-259 の設計を載せた。

### 実装した内容

| 要素 | 実装 |
|---|---|
| 自前のコマンドリスト | id 100（上）/ 101（下）。`SelectList` 後、マネージャの `+0x04`(base) が 0 なら確保済み `0x4000` の `+0x1000` / `+0x2000` と size `0x1000` を書く |
| 記録スロット（vtable `+0x14`） | `GetProperty(519)` → `SelectList(node+0x100)` → base/size 設定 → `sub_7B01CC` → `sub_7B05B0` → `DrawBegin1` → 自前スプライト → `DrawEnd1` → `Commit(node+0x104..+0x110)` → `SelectList(退避)` → `node+0x11D = 0` |
| 再生スロット（vtable `+0x08`） | **ゲームの `Layout_ReplayRecordedList`（`0x5682DC`）をそのまま指す** |
| 登録ケーブ | 優先度 `0xFF`、`node+0x100` に list id、`node+0x11D` に記録要求を毎フレーム立てる |
| 雛形 | リストの tail（本物の Layout）から `+0x28`〜`+0x74` の 20 語を一度だけ複製。幅・高さ・行列（`sub_4D6C90` が読む 0x40 バイト）で、**ポインタを含まない** |

★記録開始後の早期離脱は専用ラベル `endrec` へ飛ばし、
**必ず `DrawEnd1` → `Commit` → `SelectList(退避)` を通す**。
リストを戻さずに抜けるとゲームが自前のリストへ書き込んでしまう。

### 検証（IDA の逆アセンブル）

実機には一切適用していない。生成語を**静的 IDB の `.text`（ファイル実体のある領域）へ
一時的に書き込み、IDA に逆アセンブルさせて**確認し、そのあと元のバイト列へ戻した
（`idb_save` はしていない。復元も読み戻して確認済み）。

`0x838080` 以降の空き領域は IDB 上では書き込めないため、
ケーブの基準を `0x836000` 台にして生成し直した。相対分岐・PC 相対リテラルは
基準に依らず同じで、`BL` の飛び先も IDA が正しい関数名で解決した。

確認できたこと:

- `BL GpuCmd_GetProperty` / `BL GpuCmd_SelectList` / `BL sub_7B01CC` / `BL sub_7B05B0` /
  `BL GpuCmd_CommitListAndCaptureDelta` / `BL ssys_ma_lyt_LayoutMgr_AddLayout` がすべて正しい関数へ解決
- `LDR R2,[R2,#0xC]` → `BLX R2`（DrawBegin1）、`LDR R2,[R2,#0x14]` → `BLX R2`（DrawEnd1）
- `ADD R0,R4,#0x104 / +0x108 / +0x10C / +0x110` が Commit の 4 引数として正しく並ぶ
- 早期離脱がすべて `endrec` へ向いている
- 登録ケーブの優先度 `0xFF`・list id `0x64`・`STRB R2,[R1,#0x11D]` が意図通り

### ★逆アセンブルで見つけて直した不具合

登録ケーブで **`R3`（リストの tail）が prev/next の検査で上書きされ、
雛形の複製が永久に実行されない**状態だった。

```
LDR R3,[R0,#0xC]   ; tail
CMP R3,R1 / BEQ ...
LDR R3,[R1,#4]     ; ★prev で R3 が潰れる
LDR R3,[R1,#8]     ; ★next で更に潰れる
CMP R3,#0 / BEQ    ; tail のつもりが next(=0) を見て必ず分岐
```

`MOV R12,R3` で tail を退避し、複製のカウンタを R3 に変えて解決した。
**机上では気付けず、IDA に逆アセンブルさせて初めて分かった。**

### 実機へ入れる前に残っている確認事項

- `node+0x11C`（allowNoSplit）と `+0x114`（状態無効化フラグ）は 0 のまま。
  本物の Layout がどんな値を持つか未確認
- 記録は毎フレーム行う設計。自前リストは自前バッファなので F-223 の枯渇は起きないはずだが未確認
- `SET_PROJECTION` / `RESTORE_TEX` / マテリアルの控えは有効のまま残してある

---

