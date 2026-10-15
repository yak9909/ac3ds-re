---
id: ACNL-F0423
aliases:
- IDA-gpt-6-F007
title: 普通チャットのキャンセル・実退場とタブ復帰（2026-10-12）
summary: IDA（idalib）/GPT-6、MEDIUM。更新SHA/load/ARM/T/元bytesを再照合。普通keyboard Cancelは決定index0→byte0x949D3B=0（self+4424が真）、self+4580=1、TextInput_PublishResult(1,1)。親0x193764→Out enter0x193988→child vt17/0x57B238→button-out/window-out。0x57CF04はアニメ完了後破棄要求、R
date: '2026-10-12'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9739579
- 1652580
- 1653128
- 5747256
- 9741908
- 1652944
- 7165200
- 7167920
- 7166648
- 7161676
- 8718348
tags:
- chat
supersedes: []
source: IDA:work/FINDINGS.md:57-63
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F007: 普通チャットのキャンセル・実退場とタブ復帰（2026-10-12）

- IDA（idalib）/GPT-6、MEDIUM。更新SHA/load/ARM/T/元bytesを再照合。普通keyboard Cancelは決定index0→byte0x949D3B=0（self+4424が真）、self+4580=1、TextInput_PublishResult(1,1)。親0x193764→Out enter0x193988→child vt17/0x57B238→button-out/window-out。0x57CF04はアニメ完了後破棄要求、Release0x57F944がlive0x94A654=0/flags0x08/0x10/0x20消去。親0x1938D0→Release0x193C3Cがmanager+492=0。native list detach/資源解放が必要で、pointerだけ外して完了とはしない。
- BsMenuTabは普通chat中state13/calc0x6D5510「チャット終了待ち」。キャンセルsignal0→Return0x6D5FB0→ChatTabsIn0x6D5AB8→map/tab復帰→TabSelect0x6D474C。結果通知だけではsignalを欠く。T009はchat/kbdを凍結しこの出口を止めたままFieldIdleを待ち、利用者実機で背景のみ/180frame timeout。前fixtureの初期TabIdleは実退場の証拠でない。
- 復帰はactualFieldIdle＋list空でtab index6→state9/calc0x6D6214をnative PMFで選択。次0x6D72C0がbyte table0x85080C[6]=5を用いてmenu5をrequest、初期化0x787004のruntime registry0x23F/factory/RTTI BsMenuChat ctorと照合。旧actorを保存・再利用しない。styleコマンドの直接ShowはT008どおり。
- DB13rename/24概念注記/result enum/prototypeを保存/close→所有0、公式XML出力・全bytes/hash検証PASS。独立根拠は既存normal_chat/menu資料・RTTI/state生tableと原ARM caller/stores。設計closet_exit_fix_design.md、根拠work/evidence/gohan_closet_exit_fix。PMF/アニメ/FS/actor schedulerのCPU endpointは明示、新版成功GPU/実機timing未確認。反証: normal chatで異なるsignal/parent/tab stateを実測、cancel後にもlist/FieldIdleが復帰しない場合。unknown shared signal値/別friend-chat役割を推測renameしない。

