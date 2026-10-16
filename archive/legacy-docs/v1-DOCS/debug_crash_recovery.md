# Remote GDB のクラッシュ復旧手順

対象は、解析用の一時コードから既存関数を呼んで発生した **既知の例外フレーム** に限る。
任意の SIGSEGV にレジスタを書き戻す一般手順ではない。原因不明の例外、ゲーム本体の
状態破壊、書込み済みデータ破壊には使わず、タイトルを再起動する。

## 2026-08-29: TextBox clone の既知シグネチャ

`PATCHES/cave_ui_picture_clone.py` の旧 TextBox clone は、native 呼出しの descriptor
文脈を持たず、次の命令で停止した。

| 項目 | 値 |
|---|---:|
| 停止 PC | `0x004B7D50` |
| 関数 | `TextBox_EmitBatchToGpuCommands` |
| 例外命令 | `STR R7,[R0,#0x13C]` |
| 壊れた値 | `R0=0x0000001C` |
| clone TextBox | `R6=0x01E81EF8` |

この `STR` は無効アドレスへの書込みで例外となったため、命令自体は完了していない。
呼出し元の native `nwlyt_DrawPaneTreeToCurrentList` はまだ生存しているので、clone の
呼出しフレームを丸ごと捨ててそのエピローグへ戻せる。

## 前提確認

以下をすべて満たす場合だけ実施する。

- IDA のデバッガ状態が Suspend (`state == -1`)。
- `PC == 0x004B7D50`。
- software breakpoint が 0 件。
- clone patch の二つの hook を既に stock へ戻している。
  - `0x004D71B8 == 0xE8BD4070`
  - `0x0073CB58 == 0xE92D47F0`
- 現在の `SP` から 0x90 バイトを読んで保存する。今回の stack layout と異なる場合は中止する。

今回の stack layout は次の通りだった（`S = 例外時 SP = 0x0FFFFD7C`）。

```
S + 0x3C : cave からの TextBox_Draw 復帰先 (0x01E81B28)
S + 0x40 : cave hook が保存した R0
S + 0x44 : cave hook が保存した最終 GPU cursor (R1)
S + 0x74 : 元の DrawPaneTree の保存済み R4-R6/LR フレーム
```

`S+0x74` は固定アドレスではなく、今回の二重 hook / TextBox 呼出しに固有のオフセットである。

## 実施した復旧

clone 呼出しへ戻ると、uninstall済みの cave を実行してしまう。そこで clone の stack frameを
個別に unwind せず、直接 `nwlyt_DrawPaneTreeToCurrentList` の stock epilogue
`0x004D71B8`（`POP {R4-R6,LR}`）へ移した。

```python
# Suspend 中、かつ上のシグネチャ確認後だけ
sp = ida_dbg.get_reg_val('SP')
ida_dbg.invalidate_dbgmem_contents(sp + 0x44, 4)
saved_cursor = struct.unpack('<I', ida_bytes.get_bytes(sp + 0x44, 4))[0]

ida_dbg.set_reg_val('R0', ida_dbg.get_reg_val('R1'))
ida_dbg.set_reg_val('R1', saved_cursor)
ida_dbg.set_reg_val('SP', sp + 0x74)
ida_dbg.set_reg_val('PC', 0x004D71B8)
ida_dbg.continue_process()
```

今回、ゲームはこの方法で正常に復帰した。

## 必須の注意

- `saved_cursor` を定数として再利用しない。必ず対象停止時の `S+0x44` から読む。
- hook/caveを先に復元していないと、復帰後に同じ注入コードへ戻る。
- `SP+0x74` は今回の stack frame にだけ有効。パッチの PUSH mask、呼出し深さ、例外地点が
  変われば再計算する。
- `PC` が異なる、stack の return address が一致しない、または store が既に副作用を起こした
  疑いがある場合は使用せず、タイトルを再起動する。

## 再発防止

TextBox は Picture と異なり、`0x73CF48` の第3引数が後段
`TextBox_EmitBatchToGpuCommands` の第5引数 descriptor として必要になる。commit hook の
保存済み `R6` を渡しても native descriptor とは限らない。TextBox clone を再試行する前に、
native TextBox draw 時の descriptor を trace して、frame単位で保持する wrapper を作ること。

## 2026-08-29: descriptor observer の既知シグネチャ（F-155a）

これは `scratchpad/trace_main_text_submit_descriptor.py` 初版の純粋なobserverの実装不良で、
native関数本体やGPU状態はまだ変更していない場合だけの復旧である。

| 項目 | 値 |
|---|---:|
| 停止 PC | `0x01E81A54` |
| hook | `0x004D520C` (`TextBatch_CopyToCommandBuffer`) |
| 元命令 | `0xE92D41F0` (`PUSH {R4-R8,LR}`) |
| cave prologue | `PUSH {R0-R3,R12,LR}` (24 bytes) |

初版はfieldを読むたびにR0を上書きしてしまった。`PC`が上記cave範囲にあり、現在SPから
24 bytesに元の `R0,R1,R2,R3,R12,LR` がこの順で保存されていること、かつhookをstockへ
読み戻し確認できることを前提に、次だけを行った。

```python
# 例外位置・stack layout・stock hookを全て確認してから
saved = struct.unpack('<6I', ida_bytes.get_bytes(sp, 24))
ida_dbg.write_dbg_memory(0x004D520C, struct.pack('<I', 0xE92D41F0), 4)
# R0-R3/R12/LR = saved[0..5]
# SP = sp + 24; PC = 0x004D520C
```

その後、Resume前にcave/bufferをzero化する。PCが異なる、書込みがnative本体まで進んだ、
hookの読戻しが異なる、またはstack layoutが一致しない場合はこの手順を使わず再起動する。
今回の停止ではこの手順でstock入口からResumeし、ゲームが正常復旧したことをユーザーが確認した。
