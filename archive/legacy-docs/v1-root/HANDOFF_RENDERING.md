# 引き継ぎ — 描画機能の解析（2026-09-01 時点）

> **2026-09-02 F-241 の緊急更新:** loader lifecycle trace が live Layout を破損したため、
> 現在はゲーム再起動・IDA 再アタッチ待ちである。次担当は本書より先に
> **`HANDOFF_F241_LIFECYCLE.md`** を読むこと。旧 `probe_loader_submit_lifecycle.py` の install は
> 禁止（script 側でも拒否）であり、詳細は `RE/STATE.md` / `RE/FINDINGS.md` F-241 にある。

**この文書だけで作業を再開できるように書いてある。**
まずこれを通読し、必要に応じて `RE/FINDINGS.md` の F-110 〜 **F-185** を参照すること。
クラッシュしたら `DOCS/crash_recovery.md`。

---

# ★★★★★★★ここから読む — **TODO-131 完了。常に最前面に描ける**（F-204〜F-209, 2026-08-31）

## 現行版は `PATCHES/cave_draw_topmost.py`

`cave_draw_sprites.py` は旧版（地図やメニューより後ろになる）。

### 効いた注入点

**下画面のパス（`Frame_DrawPass1040`）で最後に再生されるレイアウト（リスト id 15）の
記録本体の直後 = `0x568770` の NOP。**

### 4 つのフック

| フック | 番地 | 役割 |
|---|---|---|
| マテリアル捕獲 | `0x4B7864` | `Material_EmitState` の `R2` を控える（F-206） |
| 記録要求フラグ強制 | `0x5686D4` | 対象を毎フレーム記録し直させる（F-204） |
| 描画 | `0x568770`（NOP） | 記録本体の直後に自前スプライトを積む |
| drawctx 記録 | `0x4B8360` | `DrawCtx_FlushBatch` の `R0`、最初のフラッシュ時のマテリアル |

### 追いかける仕組み（F-210）— リスト id を固定してはいけない

セーブ確認のメッセージウィンドウを出すと、固定で狙っていたレイアウトが再生されなくなる。
**そのフレームで下画面パスの最後に再生されたレイアウトを実行時に追いかける。**

```
Frame_DrawPass1040（下画面・再生のみ）
    入口で「前フレームに集めた値」を確定（LOG+0x34）してから集め直す
    Layout_ReplayRecordedList のたびに R0 を LOG+0x2C へ
Frame_DrawPass1024（上画面・記録してから再生）
    記録のときに LOG+0x34 と突き合わせる
```

**集めている途中の値（LOG+0x2C）を狙うと発火 0 回になる。**
記録と再生はフレーム内で入り混じるため、1 フレーム分保持した値を狙うこと。
控えた値は**比較にしか使わない**（解放済みでも安全なように参照しない）。

### CTRPF プラグイン（TODO-130 / F-213 / F-214）

`Plugin/.../Sources/OwnGui.cpp`。メニュー「自前 GUI を最前面に描く」で ON/OFF。

- **ケーブは C++ へ書き直さない。** `cave_draw_topmost.py` の `MODE = "export"` が
  `includes/GuiCaves.h` を吐き、プラグインはそれを書き込むだけ
- 書き出したら**実機メモリと機械的に突き合わせる**（不一致 0 を確認してから移す）
- GPU 可視バッファは `Render_FrameEnd` に一時フックを仕掛けて
  **ゲームのスレッド上で**ゲームのアロケータを呼ぶ。取れたら外す
- キャッシュは **`svcFlushProcessDataCache`（標準 SVC）**。
  Luma 独自の `svcFlushDataCacheRange` はカーネル内でフォルトする
- Makefile は `$(OUTPUT).3gx : $(OUTPUT).elf` / `$(OUTPUT).elf : $(OFILES)` の順で書く。
  テンプレートのままだと**リンクし直されず、.3gx の中身が古いまま**になる

**★デバッガから試すときは `TEX_VA` を `0x009B0010`（確保スロット）の値に合わせる。**
バッファの番地は boot ごとに違う。合わせ忘れると**何も描かれない**（実際に踏んだ）。

### ★いま進行中 — TODO-134: 自前チートメニュー

**★この件の引き継ぎは `HANDOFF_CHEATMENU.md` に独立して書いてある。そちらを読むこと。**
ここには描画基盤の話だけを残す。

**目標**: CTRPF のチートメニューを自前のものへ置き換え、
**開いている間もゲームが進行する**ようにする。
設計は `Plugin/CTRPF-GUI-Simulator`（ブラウザで動く実物大プレビュー）。
実装は CTRPF / C++20。ホットキーは自前 = Select、従来 = Select + DPad Up。

**段 B（描画基盤）は実機で動いている**（F-220）。

- 上下画面の描き分け（対象は実行時に追いかける。下 = パス1040 / 上 = パス1024）
- **チャンクごとの色**（.bss の配列から 16 float 読む）。
  選択帯・黄色の未適用項目・半透明パネルに必須

**再開に必要なことは `RE/TODO.md` の TODO-134「中断時点の状態」に全部ある。**
実機の状態、LOG の割り当て、ケーブの配置、再起動後の手順、
そして**プラグインが段 B をまだ取り込んでいない**こと。

グリフアトラスは 128x128 LA4（16KB = 8x8 セル 256 個）。
`Alloc` は 0x4000 までしか取れない（F-221）。**A4 ではなく LA4**にすること
（A4 だと RGB が 0 になり頂点カラーで色を付けられない）。

### SD から任意の画像を描く（F-216 / F-217）

```
python PATCHES/make_gui_image.py 入力.png 出力.acgx --format rgba8 --pos 0,-40
```

出来た `.acgx` を SD の `/luma/plugins/00086200/gui_image.acgx` へ。
無ければ埋め込みのフォントアトラスのまま動く。

- **変換は PC 側でやり切る**（8x8 タイル + Morton、2 の冪）。
  展開器を 3DS へ持ち込まない。PIL は無いので zlib だけで PNG を読む
- 上限はバッファの 0x4000 バイト。RGBA8 なら 64x64、LA4 なら 128x128
- 検証は `PATCHES/apply_gui_image.py`（プラグインと同じ手順をデバッガから）

**★★`reg 0x082` は `(幅<<16)|高さ`**（F-216）。
64x64 の正方形しか使っていなかったので、逆に書いていても長く気付けなかった。
**対称性のある値は必ず非対称な入力で試す。**

### マテリアルの選び方（F-211 / F-212 / F-214）— 「たまたま」で選ばない

3 つとも満たすものだけ採用する。

1. `*(picture+216)`（UV セット数）≥ 1
2. 4 隅の色（`*(picture+320..332)`）が全部 `0xFFFFFFFF` ではない
3. マテリアルの定数色 `+0x10 == 0` かつ `+0x14 == +0x18 == 0xFFFFFFFF`

**マテリアルは `+0x38` から ASCII の名前が読める。**
`P_base_00`（中立）/ `P_crsl_00`（`+0x14 = FF6077FF`）/ `W_msg_00`（`+0x14 = 007D4040`）。
色付きを借りると自前スプライトにその色が出る。

**★タイトル/ロード画面には 3 条件を満たすものが 1 つも無い**（F-214。
Picture 320 個中、条件 1 は 295 個、条件 1+3 は 0 個）。
そこで枠を 2 つに分け、予備（条件 1 のみ）は
**`+0x10` 〜 `+0x30` の 9 語を一時的に中立化してから積み、直後に必ず戻す**（F-215）。

```
+0x10        = 0
+0x14..+0x28 = 0xFFFFFFFF   （定数色。+0x28 はアルファを含む）
+0x2C/+0x30  = 0x15         （合成モードらしき値）
```

**3 語では足りない。** `P_soft_B` は `+0x28 = 80FFFFFF`（アルファ 0x80）と
`+0x2C = 000006AA` を持ち、半透明かつ別の合成になるので白を描いても見えない。

**★★描画の後に `Material_EmitState` を呼ばないこと**（F-215）。
内部で `DrawCtx_FlushBatch` を呼ぶので、**中身が確定していないバッチが流れて
モザイク状の乱れになる**。後始末に副作用のある関数を使わない。

