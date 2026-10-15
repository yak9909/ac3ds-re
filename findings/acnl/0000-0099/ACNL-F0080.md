---
id: ACNL-F0080
aliases:
- F-42
title: F-42 【完成】木にぶつかって切り倒す — `HIGH`
summary: 実機で確認済み。**パッチは 1 つも当てず、フック 1 箇所だけで完結する。**
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5880752
- 10151172
- 10150236
- 5880516
- 6613024
- 6680872
- 5864784
- 5864828
- 5864832
- 5864856
- 5856028
- 5864852
- 10150308
- 10150468
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1931-2085
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-42 【完成】木にぶつかって切り倒す — `HIGH`

実機で確認済み。**パッチは 1 つも当てず、フック 1 箇所だけで完結する。**
「揺する」「斧」は完全に素の挙動のまま。

### 構成（`PATCHES/cave_tree.py`）

| アドレス | 変更 |
|---|---|
| `0x59BBB0` | `BL FieldObj_FellObject` → `BL ケーブ` |

ケーブは CTRPF 空ページの `0x01E81200`（40 ワード）。
**`PATCHES/cave_particle.py` が `0x01E81000` を使うので `+0x200`。**

### 役割分担 — ここを切り分けるのに三度失敗した

| 担当 | 何をするか | 成立条件 |
|---|---|---|
| **アクション側** | **マスを切り株へ置換する** | `R6 = 1`（打撃カウンタが必要数に達している） |
| **`FieldObj_FellObject` 側** | **倒れる演出・見た目** | `a2` と `kind` が正しいこと |

**どちらか一方だけでは成立しない。** 実際に作った 3 つの版:

| 版 | 構成 | 結果 |
|---|---|---|
| A | パッチで `R6=1` 固定 + `a2`/`kind` 差し替え + キュー解放 | 動くが、斧が一撃・揺すりでも倒れる |
| B | mode 1 + `a2`/`kind` 差し替え + キュー解放 | **演出だけ出てマスが変わらない**（3 回必要） |
| C | mode 1 + 打撃カウンタ操作 + 差し替えなし + **解放なし** | **マスは変わるが演出なし・キュー詰まり** |
| **D** | **mode 1 + カウンタ操作 + `a2`/`kind` 差し替え + キュー解放** | **完成** |

B から「`FieldObj_FellObject` だけではマスは置換されない」、
C から「カウンタ操作で `R6=1` を作れる」ことが分かり、両方を足して D になった。

### ケーブの動作

到達時: `R0`=a1 `R1`=a2 `R2`=X `R3`=Y、`[SP+0]`=a5 `[SP+4]`=kind `[SP+8]`=fx

```
PUSH {R0-R5,R12,LR}          ; 32B → SP+32=a5  SP+36=kind  SP+40=fx
LDR  R0, [SP,#36]            ; kind
CMP  R0, #0
BNE  skip                    ; ★ぶつかった(kind=0)以外は素通し
; --- 打撃カウンタを 3 にする ---
LDR  R0, [SP,#8]             ; X
LDR  R1, [SP,#12]            ; Y
ADD  R2, R1, R1,LSL#2        ; 5Y
ADD  R0, R0, R2,LSL#4        ; X + 80Y
SUB  R0, R0, #0x510          ; t
LDR  R3, =0x9AE504
MOV  R2, R0,LSL#28
MOV  R1, R0,ASR#4            ; word index
MOV  R0, R2,LSR#27           ; shift = (t & 0xF) * 2
ADD  R3, R3, R1,LSL#2
LDR  R2, [R3]
MOV  R1, #3
ORR  R2, R2, R1,LSL R0
STR  R2, [R3]
; --- 斧アクションを起こす ---
LDR  R0, [SP,#8]
LDR  R1, [SP,#12]
MOV  R2, #1                  ; ★mode 1（素で FieldObj_ResolveAxeAction へ）
BL   Player_BeginFieldObjAction
CMN  R0, #1
BEQ  skip
LDR  R1, =0x9AE15C
ADD  R2, R0, R0,LSL#3
ADD  R5, R1, R2,LSL#1        ; スロット = base + r*18
ADD  R4, R5, #4
STR  R4, [SP,#4]             ; ★a2 = &item1
LDRB R4, [R5,#17]            ; キューの flags
TST  R4, #2
MOVNE R4, #5                 ; ★向きは flags bit1 から（F-41）
MOVEQ R4, #4
STR  R4, [SP,#36]            ; kind を差し替え
MOV  R4, #0
STRH R4, [R5,#14]            ; ★キュー解放（怠ると詰まって斧も使えなくなる）
skip:
POP  {R0-R5,R12,LR}
B    FieldObj_FellObject
```

