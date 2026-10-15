---
id: ACNL-F0382
aliases:
- F-356
title: 'F-356（2026-09-07）: ★「ゲームスピード変更」チート `0054C6E8` の正体 — フレームペーシングの無効化'
summary: 'confidence: **HIGH（静的）** / 実機での効果確認は未実施（利用者の報告のみ）'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5555944
- 9435996
- 9220740
- 5555844
- 9436276
- 9220816
- 9341780
- 9195024
- 2420904
- 9220428
- 9435008
- 1213480
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23069-23151
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-356（2026-09-07）: ★「ゲームスピード変更」チート `0054C6E8` の正体 — フレームペーシングの無効化

confidence: **HIGH（静的）** / 実機での効果確認は未実施（利用者の報告のみ）

利用者提供のチート `0054C6E8 E3E004FF`（ON）/ `E59400A0`（OFF）を解析した。
**実機は未接続。読み取りのみで、1 語も書き換えていない。**
詳細は `scratchpad/MEMO_f356_gamespeed.md`。

### 番地

`0x0054C6E8` は `sub_54C684` の中の `LDR R0,[R4,#0xA0]`。

`sub_54C684` = **フレーム待ち＋画面提示**（フレームペーシング）。
RTTI で確定したクラスと vtable スロット:

| vtable | TypeInfo | クラス | スロット 31 |
|---|---|---|---|
| `0x008FFB5C` | `0x008CB284` | `sead::DoubleCmdGameFrameworkCtrNw4c` | `0x0054C684` |
| `0x008FFC74` | `0x008CB2D0` | `sead::UlcdDoubleCmdGameFrameworkCtrNw4c` | `0x0054C684` |
| `0x008E8B54` | `0x008C4E10` | **`UlcdFramework`（本作の派生）** | `0x0024F0A8` |

基底は `sead::GameFrameworkCtrNw4c`（TypeInfo `0x008CB14C` / vtable `0x008FF780`）。
`sub_24F0A8` は `sub_54C684` を呼んでから `this+0x170` の後始末をするだけの上書き。

### 欄と補助関数

| | |
|---|---|
| `this+0xA0` | 前フレームを提示したときの VBlank カウンタ（★差し替え対象） |
| `this+0x70` | 1 フレームに要る VBlank 数（**値は未確定。§未確定**） |
| `this+0x14C` | フレーム数の飽和カウンタ（`sub_54C424` が 3 まで +1） |
| `this+0xB8` | `SVC 0x28`（svcGetSystemTick）の記録 |
| `sub_7B013C(1026)` | `qword_AD9A14` の lo/hi（画面 0/1 の VBlank カウンタ）の古い方 |
| `sub_1282A4` / `sub_1282E8` | lo / hi を `0x7FFFFFFF` を法に +1 する VBlank ハンドラ（`sub_121E2C` が登録） |
| `sub_7B073C(1026)` | 両画面の提示 |
| `sub_13917C` | tick→ns 変換 → `0x128428` の **`SVC 0x0A` = svcSleepThread** |
| `sub_133118` / `sub_133188` | Gfx（`dword_96F33C`）の排他ロック／アンロック（MEDIUM） |

### 何をしているか

`E3E004FF` = `MVN R0,#0xFF000000` → `R0 = 0x00FFFFFF`。
「前フレームのカウンタ」の代わりに巨大な定数が入るので、

```
経過 = (前 > 今) ? (0x7FFFFFFE - 前 + 今) : (今 - 前)
```

が常時 20 億超になり、`this+0x70 > 経過` が成立しない。
→ **待ちループ（`loc_54C734`: svcSleepThread / VBlank 待ち）に一度も入らない。**
→ フレームペーシングが消え、**CPU/GPU が出せる限りの速さで回る**。
論理は 1 フレーム 1 tick なので、歩き・アニメ・時間の進みが丸ごと速くなる。

例外は 2 つだけ:
1. カウンタが `0x00FFFFFF` 近傍を通る 2 フレーム（1 周 ≒ 21 億 VBlank ≒ 414 日に 1 度）
2. `this+0x14C <= 0` の経路（起動直後 3 フレーム）は素のまま

### 独立した裏取り 2 件

1. Vapecord `Addresses.hpp` 行 146 `//SPEED`、JPN 列 `0x54C6E8`（★作者の用途ラベル）
2. ROTATION `Sources/cheats.cpp:822` の **`FastGameSpeed()`** が
   `Write32(0x54c6e8, 0xe3e004ff)` / `0xe59400a0` と同じ 2 語を書いている

### ★キー指定の食い違い

利用者の貼り付けは `DD000000 00000012` / `00000022` だが、
`REFERENCES/CHEATS/speed.txt` の同じチートは **`00000110` / `00000120`**。

DD 行のマスクは 3DS の生 HID ビット。同じチート集の他項目のラベルで裏が取れる
（`0x101`=A+R、`0x102`=B+R、`0x042`/`0x082`=B+↑/B+↓、`0x8010`/`0x8020`=ZR+→/ZR+←）。
これは F-350 で `sub_540870` から起こした表とも一致する。

→ `0x110`=**R+→** / `0x120`=**R+←** がラベル通り。
   `0x012` / `0x022` は **B+→ / B+←** になってしまう。**`0x110` / `0x120` が正しい。**

### 未確定

`this+0x70` の値（30fps なら 2 / 60fps なら 1）。
`.text` 全域で `STR Rd,[Rn,#0x70]` 339 件を走査したが設定箇所を特定できなかった。
**実機で `sub_54C684` 入口に bp を張り `[R4+0x70]` を読めば 1 回で確定する。**
チートの効き方には影響しない（素の目標フレームレートを表すだけ）。

---

