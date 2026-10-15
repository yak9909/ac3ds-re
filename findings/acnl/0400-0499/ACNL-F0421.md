---
id: ACNL-F0421
aliases:
- IDA-gpt-6-F009
title: widget画像の参照寿命とcloset帰還・page待ち（2026-10-12）
summary: '2026-10-13追加: 原hand/touch controlは+216 counter/+220 threshold、初回11/連続3を確認。node112/152が決定アニメ。owned pageは待機を省いて親1C38A0を同Calcで完了。退場はchild outer996/pocket1988の終端→元unbind/状態移行→Actor_RequestDestroy。キーボタン解放をchat入場条件にせず、held入力だけ暫定遮断。NativeEngine::L'
date: '2026-10-12'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9354456
- 2857216
- 2857420
- 2857332
- 2520968
- 2718624
tags:
- storage
supersedes: []
source: IDA:work/FINDINGS.md:37-46
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F009: widget画像の参照寿命とcloset帰還・page待ち（2026-10-12）

- 2026-10-13追加: 原hand/touch controlは+216 counter/+220 threshold、初回11/連続3を確認。node112/152が決定アニメ。owned pageは待機を省いて親1C38A0を同Calcで完了。退場はchild outer996/pocket1988の終端→元unbind/状態移行→Actor_RequestDestroy。キーボタン解放をchat入場条件にせず、held入力だけ暫定遮断。NativeEngine::Loadのfailure2/stage1は5MiB確保失敗、メモリ破損との因果は未確定。normal名前file/matches容量を公開後、items/pending容量をactor破棄後に返す。追加9name/10注記をDBに保存、合計16name/21注記・876B型/3prototype。追加native試験はtiming_memory_runtime.json、実ヒープの断片化/実機変換復旧は未確認。

- IDA（idalib）/GPT-6、MEDIUM。原SetItemがmaterial TexMapへPAを保持するため、自前16枠LRUの再利用で他のlive widgetの画像も変わる。旧ELFでpage送りの上書きを再現、新32枠はwidget参照でpinしSetItem/dtor2種で解放、満杯ならnativeへ退避。GPU cache32KiB/借用0x1B000、atlas/spare整列・境界はPC検査。実GPU/新借用余裕は未確認。
- RTTI ItemDragIconNode0x8EBCD8、Ctor0x2B9900/dtor0x2B99CC/削除dtor0x2B9974・876B。両dtorは別bodyでLayoutとbaseを解放する。先頭PC相対LDRのR1を保持して次PUSHへMITMする。型AcnlItemDragIconNodeF009/3prototypeと7name・11注記をDBsave/close済み。未確認の構造体領域はunknownで残す。
- 原page関数0x267A50はrel4/5で1-based page循環→scroll0x267788。owned childは10項目0x297BA0/counter0x267660を即更新しidle0x267878を保持。親0x1C38A0はidle判定で入力復帰。foreignは先行LDR R2をforwardして原scroll経路。
- 旧closet終了はhold解放→GameList command2/map再入場→native tab6/chatだった。新版はholdのままmenu5を一度要求→実parent wait/ready0x80でGameListのfield復帰予約を解除しnativechat待機へ引継ぐ。通常chatを後で閉じると原の地図復帰へ。受理済み生成中の要求はtimeoutで放棄しない。
- 設計docs/topics/closet_followup_design.md、根拠work/evidence/gohan_closet_followup。新版実機成功は未確認、GPU/FS/actor schedulerはPC fixtureの明示endpoint。外部へHIGH昇格しない。

