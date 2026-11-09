---
id: ACNL-F0750
aliases: []
title: "地図メニュー準備旗 vc_MAPBOOL(0x949C30)の型と NetGameMgr 本体ポインタ g_NetGameMgrPtr(0x94D644)の型"
summary: "0x949C30 vc_MAPBOOL は 1 バイトの旗（unsigned __int8）で、村の地図メニュー BsMenuMapVillage の作成完了で 1、破棄または別種の地図画面を開くときに 0 になる。0x94D644 g_NetGameMgrPtr は NetGameMgr 本体へのポインタ（構造体の型が無いので void *）。"
date: 2026-11-09
category: ui
build: acnl_jpn_v15
confidence: MEDIUM       # LOW / MEDIUM / HIGH
tool: IDA
addresses:
- 0x949C30
- 0x94D644
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

1. `0x949C30` `vc_MAPBOOL` は 1 バイトの旗。型は `unsigned __int8` を付けた。名前は旧名（`vc_` で始まる物は残す規則）のまま変えない。役割は「村の地図メニュー（`BsMenuMapVillage`）が作成を終えて使える状態か」。作成完了で 1、破棄、または別種の地図画面を開くときに 0。確度 MEDIUM（読み書き 12 関数の静的解析。実機未確認）。
2. `0x94D644` `g_NetGameMgrPtr` は `netgame::NetGameMgr` 本体へのポインタ。構造体の型が無いので `void *` を付けた。確度 MEDIUM（静的のみ）。

## 根拠

### vc_MAPBOOL（0x949C30）

- 書き込み（すべて STRB／1 バイト）:
  - `0x2B3A04..0x2B3A0C` `BsMenuMapVillage_CreateStep`: 最終段（case 0xA、vtable `off_84B204` 設定・名前 "BsMenuMapVillage" を入れた直後）で 1。
  - `0x2B3CA8` `sub_2B3C64`（同クラスの破棄段。`BsMenuMapList_Release` 等の後）で `dword_949C34 = 0`・`vc_MAPBOOL = 0`。
  - `0x6D0928` `sub_6D0928`: 部屋の種類ごとに `UiScreen_OpenById(0x21A/0x21C/0x21D/0x21B/0x21E, ...)` で別種の地図画面を開くとき `vc_MAPBOOL = 0`（`dword_949C34..48` に画面を保存）。
- 読み取り（すべて LDRB／真偽判定）:
  - `0x6D0B54` `BsMenuMgr_MapOutByKind`: 冒頭で `if (!vc_MAPBOOL)` なら何もしない。1 のときだけ種別（+64）に応じた `BsMenuMap_RequestOut` で地図を退場させる。
  - `0x6D1428` `BsMenuMgr_ProcessMapCommand`（+484 が地図画面）: `v10 && vc_MAPBOOL`、`vc_MAPBOOL == 0` で退場の可否を決める。
  - `0x6D1E14`: `*(a1+484) && vc_MAPBOOL` のときだけ続きを処理する（`vc_MENU_FLAGS & 0x200` の判定へ進む）。`0x6D34AC`: 同じ `+484 && vc_MAPBOOL` のときだけ `sub_6D0D74` を呼ぶ。
  - `0x6D474C` `BsMenuTab_TabSelectUpdate`: `!*((_DWORD *)off_949D4C + 121) || vc_MAPBOOL` でタブ遷移の可否に使う。
- 以上から「地図画面が存在し、かつ村の地図の作成が完了している」旗として使われる。型は全アクセスが 1 バイトの 0/1 なので `unsigned __int8`。

### g_NetGameMgrPtr（0x94D644）

- 書き込みは 3 か所だけ。`0x616D8C` `sub_616D8C`: 未設定のときに `sub_618614` の返値（管理本体）を保存。`0x61769C`・`0x6176EC`: 破棄時に `sub_618868(g_NetGameMgrPtr)` のあと `nullptr` を入れる。
- 隣の `0x94D648`（`vc_GAMEPOINTER`）は `SingletonDisposer`（vtable `0x904FC4`）で、本体ではない（既存の ACNL-F0633 の周辺訂正と一致）。
- 読み取りは約 395 関数。例: `0x182488` は `*(g_NetGameMgrPtr + 0x229) = 1` を書く。構造体 `NetGameMgr` は symbols の型（`types/local_types.h`）に無いため `void *` とした。

## 反証条件・未確認点

- vc_MAPBOOL が「下画面」の地図かどうかは、書き出しからは確かめていない（画面の割り当てを追っていない）。依頼文の「下画面の地図が開いているか」は、このため旗の役割の言い方として採らなかった。
- `0x6D0928` の部屋条件（`Room_HasFlags` の各値）と画面 ID `0x21A..0x21F` の意味は未確認。`0x219` が村の地図（`BsMenuMapVillage`）かどうかも、命名された型との直接の対応は未確認。
- 実機での 0/1 の遷移の確認なし。
- g_NetGameMgrPtr 型を `NetGameMgr *` にするには構造体の定義（大きさ 0x13300 以上）が要る。別作業。