**★`.text` の空きは `0x838080` 〜 `0x839000`。** `0x839000` からは実データ。
ケーブを伸ばすときは末尾を必ず検査する。

### ★ここで踏んだ落とし穴（同じ道を通らないこと）

1. **記録は「記録要求フラグ」が立つときだけ走る**（F-204）。立てないと発火 0 回。
2. **「最後に再生される」は画面ごとに違う**（F-205）。フレーム全体で測ると上画面のものが出る。
3. **マテリアルを自前で積まないと直前のペインの色になる**（F-206）。
   実機では持ち物欄ボタンの色を、タッチ時の変化まで含めて拾った。
4. **`drawctx+1692` が 0 だと UV が読まれずテクスチャ全面が貼られる**（F-207）。
5. **レイアウトごとに投影が違う**（F-208）。旧経路の 0.8/1.0 を使い回すと半端な拡大になる。
   id 15 は **等方で 1 単位 = 1px、原点は画面中央**。
6. **記録済みリストに書いたものはフックを外しても消えない**（F-204）。
7. **「フックが発火している」と「描かれている」は別**（F-210）。
   発火 123 回でも画面に出ていないことがある。発火回数だけで安心しない。
8. **リスト id を固定で狙わない**（F-210）。場面によって再生されなくなる。
9. **マテリアルを「たまたま」で選ばない**（F-211 / F-212）。

### ★縮尺の測り方

帯を伸ばして「端に届くか」で測ってはいけない。**ぴったりとはみ出しを区別できない。**
16x16 の四角を `x = 0, ±80, ±160` / `y = 0, ±60, ±120` に並べる**目盛り**を使う。
「全部が画面端で半分切れ、中央の 1 個が画面中央」なら 1 単位 = 1px と確定できる。

---

# ★★★★★旧: 自前 GUI 描画の完成（F-176〜F-195, 2026-08-31）

## 0. ユーザーからの恒久的な指示（★復唱の義務は撤廃。エージェント側で決まる）

- 解析をする前に、AGENTS.md を必ず読む。
- 未知の解析に入る前に、TODO.md や FINDINGS.md など、既にその箇所の解析が進んでいないかを調査する。
- TODO.md や FINDINGS.md のconfidenceがHIGHだったとしても過剰に信じない。
- 導き出した答えが矛盾しないか、独立した2つの結果を突き合わせ調査する。
- 暗算は絶対にしない。必ずスクリプトで計算する。
- AIはコンテキスト圧縮等による記憶欠如対策のため、何かの変更や記憶しておく必要のあるものは必ず一時メモファイルを作成読み込む。
- プログラム部分の静的解析は必ずidalib-mcpを使いcode.bin.i64で行う。動的解析はida-pro-mcpを使う。
- 必ずIDAがSuspend済みかどうかを調べてからユーザーにお願いする。

## 1. ★達成したこと

**自前のビットマップフォントで文字列を、最前面に、任意の位置・大きさ・色で描ける。**
ゲームの描画には一切影響しない。

実装: **`PATCHES/cave_draw_sprites.py`**（現行版）

| 要素 | 状態 | 根拠 |
|---|---|---|
| 常時描ける相乗り点（ゼロフレーム **0.00%**） | 済 | F-177 |
| 位置・大きさ・色・アルファ | 済 | F-190 |
| 自前テクスチャ | 済 | F-191 |
| 独立したバッチ（ゲームに影響しない） | 済 | F-193 |
| UV でアトラスから切り出す | 済 | F-194 |
| **複数枚・ビットマップフォント・最前面** | **済** | **F-195** |

**GPU コマンドはテクスチャの 4 レジスタ（8 ワード）だけ。**
頂点データは全部ゲームのパイプラインに載せている。

## 2. 仕組み — フラッシュをラッパで包む

`DrawCtx_FlushBatch`（`0x4B8360`）は **`R0` = drawctx / `R1` = cursor** で入り、
進めた cursor を `R0` で返す（F-185。**decompiler は第 2 引数を落とす**）。

```
トランポリン:  PUSH {R4-R8,LR}     ← 元命令
              B    0x4B8364

ケーブ（0x4B8360 のフック）:
  1. そのフレームの最後のフラッシュか判定（下記 3-a）
  2. BL トランポリン        ゲームのバッチをそのまま流す
  3. 自前のテクスチャレジスタ 4 組を発行（3-c）
  4. 配列[0].w0 を 3 つとも復元（3-b）
  5. 表を見ながらスプライトを N 枚積む
  6. BL トランポリン        自前のバッチを流す
  7. POP {R4-R8,PC}         最後のカーソルを R0 で返す
```

## 3. ★★★必ず守る 4 つの掟

### (a) ★★描画順 — UI は「1 本のコマンド列」ではない（F-200）

**レイアウトごとに専用リストへ記録し、あとで再生する。**
**描画順は「記録した順」ではなく「再生した順」で決まる。**

```
Frame_DrawPass1024():             ← 記録＋再生
    BaseObj_RunDrawPhase()
    Render_DrawScene2()
    Render_DrawScene0(1024)
    Render_DrawScene1(1024)
    Frame_EndDrawPass1024()       ★描画の最後（0x5A27C8、xref 1 件）

Frame_DrawPass1040():             ← 再生のみ
    Render_DrawScene0(1040)
    Render_DrawScene1(1040)
    Frame_EndDrawPass1040()       ★描画の最後（0x5A2894、xref 1 件）
    Render_FrameEnd()
```

**最前面に入れたいなら `Frame_EndDrawPass1024` / `1040` をフックする。**
`GpuCmd_SplitAndSubmit`（28 か所から呼ばれる）を使ってはいけない。

追記の手順はゲーム自身の慣用句に倣う:

```
cursor = GpuCmd_GetCurrentWritePtr()           // = g_GpuCmdPtr（0x4D7164）
cursor = DrawCtx_FlushBatch(drawctx, cursor)
g_GpuCmdPtr = cursor
```

**★反証済み**: 「`GpuCmd_Advance` を通さなかったから GPU が固まった」は誤り。
実体は `g_GpuCmdPtr += bytes` だけ。

### (a2) 旧説（誤り。参考のため残す）— フレーム内で何回目のフラッシュか

**1 フレームに約 42 回**フラッシュがある。最初の方に相乗りすると地図などに覆われる。
**最後のフラッシュで描けば最前面。**

前フレームの総回数を覚えておき、今フレームでその回数目に達したら描く。

```
cnt++;  if (cnt != total) skip;      ← 描画ケーブ
total = cnt;  cnt = 0;               ← Render_FrameEnd のケーブ
```

### (b) フラッシュは配列の `[0].w0` をヘッダで潰す（F-192）

退避先は **「配列ポインタ − 4」**。2 回流すなら 2 回目の前に 3 配列とも復元する。
**フラッシュ後に配列を読んでも「書いた値」ではない。検証は書いた直後に。**

### (c) テクスチャは 4 レジスタすべて上書きする（F-191）

```
reg 0x082 = 高さ<<16 | 幅
reg 0x083 = 0        （bit1 拡大 / bit2 縮小フィルタ。0 = ニアレスト）
reg 0x085 = PA >> 3  （リニア FCRAM なら PA = VA - 0x10000000）
reg 0x08E = 形式     （0=RGBA8, 9=LA4, 12=ETC1 …）
```

`0x083` を忘れると相乗り先のパラメータが残って縞模様になる。

### (d) ★自前の状態を積んだら、ゲームの状態を復元する（F-198）

`unk_97B74C` はキャッシュであると同時に、
`Mem_Copy(cursor, &unk_97B74C, 32*n)` で**そのまま流されるコマンド列**。

| ユニット | 中身（`[param][header]` の 4 対 = 32 バイト） |
|---|---|
| 0 | `0x082` 大きさ / `0x085` アドレス / `0x08E` 形式 / `0x083` パラメータ |

**自前バッチの後にユニット 0 の 32 バイトを流せば元に戻る。**
キャッシュを 0 にして再発行させる手もあるが、**フェードの乱れという別の症状を生む。**

### (e) ★★UI の座標系（F-199。**これを知らないと必ずハマる**）

