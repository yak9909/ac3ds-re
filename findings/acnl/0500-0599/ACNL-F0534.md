---
id: ACNL-F0534
aliases:
- IDA-opus-5-F034
title: マス数変更中のクラッシュと、縞模様の 45 度（2026-09-22、HIGH、クラッシュダンプ＋静的）
summary: '解析ソフト: IDA / 解析モデル: opus-5。'
date: '2026-09-22'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4811068
- 4812396
- 5626132
- 7657284
- 6884200
- 5178320
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3351-3433
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F034: マス数変更中のクラッシュと、縞模様の 45 度（2026-09-22、HIGH、クラッシュダンプ＋静的）

解析ソフト: IDA / 解析モデル: opus-5。

### 1. `nwgfx_SkeletalModel_Create 0x0049693C` は確保の失敗を検査しない

利用者報告:「マス数を変更して描画更新中に再度マス数を変更するとクラッシュします」。
ダンプ（`work/evidence/gridcursor/crash_dump_00000013.dmp`）:

| 欄 | 値 |
|---|---|
| 例外 | 3 = データアボート、ARM11 |
| PC | **`0x00496E6C`**（ゲーム内） |
| LR | `0x0055D914` |
| r5 | **0** |
| 落ちた命令 | `ldr r0, [r5]` |
| 関数 | **`nwgfx_SkeletalModel_Create 0x0049693C`** |

r5 は組み立て中のオブジェクト。この関数はアロケータ（第4引数の vtable+8）が 0 を返しても
**その null をそのまま使い続ける**。つまり **instance ヒープが尽きるとゲーム自身が落ちる**ので、
`ModelInstance_Create` の戻り値や `node+0x1EC`（V2-F025）を見る検査は**全部手遅れ**だった。

**なぜヒープが尽きたか**。`SetFootprint` が `s_stage != Ready` のときに早期返却していた。
そのため**組み立ての途中に数を変えると**、ヒープは古い体数で作られたまま、
描画スレッドは毎フレーム `want = W*H` を**新しい値で**計算して建て続けていた。

直しは 3 層:

1. **呼ぶ前に残りを見る**。`sead::ExpHeap::getFreeSize 0x0074D744` で 1 体分に満たなければ
   `Fail::kHeapExhausted` で止まる。ビルド済みコードで `HeapGetFreeSize` が
   `ModelInstance_Create` より先に走ることを逆アセンブルで確認済み。
2. **建てる数は生の footprint ではなく「ヒープを作ったときの体数」**。途中で増えようがない。
3. **数の変更はどの段からでも必ず解放を挾む**。`TeardownAll` は半端な組み立ても片付ける。

### 2. 縞模様を 45 度傾けるのはアニメ 1 本

`UnitCursor.bcres` のマテリアルアニメは 3 本:

| 名前 | 位置 | フレーム | メンバ |
|---|---|---|---|
| `UnitCursor` | 0x1148 | 150 | `MaterialColor.Constant0` / `Constant1` / `TextureCoordinators[1].Translate` |
| `UnitCursorNG` | 0x1358 | 150 | `MaterialColor.Constant0` / `Constant1` |
| **`UnitCursorRotate`** | **0x161C** | **3** | **`TextureCoordinators[1].Rotate` の 1 つだけ** |

`UnitCursorRotate` のキーは 4 つで、`(frame, value)` の対:

| frame | value | |
|---|---|---|
| 0 | 0.785398 | **45度** |
| 1 | 2.35619 | 135度 |
| 2 | 3.92699 | 225度 |
| 3 | 5.49779 | 315度 |

家具の 4 向き（`Angle16_ToQuadrant 0x00690B68` の 0〜3）に 45 度ずつの斜線を割り当てている。
**利用者の「バッファサイズはそのままに縞模様のみ 45 回転」と一致する**——このアニメは
テクスチャ座標の回転しか書かないので、形も大きさも変わらない。

実装: `MaterialAnimBuildFromRes` でもう一つ組み、**slot 2**（ゲームと同じ向きの枠。IDA-opus-5-F029）へ
結んで frame 0 で止める。slot 0 の 150 フレームは `Translate` と `MaterialColor` しか書かないので衝突しない。

**★ OFF に戻すには組み直しが要る。** `ModelInstance_ClearAnimSlot 0x004F03D0` は表の枠を 0 にするだけで、
マテリアル側の `Rotate` は**最後に書かれた 45 度のまま残る**。

### 3. F028 の訂正

F028 は「4 コマの `UnitCursorRotate` … 値は π/4 と 3π/4」と書いていたが、
実際のキーは **π/4, 3π/4, 5π/4, 7π/4 の 4 つ**。縞は 180 度対称なので**見た目は 2 種類**という
F028 の結論は変わらないが、データの記述は不正確だった。

### 4. ダンプのヘッダを最初読み違えた

Luma の例外ダンプは **ヘッダ 40 B、ARM11 のレジスタ 23 語**。
44 B / 24 語 と思って読んだため全レジスタが 1 つずれ、一度「PC=0x10 のヌル vtable 呼び出し」と
誤読した。**ヘッダの合計がファイル長と一致するかを先に検算すれば即座に分かった**
（40 + 92 + 96 + 1072 + 16 = 1316 = ファイル長）。`tools/gridcursor/read_crash_dump.py` はその検算を持つ。

根拠: `work/evidence/gridcursor/crash_dump_00000013.dmp` と `.analysis.json`、
`acnl_jpn_v15_annotated.i64` の `0x0049693C` / `0x00496E6C` / `0x004F03D0`、
`artifacts/update/romfs/Ftr/Chip/UnitCursor.bcres`、`src/gohan/gohan.elf` の逆アセンブル。
反証条件: アロケータが 0 を返さず別の経路で落ちていた、
予約量 8,192 B でも足りない構成がある、slot 2 をゲーム側が別の用途で使う場面がある。
**未確認: 1・2 ともまだ画面で見ていない。**

