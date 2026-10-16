# クラッシュの診断と復旧

コードケーブ・パッチ作業中に実機が落ちたときの手引き。
根拠は `RE/FINDINGS.md` の F-110 / F-116 / F-152 / F-154 / F-155a / F-161。

---

## 0. まず「本当にクラッシュか」を判定する

**MCP のタイムアウトからは何も分からない。** 原因は少なくとも 4 つある。

| 症状 | 実際に起きていること |
|---|---|
| 呼び出しが 30 秒で切れる | **対象がまだ走っているだけ**（最も多い） |
| 同上 | bp がヒットして正常停止したが、呼び出しは RUNNING 中に始まっていた |
| 同上 | IDA 側でモーダルダイアログがメインスレッドを塞いでいる |
| 同上 | 本当にフリーズしている |

**手動 Suspend して `PC` を見るまで断定しない。**
`PC` が bp の位置なら正常停止、まったく別の場所なら本当の異常。

IDA が **SIGSEGV のダイアログ**を出したときだけは、明確にクラッシュである。

```
8380A0: got SIGSEGV signal (Segmentation fault) (exc.code b, tid 251)
```

先頭の数字が**落ちた命令のアドレス**。これが最重要の手がかり。

---

## 1. 落ちた位置と状態を読む

```python
import ida_dbg, ida_idd
r = ida_idd.regval_t()
ida_dbg.get_reg_val("PC", r)   # 落ちた命令
# R0-R12, SP, LR も同様に読む
```

自前ケーブの中なら、**ケーブ先頭からのオフセット**を出して
どの命令かを特定する。逆アセンブルして突き合わせる。

```python
import ida_bytes, ida_ua, idc
ida_bytes.del_items(ea, 0, 4)
ida_ua.create_insn(ea)
idc.GetDisasm(ea)
```

---

## 2. よくある原因

### 2-1. ★`.text` へ書き込んだ（F-161）

**`.text` はプロセスから見て RX（読み取り＋実行のみ）。**
GDB 経由では書けるので気付きにくいが、
**ケーブ内から `.text` へ `STR` するとその場で落ちる。**

| 用途 | 置き場所 |
|---|---|
| ケーブのコード | `.text` のゼロ埋め（`0x00838080`〜、F-161） |
| リテラル・パラメータ表（**読むだけ**） | 同上で可 |
| **書き込む先**（ログ・観測バッファ） | **RW 領域**。`.text` は不可 |

### 2-2. 未マップ領域を触った

`0x01E81000` の頁は **boot ごとにマップされたりされなかったりする**（F-161）。
読むと全部 `0xFFFFFFFF`、書いても定着しない。

**使う前に必ず検証する:**

```python
ida_dbg.write_dbg_memory(addr, b"\xEF\xBE\xAD\xDE", 4)
ida_dbg.invalidate_dbgmem_contents(0, 0)
idc.get_wide_dword(addr) == 0xDEADBEEF   # False なら未マップ
```

マップ済みの領域（1MB 刻みの探索結果）:

```
0x00100000-0x00C00000   コード像
0x08000000 / 0x0A000000 / 0x0C000000 / 0x10000000
0x30000000 / 0x32000000  ヒープ
```

### 2-3. 引数を根拠なく 0 で埋めた / 呼び出し文脈を満たしていない

F-154 では `TextBox_EmitBatchToGpuCommands` を直呼びして
live の DrawContext を渡し、`drawctx[417..419]` を二重更新して落ちた。

**その関数が前提とする初期化・呼び出し文脈を先に調べる。**
どの引数がどの経路で参照されるかを静的に確認し、
**参照されない経路であることを確かめてから 0 を渡す。**

### 2-4. ヒットした bp を削除せずに再開した（F-110）

これは SIGSEGV ではなく**永久停止**として現れる。
`PC` は bp の位置のまま一歩も進まない。
**その bp を削除して再開すれば何事もなく復帰する。**

---

## 3. 復旧手順

### 3-1. ケーブ内で落ちた場合

1. **落ちた命令を含むループ・処理を NOP で潰す**

   ```python
   NOP = 0xE1A01001   # MOV R1, R1
   ```

   **`MOV R0,R0`(`0xE1A00000`) を NOP に使わないこと。**
   `R0` が戻り値や cursor を保持していることが多い。
   壊して構わないレジスタを選ぶ。

