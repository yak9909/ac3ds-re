---
id: ACNL-F0300
aliases:
- F-276
title: 'F-276: ★★★★★【F-268 の訂正】既定ブロックは **記録時ではなく再生時**に出る。フラグで切り替わる — `HIGH`（アセンブリ）'
summary: F-268 で「Drawer の既定 begin ブロックは記録の先頭で出る」と書いたのは**誤り**だった。
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5075652
- 5075656
- 5075660
- 5075664
- 5075668
- 5075676
- 5075684
- 5075696
- 2097280
- 5075708
- 5075720
- 5075712
- 5075724
- 5075728
- 5075732
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16867-16956
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-276: ★★★★★【F-268 の訂正】既定ブロックは **記録時ではなく再生時**に出る。フラグで切り替わる — `HIGH`（アセンブリ）

F-268 で「Drawer の既定 begin ブロックは記録の先頭で出る」と書いたのは**誤り**だった。
`Mem_CopyBytes3` の引数を取り違えたまま（F-274）読んでいたのが遠因である。

### 決め手 — `sub_4D72C4` の先頭

```
0x4d72c4 PUSH {R4-R6,LR}
0x4d72c8 TST  R2, #1              ; R2 = フラグ
0x4d72cc MOV  R4, R0
0x4d72d0 MOV  R6, #0
0x4d72d4 BNE  loc_4D7320          ; ★フラグが立っていたら 1 語も出さずに返る
```

**フラグが 1 のとき、このコード（reg `0x06F` / `0x080` と既定ブロック）は完全に飛ばされる。**

### 出す側の全容（フラグ = 0）

```
0x4d72dc STR  R6(=0),          [R1],#4     ┐ reg 0x06F mask 2 = 0
0x4d72e4 STR  R0(=0x0002006F), [R1],#4     ┘
0x4d72f0 VLDM R0(=&unk_8ADA20), {S0-S3}    ┐ unk_8ADA20 = { 0, 0x00200080, 0, 0 }
0x4d72fc VSTM R1, {S0-S3}                  ┘ reg 0x080 mask 2 = 0（+ 詰め物 2 語）
0x4d7308 STR  R3(=0x1000),     [R1,#0x10]  ┐ reg 0x080 mask 0xB = 0x00001000
0x4d7300 STR  R2(=0x000B0080), [R1,#0x14]  ┘ ★テクスチャユニット 0/1/2 を全部無効化
0x4d730c LDM  R2(=drawer+4), {R1,R2}       ; R1 = 既定ブロックの先頭, R2 = 長さ
0x4d7310 BL   Mem_CopyBytes3               ; dst = cursor+0x18
0x4d7314 LDR  R0,[R4,#8] / BIC R0,#3 / ADD R1,R0,R5   ; cursor を長さぶん進める
```

**8 語 + 既定ブロック本体。**

### 誰がどのフラグで呼ぶか

| 呼び出し | フラグ | 結果 |
|---|---|---|
| `Layout_RecordPaneTree` → `DrawBegin1(drawer, **1**)` | 1 | **何も出さない。** drawctx の帳簿（`+1684/1688/1692 = 0`, `+1698 = 6`, `+1696 = 1`）だけリセット |
| `Layout_RecordPaneTree` → `DrawEnd1(drawer, **1**)` | 1 | 溜まっているバッチを流すだけ（`sub_4D7204` も `(a3 & 1) == 0` で判定） |
| `Layout_ReplayRecordedList` → `sub_4B8C34(drawer, DrawInfo, **0**)` | 0 | **既定 begin ブロック + reg `0x06F`/`0x080` を出し、続けて投影 uniform 24 語** |
| `Layout_ReplayRecordedList` → `DrawEnd1(drawer, **0**)` | 0 | **既定 end ブロック**（`Mem_CopyBytes3(cursor, drawer+0x14, drawer+0x18)`） |

### したがって 1 レイアウトぶんのフレーム上の並びはこうなる

```
【再生時に主リストへ出るもの】
  reg 0x06F mask2 = 0                       ← テクスチャ座標出力 OFF
  reg 0x080 mask2 = 0 / maskB = 0x00001000  ← テクスチャユニット 0/1/2 OFF
  既定 begin ブロック（頂点シェーダ・属性・0x100/0x101/0x104 など）
  投影 uniform（index 0、24 語）             ← そのレイアウトの +0x34 から
  ─────────────────────────────────
  【記録した内容をそのまま memcpy】          ← TEV・テクスチャ・uniform 6〜・draw
  ─────────────────────────────────
  既定 end ブロック
```

### F-270 / F-271 は**より強く正しくなった**

「`DrawBegin1` がテクスチャユニットと `0x06F` を落とす」という指摘は、
実際には **再生時に、我々の記録内容が展開される直前**に起きる。
つまり我々の内容の直前に必ず OFF にされるので、
**自前で立て直さなければ絶対にテクスチャは読まれない。**
F-270 / F-271 で追加した

```
reg 0x06F mask 2 = 0x00000100
reg 0x080 mask B = 0x00011001
reg 0x080 mask 4 = 0x00011001
```

は必須であり、置き場所（記録内容の中、TEV の直後）も正しい。

### 記録リストの容量への影響

**記録される内容にシェーダは含まれない。**
自前ノードの記録は「TEV 36 語 + テクスチャ 14 語 + スプライトのバッチ（実測 2072 バイト）」
＝ **およそ 2.3KB** に収まる。`LIST_SIZE = 0x4000`（16KB）に対して十分な余裕がある。

記録直後の残量検査（`g_GpuCmdPtr + 0x2000 <= g_GpuCmdEnd`）も、
`DrawBegin1` が何も出さないので `g_GpuCmdPtr` はほぼリストの先頭にあり、確実に通る。

### F-272 の結論への影響

**無い。** `sub_4D7274` の drawctx リセット（`+1698 = 6` など）は
**フラグに関係なく実行される**（`TST` の判定は `sub_4D72C4` の中だけ）。
したがって「各レイアウトの記録の先頭でマテリアルのモードキャッシュが無効化される」
という F-272 の 2 番の結論はそのまま成立する。

---

