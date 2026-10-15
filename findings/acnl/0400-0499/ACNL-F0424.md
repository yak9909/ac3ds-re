---
id: ACNL-F0424
aliases:
- IDA-gpt-6-F006
title: nativeクローゼットとmenu intrusive node（2026-10-12）
summary: IDA（idalib）/GPT-6、MEDIUM。更新SHA c635af8f.../ARM11/ARM32LE/imagebase0/主要10地点T=0を確認。原code.binのARMとRTTI/生table/ctor/索引consumerを独立照合。BsMenuChestは38708B、actualprimary0x8E5BB0（旧Explorer0x8E5BA8はheader）/25method。通常child ChangeStockItemは15528B、prima
date: '2026-10-12'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9329584
- 9349940
- 9987328
tags:
- menu
supersedes: []
source: IDA:work/FINDINGS.md:64-70
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F006: nativeクローゼットとmenu intrusive node（2026-10-12）

- IDA（idalib）/GPT-6、MEDIUM。更新SHA c635af8f.../ARM11/ARM32LE/imagebase0/主要10地点T=0を確認。原code.binのARMとRTTI/生table/ctor/索引consumerを独立照合。BsMenuChestは38708B、actualprimary0x8E5BB0（旧Explorer0x8E5BA8はheader）/25method。通常child ChangeStockItemは15528B、primary0x8EAB34/17method、1page10slot、pocket16/control6/itembase22。Warehouse137の別childとは混ぜない。
- 保存closetの式はbase+4*(slot+10*(page0+6*tab))、getter/setterと76E680/6CC194の独立ARMが一致。pageByTabは1based、pageCountは独立で既定6、page stepはこれを使い循環。native転送はMainWaitInput→native item swap/stack→SetItemAtUiIndexで、pocketは実Save+27600へ直書き。私有検索providerへredirectすれば元closetを上書きせずnative操作を借りられる。occupied pocketは元のdisabledで預入を防ぎ、空き枠への取得を保持する。
- 0x986500/986504はactorでなくlist head/tail node、node+12がactor、embedded node=actor+20。Contains/Remove/PushBack・prepare/release・PollOpenのparent選択で確定。0x6D102CはAttach、0x6D1B34はDetachで、従来名は逆（F003の保留を解決）。DBへ37rename/既知prototypes/5型・member/concept commentを反映/save/close→所有0、公式XML出力/全bytes/hashvalidation PASS。
- 解析/設計: docs/topics/closet_search_design.md。根拠: work/evidence/gohan_closet_search/{static_initial,original_assembly,native_prerequisites,static_ownership,db_changes_initial,db_readback_types}.json。新製品とCPU試験は同folder、成功GPU/FS/実機timingは未確認。実機でpage/tab/転送/復帰が異なる場合は修正し、HIGHへ昇格しない。LOWのmanager内部条件は推測renameしない。

