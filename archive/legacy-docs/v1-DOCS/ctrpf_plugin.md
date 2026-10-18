# CTRPF プラグインから描画する

根拠は `RE/FINDINGS.md` の F-163 / F-164 / F-165 / F-166。
クラッシュ時は `DOCS/crash_recovery.md`。

---

## 1. ビルド環境（ここでつまずくと時間を失う）

| 項目 | 値 |
|---|---|
| テンプレート | `Plugin/CTRPluginFramework-BlankTemplate-0.8.0` |
| libctrpf | `C:\devkitPro\libctrpf`（`include/` と `libctrpf.a`） |
| libctru | `C:\devkitPro\libctru` |
| 成果物 | `<テンプレート名>.3gx` |

### ★Git Bash から `make` を呼んではいけない

**Git Bash で `export` した環境変数は msys2 の `make` に届かない**（実測。
`DEVKITARM` が空のまま `Makefile:4` のチェックで止まる）。
`/tmp` も両者で別物を指す。

**必ず devkitPro の msys2 ログインシェル経由で叩くこと:**

```bash
/c/devkitPro/msys2/usr/bin/bash -lc 'cd "/a/Disassemble/acnl/Plugin/CTRPluginFramework-BlankTemplate-0.8.0" && make'
```

msys2 のログインシェルは `/etc/fstab` で `c:\devkitPro` を `/opt/devkitpro` に
マウントしており、`DEVKITPRO` / `DEVKITARM` も設定済み。`A:` は `/a` で見える。

### ★★テンプレートの Makefile がリンクし直さない（実際に踏んだ）

**症状: ソースを直しても `.3gx` の中身が変わらない。**
`make` は `.o` を作り直し、`creating ....3gx` まで表示するのに、
**`.elf` の日付が更新されない。**

原因はテンプレートのこの行。

```make
$(OUTPUT).3gx : $(OFILES)        # ← 誤り
```

devkitARM の `base_rules` にある `%.elf:` ルールは**前提条件を持たない**ので、
`.elf` が一度できると make は「最新」と判断して二度とリンクしない。
`.3gx` だけが古い `.elf` から作り直され、**中身は数日前のまま**になる。

正しくはこう書く。**`.3gx` を先に書くこと**（最初のルールが既定ターゲットになるため、
`.elf` を先に書くと make が `.elf` までしか作らない。これも実際に踏んだ）。

```make
$(OUTPUT).3gx : $(OUTPUT).elf
$(OUTPUT).elf : $(OFILES)
```

**確認のしかた**: ビルド後に `.elf` と `.3gx` の日付を見る。
`linking ....elf` が出ていなければリンクされていない。
念のため成果物に新しい文字列が入っているかも見る。

```bash
ls -la --time-style=full-iso *.3gx *.elf
grep -c "CTRPF_OwnGui.txt" *.3gx
```

### ★`libctru` に `lib/` が無かった

`C:\devkitPro\libctru` は**ソースツリーで `lib/` を持っていなかった**。
ビルド済みは `C:\devkitPro\_libctru old\lib\` にあり、`include/` は両者一致していた。

ソースツリーをその場でビルドして解決した（追加のみ。`make clean` で戻せる）:

```bash
/c/devkitPro/msys2/usr/bin/bash -lc 'cd /opt/devkitpro/libctru && make -j4'
```

### plgInfo

`CTRPluginFramework.plgInfo` の `Targets` にとび森 JPN を設定してある。

```yaml
Targets:
    - 0x00086200 # とびだせ どうぶつの森 (JPN 無印)
    - 0x00198D00 # とびだせ どうぶつの森 amiibo+ (JPN)
