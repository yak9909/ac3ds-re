# 描画 / GPU まわり

### F-149 native Picture/TextBox cloneによる本文フレームpanel（静的＋実機、`HIGH`）

会話list 32のcommit直前に `P_bg_L_00` / `P_bg_R_00` / `P_soft_L/R/T/B` と `T_msg_00` を
この順にclone drawへ追加すると、元会話を変えず別位置に本文フレームと文字を描ける。各Paneへ
同じ絶対translationを設定すると縁が中心へ重なるため、`P_bg_L_00`からの移動差分を各Pane固有の
translationへ加える必要がある。実機でこの差分版の四辺・本文の整列を確認した。

話者名背景/文字は意図的に含まない。`PATCHES/cave_ui_picture_clone.py`はboot限定・実行時pointer
検証付きであり、検証後に復元済み。

### F-148 native Picture cloneによる自前2D背景panel（静的＋実機、`HIGH`）

`nwlyt_DrawPaneTreeToCurrentList` の `0x4D71B8` はPane treeの最終cursorがR1にあり、stockが
`g_GpuCmdPtr`へcommitする直前である。ここでlist 32だけを選び、既存 `P_nam_00`をprivate caveへ
0x158 bytesコピーして、元のDrawContext/cursorで `nwlyt_Picture_DrawToCommandList` を直接呼んだ。
cloneはLayoutにリンクせず、source Paneも変更しない。clone transform `+0x8C/+0x9C`を
`-50.0f/-20.0f`へ変更すると、実機で会話名前欄の背景が元とは別の右下寄り位置に表示された。

これがscreen-spaceの自前背景panelを正規UI listへ追加する最小実証である。実装は
`PATCHES/cave_ui_picture_clone.py`。ただしこの版は会話中のlive `P_nam_00` materialを借りるboot限定の
実験であり、任意asset・lifetime・会話外表示は未解決である。

### F-147 `nw::lyt::Picture` の2D command-list経路（静的＋実機、`HIGH`）

`vtbl_nw_lyt_Picture=0x8FBFFC` のslot `+0x68` は
`nwlyt_Picture_DrawToCommandList` (`0x73CB58`) である。`nwlyt_Pane_DrawRecursive`
(`0x73B524`) はその戻りcursorをchild Paneへ順に渡す。PictureはmaterialとPane geometryを
DrawContextへ蓄積し、`0x4B8360`がqueued UI state/geometryを入力cursorへコピーして更新cursorを
返す。したがって画面固定の背景panelは、world/shadow用FuncNode commandを流用せず、F-145の
list 32 record→main list replay経路に載せるのが正規候補である。

live traceでは会話layoutの `P_nam_00` / `P_nam_01` / `P_soft_L/R/T/B` 等のPictureが
`vptr=0x8FBFFC`、draw context=`0x32FF62EC`、list 32で動作した。full-screen 432×240のPictureは
別のlist 19だった。自前Pictureの生成・所有権・破棄、および1枚の正確なcommand rangeは未確定。

### F-146 batch command source の構成（静的＋停止中live照合、`MEDIUM`）

`TextBatch_BuildCommandStream` (`0x4D6570`) は `TextWriter+0x44` のbatchを生成する。
最初に `0x8ADA30` の固定0x60-byte PICA command templateを `batch+0x10`へコピーし、
`batch+0x1C=24 dwords` とする。F-145の会話名batch source先頭0x60 bytesはこのtemplateと
完全一致した。その後、glyph instanceのtexture/state切替と頂点情報を `0x4D6CE0` が
group単位でbatch sourceへ追記し、最後に必要なrange cache requestを発行する。

`TextBatch_CopyToCommandBuffer` が付ける別の0x60-byte headerには、
`TextDraw_BuildFourCornerColors` (`0x4D7EF0`) が生成する64-byte四頂点色が含まれる。
これはbatch sourceの固定seedとは別物で、TextBoxの色・alphaに従ってsubmit時に作られる。
各PICA registerの詳細な意味とatlas handleのmaterialize時点は未確定である。

### F-144 会話 TextBox の batch submit 入口（静的＋実機）

会話中の `0x4BAFFC`（`sub_4BAFB0` 内の文字列描画呼出し）を捕捉し、register/string/pane
identityから会話対象と確認した（非定数のsoftware-BP conditionは後に信頼できないと判明）。
TextBox=`0x32D20220`、文字列=`あんこ`（長さ3）、local TextWriter=`SP=0x0FFFFCC0`、
font=`0x3302ABE0`、pane width=`96.0f`、size=`18×24`、batch=`0x32D22FD8`（capacity 9、
停止直前 count 0）で、writer `+0x40` は0、`+0x44` は非0だった。

同じフレームの `0x4B7CE0` 入口では `R0=0x32FF62EC`、`R1=0x327DEA78`、
`R2=0x32D20220`、`R3=0x32D2033C`、stack引数=`0x330A605C`。batch の glyph countは3、
`+0x1C` の生成済み command dword countは `0xB6`（728 bytes）だった。`sub_4D6570` で
作られた batch command stream が `0x4B7CE0`→`0x4D520C` でGPU command bufferへ取り込まれる。

静的な後段は `0x73CF48`→`0x4BAFB0`→`0x7E7F48`→`0x4D4EAC`→`0x4B7CE0`→
`0x4D520C`。`0x4B7CE0` が batch count を検査し、`0x4D520C` が descriptor/instance を
GPU command bufferへコピーする。従って会話は immediate texture path ではなく、batch
submitを使う。後段のcommand-list接続は次のF-145で解決した。atlas handle生成の瞬間は未観測。

### F-145 TextBox batchからメインGPU command listまで（静的＋実機）

会話名 `T_nam_00`（「クロベエ」、4 glyph）を対象限定traceで採取した。
`TextBatch_CopyToCommandBuffer` のentryは `R1=0x327DEAB8`、batch source=`0x32D23190`、
command count=`158 dword`（632 bytes）、control `+8/+9=1/0`。同関数はまず0x60-byteの
PICA state headerを出し、続けて`Mem_Copy`する。実機でsource 632 bytesと
`0x327DEAB8+0x60`が全一致し、copy終端は`0x327DED90`だった。

構築先はメイン二重bufferではなく専用command list 32:

| field | live value |
|---|---:|
| manager / base | `0x327DDC2C` / `0x327DDC80` |
| size / end | `0x9000` / `0x327E6C80` |
| TextBox batch entry | base `+0xE38` |

`nwlyt_Pane_DrawRecursive` (`0x73B524`) がPane slot `+0x68`の戻りpointerを子へ連鎖し、
`nwlyt_DrawPaneTreeToCurrentList` (`0x4D7174`) が最後に`g_GpuCmdPtr`へcommitする。
`ssys_ma_lyt_Layout_RecordPaneTree` (`0x5686D4`) はlist 32へ記録し、
`GpuCmd_CommitListAndCaptureDelta` (`0x7B0694`) が範囲を保存する。

再生側の対象限定traceでは、source list 32 offset 0 / length `0x3270`が、メインlist 1
（base `0x3229D0C0`, size `0x100000`）へ5秒で302回統合された。入口LRは`0x5683E8`。
`GpuCmd_ReplayRecordedListRange` (`0x7B0A28`) の直接Split回数は今回0で、専用listを個別提出
せずメインlistへ統合し、通常フレームの`GpuCmd_SplitAndSubmit`経路へ載せる構造である。

再現・再監査用: `scratchpad/trace_text_batch_submit.py`、
`scratchpad/trace_layout_list_replay.py`。両hook/cave/bufferは採取後にstock/zeroへ復元済み。

対象: 日本語版無印。静的解析は `code.bin.i64`（セッション `acnl_code`）。

**現状は「地図作り」の段階。実際に描画を試すのは解析が固まってから。**

---

## ★この文書の確度について（CLAUDE.md 準拠、F-101）

- CLAUDE.md の定義では `HIGH` は「静的解析と動的観測の双方で確認」。
  **実機観測を通したものだけが `HIGH`**、それ以外は `MEDIUM` 止まり。

| 実機で確認済み（`HIGH`） | 出典 |
|---|---|
| `g_GpuCmdPtr` / `g_GpuCmdEnd` / 管理構造体のレイアウト | F-102 |
| 二重コマンドバッファとフレームごとのスワップ | F-102 |
| GX type 1 / 2 / 3 の発火、1 フレームの構成 | F-103 |
| `GpuCmd_SplitAndSubmit` の呼び出し元 | F-104 |
| ResFont CMAP `U+904A→0x0A01` と cache 更新 | F-139 |
| CharWriter の descriptor付き batch 分岐と44-byte glyph instance | F-139 |
| TextBox batchのlist 32構築、632-byte copy、メインlist 1への再生 | F-145 |

| 静的解析のみ（`MEDIUM`） | 出典 |
|---|---|
| GX type 0 / 4（未発火） | F-100 |
| `nw::gfx` / `nw::lyt` / `nw::font` の構成 | F-94 / F-98 |
| `g3d::FuncNode` のコールバック機構 | F-106 |
| PICA レジスタ名（`REFERENCES` 由来） | F-99 / F-101 |
| ResFont atlas の TGLP/descriptor layout と native text bridge | F-133〜F-139（F-135でruntime dumpとbyte照合、F-136でrange request、F-137でtexture引数の解釈を補正、F-139でCMAP/batch経路のlive値を確認。handle materialize/backend bindは未確定） |
- **ここで扱うのは全部 SDK / ライブラリのコード**（`sead` / `nw4c` / `nn::gr` / GSP）で、
  **ACNL 固有のロジックではない。** 他の 3DS タイトルにもほぼそのまま当てはまる反面、
  「ACNL の解析」としての価値は間接的。
- **PICA レジスタ名の出典は `REFERENCES/CTRPF PROJECTS/FOXXY/Includes/ctrulib/gpu/registers.h`。**
  CLAUDE.md の通り `REFERENCES/` は一次情報ではないので、
  **名前は裏取り前提**。ただし後述の内部整合性チェックは通っている。

---

## 全体構成（F-94 / F-98 で訂正）

**★層は 4 段。F-94 では sead 層を見落としていた。**

| 層 | 名前空間 | 実装位置 | 役割 |
|---|---|---|---|
| **フレームワーク** | **`sead::`** 346 | `0x53F000`-`0x561000` と `0x74B000`-`0x750000` に散在※ | **アプリ進行・タスク・フレーム** |
| 描画 | `nw::gfx` / `nw::lyt` / `nw::font` | `0x48D000`-`0x4D8000` | 実際の描画 |
| GPU コマンド | `nn::gr` 相当（RTTI 無し） | `0x1216BC`-`0x128248`, `0x134D28` | コマンド列生成 |
| GPU 提出 | GSP IPC | `0x124000`-`0x137000` | GSP へ送る |

具象フレームワークは **`sead::UlcdDoubleCmdGameFrameworkCtrNw4c`**(vtbl `0x8FFC74`)。
Ulcd = 上下 LCD、DoubleCmd = 二重コマンドバッファ。
※ 具象フレームワークの vtable エントリの分布からの推定であり、厳密な区間ではない。

`sead::MethodTreeMgr` / `MethodTreeNode` が毎フレームの呼び出し木だと思われるが、
**これはクラス名からの推測で未検証**（F-100）。

**`sead::PrimitiveDrawer`**(vtbl `0x8FEDF4`) は即時モードの図形描画とみられ、
**自前描画の最有力候補**。
★ただし `0x544E54` は **dtor** であって実装位置ではない（F-100）。描画メソッドは未特定。

ACNL の描画は **NintendoWare for CTR (nw4c)** で組まれている。
RTTI の全クラス名（F-53、2,895 件）から名前空間を集計して確定した。

| 層 | 名前空間 | クラス数 | 役割 |
|---|---|---|---|
| ゲーム側 3D ラッパ | `g3d::` | 29 | `SkeletalModel` `Camera` `Fog` `FragmentLight` など |
| シーングラフ / 3D | **`nw::gfx::`** | **63** | `RenderContext` `MeshRenderer` `Material` `ShaderProgram` |
| 2D レイアウト | `nw::lyt::` | 15 | `Drawer` `Picture` `TextBox` `Material` `DrawInfo` |
| **フォント** | **`nw::font::`** | **7** | `RectDrawer` `Font` `ResFont` `PairFont` |
| アニメ | `nw::anim::` | 11 | `AnimBlendOp*` `AnimFrameController` |
| ヒープ | `nw::ut::` | 3 | `HeapBase` `FrameHeap` |
| UI 部品 | `gui::` / `lyt::` | 29 / 16 | ゲーム独自のウィジェット・テキスト領域 |

`nn::gr` は **RTTI 0 件**。仮想関数を持たない静的 API なので、
クラス名からは辿れず、IPC ヘッダなど別の手掛かりが必要（後述）。

### RTTI で実測した継承（F-98）

| 派生 | 基底 |
|---|---|
| **`nw::lyt::Drawer`** | **`nw::font::RectDrawer`** |
| `nw::lyt::Picture` / `TextBox` | `nw::lyt::Pane` |
| `nw::gfx::MeshRenderer` | `nw::gfx::GfxObject` |

★**2D レイアウト描画はフォントの矩形描画を土台にしている。**
テクスチャ描画とテキスト描画は下地を共有するので、片方が分かればもう片方も近い。

### 目的別の入口

| やりたいこと | 見るべきクラス |
|---|---|
| テキスト描画 | `nw::font::RectDrawer`(vtbl `0x8FC974`) / `Font`(`0x8FCA3C`) / `ResFont`(`0x8FCAAC`) |
| テクスチャ・2D | `nw::lyt::Drawer`(`0x8FBF04`) / `Picture`(`0x8FBFFC`) / `Material`(`0x8FC18C`) |
| 3D オブジェクト | `nw::gfx::MeshRenderer`(`0x8FB6F0`) / `RenderContext`(`0x8FB828`) / `Model`(`0x8FBD00`) |

### コードの所在

| 範囲 | 内容 |
|---|---|
| `0x124000`-`0x137000` | GSP セッション / IPC スタブ（下記） |
| `0x48D000`-`0x4D8000` | nw4c 描画ライブラリ（dtor 分布からの推定区間） |

**★注意 (F-100 で訂正)**: 下記は **vtable の `[0]` = デストラクタ**のアドレスであって、
「クラスの実装位置」ではない。クラスの実体メソッドは非仮想のものが多く、別途探す必要がある。

- `nw::gfx::RenderContext` の dtor … `0x496134`
- `nw::gfx::MeshRenderer` の dtor … `0x48D714`
- `nw::font::RectDrawer` の dtor … `0x4D7418` / `nw::lyt::Drawer` の dtor … `0x4D7414`

これらから推した「nw4c 本体は `0x48D000`-`0x4D8000`」も
**dtor の分布からの推定**であって厳密な区間ではない。

---

## GSP（GPU サービス）IPC スタブ（F-94）

すべて 3DS 標準の IPC 形。**実機の TLS 経由**で GSP に投げる。

```
tls = MRC p15,0,Rd,c13,c0,3   (TPIDRURO) + 0x80
tls[0] = <IPC ヘッダ>
...
SVC 0x32                       (svcSendSyncRequest)
```

| addr | 名前 | IPC ヘッダ | 呼び出し元 |
|---|---|---|---|
| `0x13149C` | `GSPGPU_WriteHWRegs` | `0x00010082` | `sub_12AAD0` |
| `0x1315B0` | `GSPGPU_WriteHWRegsWithMask` | `0x00020084` | `sub_12ABF4` |
| `0x131550` | `GSPGPU_SetLcdForceBlack` | `0x000B0040` | `sub_1247C0`, `sub_131190` |
| `0x1314E4` | `GSPGPU_AcquireRight` | `0x00160042` | `sub_12A9C8`, `sub_12AB10` |
| `0x137258` | `GSPGPU_RegisterInterruptRelayQueue` | `0x00130042` | `sub_131228` |
| **`0x13B6A4`** | **`GSPGPU_FlushDataCache`** | `0x00080082` | `sub_136ED8` |

`GSPGPU_WriteHWRegs(pHandle, regAddr, data, size)`:
`tls[3] = (size << 14) | 2` が静的バッファ記述子。

**★`GSPGPU_FlushDataCache` は自前でコマンド列やテクスチャを作るときに必須。**
GPU に渡すメモリは書いた後にこれでフラッシュしないと反映されない。

confidence **HIGH**。検証は 2 段構え（F-100）:

1. 6 本とも `MRC p15`（TPIDRURO）+ `SVC 0x32` + 該当ヘッダ定数をリテラルプールに持つ
2. **IPC ヘッダを形式で分解して引数個数と突き合わせた**
   （`cmd<<16 | normal<<6 | translate`）
   - `0x00010082` → normal 2 / translate 2 = `tls[1],tls[2]` + 静的バッファ記述子 `tls[3],tls[4]` ✓
   - `0x00080082` → normal 2 / translate 2 = addr,size + ハンドル記述子 `tls[3]=0`,handle ✓

API 名と署名は `REFERENCES/CTRPF PROJECTS/FOXXY/Includes/ctrulib/services/gspgpu.h` で照合。

---

## GPU コマンドの生成（F-95）

### ★`g_GpuCmdPtr`(`0x96EA94`) がコマンドバッファの書き込み位置

描画コードは**インラインで**ここに `(値, ヘッダ)` の 8 バイト対を積み、
ポインタを進める。専用の「AddCommand 関数」は無く、各所で直接書いている。

（疑似C を省略。原本は _local/legacy-src/…）

### ヘッダの形式

```
header = reg | (mask << 16) | (extra << 20) | (consec << 31)
```

実際に観測したもの（**`registers.h` で検証済み**、F-99）:

| 十進 | 16 進 | mask | reg | 名前 |
|---|---|---|---|---|
| 65679 | `0x0001008F` | 0x1 | `0x08F` | `GPUREG_LIGHTING_ENABLE0` |
| 65990 | `0x000101C6` | 0x1 | `0x1C6` | `GPUREG_LIGHTING_ENABLE1` |
| 65760 | `0x000100E0` | 0x1 | `0x0E0` | `GPUREG_TEXENV_UPDATE_BUFFER` |
| 65865 | `0x00010149` | 0x1 | `0x149` | `GPUREG_LIGHT0_CONFIG`（`+16*i` でライト別） |
| 983491 | `0x000F01C3` | 0xF | `0x1C3` | `GPUREG_LIGHTING_CONFIG0` |
| 262596 | `0x000401C4` | 0x4 | `0x1C4` | `GPUREG_LIGHTING_CONFIG1` |
| 131333 | `0x00020105` | 0x2 | `0x105` | `GPUREG_STENCIL_TEST` |
| 131335 | `0x00020107` | 0x2 | `0x107` | `GPUREG_DEPTH_COLOR_MASK` |
| 65645 | `0x0001006D` | 0x1 | `0x06D` | `GPUREG_DEPTHMAP_ENABLE` |
| 327808 | `0x00050080` | 0x5 | `0x080` | `GPUREG_TEXUNIT_CONFIG` |
| 983744 | `0x000F02C0` | 0xF | `0x2C0` | `GPUREG_VSH_FLOATUNIFORM_CONFIG` |
| 12518081 | `0x00BF02C1` | 0xF | `0x2C1` | `GPUREG_VSH_FLOATUNIFORM_DATA`（extra=11） |

