---
id: ACNL-F0096
aliases:
- F-58
title: F-58 【訂正】FOXXY はゲーム本来の日付変更ウィンドウを開いていた — `HIGH`
summary: F-57 で「FOXXY にはゲーム内 UI を開く経路は無い」と書いたが**誤り。**
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7158964
- 6650032
- 6862204
- 6758224
- 6831792
- 7749068
- 7152780
- 7152792
- 7152796
- 7147688
- 5373228
- 6644648
- 6752840
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:3410-3480
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-58 【訂正】FOXXY はゲーム本来の日付変更ウィンドウを開いていた — `HIGH`

F-57 で「FOXXY にはゲーム内 UI を開く経路は無い」と書いたが**誤り。**
ユーザーの記憶が正しく、FOXXY は**ゲーム本来の日付変更ウィンドウ**を開いている。

見落とした理由: `timetravelr` が呼ぶ `ExecuteAnimationWrapper` だけを見て、
**同じメニュー項目が同時に当てているコードパッチを読んでいなかった。**

### 仕組み

`cheats.cpp` の OSD メニュー項目が有効化されるとき:

```cpp
OSD::Run(timetravelr);
Process::Write32(0x6D3CB4, 0xE3A0002E);   // MOV R0, #0x2E   ★MenuID を差し替え
Process::Write32(0x6578B0, 0xE3A0101A);   // 0x17 -> 0x1A
Process::Write32(0x68B57C, 0xE3A01006);   // 6 -> 6（無効化時と同じ値＝効いていない）
Process::Write32(0x671F50, 0xE3A01006);   // 0x42 -> 6
// 無効化では 0x4A / 0x17 / 0x42 に復元
```

そして OSD の "Time" ボタンを押すと:

```cpp
Player::ExecuteAnimationWrapper(idx, 0x3F /*hole_bury1*/, 0, 1, 1, 1, 0, x, y, true);
```

### 本ビルドで辿った経路

```
アニメ 0x3F = hole_bury1（穴に埋める）を再生
  -> PlayerAction_BuryUpdate      0x683EB0   サブ状態 1 かつ this+2255 == 0
  -> PlayerAction_OpenItemSelect  0x763DCC
  -> Menu_OpenItemSelect          0x6D248C
       0x6D2498  MOV R0, #0x4A    ★FOXXY がここを #0x2E に書き換える
       0x6D249C  BL Menu_RequestOpen
  -> Menu_PollOpen                0x6D10A8
  -> UiScreen_Create(557)         0x51FD2C
  -> BsMenuSetupTime                        ★ゲーム本来の日付変更ウィンドウ
```

**「穴に埋める」動作が本来開く「持ち物欄③」(MenuID 0x4A) を
「日付変更」(MenuID 0x2E) に差し替えている。**

### アドレス対応（USA -> JPN）

| USA | JPN | 素の値 | 内容 |
|---|---|---|---|
| `0x6D3CB4` | **`0x6D2498`** | `E3A0004A` | `MOV R0,#0x4A` → `#0x2E` |
| `0x6578B0` | `0x6563A8` | `E3A01017` | `MOV R1,#0x17` → `#0x1A`（未解析） |
| `0x671F50` | `0x670A48` | `E3A01042` | `MOV R1,#0x42` → `#6`（未解析） |
| `0x68B57C` | 未特定 | `E3A01006` | **有効時も無効時も同じ値＝死んだ行** |

`0x6D3CB4` は Vapecord の表に無いので、**近傍の既知ペアから差分を出しても外れた**
（`OPENMENU` 由来の -0x14B0 では不一致）。
**JPN 側で `E3A0004A` を直接検索して `0x6D2498` を特定し、
直後の `BL` が `Menu_RequestOpen` に着くことで確認した。**
表に無いアドレスは差分推定ではなく**命令列で探すこと。**

### 教訓

- **チートの「実装」はメニュー項目の全体を読む。**
  OSD やホットキーの処理だけ見ると、同時に当てているコードパッチを見落とす
- **`Write32(addr, 0xE3A0xxxx)` は「定数の差し替え」で、
  どのアドレスの何という定数かを追うと機能の入口が分かる。**
  今回は `MOV R0,#imm` の imm が MenuID そのものだった
- 有効時と無効時で**同じ値**を書いている行は死んでいる（`0x68B57C`）。
  ここでも「チートの行がすべて必要とは限らない」が当てはまる

---

