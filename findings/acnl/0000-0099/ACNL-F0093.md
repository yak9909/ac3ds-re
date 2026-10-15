---
id: ACNL-F0093
aliases:
- F-55
title: F-55 Vapecord のコードを手がかりにした関数解析（時刻・部屋・通信） — `HIGH`
summary: F-54 の対応表を使い、プラグインが実際に呼んでいる関数を本ビルドで解析した。
date: '2026-09-08'
category: network
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9790720
- 5686716
- 1048576
- 9790704
- 9790712
- 5679472
- 5681728
- 3126180
- 3208692
- 9769786
- 8925992
- 6438784
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:3116-3221
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-55 Vapecord のコードを手がかりにした関数解析（時刻・部屋・通信） — `HIGH`

F-54 の対応表を使い、プラグインが実際に呼んでいる関数を本ビルドで解析した。
**「実機で動くコードが指しているアドレス」は出発点として強い。**

### 時刻 — `g_RealTimeNs` は「システム時刻 − オフセット」

プラグインの `Game::SetCurrentTime` は 2 箇所に書く:

```cpp
Town::GetSaveData()->CurrentTime += Time;   // セーブデータ
*(u64 *)RealTime.addr           += Time;    // ★実行時クロック
```

`Time` は**ナノ秒**（1 分 = `60000000000`）。`RealTime` は JPN `0x956500`。

これを参照するのは `0x56A9xx`-`0x56C6xx` の時刻モジュール 7 箇所のみ。
`Time_UpdateRealTime` (`0x56C5BC`) が実体:

```c
g_SystemTimeNs = Time_GetSystemNs();
if (Room_HasFlags(0x80000, room) || Room_HasFlags(0x100000, 0))
    dword_956510 = g_SystemTimeNs - g_TimeOffsetNs;   // 特定の部屋では別スロット
else
    g_RealTimeNs = g_SystemTimeNs - g_TimeOffsetNs;
```

| アドレス | 名前 | 内容 |
|---|---|---|
| `0x956500` | `g_RealTimeNs` | ゲーム内の現在時刻（ナノ秒 u64） |
| `0x9564F0` | `g_SystemTimeNs` | システム時刻 |
| `0x9564F8` | `g_TimeOffsetNs` | 差し引くオフセット |
| `0x56C5BC` | `Time_UpdateRealTime` | 毎フレーム更新 |
| `0x56A970` | `Time_LoadFromSave` | セーブデータ +0x62120 から読み込み |
| `0x56B240` | `Time_GetSystemNs` | システム時刻取得 |
| `0x2FB3A4` | `Date_GetRaw` | 日付の生値 |
| `0x30F5F4` | `Date_FromRaw` | 生値 → `ACNL_Date` 構造体 |

**時刻をずらすなら `g_TimeOffsetNs` を動かすのが筋。**
`g_RealTimeNs` を直接書いても `Time_UpdateRealTime` に上書きされ得る
（プラグインがセーブデータ側にも書いているのはそのためと思われる）。

### 部屋フラグ — F-47 の「謎のゲート」が解けた

`FieldObj_TrampleAt` の冒頭にあった正体不明の 2 関数が判明した。

```c
Room_GetCurrentId()      // = g_CurrentRoomId (0x95133A) を読むだけ。165 = 部屋なし
Room_HasFlags(mask, id)  // return id != 165 && (mask & ~g_RoomFlagTable[id]) == 0;
```

`g_RoomFlagTable` (`0x883328`) は **u32 × 166 の部屋フラグ表**。

したがって F-47 の手順 1 は

```c
Room_HasFlags(4, Room_GetCurrentId())
```

= **「今いる部屋がフラグ bit2 を持つか」** という部屋種別の判定だった。
`FieldObj_ResolveAxeAction` の `Room_HasFlags(32, ...)` も同じ表を引いている。

**165 (0xA5) がこのコードベース共通の「無効」番兵**であることも確認できた
（`g_ActiveFieldActions` の playerNo、`Item_PlaceItem` の `-91`）。

### 通信 — ラベルに騙されない例

Vapecord は `0x623F80` を **`TRAMPLE`** と名付けている
（`TRAMPLE1` = `Field_SetItemAt`、`TRAMPLE3` = `Field_MarkDirty` と並んでいる）。

しかし中身は:

```c
Net_SendPacket(packetType, dest, buf, size) {
    Net_PacketBegin(mgr);
    if (buf && size) Net_PacketWrite(mgr, buf, size);
    return Net_PacketSend(mgr, packetType, dest);
}
```

**汎用のパケット送信**で、呼び出し元は 12 箇所以上に散っている。
`drop_method.txt` の
`netgame::NetGameMgr::SendPacketToPlayer(PLAYER_PACKET_DROP, dest, buf, 0x16u)` と一致する。

- `Item_PlaceItem` の `Net_SendPacket(58, 0, &rec, 22)`
- `FieldObj_TrampleAt` の `Net_SendPacket(71, 4, &rec, 8)`

**`TRAMPLE` は「作者が踏みつけ機能で使った」というだけのラベル。**
CLAUDE.md の「チートの名前は作者の主観的ラベルで仕様書ではない」がそのまま当てはまる。
**呼び出し元の数を数えれば一発で分かる**（専用関数なら数箇所、汎用なら散らばる）。

### 効果音 ID の形式

`Game::PlaySound(u16 id)` は `Game_PlaySound(0x1000000 + id)` を呼ぶ。
**F-47 の `FieldObj_PlayPlantEffect` に出てくる `0x1000639` / `0x100063A` は
効果音 ID `0x639` / `0x63A` のこと**だと確定した。

### この資料の使い方

- **アドレスの出発点としては強い**（実機で動作するコードが指している）
- **ラベルは弱い**（作者の用途ラベル。`TRAMPLE` が汎用パケット送信だった例）
- 表は**プラグインが触る箇所の抜粋**であって網羅的ではない。
  本解析で未解決だった 40 アドレスを引いたところ、表にあったのは 5 件だけだった

---

