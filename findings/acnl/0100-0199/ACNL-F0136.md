---
id: ACNL-F0136
aliases:
- F-98
title: 'F-98: TODO-37 の否定と、描画解析の全体精査'
summary: 'confidence: **MEDIUM**（各項目を逆コンパイル／RTTI で個別に検証。**静的解析のみ**、F-101 で訂正）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9436276
- 5500928
- 5640192
- 7647232
- 7667712
- 9432564
- 5525076
- 1388544
- 1531904
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5706-5790
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0139"]
---
## F-98: TODO-37 の否定と、描画解析の全体精査

confidence: **MEDIUM**（各項目を逆コンパイル／RTTI で個別に検証。**静的解析のみ**、F-101 で訂正）

### 1. ★TODO-37 の仮説は誤り

「`sub_11C7CC` → `sub_11CE64` → `sub_121E2C` が毎フレームの描画」は**否定**。

`sub_11CE64` は文字列 **`"sead::DefaultGfxMemoryMgrCtr"`** を直接使っており、
**sead のグラフィクス初期化**だった（`sead_GfxMemoryMgr_InitBuffers` と改名）。

- ループ 2 回でダブルバッファを作る
- `sub_11EAFC(..., 1024 / 1025 / 1040, ...)` でバッファ登録
- `sub_11EA14(...)` で共有面（深度？）

`sub_11EB68` も `sub_121E2C(cb1, cb2)` にコールバック 2 つを渡すだけの薄い層で、
フレームループではない。

### 2. ★アーキテクチャの理解を訂正: 枠組みは **sead**

F-94 で「描画は nw4c」と書いたが**層が 1 つ抜けていた**。正しくは:

| 層 | 役割 |
|---|---|
| **`sead::`**(346 クラス) | **アプリのフレームワーク・タスク・フレーム進行** |
| `nw::gfx` / `nw::lyt` / `nw::font` | 実際の描画 |
| `nn::gr` 相当（RTTI 無し） | GPU コマンド生成 |
| GSP IPC | GPU への提出 |

**具象フレームワークは `sead::UlcdDoubleCmdGameFrameworkCtrNw4c`**(vtbl `0x8FFC74`)。
RTTI 実測の継承: `DoubleCmdGameFrameworkCtrNw4c` → `GameFrameworkCtrNw4c`
→ `GameFramework` → `Framework`。

名前が示す通り **Ulcd（上下 LCD）** と **DoubleCmd（二重コマンドバッファ）**。
`g_GpuCmdListMgr` / `dword_AD9960`（現在のマネージャ）の二重化と整合する。

毎フレームの呼び出し木は **`sead::MethodTreeMgr` / `MethodTreeNode`**。

**sead の実装は `0x53F000`-`0x561000` と `0x74B000`-`0x750000`**（新規に判明）。

### 3. ★`sead::PrimitiveDrawer`(vtbl `0x8FEDF4`, 実装 `0x544E54` 付近)

即時モードの図形描画。継承なし。vtable は dtor 対のみで描画メソッドは非仮想。
**自前でテクスチャ付き矩形を出すときの有力候補。**

### 4. 精査結果の一覧

| 項目 | 判定 |
|---|---|
| F-94 GSP スタブ 6 本 | ✅ 妥当（`MRC p15` + `SVC 0x32` + ヘッダ定数を確認済み） |
| F-94「描画は nw4c」 | ⚠️ **不完全**。sead 層が抜けていた（本 F-98 で訂正） |
| F-94「静的 PICA ヘッダ 0 件」 | ✅ F-95 で走査バグとして訂正済み |
| F-95 `g_GpuCmdPtr` | ✅ 妥当（逆コンパイルで直接確認） |
| F-96 `GX_SetCommandList` | ✅ HIGH のまま |
| F-96 `GX_SetDisplayTransfer` | ⬆️ **HIGH に格上げ**（`sub_137198` で型値 3 と `w\|(h<<16)` を確認） |
| F-96 `GX_SetMemoryFill` / `SetTextureCopy` / `RequestDma` | ⚠️ **MEDIUM-HIGH のまま**。個別未検証 |
| F-97 `GpuCmd_GetProperty` | ✅ 妥当 |
| F-97「`sub_16A130` 鎖は未確定」 | ✅ 保留のままが正しかった |
| 「`nw::lyt::Drawer` は `nw::font::RectDrawer` 継承」 | ⬆️ **RTTI で裏取り済み**。推測 → HIGH |

### 5. RTTI で実測した継承関係

| 派生 | 基底 |
|---|---|
| `nw::lyt::Drawer` | **`nw::font::RectDrawer`** |
| `nw::lyt::Picture` | `nw::lyt::Pane` |
| `nw::lyt::TextBox` | `nw::lyt::Pane` |
| `nw::gfx::MeshRenderer` | `nw::gfx::GfxObject` |
| `sead::UlcdDoubleCmdGameFrameworkCtrNw4c` | `sead::DoubleCmdGameFrameworkCtrNw4c` |
| `sead::PrimitiveDrawer` | （なし） |

**2D レイアウト描画はフォントの矩形描画を土台にしている**ことが確定した。
テクスチャ描画とテキスト描画は同じ下地を共有するので、**片方が分かればもう片方も近い。**

### 6. 残る誤解のリスク

- **`0x153000`-`0x176000` の正体は依然不明。**
  `sub_14A9C8`(YUV→RGB) が同居しており画像コーデックの疑いは晴れていない
- `GX_SetMemoryFill` / `SetTextureCopy` / `RequestDma` は switch 位置からの同定のみ
- **フレームループの実体はまだ掴めていない。**
  sead 側は仮想関数越しに呼ぶため、`GpuCmd_SplitAndSubmit` や `sub_1216BC` の
  直接の呼び出し元に sead 領域が出てこない

---

