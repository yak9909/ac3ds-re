---
id: ACNL-F0527
aliases:
- IDA-opus-5.5-F004
title: 村の建物の実体は BsStrcMgr が作る。1 件分を写せば読み直さずに出せる（2026-09-23、**HIGH（静的＋実機）**）
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。IDA-opus-5.5-T001（見た目を即時に出す）と、利用者の指摘'
date: '2026-09-23'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1378252
- 9764284
- 5389092
- 8310680
- 9756616
- 9385908
- 9742016
- 9742012
- 7184464
- 7201176
- 6068128
- 8936190
- 6968500
- 7104960
- 7126452
- 8937452
- 5746172
- 6065328
- 8947616
- 7202496
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2937-3015
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F004: 村の建物の実体は BsStrcMgr が作る。1 件分を写せば読み直さずに出せる（2026-09-23、**HIGH（静的＋実機）**）

解析ソフト: IDA / 解析モデル: opus-5.5。IDA-opus-5.5-T001（見た目を即時に出す）と、利用者の指摘
「実際に設置した時の配置高度」への答え。実機は使っていない。

### 1. 誰が作るか

`AcStrcFieldObj` など建物のクラスは ModuleOutdoor.cro にあるが、**CRO の中にコンストラクタの
呼び出し元が 1 件も無い**（家・橋も同じ）。static.crs の匿名インポートを引くと、本体の中継
`0x1507CC` などへ CRO の ctor が差し込まれ、本体の生成関数表 `0x94FDBC`（8 B = {create, 0x523B24}）の
create（AcStrcFieldObj は `Factory_AcStrcFieldObj 0x7ECF98` = new 0x254 → ctor）から呼ばれる。
プロファイル表は `0x94DFC8`（12 B × 0x29D、{id, 名前, u16, u16}）で、**建物は 0x6C BsStrcMgr、
0x6D〜0x9D が AcStrc 各種、0x80 が AcStrcFieldObj**。

管理役 **BsStrcMgr**（本体、vtable `0x8F37B4`、実体 `g_BsStrcMgr 0x94A6C0`、段 `0x94A6BC`）の
作成段 `BsStrcMgr_CreateStep 0x6DA050` が 0: LUT・扉アニメ読み込み → 1: holder の Setup →
**2: `BsStrcMgr_SpawnStructures 0x6DE198`** → 3: 全実体の完了待ち、と進む。

### 2. 1 件分の手順（村 = 部屋フラグ 0x20 の枝）

VillageBook `sub_314514(0)` の各スロット {x, y, id} について:

1. `Building_GetVillageFilter 0x5C97A0`（表 `0x885AFE`）が **0 か 165 のものだけ**。商店街の dobj_* は 1 で作らない
2. 位置 `Field_TileToWorldFlat 0x6A54B4`: x = 32·tx + 16、y = 0、z = 32·ty + 16
3. **高さ = `Field_GetGroundHeightAtWorld 0x6C69C0(&pos, 0)` の S0 戻り値**。区画 = floor(x/512)、
   区画内のマス = floor(x/32) & 15 に分け、`Field_GetGroundHeight` と同じ `sub_6A8C80` で**区画属性ブロック**を読む
4. `Building_IsBridge 0x6CBDB4`（分類表 `0x885FEC` == 15、**橋 0x90〜0xA7 の 24 種**）なら **y += 32.0**（`flt_6DE560`）
5. `actor = Actor_SpawnByProfile 0x57ADFC(Building_GetProfile(id) 0x5C8CB0, mgr, id, &pos, 0)`
6. 管理役の一覧（{数, 容量, 配列}）へ追加:
   id 0〜3（家）は `actor+0x5C0` が 0 なら `+0x6758`、非 0 なら `+0x67CC` / `Building_IsNpcHouse`（表 `0x8887A0`、id 8〜17）は `+0x6774` /
   92・104（桟橋）・橋・199 は `+0x67CC` / **それ以外（公共事業の大半）は `+0x68C0`**