★`SimpleMaterialActivator` が積むのは**主にフラグメントライティングの設定**。

**★`mask` は `0xF` とは限らず、部分マスク（1/2/4/5/8）が主流。**
**★`extra` は後続の追加ワード数**（一括転送に使う。`sub_148E94` がその形）。

### レジスタ名の内部整合性チェック（F-101）

`registers.h` は `REFERENCES/` 配下＝一次情報ではないので、
**ゲーム側のコードとの整合で裏を取った**:

| reg / 名前 | 整合する観測 |
|---|---|
| `0x149` `GPUREG_LIGHT0_CONFIG` | コードが `16 * i + 65865` と **`0x10` 刻み**で書く＝ライト別ブロックの先頭と一致 |
| `0x010` `GPUREG_FINALIZE` | 提出直前の**最後の 1 命令**として `0x12345678` を書く |
| `0x111` / `0x110` FLUSH / INVALIDATE | FINALIZE の直前に値 1 で連続して書かれる |
| `0x2C0` / `0x2C1` VSH uniform CONFIG / DATA | CONFIG の直後に DATA を `extra=0xB` の一括転送で書き、値の bit31（連続書き込み）も立つ |

**名前そのものは依然 `REFERENCES` 由来だが、使われ方は矛盾しない。**

### ★レジスタ名は必ず資料で引く

`REFERENCES/CTRPF PROJECTS/FOXXY/Includes/ctrulib/gpu/registers.h`
に **724 個の `GPUREG_*` 定義**がある。**記憶で名付けないこと。**
F-99 でこれを怠って 3 件間違えた。

### 補助プリミティブ

| addr | 名前 | 役割 |
|---|---|---|
| `0x1280B4` | `GpuCmd_Advance(bytes)` | `g_GpuCmdPtr += bytes` して返す |
| `0x14E8B4` | `Copy24Bytes(dst, src)` | 6 dword = 24 (0x18) バイト = コマンド 3 組を一括で積む |
| `0x12EC54` | （未命名） | ブロック転送。LUT など大きい塊に使う |

### `nn::gr` 相当の所在

`g_GpuCmdPtr` の参照元から、GPU コマンド層は
**`0x1216BC`-`0x128248`** と **`0x134D28`** に集中している。

| addr | サイズ | 備考 |
|---|---|---|
| `0x1216BC` | `0x158` | |
| `0x121988` | `0xD4` | |
| `0x121E2C` | `0xCA4` | 大きい。状態更新かフラッシュの本命 |
| `0x127D98` | `0x130` | |
| `0x127EDC` | `0x1C0` | |
| `0x1280CC` | `0x178` | |
| `0x134D28` | `0x800` | |

### ★読み方の実例として最適な関数

`nwgfx_SimpleMaterialActivator_Activate`(`0x4A17B8`)。
マテリアルの差分を見ながらコマンドを積む。
`a2+256`〜`a2+296` に前回の各状態 ID を保存し、変化が無ければ積まない
（**差分更新**なので、毎フレーム全部を積んでいるわけではない）。

---

## コマンドリストの終端と提出（F-96）

### 全体の流れ

```
描画コード
   ↓ g_GpuCmdPtr に (値, ヘッダ) の 8B 対をインラインで積む
GpuCmd_SplitAndSubmit (0x1280CC)
   ↓ 終端コマンドを付けて 28 (0x1C) バイトの GX キューに type=1 を積む
GxQueue_Dispatch (0x12E7D8)
   ↓ entry[0] の型で振り分け
GX_SetCommandList (0x136F0C) ほか
   ↓ 0x20B の GX コマンドを GSP 共有メモリへ
sub_13B5AC → GSP
```

### `GpuCmd_SplitAndSubmit`(`0x1280CC`)

コマンドリストを閉じる関数。**自前のコマンドを割り込ませるならこれより前に積む。**

末尾に必ずこの 4 つを積む:

| 値 | ヘッダ | reg | 意味 |
|---|---|---|---|
| 0 | `0x0008025E` | `0x25E` | `GPUREG_PRIMITIVE_CONFIG` |
| 1 | `0x000F0111` | `0x111` | `GPUREG_FRAMEBUFFER_FLUSH` |
| 1 | `0x000F0110` | `0x110` | `GPUREG_FRAMEBUFFER_INVALIDATE` |
| **`0x12345678`** | `0x000F0010` | `0x010` | **`GPUREG_FINALIZE`** |

`0x12345678` → reg `0x010` は 3DS 標準の終端。

各書き込みは `g_GpuCmdPtr < g_GpuCmdEnd`(`0x96EA98`) の境界検査つき。

**★`g_GpuCmdEnd` は固定値ではない（F-102 で実機確認）。**
二重バッファのスワップに追随して変わる。`mgr[1] + mgr[2]` と常に一致する。
**自前で足すときもこの上限を超えないこと。**

### GX キュー（1 エントリ = 28 (0x1C) バイト）

`g_GpuCmdListMgr`(`0xAD995C`) が管理オブジェクトへのポインタ。

| 添字 | 意味 |
|---|---|
| `[1]` | バッファ基底 |
| `[3]` | 現在オフセット |
| `[5]` | 前回提出済みオフセット |
| `[6]` | GX キューの基底（28 (0x1C) バイト × N） |
| `[8]` | 積んだ数 |
| `[9]` | `GxQueue_Dispatch` の処理カーソル |
| `[10]` | 同ループの上限計算と id 524/525 の参照インデックス（役割未確定） |

### ★GX API 一式（`GxQueue_Dispatch` の switch）

| type | addr | 名前 | 用途 |
|---|---|---|---|
| 0 | `0x13594C` | `GX_RequestDma` | DMA 転送 |
| 1 | `0x136F0C` | **`GX_SetCommandList`** | コマンドリスト実行 |
| 2 | `0x135980` | **`GX_SetMemoryFill`** | **バッファのクリア** |
| 3 | `0x135960` | **`GX_SetDisplayTransfer`** | **フレームバッファ転送・形式変換** |
| 4 | `0x1359A0` | **`GX_SetTextureCopy`** | **テクスチャ転送** |

★**5 本すべて impl 側の type バイトを直接確認済み。全て confidence HIGH**（F-100）。

| type | 公開関数 | impl | 確認した命令 |
|---|---|---|---|
| 0 | `0x13594C` | `0x136D88` | `MOV R12,#0` → `STRB R12,[SP]` |
| 1 | `0x136F0C` | — | （疑似C を省略。原本は _local/legacy-src/…）（flush 時 5） |
| 2 | `0x135980` | `0x136E68` | （疑似C を省略。原本は _local/legacy-src/…） |
| 3 | `0x135960` | `0x137198` | （疑似C を省略。原本は _local/legacy-src/…） |
| 4 | `0x1359A0` | `0x136FDC` | `MOV R12,#4` → `STRB R12,[SP]` |

GX コマンドは **0x20 バイト = `u32 x 8`**
（ctrulib `gspgpu.h` の `gspSubmitGxCommand(u32*, u32 gxCommand[0x8])` と一致）。

`GX_SetMemoryFill` は ctrulib の
`GX_MemoryFill(buf0a, buf0v, buf0e, ctrl0, buf1a, buf1v, buf1e, ctrl1)` に対応。

---

---

## 実機で観測した実際の値と 1 フレームの構成（F-102 / F-103）

### コマンドバッファの実測値

| addr | 名前 | 実機の値（ある瞬間） |
|---|---|---|
| `0x96EA94` | `g_GpuCmdPtr` | `0x323CE870` |
| `0x96EA98` | `g_GpuCmdEnd` | `0x324B2130` |
| `0xAD995C` | `g_GpuCmdListMgr` | `0x323B20D0`（id=2） |
| `0xAD9960` | 処理中のマネージャ | `0x3229D06C`（id=1） |

いずれも `0x32xxxxxx` = linear heap 帯。

**恒等式が成立する（偶然では起きない）:**

```
mgr[1] + mgr[3] = g_GpuCmdPtr
mgr[1] + mgr[2] = g_GpuCmdEnd      mgr[2] = 0x100000 (1MB)
mgr[6]          = mgr[1] + mgr[2]  ＝バッファ直後に GX キュー
```

### ★二重バッファはフレームごとに入れ替わる

`g_GpuCmdListMgr` と `dword_AD9960` の**入れ替わりを直接観測した**:

| | `g_GpuCmdListMgr` | `dword_AD9960` |
|---|---|---|
| 1 回目 | `0x323B20D0` (id=2) | `0x3229D06C` (id=1) |
| 2 回目 | `0x3229D06C` (id=1) | `0x323B20D0` (id=2) |

`sead::DoubleCmdGameFrameworkCtrNw4c` の「DoubleCmd」の実体。

### 1 フレームあたりの実測量

- コマンド量 ≈ `0x1BC80` バイト（113,280）
- バッファ 1MB のうち**空きは約 900KB**
- GX キューのエントリ数は **12（`0xC`）**

### ★1 フレームの GX 構成

```
[0]  SetCommandList  mgr[1], size 0x20        フレーム冒頭の定型
[1]  MemoryFill      0x1F181200 (VRAM)        クリア
[2,4,6,8,10] SetCommandList                   バッファ内の断片
[3,7] SetCommandList 0x32677600 size 0x26070  ★バッファ外の固定リスト
[5,9,11] DisplayTransfer  VRAM -> linear heap 上画面(左右)+下画面と推定(LOW)
```

- **`MemoryFill` の宛先は VRAM** → フレームバッファのクリア
- **`DisplayTransfer` は VRAM → linear heap** → 描画結果を表示用へ運ぶ
- `[3][7]` は毎フレーム同じアドレス・サイズなので**事前に構築された固定コマンドリスト**

### 観測方法（CLAUDE.md 準拠）

GX 関数は毎フレーム 12 回 ≈ 秒 700 回超。
**キューの中身はメモリから直接読める**ので、この用途に breakpoint は不要。
**「誰が呼んだか」を知りたいときだけ breakpoint を使う**（F-104）。

## ★自前でコマンドを積む定石（F-97）

`GpuCmd_GetProperty`(`0x127EDC`) は **予約ではなく getter**。
`id = 512 (0x200) + case` で各種値を返す。**`520` (0x208) が `g_GpuCmdPtr`。**
※ id は十進表記（逆コンパイラの出力どおり）。

| id | 返すもの |
|---|---|
| 514 | 現在オフセット（`mgr[3]` も更新） |
| 515 | GX キューに積んだ数 |
| 518 | バッファ基底 |
| **520** | **`g_GpuCmdPtr`（現在の書き込み位置）** |
| 522 | `mgr[10]`（役割未確定。`mgr[9]` とは別物） |
| 523 | GX キュー基底 |
| 524 | 現エントリの型（`784` + type。784 = 0x310） |

ゲーム自身が使っている追加手順:

（疑似C を省略。原本は _local/legacy-src/…）

実例は `sub_4DE7F4`(`0x4DE7F4`) と `sub_15504C`(`0x15504C`)。

**注意点**

- `g_GpuCmdEnd`(`0x96EA98`) を超えないこと（ゲーム側も毎回検査している）
- 積むなら `GpuCmd_SplitAndSubmit`(`0x1280CC`) が走る**前**
- GPU に見せるメモリは `GSPGPU_FlushDataCache`(`0x13B6A4`) が必要

---

---

## ★1 フレームの描画（F-113）

confidence **HIGH**（静的＋実機の `LR` / スタックで連鎖を確認）。

（疑似C を省略。原本は _local/legacy-src/…）

**★登録は 3 つのシーン描画の前に 1 回だけ走る。ここが自前描画を差し込む場所。**

**★実行順は実機で確認済み (F-115)。** `Frame_DrawPass1040` の入口で
`ctx[0]` に 24 件・`ctx[2]` に影ノードが載ったままだった（＝ 1024 が先）。
両者は `MethodTree_WalkAndInvoke`(`0x543C48`) から呼ばれる
（bp ヒット時 `LR = 0x543C6C`）。

### `1024` / `1040` の正体

`Render_DrawSceneIndexed` の `if (a1 == 1024)` は**この 2 パスを区別する門**。
`1024` のパスだけが `Scene_DrawLayers` とコマンド提出を行い、`1040` は末尾処理のみ。
呼び出し元はこの 2 関数だけで、`1025` は現れない。
**2 パスが上画面 / 下画面に対応するかは未確認**（TODO-70）。

### `Base` オブジェクトの走査

`BaseObj_RunDrawPhase`(`0x51EE50`) が連結リストを毎フレーム回す。

（疑似C を省略。原本は _local/legacy-src/…）

`vc_GETDATA1`(`0x51EE40`) は CTRPF の作者ラベルで、
実体は **`Base` オブジェクトマネージャのシングルトン取得**。

### `Base` のライフサイクル — 4 フェーズ × (pre, main, post)

`Obj_InvokePmfTriple`(`0x51FF8C`, 旧名 `UiScreen_RunCreateVirtual`) は
`UiScreen` 専用ではなく **Itanium ABI のメンバ関数ポインタ用トランポリン**。
奇数ビット = virtual フラグ、`>>1` = vtable オフセット。
`pre()` が非 0 のときだけ `main()`、最後に必ず `post(result)`。

| フェーズ | vtable slot (pre/main/post) | 起動関数 |
|---|---|---|
| A（生成） | 2 / 3 / 4 | `BaseObj_InvokeCreateTriple`(`0x520010`) |
| B | 5 / 6 / 7 | `BaseObj_InvokePhaseBTriple`(`0x520040`) |
| C | 8 / 9 / 10 | `BaseObj_InvokePhaseCTriple`(`0x520080`) |
| **D（描画）** | **11 / 12 / 13** | `BaseObj_InvokeDrawTriple`(`0x520A58`) |

---

## ★★描画コールバックが積むもの（F-114）— 自前描画の手本

confidence **HIGH**（静的＋実機のメモリ直読み。レジスタ名は `registers.h` で照合）。

`BsShadowViewMgr_DrawCallback`(`0x28E89C`) は**実機で観測できた唯一の
`FuncNode` コールバック**（1 部屋・1 瞬間の観測。他にいないとは言えない — F-115）。
3 段構成になっている。

（疑似C を省略。原本は _local/legacy-src/…）

| 段 | 内容 | 実機の量 |
|---|---|---|
| ① 既製ブロック | シェーダとパイプライン設定を丸ごと `memcpy`（`Mem_CopyBytes` `0x12EC54`） | **1032 dword = 4128 バイト** |
| ② 可変部 | 影ごとの「色＋アルファ」と「行列」だけ | 可変 |
| ③ 後始末 | 頂点属性の完全リセット | 114 dword = 456 バイト |

### ① 既製ブロック（実機 `0x308950D4` を PICA ストリームとして解析）

| 位置 | reg | 名前 | 内容 |
|---|---|---|---|
| `@82` | `0x2CB` | `VSH_CODETRANSFER_CONFIG` | — |
| `@84` `@214` `@344` `@474` | `0x2CC` | `VSH_CODETRANSFER_DATA` | 128+128+128+97 = **481 命令のシェーダ本体** |
| `@572` | `0x2BF` | `VSH_CODETRANSFER_END` | `1` |
| `@576` | `0x2D6` | オペランド記述子 | 82 ワード |
| `@660`-`@672` | `0x2C0` | `VSH_FLOATUNIFORM_CONFIG` | uniform `0x5D`/`0x5E`/`0x5F`（f24） |
| `@678` | `0x2B0` | `VSH_BOOLUNIFORM` | `0x7FFF1201` |
| `@690` | `0x2BA` | `VSH_ENTRYPOINT` | `0x7FFF01D8` |
| `@692` | `0x2BD` | `VSH_OUTMAP_MASK` | `0x1F` |
| `@702`-`@720` | `0x04F`-`0x06F` | シェーダ出力マップ | — |
| `@722` | `0x2C0` | `VSH_FLOATUNIFORM_CONFIG` | `0x80000000`（f32, index 0） |

**★ゲームは「毎フレーム変わらない設定」を作り置きして `memcpy` している。**

`0xEAD0FEAD`（sead の未使用メモリ埋め）が 77 dword 現れるが、**すべて `mask = 0` の
バーストのパラメータ部**に収まる。`mask = 0` は何も書かないので無害。
**この一致がストリーム解釈の裏付けになった**（(value, header) のペア前提で読むと崩れる）。

### ② 可変部で書くのは 2 つだけ

**色＋アルファ**（(value, header) を 1 組）

```
value  = (*(u32*)(this+38) & 0xFFFFFF) | (alpha << 24)
header = (*(u16*)(this+42) + 3) | 0x000F0000
```

実機 `*(u16*)(this+42) = 0x00C0` → **reg `0x0C3` = `GPUREG_TEXENV0_COLOR`**。
色は TexEnv0 の定数色に入り、アルファはその最上位バイト。

**行列** — 事前計算済みなら 16 dword をコピー、そうでなければ
`0x000F02C0`（`VSH_FLOATUNIFORM_CONFIG`, f32）+
`0x00BF02C1`（`VSH_FLOATUNIFORM_DATA`, extra 11 = 12 ワード = 3×4 行列）。

### ③ 後始末 — 頂点属性の完全リセット

```
q[0]=0, q[1]=0x000F0201     ATTRIBBUFFERS_FORMAT_LOW  = 0
q[2]=0, q[3]=0x000F0202     ATTRIBBUFFERS_FORMAT_HIGH = 0
Mem_ZeroFill(q+4, 0x98)     38 dword を 0 埋め
q[5] = 0x823F0203           reg 0x203 mask 0xF extra 35 consec 1
                            → 属性バッファ 12 本 × 3 reg を全部 0 に
12 回（6 dword/回）:
    w0 = i, w1 = 0x803F0232  reg 0x232 mask 0xF extra 3 consec 1
                             → FIXEDATTRIB_INDEX = i、DATA0/1/2 = 0
    w2..w5 = 0
```

`4 + 38 + 72 = 114` dword = 456 バイト = `0x1C8`。

**★訂正 (F-114):** F-109 でこれを「頂点属性バッファの設定」と書いたが、
**方向が逆で実際はリセット**。自前描画でも同じ後始末をしないと後続の描画を壊す。

### ★自前描画の設計