| 項目 | 値 |
|---|---|
| 原点 | **画面中央** |
| UI 空間 | **400 x 240 単位** |
| 下画面 | 320 x 240 px |
| **縮尺** | **横 0.8 / 縦 1.0（非等方）** |

```
横の単位 = 欲しい px / 0.8   （= px * 1.25）
縦の単位 = 欲しい px / 1.0
```

**★正方形の単位で指定してはいけない。**
8 テクセルのグリフを 3 倍（画面 24x24 px）で出すには **30 x 24 単位**。
正方形（48x48）だと横だけ非整数倍になり、列によって 1px 狭くなる。

位置も `X * 0.8` が整数になるようにする（X を 5 の倍数にすればよい）。

### (f) ★ドット絵をきれいに出す条件（F-198）

```
画面上の倍率 = 描画サイズ（単位） x 相乗り先の縮尺 / グリフのテクセル数
```

**これが整数になること。** 縮尺は batch ごとに違うので**乗り換えたら測り直す**。
実測: 「最初のフラッシュ」のバッチは **縮尺 0.5**。
8 テクセルのグリフを 3 倍にするには **48 単位**（= 画面 24px）。
`reg 0x083 = 0`（ニアレスト）も必須。

### (g) 素通り経路で `R0` / `R1` を絶対に壊さない

判定に `R1` を使うと `Mem_Copy(dst=0)` で SIGSEGV する（`DOCS/crash_recovery.md`）。
**判定は `R6`（自分で PUSH）と `R12` だけ。**
設置前に入口の全命令を機械的に走査して確認すること。

## 4. スプライト 1 枚を決めるもの

```
索引エントリ  *(drawctx+1640) + 16*n      カウンタ drawctx+36
  w0 = 行列の索引 / w1 = 自分の幾何 / w2 = 追加幾何(UV) / w3 = 色ブロックの索引

行列  *(drawctx+1644) + 16*w0   3 エントリ。**単位行列＋平行移動**
                                 (1,0,0,X) (0,1,0,Y) (0,0,1,Z)
色    *(drawctx+1644) + 16*w3   4 エントリ（左上→右上→左下→右下、各 (R,G,B,A)）
幾何  *(drawctx+1648) + 16*w1   (幅, 高さ, -幅/2, +高さ/2)
UV    *(drawctx+1648) + 16*w2   (u0, v0, u1, v1)。**v0 が上端、v1 が下端**
```

**アンカーは必ず大きさに合わせる**（`-幅/2, +高さ/2`）。忘れると画面外へ飛ぶ（F-190）。
色は**テクスチャへの掛け算**。

## 5. N 枚描くときの配置

| 領域 | 割り当て |
|---|---|
| 行列 | `3k`..`3k+2` |
| 幾何 | `2k` = UV / `2k+1` = 幅・高さ・アンカー |
| 色 | `3N`..`3N+3`（共有） |
| カウンタ | `+36 = N` / `+37 = 3N+4` / `+38 = 2N` |

**上限は `+37 + 7 > 32` より N <= 7。**

**★索引もバイトオフセットも全部 Python 側で計算して表に入れる。**
ケーブ側に整数→float 変換（VFP）が要らなくなる。

## 6. フォントアトラス

64x64 の LA4（4096 バイト）に 8x8 グリフを 8x8 = 64 文字ぶん並べる。

- **★設計に入る前に必ず `RE/TODO.md` と `RE/FINDINGS.md` を読む。**
  解析のときだけでなく**実装方針を決めるとき**も読む。
  （F-202: 「UI はレイアウトごとに別リストへ記録される」と自分で書いていたのに、
  その含意「**状態もサブリストの中にある**」を設計に反映できず、
  メインリストの末尾に積んで何も描かれずクラッシュさせた）
- **文字部分 = `0xFF`（L15/A15）、背景 = `0x00`（L0/A0）**
- タイリング: `byte = tile*64 + (x0|y0<<1|x1<<2|y1<<3|x2<<4|y2<<5)`、
  `tile = (y>>3)*(幅>>3) + (x>>3)`
- 列 `k` の UV = `(k/8, 1.0, (k+1)/8, 1-1/8)`

**インクの色は頂点カラーで変えられる。**
ドロップシャドウは同じ文字を少しずらして暗い色でもう 1 枚描く。

## 7. GPU 可視バッファ

`PATCHES/cave_gfxalloc_probe.py` で `g_GfxAllocator`（`0x94CA30`）から確保。
**リニア FCRAM なので `PA = VA - 0x10000000`。**
ゲームの UI テクスチャは VRAM にあり、GDB スタブからは読めない（F-191）。

## 8. 道具

| ファイル | 用途 |
|---|---|
| **`PATCHES/cave_draw_sprites.py`** | **現行版。**N 枚・フォント・最前面 |
| `PATCHES/cave_own_batch.py` | 1 枚版（読みやすい最小形） |
| `PATCHES/cave_add_sprite2.py` | 相乗り版（バッチを分けない）。切り分けフラグが充実 |
| `PATCHES/probe_vertex_color.py` | ゲーム自身が色を使う瞬間を捕獲 |
| `PATCHES/cave_gfxalloc_probe.py` | GPU 可視バッファを確保 |
| `run_timed.py` | N ミリ秒だけ走らせて自動停止 |

## 9. 次にやること

- **TODO-128**: SD カードから実際の画像を読む
- **TODO-129**: 8 枚を超えるスプライト（フラッシュを繰り返す）
- **TODO-130**: CTRPF プラグインへ移植（`DOCS/ctrpf_plugin.md`）

## 10. 進め方の教訓

**複数の値を同時に動かして誤診を繰り返したのが最大の遠回り。**
1 変数ずつ動かし、版ごとの差分を表にすること。
**動作実績のある構成をそっくり真似て、変える変数を 1 つに絞る**のが最短だった。
判定用のテクスチャは「効いていない」と「指定を間違えた」を区別できる形にする
（市松模様ではなく 4 象限で輝度を変える、など）。

---

# ★★★自前 GUI 描画の土台が完成（F-163〜F-169, 2026-08-30）

**自前で確保したメモリに自前で詰めたテクスチャを、自前サイズの四角形に貼って表示できた。**

| 要素 | 手段 | 出典 |
|---|---|---|
| GPU 可視メモリの確保 | `g_GfxAllocator->Alloc(size, 0x80)` をフック内から | F-164/165/166 |
| 物理アドレス | `PA = VA - 0x10000000`、reg `0x085` は `PA >> 3` | F-124/166 |
| テクスチャの詰め方 | 8x8 タイル + Morton、A4 は下位ニブル先 | F-124/125 |
| 四角形の位置と大きさ | `c[0x40+2k+1] = (幅, 高さ, X, Y)` | F-167/168 |
| テクスチャの貼り替え | `reg 0x085` / `0x082` / `0x08E` と UV | F-169 |

## ★グリフに頂点データは無い（F-167）

テキストの batch に **`reg 0x200`-`0x226` は 1 つも入っていない。**
頂点シェーダの float 定数から四角形を生成している。

```
c[0x40 + 2k]     = (u0, v0, u1, v1)     UV。0..1
c[0x40 + 2k + 1] = (幅, 高さ, X, Y)      レイアウト単位。高さは負
reg 0x228 NUMVERTICES = 6 * グリフ数
reg 0x22E DRAWELEMENTS = 1
```

## 書き換え方

コピー先 = `cursor + 0x60`（`TextBatch_CopyToCommandBuffer` の 0x60 バイトヘッダの後）。
そこからソースのワード番号 x4 でアクセスする。

- **1 枚目（ゲーム本来）を書き換える**なら `R9 + 0x60` 起点
- **2 枚目を追加する**なら `CopyToCommandBuffer` に渡した cursor + 0x60 起点

主なワード番号（`decode_text_batch.py` で対象ごとに引き直すこと）:

| ワード | 内容 |
|---|---|
| 36 / 37 | `reg 0x08E` 形式（`0x0B` = A4） |
| 40 / 41 | `reg 0x085` テクスチャ物理 >> 3 |
| 42 | `reg 0x082` 寸法 |
| 60,62,63,64 | UV |
| 65,66,67,68 | 幅, 高さ, X, Y |

