---
id: ACNL-F0565
aliases:
- IDA-unknown-F017
- V2-F017
title: 郵便ポストの手紙は「通信相手から」を判定できる／sub_6070CC・sub_606964 はデバッグ判定（2026-09-18、MEDIUM）
summary: sub_6070CC/sub_606964（SaveIo_DbgIsWholeIo89A60/89B00）はセーブ入出力中のオフセット0・サイズ0x89A60/0x89B00を返すだけで、Save_GetTownBase等27/15か所で戻り値は使われない（アサート残骸、影響なし）。手紙640Bは Mailbox_WriteLetter 0x6F4454 のコピー区切りから +0x00 宛先PersonalID(0x2E)+種別+0x30、+0x34 差出人PersonalI
date: '2026-09-18'
category: network
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7291988
- 6074460
- 1815748
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4264-4267
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F017: 郵便ポストの手紙は「通信相手から」を判定できる／sub_6070CC・sub_606964 はデバッグ判定（2026-09-18、MEDIUM）

sub_6070CC/sub_606964（SaveIo_DbgIsWholeIo89A60/89B00）はセーブ入出力中のオフセット0・サイズ0x89A60/0x89B00を返すだけで、Save_GetTownBase等27/15か所で戻り値は使われない（アサート残骸、影響なし）。手紙640Bは Mailbox_WriteLetter 0x6F4454 のコピー区切りから +0x00 宛先PersonalID(0x2E)+種別+0x30、+0x34 差出人PersonalID+種別+0x64、+0x68 ヘッダ、+0xAA 本文、+0x22C 署名、+0x274 アイテム。PersonalID は +0 プレイヤーID・+2 名前・+22 町ID・+24 町名（Letter_IsForOtherTown が [garden+401848] と比較）。Letter_InitFromCurrentPlayer 0x5CB05C はプレイヤーが書く手紙の差出人に自分の PersonalID と種別1を入れる。郵便ポストは D_GARDEN+0x73958+0x1B88*i（コードと Vapecord 一致）、書くのは Mailbox_WriteLetter（呼び出し元 Mail_DeliverToMailboxNow / Mail_DeliverFromPool）と Mailbox_DeliverFutureLetter だけ。ゲストが郵便局で出す手紙は Net_SendPacket(74) → ホストの NetPkt74_StoreGuestLetter 0x1BB4C4（off_875B4C[74]）が640Bのまま預かりへ → Mail_DeliverFromPool で配達。よって「差出人種別がプレイヤー かつ 差出人の町≠自分の町」で通信相手の手紙を判別でき、Mailbox_WriteLetter の入口が止める候補。LOW: 種別3/4/6の意味、他の通信経路の有無。反証条件: 実機でゲストの手紙の +0x34/+0x64 がゲストの ID・1 でない。根拠 work/evidence/mail_sender/README.md。

