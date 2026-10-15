---
id: ACNL-F0376
aliases:
- F-350
title: 'F-350（2026-09-07）: ★入力の無効化 — `0x32C85A2D` の正体と、全ボタン／タッチを塞ぐ場所'
summary: '**confidence: HIGH（静的解析）/ MEDIUM（実機。読み取りのみで未適用）**'
date: '2026-09-07'
category: input
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9361696
- 9430776
- 9433884
- 5535188
- 1048576
- 2097152
- 4194304
- 8388608
- 5492212
- 5492164
- 5492216
tags:
- touch
- button
supersedes: []
source: v1:RE/FINDINGS.md:22649-22739
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-350（2026-09-07）: ★入力の無効化 — `0x32C85A2D` の正体と、全ボタン／タッチを塞ぐ場所

**confidence: HIGH（静的解析）/ MEDIUM（実機。読み取りのみで未適用）**
根拠: decompile（`sub_540870` / `sub_542E88` / `sub_543050` / `sub_5475D4` / `sub_2E08F8`）
      + 実機のオブジェクト実測（bp で `R0` を捕獲）
詳細: `scratchpad/MEMO_f350_input_block.md`

### 1. `0x32C85A2D` = `ButtonActionNodeEx[0] + 0xD9`

実機で前後を読むと `0x184` 刻みの配列で、vtable は **`0x008ED920` = `vtbl_ButtonActionNodeEx`**
（RTTI `18ButtonActionNodeEx`）。先頭 `0x32C85954`、この場面で **11 個**。

`+0xD9` の意味は `sub_2E08F8(this, a2)` から確定 —
**「この Button Action が結び付いている（有効）か」の旗**（結ぶとき 1 / 外すとき 0）。

★**これでは全ボタンの無効化にならない。** 覆うのは UI に登録された Button Action だけで、
  移動・カメラ・A ボタンの当たり判定は別経路。個数も並びも**場面で変わる**。

### 2. ★本命 — `sead` の入力

| | 実機 | vtable | ボタン数 |
|---|---|---|---|
| 物理入力 `sead::CtrController` | `0x32945634` | `0x008FE6F8` | 28 |
| ゲームが読む `sead::ControllerWrapper` | `0x32FF8080` | `0x008FF31C` | 19 |

**Wrapper は元の CtrController から全部写す**（`ControllerWrapper::calc` `0x005475D4`。
ビットは `+0x174` の対応表で読み替え、スティックとタッチはそのまま複製）。
→ **元を 1 個塞げばゲーム側は全部塞がる。**

#### `sead::ControllerBase` の欄（`sub_543050` / `sub_542E88` から）

| off | 意味 |
|---|---|
| `+0x04` | trig（押した瞬間）= 新 hold & ~旧 hold |
| `+0x08` | release（離した瞬間） |
| `+0x0C` | repeat |
| `+0x10` | **タッチの旗**。bit0 タッチ中 / bit1 押した瞬間 / bit2 離した瞬間 |
| `+0x14` `+0x18` | ポインタ座標 int |
| `+0xFC` | ボタン数 / `+0x100` `+0x104` スティック→ビットの開始（**どちらも -1**） |
| **`+0x110`** | **hold** |
| `+0x114` `+0x118` | ポインタ座標 float |
| **`+0x11C` `+0x120`** | **スライドパッドのアナログ値 X / Y** |

#### ★ビット対応（`sub_540870` = CtrController の生読み）

```
A 0x1 / B 0x2 / X 0x8 / Y 0x10 / ZL 0x80 / START 0x800 / SELECT 0x1000
L 0x2000 / R 0x4000 / 十字 上0x10000 下0x20000 左0x40000 右0x80000
スライドパッド 上0x100000 下0x200000 左0x400000 右0x800000
```

→ **スライドパッドの 4 方向 = `0x00F00000`。** アナログ値は別欄なので、
  ビットを残せば移動は完全に生きる。

### 3. 仕掛ける場所 — `0x0053CDF4` の `BL` 1 本

```
0053CDE4  BLX R1              生読み（sub_540870）。ここで +0x110 / +0x10 が更新される
0053CDF4  BL  sub_542E88      ← ★ここを差し替える（現在の語 0xEB001823）
0053CDF8  LDR R0,[R4,#0x140]
```

「生読みの直後・edge 計算の直前」なので、ここで hold を削れば
**trig / release / repeat も削った値から計算され、幻の押下・離しが出ない。**
`sead::Controller::calc`（`0x0053CDC4`）を使うのは **CtrController だけ**
（Wrapper は自前の `sub_5475D4`）。

ケーブ（約 18 語）:

```
PUSH {R0-R3,LR} / 制御ブロックの旗を見る
  ボタン: LDR R12,[R0,#0x110] ; AND R12,R12,#0xF00000 ; STR R12,[R0,#0x110]
  タッチ: LDR R12,[R0,#0x10]  ; BIC R12,R12,#1        ; STR R12,[R0,#0x10]
POP {R0-R3,LR} / B sub_542E88     ← 末尾ジャンプ。LR そのままで 0x53CDF8 へ戻る
```

★`AND R12,R12,#0xF00000` は ARM の即値（0xF ROR 12）で表現できる。

### 4. ★プラグイン自身の入力は影響を受けない

CTRPF の `Controller` は HID を直接読むので、ゲームの sead 側を塞いでも
**自前メニューの操作とタッチは生きる**。要望（ゲームだけ止める）にそのまま合う。

### 5. まだ確かめていないこと

1. ビット対応を実機で目視確認していない（利用者にボタンを押してもらい `+0x110` を読めば取れる）
2. ケーブは**未実装・未適用**
3. この解析ではコードを 1 語も書き換えていない。bp 2 回はどちらも削除済み

---

