---
id: ACNL-F0574
aliases:
- IDA-unknown-F011
- V2-F011
title: サイズqueryとOOM・ready・owner寿命（2026-09-17、MEDIUM）
summary: 元命令を原本codeと照合し、ARM11MPCoreでquery経路のみ実行。独立allocation ledgerと23 Season×mask0/0x10の46ケース一致。932/1664 bytes・最大alignment32はbuilder見積もりで、heap管理・size+align・資源/GPUメモリを除く。OOM時は0x4AB4A0でnull vtable参照、Setup結果も伝播されず事後検査だけでは安全でない。fgobj::ProcはSetup完了前にglo
date: '2026-09-17'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4307-4310
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0557"]
---
## IDA-unknown-F011: サイズqueryとOOM・ready・owner寿命（2026-09-17、MEDIUM）

元命令を原本codeと照合し、ARM11MPCoreでquery経路のみ実行。独立allocation ledgerと23 Season×mask0/0x10の46ケース一致。932/1664 bytes・最大alignment32はbuilder見積もりで、heap管理・size+align・資源/GPUメモリを除く。OOM時は0x4AB4A0でnull vtable参照、Setup結果も伝播されず事後検査だけでは安全でない。fgobj::ProcはSetup完了前にglobalを公開し、Destroyはstock instance→globalクリア→資源/heap解放。nonnullやpointer pollingだけをready/寿命保証にしない。CPU解放順をGPU retirementの証明にしない。根拠tree_contract.jsonと静的根拠、verify_tree_contract.py。実機適用・表示試験なし。

