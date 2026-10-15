---
id: ACNL-F0098
aliases:
- F-60
title: 'F-60: Vapecord の時間設定チートと、ゲーム自身の時計確定経路'
summary: 'confidence: **HIGH**（静的解析。Vapecord のソースと逆コンパイルが独立に一致）'
date: '2026-09-08'
category: time
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9819400
- 9790720
- 5679556
- 3125064
- 5686716
- 9790704
- 9790712
- 5679472
- 5679892
- 2672064
- 2675284
- 7152792
- 4914564
- 1993908
- 4914572
- 4914600
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:3552-3686
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-60: Vapecord の時間設定チートと、ゲーム自身の時計確定経路

confidence: **HIGH**（静的解析。Vapecord のソースと逆コンパイルが独立に一致）

### 1. 入口は 2 つ

`REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master`

| 入口 | 実装 | 操作 |
|---|---|---|
| キーボード版 | `ExtraCodes.cpp:171 TTKeyboard` | 前進/後退を選んでから 分・時・日・月・年 を順にスライダ入力 |
| ホットキー版 | `ExtraCodes.cpp:206 TimeTravel` | `R + →` で進む / `R + ←` で戻る、1 分ずつ連射 |

登録は `MenuCreate.cpp:560` の `EntryWithHotkey(...)`、ID は
`MenuEntryIds.hpp:216 ExtraTimeTravel = Make(GroupExtra, 0x000A)`。

スライダの上限は `TimeMax[5] = {60,24,30,12,50}` を `SetSlider(0, TimeMax[i]-1)` で使うので
**分 0-59 / 時 0-23 / 日 0-29 / 月 0-11 / 年 0-49**。

連射カーブは `PressedTicks` で
`<50 tick は 8 tick に 1 回 → 以降 3 tick に 1 回 → 100 tick 超で毎 tick`。

### 2. どちらも `Game::SetCurrentTime` に落ちる

`src/core/game_api/Game.cpp`。ns へ換算して**差分**を作り、2 か所へ加算する。

```
Δ = 分*60e9 + 時*3600e9 + 日*86400e9 + 月*30*86400e9 + 年*365*86400e9
forward でなければ Δ = −Δ
Town::GetSaveData()->CurrentTime += Δ      … セーブデータ
*(u64 *)0x95D508 (USA) += Δ                 … JPN 0x956500 = g_RealTimeNs
```

**★換算は近似**。1 ヶ月 = 30 日固定、1 年 = 365 日固定なので
**「12 ヶ月」= 360 日で「1 年」= 365 日と一致しない**。うるう年も月の大小も見ていない。

### 3. 書き込み先 2 つの正体（本解析側）

| Vapecord | 本ビルド | 実体 |
|---|---|---|
| `RealTime` USA `0x95D508` | JPN **`0x956500`** | `g_RealTimeNs` (s64, ns) |
| `Town::GetSaveData()->CurrentTime` | **`D_GARDEN + 0x621A0`** | セーブデータ上の現在時刻 |

セーブ側のアドレスは**独立に一致を確認**した。

- Vapecord: `Town::GetSaveData()` = `D_GARDEN + 0x53424`、
  `GameStructs.hpp` の `//0x…` 注記は **D_GARDEN からの絶対オフセット**なので
  `CurrentTime //0x621A0` の構造体内相対は `0x621A0 − 0x53424 = 0xED7C`。
- 本解析: `Time_StoreToSave`(`0x56A9C4`) が `Save_GetTownBase() + 401696`、
  `Save_GetTownBase`(`0x2FAF48`) = `D_GARDEN(dword_955F8C) + 128`
  → `D_GARDEN + 0x80 + 0x62120` = **`D_GARDEN + 0x621A0`**。一致。

補強: `Time_AnchorFromSave` は `D_GARDEN + 401848 = +0x621B8` を触るが、
これは `GameStructs.hpp` の `TownID TownData1; //0x621B8` にそのまま一致する。

### 4. なぜ 2 か所書く必要があるのか（★核心）

`g_RealTimeNs` は**権威ではなく導出値**。