```

配置先は SD の `/luma/plugins/00086200/`。Rosalina で plugin loader を ON。

### C++ の落とし穴

- `-std=gnu++11 -fno-rtti -fno-exceptions`
- `va_start` を使うなら `<cstdarg>` が要る
- **ローカル変数に `vramFree` のような libctru の関数名を使わない**（隠してしまう）
- ヒアドキュメントでソースを書くと `\n` が実改行になって
  「missing terminating " character」になる事故が起きやすい。
  **文字列に改行を入れないか、ファイル書き込みツールを使う**

---

## 2. ★プラグインからは GPU 可視メモリを確保できない（F-163）

**結論を先に:** 自前で確保するのは不可能。**ゲームのアロケータを呼ぶ**（3 節）。
それで GPU が実際に読めることは実機で証明済み（F-166）。

実機で検証した結果は**全滅**。

| 呼び出し | 結果 |
|---|---|
| `linearSpaceFree()` / `vramSpaceFree()` | 0 / 0 |
| `linearAlloc()` 4KiB〜2MiB | 全て失敗 |
| `linearMemAlign(0x10000, 0x80)` | 失敗 |
| **`svcControlMemory(MEMOP_ALLOC_LINEAR)`** | **`0xD86007F3`** |
| `vramAlloc(0x10000)` | 失敗 |
| `new u8[0x10000]`（対照） | VA `0x061FE170`、**PA = 0** |
| `GSPGPU_FlushDataCache` | `0xD8E007F7` |

結果コードの分解:

```
0xD86007F3 = Kernel / OutOfResource / OutOfMemory  / Permanent
0xD8E007F7 = Kernel / InvalidArgument / InvalidHandle / Permanent
```

**`OutOfMemory` は「プロセスに空き linear が無い」という意味。**
ACNL は起動時にメモリ予算を使い切る。
`linearSpaceFree = 0` は「プラグインが libctru の起動処理を通らない」ことの
確認にすぎず、**libctru を初期化しても解決しない**（`svcControlMemory` 直呼びでも同じ）。

**`GSPGPU_FlushDataCache` の失敗は別問題で回避できる。**
module が GSP でなく Kernel / InvalidHandle なので、
GSP サービスセッションが未作成なだけ。代替:

```c
svcFlushProcessDataCache(CUR_PROCESS_HANDLE, addr, size);   // サービス不要
```

---

## 3. ★代わりにゲームのアロケータを呼ぶ（F-164 / F-165）

```
g_GfxAllocator (0x0094CA30) : ssys::ma::Allocator   vtbl 0x009006A4
  +0x00  vtable
  +0x04  sead::ExpHeap*                             vtbl 0x008FFEF8
