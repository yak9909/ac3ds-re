# TextWriter + 自前ビットマップフォント — 2026-09-06 中断時の引き継ぎ

## ユーザーの指示と現在地

ユーザーは **TextWriterで実装し、静的解析で安全に設計してから、自前フォントを上画面・下画面へ描画**する方針を選択した。
途中で「リミット制限にかかりそうなので一旦中断して文書化」と指示。**ここで作業を止めた。**

- 今回は静的解析・設計の途中まで。**描画実装、アトラス生成、ビルド、実機への適用はまだしていない。**
- 実機への書込み・Resume・bp操作は今回も前ターンも行っていない。
- 前回までの成功例F-302は **TextBox＋ゲームの日本語フォント**。TextWriter直呼び＋自前フォントの成功例ではない。
- **TextBoxを経由しない、独立PaneのDrawSelf＋TextWriter/CharWriter＋標準TextBatch**を目指す。
- `BASELINE/gui_spec_v2/README.md` は別案の基準として固定されたまま。探索中に書き換えない。
- 完了した解析証拠は `scratchpad/textwriter_static_20260906.json`（idalib出力の保存）にある。
  設計・未確定箇所は本書。前ターンの方式比較は `scratchpad/MEMO_20260906_font_cost.md`。

## 実機・IDAの状態

- ida-pro-mcp: 一時IDB `C:/Users/<伏せ字>/AppData/Local/Temp/ida77735.tmp.i64`。
  ARM 32bit、imagebase表示0、**state=-1 / PC=0x00463E24 / breakpoint=0**。
- **自前GUIの既知の登録経路は導入されていない**。
  `0x566DF8=0xE92D4010` / `0x568F98=0xE92D4010` / `0x4B8360=0xE92D41F0` /
  `0x4F1CE4=0xE92D4070`。
- 前ターンで `HEAP_SLOT 0x9B7000` の2語、上下node/root先頭16B、記録長、node+0xB0がゼロと確認。
  F-302末尾の「導入したまま」は現在の実機状態とは異なる。再起動・撤去の経緯や旧ヒープ解放は未判定。
- `*(0x96FC38)=0x32FF5F88`（LayoutMgr）。過去のヒープ/アトラス番地を使い回してはいけない。
- 静的: `code.bin.i64` を **idalib / acnl_code / force_headless / run_auto_analysis=true** で開いた。
  セッションが一度消えていたので開き直し、今回は `idle_ttl_sec=7200` を指定した。
  再開時にidb_listで確認。同じIDBをGUIで同時に開かない。今回はrename/型/コメント変更なし。
- 前ターンに6関数の先頭16Bを静的IDBと実機の同一VAで照合、一致した。
  メモリマップ全体は `get_dbg_memory_info=-6` / 0件で取得不能だった。
- IDAPython: `ida_dbg.get_reg_val('pc')` のように**小文字**で読む。大文字は失敗した。
  `ida_dbg.read_dbg_memory` はこの環境ではbuffer引数が要る。
  読取りは既存スクリプト同様に `invalidate_dbgmem_contents(start,end)`＋`ida_bytes.get_bytes` が使える。
  `ida_idd.dbg_read_memory(ea, size)` もローカルAPI定義で存在確認したが今回未使用。
  py_evalで例外が出ると前のprintも返らないので、存在未確認APIを末尾へ無防備に足さない。

## 静的に確認した呼び出し契約

confidenceは **MEDIUM（複数静的証拠。今回の直呼び経路は実機未検証）**。
既存F-299〜302の実機証拠と整合するが、新方式全体をHIGHとしない。

