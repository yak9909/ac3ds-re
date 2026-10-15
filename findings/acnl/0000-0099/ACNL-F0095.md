---
id: ACNL-F0095
aliases:
- F-57
title: F-57 ゲーム内メニューを ID で開く仕組み — 日付変更ウィンドウは `MenuID 0x2E` — `HIGH`
summary: 「ゲーム内の時間変更ウィンドウを呼び出すチートがあったはず」という問いの答え。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7154396
- 7159692
- 7148336
- 9739550
- 9739551
- 7147688
- 5373228
- 9987044
- 9764284
- 5389092
- 1915524
- 2675284
- 8315548
- 9770427
- 9770426
- 7158964
- 9782856
- 6114440
- 3109764
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:3315-3409
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-57 ゲーム内メニューを ID で開く仕組み — 日付変更ウィンドウは `MenuID 0x2E` — `HIGH`

「ゲーム内の時間変更ウィンドウを呼び出すチートがあったはず」という問いの答え。
**Vapecord に `Game::OpenMenu(u8 menuID)` があり、`MenuID.txt` の `2E 日付変更` がそれ。**
FOXXY 側にはこの経路は無い（後述）。

### 呼び出しの連鎖（全部本ビルドで確認）

```
Menu_Open(menuId, arg)            0x6D2ADC   Vapecord の OpenMenu (USA 0x6D3F8C)
  -> Menu_RequestOpen(menuId,arg) 0x6D1330   ★要求を積むだけ
       g_MenuOpenState(0x949D1E) != 1 なら return 0   (1 = アイドル)
       g_MenuOpenState = 2; g_MenuOpenId(0x949D1F) = menuId; g_MenuOpenArg = arg
  -> Menu_PollOpen                0x6D10A8   毎フレーム
       if (state == 2 && menuId < 0x8C) {
           state = 3;
           UiScreen_OpenById(g_MenuIdToScreenId[menuId], a1, menuId, 0);
       }
  -> UiScreen_Create(screenId)    0x51FD2C
       g_UiScreenFactory[screenId].ctor()
```

| アドレス | 名前 | 内容 |
|---|---|---|
| `0x9863E4` | `g_MenuIdToScreenId` | **MenuID → 画面ID**（u16 × 140、`0x00`-`0x8B`） |
| `0x94FDBC` | `g_UiScreenFactory` | **画面ファクトリ表**（`{ctor, 0x523B24}` × 669） |
| `0x949D1E/1F/20` | `g_MenuOpenState` / `Id` / `Arg` | 開き要求の状態 |
| `0x1D3A84` | `UiScreen_RegisterFactoryTable` | 表と件数 669 を登録 |

### `MenuID.txt` の記述がすべてコードで説明できた

| MenuID | 画面ID | クラス | `MenuID.txt` |
|---|---|---|---|
| `0x00` | 544 | `BsMenuItem` | 持ち物欄 ✓ |
| `0x01` | 546 | `BsMenuMyDesign` | マイデザイン欄 ✓ |
| `0x02` | 545 | — | 図鑑 |
| **`0x2E`** | **557** | **`BsMenuSetupTime`** | **日付変更【★】** |
| `0x2F` `0x30` `0x31` | 557 | 同上 | 約束の時間 / 手紙の日付 / 誕生日変更 |
| `0x8B` | **669** | — | すぐ閉まる |
| `0x8C`- | 1748 等 | — | 何も表示されない |

- **`0x8B` の「すぐ閉まる」** — 画面ID 669 は表（0-668）の**範囲外**で factory が NULL
- **`0x8C` 以降の「何も表示されない」** — `Menu_PollOpen` の `menuId < 0x8C` で弾かれる

**有志のメモが観察で書いた挙動が、コード側の境界値とぴたり一致した。**

### 日付変更ウィンドウの本体

- クラス **`BsMenuSetupTime`**（`SetDateTimeBg` を内部に持つ）
- コンストラクタ `BsMenuSetupTime_Ctor` (`0x28D254`)
- ファクトリ `UiScreenFactory_BsMenuSetupTime` (`0x7EE29C`) — 14528 バイト確保して構築

**開き方は 2 通り:**

```
Menu_Open(0x2E, 0)        JPN 0x6D2ADC   ゲーム本来の経路（状態管理つき）
UiScreen_Create(557)      JPN 0x51FD2C   画面を直接生成
```

`Menu_Open` の方が安全（`g_MenuOpenState` を見るので二重に開かない）。

### 2 つのプラグインの時間変更方式の違い

| | 方式 | ゲーム内 UI |
|---|---|---|
| **Vapecord** | CTRPF の `Keyboard` で入力 → `SetCurrentTime` がセーブデータと `g_RealTimeNs` に加算（F-55） | **使わない** |
| **Vapecord** | `Game::OpenMenu(menuID)` は**別機能**として存在（`SaveMenuChanger` で使用） | **`0x2E` で開ける** |
| **FOXXY** | OSD に自前ボタンを描画 → `ExecuteAnimationWrapper` でアニメ再生 | **使わない** |

FOXXY の "Loading clock, Please wait..." は**FOXXY 自身の OSD 表示**で、
ゲームの時計ウィンドウではない（`0x9515BB`/`0x9515BA` から時分を読んで自前描画している）。

**【訂正 / F-58】上記は誤り。FOXXY は実際にゲーム本来の日付変更ウィンドウを開いている。**
`timetravelr` の OSD 処理だけを見て、同じメニュー項目が同時に当てている
コードパッチ（`0x6D3CB4` の MenuID 差し替え）を読み落としていた。詳細は F-58。

### FOXXY について

- **USA 専用。** `main.cpp` が `Process::GetTitleID() == 0x0004000000086300`（TID_USA）で判定
- **地域変換の仕組みを持たない。** アドレスは Vapecord の表の **USA 列**と一致する
  （`0x954648`=GAMEPOINTER、`0x5D4C88`=COORDOFFSET、`0x2F7384`=GETROOM）
- **本ビルドで使うには表で JPN へ変換が必要**

### 【訂正】アニメ ID の読み違い

FOXXY が `catchbug` で `0x71` を使っているのを見て
「本解析の 71 = `scoop_swing1` と矛盾する」と考えたが、**私の読み違い**だった。

- FOXXY の `0x71` は**十六進**で **113** = `ts_net_inertia1`（あみ）
- 本解析のスコップ帯は**十進 71-79** = `0x47`-`0x4F`

矛盾はなく、両者は整合している。**進数を取り違えた。**

---