7. 特別扱い: 93（sobj_boat）は profile 0x7F で `+0x68A0`、90（踏切）は actor+1468 に別の実体、
   89 は mgr+27468 に保存、80〜83（役場）は追加で profile 0x9E を作る

**逆コンパイラは手順 3 を「y に 0.0 を書く」と誤読する**（`FSTS S0` を見落とす）。逆アセンブル `0x6DE6C0`〜`0x6DE6E4` で確定。

### 3. 実体の欄

- `Actor_ctor 0x57AE88`: **位置 actor+0x14**（x, y, z。`g_ActorSpawnPos 0x947FE8` から写す。
  ゲームはこのポインタを戻さない）、回転 +0x2C
- `actor+0x66` = 建物 id（CRO の取得子 `0xB7E5E8`、本体の中継 `0x15009C` がそれになる）
- `actor+0x5C0`（家だけ、CRO `0xB7E19C`、中継 `0x15040C`）
- 削除要求 `0x5200B8(actor)`（Vapecord DESPAWN_INSECT）= `UiScreen_RequestDestroyRecursive(基本マネージャ, actor)`
- **AcStrc の基底 dtor（CRO `0xB4B7AC`）は一覧から自分を外さない**（mgr+0x6B50 に 1 を立てるだけ）。
  `BsStrcMgr_TrackBridges 0x6D9B7C`（vtable slot 18）が **毎フレーム `+0x67CC` を読む** ので、
  消すときは**一覧から抜いてから**削除を要求しないと解放済みを読まれる
- モデルは実体の vtable slot 55（CRO `0xB27CFC`）が自分で要求し、読めるまで待つ（非同期）

### 4. gohan の実装（`work/grid-cursor`、実機未確認）

`PublicWorks.cpp` の `SpawnVisual` / `KillVisual` が上の 1 件分と逆をやる。置くと動かすは実体を作って
プレイヤーを 2 マス手前へ移す（位置の直接書き込み）。**特別 id・選別で弾かれる id・実体が見つからない
ときは従来の部屋の読み直しへ退避**。通知に「その場で反映」か「部屋を読み直しました」を出す。
「当たり判定を作り直す」は見た目が変わらないので読み直しをやめた（T004 で判定が即時と分かったため）。

検査 `tools/strc/verify_publicworks.py`（56 件 PASS）: 5 関数が `0x6DE198` から呼ばれている、一覧の番地 8 本が
`0x6DE198` の即値の組み合わせ（`ADDHI R8,R6,#0x6800` + `#0x25C` など）で作られている、`g_BsStrcMgr` は
本体の段変数 + 4 と CRO のリテラルの 2 経路で一致、32.0、住民の家の表、削除要求の末尾分岐、位置 +0x14、
CRO 取得子 2 本と中継の対応。成果物 `gohan.elf` の逆アセンブルで、高さを S0 で受けていること・
生成関数の第 5 引数（スタック）が 0 であること・特別 id のビット表を確かめた。

反証条件: 実機で置いても何も出ない／二重に出る／消した建物が残る・落ちる、村以外の部屋で
`g_BsStrcMgr` の一覧が別の意味を持つ。**生成をフレームフック（`Frame_DrawPass1024` 内）から
呼んで安全かは実機でしか分からない**（部屋の読み直しと設置関数は同じ場所から動いた実績がある）。

### 5. 実機の結果（2026-09-23、利用者）

1. 足元に置くと**その場で見た目が出て**、通知が「その場で反映」
2. 消す・足元へで**古い見た目が消える**
3. **全建物で高さが周りと合う**
4. 落ちない
5. 画面遷移のあとも異常なし

残った問題（→ F005）: 下画面の地図アイコンが変わらない、足元のアイテムの高さが変わらない（遷移で直る）、
プレイヤーが 2 マス動く。

道具: `tools/patches/cro_xref.py`（CRO 内の呼び出し元・参照）、`tools/patches/crs_import_slots.py`
（本体の中継に何が差し込まれるか）。IDB: 上の名前 19 本と `g_BsStrcMgr` ほか 4 変数、コメント 6 件。