## ★実験の作法

**位置を動かす実験では、まず大きさだけを変えて位置は据え置く。**
`(X, Y)` は pane の変換行列に対する相対座標なので、大きく動かすと
画面外やシザー矩形の外に出て「描けていない」と誤診する（F-168 で実際に踏んだ）。

**ケーブに `.bss` のカウンタを持たせ、「総呼び出し回数」と
「対象一致回数」を分けて数える。** これで「動いていない」を早く消せる。

## 残っている本質的な課題

**TextBox に依らない発行点**（TODO-115）。
現状は既存のテキスト描画に相乗りしているので、
対象の TextBox が描かれる場面でしか出せない。

---

# ★★CTRPF プラグインから描く場合（F-163 / F-164 / F-165, 2026-08-30）

詳細は **`DOCS/ctrpf_plugin.md`**。要点だけ:

## プラグインからは GPU 可視メモリを確保できない

実機で全滅。`svcControlMemory(MEMOP_ALLOC_LINEAR)` すら
`0xD86007F3` = **Kernel / OutOfResource / OutOfMemory / Permanent**。
ACNL が起動時にメモリ予算を使い切っているため。
**libctru のヒープ初期化とは無関係で、直呼びでも同じ。**

`GSPGPU_FlushDataCache` の失敗（`0xD8E007F7` = InvalidHandle）は別問題で、
`svcFlushProcessDataCache(CUR_PROCESS_HANDLE, addr, size)` で回避できる。

## 代わりにゲームのアロケータを呼ぶ

```
g_GfxAllocator (0x0094CA30) : ssys::ma::Allocator
  +0x04  sead::ExpHeap*
  vtable +0x08 = Alloc(size, align)   -> 0x569B54
  vtable +0x0C = Free(ptr)            -> 0x569B44
```

**decompiler は両方とも引数を落とす。assembly を見ること。**
`Alloc` は `R2`(align) が残るので `heap->alloc(size+align, align)`。
`Free` は `BX R2` のテール呼び出しで `R1`(ptr) が素通し。

フックから `Alloc(size, 0x80)` を呼べば **GPU が実際に読めるメモリ**が得られる。
**実機で証明済み**（F-166: フォントアトラスの記述子を自前バッファに向けたら
上画面の時計の時分 4 文字が塗りつぶされた四角になった）。

```
PA = VA - 0x10000000
reg 0x085 に入れる値 = PA >> 3
```

`nw::font::ResFont` の記述子 `table + 0x14*i + 0x08` が PA>>3 を持っており、
**毎フレーム読まれる**ので書き換えるだけで差し替えられる。
読み取りは `scratchpad/dump_glyph_atlas.py`、適用/復元は `PATCHES/font_atlas_redirect.py`。

**検証の注意:** 上画面の時計 UI は一定時間操作しないときにだけ出る。
動いている間は上画面に UI が何も描かれていない。
「常に見えているはず」を前提に検証を組まないこと。

## ★メモリ領域の使い分け（最重要）

| 領域 | ケーブから | 用途 |
|---|---|---|
| `.text` `0x00838080`〜 | **実行・読みのみ。`STR` は SIGSEGV** | コード、リテラル、表 |
| `.bss` `0x009B0000`〜 | **読み書き可** | ログ、観測、状態 |
| `g_GfxAllocator` の払い出し | 読み書き可・GPU 可視候補 | 頂点／テクスチャ／コマンド |
| `0x01E81000` の頁 | **boot によって未マップ。使わない** | — |

## ビルド

**Git Bash から `make` を呼ばない。** 環境変数が msys2 の make に届かない。

```bash
/c/devkitPro/msys2/usr/bin/bash -lc 'cd "/a/Disassemble/acnl/Plugin/CTRPluginFramework-BlankTemplate-0.8.0" && make'
```

---

# ★★★達成（F-162, 2026-08-30）— 「好きな位置に好きなテキストを好きな色で」が通った

実機の会話ウィンドウに **4 つの「テスト」**を出した。

| | 文字列 | 位置 | 色 | 発行者 |
|---|---|---|---|---|
| 元の名前欄 | 我々 | ゲーム | 緑 | ゲーム |
| 左上 | 我々 | 我々 (-150, 90) | 赤 | **我々** |
| 右上 | 我々 | 我々 (120, 90) | 水色 | **我々** |
| 左下 | 我々 | 我々 (-150, -90) | 黄 | **我々** |

## 構成 — 独立した 2 つのフック

| 要素 | フック | ケーブ | スクリプト |
|---|---|---|---|
| 文字列 | `nwlyt_TextBox_SetString` `0x4BACBC` | `0x00838400` | `PATCHES/cave_textbox.py` |
| 描画発行・位置・色・枚数 | `0x4B7DCC` | `0x00838140` | `PATCHES/cave_text_emit.py` |

## `0x4B7DCC` が特別な理由

`TextBox_EmitBatchToGpuCommands` 内、`TextBatch_CopyToCommandBuffer` から戻った直後。
ここでは必要なものが**全部レジスタに生きている**:

```
R0 = 進んだ cursor        R4 = 完成済み submit descriptor
R5 = drawctx              R6 = textbox
R9 = プリフィックス直後の cursor
```

- `desc+0x44` のクリアは `0x4B7DDC` まで起きない
  → **自前で `0x4A` バイトの descriptor を組む必要がない**（F-156 の計画は不要だった）
- プリフィックス 16 ワードは `[R9-64, R9)` にある → **複製して平行移動だけ差し替えられる**
- `R1/R2/R3/R7/R8/R12` は以降どこからも読まれない → 自由に使える
  （`R7/R8` は関数末尾の `POP {R4-R9,PC}` が呼び出し元の値を復元する）

## 1 枚描く手順

1. `[R9-64, R9)` の 16 ワードを cursor へ複製
2. 複製の `matrix[3]`（= `cursor-40`）に X、`matrix[7]`（= `cursor-24`）に Y を書く
   — **ずらすのではなく絶対位置**。`+X` 右 / `+Y` 上、単位はレイアウト px
3. `desc+0x04` に色を書く — u32 で **`0xAABBGGRR`**（メモリ上 R,G,B,A 順）
4. `TextBatch_CopyToCommandBuffer(desc, cursor, 0)` を呼ぶ。戻り値が次の cursor

`a3 = 0` が安全なのは `batch+9` の bit1 が 0（直接コピー経路）のときだけ。
会話 TextBox は 3 つとも 0。これで F-154 の SIGSEGV を回避できる。

## ★踏みやすい罠（全部このセッションで実際に踏んだ）

1. **`.text` は RX。ケーブ内から `.text` へ `STR` すると落ちる**（F-161）。
   GDB 経由では書けるので気付きにくい。**書き込み先は RW 領域に置く**
2. **`0x01E81xxx` は boot によって未マップ**（F-161）。使う前に
   `DEADBEEF` を書いて読み戻す検証をすること。
   恒久ケーブは **`.text` 末尾のゼロ埋め `0x00838018`**（`0xFE8` バイト、外部分岐 0 件）
3. **`SetString` フックは即座には効かない。** 会話の最後のメッセージで発火する（F-162）。
   変化しないことを「効いていない」と即断しない
4. **`matrix[3]/matrix[7]` は絶対位置**なので、狙った位置に置くには基準値が要る。
   `T_nam_00` は `(-126.0, -5.0)`
5. **改版のたびに未実行の番地へ移す**（F-155a の I-cache 制約）。
   パラメータをテーブル化しておけば、値だけ更新でき番地を消費しない

## 残っていること

- **TODO-115** TextBox の有無に依らず描く（今は会話ウィンドウが出ている間だけ）
- **TODO-114** 自前 batch を組んで字形・容量・発火タイミングの制約を外す
- **TODO-116** `.text` のケーブは IPS で恒久化できる

---

### ★★最新チェックポイント（F-156, 2026-08-29）

**F-155a の observer は不要になった。submit descriptor を静的に全導出した。**