2. **`PC` を安全な地点へ進める**

   ```python
   ida_dbg.set_reg_val("PC", 復帰させたい命令のアドレス)
   ```

   スタックの状態に注意する。`PUSH {LR}` の後なら、
   対応する `POP {LR}` を通る地点に飛ばすこと。
   途中で初期化し直されるレジスタ（ループカウンタ等）は気にしなくてよい。

3. **★修正版は未実行の別番地に作り、フックを張り替える**（F-155a）

   一度実行した番地に書き直すと **I-cache に古い命令が残る**。
   実行中の呼び出しは旧ケーブの残りを走り終えるので問題ない。

4. `continue` して `PC` が通常の待機位置に戻ることを確認する

   本プロジェクトの待機位置は **`0x00137064`**。

### 3-2. 復旧できないとき

3DS を再起動する。メモリパッチは全部消える。

再起動後にやること:

- フックが素に戻っていることを確認（`0x4B7DCC` = `E3A02000` など）
- **ケーブ番地のマップ状態を再検証する**
- **live のオブジェクトアドレスを引き直す**
  （`scratchpad/scan_live_textboxes.py`。ただし同じ会話・同じ住民なら
  ヒープ配置は決定的で、実測では前 boot と完全に同一だった）

---

## 4. 落ちにくくするための作法

- **最小構成で検証してから広げる。** ループや複数対象をいきなり書かない
- **適用前に必ず IDA の逆アセンブラでケーブを検証する。**
  リテラルプールの解決先、全分岐の着地点、`BL` の逆算まで見る
- **`run_timed.py` で走行時間を区切る。** 走り出したら外から止められない（F-116）
- **パラメータはテーブル化する。** 値だけ更新すればコードを書き換えずに済み、
  新しいケーブ番地を消費せず I-cache の問題も起きない
- 呼び出し規約を守る。`BL` の前後で `LR` を退避し、
  AAPCS で callee-saved（R4-R11）を壊さない。
  **フック地点以降で読まれないレジスタは自由に使える** —
  どのレジスタが死んでいるかは元関数の逆アセンブルで確認する

---

## ★フックで `R1` を壊すと `Mem_Copy` で `R0 = 0` の SIGSEGV（2026-08-31）

### 症状

```
PC = 002FBBA4   STM R0!, {R3-R6}      （Mem_Copy 内）
R0 = 00000000                          ← コピー先が NULL
LR = 004B83B8                          ← DrawCtx_FlushBatch の最初の Mem_Copy 直後
```

### 原因

`DrawCtx_FlushBatch`（`0x4B8360`）は **引数が 2 つ**で、**`R1` がコマンドカーソル**（F-185）。
フックのケーブが素通り経路で `R1` を作業用に使うと、
**元関数がゴミのカーソルで走り出して `Mem_Copy(dst=0, ...)` になる。**

```
PUSH {R4-R6,LR}          ← R0-R3 を保存していない
LDR  R12, =LOG
LDR  R1, [R12,#8]        ← ★ここでカーソルを破壊
LDRB R1, [R0,#36]        ← ★さらに破壊
...
skip: POP {R4-R6,LR} ; PUSH {R4-R8,LR} ; B 0x4B8364
```

### 対策

**引数レジスタを潰さない。** 選択肢は 2 つ。

1. `PUSH {R0-R3,R12,LR}` で丸ごと保存する（`cave_add_sprite2.py` 方式）
2. 判定を **`R12` と保存済みレジスタ（R4-R6）** だけで行い、`R0`/`R1` に触れない

**保存するレジスタを減らすときは、フック先が入口で読む引数を必ず確認すること。**
`DrawCtx_FlushBatch` は `R0`（drawctx）と `R1`（cursor）の 2 つ。

### 復旧

`R0 = 0` のまま再開しても同じ場所で再フォルトするため、**再起動が確実**。
フックを素に戻し、ケーブを 0 で消してから再起動する。

---

## ★block-copy で destination register を LDM/STM の両方に使うと Layout を壊す（F-241）

`LDMIA R2,{R0-R3}` の直後に `STMIA R1!,{R0-R3}` を置いてはいけない。
LDM が `R1` をロードした第2 wordで上書きするため、STM の宛先は事前に作った LOG address ではなく
その第2 wordになる。`R1` が STM register list にも入るので、書込み値も writeback の影響を受ける。

F-241 では stage 第2 word が loader Layout `0x3225A2B4` で、vptr を含む先頭16 byteが破損した。
フックを復元しても heap object の元の全フィールドは復元できないため、ゲーム再起動が必要だった。

対策は、block-copy を使わず `LDR/STR` を1 wordずつ行うこと。使用するなら source、destination、
ロード先レジスタを必ず別々にし、最小1 wordで実機検証する。