| 関数 | 引数・働き |
|---|---|
| `0x007E8488` | `InitTextWriter(R0=writer)`。R0が入力であることを `0x4BAFC0 MOV R0,SP`→BLで確認。decompilerは引数を落とす |
| `0x004D5194` | `ResetBatch(R0=writer)`。`writer+0x44`のbatchの件数・構築済み印・使用語数を0へ |
| `0x007E7F48` | `DrawString(R0=writer,R1=UTF-16LE,R2=文字数)`。R3は呼出契約の有効引数ではない。writerを0x64BコピーしてDrawString本体へ渡し、カーソル+0x2C/+0x30だけ戻す |
| `0x004D6570` | `BuildCommandStream(R0=drawctx,R1=writer)`。有効入力はこの2つ。decompilerに見えるR2/R3は未初期化引数ではなく、内部の一時値やMem_Copyの誤った第4引数表示に由来 |
| `0x004D5BCC` | CharWriter終了処理。実体は空。標準経路は最後に呼ぶ |
| `0x004D5CB0` | `TextDraw_EmitStatePrefix(R0=drawctx,R1=cursor)`。行列配列を出力し、新cursorを返す |
| `0x004D520C` | `TextBatch_CopyToCommandBuffer(R0=submitDesc,R1=cursor,R2=drawctx)`。batch+9 bit1=0ならコマンドをMem_Copy。新cursorを返す |
| `0x004B7DEC` | `TextBox_UpdateDrawState(R0=drawctx,R1=cursor,R2=material,R3=emitSuffix)`。**4引数**。TextBox提出末尾ではR2=0、R3=1とassemblyで確認 |
| `0x004D6530` | `TextDraw_EmitStateSuffix(R0=drawctx,R1=cursor)`。テクスチャ無効化コマンドを出力し新cursorを返す |
| `0x004B8360` | `DrawCtx_FlushBatch(R0=drawctx,R1=cursor)`。先行Pictureがあれば先に流す。R1を落とすdecompileに注意 |

### 標準経路からの独立した裏取り

`TextBox_RebuildBatchWriter 0x4BAFB0` のassembly:

1. `writer[0x64]`をstackに確保、R0=SPでInitTextWriter。
2. TextBox+0x104をwriter+0x44へ。ConfigureTextWriterでFont/色/配置を設定。
3. dirtyならResetBatch→DrawString。dirtyを0へ。
4. batch+8==0かつdrawctx!=0ならBuildCommandStream(drawctx,writer)。
5. 終了処理。

`0x73CF48` のDrawSelfはdirty/構築済み印を見てこの再構築を省略する。
**自前実装でも文字変更時だけ再構築し、通常はバッチを再利用する**予定。
ただしゲームのLayout記録列を毎回作り直すか、変更時だけにするかは別の設計項目。
初回は実績のある毎フレーム記録要求を維持し、最適化を混ぜない。

## TextWriterのデータ（0x64B）

Init後に必要欄を設定する。初期化を省いてゼロで代用しない。

| offset | 内容 |
|---|---|
| +0x00/+0x04 | 初期値0 / 0xFFFFFFFF。提出色と混同しない |
| +0x08..+0x14 | 4隅の色。`0x4D5418`で上下色から展開できる |
| +0x18/+0x1C | 上下色 `0xAABBGGRR` |
| +0x20 u8 | 諧調。0=単色、2=上下が異なる |
| +0x24/+0x28 | X/Y倍率。初期値1.0 |
| +0x2C/+0x30/+0x34 | カーソルX/Y/Z。初期値0 |
| +0x38 | 固定送り幅（+0x48が有効なとき） |
| +0x3C | 自前ResFont |
| +0x40 | 即時経路のRectDrawer文脈。**今回のバッチ経路は0のままでよい** |
| +0x44 | 標準TextBatch |
| +0x48 u8 | 固定送りを使うフラグ。初期値0 |
| +0x49 u8 | α。初期値0xFF |
| +0x4C | 折り返し幅。初期値FLT_MAX |
| +0x50/+0x54 | 字間・行間 |
| +0x58 | 初期値4 |
| +0x5C | 整列フラグ。初期値0 |
| +0x60 | 既定TagProcessor `0x0097C0B4`。Initが設定 |

`CharWriter_EmitGlyphQuad 0x4D4EAC`はwriter+0x44!=0なら44Bのグリフ記録を積んでreturnする。
RectDrawer/即時GL関数の側へは進まない。最大件数はbatch+0で制限される。

### 座標で残る確認

- 字形記録は `幅=glyphWidth*scaleX` / `高さ=-cellHeight*scaleY` / X,Y / 色2語 / UV4語 / 記述子。
- `DrawString 0x7E7FA4`は描字直前にbaselineをYから引く。
- `ApplyAlignment 0x7E782C`は整列0でもFont+0x10スロットによる値×scaleYをYへ加える。
  `sub_743600`のfloat戻りはdecompilerが落とす。**assemblyはS0へ値を返す**。
- **従って、writerのYだけで「画面上の字の上端」を決め打ちしない**。
  自前行列のY反転と合わせ、1文字で画面・44B記録を照合してから行/複数文字へ広げる。

## 提出時の状態設定（ここを省略しない）

`TextBox_EmitBatchToGpuCommands 0x4B7CE0`のassemblyで以下を確認した。
自前Paneでもこの順序を再現する設計。**TextBox本体を偽装してこの関数へ渡す計画ではない。**