```
Time_SetFromDate(date)  0x56C5BC   ← 旧名 Time_UpdateRealTime は誤り
    g_SystemTimeNs(0x9564F0) = Time_GetSystemNs(date)
    g_RealTimeNs  (0x956500) = g_SystemTimeNs − g_TimeOffsetNs(0x9564F8)
```

`E8901006 / E8831006 / EBFFFB1B`（LDM R0 → STM R3 → BL）で
**R0 が入口から不変のまま `Time_GetSystemNs` へ渡る**ことを生バイトで確認した。
引数は日付構造体で、この関数は毎フレーム更新ではなく**「日付から時刻を確定する」**処理。
呼び出し元は 6 箇所しかない。

したがって `g_RealTimeNs` へ直接足した分は `Time_SetFromDate` が走ると消える。
Vapecord が同時にセーブ側 `CurrentTime` にも足しているのは、

- `g_RealTimeNs` … **即座に見た目へ反映する**ため
- `CurrentTime` … `Time_LoadFromSave`(`0x56A970`) → `Time_AnchorFromSave`(`0x56AB14`)
  で読み戻される**永続側**

という役割分担。片方だけでは成立しない。

**★時刻をずらす「筋の良い」ノブは `g_TimeOffsetNs`(0x9564F8)。**
`g_RealTimeNs = 本体日付 − g_TimeOffsetNs` と**減算**なので、
ゲーム内時刻を進めたければこの値を**減らす**（向きに注意）。
書き込みは `Time_AnchorFromSave` と `sub_56BBE8` の 2 箇所だけ。

### 5. ゲーム自身の時計ウィンドウの確定経路

`BsMenuSetupTime_Update`(`0x28C5C0`, `BsMenuSetupTime_Ctor` 0x28D254 と同一クラス領域)

```
UiAnim "G_inout_00" が終わるのを待つ
結果コード 46 かつ byte_949D3B == 1:
    部屋 99 なら sub_150054(this+1564)
    Time_SetFromDate(this+1564)     ← this+1564 = 入力された日付構造体
    Time_StoreToSave()              ← g_RealTimeNs をセーブ CurrentTime へ
    部屋 93 なら sub_56C39C()
結果コード 47: 終了処理
```

**Vapecord の `SetCurrentTime` は、この 2 段（時刻を作る → セーブへ書く）を
絶対日付ではなく差分で直接叩いているだけ**だと分かる。

### 6. FOXXY との対比

| | Vapecord | FOXXY (F-58/F-59) |
|---|---|---|
| 方式 | メモリへ差分を直接加算 | ゲームの時計ウィンドウを開かせる |
| 触る所 | `g_RealTimeNs` + セーブ `CurrentTime` | `0x6D2498` の `MOV R0,#0x4A`→`#0x2E`（穴に埋める→時計窓）ほか姿勢 2 箇所 |
| 確定処理 | 自前 | ゲームの `BsMenuSetupTime_Update` に任せる |
| 精度 | 月=30日 / 年=365日 の近似 | ゲーム側の正規処理なので正確 |
| UI | CTRPF のキーボード | ゲーム内 UI |

FOXXY のほうが**ゲームの正規経路を通る**ぶん整合性が高い。
Vapecord は窓を開かずに済むぶん速く、ホットキー連射ができる。

### 7. 別物なので混同しないもの

`MenuCreate.cpp:482` の `Daytime` / `EnvironmentDaytime`
(`EnvironmentCodes.cpp:17`) は**時刻ではなく採光のパッチ**。
USA→JPN: `DAY1 0x4AFD84` / `DAY2 0x1E6CB4` / `DAY3 0x4AFD8C` / `DAY4 0x4AFDA8`。
未解析（TODO）。

### IDA へ反映済み

| addr | name |
|---|---|
| `0x56C5BC` | `Time_SetFromDate`（旧 `Time_UpdateRealTime` を訂正） |
| `0x56A9C4` | `Time_StoreToSave` |
| `0x56AB14` | `Time_AnchorFromSave` |
| `0x28C5C0` | `BsMenuSetupTime_Update` |
| `0x2FAF48` | `Save_GetTownBase` |

コメントは `0x956500` / `0x9564F0` / `0x9564F8` にも入れた。

---