`TextBatch_CopyToCommandBuffer`(`0x4D520C`) が読む descriptor は次の 7 フィールドだけ
（アセンブリで裏取り済み）。span は `0x4A` バイト。GPU から見える必要はない。

| offset | 内容 | 出所（TextBox から） |
|---|---|---|
| `+0x00` / `+0x04` | 色 2 つ（reg `0x11B` / `0x133` へ） | `+272` / `+276` |
| `+0x18` / `+0x1C` | 文字色 上 / 下 | `+216` / `+220` |
| `+0x20` | グラデーションフラグ 0/1/2 | 2 色が違えば 2 |
| `+0x44` | **batch ポインタ**（`batch+0x1C`==0 なら即 return） | `+260` |
| `+0x49` | alpha 倍率 | `+181` |

**さらに重要: `a3`(DrawContext) は `batch+9` の bit1 が立つ経路でしか使われない。**
会話 TextBox は bit1 クリアの直接コピー経路（F-145 実測）なので、
`a3=0` で呼べばどちらの経路でも range bookkeeping を触らない。
**F-154 の SIGSEGV の正体はこの bookkeeping の二重更新だった。**

実装手順:

```
1. cave に 0x4A バイトの descriptor 領域を確保
2. 対象 TextBox から上記 7 フィールドをコピー
3. TextSubmitDesc_ExpandCornerColors(0x4D5418) を呼ぶ（色を入れた後）
4. TextBatch_CopyToCommandBuffer(desc, cursor, 0) を呼ぶ
5. 戻り値が新しい cursor
```

**`TextBox_EmitBatchToGpuCommands` も `TextBox_Draw` wrapper も呼ばない。**

静的のみで**実機未検証**。適用は fresh boot 後、または
この boot で一度も実行していない cave アドレスを使うこと。

### ★前チェックポイント（F-155a）

submit descriptorを採るobserver初版は、native関数へ入る前のcave `0x01E81A54`でSIGSEGVした。
原因はdescriptorを保持するR0をfield値で上書きし、その値を次のbaseとして連鎖参照した実装ミス。
hookをstockへ戻し、stack保存済み引数・SP・LRを復元して`PC=0x004D520C`からResumeし、
**ユーザーがゲームの正常復旧を確認済み**。hook/cave/bufferはResume前にstock/zeroへ戻した。

descriptorの値は取得できていない。修正版はR0を保持してR12へfieldを読む形に直し、140-byteの
generator auditも通るが、`ALLOW_TRACE_INSTALL=False`で適用を禁止してある。旧版caveを実行した
同一bootではI-cache不整合を避けるため再注入しない。次エージェントはdebugger stateを読み直し、
試す場合もfresh boot／再attach／会話表示／Suspend／BP 0件を確認してから行うこと。

`CLAUDE.md` のルールは全て有効。特に以下は必ず守る。

- 静的解析は **idalib-mcp**（`code.bin.i64` / セッション `acnl_code` / `run_auto_analysis=true`）
- 動的解析は **ida-pro-mcp**
- **走らせるときは必ず `run_timed.py`**（後述。これを使わないと詰む）
- 進数は必ず `0x` 付き。数値変換は暗算せず `int_convert` を使う

---

## 1. このセッションで到達したこと

**当初の目標「GPU 命令を使ったテクスチャ・テキストの描画」は達成済み。**
さらにユーザーの追加目標「好きな位置に好きなテキストを、フォントと装飾を変えて描画」も
達成し、フォント差し替え・CMAP fallback・filter・折り返しまで解析済み。

| 達成項目 | 根拠 | 実装 |
|---|---|---|
| 自前 `g3d::FuncNode` の生成・毎フレーム実行 | F-119 | `PATCHES/cave_own_funcnode.py` |
| 自前コールバックから画面へ描画 | F-120 | 同上 |
| 積まれたコマンドの解釈・書き換え | F-121 | 同上（`CB_MODE="scale"`） |
| **ゲームの描画関数を一切呼ばない自己完結描画** | F-122 | 同上（`CB_MODE="own2"`） |
| テクスチャの実体特定と差し替え | F-123 | `scratchpad/tex_patch.py` |
| **任意フォーマット・任意画像の表示** | F-124 | `scratchpad/tex2_patch.py` |
| **テキスト描画（3D 空間）** | F-125 | 同上 |
| **2D テキスト（UI 層）** | F-126 | `PATCHES/cave_textbox.py` |
| テキストの位置・色の制御 | F-127 | 同上 |
| **ドロップシャドウの正体解明** | F-128 | 同上 |
| **live ResFont差し替え・CMAP fallback・LINEAR/NEAREST** | F-129/F-130 | `PATCHES/textbox_font_swap.py`, `resfont_filter_once.py` |
| **TextBox折り返しとglyph quad境界** | F-131 | 静的IDB + `dump_clock_textboxes.py` |
| ResFont atlas / descriptor / handle 分岐 | F-133/F-134 | `code.bin.i64` 静的解析 |
| `code_runtime` との独立 byte/xref 照合 | F-135 | 6関数・vtable・magic文字列・loader caller。live実機ではない |
| atlas range request の再監査 | F-136 | `0xFFFF8001` は process handle、IPC header は `0x001F0082`。既知の `0x13B6A4` と同一視しない |
| glyph texture parameter 引数の再監査 | F-137 | `0x4D8484` は decompiler 表示より多く width/height/format/raw を使い、`0x7ABDBC` へ渡す |
| ida-pro-mcp 実機接続経路の復旧 | F-138 | RPC `127.0.0.1:13337` は正常。`--ida-rpc` 固定の proxy を `.codex/config.toml` に追加。Codex再起動後に直結namespaceがロードされる |
| ResFont→CMAP→batch quad の実機照合 | F-139 | `0x743768` の `U+904A→0x0A01`、`0x4D4EAC` の descriptor付きbatch instanceを採取。`0x4D5118` は未到達 |
| 会話 TextBox の batch command 生成・入口 | F-144 | `0x4BAFFC` で「あんこ」、`0x4B7CE0` で glyph count=3 / command count=`0xB6` を採取 |
| TextBox batch→専用list→メインlist | F-145 | sourceと`R1+0x60`の632-byte一致。list 32へ構築後、recorded range `0x3270`をメインlist 1へ再生することを実測 |
| TextBox batch sourceの内訳 | F-146 | `0x8ADA30`固定0x60-byte seedがlive source先頭と一致。後段はglyph/state block、submit header色とは別物 |
| Pictureの2D UI経路 | F-147 | Picture slot `+0x68`がcursorをPane treeでthreadし、会話PictureもTextBoxと同じlist 32 record/replayへ載る。panelはworld FuncNodeでなくUI listへ |
| **submit descriptor の静的全導出** | **F-156** | observer 不要。`a3=0` で bookkeeping 回避 |
| **自前2D本文panel** | **F-149** | 背景2枚・縁4枚・`T_msg_00`を非所有cloneし、元からのtranslation差分を維持してcommit前に追加。実機で整列を確認。話者名は未追加。`PATCHES/cave_ui_picture_clone.py`（boot限定） |

**7px fallback glyph右端のcontrolled testは完了（F-132）。**

---

## 2. 実機・IDA の状態（引き渡し時）

| 項目 | 状態 |
|---|---|
| 3DS / IDA | Remote GDB接続中。F-155aからのResumeで正常復旧をユーザー確認済み。現在のrunning/Suspend状態は未再取得 |
| パッチ | F-149を含む診断用パッチはstockへ復元済み。F-155a observer hook/cave/bufferもstock/zero |
| フック | `0x28FE0C` = `0xE92D4010`、`0x4BACBC` = `0xE92D4070`（どちらも素） |
| テクスチャ | 2 枚とも原本に復元済み |
| マテリアル | アイテム名の 2 枚とも原本に復元済み |
| breakpoint | 復旧直前の確認では0件。次エージェントは開始時に再確認すること |
| `code.bin.i64` | F-148のcommit境界commentまで保存済み。idalibセッションはclose済み |

再起動後の `0x00100000` 先頭と既知hook 2箇所は静的IDBと一致。breakpoint 0件。
live ResFont/TextBoxも再探索済み。旧起動のpointerを検証なしに使わないこと。

### F-149 中断チェックポイント