1. 固定設定は**事前に 1 本のブロックとして作り、コールバックでは `Mem_Copy` だけ**
2. 毎フレーム変わる値だけを `(value, header)` で直接書く
3. **最後に頂点属性をリセットする**（③ をそのまま真似る）
4. `GpuCmd_Advance` には**基点からの総バイト数**を渡す（4 バイト境界に丸める）

### 補助関数

| address | 名前 | 内容 |
|---|---|---|
| `0x12EC54` | `Mem_CopyBytes` | **バイト粒度 memcpy。①で使うのはこちら**（F-115 で訂正） |
| `0x2FBB8C` | `Mem_Copy` | ワード単位 memcpy（LDM/STM 0x20 バイト＋PLD）。②の中で使う |
| `0x2F8370` | `Mem_WordFill` | ワード単位 memset |
| `0x2F836C` | `Mem_ZeroFill` | `Mem_WordFill(dst, bytes, 0)` |

---

## ★実例 — `BsShadowViewMgr`（F-113）

**自前描画を入れるときの手本。** 実機で動いている唯一の `FuncNode` の持ち主。

`BsShadowViewMgr : Base`（`vtbl` `0x8EAA30` / `ti` `0x8C52D4` / 基底 `ti_Base` `0x8C6540`）

（疑似C を省略。原本は _local/legacy-src/…）

**`sceneIndex` がオブジェクトのフィールドから来ているのが要点。**

実機で確認した値（`g_BsShadowViewMgr` = `0x94A5BC`）:

| 読んだもの | 値 |
|---|---|
| `g_BsShadowViewMgr` | `0x3309C334`（= コールバックの `userdata`） |
| `*(this + 172)`（holder の node） | `0x30896104`（`ctx[2]` の配列 #0 にいたもの） |
| `*(this + 197)` | `3`（部屋カテゴリ） |
| `*(this + 200)` | `2`（sceneIndex） |

### ★これを真似る最短の形

既存の `Base` オブジェクトの slot 12 をフックし、
`Scene_SubmitNode` の直後に自前 holder をもう 1 回 submit する。
**新しい `Base` オブジェクトを作らずに 1 ノード足せる。**

---

## ★シーンへの登録経路（F-111）— ノードはどうやって描画対象になるか

confidence **HIGH**（静的解析と実機観測の双方で一致。F-112 で検証済み）。

### 登場人物

| もの | アドレス | 正体 |
|---|---|---|
| `g_SceneContexts[3]` | `0x9C3098` | `nw::gfx::SceneContext` × 3 |
| `g_SceneTraversers[3]` | `0x9C30A4` | `nw::gfx::SceneTraverser` × 3 |
| `g_GfxAllocator` | `0x94CA30` | グラフィクス用アロケータ |

いずれも `Render_InitGlobal`(`0x4E97CC`) が起動時に生成する。

### `nw::gfx::SceneContext` のレイアウト

デストラクタ(`0x48FD6C`)と `Scene_ResetAllContexts`(`0x4EA414`) の
**両方から独立に同じ形が読める**。

```
+0x00  vtable
+0x04  ?
+0x08 + 0x10*n   配列 n = { allocator, begin, end, flags|capacity }   n = 0..14（15 本）
                 ★4 番目は 上位2bit = フラグ / 下位30bit = capacity（F-115 で訂正）
```

| 配列 | begin / end | 埋め手（visitor slot） | 用途 | 確度 |
|---|---|---|---|---|
| #0 | `+0x0C` / `+0x10` | **全 6 本** | **★描画対象ノード。`Scene_DrawLayers` が回すのはここ**。容量 1024 | HIGH |
| #1 | `+0x1C` / `+0x20` | `vtbl[5]` `0x49909C` | 未確定 | MEDIUM |
| #2 | `+0x2C` / `+0x30` | `vtbl[6]` `0x498800`, `vtbl[7]` `0x498F20` | 未確定 | MEDIUM |
| #3 | `+0x3C` / `+0x40` | `vtbl[7]` `0x498F20` | 未確定 | MEDIUM |
| #4 | `+0x4C` / `+0x50` | `vtbl[8]` `0x498860` | **カメラ** | HIGH |
| #5 | `+0x5C` / `+0x60` | `vtbl[9]` `0x499518` | 未確定。`Render_DrawSceneIndexed` が `sub_4A41EC` で回す | MEDIUM |
| #7 | `+0x7C` / `+0x80` | 未確認 | `0x9C3088` の 4 オブジェクトへ配る | LOW |
| #9 | `+0x9C` / `+0xA0` | 未確認 | 同上 | LOW |
| #10 | `+0xAC` / `+0xB0` | 未確認 | 同上 | LOW |
| #14 | `+0xEC` / `+0xF0` | `vtbl[6][7][8][9]`（`*(node+40)` が非 0 のとき） | 未確定 | MEDIUM |

**★訂正の履歴:**
F-111 で #5 を「カメラ系」としたのは誤り → カメラは **#4**（F-112）。
F-112 で #5 を「不明」としたが、埋め手は **visitor `vtbl[9]`**（F-115）。

### 経路

```
Scene_SubmitNode(pHolder, sceneIndex)          0x4ED630   ← ★入口。呼び出し元 40+ 件
    node = *(pHolder + 4)
    node->vtbl[4](node, g_SceneTraversers[sceneIndex])
        │
        └─ Accept(node, visitor)                          ← node のクラスごとに実装が違う
               visitor->vtbl[N](visitor, node)            ← ★呼ぶスロットもクラスごとに違う
                   └─ Visit …  ctx = *(visitor + 8)
                                nwut_Array_PushBack(ctx + 8, &node)   ← ★配列 #0 へ
               for (child in [node+0x18, node+0x1C))      ← 子ノード配列（再帰）
                   child->vtbl[4](child, visitor)
```

| ノードのクラス | `Accept` | 呼ぶ visitor スロット |
|---|---|---|
| `SceneNode` / `g3d::FuncNode` | `nwgfx_SceneNode_Accept`(`0x497D28`) | `vtbl[4]`（`+16`）= `0x499080` |
| `nw::gfx::Camera` | `0x4ACE24` | `vtbl[8]`（`+32`）= `0x498860` |

`SceneTraverser` の vtable には Visit が **6 本**ある（`vtbl[4..9]`）。
ノード種別ごとに追加で入る配列が違うが、**どれも配列 #0 には入る**
（F-115 で 6 本すべて確認。F-112 時点では 2 本しか読んでいない一般化だった）。
`Scene_DrawLayers` はそこで型チェックし、`Model` と `FuncNode` だけを処理する
（Camera は素通り）。

そのあと `Scene_DrawLayers(ctx, …)` が配列 #0 を 4 レイヤー分回す。

### ★毎フレーム呼ぶ必要がある

`Render_FrameEnd`(`0x4F1CE4`) がフレーム末に `Scene_ResetAllContexts` を呼び、
`nwgfx_SceneTraverser_BindContext`(`0x499458`) 経由で
**15 本の配列を全部空にする**（`end = begin`）。

`SceneNode` には子配列（`+0x18`/`+0x1C`）があり本物のシーングラフは存在するが、
**ゲーム側はそこに繋がず、毎フレーム直接 `Accept` を呼ぶ使い方をしている。**

### ★実機で確認した値（F-112）

```
g_SceneContexts   = [0x329ABEF0, 0x329B33F0, 0x329BA8F0]   vptr 全て 0x008FB700
g_SceneTraversers = [0x329ABFFC, 0x329B34FC, 0x329BA9FC]   vptr 全て 0x008FB8B0
trv[i] + 8 == ctx[i]   3 組とも一致
配列 #0: alloc = g_GfxAllocator(0x329A4820), cap = 1024
byte_94CA2C = 0
```

`Scene_DrawLayers` 到達時（`R0 = ctx[2]`, `LR = 0x4E97A8`）の配列 #0 は 1 件:

```
node = 0x30896104  vptr = 0x008FCF10 (vtbl_g3d_FuncNode)
vt[4] = 0x00497D28 (nwgfx_SceneNode_Accept)
子ノード 0 件   cb0 = 0   cb1 = 0x0028E89C   ud = 0x3309C334
```

`Scene_SubmitNode` 到達時（`LR = 0x68EA88`）:
`R0 = 0x3309BE28`, `R1 = 0`, `*(R0+4) = 0x329D7B0C`（`nw::gfx::Camera`）。
呼び出し前 `n = 0` → 復帰時 `n = 1`、要素は `0x329D7B0C`。**push を直接確認。**

### sceneIndex と描画関数

| index | 描画する関数 | 条件 |
|---|---|---|
| 0 | `Render_DrawScene0`(`0x4F2334`) → `Render_DrawSceneIndexed(a1, 0)` | `byte_94CA2C == 0` |
| 1 | `Render_DrawScene1`(`0x4EA01C`) → `Render_DrawSceneIndexed(a1, 1)` | `byte_94CA2C == 1` |
| 2 | `Render_DrawScene2`(`0x4E976C`) → `Scene_DrawLayers(g_SceneContexts[2], …)` | **無条件** |

`byte_94CA2C` は `Render_InitGlobal` 末尾で `0` に初期化される。
**0 と 1 は排他のモード切り替えに見えるが意味は未確定**（TODO-65）。
F-109 で実機の `LR` が `0x4E97A8` だったのは **index 2 の経路**。

**★訂正（F-111）:** F-104 で「`sub_4EEDD8` の `1024 / 1025 / 1040` が
シーンを選んでいる」かのように書いたが、シーンを選ぶのは**第 2 引数**であって
`a1` ではない。`a1` は `if (a1 == 1024)` の門にしか使われていない。

---

## ★自前描画をどう実現するか（手段の比較）

**まだどれも実行していない。以下は解析から導いた設計案。**

### 手段 A: `g3d::FuncNode` のコールバックに乗る（F-106）

`Scene_DrawLayers`(`0x4EB840`) は 4 レイヤーでシーンを走査し、
型が `g3d::FuncNode` のノードでは登録された関数を呼ぶ。

型ノードは **クラス自身の vtable slot 2（型ゲッタ）から確定済み**（F-108）:

| 型ノード | クラス |
|---|---|
| `0x94CA60` | `g3d::FuncNode` |
| `0x96F0D4` | `nw::gfx::Model` |
| `0x96F0F0` | `nw::gfx::TransformNode`（両者の親） |

**`Scene_DrawLayers` の呼び出し元は 2 つある**（F-108）:
`sub_4EEDD8`（`if (a1 == 1024)` の内側）と
`sub_4E976C`（別シーンを無条件で描画）。

| offset | 内容 |
|---|---|
| `+0x148` | コールバック（レイヤー 0） |
| `+0x14C` | コールバック（レイヤー 1） |
| `+0x150` | ユーザーデータ |

```c
cb(dword_94CA48 /* 描画コンテキスト */, userdata);
```

生成は `g3d_FuncNode_Create`(`0x4EFFB4`)、サイズ `0x154`、3 つとも 0 で初期化。

**★登録 API も判明（F-107）:**

```c
g3d_FuncNode_Create(&out, allocator);                       // 0x4EFFB4
g3d_FuncNode_SetCallbacks(&out, cb0, cb1, userdata);        // 0x4EFF58
```

最小実例は `sub_1F9A6C`（全 4 行）。

**★シーンへ載せる手順も判明（F-111）。上の「シーンへの登録経路」を参照。**

（疑似C を省略。原本は _local/legacy-src/…）

生成と登録は**別関数に分かれている**のが要点。
ゲーム内の最小ペアは `sub_1F9A6C`（生成）と `sub_1F9BC4`（登録, `sceneIndex = 0`）。

**★実在・常用が確認できた（F-107）。** `g3d_FuncNode_Create` の呼び出し元は
**12 箇所**あり、多様な subsystem に分布している。
型ノード `g_TypeNode_g3d_FuncNode`(`0x94CA60`) を
**書く側（`SetCallbacks`）と読む側（`Scene_DrawLayers`）の両方が参照**しており、
2 経路から裏付けが取れている。

コールバックの中では `g_DrawContext`(`0x94CA48`) を使って実際に描ける
（実例 `sub_188340` はキューのオブジェクトの `vtable+8` をこれで呼んでいる）。

**★実機で確認済み（F-109、confidence `HIGH`）:**

`Scene_DrawLayers` に bp を張って観測した実際のシーン:

```
scene=329BA8F0  ノード数=1
  [0] node=30896220  vptr=008FCF10 (= vtbl_g3d_FuncNode)
       cb0=00000000  cb1=0028E89C  user=3309C334
```

**`vptr` が静的 IDB の vtable と完全一致、オフセットも予測どおり。**

さらに **登録されていた `cb1`（`sub_28E89C`）の中身が
「手段 C の定石」そのものだった**:

（疑似C を省略。原本は _local/legacy-src/…）

積んでいたのは `ATTRIBBUFFERS_FORMAT_LOW/HIGH`、`ATTRIBBUFFER0_OFFSET`、
`FIXEDATTRIB_INDEX` = **頂点属性バッファの設定**。

**つまり手段 A と手段 C は排他ではなく、A の中で C を使うのが正規の形。**

- **利点**: ゲームが用意した正規の拡張点。描画コンテキストが引数で渡る。
  **前例が 12 件あり、実機で動作を確認済み**
- **欠点**: ノードをシーンに登録する手順が未解明（TODO-60）
- **これを第一候補とする。**

### 手段 B: `GpuCmd_SelectList` で別リストに描く（F-104）

`sub_4EEDD8` が実演している型:

（疑似C を省略。原本は _local/legacy-src/…）

- **利点**: ゲーム自身が使っている手順なので確実性が高い
- **欠点**: 別リストの確保が必要。切り替え中に他の描画が走ると壊れる

### 手段 C: `g_GpuCmdPtr` に直接積む（F-97）

（疑似C を省略。原本は _local/legacy-src/…）

- **利点**: 最も低レベルで自由度が高い
- **欠点**: **`g_GpuCmdPtr` / `g_GpuCmdEnd` は毎フレーム変わる**（F-102 で実測）。
  キャッシュするとスワップ後に別バッファを壊す。
  GPU の状態（シェーダ・テクスチャ・行列）を自分で全部積む必要があり、
  ゲーム側の差分更新（`SimpleMaterialActivator` は前回状態を覚えている）と
  食い違うと以後の描画が壊れる

### 手段 D: 別バッファを `GX_SetCommandList` で流す（F-103）

実機観測で、ゲーム自身がバッファ外の固定コマンドリスト
（`0x32677600`、`0x26070` バイト）を毎フレーム 2 回提出していた。

- **利点**: 事前に組んだコマンド列を丸ごと流せる。前例がある
- **欠点**: いつ提出するかのフックが別途必要

### 共通の注意点

- **GPU に渡すメモリは `GSPGPU_FlushDataCache`(`0x13B6A4`) が必要**
- 空きは 1MB 中 約 900KB（F-102 実測）なので容量の余裕はある
- 積むなら `GpuCmd_SplitAndSubmit`(`0x1280CC`) が走る**前**

### 次に確かめるべきこと

1. `g3d_FuncNode_Create` の呼び出し元（実際に使われているか）— TODO-55
2. `dword_94CA48`（描画コンテキスト）の実体 — TODO-56
3. 4 レイヤーの意味 — TODO-58

---

## 分かっていないこと
- `GSPGPU::SetBufferSwap`(`0x00050200`) / `TriggerCmdReqQueue`(`0x000C0000`) の
  スタブが見つかっていない。GX コマンドキュー（GSP 共有メモリ）経由と思われるが未確認
- **毎フレームの描画ループの入口**（依然未特定）。判明している範囲:
  - **実機で `GpuCmd_SplitAndSubmit` の呼び出し元を捕捉 → `sub_4EEDD8`**（F-104）。
    これは「別コマンドリストへ切り替えて描くパス」で、その本体が
    `Scene_DrawLayers`(`0x4EB840`)（F-106）
  - `sub_11CE64` は **sead のグラフィクス初期化**だった（F-98 で否定済み）
  - `sub_16A130` → `sub_15504C` → `sub_1534A8` → `sub_4DE7F4` の鎖は未確定。
    近所の `sub_14A9C8` が YUV→RGB なので
    **`0x153000`-`0x176000` は画像コーデック側の疑いが残る**
  - 枠組みは `sead::UlcdDoubleCmdGameFrameworkCtrNw4c`(vtbl `0x8FFC74`) のはずだが、
    実インスタンスの確認は未了（TODO-44）
- `nw::font` / `nw::lyt` / `nw::gfx` それぞれの実際の描画関数
- **`g3d::FuncNode` が実際に使われているか**（TODO-55）。
  使われていれば自前描画の第一候補になる
- `dword_94CA48`（描画コンテキスト）の実体（TODO-56）
- 4 レイヤーの意味（TODO-58）

---

## 解析上の落とし穴

- **★前回「静的な PICA コマンドヘッダは 0 件」と書いたのは走査バグだった (F-95)。**
  条件を `(w & 0xFFF00000) == 0x000F0000` と書いたが、`0x000F0000` の立っている
  ビットは 16-19 で上位 12 ビットのマスクに掛からず、**恒偽**だった。
  正しく `(w >> 16) == 0x000F` で引くと 1192 件出る。
  ただしそれらは `0x001Fxxxx` のアドレス列や `0x015F015F` の埋め値が大半で、
  **結論（静的なコマンド列は無い＝実行時生成）自体は変わらない。**
  さらに実際の mask は 0xF に限らないので、この走査手法自体が筋が悪い。
- **定数走査は偽陽性を出す。** `sub_14A9C8`(`0x14A9C8`) は
  `TriggerCmdReqQueue`(`0x000C0000`) の一致で GSP 関数に見えたが、
  中身は **YUV→RGB 変換**（`QADD16`/`USAT16`、係数 11277/29033）だった。
  直後の `dword_14AAE4` がたまたまその値を持つデータ表。
  **定数が一致しただけで断定せず、必ず中身を読むこと。**
- IPC スタブのヘッダ定数は**関数本体の直後のリテラルプール**にある
  （例: `0x13149C` + `0x44` = `0x1314E0`）。関数サイズだけ走査すると取り逃す。

---

# ★★自前描画の作り方（F-116 〜 F-121、実機で到達済み）

**この節だけ読めば自前描画を再現できる。** 出典は `RE/FINDINGS.md` F-116〜F-121。
すべて実機で確認済み（confidence **HIGH**）。

## 到達点

| できること | 根拠 |
|---|---|
| 任意のシーンへノードを追加する | F-116（`ctx[1] n=1`） |
| 何個でも追加する（8 個で確認） | F-117（`ctx[2] n=8`） |
| **自前の `FuncNode` を生成する** | F-119（`vptr = vtbl_g3d_FuncNode`） |
| **自前コールバックを毎フレーム呼ばせる** | F-119（約 31fps で呼ばれる） |
| **自前コールバックから GPU コマンドを積む** | F-120 |
| **その結果を画面に出す** | F-120（3 条件の対照実験） |
| **積まれたコマンドを解釈して書き換える** | F-121（影を横に 2 倍に伸ばした） |

