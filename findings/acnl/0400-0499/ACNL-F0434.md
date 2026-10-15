---
id: ACNL-F0434
aliases:
- IDA-gpt-6.1-sol-F017
title: チップ長押しのstatic記録拒否と選択アニメ再開始（2026-10-10、MEDIUM）
summary: 解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。F016配布で利用者が「窓未表示/縞アニメ振動」を実機報告。修正版はPC検査のみ、実機未確認。日本語無印ACNL＋更新、main SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ModuleFtr.cro SHA d2a65c85909782a66a5300df7f26f76289db69f7474f563d59
date: '2026-10-10'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:164-173
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F017: チップ長押しのstatic記録拒否と選択アニメ再開始（2026-10-10、MEDIUM）

解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。F016配布で利用者が「窓未表示/縞アニメ振動」を実機報告。修正版はPC検査のみ、実機未確認。日本語無印ACNL＋更新、main SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ModuleFtr.cro SHA d2a65c85909782a66a5300df7f26f76289db69f7474f563d596c52f844423eca。

- FtrRec_Get 0xB1D244はCRO static `.bss` 表g_FurnitureRecords 0xB480D4から32B×112記録を返す。登録側0xB1CF44の+4 actor参照書込と原CRO/ELF/IDAの6地点を独立照合、原ARMで全112handleを検査。範囲外はrecord0へaliasする。F016のHeap(rec)は正規返値を拒否。handle[0,112)とread permission検査へ修正。
- Chip_Select_Calc 0xB429BCはcounter+1092==0でanim5/6のbind/reset/step/終了unbindを呼び、6以上でdrag、24移動でdrag。F016がcounterを毎frameゼロへ戻すため、原ARM＋旧ELFで18frameにreset10回/窓未開を再現。counter>5だけ5へ制限し、初回アニメ後の非ゼロ値を維持する。
- 新ELFは原状態表[0xB62778,0xB6282C)とSelect/取消/StateObj/NeutralEnter/親整理を実行し、18frame窓・A複製/B取消・PMF復帰・短release DecideRotate・24移動drag・無効handle拒否の7条件PASS。アニメ開始reset2回＋正規取消2回のみ。GPU/resource primitivesは明示モデル、実機描画の証明にしない。
- DBへ4関数の確定名、S0付きone-shot型、20B×9状態表、32B家具部分型/112件表/Get型、counter/recordメンバーのオペランド/根拠コメントを反映。保存再openと両最新XML/bytes/構文・参照/hash/型/Tを検査。
- 根拠work/evidence/chip_longpress_fix、設計docs/topics/chip_longpress_fix_design.md、gohan work/chip-longpress-fix。反証条件: 同新版で窓が開かない/震えが残る場合はactor-ready/heap空き/window Load/描画frame入力を実測。新追加の周辺機能を実機PASSへ一般化しない。