- `PATCHES/cave_ui_picture_clone.py` は本文フレーム（背景2＋縁4）と `T_msg_00` の成功版。
  **現在はuninstall済み**で、`0x4D71B8=0xE8BD4070`、`0x01E81000-0x01E81947`、
  `0x01E81A00-0x01E81C57` は全てzero、BP 0件。
- 次の最小作業は、会話途中で `P_nam_00` / `P_nam_01` / `T_nam_00` を再照合し、本文と同じ
  background-relative delta方式で名前欄を追加すること。名前TextBoxの既存batch再生は未実証。
- 3DS再起動後はこのscriptの `SRC_*` runtime pointerを絶対に再利用しない。
  `trace_picture_range.py`等で当該会話layoutを再取得し、vtable/name/batch検証を通す。

---

## 3. ★必ず使う道具

### `run_timed.py` — N ミリ秒だけ走らせて自動停止

**これを使わないと詰む。**
ida-pro-mcp の要求は**デバッガが RUNNING の間は一切処理されない**。
`server_health`（疎通確認だけ）すらタイムアウトする。
つまり**走り出したあとに外から止める手段が無い**。

```
RUN_MS を編集 → py_exec_file("A:/Disassemble/acnl/run_timed.py")
→ 次の py_eval で state == -1 を確認してから読み出す
```

`ida_kernwin.register_timer` で「止まる予約」を入れてから `continue_process()` する仕組み。
bp が先にヒットすればそこで、しなければ時間切れで必ず停止する。

- `RUN_MS` は **30 秒より十分短く**（次の呼び出しは対象が止まるまで待つため）
- 1 フレームに 1 回しか通らない場所に bp を張るなら `RUN_MS` を大きめに
  （1500ms で未ヒット、5000ms でヒットした実例がある）
- ユーザーに画面を見てもらうときは 15000〜45000 を使う

### パッチスクリプト

| ファイル | 用途 |
|---|---|
| `PATCHES/cave_own_funcnode.py` | **自前 `FuncNode` で 3D 描画**。6 フラグで全実験を再現 |
| `PATCHES/cave_textbox.py` | **UI の 2D テキスト**。`trace` / `dump` / `install` / `uninstall` |
| `PATCHES/textbox_font_swap.py` | TextBox 1枚のlive ResFont差し替え。現在`MODE="status"` |
| `PATCHES/resfont_filter_once.py` | ResFont filter 2bitを1回だけ変更。現在`MODE="status"` |
| `PATCHES/cave_scene_node_dup.py` | シーンへノードを追加する最小実験 |
| `scratchpad/dump_shadow_cmds.py` | 積まれたコマンド列をファイルへ吸い出す |
| `scratchpad/tex_patch.py` | 32×32 テクスチャの保存 / 縞 / 復元 |
| `scratchpad/tex2_patch.py` | 32×64 テクスチャの保存 / 市松 / テキスト / 復元 |
| `scratchpad/capture_batch_submit.py` | `0x4D520C` のbatch→GPU command buffer入口を読み取り専用で採取 |
| `scratchpad/trace_text_batch_submit.py` | 会話名TextBoxのbatchだけを止めずに採取。F-145後はuninstall済み |
| `scratchpad/trace_layout_list_replay.py` | source list 32のメインlist再生と直接Split回数を採取。F-145後はuninstall済み |

---

## 4. 2 つの描画方式（用途が違う）

### 方式 A: 影のパイプラインを借りる（3D 空間）

**ワールド空間の地面に描かれる。** 任意の絵を任意の形で出せるが実装が重い。

```
一度だけ:  g3d_FuncNode_Create(&holder, *g_GfxAllocator)   0x4EFFB4
           g3d_FuncNode_SetCallbacks(&holder, 0, cb1, ud)  0x4EFF58
毎フレーム: Scene_SubmitNode(&holder, sceneIndex)           0x4ED630

コールバックの中身（完全自己完結版 = 4560 バイト）:
  p = GpuCmd_GetProperty(0x208)                    0x127EDC
  Mem_CopyBytes(p,        *(mgr+0xB4), 4128)       0x12EC54  既製ブロック
  Mem_CopyBytes(p + 4128, TEMPLATE,     432)                 自前テンプレート
  GpuCmd_Advance(4560)                             0x1280B4
```

フック先は `BsShadowViewMgr_SubmitToScene`(`0x28FE0C`)。毎フレーム 1 回だけ通る。

**テンプレート 432 バイトの中身**（カテゴリ設定 + インスタンス描画）:

| reg | 決めるもの |
|---|---|
| `0x200`〜`0x205` | 頂点バッファの基底・書式・オフセット・ストライド |
| `0x082` | テクスチャの大きさ（bits0-10 高さ / bits16-26 幅） |
| `0x083` | フィルタ(bit1,2) / **ETC1 フラグ(bit5)** / wrap(bits8-9, 12-13) |
| `0x085` | **テクスチャのアドレス**（`<<3` で物理） |
| `0x08E` | フォーマット（`0x0C`=ETC1 / `0x0A`=L4 / `0x0B`=A4） |
| `0x0C3` | 色（最上位バイトがアルファ） |
| `0x2C0`/`0x2C1` | **3×4 行列**（uniform 25、**`w,z,y,x` 順**） |
| `0x227`/`0x228` | インデックスバッファ / 頂点数（6 = 四角形） |
| `0x22F` | 描画発火 |

**テクスチャの仮想アドレス = 物理 + `0x10000000`**（実測で確定）。
カテゴリごとにテクスチャと寸法が違う（32×32 と 32×64 の 2 種類を確認）。

### 方式 B: UI 層に乗る（2D）★こちらが軽い

**画面座標のオーバーレイになる。ゲーム内蔵フォントが使える。わずか 9 ワード。**

`nwlyt_TextBox_SetString`(`0x4BACBC`) の先頭 1 ワードを `B ケーブ` に差し替え、
引数の文字列ポインタを自前のものに置き換える。

```asm
LDR  R12, =TARGET_THIS    ; 対象の TextBox（this）
CMP  R0, R12
BNE  pass                 ; 違えば素通し（他の UI は無傷）
  LDR R1, =MYSTR
  MOV R3, #len
pass:
PUSH {R4-R6,LR}           ; 元の 1 命令
B    0x4BACC0             ; 続きへ（LR は変えていないので戻り先は同じ）
```

---

## 5. ★`nw::lyt::TextBox` の構造（実機で確定）

| offset | 型 | 内容 | 備考 |
|---|---|---|---|
| `+40`/`+44`/`+48` | float | **位置 translate x,y,z** | 書けば動く |
| `+52`〜`+60` | float | 回転 | 未検証 |
| `+64`/`+68` | float | 拡大率 | 未検証 |
| `+72`/`+76` | float | ペインのwidth/height | **widthは自動折り返し幅。heightは文字描画をclipしない** |
| `+184` | char[8] | **ペイン名** | `T_` = 本文 / `S_` = 影 |
| `+212` | ptr | 文字列バッファ `wchar_t*` | 直接書いても戻される |
| `+216`/`+220` | RGBA | **文字色（上/下）** | バイト順 R,G,B,A |
| `+224` | ptr | **フォントオブジェクト** | 非 0 でないと即 return |
| `+228`/`+232` | float | フォントサイズ（幅・高さ） | Font metricsから独立した描画scale |
| `+236`/`+240` | float | 文字間隔・行間隔 | writerへそのままコピー |
| `+248` | u16 | バッファ長（バイト）。`/2-1` が最大文字数 | |
| `+250` | u16 | 現在の文字数 | |
| **`+254`** | u8 | **bit0 = 更新フラグ** | **立てないと反映されない** |
| `+256` | ptr | マテリアル。その **`+20` が乗算色** | |

**最終的な色 = 文字色(`+216`/`+220`) × マテリアル `+20`**（実機で三段階に検証）

### ドロップシャドウ（F-128）

**フォント側でも専用処理でもない。同じ文字列の `TextBox` を 2 枚、1 ドットずらして描いている。**

