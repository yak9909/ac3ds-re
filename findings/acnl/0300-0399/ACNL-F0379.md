---
id: ACNL-F0379
aliases:
- F-353
title: 'F-353（2026-09-07）: ★SELECT のビットは `0x800` — libctru の並びと違った（実測で確定）'
summary: '**confidence: HIGH（実機で実測。基準値も取った）**'
date: '2026-09-07'
category: input
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:22865-22922
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0742"]
---
## F-353（2026-09-07）: ★SELECT のビットは `0x800` — libctru の並びと違った（実測で確定）

**confidence: HIGH（実機で実測。基準値も取った）**

### 症状

「メニューを開いているときは SELECT が効かないが、**閉じると効く**」。

ボタン一括マスクは全ビットを落とすので開いている間は止まるが、
常時落としているビットが違っていたので、閉じると通っていた。

### 測り方（★計数器を使うとタイミングに依存しない）

生 HID は装置の **`0x329455AC`**（`CtrHidDevice + 0x15C0`）。
`sead::ControllerBase + 0x2C + 4*i` は**ボタンごとの押し続けフレーム数**で、
離すと 0 に戻る。これを読めば「いま押されている全ボタン」がタイミング無しで分かる。

| 手順 | 生 HID | hold | 押し続け |
|---|---|---|---|
| 指を離す（基準） | `0x00000000` | 0 | すべて 0 |
| **SELECT を押す** | **`0x00000008`（bit3）** | 0（※） | — |

※このとき SELECT で自前メニューが開き、制御ブロックが `01 00` になっていたため
  ボタン一括マスクで 0 になった。生 HID は我々のコードより手前なので影響を受けない。

### 確定した事実

```
SELECT を押す -> 生 HID bit3 -> sub_540870 が sead 0x800 へ写す
```

**libctru では bit2=SELECT / bit3=START だが、この経路（nn::hid）は逆。**
F-350 の対応表は libctru の並びを当てはめていたので、SELECT と START が入れ替わっていた。
★実測したのは **SELECT だけ**。`0x1000` が START かどうかは未実測。

### 直し

- `BIT_SELECT` を **`0x800`** に（`BIT_START` は `0x1000` と推定）
- 常時落とす命令を `BIC R12,R12,#0x800` へ
- 一括マスク `BUTTONS` は両方を含むので**変わらない**

### ★もう 1 つの誤り — 即値を手で書いて間違えた

`BIC R12,R12,#0x800` を手で `0xE3CCCC02` と書いたが、これは **`#0x200`** だった
（objdump が `bic ip, ip, #512` と表示して発覚）。
正しくは `0xE3CCCB02`。

→ `input_block_cave.py` に **`enc_imm()`（imm8 ROR 2*rot の探索）** を入れ、
  **即値を手で書かない**ようにした。

★**objdump による独立検証がこれを捕まえた。** ケーブを実機へ入れる前に必ず通すこと。

### 状態

再生成・検証器 0 件・ビルド成功。**実機未確認。**

---

