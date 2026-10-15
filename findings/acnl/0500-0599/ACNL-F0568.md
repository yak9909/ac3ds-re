---
id: ACNL-F0568
aliases:
- IDA-unknown-F014
- V2-F014
title: 準備中の日替わり処理に掲示板・雑草・住民の引っ越しがある（2026-09-17、MEDIUM＋実機傍証）
summary: 'Save_RunDayChange 0x114D18配下を静的に追跡。掲示板: Town_OnDayChange→Bbs_OnDayChangePworks 0x107F80（BBS_Pworks）、Town_OnDayChangeLate 0x103A18→Bbs_OnDayChangeEvents 0x107688（BBS_Event）。記事はBbs_BuildPost 0x302280→Bbs_AddPost 0x302300（TownBase+451128）。雑草: '
date: '2026-09-17'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1081216
- 1063448
- 1078920
- 3154560
- 3154688
- 1074172
- 1067860
- 1110188
- 5990492
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4276-4280
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F014: 準備中の日替わり処理に掲示板・雑草・住民の引っ越しがある（2026-09-17、MEDIUM＋実機傍証）

Save_RunDayChange 0x114D18配下を静的に追跡。掲示板: Town_OnDayChange→Bbs_OnDayChangePworks 0x107F80（BBS_Pworks）、Town_OnDayChangeLate 0x103A18→Bbs_OnDayChangeEvents 0x107688（BBS_Event）。記事はBbs_BuildPost 0x302280→Bbs_AddPost 0x302300（TownBase+451128）。雑草: Field_OnDayChangeGrowUp 0x1063FC→Field_GrowUp 0x104B54（GrowUpHeap）→Field_GrowUpSpawnWeed 0x115B00がword_85FA56={0x7C..0x7F}（IDS weed A-D一致）から乱数で空きマスへ、経過日数（最大30）×2本、条例[garden+0x621CF] bit4で10%×1本。住民: Town_OnDayChange→Villager_OnDayChange 0x10F0AC→Villager_DayChangeMoveInOut 0x5B685C（住民数で入居Villager_TryMoveIn／転出候補Villager_PickMoveOutCandidate→村+104290）。残件のsub_30C9C4（→Villager_DailyUpdateOnce）はTown_OnDayChangeLate→Villager_OnDayChangeLateから先に走る住民の日次処理（誕生日の手紙・在宅/外出・持ち物配置）。IDBに22関数命名。しずえスキップはこれらを飛ばす可能性。反証条件: 実機で準備中にこれらが走らない。根拠work/evidence/prepare_screen/README.md。
実機傍証（2026-09-17、利用者）: 同じ日替わり処理に属する寝癖・郵便ポストのメールがしずえスキップで飛ぶことを確認（IDA-unknown-F013）。掲示板・雑草・引っ越し判定なども同様に飛ぶ可能性が高いが、個別には未確認なので断定しない。