| | ペイン名 | 位置 | 乗算色 |
|---|---|---|---|
| 本文 | `T_itm_na` | (0, 0) | `00 2d 46 ff` |
| 影 | `S_itm_na` | **(1, -1)** | `ff ff ff ff` |

したがって装飾は次で完全に制御できる。

- **影の色** … 影ペインのマテリアル `+20`
- **影のずれ** … 影ペインの `+40`/`+44`
- **影の有無** … 影ペインを潰す
- **`S_` で始まるペイン名を探せば影が見つかる**

---

## 6. ★次にやるべきこと

### ★完了: 7px fallback glyph右端のcontrolled test（TODO-101 / F-129〜F-132）

`+224` は **`nw::font::ResFont*` と確定**。実機には少なくとも次の4種がある
（アドレスは現在の起動のみ）。

| runtime | CFNU metrics | 本来の用途 |
|---|---|---|
| `0x3302ABE0` | 24 / 18 / 18 | 通常UI、日本語本文 |
| `0x3302AD78` | 7 / 7 / 5 | `RT_`/`RS_` のルビ用と推定 |
| `0x3302AF10` | 40 / 35 / 29 | 未特定 |
| `0x3302B0A8` | 26 / 24 / 17 | ベル・個数カウンタ |

時計本文 `T_time_0` 1枚だけを通常版→7px版へ差し替えると、数字が2個の
`U+3041「ぁ」` fallbackへ変わり2行になった。影は未変更。**TODO-98は完了**。

counter26版では本文が `07` と正しく1行表示された。字形の骨格は影と同じだが黒縁があり、
minute `03` より少し左上へ見えた。`+224` 以外は未変更なのでbuffer/pane座標の変更ではなく、
font資源の輪郭とメトリクス差。試験後は通常版 `0x3302ABE0` へ復元し、5秒描画済み。

`scratchpad/dump_font_maps.py` でCMAP/CWDHを直接読んだ結果、7px版は `0/6/7` が全て
`0xFFFF`（欠落）、alternate glyph 0は正確には `U+3041「ぁ」`。この点は確定。
全4フォントの `ResFont+16` はstock `0x6`。両bit OFFの直接試験で拡大glyphが
ぼやけた表示からくっきりしたドット表示へ変化したため、`0x4D7474` は
`nwfont_ResFont_SetLinearFilter` と確定（F-130 HIGH）。試験は完全復元済み。

折り返しも静的に確定した。時計pane widthは26。7px glyphのadvance 7を要求幅18へ
拡大すると1文字18、2文字36なので、`nwfont_TextWriter_DrawString` (`0x7E7FA4`) が
2文字目の前でsynthetic newlineを出す。pane height 21.6はwriterへ渡らないため、
2行目はTextBox内でclipされず、そのまま物理画面下端の外へ出る。

当初の残件だったglyph右端1〜3pxはcontrolled testで解決した。`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) は
CWDH `glyphWidth`をquad幅とtexture U右端の両方に使う。7px fallbackは
`cellWidth=7 / glyphWidth=6 / advance=7`。要求幅18では本体15.43px、advance18pxで、
1 source pixel相当の約2.57pxが境界になる。**文字列bufferやpane越境ではない。**

第1比較（7px NEAREST、要求size 18 x 24、pane width 26→40）は実機で一行化を確認済み。
続く第2比較ではpane width40と7px NEARESTを維持し、要求sizeだけ14 x 14へ変更した。
これは7px glyphの横・縦2倍の整数scaleである。font/CWDH/string/pane/filterを固定した
A/Bの結果、整数倍率では右端の欠け・不均一さが改善し、字形自体に異常はなかった。
従って症状はbuffer越境ではなく、非整数scale `18/7` を最近傍補間した端部境界・丸めの
見え方が主因と確定した（F-132）。CWDH `glyphWidth=6`→7またはnative7x7への改変は不要。

比較後は `textbox_font_integer_scale_test.py` uninstall → `textbox_font_width_test.py` uninstall
→ `resfont_filter_once.py` set_linear → `run_timed.py` → filter cleanup の順で復元した。
実機読み戻し: `T_time_0 +224=0x3302ABE0`, pane width `26.0`, size `18 x 24`,
7px `ResFont+16=0x6`, hook `0x28FE0C=0xE92D4010`, process Suspend。

採取・確認用:

- `PATCHES/cave_textbox.py`: `trace_fonts` / `dump_fonts` を追加。現在は `uninstall`
- `scratchpad/scan_resfonts.py`: `0x33000000` の1 MiB限定走査
- `scratchpad/scan_textboxes.py`: UIヒープを1 MiBずつ走査
- `scratchpad/inspect_resfonts.py`: CFNU/FINF/TGLPの実体確認
- `scratchpad/dump_glyph_atlas.py`: live ResFont/TGLP/descriptor を再走査してダンプ（読み取り専用）

### ★追加: ResFont glyph atlas の静的再監査（F-133〜F-139）

`nwfont_ResFont_ParseAndAttachResource` (`0x4D8048`) が `CFNU/CFNT` を検証し、
`FINF/CMAP/CWDH/TGLP/GLGR` のオフセットを再配置して `ResFont+4/+8` に保存する。
TGLP の重要フィールドは `+4`=sheet stride、`+8`=sheet count、`+0A`=texture format、
`+0C/+0E`=columns/rows、`+10/+12`=sheet width/height、`+14`=raw atlas pointer。

glyph-sheet descriptor は 0x14 bytes。`0x13C518` が配列を保存し、`0x1426C8` →
`0x141B48` が sheet ごとに `+0` handle、`+4` owner、`+8` `sub_143B54(raw)>>3` のアドレス変換済みGPU表現、
`+C/+E` height/width、`+10` format を設定する。raw atlas 全体は `0x143718`→`0x144C44` の
IPC header `0x001F0082` へ渡される。`0xFFFF8001` は `dword_8AD218` の process handle
値であり command ID ではない。既知の `GSPGPU_FlushDataCache` (`0x13B6A4`, header
`0x00080082`) とは header が異なるため、`0x143718` の正確な cache semantics は未確定とする。

native glyph draw は `0x7438B4` (`GetGlyph`) → `0x4D4EAC` (quad/UV) →
`0x4D8484` (texture setup/state) → `0x7A7FAC` (generic draw) の順。F-139 で live
`ResFont*`、CMAP入出力、glyph record、batch instanceを読み取り専用で確認した。
texture handle の生成時点、自前 GPU callback から descriptor を直接参照する後段 submit、
`0x4D8484` backend の GPU bind 完了時点は未検証であり、次はそれらを分離して観測する。

F-134 の追加確認では、descriptor `+0` の texture handle は 0 のときだけ
`sub_7A8B08(1,&local)` で遅延生成され、`sub_7A6558(3553,handle)` で bind されること、
writer `+0x44` の batch 経路は texture bind せず 0x2C-byte instance を後段へ渡すことを
静的に確定した。自前実装は当面 descriptorありの immediate 1 glyph に限定する。

F-135 の再監査では、`code.bin.i64` と実機コードダンプ由来の
`code_runtime.elf.i64` を同時に開き、parser / EmitGlyphQuad / descriptor loop / descriptor init /
sheet-table size / texture-parameter の6領域（計6関数）の raw bytes を同じ VA で比較した。
全領域で差分は 0 bytes、vtable 128 bytes・`CFNU/FINF/CFNT/CMAP/TGLP` 文字列・主要 xref と
2つのfont loader callerも一致した。従ってこのビルドの命令列・関数境界・VA対応に矛盾はない。
ただし runtime IDB はライブ実機ではない。F-139 で `ida-pro-mcp` の実機メモリ endpoint を
使い、live descriptor/glyph/batch instance の値を確認した。texture handle の materialize と
自前 callback 再利用可否は MEDIUM/LOW のまま維持する。

F-136 で、`0x143718` の旧名と `0xFFFF8001` の解釈を補正した。`0xFFFF8001` は
command ID ではなく process handle、IPC header は `0x001F0082` であり、既知の
`GSPGPU_FlushDataCache` (`0x13B6A4`, `0x00080082`) と同一 API とは断定しない。
IDB では `nwgfx_GspGpu_RangeCacheOp_1F` / `j_nwgfx_GspGpu_RangeCacheOp_1F` と命名した。

F-137 で `0x4D8484` の decompiler 表示を assembly と突き合わせた。`0x4D5118` が渡す
width/height/format/raw sheet は本体の format switch と `0x7ABDBC` generic texture setup
dispatcher に入り、wrap/filter state も続けて設定される。従って filter-only と解釈しない。
ただし backend の実 GPU side effect と format enum は動的未確認で、確度は MEDIUM のままとする。

### F-139 実機動的照合（2026-08-28）

会話表示中の `tid=219` で `0x743768` に停止し、`R0=0x3302ABE0`、`R1=0x904A`、終端戻り値
`R0=0x0A01`、ResFont cache `+0x14/+0x16=0x904A/0x0A01` を採取した。続く `0x4D4EAC` では
writer `0x0000FC70`、glyph record `SP=0x0FFFFB10`、raw `0x318B2A80`、幅4・高さ24・
128×128・format `0x0B`、descriptor `0x319BEB70`、`writer+0x44=0x32D3A6F0`（非零）を確認。
`0x4D4FC8` で count増加後の44-byte instance `0x32D3A770`とdescriptor末尾を読み取った。
従ってこの経路はbatchで、`0x4D5118`→`0x4D8484` は呼ばれない。5秒走行後も4フォントの
descriptor handleは全て0で、lazy materializeの時点は後段submit／immediate経路に残る。

### その他の未着手

| TODO | 内容 |
|---|---|
| 99 | **解決**。折り返し・縦非clip・右端の見え方（F-131/F-132） |
| 100 | **解決**。CMAP/代替文字とLINEAR→NEAREST直接試験（F-130） |
| 101 | **解決 (F-132)**。pane width40で折り返しを除外し、18x24対14x14をA/B。整数倍率で右端症状が改善したため、CWDH改変は不要 |
| 102 | **前進 (F-139)**。live ResFont/TGLP/descriptorを採取済み。handle materializeは未確定 |
| 103 | 既存 atlas を使う一文字の native GPU callback を最小実装 |
| 104 | TextBox alignment byte と font format/filter の実値を動的照合 |
| 105 | **前進 (F-139)**。descriptor付きbatch経路を確認。handle生成・bindの後段時点は未観測 |
| 89 | 頂点/インデックスを差し替えて任意形状（3D オブジェクト） |
| 88 | 3×4 行列で任意の位置・大きさ（ワールド座標との対応） |
| 92 | GPU 可視の大バッファを確保してカラー画像 |
| 76 | `Frame_DrawPass*` が `vtbl_SystemTask` のスロットか delegate か |

---

## 7. ★次のエージェントが踏みやすい罠（全て実際に踏んだ）

1. **走行中はデバッガの要求が一切通らない。** `run_timed.py` を必ず使う
2. **タイムアウトからは何も分からない。** `PC` を見るまでフリーズと断定しない。
   `PC` が bp の位置なら正常停止。**これを 2 回誤読した**
3. **パッチ投入直後のフレームは移行フレーム。** フル 1 フレーム回してから測る
4. **ARM の即値は `imm8 ROR (2*r)`。** 自作エンコーダで回転方向を逆にすると
   `MOV R2,#432` が `MOV R2,#27` になる。**これで長時間溶かした。**
   生成した命令は必ず逆アセンブルして目視確認する
