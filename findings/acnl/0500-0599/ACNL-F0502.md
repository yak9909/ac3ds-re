---
id: ACNL-F0502
aliases:
- IDA-opus-5.5-F029
title: 髪は毎フレームの部品更新が pm+548 から読む。複製は本物のプロフィールで作り pm+548/+552 を書くだけでよい（F028 の一部訂正）（2026-09-24、MEDIUM（静的。複製での実機確認は未実施））
summary: '`PlayerModel_UpdateParts 0x1D0AEC`（旧 vc_UPDATETANOFFSET）: 各バンクの枠の部品と望む値を比べ、違えば入れ替え式で読み直す。頭の望む値は'
date: '2026-09-24'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1903340
- 3316116
- 2563536
- 6856156
- 6634196
- 1894616
- 1913852
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2279-2287
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F029: 髪は毎フレームの部品更新が pm+548 から読む。複製は本物のプロフィールで作り pm+548/+552 を書くだけでよい（F028 の一部訂正）（2026-09-24、MEDIUM（静的。複製での実機確認は未実施））

- `PlayerModel_UpdateParts 0x1D0AEC`（旧 vc_UPDATETANOFFSET）: 各バンクの枠の部品と望む値を比べ、違えば入れ替え式で読み直す。頭の望む値は
  `PlayerHeadKey_Build 0x329994(key, pm+548, 帽子 Item, 日焼け色)`。ファイル名 `PlayerHeadBank_BuildPath 0x271DD0` = `Player/head_mdl/{boy|girl}{髪型%17:02}{a|b}.bcres`。
- 本物の `vc_UPDATE 0x689DDC` も pm+548 を書いてから作り直しの印を立てるだけ（F-68 の即時髪型変更と整合）。
- よって F028 の「プロフィールを写して渡す」は髪型・髪色には不要。性別・目の形は作成時の引数と顔のバンクに関わるので別途。
- 毎フレーム: `AcPlayer_UpdateModel 0x653AD4` = sub_1D2BE8 → `PlayerModel_CalcAnim 0x1CE8D8(pm,1,1)` → vtbl[4] 0x1D33FC。描画への登録経路は未確認。
- 反証条件: 複製の pm+548 を書いても頭が替わらない（部品更新が別の値を見ている）。

