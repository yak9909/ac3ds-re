---
id: ACNL-F0770
aliases: []
title: "vc_MENU_FLAGS の 0x08/0x10/0x20 の意味と ButtonActionControl_GetDecidedIndex の戻り値"
summary: "vc_MENU_FLAGS(0x949D68) の 0x08=入場を始めた、0x10=入場し終えた（互いに排他の段階値）、0x20=終了要求。ButtonActionControl_GetDecidedIndex(0x72294C) は int を返し、決定なし=-1、this+0xB4 が NULL なら -2。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x949D68, 0x72294C, 0x199F9C, 0x199F44, 0x19AAC0, 0x19AB74, 0x6D6060, 0x6D7194]
tags: [menu, button]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: sonnet-5.5
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

`vc_MENU_FLAGS`（0x949D68、4 バイト）の次のビットは、静的解析で確かめられた。

- 0x08 = 入場を始めた。0x10 = 入場し終えた。この 2 つは排他的な段階値で、一方を立てるとき他方を消す（`& 0xFFFFFFE7 | 8` など）。
- 0x20 = 終了要求（close broadcast）。

`ButtonActionControl_GetDecidedIndex`（0x72294C）は `int f(void *this)`。決定が無い時は -1。`this+0xB4` が NULL の時は -2。決定があれば `*(*(this+0xB4)+0xC8)`（`this+0xB4` は選択中のノードへのポインタ、その +0xC8 を返す）。

確度 MEDIUM（書き手の命令列と読み手の命令列の 2 系統の静的根拠。実測はしていない）。

## 根拠

書き手（命令列）:
- `BsMenuItem_OpenEnter`（0x199F9C）: `BIC R2,R2,#0x10; ORR R2,R2,#8; STR` のあと `B sub_26FB6C`。0x10 を消して 0x08 を立てる。
- `BsMenuItem_OpenUpdate`（0x199F44）: `ItemDragWindow_IsTransitioning(this+0x1EC0)` が 0 のとき `BIC #0x800; ORR #0x10`（疑似C: `flags & 0xFFFFF7EF | 0x10`）。
- `BsMenuItem_CloseUpdate`（0x19AAC0）: `IsTransitioning` が 0 のとき `&= 0xFFFFFFE7`（0x08 と 0x10 を消す）。
- `BsMenuItem_CloseEnter`（0x19AB74）: `sub_68E6E4` のあと 0x20 を消す。
- `BsMenuTab_WaitMenuEndUpdate`（0x6D7194）: 0x08 が消えたら `|= 0x20` して `BsMenuBg_StartLeave` を呼ぶ。
- 0x20 を立てる関数は `sub_18DE34`・`sub_1A08F8`・`sub_6D4CB4` など 8 件。読む側は `BsMenuCatalog_Update`（0x21CC10）ほか約 17 件。

読み手:
- `BsMenuTab_LowerMenuSwitchUpdate`（0x6D6060）: `TST #8` が偽なら何もせず戻る。真なら効果音とタブ表示を進め、そのあと `TST #0x10` で次の段へ進む（0x08 → 0x10 の順の待ち合わせ）。
- `BsMenuTab_WaitMenuEndUpdate`（0x6D7194）: `TST #8` が真の間は戻る（待つ）。

`ButtonActionControl_GetDecidedIndex`（0x72294C、0x50 バイト）:
```
LDR R1,[R0,#0xD4]; TST R1,#1; BEQ L72296C
L722958: LDR R0,[R0,#0xB4]; CMP R0,#0; LDRNE R0,[R0,#0xC8]; MOVEQ R0,#-2; BX LR
L72296C: LDR R1,=dword_94A874; LDR R1,[R1]; CMP R1,#0; BEQ L722994
  LDR R2,=ButtonActionControl_StateDecideAnim; LDR R1,[R0,#0xB8]; CMP R1,R2
  LDREQ R1,[R0,#0xBC]; CMPEQ R1,#0; BEQ L722958
L722994: MOV R0,#-1; BX LR
```
- 引数は R0 の 1 つ（this）。戻りは int。
- `this+0xD4` のビット 0 が立つ、または（`dword_94A874` が非 0 で `this+0xB8` が `ButtonActionControl_StateDecideAnim`（0x2F6694）かつ `this+0xBC==0`）のとき、`this+0xB4` を見る。非 NULL なら `*(*(this+0xB4)+0xC8)`（`LDR R0,[R0,#0xB4]` → `LDRNE R0,[R0,#0xC8]`。選択ノードの +0xC8）、NULL なら -2。
- それ以外は -1。

IDB の作業用コピーに `enum MenuFlags`（ビット列挙。EnterStarted=8、EnterDone=0x10、CloseRequested=0x20）を作り 0x949D68 に付けた。0x72294C には `int __fastcall ButtonActionControl_GetDecidedIndex(void *this)` を付けた。

## 反証条件・未確認点

- 0x08/0x10/0x20 以外のビットは確かめていない。0x800（入場の途中に立て、OpenUpdate で消す）、0x40/0x80（`BsSkb_*`）、0x100・0x200・0x400 は意味が未確認。enum には入れていない。
- 低位の 1/2/4 も排他的な段階値に見える（`& 0xFFFFFFF8|1`、`&0xFFFFFFFC|2`、`&0xFFFFFFF9|4`）が、意味は未確認。
- `BsSkb_WindowInEnter`（0x57CDC8）は `& 0xFFFFFF67 | 8` で、0x08 を立てるときに 0x10・0x80 も消す。0x08 の意味が下画面メニュー以外でも同じかは未確認。
- `dword_94A874` の意味、`this+0xB4` の型、`this+0xD4` bit0 の意味は未確認。this の型名は IDB に無いため `void *`。
- 実測（実機・エミュレータでの値の確認）はしていない。
- F0118 との差: 0x08 を立てるとき 0x10 も消す。0x10 は `IsTransitioning` が 0 になった時に立つ。
