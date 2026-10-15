---
id: ACNL-F0399
aliases:
- F-372@v1:RE/FINDINGS.md:24106
title: 'F-372（2026-09-08）: E1—素では落ちない。チートON状態に絞られた'
summary: 再起動直後（チートOFF）でタイトル→しずえ遷移。実機値：
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1273956
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24106-24116
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-372（2026-09-08）: E1—素では落ちない。チートON状態に絞られた

再起動直後（チートOFF）でタイトル→しずえ遷移。実機値：
停止中・PC=`0x00137064`（通常の待ち位置）・3 語とも素
（SH=`E92D4070`・A1/A2=`E92D4010`）・部屋 `0x63`・R4 正常。
遷移自体は素で完走する。素の遷移バグの線は消えた。

残る軸： (1) フック存在自体、(2) チートON状態の他要素。
次はチートON＋項目OFF（フック有り・発火なし）で同遷移。
落ちればフック抜きビルドで (1)/(2) を分ける。