### 「ぶつかった」と「揺すった」の区別

`FieldObj_BumpFellCaller` (`0x59BAC4`) は**両方から呼ばれる**。木が揺れる演出が共通のため。
トレース用ケーブで呼び出し元と引数を実測した:

| 操作 | 呼び出し元 | `kind` |
|---|---|---|
| ぶつかる | `0x0064E820` | **0** |
| 揺する | `0x0065F128` | **2** |

**`kind` の値そのものが違う**ので、呼び出し元を見るまでもなく `CMP R0,#0` で分離できる。

### 打撃カウンタ `dword_9AE504`

`FieldObj_ResolveAxeAction` の `0x597D50`-`0x597D7C` から（**decompile ではなく asm から読んだ**）:

```
00597D50  ADD R0, R8, R8,LSL#2   ; 5Y      (R7 = X, R8 = Y)
00597D58  ADD R0, R7, R0,LSL#4   ; X + 80Y
00597D5C  SUB R0, R0, #0x510     ; t
00597D68  MOV R1, R0,ASR#4       ; word index（算術シフト）
00597D6C  MOV R0, R2,LSR#27      ; shift = (t & 0xF) * 2
00597D70  LDR R1, [R3,R1,LSL#2]  ; dword_9AE504[index]
00597D7C  MOV R9, R1,LSR R0      ; 打撃数 = 2 bit
```

判定は `0x597D80`-`0x597D98`:

```
CMP R4, #4 / SUBGE R4, R4, #1    ; R4 = 必要打撃数（FieldObjDef[13] 由来）
ADD R0, R9, #1
CMP R4, R0
BGT → R6 = 0                     ; まだ倒れない
      R6 = 1                     ; 倒す
```

カウンタを 3 にすると `R0 = 4` になり、**そのマスだけ**「次の一撃で倒れる」状態になる。
斧の必要打撃数そのものは変えていないので、他の木への影響はない。

### `mode 1` は素で伐採判定へ行く

```
00595B18  CMP R6, #0
00595B1C  BEQ loc_595D2C     ← F-38 でパッチしていた場所。**使わない**
00595B20  CMP R6, #1
00595B24  BEQ loc_595D2C     ★mode 1 は素で FieldObj_ResolveAxeAction へ
00595B28  CMP R6, #2
00595B30  B   loc_595D58     ; mode 2 = スコップ
```

`mode 1` を使えば `0x595B1C` を書き換える必要はない = **A ボタンの「揺する」は素のまま。**

### やってはいけないこと

- **`0x595B1C` の書き換え**（mode 0 を伐採判定へ）— A ボタンで揺すっても倒れてしまう
- **`0x597D94` の NOP 化**（1 回で切り倒す）— **斧まで一撃になる**。
  この `BGT` が制御しているのは `Player_StartFieldAction` の第 10 引数 `R6` **だけ**で、
  結果アイテム `v22` は別引数なので、ここを触っても結果アイテムには関係しない
- **キュー `[14]`/`[15]` を解放し忘れる** — 4 スロットが `act=14 state=2` で埋まり、
  斧を含む他のアクションが一切効かなくなる
- **`FieldObj_ApplyDigRecord` によるレコード登録** — 消化されず 32 件超で SIGSEGV (F-39)

### 詰まったキューの手当て

```
キュー   0x9AE15C + i*18 + 14 に 0x0000 を書く（actionID と state）
進行中   0x9AE1A4 + i*5  + 2  に 0xA5 を書く（pNo = 165 = 空き）
レコード 0x9AE244 + i*22 + 17 に 0x00 を書く（state）
```

`act` が該当するものだけを選んで解放する。実際にこれで復旧できた。

---