5. **PICA の f32 uniform は `w,z,y,x` 順。** 知らずに float 列を行列として読むと
   成分の意味を取り違える
6. **`TextBox` は `+254` bit0 を立てないと反映されない。**
   値は上書きされないので「書けたのに効かない」状態になる
7. **1 度に複数の項目を変えない。** 4 項目同時に変えて表示が消え、
   原因を特定できずに「位置も色も効かない」と誤結論しかけた
8. **色を試すときは背景と明確に違う色を選ぶ。**
   ピンクの欄に赤を出して「変化なし」と誤判定した
9. **推測で対象を選ばず、トレースして実データから選ぶ。**
   最初に選んだ `TextBox` は画面に出ておらず空振りだった。
   `cap = 0` の箱はバッファ未確保で描画されない
10. **A/B で片方だけ変えると報告が食い違う。**
    2 枚を緑と赤に塗り分けたら一発で確定した

11. **同じ実行済みcode caveを停止中に上書きして改版しない。** 2026-08-29にRAM読戻しが
    正しい改版でもCPUは前版を実行し、`0x01E81B88`でSIGSEGVとなった。GDB memory writeは
    ARM I-cacheを同期しない場合がある。修正版を試す前にタイトルを再起動して再attachし、
    runtime pointerも再取得する（F-150 / TODO-114）。

12. **TextBox cloneにはnative descriptorを渡す。** `T_msg_00`を直接traceしたF-151で
    `TextBox_Draw(0x73CF48)` のR2は`0x330A605C`、R3は`0x32FF62EC`だった。前者は
    `TextBox_EmitBatchToGpuCommands`の第5引数になり、`+0x80`は有効pointerである。
    commit hookのR6をこれの代わりに渡すと`0x4B7D50`でSIGSEGVする。

13. **commit hookから`TextBox_Draw` wrapperを呼ばない。** F-152でdraw contextがlayout recordを
    再入し、`GpuCmd_SelectList(0x1216DC)`を壊した。batchが既にreadyなら後段
    `TextBox_EmitBatchToGpuCommands(0x4B7CE0)`を直接呼ぶ。ABIは
    `R0=drawctx,R1=cursor,R2=clone,R3=clone+0x100,[SP]=descriptor`。

14. **direct-emitter版は適用前に必ずgenerator auditする。** `PATCHES/cave_ui_picture_clone.py`
    の`MODE=audit`は書込みなしでBL target数、TextBox ABI setup、cave mapを検査する。
    F-153でbody=744B、aux=168Bは合格したが、実機検証まではMEDIUMである。

15. **emitter直呼びも現在は禁止。** F-154で`TextBox_EmitBatchToGpuCommands`は末尾の
    `TextBatch_CopyToCommandBuffer(..., a3=live DrawContext)`によりrange bookkeepingを二重更新し、
    wrapper版と同じ`GpuCmd_SelectList(0x1216DC)` SIGSEGVを再現した。次はprivate submit
    descriptorを作り、`TextBatch_CopyToCommandBuffer(..., a3=0)`だけを使う。

16. **F-155a: trace caveでもdescriptor読取りのレジスタを連鎖させない。** 初版observerは
    `0x01E81A54`で停止した。`R0=descriptor`をfield値で上書きして次のoffsetを読んだ実装ミスで、
    native `TextBatch_Copy`には未到達だった。元引数をstackから戻し`PC=0x4D520C`へ戻し、
    Resume後にユーザーが正常復旧を確認した。これはこの例外位置だけの手順である。
    修正版は全fieldをR12へ読み、`MODE=audit`は140Bのbranch/literal/ABIを検査する。
    旧caveを実行したbootではCPU I-cacheのため改版を実行せず、
    fresh bootでのみ `ALLOW_TRACE_INSTALL` を検討する。

---

## 8. ユーザーとのやりとりで有効だった進め方

- **ユーザーは実機を見ている唯一の目。** 観察の報告は自分の測定より信頼できる。
  「位置が右にずれた」の一言で自分の誤結論を訂正できた
- **陰性対照を取る。** 「自前ノードだけ → 影あり」だけでは足りず、
  「どちらも無し → 影なし」で初めて確定した（ユーザーの発案）
- 画面を見てもらうときは**何がどう見えるはずか**を先に書く。
  見どころを表にしておくと報告が具体的になる
- 45 秒走らせて**ユーザーに操作してもらう**とトレースが一気に集まる

---

## 9. 参照

| 文書 | 内容 |
|---|---|
| `RE/FINDINGS.md` F-110〜F-137 | 全ての根拠と経緯。誤りとその訂正も記録 |
| `DOCS/rendering.md` | 描画の完成した解説。末尾に自前描画のレシピ |
| `RE/STATE.md` 冒頭 | 実行時アドレスなど生きた状態 |
| `RE/TODO.md` 冒頭 | 残タスク |
| `RE/FUNCTIONS.md` | 関数索引 |
