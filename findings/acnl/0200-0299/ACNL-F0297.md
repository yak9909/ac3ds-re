---
id: ACNL-F0297
aliases:
- F-273
title: 'F-273: ★★★★★致命的なバグ。記録スロットのエピローグが `R4` = drawctx のまま `Commit` していた — `HIGH`（静的のみ・未適用）'
summary: F-267 の教訓「生成器を変えたらケーブ 1 本を丸ごと IDA に通す」に従って
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8612944
- 8612948
- 8612952
- 8612956
- 8612960
- 8612964
- 8612968
- 8612972
- 8612976
- 8612980
- 8612984
- 8612988
- 8612992
- 8612996
- 8613000
- 8613004
- 8613008
- 8613012
- 8613016
- 8613020
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16609-16731
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-273: ★★★★★致命的なバグ。記録スロットのエピローグが `R4` = drawctx のまま `Commit` していた — `HIGH`（静的のみ・未適用）

F-267 の教訓「生成器を変えたらケーブ 1 本を丸ごと IDA に通す」に従って
`CAVE_Q`（記録スロット本体、391 語）を全部逆アセンブルしたところ見つかった。
**これがあると自前ノードは一度も描画されない。**

### 何が起きていたか

記録スロットは `(*(vtable+0x14))(node)` で呼ばれるので、入口では `R0` = 自前ノード。

```
PUSH {R4-R8,LR}
MOV  R4,R0                      ; R4 = ノード
…
（残量検査などで早期離脱するときは endrec へ。このとき R4 はまだノード）
…
MOV  R4,R5                      ; ★R4 = drawctx に載せ替える
…（スプライトを積む。R4 は drawctx として使われる）…
endrec:
    Drawer->DrawEnd1(drawer, 1)
    ADD R0,R4,#0x104            ; ★★R4 は drawctx のまま
    ADD R1,R4,#0x108
    ADD R2,R4,#0x10C
    ADD R3,R4,#0x110
    BL  GpuCmd_CommitListAndCaptureDelta
    …
    STRB R2,[R4,#0x11D]         ; ★★同上
```

`Commit` は記録の開始位置・長さ・GX キューの範囲を書き出す関数で、
**書き先が `drawctx+0x104..0x110` になっていた。**

結果:

1. **ノードの `+0x108`（記録長）が 0 のまま** →
   `Layout_ReplayRecordedList` の `if (+0x108 > 0)` を満たさず**早期 return**。
   記録は毎フレーム走るのに、**一度も再生されない**
2. `drawctx+0x104`〜`+0x110` を毎フレーム破壊する
3. `STRB [R4,#0x11D]` も drawctx を叩くので、
   ノードの記録要求フラグが下りない（登録ケーブが毎フレーム立て直すので実害は小さい）

**早期離脱の経路（記録開始直後の 3 か所）では `R4` がまだノードなので正しく動く**という
非対称があり、症状が経路によって変わるたちの悪い形だった。

### 直し方

ノードのポインタを `LOG + 0xF4`（`LOG_NODE`、空きスロット）へ控え、
`endrec` で読み直す。早期離脱の経路でも同じ値になるので分岐が要らない。

```
入口:   MOV R4,R0
        LDR R12,=LOG            ; R12 は呼び出し規約上こちらで壊してよい
        STR R4,[R12,#0xF4]
endrec: LDR R4,=LOG
        LDR R4,[R4,#0xF4]       ; ★R4 をノードへ戻す
        （以降 DrawEnd1 → Commit → SelectList → STRB）
```

`BLX R2`（DrawEnd1）は AAPCS で `R4` を保存するので、その後も `R4` は生きている。

### 検証（IDA）

```
0x836c50 LDR  R4, loc_836CA8        ← =LOG
0x836c54 LDR  R4, [R4,#0xF4]        ← ノードを復元
0x836c58 LDR  R0, loc_836CB8        ← =MGRP
0x836c5c LDR  R0, [R0]
0x836c60 ADD  R0, R0, #0x364        ← drawer
0x836c64 LDR  R2, [R0]
0x836c68 LDR  R2, [R2,#0x14]        ← DrawEnd1
0x836c6c MOV  R1, #1
0x836c70 BLX  R2
0x836c74 ADD  R0, R4, #0x104
0x836c78 ADD  R1, R4, #0x108
0x836c7c ADD  R2, R4, #0x10C
0x836c80 ADD  R3, R4, #0x110
0x836c84 BL   GpuCmd_CommitListAndCaptureDelta
0x836c88 LDR  R0, loc_836CC0
0x836c8c LDR  R0, [R0]
0x836c90 BL   GpuCmd_SelectList
0x836c94 MOV  R2, #0
0x836c98 STRB R2, [R4,#0x11D]
0x836c9c POP  {R4-R8,LR}
0x836ca0 MOV  R0, #0
0x836ca4 BX   LR
```

`LDR R4,=LOG` のリテラル（`loc_836CA8`）が `0x009B0D00` = `LOG` であることも
生成語から独立に復号して確認した。

`CAVE_Q` の全 BL も IDA で確認した。

```
GpuCmd_GetProperty / GpuCmd_SelectList / sub_7B01CC / sub_7B05B0
Material_EmitState / TextBox_UpdateDrawState
CAVE_T (0x838CE0) x2 / GpuCmd_CommitListAndCaptureDelta / GpuCmd_SelectList
```

10 件すべて、オフラインで計算した飛び先と一致した。

### ★手順上の落とし穴（今回踏んだ）

1.4KB の 16 進を手で写してツール呼び出しへ貼ったところ、**8 バイト（2 語）落とした。**
その結果、後半の BL が全部 8 バイトずれて見え、一瞬「生成器のバグか」と思った。
オフラインで飛び先を計算して突き合わせたら**貼り間違い**だと分かった。

- **大きなバイト列は手で写さない。** 分割して、貼った後に必ず
  `get_bytes` と元データを突き合わせる
- **「IDA がおかしい」と思ったら、まず自分の入力を疑う**

### ケーブ配置（F-273 時点。現行）

```
CAVE_Q=0x838200(391) CAVE_P=0x838820(35)  CAVE_V=0x8388B0(44)
CAVE_A1=0x838960(87) CAVE_A2=0x838AC0(82) CAVE_N=0x838C10(11)
CAVE_M=0x838C40(7)   CAVE_B=0x838C60(12)  CAVE_U=0x838C90(12)
CAVE_F=0x838CC0(10)  CAVE_T=0x838CF0(2)    末尾 0x838D00 / 上限 0x839000（余り 768 バイト）
```

**未適用。実機へは入れていない。**

---