## レシピ

`PATCHES/cave_own_funcnode.py` が完全な実装。要点だけ書くと:

### 1. フック位置

`BsShadowViewMgr_SubmitToScene`(`0x28FE0C`) の先頭 1 ワードを `B ケーブ` にする。
ここは `Frame_DrawPass1024` の登録フェーズで**毎フレーム 1 回だけ**通る（F-113）。

登録フェーズならどこでもよいが、この関数は
「毎フレーム 1 回」「`this` が使える」「1 ワードで乗っ取れる」ので都合がよい。

### 2. ノードの生成（初回だけ）

```asm
LDR  R5, =HOLDER            ; 8 バイトの領域。+4 にノードが入る
LDR  R0, [R5,#4]
CMP  R0, #0
BNE  skip                   ; 生成済みなら飛ばす
  MOV  R0, R5
  LDR  R1, =&g_GfxAllocator ; 0x94CA30
  LDR  R1, [R1]
  BL   g3d_FuncNode_Create      ; 0x4EFFB4
  MOV  R0, R5
  MOV  R1, #0                   ; cb0（レイヤー 0）
  LDR  R2, =MY_CALLBACK         ; cb1（レイヤー 1）
  MOV  R3, #0                   ; userdata
  BL   g3d_FuncNode_SetCallbacks ; 0x4EFF58
skip:
```

**アロケータは `g_GfxAllocator`(`0x94CA30`) を使う。**
`Render_InitGlobal` が `(*(vtbl+8))(alloc, size, align)` の形で使っており、
`g3d_FuncNode_Create` の要求と同一。グローバルなので寿命が長い。

### 3. 毎フレームの登録

```asm
MOV  R0, R5
LDR  R1, [R4,#0xC8]         ; sceneIndex（影と同じ 2。0/1 でもよい）
BL   Scene_SubmitNode       ; 0x4ED630
```

**`Render_FrameEnd` が毎フレーム全配列を空にするので、毎フレーム呼ぶ必要がある**（F-111）。

### 4. コールバック

到達時 `R0 = g_DrawContext`, `R1 = userdata`。

```asm
PUSH {R4,LR}
...  好きな処理 ...
POP  {R4,PC}
```

GPU コマンドを積むなら F-97 の定石:

```
GpuCmd_GetProperty(0x208, &p)   ; 0x127EDC。p = 現在の書き込み位置
（p から (value, header) の組を書く）
GpuCmd_Advance(bytes)           ; 0x1280B4。基点からの総バイト数を渡す
```

## シーンの選び方

| sceneIndex | 描画される条件 | 用途 |
|---|---|---|
| 0 | `byte_94CA2C == 0`（既定） | 本編。ここが本命 |
| 1 | `byte_94CA2C == 1` | 現状描画されない。**GPU に触れず登録だけ試すのに安全** |
| 2 | **無条件** | 影が使っている。確実に描かれる |

## ★落とし穴

- **パッチを入れた瞬間のフレームは移行フレーム。**
  プロセスがフレーム途中で止まっていると、その回の登録はパッチ適用前に済んでいる。
  **必ずフル 1 フレーム回してから測ること**（F-116 でこれを誤読した）
- **`uninstall` で `HOLDER` をゼロ埋めすると、生成済みノードが孤児になる**（340 バイト漏れ）。
  `cave_own_funcnode.py` は既存ノードを再利用するようにしてある
- **走行中はデバッガの要求が一切通らない。** `run_timed.py` を使うこと（後述）

## ★実測した描画ステート（自前でパイプラインを組むときの手本）

影の既製ブロック（`*(mgr+0xB4)`、1032 dword = 4128 バイト）は
**59 種類のレジスタ**を設定している。主要なもの:

| レジスタ | 値 | 意味 |
|---|---|---|
| `0x2CB`/`0x2CC`/`0x2BF` | — | 頂点シェーダ **481 命令**の転送 |
| `0x2D5`/`0x2D6` | — | オペランド記述子 82 ワード |
| `0x2BA` `VSH_ENTRYPOINT` | `0x7FFF01D8` | — |
| `0x2BD` `VSH_OUTMAP_MASK` | `0x1F` | — |
| `0x100` `COLOR_OPERATION` | `0x00E40100` | mask 0x3 |
| `0x101` `BLEND_FUNC` | `0x76760000` | **SRC_ALPHA / ONE_MINUS_SRC_ALPHA** |
| `0x104` `FRAGOP_ALPHA_TEST` | `0` | 無効 |
| `0x105` `STENCIL_TEST` | `0xFF00FF10` | 無効 |
| `0x107` `DEPTH_COLOR_MASK` | **`0x00000F40`** | **深度テスト無効・深度書き込み無効**、カラーマスク `0xF` |
| `0x112`/`0x113` | `0xF` | colorbuffer read/write |
| `0x114`/`0x115` | `0` | depthbuffer read/write |

**ブロックはメモリ上の生バッファなので、値を書き換えれば挙動を変えられる。**

## ★1 インスタンスあたりのコマンド構造（F-121）

`BsShadowViewMgr_BuildShadowCmds` が影 1 個につき積む並び:

```
(color)          0x78260000      アルファは最上位バイト
(header)         0x000F00C3      GPUREG_TEXENV0_COLOR
(uniform index)  0x80000019      ★uniform 番号 25、bit31 = f32 モード
(header)         0x000F02C0      VSH_FLOATUNIFORM_CONFIG
(f0)             ...
(header)         0x00BF02C1      VSH_FLOATUNIFORM_DATA  extra 11 = 12 ワード
(f1..f11)        ...
```

**★PICA の f32 uniform は `w, z, y, x` の順で送られる。** 並べ直すと 3×4 行列:

| | x | y | z | w（平行移動） |
|---|---|---|---|---|
| 行0 (c25) | `hdr+12` | `hdr+8` | `hdr+4` | `hdr-4` |
| 行1 (c26) | `hdr+28` | `hdr+24` | `hdr+20` | `hdr+16` |
| 行2 (c27) | `hdr+44` | `hdr+40` | `hdr+36` | `hdr+32` |

実測値の例（`hdr` は `0x00BF02C1` の位置）:

| | x | y | z | w |
|---|---|---|---|---|
| 行0 | 100.0 | 0 | 0 | 2643.0 |
| 行1 | 0 | -0.996 | 6.286 | -486.92 |
| 行2 | 0 | -0.090 | -69.71 | -43.91 |

**この順序を知らずに float 列を行列として読むと成分の意味を取り違える**（F-114 の誤り）。

## ★影はテクスチャ投影（F-121）

行0 の x（拡大縮小）を 2 倍にしたときの実機の見え方:

- 影が横に引き伸ばされ、**位置は変わらない**
- 左に少し傾く（他の行の交差項との釣り合いが崩れて剪断）
- **横に伸びた分、上下からループするように描画される**

**ループするということはテクスチャ参照であり、ラップモードが REPEAT。**
つまりこの 3×4 行列は**サンプリング座標に効く投影行列**。
自前でテクスチャを出したいなら、この参照先を差し替えるのが最短（TODO-85）。

## 検証の作法

- **陰性対照を取る。** 「自前ノードだけ → 影あり」だけでは不十分で、
  「どちらも無し → 影なし」を確かめて初めて確定する（F-120）
- **相対変化を使う。** float の指数部に `±0x00800000` を足すと正確に ×2 / ÷2。
  元の値の大きさを知らなくても安全に試せる
- **ヒット位置を記録する 1 命令**（`STREQ R4,[LASTHDR]`）を仕込めば、
  停止後にいくらでも周辺メモリを読める。トレース用ケーブの最小形
- **視覚での総当たりは往復が高くつく。** メモリから構造を読んで絞り込むほうが速い

---

## ★★★完全自己完結の自前描画（F-122）— 到達点

**ゲームの描画関数を一切呼ばずに画面へ絵を出す最小構成。**
実機で確認済み（自前が積んだ 1 個だけが描かれ、他の影は全部消えた）。

```asm
p = GpuCmd_GetProperty(0x208)                       ; 0x127EDC
Mem_CopyBytes(p,        *(mgr+0xB4), 4128)          ; 0x12EC54  既製ブロック
Mem_CopyBytes(p + 4128, TEMPLATE,     432)          ;           自前テンプレート
GpuCmd_Advance(4560)                                ; 0x1280B4
```

- **既製ブロック 4128B** … シェーダ 481 命令＋パイプライン一式。
  ゲームが `*(g_BsShadowViewMgr+0xB4)` に持つ静的データをコピー元にするだけ
- **自前テンプレート 432B** … カテゴリ設定＋インスタンス描画。**ここが自分の絵**

### テンプレートの構造

**カテゴリ設定**（テクスチャと頂点バッファを決める）

| reg | 値の例 | 何を決めるか |
|---|---|---|
| `0x2B9` / `0x242` | `0xA0000001` / `1` | 頂点属性の本数 |
| `0x200`〜`0x205` | `0x03000000` ほか 5 語 | **頂点バッファ**の基底・書式・オフセット・ストライド |
| `0x082` | `0x00200020` | **テクスチャの大きさ 32×32** |
| `0x083` | `0x00003326` | ラップ／フィルタ |
| `0x085` | `0x0460EC90` | **テクスチャのアドレス**（`<<3` で物理） |
| `0x08E` | `0x0C` | フォーマット |

**インスタンス描画**（1 個の絵を置く。144 バイト）

| reg | 値の例 | 何を決めるか |
|---|---|---|
| `0x0C3` | `0x78260000` | **色**（最上位バイトがアルファ） |
| `0x2C0` / `0x2C1` | `0x80000019` / 12 float | **3×4 行列**（uniform 25、`w,z,y,x` 順） |
| `0x227` / `0x228` | `0x000A4B98` / `6` | **インデックスバッファ** / **頂点 6 個 = 四角形** |
| `0x22F` | `1` | **描画発火** |

**インスタンスブロックを並べれば複数描ける。**

### 実物の取り方

```
1. PATCHES/cave_own_funcnode.py を CB_MODE="scale" / EXP_ADD=0 / KEEP_ORIGINAL=False で設置
2. run_timed.py で 1 回走らせる（P0/P1 が記録される）
3. scratchpad/dump_shadow_cmds.py で P0..P1 をファイルへ吸い出す
4. ローカルで解析し、カテゴリ設定＋好きなインスタンスを切り出して
   scratchpad/own_template.bin に保存
5. CB_MODE="own2" で設置
```

**`KEEP_ORIGINAL=False` にすること。** `True` だとゲーム本来の影が先に走り、
**影インスタンスのリストが消費されて 2 回目は 1 個も描かない**（F-122、TODO-83 の答え）。

### ★はまりどころ

- **ARM の即値は `imm8 ROR (2*r)`。** 自作エンコーダで回転方向を逆にすると
  `MOV R2,#432` が `MOV R2,#27` になる。**F-122 で実際にこれで数時間溶かした。**
  生成した命令は必ず逆アセンブルして目視確認すること
- **テンプレートの行列は捕捉時のカメラ位置に固定。** 移動すると位置がずれる
- **描画は深度テスト無効**（`0x107 = 0x00000F40`）なので、同一パス内で他の物に隠れることはない

---

## ★★★自前の画像を出す（F-123 / F-124）— 当初目標の達成形

### 手順

1. **F-122 の完全自己完結の描画**を動かす（自前ノード＋自前テンプレート）
2. テンプレート内の **2 ワード**を書き換えてフォーマットを変える
3. テクスチャ本体に自作の絵を書き込む

### 2 ワードの書き換え

| reg | 元 | 変更後 | 意味 |
|---|---|---|---|
| `0x083` `TEXUNIT0_PARAM` | `0x00003326` | `0x00003306` | **ETC1 フラグ（bit5）を落とす** |
| `0x08E` `TEXUNIT0_TYPE` | `0x0C`（ETC1） | `0x0A`（`GPU_L4`） | 非圧縮 4bpp に |

`0x083` のビット割り当て:

| ビット | 意味 |
|---|---|
| bit1 / bit2 | 拡大 / 縮小フィルタ（1 = LINEAR） |
| bit5 | ETC1 フラグ |
| bits 8-9 | wrap T（3 = MIRRORED_REPEAT） |
| bits 12-13 | wrap S |

### テクスチャ本体の場所

`0x085 TEXUNIT0_ADDR1` の値を `<<3` すると物理アドレス。
**仮想アドレス = 物理 + `0x10000000`**（実測。他の候補は全て未マップだった）。

大きさは `0x082 TEXUNIT0_DIM`（bits 0-10 = 高さ、bits 16-26 = 幅）。

**★カテゴリごとにテクスチャと寸法が違う。**

| カテゴリ | `0x085` | 物理 | 仮想 | 寸法 | サイズ |
|---|---|---|---|---|---|
| 多数派 | `0x0460EC90` | `0x23076480` | `0x33076480` | 32 × 32 | 512 B |
| 大きい影 | `0x0460FDF0` | `0x2307EF80` | `0x3307EF80` | 32 × 64 | 1024 B |

**テンプレートを作ったら、その中の `0x085`/`0x082` を見て対象を決めること。**

### ★スウィズルを知らずに絵を作る方法

3DS のテクスチャは **8×8 タイル内が Morton スウィズル**されている。
ピクセル単位の絵にはこの順序の解明が要るが、**タイル単位なら中身が一様なので不要。**

```python
# 32×64 L4 のタイル市松模様（1024 バイト）
img = bytearray(1024)
for tile in range(32):            # 4 タイル幅 × 8 タイル高
    tx, ty = tile % 4, tile // 4
    v = 0xFF if (tx + ty) % 2 == 0 else 0x00
    for k in range(32):           # 1 タイル = 64 px × 4bit = 32 バイト
        img[tile * 32 + k] = v
```

**この形で「はっきりした市松模様」が実機に出た。**

### 枠に収まるフォーマット

テクスチャの割り当ては元のサイズのままなので、**bpp を増やすとはみ出す**。

| フォーマット | 値 | bpp | 32×64 | 32×32 |
|---|---|---|---|---|
| `GPU_L4` / `GPU_A4` | `0xA` / `0xB` | 4 | **1024 B** ✔ | **512 B** ✔ |
| `GPU_L8` / `GPU_A8` | `0x7` / `0x8` | 8 | 2048 B ✘ | 1024 B ✘ |
| `GPU_RGBA8` | `0x0` | 32 | 8192 B ✘ | 4096 B ✘ |

**カラーを出すには GPU 可視の大きなバッファを別に確保する必要がある。**

### 道具

| ファイル | 用途 |
|---|---|
| `scratchpad/tex_patch.py` | 32×32 側（`0x33076480`）の保存 / 縞 / 復元 |
| `scratchpad/tex2_patch.py` | 32×64 側（`0x3307EF80`）の保存 / 市松 / 復元 |
| `scratchpad/dump_shadow_cmds.py` | コマンド列の吸い出し |

## UIの2Dテキストとフォント（F-126〜F-131）

`nwlyt_TextBox_SetString`(`0x4BACBC`) を対象箱だけフックすれば、既存UIへ任意の
UTF-16文字列を出せる。実装は `PATCHES/cave_textbox.py`。

主要フィールド:

| offset | 内容 |
|---|---|
| `+40/+44/+48` | translate x/y/z |
| `+72/+76` | pane width/height。**widthはTextWriterの自動折り返し幅になる** |
| `+184` | char[8] ペイン名。`T_`本文、`S_`影、`RT_`/`RS_`は7px版を使用 |
| `+212` | wchar_t* 文字列バッファ |
| `+216/+220` | RGBA文字色（上/下） |
| `+224` | **`nw::font::ResFont*`** |
| `+228/+232` | float フォント幅/高さ |
| `+248/+250` | u16 バッファバイト数 / 現在文字数 |
| `+254` bit0 | 更新フラグ。変更後に立てる |
| `+256` | material*。material `+20` が乗算色 |

TextBox Ctor (`0x4BB2A4`) はリソース `+82` の font index から名前を引き、
ResourceAccessor virtual `+12` の戻り値を `+224` に保存する。

実機で確認した初期化済みCFNU（runtimeアドレスは起動ごとに変わる）:

| 例 | FINF linefeed / metrics | 利用例 |
|---|---|---|
| 通常 | 24 / 24,18,18 | 時計、会話本文、アイテム名、日本語UI |
| 7px | 7 / 7,7,5 | `RT_msg_0` / `RS_msg_0` / megaphone系 |
| 40px | 40 / 40,35,29 | 用途未特定 |
| count | 26 / 26,24,17 | `T_bell_0` / `T_count_` |

フォントの差し替えは TextBox `+224` だけを書き換え、`+254` bit0を立てればよい。
`+228/+232` は独立なので、フォント形状と表示サイズを別々に試験すること。
最小の適用・復元スクリプトは `PATCHES/textbox_font_swap.py`。

実機で時計本文 `T_time_0` のみを通常版から7px版へ変えると、本文 `06` はぼやけた
「あ」状の文字に変化し2行になった。2行目はpane内でclipされたのではなく、そのまま
画面下端の外へ出ている。独立した影は `06` のまま。
したがって `+224` の変更が実描画へ反映されること、本文と影のフォントが独立であることは
目視でも確定した。CMAPを直接確認すると7px版には数字がなく、`0/6/7`はいずれも
`0xFFFF`。`GetGlyph`はalternate glyph 0へ置換し、その逆引きは正確には
`U+3041「ぁ」`だった。したがって2桁が2個の「ぁ」へ置換され、拡大・折り返された。

counter26版なら `07` は1行表示される。本文に黒縁が付き、少し左上へ見えるが、変更は
`+224`だけなのでbuffer容量やpane座標の変化ではない。通常版とcounter版はlinefeed/cell系が
`24 / 24,18,18` 対 `26 / 26,24,17`、数字advanceが12対16。時計要求サイズ
`18 x 24`ではcounter側が横0.75・縦約0.923に縮小されるため、輪郭とbaselineの差が残る。

`nwfont_ResFont_MapCharToGlyph`(`0x743768`) がCMAP method 0/1/2を処理し、
`nwfont_ResFont_GetGlyph`(`0x7438B4`) がalternateとCWDH/TGLPを解決する。
全live ResFontの `+16` は `0x6`。`0x4D7474` は2個のboolをbit2/bit1へ格納して全textureを
再生成する。両方OFFの直接視覚試験では、拡大7px glyphの輪郭がくっきりしたドット表示へ
変化した。したがって拡大/縮小時のLINEAR filter設定と確定し、`0x4D7474` を
`nwfont_ResFont_SetLinearFilter` と命名した（HIGH）。