1. batch使用語数が0ならcursorを返す。
2. `drawctx+0x6A2=4`、`+0x6A0=1`、`+0x6A1=1`。
3. `*(drawctx+0x66C)`へfloat行列12語を書き、`drawctx+0x25=3`。
4. `TextDraw_EmitStatePrefix(drawctx,cursor)`。
5. submitDescを設定して`TextBatch_CopyToCommandBuffer(desc,cursor,drawctx)`。
6. `desc+0x44=0`。
7. `TextBox_UpdateDrawState(drawctx,cursor,0,1)`。

標準の行列生成`sub_73CE64`はTextBoxの整列・Anchorまで読むため、**自前Paneでそのまま呼ばない**。
独立に組む行列をステージングへコピーする案。想定はX右/Y下のwriterを画面中央原点へ写す
行列（Y列反転＋平行移動）だが、**数値の正当性は1文字で検証するまで未確定**。

`TextDraw_EmitStatePrefix`は配列先頭語をヘッダに上書きする。**提出するたび行列12語を全て入れ直す**。
BuildCommandStreamもdrawctxを作業場に使うので、行列の設定はBuildの**あと**に行う。
既存Pictureがある場合は冒頭でFlush。自前テキストPaneは子リスト末尾。

### submitDesc（最低0x4A、実装では境界を揃える）

| offset | 内容 |
|---|---|
| +0x00/+0x04 | Material由来の色2語。実績値0 / 0xFFFFFFFF（F-302） |
| +0x18/+0x1C | 上下の文字色 |
| +0x20 | 諧調フラグ |
| +0x44 | バッチ。提出後0へ戻す |
| +0x49 | α |

`0x4D5418`は上下色を4隅へ展開する関数。writerとdescで利用できる。
TextBoxが使うLayoutMgr+0x1Cの共有作業オブジェクトは、自前descを用意すれば不要。

## 自前フォント設計案

**ResFont vtable `0x008FCAAC`を流用し、データだけ組む**（F-298/F-299）。
独自Fontのvtable/stubは要らない。ゲームのフォント資源は借りない。

| 構造 | 欄 |
|---|---|
| ResFont | +0 vtable / +8 FINF / +0x0C sheetDesc / +0x10 filter flags / +0x14,+0x16 文字→字形cache |
| FINF | +2 代替字形(u16) / +4 left,glyphWidth,advance / +7 linefeed / +8 TGLP / +0x0C CWDH / +0x10 CMAP / +0x14,+0x15,+0x16 寸法・ascent関係 |
| TGLP | +0 cellW / +1 cellH / +2 baseline(s8) / +3 maxCharW / +4 sheetSize / +8 枚数(u16) / +0x0A PICA書式(u16) / +0x0C,+0x0E 列/行 / +0x10,+0x12 sheet幅/高 / +0x14 sheetVA |
| sheetDesc(20B) | +0=0 / +4=ResFont自身 / +8=(sheetVA-0x10000000)>>3 / +0x0C=(height<<16)\|width / +0x10=PICA形式9(LA4) |
| CMAP方式0 | +0/+2 開始/終了code(u16) / +4=0(u16) / +8=next(0) / +0x0C=先頭glyph(u16) |

Font取得子を確認:
- slot2 `0x743A40`: FINF+0x15。
- slot3 `0x743A74`: FINF+0x14。
- slot4 `0x743A68`: FINF+0x16（ApplyAlignmentが使用）。
- slot6 `0x743878`: TGLP+3。
- slot18 `0x743888`: FINF+7。
- slot19 `0x743868`: TGLP+2 baseline（既存F-298）。
- slot25 `0x743A10`: ResFont+0x10を返す（既存F-299）。nearestなら0の案。

字形は`PATCHES/make_font_atlas.py`の既存5x7パターンを使用予定。
**このファイルは末尾でmain()を無条件実行するため、そのままimportすると旧生成物を上書きする。**
安全な定義読込み、または共通化を検討。新アトラスは別名へ保存して旧基準を保つ。

- 128x128 LA4、cellW=7/cellH=7、8px刻み、**開始UV=(cell+1)*列/行+1**に合わせる案。
- glyphWidth=5、advance=6。CWDHを0にしてFINFの既定幅を使える。
- ASCII `0x20..0x7E`をCMAP方式0で順番に配置する案。既存にない文字の扱いは未実装。
- アトラスの上下向きは既存Morton配置とEmitGlyphQuadのV計算を照合し、画素検証＋実機で確かめる。
- これは **ランタイムのBCFNT構造を組む案**で、BCFNTファイルのロード処理は不要。
- 上下でアトラス/ResFontを共有、writer/batch/submitDescは独立。倍率は整数倍で確認する。