```

vtable は 4 スロットのみ。

| slot | offset | 内容 | 実体 |
|---|---|---|---|
| 0 / 1 | +0x00 / +0x04 | デストラクタ 2 種 | `0x569B74` / `0x569B70` |
| **2** | **+0x08** | **`Alloc(size, align)`** | `0x569B54` |
| **3** | **+0x0C** | **`Free(ptr)`** | `0x569B44` |

取得は `GfxAllocator_Get`(`0x4EF2D8`)。

### decompiler は両方とも引数を落とす

**assembly を見ること。**

- `Alloc`: `ADD R1,R1,R2` のあと **`R2`(align) が消えずに残る**ので
  実際は `heap->alloc(size + align, align)`。アラインメントは効く
- `Free`: `BX R2` のテール呼び出しで **`R1`(ptr) が素通し**。
  decompiler は 1 引数に見せるが実態は `Free(ptr)`

### 呼び出し方

（疑似C を省略。原本は _local/legacy-src/…）

**ゲームのスレッド上（フック内）から呼ぶこと。**

### 実測結果（F-165）

| | |
|---|---|
| `Alloc(0x1000, 0x80)` の戻り | **`0x329D8500`** |
| `0x80` 境界 | 満たす |
| linear の窓 | 中にある |
| F-124 に従った物理アドレス | `0x229D8500` |

### ★GPU 可視であることは証明済み（F-166）

`Alloc` の払い出しを **GPU が実際に読んだ**。

`nw::font::ResFont` のテクスチャ記述子

```
table + 0x14*i + 0x08  =  物理アドレス >> 3   （そのまま PICA reg 0x085 に入る）
```

を自前バッファ（`0xFF` 埋め）に向けたところ、
**上画面の時計の時分 4 文字が塗りつぶされた四角になった。**

- 記述子は**毎フレーム読まれる**（書き換えたまま走らせても戻らない）
- 読み取りは `scratchpad/dump_glyph_atlas.py`、適用/復元は `PATCHES/font_atlas_redirect.py`
- **コマンド注入もコードケーブも不要**だった

```
PA = VA - 0x10000000
reg 0x085 に入れる値 = PA >> 3
```

`VA - PA = 0x10000000` は影テクスチャ（F-124、`0x33xxxxxx`）と
フォントアトラス（F-166、`0x31xxxxxx`）という**別々のオブジェクトで一致**した。

### ★検証を組むときの注意

**上画面の時計 UI は一定時間操作しないときにだけ出る。**
動いている間は上画面に UI 系が何も描画されていない。
「常に見えているはず」を前提に検証を組まないこと（F-166 で踏んだ）。

---

## 4. ★メモリ領域の使い分け（F-161 / F-165 / F-166）

| 領域 | ケーブ／プラグインから | 用途 |
|---|---|---|
| `.text` `0x00838080`〜**`0x00839000`**（`0xF80` バイト） | **実行・読みのみ** | コード、リテラル、パラメータ表 |
| `.bss` `0x009B0000`〜 | **読み書き可** | ログ、観測バッファ、状態 |
| `g_GfxAllocator` の払い出し | 読み書き可・**GPU 可視（F-166 で証明）** | 頂点・テクスチャ・コマンドリスト |
| プラグインヒープ（`new`） | 読み書き可・**PA=0** | CPU 側のみ。GPU には見せられない |

`.text` へケーブから `STR` すると **SIGSEGV**（F-161 で実際に踏んだ）。
`.bss` は書ける（F-165 で確認）。

**★かつて「`0xFE8` バイト」と書いていたが過大だった。**
`0x839000` から実データが入っている（`"K---"` の ASCII と生きたポインタを実機で確認）。
ケーブを伸ばすときは末尾が `0x839000` を超えないか必ず検査すること（F-215）。

`0x01E81000` の頁は **boot によって未マップ**なので使わない。

---

## 5. CTRPF の 3 つの描画方式

| 方式 | 内容 | 必要な解析 |
|---|---|---|
| **A. OSD** | `OSD::Run` / `Draw` / `DrawRect` でフレームバッファへ直描き | 不要 |
| **B. ゲームの関数を呼ぶ** | ゲームの状態を組み立て、ゲームに描かせる | レイアウト生成経路 |
| **C. `Hook` で自前 GPU コマンド** | ゲームのスレッド上で自前コードを走らせる | 本プロジェクトの成果がそのまま使える |

### ★実在プラグインは OSD を使っている（F-179）

Vapecord の「マップ上に他プレイヤーを表示」機能は、
**ゲームのアイコンを複製しているのではなく、`OSD::Run` でフレームバッファに直接描いている。**

（疑似C を省略。原本は _local/legacy-src/…）

座標は `CalculateMapCoordinates` が `x = -33.0 + coords[0]/14.2f` のように
**画面ピクセル空間へ手計算**してクランプする。

**★ただし OSD には実用上の欠点がある**（ユーザーからの情報）:

- **描画がチカチカして乱れる**
- **アルファブレンドが使えない**

**本プロジェクトが Picture 経路（F-177/F-178）を追うのはこのため。**
「OSD で済むのでは」という結論に安易に流れないこと。

方式 B の実例は `REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master/src/core/game_api/ACMessageBox.cpp`。
**GPU コマンドを一切触らず**、メッセージボックスのデータを組み立てて
ゲームの関数 5 本を呼んでいる。プラグインスレッドから安全なのはそのため。

方式 C の `Hook`:

（疑似C を省略。原本は _local/legacy-src/…）

- 上限 91 個、`ExecuteOverwrittenInstructionBeforeCallback` で元命令を処理
- **必要なレジスタが引数レジスタでない場合は `__attribute__((naked))` の shim が要る**
  （例: `0x4B7DCC` のフックは `R0/R4/R5/R6/R9` を読む）
- `.text` からプラグイン領域へは `B` の ±32MB を超えるが、
  トランポリンは CTRPF 側が処理する


---

## 6. ★自前 GUI の組み込み（F-213）— `Sources/OwnGui.cpp`

### ケーブは C++ へ書き直さない

描画本体は 225 ワードの ARM コードケーブで**実機で検証済み**。
書き直すと「同じ挙動を再現できたか」を再検証する羽目になる。

```
PATCHES/cave_draw_topmost.py  MODE = "export"
    -> Plugin/.../includes/GuiCaves.h   （ケーブ 9 個・フック 8 個・スプライト表）