### 折り返し・縦方向・glyph右端（F-131）

`nwlyt_TextBox_ConfigureTextWriter` (`0x4BAD78`) は `TextBox+72` のpane widthを
`TextWriter+76` のwrap limitへコピーするが、pane heightはコピーしない。
`nwfont_TextWriter_DrawString` (`0x7E7FA4`) はscaled line widthがlimitを超えたときだけ
synthetic newlineを発生させる。縦方向のpane-height比較はない。

時計paneは `26.0 x 21.6`。7px fallback glyphのadvance 7を要求幅18へ拡大すると
1文字18、2文字36となり、`36 > 26` のため2文字目が次行へ回る。改行stepは
`7*(24/7)=24` なのでpane高21.6を越えるが、そのまま描画される。

1文字quadは `nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) が作る。CWDHの
`glyphWidth` がgeometry幅とtexture U右端の双方を決める。7px fallback glyph 0は
`cellWidth=7 / glyphWidth=6 / advance=7` のため、要求幅18では本体15.43px・advance18px。
目視された右端1〜3pxの欠けに見える部分は、この1 source pixel分（約2.57px）の境界と
一致する。文字列bufferやpaneの越境ではない。後続の整数倍率比較（F-132）で症状が改善し、
非整数倍率の最近傍ラスタライズ境界・丸めが主因と確定した。
## F-132: 7px fallback glyphの右端症状は非整数倍率由来

時計本文を7px fallbackへ差し替え、pane widthを40pxとして折り返しを除いた状態で、
要求サイズだけを `18 x 24`（横・縦とも `7` の非整数倍率）と `14 x 14`（整数2倍）で比較した。
font/CWDH/string/pane width/NEAREST設定は固定。整数2倍では右端1〜3pxの欠け・不均一さが
改善し、字形自体も正常だった。

従って、F-131で確認した `cellWidth=7 / glyphWidth=6 / advance=7` はquadとadvanceの
差を作るものの、今回の見た目の主因はbuffer越境ではなく非整数倍率の最近傍ラスタライズに
おける端部境界・丸めである。CWDHを診断的に改変する必要はなく、stock資源を維持する。

## F-133: ResFont glyph atlas と native GPU text bridge（静的解析）

### リソース形式と TGLP

`nwfont_ResFont_ParseAndAttachResource` (`0x4D8048`) は `CFNU`/`CFNT` を検証し、
`FINF`・`CMAP`・`CWDH`・`TGLP`・`GLGR` チャンクの埋め込みオフセットをリソース基底へ
再配置したうえで `ResFont+0x04`（resource）と `+0x08`（FINF payload）へ保存する。
TGLP の実使用フィールドは次の通り。

| offset | 内容 |
|---:|---|
| `+0x00/+0x01` | cell width / cell height |
| `+0x02/+0x03` | baseline 系 / max character width（名称未確定） |
| `+0x04` | 1 sheet の byte stride/size |
| `+0x08` | sheet count |
| `+0x0A` | texture format |
| `+0x0C/+0x0E` | columns / rows per sheet |
| `+0x10/+0x12` | sheet width / height (pixels) |
| `+0x14` | raw glyph-sheet atlas pointer |

`nwfont_ResFont_GetGlyphSheetTableBytes` (`0x4D8220`) が `20 * LE16(TGLP+8)` を返すため、
glyph-sheet descriptor は 1 sheet あたり 0x14 bytes である。

### descriptor 初期化と range cache request

`nwfont_ResFont_SetGlyphSheetTable` (`0x13C518`) →
`nwfont_ResFont_InitGlyphSheetDescriptors` (`0x1426C8`) →
`nwfont_GlyphTextureDescriptor_Init` (`0x141B48`) の順で、sheet ごとに次を設定する。

| descriptor offset | 内容 |
|---:|---|
| `+0x00` | texture handle 初期値 0 |
| `+0x04` | owner `ResFont*` |
| `+0x08` | `sub_143B54(raw_sheet) >> 3`。アドレス変換後の GPU 用表現（raw virtual pointer の単純な `>>3` ではない） |
| `+0x0C/+0x0E` | height / width |
| `+0x10` | texture format |

raw sheet は `TGLP+0x14 + index * LE32(TGLP+0x04)`。全 sheet 範囲は
`0x143718`→`0x144C44` の `0x001F0082` IPC request へ渡される。`0xFFFF8001` は
`dword_8AD218` から読み出される process handle 値であり command ID ではない。既知の
`GSPGPU_FlushDataCache` (`0x13B6A4`, header `0x00080082`) と同じ SVC 形式だが header が
異なるため、`0x143718` の正確な command semantics（flush/invalidate等）は未確定とする。

この補正は F-136。`0x143718` (0x2C bytes)、`0x144C44` (0x38 bytes)、header literal
`0x144C7C`、process handle literal `0x8AD218` は `code_runtime.elf.i64` とも byte-for-byte
一致したため、request の存在とビルド対応は強いが、ライブ実行時の結果は未観測である。

### 既存 atlas を使う native text draw

`nwfont_ResFont_GetGlyph` (`0x7438B4`) が CMAP/CWDH/TGLP から一時 glyph record を作り、
`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) が `glyphWidth` と cell 座標から quad/UV を生成する。
`0x4D5118` で sheet width/height・format・raw base・filter flags を
`nwfont_CharWriter_SetGlyphTextureParams` (`0x4D8484`) に渡し、`0x4D5148` の
generic GPU draw routine (`0x7A7FAC`, `(6,0,4)`) へ進む。この一連が、自前 GPU callback から
ゲームの glyph atlas を再利用するための静的な最短経路になる。

`0x4D8484` の decompiler 表示では `0x7ABDBC` の引数が省略されることがあるが、assembly
では `0x4D5118` から渡された width/height/format/raw sheet address を使って format switch
を行い、stack/register に pack して `0x7ABDBC` へ渡している。従って同関数は filter-only
ではなく、format/寸法/raw に依存した generic texture setup dispatcher と wrap/filter state
設定を兼ねる。ただし backend の実 GPU upload/bind 完了時点と format enum の意味は未検証。

構造と引数のうち、live `ResFont*`、font ごとの format/stride、glyph record、batch instance は
F-139 の読み取り専用動的観測で確認済みである。texture handle 生成時点、自前 callback から
descriptor を直接参照する後段 submit、`0x4D8484` backend の GPU bind 完了時点は未検証であり、
次はそれらを分離して観測する。

再現用スクリプトは `scratchpad/dump_glyph_atlas.py`。IDA Remote GDB でプロセスを
Suspend した状態から実行し、毎回 `0x33000000-0x330FFFFF` を再走査して stale な
runtime address を使わない。メモリ書込み・breakpoint 操作は行わない。

## F-134: glyph texture handle の lazy allocation と batch 分岐

`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) は `glyph+0x14` の descriptor があるかで
texture 経路を分ける。descriptor があれば `descriptor+0` の handle を使い、0 のときだけ
`sub_7A8B08(1,&local)` で 1 個の handle を遅延生成して書き戻す。その後
`sub_7A6558(3553,handle)`、`nwfont_CharWriter_SetGlyphTextureParams`、
`sub_7A7FAC(6,0,4)` の順で即時描画する。descriptor がない場合は writer `+0x40` context の
共有 handle (`+4`) と raw pointer cache (`+0xE4`) を使い、raw pointer が変わった場合だけ
texture parameter を更新する。

writer `+0x44` が非 nullの batch 経路では、texture bind を行わず 44-byte glyph instance
（位置・色・UV・descriptor pointer）だけを配列へ追記して return する。したがって最初の
自前実装は descriptor ありの immediate 1 glyph に限定し、batch は後段 submit と状態復元を
追跡してから扱う。

## F-139: ResFont→CMAP→batch quad の実機照合

Remote GDB で会話表示中に `0x743768` へ停止し、`tid=219` の `R0=0x3302ABE0`（17×24
ResFont）と `R1=0x904A`（「遊」）を取得した。`0x74385C` の戻り値は `R0=0x0A01`で、
ResFont `+0x14/+0x16` のキャッシュは `0x904A/0x0A01` へ更新された。CMAP の入力・出力・
キャッシュ更新が静的コードと一致する。

続く `0x4D4EAC` では writer `0x0000FC70`、glyph record `SP=0x0FFFFB10`、raw sheet
`0x318B2A80`、glyphWidth=4、cellHeight=24、sheet=128×128、format `0x0B`、descriptor
`0x319BEB70` を読み取った。`writer+0x44=0x32D3A6F0` が非零で、batch 分岐が選択された。
終端 `0x4D4FC8` では count 増加後の44-byte instance `0x32D3A770`を確認し、末尾に同じ
descriptor が格納されていた。よってこの表示経路では `0x4D5118`→`0x4D8484` は呼ばれず、
texture bind は後段 submit の責務である。5秒走行後も4フォント（154/3/3/1 sheets）の
descriptor `+0` handle は全て0だったため、lazy materialize の時点は別経路の未解決事項とする。

### F-140 TextBox 描画入口（静的）

標準 UI テキストの一回分の流れは、`nwlyt_TextBox_DrawText` (`0x4BB1E8`) 内の次の順序で
固定されている。

```
sub_7E8488(SP)                         // 0x64-byte TextWriter 初期化
nwlyt_TextBox_ConfigureTextWriter       // TextBox の font/size/spacing/context をコピー
sub_4D5858(SP)                          // 0x4BB278: GPU/text state 準備
sub_7E7F48(SP, string@+0xD4, len@+0xFA) // 0x4BB288: UTF-16 glyph emission
sub_4D7730()                            // GPU channel/state reset
```

`sub_4D5858` は `writer+0x40` の persistent context を使用するため、単に 0x64-byte writer
をゼロ初期化して `sub_7E7F48` を呼ぶだけでは不十分である。自前描画で stock ResFont atlas
を使う場合は、少なくとも有効な `ResFont*`、context、scale/座標/色、`+0x44`（batch buffer
または immediate=0）の整合した組を用意し、同じ render pass 内で state reset まで行う必要が
ある。`0x4BB278` は writer/context の live 値を採取するための静的測定点であり、実機で
TextBox を再描画させてから動的に確認する。

### F-141 TextWriter wrapper と描画後 reset（静的）

`sub_7E7F48` (`0x7E7F48`) は caller writer を 0x64 bytes丸ごと stackへコピーし、
`nwfont_TextWriter_DrawString(local,R1,R2)` を呼ぶ。終了後に callerへ書き戻すのは local
`+0x2C/+0x30` の cursor 8 bytesだけで、R3は使用しない。自前描画でこの wrapper を使うなら、
writerのcursorを毎回設定し、R3に意味のある値を仮定しない。

`sub_4D7730` (`0x4D7730`) は channel 0〜3の dirty byteを `sub_7A7F74` 経由でクリアし、
共通 command state のbit `0x40`を必要時に立てる。これはnative TextBox draw後の状態境界なので、
同じrender passでstock atlasを描く自前経路にも対として置くべきである。

### F-143 TextBox vtable の実描画入口

`nw_lyt_TextBox` vtable (`0x8FC07C`) の slot `+0x68` (`0x8FC0E4`) は `0x73CF48`。
この wrapper は dirty TextBox を `sub_4BAFB0` へ送り、local TextWriter の `+0x44` に
TextBox+0x104 の batch bufferを設定して `sub_4D5194`→`sub_7E7F48` を実行する。
`+0x40` context は0のままで、`sub_4D5858` は通らない。実機では会話外の時計 TextBox
（UTF-16 `"00"`）で `0x73CF48` を捕捉し、これが `0x4BB278` 未ヒットの理由と確定した。

### F-142 EmitGlyphQuad の共有経路（実機）

会話を開いていない状態でも `0x4D4EAC` で停止し、R0=`0x0FFFFC58`（TextWriter）、
R1=`0x0FFFFAF8`（glyph record）、LR-4=`0x4D5834`、font=`0x3302ABE0`、
writer+0x40=`0`、writer+0x44=`0x32D0721C`、raw sheet=`0x3187CA80`、
descriptor=`0x319BE954`、scale=1.0を確認した。したがってこの関数は会話専用ではなく、
他のUI文字も同じbatch経路を使う。`+0x40==0` のwriterを即時経路へ強制するのは危険であり、
まず有効なcontextを持つwriterの捕捉が必要である。

### F-135 再監査: 静的 IDB と実機コードダンプの独立照合

`code_runtime.elf.i64` は実機から吸い出したコードダンプ由来の照合用 IDB（ライブプロセス
ではない）である。`code.bin.i64` と同時に開き、同じ VA の raw bytes を6領域で比較したところ、
次の全てで差分は 0 bytes だった。

| VA | 長さ |
|---:|---:|
| `0x4D8048` parser | `0x1B8` |
| `0x4D4EAC` EmitGlyphQuad | `0x2E4` |
| `0x1426C8` descriptor loop | `0x90` |
| `0x141B48` descriptor init | `0x40` |
| `0x4D8220` sheet-table size | `0x194` |
| `0x4D8484` texture parameters | `0x90` |

`0x8FCAAC` の ResFont vtable、`0x4D8200` の `CFNU/FINF/CFNT/CMAP/TGLP` 文字列、主要
xref（parser 2件、sheet-table 2件、descriptor init 2件、texture parameter 1件）、および
`0x4B4AB4` / `0x52D74C` の2つの loader callerも両 IDB で一致した。したがって6関数の
命令列・関数境界・同一ビルドの VA 対応に矛盾はない。F-139 で live descriptor/glyph/batch
instance の実値も確認済みだが、texture handle の materialize 時点と自前 callback からの
再利用可否は未検証のままとする。

---

# 自前テキスト描画（F-156 〜 F-162、2026-08-30 完成）

**「好きな位置に好きなテキストを好きな色で」が実機で通った。**
ゲームの `TextBox_Draw` wrapper も `TextBox_EmitBatchToGpuCommands` も呼ばない。

適用: `PATCHES/cave_text_emit.py` + `PATCHES/cave_textbox.py`

## 1. フック地点 `0x4B7DCC`

`TextBox_EmitBatchToGpuCommands` 内、`TextBatch_CopyToCommandBuffer` から戻った直後。
必要なものが全部レジスタに生きている。

| reg | 内容 |
|---|---|
| `R0` | 進んだ cursor |
| `R4` | **完成済み submit descriptor**（`+0x44` のクリアは `0x4B7DDC` まで起きない） |
| `R5` | drawctx |
| `R6` | textbox |
| `R9` | **プリフィックス直後の cursor**（`0x4B7D44` で設定、以後不変） |

`R1/R2/R3/R7/R8/R12` は以降どこからも読まれないので自由に使える
（`R7/R8` は関数末尾の `POP {R4-R9,PC}` が呼び出し元の値を復元する）。

## 2. 1 枚描く手順

1. `[R9-64, R9)` の **プリフィックス 16 ワード**を cursor へ複製
2. 複製の平行移動を書き換える
3. `desc+0x04` に色を書く
4. `TextBatch_CopyToCommandBuffer(desc, cursor, 0)` を呼ぶ。戻り値が次の cursor

出力サイズ = `0x60` バイトのヘッダ + `(batch+0x1C)*4`。

## 3. プリフィックス 16 ワードの構造

`TextDraw_EmitStatePrefix`(`0x4D5CB0`) が `drawctx+568` から流すもの。
長さ = `16*(drawctx+37)+16`。呼び出し前に `drawctx+37 = 3` が書かれるので**常に 64 バイト**。

```
[ 0] 0x80000020        param0（uniform index）
[ 1] 0x000F02C0        header  reg 0x2C0
[ 2] matrix[0]         param0
[ 3] 0x00BF02C1        header  reg 0x2C1 + 11 params
[4..14] matrix[1..11]
[15] 0
```

`*(drawctx + 0x66C)` == `drawctx + 580` == `&staging[3]`（実測、差 12）。

## 4. 座標系

行列は 3 行 x 4、**行内は `(x, y, z, w)`**。`w` が平行移動。

| 要素 | ストリーム index | cursor 基準 |
|---|---|---|
| `matrix[3]` 平行移動 X | `[6]` | `(cursor+64) - 40` |
| `matrix[7]` 平行移動 Y | `[10]` | `(cursor+64) - 24` |
| `matrix[11]` 平行移動 Z | `[14]` | `(cursor+64) - 8` |

- **`+X` は右、`+Y` は上。** 単位はレイアウト px（クリップ空間ではない）
- **「ずらす」のではなく「絶対位置を設定する」。** 元の値を上書きする
- `T_nam_00` の基準値は `(-126.0, -5.0)`
- `matrix[0]` は **pane ごとの拡大率**。全体比ではない

`sub_73CE64`(`0x73CE64`) が `textbox+128` から行列を組み、
index 1/5/9（Y 列）を負号反転してレイアウト Y 下向きをクリップ Y 上向きに変換する。

## 5. 色

**u32 で `0xAABBGGRR`**（メモリ上 R,G,B,A 順）。実機で `0xFF0000FF` が赤になることで確定。

| 出所 | descriptor | 用途 |
|---|---|---|
| `*(textbox+256)` = マテリアル の `+20` | `desc+0x04` | **本体の色** |
| 同 `+16` | `desc+0x00` | live では常に A=0 |
| `textbox+216` / `+220` | `desc+0x18` / `+0x1C` | 文字色 上 / 下 |
| `textbox+181` | `desc+0x49` | alpha 倍率 |

最終 alpha = `色の上位バイト * desc[0x49] / 255`。

### ドロップシャドウの正体

**フォントでも専用の影描画処理でもない。マテリアル色が黒の 2 枚目の TextBox。**

| pane | `mat+20` | `tb+181` | 見え方 |
|---|---|---|---|
| `T_msg_00` 本文 | `FFFFFFFF` | `0xFF` | 白・不透明 |
| `S_msg_00` 影 | **`FF000000`** | **`0xF0`** | 黒・94% |

## 6. `a3 = 0` が安全な理由

`a3`(DrawContext) は `batch+9` の bit1 が立つ indexed 経路でしか参照されない。
会話 TextBox は 3 つとも `batch+9 == 0x00` の直接コピー経路。
これで F-154 の `drawctx[417..419]` 二重更新 SIGSEGV を回避できる。

## 7. 文字列の差し替え

`nwlyt_TextBox_SetString`(`0x4BACBC`) をフックして `R1`（文字列）と `R3`（長さ）を差し替える。
バッファに直接書いてもゲームが毎フレーム書き戻すので消える。

**★フックを入れても即座には変化しない。**
名前 pane の `SetString` は**会話の区切り**でしか呼ばれない
（実測: 会話の最後のメッセージに達した瞬間 / 話しかけ直したとき）。

## 8. 制約

- **既存 TextBox の描画に相乗りしている。** 会話ウィンドウが出ている間しか描けない（TODO-115）
- **字形はゲームの batch 生成に依存。** 容量（pane の `cap`）と発火タイミングに縛られる（TODO-114）
- ケーブは `.text` 末尾のゼロ埋め `0x00838018` に置く。
  **`.text` は RX なのでケーブ内から書き込んではいけない**（F-161、`DOCS/crash_recovery.md`）

---

# 自前 UI 画像（スプライト）の描画（F-176 〜 F-185、2026-08-30）

**GPU コマンドを 1 バイトも書かずに UI 画像を 1 枚足せる。**
さらに**任意の GPU コマンドも発行できる**（F-185）。

実装: `PATCHES/cave_add_sprite.py`（ラベル解決つき簡易アセンブラ `Asm` 内蔵）

## 1. Picture はコマンドを直接吐かない

描画コンテキスト（drawctx）の 3 つの配列にエントリを溜め、
`sub_4B8360(drawctx, cursor)` が一括で流す。

| 配列 | ポインタ | カウンタ | 1 画像あたり |
|---|---|---|---|
| 索引 | `*(drawctx+1640)` | `drawctx+36` | 1 エントリ |
| 行列＋色 | `*(drawctx+1644)` | `drawctx+37` | 行列 3 ＋ 色 4 |
| 幾何・UV | `*(drawctx+1648)` | `drawctx+38` | 2 エントリ |

索引エントリ（16 バイト）:

| ワード | 意味 |
|---|---|
| `w0` | 行列の索引（float） |
| `w1` | 幾何の索引 + 1（float） |
| `w2` | 幾何の索引（float） |
| `w3` | **色の索引**（float）— F-183。F-180 では「マテリアル」と誤記していた |

## 2. 1 枚足す手順

`sub_4B8360`（`0x4B8360`）の入口をフックする。`R0 = drawctx`。

1. 複製元の行列 3 エントリ（12 ワード）を末尾へコピー
2. 複製元の幾何 2 エントリ（8 ワード）を末尾へコピー
3. コピーした幾何の先頭 2 ワードを**幅・高さ**に書き換える
4. コピーした行列の平行移動成分を書き換える（`+48+12` が X、`+28` が Y）
5. 4 隅ぶんの色（R,G,B,A の float x 4）を行列配列の末尾に積む
6. 索引エントリを 1 つ足し、`w0/w1/w2/w3` に各索引を入れる
7. カウンタ `+36` `+37` `+38` を増やす

**フレームごとに 1 枚だけにするには**、`Render_FrameEnd`（`0x4F1CE4`）にも
フックを置いてフラグを立て、こちらでフラグを見て降ろす。

## 3. 効くもの・効かないもの（実機で A/B）

| 要素 | 結果 |
|---|---|
| 大きさ | **効く**（幾何エントリの先頭 2 ワード） |
| 位置（絶対座標） | **効く**（行列の平行移動成分） |
| **アルファ** | **効く**（色エントリの 4 番目の float） |
| 色（RGB） | **効かない** — 素材の TexEnv が頂点カラーの RGB を使っていない |
| TexEnv 定数色 6 段 | **効かない** — テクスチャが LA4（色を持たない） |

## 4. ★任意の GPU コマンドを発行する（F-185）

```
sub_4B8360:  PUSH {R4-R8,LR}     ← フック地点
             MOV  R4, R0         ; drawctx
             MOV  R6, R1         ; ★cursor
