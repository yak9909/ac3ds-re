---
id: ACNL-F0404
aliases:
- F-377
title: 'F-377（2026-09-08）: クラッシュダンプ解読＋対象走行中'
summary: 利用者が `Plugin/crash_dump_00000003.dmp` (604 B) を配置。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 9892668
- 1270920
- 5555256
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24220-24250
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-377（2026-09-08）: クラッシュダンプ解読＋対象走行中

利用者が `Plugin/crash_dump_00000003.dmp` (604 B) を配置。
magic `DEADC0DE`/`DEADCAFE`・例外種別 3（データアボート）。

### デコード（全項目がライブ読みと一致）

R0=1 / R1=0 / R2=`0xFFFFFFFF` / R3=`0x070A26B8` / R4=0 /
R5=`0x32939CC4` / R6=`0x0096F33C` / R7=`0x0FFFFEF8` /
R8=`0x30000000` / R9=2 / R10=0 / R11=0 / R12=`0xFFFFFFFF` /
SP=`0x0FFFFE98` / LR=`0x00136488` / PC=`0x0054C438` /
CPSR=`0x10` / DFSR=5 / IFSR=0 / **FAR=`0x148`**。

**DFSR=5（Translation fault）＋FAR=`0x148`** により、
`LDR R0,[R4,#0x148]`（R4=0）のフォールトで確定。
PC の報告ずれ説は捨てる。

### ボタン不通の読み

入力遮断フックは入っていない（2 語とも素を確認済み）。
それでもゲームボタンが効かずタッチだけ効くなら、
ゲームメインスレッドが wedge 状態で、タッチは別経路という構図。
タッチで何を操作したかは要確認。

### 対象の状態変化

読み出し中に state が -1 → 0（走行中）へ変わり、
レジスタ読みが効かなくなった。再起動・再開のどちらかは不明。
次は起動直後からの wedge 検査（ON 後・無操作で PC を 3 点読む）で
Enable 起因と遷移起因を分ける。

