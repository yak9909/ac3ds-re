---
id: ACNL-F0418
aliases:
- IDA-gpt-6-F012
title: UI入口・pocket再入場・非drag trash・青選択（2026-10-13）
summary: GPT-6/idalib、MEDIUM（原JPN ARM＋caller/vtable/source、PC/実機訂正）。通常ActivateSelectedにcheckboxlist入口が無い。既存inline編集/描画へ分岐を追加。manual closet3cheat/Wire/configを削除、chat検索closetは保持。
date: '2026-10-13'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9350072
tags:
- inventory
supersedes: []
source: IDA:work/FINDINGS.md:16-23
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F012: UI入口・pocket再入場・非drag trash・青選択（2026-10-13）

- GPT-6/idalib、MEDIUM（原JPN ARM＋caller/vtable/source、PC/実機訂正）。通常ActivateSelectedにcheckboxlist入口が無い。既存inline編集/描画へ分岐を追加。manual closet3cheat/Wire/configを削除、chat検索closetは保持。
- 背景priorityはnativeBuildが0x83を設定。trash6を0x84へ。AppendIconGroupはgroupからnodeを移すため、短い再入場でgroupへ戻す必要がある。Disposeはletter/control破棄前の解除地点、managerから外れていてもthisは生存。資源失敗でもONを維持して再試行する。
- 真のDragIconControl vtable0x8EABB8/vt+16=0x29A22Cはgroup+317でdrag開始、+318でクリック、+319で受け取り。私有trashだけ+317=0。node+264は任意のdrop-hit Paneであり旧generic SetModeをSetDropHitPaneへ訂正、新F012型とprototypeに反映。旧F010型は来歴を保持。
- F011のSetTouch(+32/+72)色保持を訂正。青はnativeSetSelectVisualと同じdecide終端(+112/+152)。native旧行SetSelect(0)は+72だけ戻すため、取得後の保持色を移動前に4anim解除する私有vt16と、touch/scroll物理row追跡を使う。
- 根拠work/evidence/gohan_inventory_ui_fix、設計docs/topics/inventory_ui_fix_design.md。DB15rename/21注記、新group320/node304型・3prototype保存/close。旧closet fixtureの29BAB4置換を解除し、真のclick後片付け/通常itemdrop/消去音まで53caseで確認した。公式XML/hash/保存結果はSESSIONを正とする。静的/PCでGPU色・draw・実機heapタイミングをHIGHへ昇格しない。