---

## ★Luma3DS のクラッシュダンプ（`crash_dump_XXXXXXXX.dmp`）を読む（F-320）

SD の `/luma/dumps/ctr/` に落ちる。**デバッガが繋がっていなくても、
落ちた瞬間の PC・レジスタ・命令列・スタックが全部入っている。**
CTRPF プラグインが絡む落ち方は、これを読むのが一番速い。

### 表題（先頭 0x28 バイト）

```
+0x00  magic       0xDEADC0DE / 0xDEADCAFE
+0x08  版          u16 minor、+0x0A u16 major
+0x0C  プロセッサ  u16（9 または 11）
+0x0E  コア番号    u16
+0x10  例外種別    0=FIQ  1=未定義命令  2=プリフェッチ中断  3=データ中断
+0x14  総サイズ（= ファイルの大きさ。ここで検算できる）
+0x18  レジスタ部の長さ   +0x1C コード部   +0x20 スタック部   +0x24 付加データ
```

続けてレジスタ 23 語:
`R0..R12, SP, LR, PC, CPSR, DFSR, IFSR, FAR, FPEXC, FPINST, FPINST2`。

- **`FAR` が触ろうとした番地**、DFSRのstatusは `(DFSR & 0xF) | ((DFSR >> 6) & 0x10)`
  （`5` = セクションの変換フォルト = 未マップ。`FAR` が小さければ NULL 参照）
- ARM状態では**コード部の最後の語が `PC` の命令**。保存PCはLuma側で補正済みで、再補正しない。
  コード部先頭は `PC + (Thumbなら2、それ以外4) - codeSize`。直前の命令列が分かるが、実行履歴そのものではない。
- 付加データは8-byteプロセス名とu64 TitleID。`GARDEN` / `0x0004000000086200` は一例。
  F-405では `socket` / `0x0004013000002E02` だった。

F-406で公式の `fatalExceptionHandlers.h` / `fatalExceptionHandlersMain.c` と
`crash_dump_00000004.dmp` を突き合わせ、旧記述の「下位4bitがプロセッサ・次の4bitがコア」を訂正。
再現パーサは `SYSTEM_KEYBOARD/parse_crash_f405.py`。
今回の停止命令はカーネル内のD-cache clean by MVAで、FARがplugin heapの試験arenaと一致した。
範囲cache SVCを全体cache SVCへ変更した最小実行試験は復帰・全解放まで成功。
詳細は [F-405/F-406](system_keyboard_plugin_probe.md)。

### 呼び出し元を復元する

スタック部から**プラグインの `.text`（`0x07000100`..`.rodata` の手前）を指す語**
を拾って `addr2line` に流すと、そのまま呼び出しの連なりになる。

```
arm-none-eabi-addr2line -f -C -e gohan.elf 0x07005A04 0x07001650 ...
arm-none-eabi-objdump -d --start-address=... --stop-address=... gohan.elf
```

★**古い戻り番地が同じスタックに残っている**（別の呼び出しの残骸）。
SP に近い順に読み、意味が通るところまでを採用する。
実例では `LoadCROHooked` / `OnLoadCro` が上の方に残っていて紛らわしかった。

### ★`threadCreate()` を呼んでよいスレッドは限られる

`libctru` の `__createThread` は**現在のスレッドの TLS を無検査で読む**。

```
mrc p15,0,r3,c13,c0,3     ; r3 = TLS
ldr r3,[r3,#8]            ; r3 = reent   ★magic を確かめない
ldr r2,[r3,#4]            ; ← r3 = 0 ならここでデータ中断（FAR=4）
```

TLS の並びは `initThreadVars` から確定できる。

```
+0x00 magic 0x21545624   +0x04 Thread   +0x08 reent   +0x0C tls_tp
```

`__getreent` / `__getThreadLocalStorage` は magic を照合して、
違えば `__ctrpf_getThreadVars` へ回る。**`__createThread` だけがそれをしない。**
つまり **libctru が初期化していないスレッド（CTRPF の `ThreadEx` など）から
`threadCreate()` を呼ぶと未定義**で、TLS の中身しだいで落ちる。

実例（2026-09-06）: plugin ready の直後にチートを ON にすると
`PluginMenuExecuteLoop::operator()` → `MenuEntryImpl::_Execute()` →
`GuiMenu::Initialize()` → `threadCreate()` の経路でここに落ちた。
**描画そのものは無関係**で、一呼吸おいてから ON にすれば普通に動く。
