---
id: ACNL-F0422
aliases:
- IDA-gpt-6-F008
title: closet直通とnative転送・低ID/ウィジェット（2026-10-12）
summary: '最終DB監査: 0x4DD030/0x4DD4A4は原数量merge/predicateとして原ARMと実行検査から2rename追加。周辺9注記も追加し合計9name/26注記、未知のlookup全ABI/choice PMF・数量action/stack第5引数は理由と次の照合をDBへ記し推測renameしない。製品不変、根拠db_peripheral_changes.json・更新XML読戻し。'
date: '2026-10-12'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5099568
- 3286156
tags:
- storage
supersedes: []
source: IDA:work/FINDINGS.md:47-56
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F008: closet直通とnative転送・低ID/ウィジェット（2026-10-12）

- 最終DB監査: 0x4DD030/0x4DD4A4は原数量merge/predicateとして原ARMと実行検査から2rename追加。周辺9注記も追加し合計9name/26注記、未知のlookup全ABI/choice PMF・数量action/stack第5引数は理由と次の照合をDBへ記し推測renameしない。製品不変、根拠db_peripheral_changes.json・更新XML読戻し。

- IDA（idalib）/GPT-6、MEDIUM。利用者T010実機でcloset表示を確認、chat→Map/BsMenuTab入退場が余分と報告。普通chatはkeyboard Initでflag0x10を消し、ButtonsIn0x57CA00が0xC0を立てて親0x193850は0x80を待つ。通常menu-ready0x10をguardにすると普通chatを拒否する。既存GameListのBeginMenuClose/FinishMenuCloseをCancelより先に同期適用するとtabをnative待機0x6D4444へ置いてReturn/MapSyncを省ける。actorのCalc/Draw/Releaseは止めない。
- 原BsMenuChest WaitInputはDragControl+180/sourceと+260/target nodeの+200 UIindexを取り、2項目をローカルcopyしてstack/swap後に両側SetItem。検索providerへの書込みを無視すると取得しても項目は残る。pocket-source→storage-targetの戻し値は空とし、同sourceへcloneを返さず破棄する。pocket同士のswap/stackは元コード。検索側で通常保存closetを書き換えない。
- 低ID/非pocket品の消失はgetterとsetterで異なる。Inventory_GetSlot0x723878は0x7238C0分岐で空pointerを返す表示除外、Inventory_WriteSlotChecked0x32248C→Normalize0x6B9598は低ID変換/空化/不可判定を含む。PocketItem/F048のraw書込み/没表示と原ARMを照合。owned closet setterはraw4byte+flag0、owned nativeLoadStep/Calcのscopeのみgetterをraw化し、外部BEQ/NOP・他画面は元のまま。
- change.arc/cng_base原CLYTでB_btn_01/02はhitbox、N_btn_01/02が絵/文字/枠を所有し影P_btn_sh_01/02は兄弟。boundだけ非表示にしても絵が残る。親と影をCalc後も非表示にする。groupAのみbind・nativepageを保持。
- DB7rename/endpoint partial型+4prototype/17注記を保存、公式XML7新名/17注記/50旧名/全member/T/fullbytes/hash読戻しPASS、所有0。根拠gohan_closet_direct/{static,original_assembly,layout_input,db_xml_readback}.json、実装前設計closet_direct_design.md。原IDBにある過去のNOPは維持し原code.binで独立照合、新実機表示/タイミングは未確認。反証: normal chat readyに別のflagwriterがある、native転送がローカルcopy以外へ書く、原階層/アニメで親hideが反映しない場合。未知のIDやclass名は推測renameしない。

