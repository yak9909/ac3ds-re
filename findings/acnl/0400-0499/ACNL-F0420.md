---
id: ACNL-F0420
aliases:
- IDA-gpt-6-F010
title: list再tap・drag倍率・pocket操作（2026-10-13）
summary: IDA（idalib）/GPT-6、MEDIUM。selectedrowをnative待機が毎回node217=0へして再tapを禁止する。owned行だけ戻し、別touchfocusを持つと初tap選択/再tap実行になる。A/再tapはnativeStartDecideで音と2anim。scroll pressのknob/trackは別経路、dragだけ初期localpointから0.5倍へ変換すると原8→4、track9→9。指を止めても動かない。原ARM＋native
date: '2026-10-13'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags:
- inventory
supersedes: []
source: IDA:work/FINDINGS.md:30-36
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F010: list再tap・drag倍率・pocket操作（2026-10-13）

- IDA（idalib）/GPT-6、MEDIUM。selectedrowをnative待機が毎回node217=0へして再tapを禁止する。owned行だけ戻し、別touchfocusを持つと初tap選択/再tap実行になる。A/再tapはnativeStartDecideで音と2anim。scroll pressのknob/trackは別経路、dragだけ初期localpointから0.5倍へ変換すると原8→4、track9→9。指を止めても動かない。原ARM＋native fixture/既存入力経路を照合、実機未確認。
- native option descriptor32B/row172B/system prefix220B、6行capacity。builder scope内でhelperを拡張すれば既存行・cancel・wall action42を保てる。Bells category2、bank6B8C/loan6B94/pocket6BD0/storage92F0は財布回収/ATM返済/郵便利息/native storageとVapecord構造を独立照合。raw複製は空きのみ、返済はnative暗号化/チェックサム/貯金上限を検査。
- Native PartsDragIconNode304B/DragIconGroup320Bをprivate trashへ利用。group nodesはcontrol main listへ移り、group+12がcontrol+228 registryへ。native cleanupには登録済みgroup292/layout28が必要。手紙button19とattach対象17は別。BBox origin差はnative矩形/affine中心で合わせる。native全削除窓は既存InteriorChoiceをlabel引数化し共用。
- closet DPadは実時間200msからrepeat、1500ms加速で50ms。39operation・half6・exit/memory7と旧list20/repeat12/style6、68原ARM/19CPP/4334parser、全linked/ABI/hash PASS。DB24name/35注記/10型・公式XMLへ反映。source/設計/反証条件はdocs/topics/inventory_controls_design.md、根拠work/evidence/gohan_inventory_controls。UIのGPU/音/実機timingは未確認。XML表注記のitem-head補正とGit結果はSESSION参照。

