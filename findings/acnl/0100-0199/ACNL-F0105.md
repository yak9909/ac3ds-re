---
id: ACNL-F0105
aliases:
- F-67
title: 'F-67: 髪型変更状態 `0xB9` が帽子・アクセサリを消し、2 段アニメが反映を遅らせる'
summary: 'confidence: **MEDIUM**（削除先・同期先・アニメ分岐を静的に確認。提案パッチは実機未検証）'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1092684
- 1914848
- 6828472
- 6828776
- 6828788
- 6838072
- 6838180
- 6838192
- 6863352
- 6863436
- 6863448
- 6848036
- 7380972
- 7380544
- 6856156
- 6848268
- 6828604
- 6829180
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4490-4574
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-67: 髪型変更状態 `0xB9` が帽子・アクセサリを消し、2 段アニメが反映を遅らせる
confidence: **MEDIUM**（削除先・同期先・アニメ分岐を静的に確認。提案パッチは実機未検証）

### 消えるのは描画だけではなく、衣装データの先頭 2 枠

プレイヤーアクターの `player+0x920` からは 4B Item が 8 個並ぶ。
`PlayerOutfit_Copy` (`0x10AC4C`) はこの 8 Item と末尾 1 byte（計 `0x21` byte）を一括コピーし、
`PlayerRender_SetOutfitBlock` (`0x1D37E0`) は同じブロックを描画側へ渡す。
プロフィール側の対応は `profile+10` から始まり、既存の `Player_Outfit` 構造体とも一致する。

| actor off | profile off | 衣装枠 |
|---|---|---|
| `+0x920` | `+10` | Hat（帽子） |
| `+0x924` | `+14` | Accessory（眼鏡・アクセサリ） |
| `+0x928` 以降 | `+18` 以降 | 上着、下着、ボトム、靴下、靴、手持ち品 |

`PlayerState_AppearanceChangeUpdate` (`0x6831B8`) はアニメ 237 `barber_set1` の
マーカー到達時に、次を明示的に行う。

```c
Item_Copy(player + 0x920, &ItemToPlace); // 0x6832E8: Hat = empty
Item_Copy(player + 0x924, &ItemToPlace); // 0x6832F4: Accessory = empty
Player_RebuildAppearanceFromCache(player);
```

さらに状態 `0xB9` を抜けるとき、記述子 `+0x10` の
`PlayerState_AppearanceChangeSyncLocal` (`0x685738`) がプロフィールにも書き戻す。
通常の髪型変更は packet Item に空 Item を渡すので、`0x6857A4` が Hat を空にし、
`0x6857B0` は Accessory を無条件に空にする。アクターを生成できないリモート相手用の
`PlayerState_AppearanceChangeSyncRemote` (`0x68B9F8`) も `0x68BA4C/0x68BA58` で同じ処理をする。

したがって「帽子・アクセを外すこと」という配布文の注意は、単なる表示上の都合ではない。
美容室の正規状態が先頭 2 衣装枠を意図的に外す設計であり、それを虫取り網から直接起動したため、
装備中データまで空 Item に置換される。

### 遅延は 2 本のアニメと 4 個の待機ゲート

通常の髪型変更は次の順に進む。

1. enter `0x687E24` が anim 237 `barber_set1` を開始する。
2. `AnimSlot_CrossedMarker` (`0x709FEC`) を待ち、Hat/Accessory を外して一度再構築する。
3. `AnimSlot_IsFinished` (`0x709E40`) を待ち、anim 238 `barber_cut1` を開始する。
4. 238 のマーカーを待って髪型・髪色を `player+0x942/+0x944` へ適用する。
5. 238 の終了を待って状態 15/16/18 のいずれかへ戻る。

目色変更では 239、Mii マスクでは 240 が第 2 段になる。
髪型値のポーリングが遅いのではなく、**ゲーム自身が 2 本の演出のマーカーと終了を待っている**。

### 即時化の設計

ローカルだけなら、プロフィールの髪型・髪色を書いて `vc_UPDATE` (`0x689DDC`) を呼ぶ経路が最短。
これは衣装 8 枠をプロフィールから丸ごと再ロードするので頭装備を保ったまま即時反映できる。
ただし `vc_UPDATE` 自身には送信処理がなく、これだけではオンラインへ伝播しない。

標準の状態パケットを残す場合は、次の 3 命令で状態 `0xB9` を 1 update tick に短縮できる。

- `0x687F0C`: 開始 anim を 237 から 238 にし、頭装備を外す第 1 段を丸ごと迂回
- `0x68323C`: 第 2 段のマーカー判定を成功扱いにして髪型を即適用
- `0x68347C`: 第 2 段の終了判定を成功扱いにして即退出

プロフィールの頭 2 枠を保つには、これに `0x6857A4/0x6857B0` と
`0x68BA4C/0x68BA58` の Item コピー抑止が必要。候補 AR コードと復元値は
`DOCS/ar_codes.md` に記載した。全て静的構成で実機未検証。

### オンラインでの限界

`Actor_SetState` は enter 後、update より前に `sub_675F14` を通って状態 `0xB9` の
38B パケットを送る。退出先 15/16/18 は同じ送信フラグを持たないため、上記の短縮でも
`0xB9` パケット自体は送信され、髪型変更はオンラインへ伝播する。

ただし処理速度は各クライアントの実行コードで決まる。

- パッチ済みの受信側: 受信した相手アクターにも同じ短縮処理が走り、ほぼ即時になる。
- 未パッチの受信側: stock の 237→238 を実行するため、相手からは従来どおり遅れて見える。
- 未パッチの受信側の頭装備: packet は見た目 Item 1 個しか持たず、Accessory は受信側で無条件に空にされる。送信側だけでは Hat と Accessory の両方を保持できない。

未改造の相手にも最終的に頭装備を戻すなら、状態 `0x36` の衣装変更を Hat/Accessory に対して
後送するプラグイン処理は構成できる。ただし相手の `0xB9` 完了後まで待つ必要があり、
「相手側も一瞬で、かつ両方保持」は標準 `0xB9` プロトコルだけでは実現できない。

提案パッチは正規の目色変更・Mii マスク変更にも同じ状態ハンドラを使うため、
髪型チートと同時だけ有効にし、使用後は必ず復元すること。

---

