---
id: ACNL-F0516
aliases:
- IDA-opus-5.5-F015
title: 建物エディターの下調べ — カメラ・プレイヤーの停止・占有マップ・足元の読み方（2026-09-23、MEDIUM（静的。実機未確認））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「Vapecord の MapEditor のカメラを参考に、建物を遠隔で建てる。プレイヤーは操作不可」。'
date: '2026-09-23'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9742464
- 1735708
- 1731388
- 9327652
- 1724708
- 1709488
- 1724712
- 1731804
- 5401100
- 3038904
- 11214312
- 3038932
- 1775392
tags:
- player
- map
- camera
supersedes: []
source: IDA:work/FINDINGS.md:2506-2538
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F015: 建物エディターの下調べ — カメラ・プレイヤーの停止・占有マップ・足元の読み方（2026-09-23、MEDIUM（静的。実機未確認））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「Vapecord の MapEditor のカメラを参考に、建物を遠隔で建てる。プレイヤーは操作不可」。

### 1. カメラ
- `*(0x0094A880)` = **CameraGame**（RTTI。dtor `0x1A7C1C` が 0 を書く。Vapecord CAMERA1 の JPN 列と一致）
- `CameraGame_Calc 0x1A6B3C`（vtbl_CameraGame `0x8E5424` の +0x10）: モード表 `off_94A8F0`（16 B = enter / calc の PMF）を +242 のモードで回す →
  **`CameraGame_ApplyTarget 0x1A5124`** が目標 +276..（基準 xyz、ずれ xyz、角 u16×2、距離）を **+4..** へ写す（または +244.. と補間）→
  `CameraGame_UpdateEye 0x1A15B0` が注視点 +36 = 基準 +4 + ずれ +16、視点 +48.. = 注視点 + 距離 +32 × 角 +28/+30 の方向
- Vapecord UNLOCKCAMERA（JPN `0x1A5128`）は ApplyTarget の 2 語目 `E2805C01` を **`E8BD81F0`（POP {R4-R8,PC}）**にして止める。
  先頭は PUSH {R4-R8,LR} なので釣り合う。呼び元 `0x1A6CDC` の次の命令は `LDRB R0,[R4,#0xF2]` で戻り値を使わない。
  → 止めている間は **+4..+C（基準位置）を自分で書けばカメラが動く**（静的な結論。実機で確かめる）

### 2. プレイヤーを止める
既存の入力遮断ケーブ A はスライドパッドを通す（ビット 0x00F00000 は残し、アナログ値は触らない。仕様）。
アナログ値は生読み `sub_540870` の中で `sub_353500` が **+0x11C / +0x120** へ書く（このケーブより前）。
→ ケーブ A に**モード 3**（既知のボタン＋スライドパッドのビットを落とし、+0x11C/+0x120 を 0）を追加。40 語、`0x838020..0x8380C0`（原本 0、確保ケーブ 0x838100 の手前）。
`verify_input_block_modes.py` が Unicorn で 6,000 件（モード 0〜4 × タッチ × アナログ）を独立模型と照合。

### 3. 占有マップ（どの建物の上か）
`Building_WriteOccupancy 0x526A0C(1, x, y, id, slot)` → `OccupancyLayer_SetCell 0x2E5EB8`: **層 1 = `*(0xAB1DE8)`、112×96 バイト、値 = 建物表のスロット番号**、
消去 `OccupancyLayer_Clear 0x2E5ED4` は 0xFF で埋める（HIGH、静的）。

### 4. 足元（カーソルのマス）
`Building_GetFootprint 0x1B1720` → カテゴリ別 → `sub_1BD87C` は**読み込み済みの一覧を名前のハッシュで探すだけ**で、村に無い種類は 0 を返す。
→ gohan は `Strc/data/<名>.bin` を **RomFS から直接読む**（`RomfsIndex::ReadFile`。ディレクトリ／ファイルのハッシュ表を辿り小さく読む。更新 → base の順）。
ハッシュの式は Python で base 12,938 本・update 4,150 本の全ファイルで照合、C++ はホストの g++ で組んで生の RomFS 4,266 本＋無いパス 400 本を照合（`tools/strc/verify_building_editor.py`）。
マスの規則は Building_WriteOccupancy と同じ（橋は 0 と 0xA1 を飛ばす、ほかは 0 を飛ばす）。最大 48 マス（`dobj_rebuilding_03`）。

根拠: `acnl_jpn_v15_annotated.i64` の上記関数（名前とコメントを入れた）、Vapecord `SeedCodes.cpp` tileSelector / `Game.cpp` Camera / `Addresses.hpp`、
`tools/strc/verify_building_editor.py`、`tools/patches/verify_input_block_modes.py`。
反証条件: エディター中にカメラが動かない（ほかにも +4 を書く経路がある）、スライドパッドでプレイヤーが歩ける（別経路でアナログ値を読む）。