## バッチ・領域・登録

最大文字数nの容量（F-299、今回`0x4D76BC`の配置とも再照合）:

```
align16(44*n + 0x28 + align4(ceil(n/8))) + 4*((78*n+57)&~3)
```

batch+9=0の普通メモリ経路を使う。グリフ記録/バッチ/オブジェクトは通常ヒープ、
**アトラスだけGPU可視領域**が必要。アトラス変更後のキャッシュフラッシュも必要。
`cave_node_record.py build_n()`の既存実績はSVC #0x54、CurrentProcess=0xFFFF8001。

参考スクリプト:
- `alloc_lyt_heap.py`: FrameEnd一発ケーブで `0x4B8CF0(size,align)`、freeは`0x569B44(allocator,ptr)`。
- `cave_gfxalloc_probe.py`: `*(0x94CA30)`のAllocatorからアトラスを確保。現在の設定は0x4000/align0x80。
- `cave_node_record.py build_a()`: 自前コマンドリスト作成→ノード登録の検証済み実装。
  単なる`probe_own_layout_node.py build_add()`だけでは**描画用リストを確保しないので不足**。
- `build_pane_tree.py`: Pane共通初期化、DrawInfo、上下独立root、解放前detachの実績。

登録の契約:
`GetProperty(519,&saved)`→`GenCmdlists(1,&node+0x100)`→SelectList→CmdlistStorage→SelectList(saved)。
node+0x114=0 / +0x118=16 / +0x11C=1、画面寸法、投影、記録要求、二重登録ガードを維持する。
vtable+8=`0x5682DC`（replay）、+0x14=`0x5686D4`（record）、+0x18=`0x567BC0`（投影）。
`Layout_RecordPaneTree`がDrawBegin/End・記録commitを担当し、独立PaneのDrawSelfからwriterを使う。
登録フックはRenderTop `0x566DF8` / RenderBottom `0x568F98`。

**領域は未決定。** 既存利用域・このbootのケーブ使用状況・実メモリのゼロを機械的に確認してから割り当てる。
一時的にゼロだっただけでfree済みと判断しない。取り外し/単独revertを必ず用意する。
`apply_patches.py`は既存の掘りパッチ用でMODE=applyなので、**確認目的で実行してはいけない**。
新機能を集約窓へどう追加するかは未着手。

## 次に進める順序

1. 本書とSTATE先頭を読む。IDAの接続/停止・フック・使用域を確認。
2. writer座標・提出行列の設計を最小1文字に絞り、必要なら残るassembly確認。
3. 新しい専用スクリプト/ARMソースを作る。**現時点ではまだ存在しない**。
   apply/status/detach/revertと領域所有情報を備える。文字長の上限・バッチ容量を検査する。
4. フォント専用アトラスと構造を生成し、画素とCMAP/UV/幅/容量を独立した読み側で検算。
5. 全LDRの参照先と値、全分岐、コード/リテラル境界、.text/.bss/heap重なりを機械監査。
   既存`audit_node_cave.py`/`verify_literals.py`を新実装に対応させるか同等の監査を付ける。
6. 動的に領域を確保→データ/ケーブを読戻し確認→まず片画面・1文字を有効化。
7. `run_timed.py`で停止予約つきResume。停止後は別呼出しでPC/バッチ/記録列を読む。
8. Chokistreamを`grab_screen.ps1`でキャプチャして見る。複数字・上下へ順に広げる。
9. 文字変更時の再構築と、変更なしの再利用をカウンタ/データで検証。取り外しも検証。
10. 実機の成功状態をSTATE/FINDINGS/TODO/DOCSに保存。今回の実装を基準仕様へ勝手に昇格しない。

### ローカルツール

`C:/devkitPro/devkitARM/bin/arm-none-eabi-{as,ld,objdump,objcopy}.exe` の存在確認済み。
ローカルPythonにcapstone/keystone/unicorn/PILは無い。**今回、新規インストールはしていない。**
GNU assembler/linker/objdumpでARMソースを機械生成・逆アセンブル監査できる。
ただし対象ゲーム関数の静的解析は引き続きidalibのcode.bin.i64で行う。

`run_timed.py`は `runpy.run_path(...,init_globals={'RUN_MS_OVERRIDE':3000})` 対応。
`grab_screen.ps1`はpowershell.exe 5.1で実行。Resumeを挟まない連写を明滅証拠にしない。
