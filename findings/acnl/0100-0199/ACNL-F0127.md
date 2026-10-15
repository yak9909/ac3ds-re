---
id: ACNL-F0127
aliases:
- F-89
title: 'F-89: 2回目の同一SIGSEGVはmanager phase 3の屋外map走査。Catalog選択品とは別'
summary: 'confidence: **HIGH**（2回目のstack、Item request、phase 3逆アセンブル、命令stepを照合）'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6879024
- 6877632
- 6879020
- 6878456
- 6879432
tags:
- catalog
- map
supersedes: []
source: v1:RE/FINDINGS.md:5219-5244
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-89: 2回目の同一SIGSEGVはmanager phase 3の屋外map走査。Catalog選択品とは別

confidence: **HIGH**（2回目のstack、Item request、phase 3逆アセンブル、命令stepを照合）

第4版で1回目を回収して再開すると、再びthread 220が `PC=0xE1A04000` で停止した。ただし
生成actorは同じheap番地 `0x30C51C70`を再利用した新規objectで、actor識別値は
`0x17D8 -> 0x17D9`。stack深部のreturnは `0x68F730`であり、今回は
`BsFtrMgr_PopulateRoom` (`0x68F1C0`) 内の `sub_57ADFC` (`0x68F72C`) からだった。

phase 3はcommon transition/modelの初期化後、`Field_GetMapManager` (`0x68F4F8`)を取得し、field mapの
全座標を走査して配置Itemを家具actorへ変換する。例外時requestのItemはstack上 `0x2090`で、Catalogの
cached Itemは引き続き `0x2EA3`だった。従って2回目は「0のランプ」のpreview生成ではなく、stockでは
屋外に存在しない `BsFtrMgr` がfield配置物まで室内家具としてpopulateした結果である。

第5版は `0x68F4F8` をguard付きwrapperへ接続する。adapter state 2、かつ
`CAVE_FTR_MANAGER == [SP+0x60]`（現在phase 3のsaved arg0）の時だけ0を返し、それ以外は
本物の `Field_GetMapManager`へtail branchする。これによりcommon初期化とphase 3末尾の時刻設定は
維持し、屋外map走査だけを省く。stock室内managerには作用しない。

進行中の2回目は既にmap取得後だったため、失敗actorを基底vtableでstock破棄し、唯一のstack return
`0x68F730`を走査後 `0x68F8C8`へ変更した。single-step / step-until-returnで破棄完了、到達PC
`0x68F8C8`、phase 3 return 1、`UiScreen_CreatePhases`によるmanager flag `1 -> 3`を順に確認した。
第5版hook `0x68F4F8=0xEB5FC8B5` とcaveは読戻し一致後に再開した。

---

