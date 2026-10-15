---
id: ACNL-F0463
aliases:
- IDA-opus-5.5-F070
title: 'ゆうめいなキノコで大きくなる仕組みと、プレイヤーの大きさは通信に乗らないこと（2026-09-30、MEDIUM: 静的＋Vapecord の送信側の形と受信側の独立一致。実機未観測）'
summary: '解析ソフト: IDA（主 IDB）/ 解析モデル: opus-5.5。利用者の問い: 椅子の座る高さはオンラインに反映される（他人にも見える高さ変更チートがある）。'
date: '2026-09-30'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 8664628
- 6841860
- 6816684
- 6822860
- 6862968
- 8664564
- 1913776
- 8662048
- 6779300
- 1597032
- 8870936
- 6794756
- 6740116
tags:
- player
supersedes: []
source: IDA:work/FINDINGS.md:1384-1409
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F070: ゆうめいなキノコで大きくなる仕組みと、プレイヤーの大きさは通信に乗らないこと（2026-09-30、MEDIUM: 静的＋Vapecord の送信側の形と受信側の独立一致。実機未観測）

解析ソフト: IDA（主 IDB）/ 解析モデル: opus-5.5。利用者の問い: 椅子の座る高さはオンラインに反映される（他人にも見える高さ変更チートがある）。
ゆうめいなキノコで大きくなるアニメも他人から見える → いじれば他人にも見える大きさ変更ができるか。骨格アニメなら反映しないかも。ほかにパケットで大きさを書く処理はあるか。
- **食べる → 状態 0xD6**: 食べる状態の毎フレーム sub_64FE18 が、品物 == 0x209D（famous mushroom。All_ACNL_Items）なら区切りで Actor_SetState(プレイヤー, 0xD6)。
  状態表 **g_PlayerStateTable 0x843634**（0xEB 項目 × 28 B = {始め, 毎フレーム, 終わり（各 8 B のメンバ関数ポインタ）, +0x18 = 受信した状態を相手側で当てる関数}）。
  0xD6 = 始め 0x686604 / 毎フレーム 0x6803AC / 終わり 0x681BCC / +0x18 = 空関数 0x68B878。
- **大きくなる方法 = モデル全体の拡大率（骨格アニメではない）**: 毎フレーム 0x6803AC が数え +0x1470（u16）÷ 6 で **g_MushroomGrowScale 0x8435F4**
  {1, 1, 1.08, 1.35, 1.8, 1.8, 1.8, 1.35, 1.08, 1, 1} を引き、**PlayerModel_SetUniformScale 0x1D33B0**(プレイヤー+0x1B4, s0) と +0x858 へ。
  0x1D33B0 = モデル+0x238（= プレイヤー+0x3EC）に控え、違えば TransformNodeHolder_SetScale(モデル+0x78, {s,s,s})。11 段を過ぎると 1.0 に戻して次の状態へ。終わり 0x681BCC も 1.0。
  +0x858 は sub_64E9F8 が +0x848 へ写し（0 なら状態ごとの表 0x842C20 の [2] × 0.01 へ寄せる）、+0x848 は影の描画 sub_68BF44 が使う。
- **拡大率を書く場所の全数**: PlayerModel_SetUniformScale の呼び出し 13 件（xref）はすべて状態の関数で、値は定数（リテラルを読んだ）: 1.0 が 10 件・0.82 が 1 件（sub_676D78、状態 0x31 のとき）・
  表が 2 件（0xD6）。**パケットの中身を渡す箇所は無い**。TransformNodeHolder_SetScale の呼び出し 36 件もプレイヤーのモデルに対しては 0x1D33B0 経由だけ（ほかは家具・fgobj など）。
- **状態パケット**: 受信 = **PlayerState_ApplyRemotePacket 0x6771A4**（呼ぶのは vc_ANTI_ANIM_1〜4 0x185E68.. の 4 本 = プレイヤー 1〜4、ハンドラ表 0x875C18）。
  pkt[1] = 状態番号、相手が同じ部屋にいれば Actor_SetState(相手, pkt[1], pkt) → 状態の引数ブロック（プレイヤー+0x8BC に写る。+0x8CA = pkt+0xE）。いなければ状態表 +0x18。
  送信側の形は Vapecord の SendAnimPacket（[0] = 部屋、[1] = 状態番号、+0xE.. = 状態ごとの引数、AnimData.cpp）と一致（独立した 2 経路）。
  **0xD6 の始めは引数を読まない** → 相手の端末は「0xD6 になった」ことだけを受け取り、**自分の g_MushroomGrowScale で**大きくして戻す。
- **結論**: 大きくなるのが他人から見えるのは、相手の端末が同じ状態を自分で再生しているから。**大きさの値は通信に乗らない**。
  自分の端末で表や +0x238 を変えても、相手には見えない（逆に、自分が見る全員のキノコの大きさが変わるだけ）。相手に見せられるのは「状態 0xD6 を送る」ことだけで、
  それは本来の 1.0 → 1.8 → 1.0（66 フレーム）そのまま。任意の大きさを相手に見せるには、相手側にも同じ改変が要る。
- 椅子（比較）: 座る状態 = 0xA9（始め PlayerState_ChairSitDown_Enter 0x67AE04 = chair_sitdownF1、毎フレーム 0x66D894）。どちらも引数ブロック +0xE（pkt+0xE）の座標を sub_75926C で解いて使う
  → 座る位置は通信に乗る。高さ（y）は 0x66D894 で表 unk_A0EB3C(171) の +20 を使っており、**高さ変更チートがどこを変えているかは未確認**（反映される経路は未特定）。
- IDB: PlayerModel_SetUniformScale・PlayerState_MushroomGrow_Enter/Calc/Exit・PlayerState_ApplyRemotePacket・PlayerState_ChairSitDown_Enter/Calc・g_PlayerStateTable・g_MushroomGrowScale、注記 7。
  道具: tools/patches/scan_field_offset.py（構造体の欄 +off を読み書きする命令の全数走査）。
- 反証条件: 相手の端末で自分の +0x238 を書き換えた値が見える、状態パケットに拡大率らしい float がある、0xD6 の始めが引数ブロックを読む。

