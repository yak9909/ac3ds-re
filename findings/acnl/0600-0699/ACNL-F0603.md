---
id: ACNL-F0603
aliases:
- IDA-opus-5.5-F087
title: 'オンラインで見た目を伝える経路 — 美容室状態 0xB9 と状態 0 の抜け、プロフィール丸ごとの転送（2026-10-06、MEDIUM: 静的のみ。実機・通信未検証）'
summary: 解析モデル opus-5.5。旧 F-66 / F-67（reference/old_project/RE/FINDINGS.md）と docs/topics/network_packets.md を前提に、受信側の処理を読み直した。
date: '2026-10-06'
category: network
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1909196
- 6632388
- 6774548
- 6421592
- 1601048
- 1600804
- 8664628
- 6779300
- 6604840
- 6601672
- 6838072
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4651-4671
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F087: オンラインで見た目を伝える経路 — 美容室状態 0xB9 と状態 0 の抜け、プロフィール丸ごとの転送（2026-10-06、MEDIUM: 静的のみ。実機・通信未検証）

解析モデル opus-5.5。旧 F-66 / F-67（reference/old_project/RE/FINDINGS.md）と docs/topics/network_packets.md を前提に、受信側の処理を読み直した。
IDB: `PlayerState00_Enter 0x1D21CC` / `PlayerState00_Exit 0x6533C4` / `Player_SendStatePacketOnSetState 0x675F14` / `NetTransfer06_SendPlayerJoinData 0x61FC58` /
`NetTransfer06_ReceivePlayerJoinData 0x186E18` / `NetTransfer11_ReceivePlayerProfile 0x186D24` を命名・注記。
- 状態表 `g_PlayerStateTable 0x843634`: 1 状態 28 B（7 語）。索引は `Actor_SetState`（`表 + 7×状態`）と `PlayerState_ApplyRemotePacket`（`表 + 7×状態 + 6`）の 2 か所で一致。
  欄 = +0 入る（メンバー関数ポインタ 2 語）/ +8 毎フレーム / +0x10 抜ける（新しい状態とそのパケットを受け取る）/ +0x18 アクターが無い相手用。
- 状態パケット（0x33〜0x36、38 B）= ローカルのアクター +2236: +0 部屋 / +1 状態 / +2・+4 X×4・Z×4（s16）/ +6 向き / +8 通し番号（送るたび +1）/ +9 旗 / +14.. 状態ごとの引数（アクター +2250）。
  `Player_SendStatePacketOnSetState` が状態の属性（記述子とは別の表 `sub_64E960`、+7 bit3）が立つ状態だけ送る。
- 受信 `PlayerState_ApplyRemotePacket 0x6771A4`: 相手が同じ部屋にアクターを持てば `Actor_SetState(相手, 状態, パケット)`、無ければ記述子 +0x18。
- 相手の画面の見た目は「その端末が持つ、こちらのプロフィールの写し」から作られる（アクター生成 `0x64C828` / `0x64BBC8`）。写しの見た目を書くのは
  0xB9 の抜け `PlayerState_AppearanceChangeSyncLocal 0x685738`（髪型・髪色・目の色、帽子 = パケットの Item、アクセサリー = 無条件に空）と +0x18 `SyncRemote` だけ
  （`PlayerAppearance_SetHairColor` / `SetEyeColor` の呼び元はこの 2 つだけ）。アクターの控え（+2370 髪型 / +2372 髪色 / +2376 目の色）へ書くのは
  0xB9 の毎フレーム（アニメのマーカー）・`vc_UPDATE`・アクター生成だけ（全 STR 命令の走査）。
- **状態 0 の抜け `PlayerState00_Exit`**: 相手のアクターならパケットの位置・向きへ置き、`vc_UPDATE` = 写しのプロフィールから見た目を作り直す。状態 0 の毎フレームは空。
  → 改造していない相手でも「0xB9（新しい見た目・帽子）→ 状態 0 → 今の状態」の順に状態パケットが届けば、写しを書き換えてから読み直すので、アニメを待たずに変わる見込み（未検証）。
  アクセサリーは相手側の写しで空になる（0xB9 の抜けが無条件に消す）。
- 目の形（記録 +2）を写しへ書く経路は、プロフィール丸ごとの転送だけ: 下位種別 6（参加時。ホストは確保などもする）/ 種別 11（プロフィール + 50 B + セーブ準備の旗）。
  途中で送り直す安全性は未確認。写しが変わっても、相手が顔を読み直すのはアクターを作り直したとき（部屋の出入り）。
- 反証条件: 3 つのパケットを送っても相手側で変わらない、相手のアクターが状態 0 で消える／位置が飛ぶ、順序が入れ替わる。