```

**引数は 2 つ。decompiler は第 2 引数を落とす。**
ケーブ冒頭が `PUSH {R0-R3,R12,LR}` なので `[SP,#4]` が元の `R1`。

```
LDR R2,[SP,#4]        ; カーソル
STR Rx,[R2],#4        ; パラメータ
STR Rh,[R2],#4        ; ヘッダ  header = reg | (mask<<16) | (extra<<20) | (consec<<31)
STR R2,[SP,#4]        ; 進めたカーソルを書き戻す → POP で反映
```

## 5. マテリアルが色とテクスチャを出す経路

`sub_4B7864`（`0x4B7864`）。Picture のマテリアルは `*(picture + 316)`。

（疑似C を省略。原本は _local/legacy-src/…）

**マテリアルが変わるたび `sub_4B8360` を呼んで流す** ← 「1 バッチ = 1 マテリアル」の正体。
状態キャッシュ: `0x97B6FC` / `0x97B714` / `0x97B72C`。
自前の色を出したあとは、ここを潰さないと後続が色を引き継ぐ。

## 6. テクスチャのレジスタ（実機のコマンド列から）

| reg | 例 | 意味 |
|---|---|---|
| `0x080` | `0x00011001` | テクスチャ有効化 |
| `0x082` | `0x00080008` | テクスチャ 0 の大きさ（高さ<<16 \| 幅） |
| `0x085` | `0x03037AE0` | テクスチャ 0 のアドレス（**PA >> 3**） |
| `0x08E` | `9` | 形式（0=RGBA8, 5=LA8, 7=L8, 8=A8, 9=LA4, 11=A4 …） |
| `0x083` | `6` | ラップ / LOD |

**UI のテクスチャは VRAM にある**（PA `0x18000000`-`0x18600000`）。
`VA = PA + 0x10000000` は**リニア FCRAM 専用**の規則なので VRAM には使えない。

## 7. バッチ本体の形

`sub_4B8360` が流すのは頂点シェーダの float uniform 転送。

```
80000006  000F02C0    ; VSH_FLOATUNIFORM_INDEX = float32 モード | 開始 index 6
00000000  007F02C1    ; VSH_FLOATUNIFORM_DATA を連続バースト
...
```

つまり配列に積んだ「行列」「色」「幾何」は、**すべてシェーダの uniform** になる。

---

# ★自前 UI 画像を 1 枚足す — 完成形（F-187 〜 F-190、2026-08-31）

**位置・大きさ・色・アルファをすべて自前で決められる。GPU コマンドは 1 バイトも書かない。**
実装: `PATCHES/cave_add_sprite2.py`

## 1. 1 枚のスプライトを決めるもの

```
索引エントリ  *(drawctx+1640) + 16*n      カウンタ drawctx+36
  w0 = 行列の索引        -> 位置
  w1 = 自分の幾何の索引  -> 大きさ・アンカー
  w2 = 追加幾何の索引    -> UV
  w3 = 色ブロックの索引  -> 4 隅の色

行列  *(drawctx+1644) + 16*w0   3 エントリ。行0 の w が X、行1 の w が Y
色    *(drawctx+1644) + 16*w3   4 エントリ
幾何  *(drawctx+1648) + 16*w1   (幅, 高さ, -幅/2, +高さ/2)
```

**色ブロックは 4 隅ぶん連続。並びは 左上 → 右上 → 左下 → 右下、各 `(R, G, B, A)`。**
色は**テクスチャへの掛け算**（真っ赤にしても模様が残る）。

## 2. ★相乗り先は `+37` で見分ける

| `+37` | 中身 |
|---|---|
| 3 | 行列 3 エントリだけ = **色を持たない**。`w3` はアルファとして解釈される |
| 7 | 行列 0..2 ＋ **色 3..6**。`w3` が色の索引になる |

**色を使いたいなら `+37 = 7` のバッチに乗る。**

## 3. ★アンカーを必ず大きさに合わせる

幾何エントリの後ろ 2 ワードはアンカーのオフセットで、中央揃えなら **`(-幅/2, +高さ/2)`**。
**幅・高さだけ書き換えると釣り合いが崩れて画面外へ飛ぶ。**

`sub_73B5C4` が計算し、**この関数は `S0` を上書きする**。
Hex-Rays はそれを追えず `v14[2] = 行列索引` と誤って出す。

## 4. 実際の配置

| 索引 | 用途 |
|---|---|
| 0..2 | ゲームの行列 |
| 3..6 | ゲームの色ブロック |
| 7..9 | 自前の行列 |
| 10..13 | 自前の色ブロック |

カウンタ: `+36 = 2` / `+37 = 14` / `+38 = 4`

## 5. 配列ポインタは実体の 12 バイト先

`*(drawctx+1640)` = `drawctx+148`（実体 `+136`）、
`*(drawctx+1644)` = `drawctx+580`（実体 `+568`）、
`*(drawctx+1648)` = `drawctx+1108`（実体 `+1096`）。

フラッシュは実体の先頭から `16*個数+16` バイトを流し、先頭 12 バイトが
PICA のバースト用ヘッダになる。**フラッシュ後に配列を読んでも「書いた値」ではない。
検証は書いた直後に行うこと。**

---

# ★自前スプライトを独立したバッチで描く（F-192 / F-193、2026-08-31）

**位置・大きさ・色・アルファ・テクスチャをすべて自前で決められ、
ゲームの描画には一切影響しない。** 実装: `PATCHES/cave_own_batch.py`

## 1. フラッシュをラッパで包む

`DrawCtx_FlushBatch`（`0x4B8360`）は `R0` = drawctx / `R1` = cursor で入り、
進めた cursor を `R0` で返す。元命令を別番地に置けば `BL` で呼べる。

```
トランポリン:  PUSH {R4-R8,LR}     ← 元命令
              B    0x4B8364

ケーブ:
  1. BL トランポリン        ゲームのバッチを流す（カウンタが 0 に戻る）
  2. 配列[0].w0 を 3 つとも復元
  3. 自前のテクスチャレジスタ 4 組を発行
  4. 配列に自前スプライトだけを組む
  5. BL トランポリン        自前のバッチを流す
  6. POP {R4-R6,PC}         最後のカーソルを返す
```

## 2. ★フラッシュは配列の `[0].w0` を破壊する

```c
v6 = v5[3]; v5[3] = ヘッダ; v5[2] = v6;
```

PICA のバーストが `[param0][header][params...]` なので、
**配列の実体はポインタの 12 バイト手前から始まり、`[0].w0` はヘッダ用スロットを兼ねる。**

| 配列 | ポインタ | 実体 | 退避先 |
|---|---|---|---|
| 索引 | `drawctx+148` | `drawctx+136` | `drawctx+144` |
| 行列＋色 | `drawctx+580` | `drawctx+568` | `drawctx+576` |
| 幾何 | `drawctx+1108` | `drawctx+1096` | `drawctx+1104` |

**いずれも「配列ポインタ − 4」。** 2 回流すなら 2 回目の前に復元する。

## 3. ★素通り経路で `R0` / `R1` を壊さない

判定に `R1` を使うと `Mem_Copy(dst=0)` で SIGSEGV する。
**`R6`（自分で PUSH）と `R12` だけを使う。**

## 4. 行列は単位行列＋平行移動

```
行0 = (1, 0, 0, X)
行1 = (0, 1, 0, Y)
行2 = (0, 0, 1, Z)
```

---

# ★自前ビットマップフォントで文字列を描く（F-194 / F-195、2026-08-31）

実装: `PATCHES/cave_draw_sprites.py`

## 1. UV（アトラスからの切り出し）

追加幾何エントリ（索引エントリの `w2` が指す先）の 4 float。

**`(u0, v0, u1, v1)`。`v0` が上端、`v1` が下端**（v は上が 1）。

| 値 | 範囲 |
|---|---|
| `(0, 1, 1, 0)` | テクスチャ全体 |
| `(0.0, 1.0, 0.5, 0.5)` | 左上象限 |

## 2. N 枚描くときの配置

| 領域 | 割り当て |
|---|---|
| 行列 | `3k`..`3k+2` |
| 幾何 | `2k` = UV / `2k+1` = 幅・高さ・アンカー |
| 色 | `3N`..`3N+3`（共有） |
| カウンタ | `+36 = N` / `+37 = 3N+4` / `+38 = 2N` |

**上限は `+37 + 7 > 32` より N <= 7。**

**★索引もバイトオフセットも Python 側で計算して表に入れる。**
ケーブ側に整数→float 変換（VFP）が要らなくなる。

## 3. ★描画順は「フレーム内で何回目のフラッシュか」

**1 フレームに `DrawCtx_FlushBatch` は約 42 回**呼ばれる。
最初の方に相乗りすると後続の UI（地図など）に覆われる。
**最後のフラッシュで描けば最前面。**

```
cnt++;  if (cnt != total) skip;      ← 描画ケーブ
total = cnt;  cnt = 0;               ← Render_FrameEnd のケーブ
```

**相乗り先が「色つきバッチ」である必要はない。**
行列・色・幾何・カウンタ・テクスチャを全部自分で組むので条件は外せる。

## 4. フォントアトラス

64x64 の LA4（4096 バイト）に 8x8 グリフを 64 文字ぶん。

- **文字 = `0xFF`（L15/A15）、背景 = `0x00`（L0/A0）**
- `byte = tile*64 + (x0|y0<<1|x1<<2|y1<<3|x2<<4|y2<<5)`、`tile = (y>>3)*(幅>>3) + (x>>3)`
- 列 `k` の UV = `(k/8, 1.0, (k+1)/8, 1-1/8)`

インクの色は頂点カラーで変えられる。
ドロップシャドウは同じ文字を少しずらして暗い色でもう 1 枚描く。

## 5. フルカラー画像（RGBA8）

**メモリ上は `A, B, G, R` の順**（u32 LE で `0xRRGGBBAA`）。

```python
data[o+0] = A;  data[o+1] = B;  data[o+2] = G;  data[o+3] = R
```

タイリングは形式によらず共通:

```python
tile = (y >> 3) * (W >> 3) + (x >> 3)
m    = (x&1) | ((y&1)<<1) | (((x>>1)&1)<<2) | (((y>>1)&1)<<3) | (((x>>2)&1)<<4) | (((y>>2)&1)<<5)
o    = (tile * 64 + m) * bytes_per_texel
```

| 形式 | `reg 0x08E` | バイト/テクセル |
|---|---|---|
| RGBA8 | 0 | 4 |
| LA4 | 9 | 1 |
| ETC1 | 12 | 0.5 |

64x64 RGBA8 = 16384 バイト。`g_GfxAllocator` の `ALLOC_SIZE = 0x4000` にちょうど収まる。

**★検証用の画像は「効いていない」と「指定を間違えた」を区別できる形にする。**
4 象限を赤・緑・青・白にして外周に黒枠を付けると、
バイト順・上下の向き・タイリングを 1 枚で同時に判定できる。
枠が破線状に散らばればタイリングの誤り。

## 6. ★ドット絵をきれいに出す条件（F-198）

```
画面上の倍率 = 描画サイズ（単位） x 相乗り先の縮尺 / グリフのテクセル数
```

**これが整数になること。** 縮尺は batch ごとに違うので**乗り換えたら測り直す**。

| 単位 | 画面 px | 倍率 | 見え方 |
|---|---|---|---|
| 24 | 12 | 1.5 | 線が 1px と 2px に割れる |
| 48 | 24 | 3.0 | **均一** |

（相乗り先の縮尺 = 0.5、グリフ 8 テクセルの場合）

`reg 0x083 = 0`（ニアレスト）も必須。リニアだと境界がぼやける。

## 7. ★自前の状態を積んだら復元する

`unk_97B74C` はキャッシュであると同時に、
`Mem_Copy(cursor, &unk_97B74C, 32*n)` で**そのまま流されるコマンド列**。
ユニット 0 の 32 バイト = `0x082` / `0x085` / `0x08E` / `0x083` の 4 対。

**自前バッチの後にこれを流せば元に戻り、キャッシュとも整合する。**
キャッシュを 0 にして再発行させる手（`0x97B754` / `0x97B774` / `0x97B794`）もあるが、
**フェードの乱れという別の症状を生んだ。**

## 8. 7 枚を超えるとき

1 バッチ 7 枚まで（`3N+4 <= 25`）。超えるならフラッシュを繰り返す。
**最後のチャンクを大きさ 0 のダミーで埋めて全チャンクを 7 枚にそろえる**と、
カウンタも索引も定数のままで済む。
表の索引は**チャンク内の位置 `j`** で作る。
**配列 `[0].w0` の復元はチャンクごとに必要**（フラッシュのたびに潰れる）。

## 9. ★★UI の座標系（F-199）

| 項目 | 値 |
|---|---|
| 原点 | **画面中央** |
| UI 空間 | **400 x 240 単位** |
| 下画面 | 320 x 240 px |
| **縮尺** | **横 0.8 / 縦 1.0（非等方）** |

3DS の UI は上画面の 400x240 で作られ、下画面では横だけ 0.8 倍に潰される。

```
横の単位 = 欲しい px / 0.8   （= px * 1.25）
縦の単位 = 欲しい px / 1.0
```

**★正方形の単位で指定してはいけない。**

| 指定 | 画面 px | 倍率 | 見え方 |
|---|---|---|---|
| 48 x 48 単位 | 38.4 x 48 | 横 4.8 / 縦 6.0 | 横だけ不均一 |
| **30 x 24 単位** | **24 x 24** | **3.0 / 3.0** | **完全に均一** |

位置も `X * 0.8` が整数になるようにする（X を 5 の倍数にすればよい）。

### 測り方

**幅を変えた帯を複数本、同時に縦に並べる。** 1 本だけでは「はみ出している」ことしか
分からないが、複数本なら目盛りとして使えて 1 回で絞れる。
そのうえで **原点の位置**（四角を並べてどれが中央か）と突き合わせると 1 点に確定する。


---

# 自前 GUI を「常に最前面」に描く（F-204 〜 F-209）

実装: `PATCHES/cave_draw_topmost.py`

## 描画順の決まり方

UI は 1 本のコマンド列ではない。**レイアウトごとに専用リストへ記録し、再生で差し込む**（F-200）。
したがって **描画順 = 再生順** であり、記録の順ではない。

フレームは 2 つの描画パスから成り、**1040（下画面）→ 1024（上画面）** の順に走る。

| パス | 画面 | 最後に再生されるレイアウト | リスト id |
|---|---|---|---|
| `Frame_DrawPass1040`（`0x1B72E4`） | 下 | `0x3225AF24` | **15** |
| `Frame_DrawPass1024`（`0x1B71C4`） | 上 | `0x32C4CBCC` | **8** |

120 フレーム測定でどちらもブレ 0。**最前面に出したい画面のパスの、最後のレイアウトを狙う。**

## 注入点

`ssys_ma_lyt_Layout_RecordPaneTree`（`0x5686D4`）の記録本体の直後。

```
0056876C  BL nwlyt_DrawPaneTreeToCurrentList   記録本体
00568770  NOP    ★ここを分岐に置き換える（元命令を潰さない）
00568774  NOP    ← 戻り先
0056879C  BL GpuCmd_CommitListAndCaptureDelta  長さを確定（追記が反映される）
```

この時点で `R4` = レイアウト、選択中のリストはそのレイアウト専用、カーソルは `g_GpuCmdPtr`。

## 積む前に必ず整える 3 つの状態

### 1. 記録要求フラグ（F-204）

```
00568704  LDRB R0,[R5,#0x1D]   = レイアウト+0x11D
00568708  CMP  R0,#0
0056870C  BEQ  locret          立っていなければ何もせず帰る
005687B0  STRB R0,[R4,#0x11D]  記録し終えたら降ろす
```

**変化したレイアウトしか記録し直されない。** 入口で `*(layout+0x11D) = 1` を書いて強制する。

★**記録済みリストに書いたものは、記録し直されるまで消えない。**
フックを外しても画面に残る。掃除はフラグを 1 回立てるだけでよい。

### 2. マテリアル（F-206）

`nwlyt_Picture_DrawToCommandList` は必ず先頭でこう呼ぶ。

```c
cursor = Material_EmitState(drawctx, cursor, *(picture + 316));       // 0x4B7864
cursor = TextBox_UpdateDrawState(drawctx, cursor, *(picture+316), 1); // 0x4B7DEC
```

積まないと**直前のペインの色と TEV** がそのまま効く。
テクスチャレジスタだけ上書きしても、TEV が定数色を使う設定なら勝てない。

### 3. UV セット数（F-207）

**`drawctx+1692` が 0 だと UV 属性が構成されず、テクスチャ全面が貼られる。**
ゲームと同じ手順で、溜まっているぶんを流してから 1 にする。

## 座標系はレイアウトごとに違う（F-208）

| 経路 | 原点 | 縮尺 | 画面 |
|---|---|---|---|
| `cave_draw_sprites.py`（最初のフラッシュ相乗り） | 画面中央 | 横 0.8 / 縦 1.0（**非等方**） | 400 x 240 単位 |
| `cave_draw_topmost.py`（リスト id 15） | 画面中央 | **等方 1 単位 = 1px** | 320 x 240 単位 |

8px のグリフを 3 倍で出すなら、前者は 30 x 24 単位、後者は **24 x 24 単位**。
**相乗り先を変えたら必ず測り直すこと。** 使い回すと半端な拡大になり、
「一部の線が 1px、一部が 2px」という症状が出る。

### 縮尺の測り方

帯を伸ばして端に届くかで測ってはいけない。**ぴったりとはみ出しを区別できない。**

**目盛りを使う。** 16x16 の四角を `x = 0, ±80, ±160` と `y = 0, ±60, ±120` に並べ、
「全部が画面端で半分切れ、中央の 1 個が画面中央」を確認する。
縮尺と原点が同時に、一意に決まる。


## 対象は実行時に追いかける（F-210）

リスト id を固定で狙うと、その UI が消える場面（セーブ確認のメッセージウィンドウなど）で
**描かれなくなる**。「いついかなる時も描画されない事態を起こさない」ためには追いかける。

```
Frame_DrawPass1040（下画面・再生のみ）
    入口で「前フレームに集めた値」を確定（LOG+0x34）してから集め直す
    Layout_ReplayRecordedList のたびに R0 を LOG+0x2C へ
Frame_DrawPass1024（上画面・記録してから再生）
    記録のときに LOG+0x34 と突き合わせる
```

- **集めている途中の値を狙うと一致しない。** 記録と再生はフレーム内で入り混じる。
  1 フレーム分まるごと保持した値を狙う。
- **控えた値は比較にしか使わない。** 解放済みのポインタを掴んでも安全なように参照しない。
  フラグを書き込むのは「ゲームがいま処理しているレイアウト」だけ。

### ★「フックが発火している」と「描かれている」は別

発火 123 回（毎フレーム）でも画面に出ていないことがある。
切り分けは次の順で行う。

1. 発火回数
2. `*(layout+264)` 記録長（0 なら再生されない）
3. `*(layout+312)` scissor
4. `GpuCmd_ReplayRecordedListRange`（`0x7B0A28`）を直接フックして再生順を見る
5. マテリアル

## マテリアルの選び方（F-211 / F-212）

自前スプライトは**ゲームのマテリアルを借りて**描く。借り先は条件で選ぶ。

| 条件 | 根拠 |
|---|---|
| `*(picture+216)`（UV セット数）≥ 1 | 0 だと UV 属性が構成されない（F-207） |
| 4 隅の色が全部 `0xFFFFFFFF` ではない | 全部白だと `DrawCtx_PushVertexColors` が索引経路を使わない |
| 定数色 `+0x10 == 0` かつ `+0x14 == +0x18 == 0xFFFFFFFF` | 色付きだとその色が自前スプライトに出る |

### ★中立なマテリアルが 1 つも無い場面がある（F-214）

**タイトル画面とロード画面には、3 条件を満たすマテリアルが存在しない。**
実測でロード画面の Picture 320 個中、条件 1 は 295 個、条件 1+3 は **0 個**だった。
条件 2 を緩めても解決しない。

そこで枠を 2 つに分ける。

| 枠 | 条件 | 使い方 |
|---|---|---|
| 優先 | 1+2+3 すべて | そのまま積む |
| 予備 | 1 だけ | **`+0x10` 〜 `+0x30` の 9 語を一時的に中立化してから積み、直後に必ず戻す** |

ゲームのオブジェクトを一瞬書き換えるが、描画はゲームのスレッド上で単線なので安全。

### 中立化する 9 語（F-215）

```
+0x10        = 0
+0x14..+0x28 = 0xFFFFFFFF   （定数色。+0x28 はアルファを含む）
+0x2C/+0x30  = 0x15         （合成モードらしき値）
```

**3 語（`+0x10`/`+0x14`/`+0x18`）では足りない。**
しずえ会話の切り替えで使う `P_soft_B` は `+0x28 = 80FFFFFF`（アルファ 0x80）、
`+0x2C = +0x30 = 000006AA` を持ち、**半透明かつ別の合成**になるので
白を描いても見えない。動作実績のある `P_base_00` と同じ並びに揃える。

### ★描画の後に `Material_EmitState` を呼んではいけない（F-215）

「中立化した状態を積み直して戻す」つもりで描画後に呼ぶと、
**自前スプライトの位置にモザイク状の乱れ**が出る。
`Material_EmitState` は内部で `DrawCtx_FlushBatch` を 12 箇所から呼ぶので、
描き終えた直後の**中身が確定していない配列**が流されてしまう。

積み直しは不要。マテリアルの中身は既に素へ戻してあり、
ゲームは毎フレーム、ペインごとに `Material_EmitState` を呼び直す。
**副作用のある関数を「後始末」に使わないこと。**

### マテリアルの構造（実機で採取）

| オフセット | 内容 |
|---|---|
| `+0x10` | 定数色（中立なら `0`） |
| `+0x14` 〜 `+0x2C` | 定数色（中立なら `0xFFFFFFFF`） |
| `+0x38` 〜 | **ASCII の名前** |
| `+0x4D` | `Material_EmitState` が最初に読むバイト |

| 名前 | `+0x10` | `+0x14` | 判定 |
|---|---|---|---|
| `P_base_00` | `0` | `FFFFFFFF` | 中立 |
| `P_list_arrow_00` | `0` | `FFFFFFFF` | 中立 |
| `P_crsl_00` | `00FFFFFF` | `FF6077FF` | ★色付き（カーソル） |
| `W_msg_00` | `0` | `007D4040` | ★色付き（メッセージ枠） |

**名前が読めるので、マテリアルはアドレスではなく名前で語れる。**


---

# SD から任意の画像を描く（F-216 / F-217）

## ★`reg 0x082` は `(幅<<16)|高さ`

**正方形のテクスチャでは並び順を区別できない。**
自前 GUI は 64x64 のアトラスしか使っていなかったので、
`(高さ<<16)|幅` と書いていても何ヶ月も気付かなかった。
64x32 を貼って初めて「乱れているが単純なズレではない」という形で表に出た。

**対称性のある値（幅と高さ、X と Y、u と v）は、必ず非対称な入力で試すこと。**

## 変換は PC 側でやり切る

3DS の GPU は **8x8 タイル + Morton 順**、幅・高さは **2 の冪**しか読めない。
PNG をそのまま置いても描けない。展開器を 3DS 側へ持ち込むと失敗の仕方が増えるので、
**並べ替えと形式変換は PC で終わらせ、3DS は「読んで転送するだけ」**にする。

```
python PATCHES/make_gui_image.py 入力.png 出力.acgx --format rgba8 --pos 0,-40 --size 64,64
```

`--format` は `rgba8` / `la4` / `a4`。PIL は不要（zlib だけで PNG を読む）。
2 の冪でない画像は左上へ置いて余白を透明で埋め、UV をそのぶんに詰める。

出来た `.acgx` を SD の `/luma/plugins/00086200/gui_image.acgx` へ置く。

## 使い方（好きな画像を出す手順）

### 1. PNG を用意する

- 8bit の PNG（グレースケール / パレット / RGB / RGBA。**インタレースは不可**）
- 大きさは自由。2 の冪でなければ左上へ置いて余白を透明で埋める
- **透明部分はそのまま透明に出る。半透明も使える**（F-218 で実機確認）。
  アルファ 255/170/85/0 の 4 段階も、0→255 のなめらかな階調も潰れない。
  OSD を避けた理由の 1 つがこれ

大きさの上限（バッファ 0x4000 バイト）:

| 形式 | 最大 |
|---|---|
| `rgba8` | 64x64 |
| `la4` | 128x128（色は失われ、輝度とアルファだけになる） |
| `a4` | 256x128（アルファだけ。色はスプライト側の 4 隅の色で付く） |

### 2. 変換する

```
python A:/Disassemble/acnl/PATCHES/make_gui_image.py 入力.png gui_image.acgx        --format rgba8 --pos 0,-40 --size 64,64
```

| オプション | 意味 |
|---|---|
| `--format` | `rgba8` / `la4` / `a4`。既定 `rgba8` |
| `--pos X,Y` | 画面上の位置（px）。**画面中央が原点、+X が右、+Y が上**。既定 `0,0` |
| `--size W,H` | 画面上の大きさ（px）。既定は元画像の大きさ（等倍） |

下画面は 320x240 px なので、`--pos` は X が -160〜160、Y が -120〜120。
**位置は画像の中心**（左上ではない）。

### 3. SD へ置く

```
/luma/plugins/00086200/gui_image.acgx
```

### 4. 反映する

3DS を起動し、**ゲームが動き出してから**プラグインメニューの
「自前 GUI を最前面に描く」を ON にする。
一度 OFF にして ON にし直せば読み直される。

ファイルが無い・壊れている場合は**埋め込みのフォントアトラスのまま動く**
（「いついかなる時も描画されない事態」を避けるため）。
読み込みの結果は SD の `/CTRPF_OwnGui.txt` に出る。

### いま出来ないこと

- 1 ファイルにつきスプライトは 1 枚（形式は 14 枚まで持てるが、変換ツールが 1 枚しか出さない）
- 画像の差し替えは ON/OFF のやり直しが要る（実行中の再読み込みは未実装）

## `.acgx` の形式

```
0x00  4  "ACGX"
0x04  2  版 = 1
0x06  2  テクスチャ形式（PICA reg 0x08E。0=RGBA8 / 9=LA4 / 11=A4）
0x08  2  幅（2 の冪）      0x0A  2  高さ（2 の冪）
0x0C  2  スプライト数（1〜14）
0x10  4  画素データの位置   0x14  4  画素データの長さ
0x20  スプライト表（1 件 16 バイト: s16 x,y,w,h + u16 u0,v0,u1,v1）
```

## プラグインが差し替えるもの

| もの | やり方 |
|---|---|
| 画素データ | バッファへ転送し `svcFlushProcessDataCache` |
| テクスチャの寸法・形式 | 描画ケーブのワードを差し替え（`kGuiTexSizeWord` / `kGuiTexFmtWord`） |
| スプライト | 表の**位置・大きさ・アンカー・UV だけ**。**`0x30` 以降は触らない** |

使わない枠は幅・高さを 0 にして消す（ダミーと同じ扱い）。

## 大きさの上限

バッファは `Alloc(0x4000, 0x80)` の 16 KB。

| 形式 | 最大 |
|---|---|
| RGBA8（4 B/texel） | 64x64 |
| LA4（1 B/texel） | 128x128 |
| A4（0.5 B/texel） | 256x128 |

超えるものは変換ツールが警告する。

---

# 上画面の常時描画へ向けたパス末尾の再監査（F-233、2026-09-01）

**観測状態の訂正:** 初期停止時はロード画像が表示されていたが、最初に実機を走らせた時点で
ロードは終了した。以後の pass 順、id 30、主リスト容量、Drawer の標本はすべて通常場面。
この時点ではロード画像表示中の低レベル replay 順は未取得だった。後の F-234 で取得済み。

## `Frame_EndDrawPass1024/1040` は通常の submit 点ではない

`code.bin.i64` の静的解析と実機値を突き合わせた。guard 値だけはロード画像表示中の
初期停止で読み、入口 breakpoint はロード終了後に観測した。

| 入口 | 静的な guard | 初期停止時の実機値 | 結果 |
|---|---|---:|---|
| `0x5A27C8`（1024 / 上） | `dword_94C8A0 == 0` | 0 | 早期 return |
| `0x5A2894`（1040 / 下） | `byte_94C898 == 0` | 0 | 早期 return |

従って、両入口は描画パス末尾の**注入位置候補**にはなるが、stock が直後に必ず
`GpuCmd_SplitAndSubmit` する場所ではない。提出が必要なら明示呼出しを別の実験として検証する。

実測の入口順は `1024（上）→1040（下）→次の1024`。
両入口の caller は `LR=0x543C6C` (`MethodTree_WalkAndInvoke`)、同じ描画 thread 219 だった。

## Layout 入口順と GPU の実 replay は区別する

ロード終了後の通常場面で、Layout 関数入口の最後は上 id 8 / 下 id 15 だったが、
`GpuCmd_ReplayRecordedListRange` で非ゼロ長として実際に観測した列は両 pass とも次だった。

```
Render_DrawSceneIndexed: list id 4 または 5, length 0x92B0
Layout_ReplayRecordedList: list id 30, length 0x1940..0x2E50
```

この結果は「Layout 入口の最後」と「実 replay の最後」を同一視できないことを示す。
従って、その同一視に依存した F-230 の「ロード画像は別経路」という帰属は未立証へ戻した。
id 30 は通常場面の標本であり、ロード画像との対応を示さない。

## 上入口にある主リストと Drawer

`0x5A27C8` 入口の通常場面の実機標本（差分計算は IDAPython）:

```
base        = 0x323B2130
g_GpuCmdPtr = 0x323B59A8
g_GpuCmdEnd = 0x324B2130
capacity    = 0x100000
used        = 0x3878
remaining   = 0xFC788
```

`*(0x96FC38)+0x364 = 0x32FF62EC` の vptr は
`0x008FBF04 = vtbl_nw_lyt_Drawer`。静的にも、非ゼロ Layout の replay 前に
`sub_4B8C34(drawer, layout+0x30, 0)` がこの Drawer を更新する。

ただし `cave_draw_topmost.py` が自前設定するのはマテリアル、UV、テクスチャ、頂点、色であり、
**投影は直前の有効 Layout が Drawer に残した状態へ依存する。**
「投影まで完全に自前確立済み」という旧記述は誤り。

> ### ★★★【F-265 / F-266 / F-272 による精密化】
>
> 「Drawer に残った状態」という言い方は結果としては合っているが、**機序が曖昧**だった。
> 正確には次のとおり。
>
> 1. 各 Layout は `+0x28`（幅）/ `+0x2C`（高さ）の float 2 本しか投影の入力に使わない。
>    `sub_73BAC0(&rect, Layout+0x10)` が
>    `l = -W/2, t = H/2, r = W/2, b = -H/2` を返す（ペインツリーは読まない）。
> 2. `ssys_ma_lyt_Layout_SetupProjectionMatrix`（`0x567BC0`、vtable `+0x18`）が
>    直交行列を組み、`Mtx44_RotateForScreen(m, 1)`（3DS の 90 度回転）をかけ、
>    **`Layout+0x34` の 16 語**として保持する。
> 3. **replay 時**に `Layout_ReplayRecordedList`
>    → `nwlyt_Drawer_BeginLayoutReplayState`（`0x4B8C34`）
>    → `nwlyt_Drawer_EmitProjectionUniform`（`0x4D6C90`）が
>    その 16 語を `drawer+0x34` へ写し、24 語のコマンドとして
>    **VSH float uniform index 0** へ流す。
>
> つまり「相乗りしたレイアウトの投影が効く」のは、
> **そのレイアウトの replay がその場で uniform を送っているから**である。
> `LayoutMgr_SetDisplaySize` が出すのは**ビューポート**であって投影ではない。
>
> 自前ノードがゲームの replay 関数を使う場合、投影は **自前ノードの `+0x28`/`+0x2C`**
> で決まる。`PATCHES/cave_node_record.py` はこれを画面実寸で明示し、
> `SetupProjectionMatrix` を自分で呼んでいる（F-264 / F-266）。

## 次の安全な最小実験

1. `0x5A27C8` 入口で上画面の UI 画像（スプライト）1枚・1チャンクだけを主リストへ積む
2. 同一 manager 由来の `base / ptr / end` で残量を検査し、不足時は描画しない
3. 自然提出版と、明示的 `GpuCmd_SplitAndSubmit(0x1280CC)` 版を分離して A/B する
4. 通常画面とロード画面の両方で、表示順と投影を比較する
5. 1→2→6→19チャンクの順に広げ、ptr 差・残量・表示・クラッシュ有無を表にする

実行前に全 branch target、PC-relative literal、コードケーブ範囲、`.bss` 範囲を
generator で機械監査する。現行 `cave_draw_topmost.py` には `CMDEND` / `LISTMGR` の定数があるが、
描画ケーブ本体は残量を実際に検査していないため、容量安全の証拠にはならない。

---

# ロード画像の実 replay 順と上画面常時描画の根本原因（F-234、2026-09-01）

F-233 ではロード開始後に通常場面へ移ってからしか低レベル replay を測れていなかった。
ユーザーがロード画像を目視して Suspend した状態を改めて作り、一回だけ制御再開して
上画面パス末尾 `0x5A27C8` で停止した。

## ロード画像表示中の上画面 replay

`GpuCmd_ReplayRecordedListRange` の引数と caller を直接記録した結果:

| 順序 | pass | list id | length | caller LR |
|---:|---:|---:|---:|---:|
| 0 | 1（上） | 8 | `0x180` | `0x5683E8` |
| 1 | 1（上） | 10 | `0x2C0` | `0x5683E8` |

どちらも `Layout_ReplayRecordedList` からの replay である。
現行 record-list 方式は上画面候補 id 8 の記録末尾へ UI 画像（スプライト）を積むため、
**後から replay される id 10 に覆われる。** ロード画像は Layout の後の別経路ではない。

## id 10 の視覚リソースによる独立同定

停止中のスタックから `Layout 0x3225A2B4` を得た。vptr は
`0x008F1F54 = vtbl_Layout`、記録値は id `10` / start `0` / length `0x2C0`。
リンクは id 8 → id 10 → NULL で trace 順と一致する。

さらに Layout から直接到達するリソースに以下があった。

- pane: `RootPane`, `N_All`, `P_bg`, `G_loop`
- texture: `tc_load_01.bclim`〜`tc_load_03.bclim`
- animation: `load_wait_kind.bclan`
- archive: `Layout/common/save_wait.arc`

従って id 10 は、停止時に表示されていたロード画像 Layout である。
これは低レベル replay trace とは独立したオブジェクト／リソース側の証拠。

## replay 前の Drawer 反映と fingerprint

`Layout_ReplayRecordedList` は replay 前に
`sub_4B8C34(Drawer, Layout+0x30, 0)` を呼ぶ。下位の `sub_4D6C90` は
`Layout+0x34` の `0x40` bytes を Drawer へコピーした後、次の変換を行う。

```
Drawer+0x30 = Layout+0x34 の先頭 word
Drawer+0x34 = 0x013F02C1
Drawer+0x38..+0x70 = Layout+0x38..+0x70
```

よって raw `0x40` bytes の完全一致で Layout を探してはいけない。
この変換後 fingerprint は停止中の id 10 Layout と Drawer で一致した。

## 容量比較

`GpuCmd_SelectList` の静的な bucket 式と runtime manager、Layout の記録値を突き合わせた。

| 対象 | base | ptr / offset | end / size | 残量 |
|---|---:|---:|---:|---:|
| ロード画像 id 10 記録リスト | `0x327AE270` | `0x2C0` | size `0x1000` | `0xD40` |
| ロード中の上画面主リスト | `0x3229D0C0` | `0x3229E370` | `0x3239D0C0` | `0xFED50` |

id 10 の末尾へ積めば描画順だけは改善できる可能性があるが、`0xD40` では
19チャンク級の全メニューを収められない。**全GUIは上パス末尾の主リスト方式を優先する。**

ただし `0x5A27C8` は通常 submit 点ではなく、現在のケーブは投影を直前 Layout の
Drawer 状態へ依存する。

### F-235: 主リスト末尾の手製 Drawer-state / 自然提出版は不成立

2026-09-02 に UI画像（スプライト）1枚だけの自然提出版を、branch / PC literal / cave /
`.bss` / list capacity を停止中に監査して適用した。表示は出ず、通常 Resume 後も
**画面更新だけが停止し音声は継続**した。ユーザー Suspend 後に hook・LOG・cave を
stock/zero へ復元し、cave 2範囲の各320 wordsも bulk read で zero を確認した。

この結果は「同入口に十分な容量がある」ことと「UI画像を安全に描いて提出できる」ことが
別問題である実証である。後から読んだリストに固有 float が無かったため、ケーブのどこまで
実行されたかは未確定。**同版を再適用せず、ここへ明示的 Split を重ねない。**
次は同一フレーム内の cursor / manager / submit 境界を採取する読み取り専用 trace を先に作る。

### F-236: Layout record-list の容量は「buffer を置換してから」拡張する

`Layout_RecordPaneTree(0x5686D4)` は Layout 専用 list へ Pane tree を記録し、
`GpuCmd_CommitListAndCaptureDelta(0x7B0694)` が range を確定、
`Layout_ReplayRecordedList(0x5682DC)` が主 list へ replay する。`LayoutList` の child-record
walk は `0x566EA0`（IDB 名 `ssys_ma_lyt_LayoutList_RecordChildren`）で、`list+4` から
node+8 を辿って child vslot+0x14（`Layout_RecordPaneTree`）を呼ぶ。

`GpuCmd_SelectList(0x1216BC)` の新 id 経路は manager header だけを alloc し、buffer の
base/capacity は用意しない。capacity field だけの増加は不正である。また
`Layout_RecordPaneTree` の `0x568770`（raw word **`0xE320F000`**）は DrawPaneTree の直後、
DrawEnd/Commit の前であり、manager+0x0C はまだ commit 前の offset である。正しい copy 量は
`used = g_GpuCmdPtr - manager->base`。

`PATCHES/probe_layout_record_buffer_extend.py` は描画を変えない検証用実装である。id 0x10 に限り、
game `g_GfxAllocator` から 0x4000-byte / 0x80-aligned buffer を取得し、`Mem_Copy` で `used`
bytes を移し、manager base/size と global cursor/end を同時に替える。実機ではゼロ長 record で
一度成功（`0x1000 -> 0x4000`）したが、nonzero copy と replay、視覚安定性は未確認。従って
完成した拡張方式と呼ばず、次は nonzero record を trace してから UI画像（スプライト）1枚へ接続する。

### F-237: command-add と再生順制御を分離する

gokiro 氏の `render.txt` は、描画コマンドを追加するフック、再生順を変えるフック、コマンド
バッファの拡張を分ける設計を示す。本解析ではこれを高価値な設計参考として用い、ACNL JPN 無印の
実装は静的 IDB と実機を別々に照合した。

`LayoutMgr_RenderTop(0x566DF8)` は top list の child record を終え、表示サイズ 400x240 を設定後、
`LayoutList_SetDisplay(0x566E30)` へ display token `0x400` を渡す。後者は `list+4` から
node `+8` を辿り、各 Layout の `+0x134` に token を書いて vtable `+0x08`
(`Layout_ReplayRecordedList`) を呼ぶ。これは `Layout_RecordPaneTree` を呼ぶ別の child-record
loop (`0x566EA0`, vtable `+0x14`) と独立している。

実機 software breakpoint は `R0=root+4`, `R1=0x400`, `LR=0x001B7294` で止まり、この静的 call
site を裏付けた。`probe_layout_reorder.py` は node link を変えず、top pass だけ指定 Layout を
一度保留して他 node の後に replay する no-draw 実験である。元から tail の対象で 1200 ms 動かし、
`call=0x72` / top target match=`0x26` を得て clean uninstall した。

これは「順序フックが動く」根拠であって、「ロード画像より UI画像（スプライト）が前面になる」
根拠ではない。次の証明は、ロード中に id `0x08` の non-tail Layout を選び、id `0x0A` より後へ
再生されたことを ring trace と視覚結果の二経路で確認してから行う。最終実装ではその同一 Layout
pointer を command-add と buffer-extension の共有対象にする。

### F-238: ロード画像は単一の LayoutList 組成ではない

F-234 の `id 0x08 -> 0x0A` replay 記録を「ロード画面では常に二 node が同居する」と一般化しては
ならない。後の user-visible loader stopped snapshot を read-only node walk すると、top list には
id `0x10` の tail 1 node、bottom list には node が無かった。

`probe_layout_reorder_auto.py` は毎回の top pass で current list を二段階で走査し、id `0x08` が
ちょうど一つで tail 以外ならのみ、その replay を最後へ回す no-draw probe である。300 ms 標本は
`calls=0x5D`, last top match `1`, `reorders=0` だった。従ってその期間には id `0x08` があっても
tail だった。F-234 の一回限りの pass と矛盾と断定せず、**loader は組成が変わる phase を持つ**と
扱う。

最終的な ordering hook は id を固定せず、command-add 対象と同一の current Layout pointer を
そのフレームだけ共有しなければならない。次回は transition 前から self-logging hook を置き、
unique non-tail 条件を満たした run に限って replay ring と UI画像（スプライト）を検証する。

---

# ★UI 描画の完全な状態表（F-264〜F-272、2026-09-04）

自前ノードから「上下画面に常時・最前面で描く」ために必要な GPU 状態を、
**誰がいつ確立するか**でまとめたもの。すべて静的解析による。

## 1 フレームの流れ

```
RenderTop        (0x566DF8) RecordChildren(mgr+4)    → SetDisplaySize(400,240) → SetDisplay(mgr+4,    0x400)
RenderTopRightEye(0x5692B0)                          → SetDisplaySize(400,240) → SetDisplay(mgr+4,    0x410) → UnlinkAll
RenderBottom     (0x568F98) RecordChildren(mgr+0x10) → SetDisplaySize(320,240) → SetDisplay(mgr+0x10, 0x401) → UnlinkAll
```

- `SetDisplaySize` = **ビューポート**。主リストへ直接出る。そのパスの全 replay に先行する
- `SetDisplay` = 各 Layout の replay。**描画順はリストの並び順**
- リストは毎フレーム `sead_List_UnlinkAll`（`0x133B20`）で空になり、各ノードの
  `+0x04`（prev）/ `+0x08`（next）も 0 にされる。**毎フレーム登録し直す設計**
- `LayoutMgr_AddLayout`（`0x56928C`）は `Layout+0x0C`（バイト）の昇順挿入。
  `node[+0x0C] <= new[+0x0C]` の間だけ進むので **`0xFF` なら必ず末尾＝最前面**

## 記録（`Layout_RecordPaneTree` = `0x5686D4`、vtable `+0x14`）

（疑似C を省略。原本は _local/legacy-src/…）

## 再生（`Layout_ReplayRecordedList` = `0x5682DC`、vtable `+0x08`）

```
scissor コマンド（+0x138 が 1 なら +0x13C..、そうでなければ +0x28/+0x2C から全画面）
if (+0x108 > 0) {
    nwlyt_Drawer_BeginLayoutReplayState(drawer, this+0x30, 0)
        → nwlyt_Drawer_EmitProjectionUniform(drawer, cursor, this+0x34)   ← ★投影 uniform
    GpuCmd_ReplayRecordedListRange(+0x100,+0x104,+0x108,+0x10C,+0x110,+0x114,+0x11C)
    Drawer->DrawEnd1(drawer, 0)
}
```

## 状態の出所

| GPU 状態 | 出所 | いつ |
|---|---|---|
| ビューポート | パスの `SetDisplaySize` | replay の直前（主リスト） |
| **投影行列**（uniform 0〜3） | **Layout `+0x34`** ← `+0x28`/`+0x2C` から | **replay 時** |
| scissor | Layout `+0x28`/`+0x2C`（または `+0x13C..`） | replay 時 |
| シェーダ本体・頂点属性 | Drawer 既定 begin ブロック（`sub_4D5D1C` が LayoutMgr 初期化時に構築） | **再生時**（記録内容の直前） |
| ブレンド `0x101` / 色演算 `0x100` / アルファテスト `0x104` | 同上（`unk_8ADB10`） | **再生時**（記録内容の直前） |
| **TEV 6 段** | **マテリアル**（既定ブロックには**無い**） | 記録の中 |
| テクスチャ座標出力 `0x06F` / ユニット有効化 `0x080` | `TextBox_UpdateDrawState`（`0x4B7DEC`） | 記録の中 |
| テクスチャ結び付き `0x082`/`0x083`/`0x085`/`0x08E` | `unk_97B74C`（ユニットごと 32 バイト） | 記録の中 |
| 行列・色・幾何（uniform 6〜） | `DrawCtx_FlushBatch`（`0x4B8360`） | 記録の中 |

**★★F-276: `DrawBegin1` / `DrawEnd1` は第 2 引数で挙動が変わる。**

```
sub_4D72C4:  TST R2,#1 / BNE →  ★フラグが立っていたら 1 語も出さない
sub_4D7204:  if ((a3 & 1) == 0) → 同上（end ブロック）
```

| 呼び出し | フラグ | 出るもの |
|---|---|---|
| 記録 `DrawBegin1(drawer, 1)` | 1 | **無し**（drawctx の帳簿リセットのみ） |
| 記録 `DrawEnd1(drawer, 1)` | 1 | **無し**（溜まったバッチを流すだけ） |
| 再生 `sub_4B8C34(drawer, DrawInfo, 0)` | 0 | reg `0x06F` / `0x080` + **既定 begin ブロック** + 投影 uniform |
| 再生 `DrawEnd1(drawer, 0)` | 0 | **既定 end ブロック** |

**1 レイアウトぶんの、フレーム上の実際の並び**

```
reg 0x06F mask2 = 0                       ← テクスチャ座標出力 OFF
reg 0x080 mask2 = 0 / maskB = 0x00001000  ← テクスチャユニット全 OFF
既定 begin ブロック（シェーダ・属性・0x100/0x101/0x104）
投影 uniform（index 0、24 語）
────── 記録した内容をそのまま memcpy ──────
既定 end ブロック
```

**自前で描くなら、記録内容の先頭で `0x06F` と `0x080` を立て直すこと。**

**`DrawBegin1`（`sub_4D7274`）は記録の先頭で drawctx の状態をリセットする（フラグに関係なく）。**

（疑似C を省略。原本は _local/legacy-src/…）

**`0x06F` と `0x080` は再生時に 0 にされる**（記録内容が展開される直前）ので、
自前記録では**必ず立て直す**こと。

```
reg 0x06F mask 2 = 0x00000100     ← 使うユニットのビットマスク << 8
reg 0x080 mask B = 0x00011001
reg 0x080 mask 4 = 0x00011001
```

## マテリアルの TEV テンプレート

`Material_EmitState`（`0x4B7864`）は `*(mat+0x30) & 3` でモードを選び、
**テンプレートを丸ごとコピーして色の穴だけ差し替える**。

| モード | テンプレート | 語数 | 触る段 | 先頭段の src |
|---|---|---|---|---|
| 0 | `0x97B6EC` | 6 | 5 | `PRIMARY, CONST, CONST` |
| 1 | `0x97B704` | 18 | 3,4,5 | `CONST, TEX0, CONST` |
| 2 | `0x97B7AC` | 22 | 3,4,5 | `TEX0, TEX1, CONST` |
| 3 | `0x97B804` | 34 | 1,2,3,4,5 | `TEX0, CONST, CONST` |

**どのモードも先頭段が `PREVIOUS` を読まない**ので、それより前の段の設定は結果に出ない。
最終段（TexEnv5）は**常に `PRIMARY_COLOR`（頂点カラー）を掛ける**。

段ごとのレジスタは `0x0C0`（TexEnv0）/ `0x0C8` / `0x0D0` / `0x0D8` / `0x0F0` / `0x0F8`（TexEnv5）で、
それぞれ `SOURCE / OPERAND / COMBINE / COLOR / SCALE` の 5 語を
ヘッダ `0x804F00xx`（mask `0xF` / extra 4 / consecutive）の 1 バーストで書く。

解読には `scratchpad/pica_decode.py` を使う（**IDA 不要**。`code_runtime.bin` から読む）。

---

# ★自前 GUI を「上下画面に常時・最前面」で描く — 完成形（F-281、2026-09-04 実機確認）

`PATCHES/cave_node_record.py`。**自前の `Layout` ノードをリストへ登録し、
ゲームと同じ契約で記録・再生させる**方式。借り物の GPU 状態はゼロ。

## 仕組み

```
RenderTop(0x566DF8) 入口フック   → 上ノードを mgr+4    へ優先度 0xFF で登録
RenderBottom(0x568F98) 入口フック → 下ノードを mgr+0x10 へ優先度 0xFF で登録
  登録時に
    +0x28/+0x2C = 画面実寸（上 400x240 / 下 320x240）
    +0x121 = 0 → Layout_SetupProjectionMatrix(0x567BC0) を呼ぶ → +0x34 に投影行列
    +0x11D = 1（記録要求）
  ↓
RecordChildren が自前ノードの vtable +0x14（CAVE_Q）を呼ぶ
    GetProperty(519) → SelectList(自前 id) → Clear → StartSave
    → DrawBegin1(drawer, 1)     ← 何も出さない。drawctx の帳簿だけリセット
    → 自前 TEV 36 語 / reg 0x06F / reg 0x080 / テクスチャ 4 対 / スプライト
    → DrawEnd1(drawer, 1)       ← 溜まったバッチを流す
    → Commit(+0x104..+0x110) → SelectList(戻す) → +0x11D = 0
  ↓
SetDisplay が vtable +0x08（= ゲームの Layout_ReplayRecordedList）を呼ぶ
    sub_4B8C34 → 既定 begin ブロック + reg 0x06F=0 / 0x080=OFF + 投影 uniform
    ReplayRecordedListRange → 記録した内容を主リストへ memcpy
    DrawEnd1(drawer, 0) → 既定 end ブロック
```

**既定ブロックは再生時に出る**（F-276）。そこで `0x06F` と `0x080` が落とされるので、
**記録内容の中で必ず立て直す**（F-270 / F-271）。

## 実機に入るもの

| フック | 番地 | 素の値 |
|---|---|---|
| `RenderTop` 入口 | `0x566DF8` | `0xE92D4010` |
| `RenderBottom` 入口 | `0x568F98` | `0xE92D4010` |
| `DrawCtx_FlushBatch` 入口 | `0x4B8360` | `0xE92D41F0` |

**この 3 本だけ。** テクスチャは `g_GfxAllocator` から 0x4000 を借りて置く。

## 記録される内容（実機から読み出して静的設計と一致を確認）

```
+000  00300030 804F00C0   TexEnv0 = MODULATE(PRIMARY, TEXTURE0)
+018  0FFF0FFF 804F00C8   TexEnv1..5 = REPLACE(PREVIOUS)（0x0D0/0x0D8/0x0F0/0x0F8）
+090  00000100 0002006F   reg 0x06F = テクスチャ座標出力 ON
+098  00011001 000B0080   reg 0x080 = ユニット 0 有効化
（以降 テクスチャ 0x082/0x083/0x085/0x08E、uniform 6〜、draw）
```

下画面 91 枚で **11536 バイト**（1 枚あたり約 127 バイト）。`LIST_SIZE = 0x4000`。

## 座標系

```
NDC.x = (2/H) * y      NDC.y = -(2/W) * x      （3DS の 90 度回転込み）
```

**原点は画面中央、等方 1 単位 = 1px。**
上画面（400x240）は x=±200 / y=±120、下画面（320x240）は x=±160 / y=±120 が端。

## テクスチャと文字

- `PATCHES/make_font_atlas.py` が 128x128 LA4・16x16 マスの ASCII アトラス（61 文字）を作る。
  **マス (15,15) は塗り潰し**（枠・カーソル用）
- **拡大率は元テクセル 8px の整数倍にすること。**
  1.75 倍だと最近傍サンプリングで元 1 画素が出力 1px と 2px に割れ、
  線幅が不揃いになり 1px のノイズが点々と走る（F-281 で実機確認）
- **色はチャンク（7 枚）単位**でしか変えられない。`pack_groups` が境界を揃える

## 見た目を変えるとき

`PATCHES/update_tables.py` を `py_exec_file` するだけ。
**ケーブもフックも vtable も触らない。** `.bss` の表・色・`LOG` のポインタを書き換える。
登録ケーブが毎フレーム `+0x11D` を立てるので次のフレームで反映される。