```

**★書き出したら、実機メモリと機械的に突き合わせること。**
ケーブ 9 個・フック 8 個・スプライト表 280 ワードで不一致 0 を確認してから移した。

### 実行時に決まるもの

| もの | 扱い |
|---|---|
| テクスチャの物理アドレス | 描画ケーブ内の 1 ワードを `((VA - 0x10000000) >> 3)` で差し替える |
| GPU 可視バッファ | `Render_FrameEnd` に一時フックを仕掛けてゲームのアロケータを呼ぶ。確保できたら外す |
| フォントアトラス | SD の `/luma/plugins/00086200/font_atlas.bin` があれば優先、無ければ埋め込み |

### 順序を守る

```
確保 -> アトラス転送 + svcFlushDataCacheRange
     -> ケーブとスプライト表を書く
     -> svcInvalidateEntireInstructionCache
     -> フックを有効化
```

**逆順にすると、書き込む前のケーブへ飛ぶ瞬間ができる。**
OFF はこの逆順。**バッファは解放しない**（`Free` はゲームのスレッドからでないと呼べない）。

### ★キャッシュ操作 — 範囲を取る Luma 独自 SVC を使わない

```c
svcFlushProcessDataCache(CUR_PROCESS_HANDLE, addr, size);   // ★GPU に見せるデータ
svcInvalidateEntireInstructionCache();                      // 書き込んだコード（csvc.h）
```

| 関数 | 可否 |
|---|---|
| `GSPGPU_FlushDataCache` | ✗ サービス未作成で失敗（2 節） |
| **`svcFlushDataCacheRange`（Luma 独自）** | **✗ 実機でカーネル内の書き込みフォルト** |
| `svcFlushProcessDataCache`（標準 SVC） | ○ |
| `svcInvalidateEntireInstructionCache`（Luma 独自・範囲なし） | ○ 実機で通った |

`svcFlushDataCacheRange` で落ちたときの様子:

```
PC FFF0324C（カーネル）  R0 = バッファ先頭  R1 = 先頭+0x1000
FAR = バッファ先頭       Access type: Write
```

**範囲の最初の番地で落ちる。** 範囲を取るキャッシュ SVC は避けること。

### ★型と即値の落とし穴

- **3DS の `u32` は `unsigned long`。** ヘッダを `unsigned int` で吐くと型が合わない
- **`<cstdarg>` を忘れない**（1 節にも書いてあるが実際に踏んだ）
- **ARM の即値は「8bit を偶数ビットだけ右ローテート」。**
  `MOV R1,#0x4000` は `0xE3A01901`。`0xE3A01A01` と書くと **`0x1000`** になる。
  **プラグインが組み立てるケーブも、一度メモリへ置いて逆アセンブルして確かめること。**
  この誤りは実際にそれで見つけた。


---

## 7. ★ファイルのパスはプラグインのフォルダ基準（F-219）

`File::Open(f, "/CTRPF_OwnGui.txt")` と書いても、SD の根ではなく
**`.3gx` と同じフォルダ**に出来る。絶対パスのつもりで書くと見つからない。

**候補を順に試し、どれで開けたかを必ずログに残すこと。**

（疑似C を省略。原本は _local/legacy-src/…）

`File::Read` / `Seek` は **成功で `File::SUCCESS`（= 0）** を返す。
読めたバイト数ではない。

## 8. ★ゲームが動く前に組み込まない（F-219）

プラグインが ready になった瞬間に有効化すると、無効な番地へ飛んで落ちた。

```
PC 0551C928（どこにも属さない）  LR 061CFCEC（プラグイン）
SP 0FFFFE00（ゲームのメインスレッド）
```

**★原因も対策も未解明。TODO-133 として保留にしてある。**
`g_GfxAllocator` が 0 かどうかで見分ける案と、
確保した番地が linear の窓（`0x30000000` 台）にあるか見る案を試したが、
**どちらも実機では防げなかった。効かなかった対策はコードから外した。**

**当面の回避策は「ゲームが動き出してから ON にする」こと。** 2 回目は正常に動く。
