---
id: ACNL-F0124
aliases:
- F-86
title: 'F-86: parent拒否説を撤回。`ScStage` と`BsMenuTab`はいずれもchild gateを通る'
summary: 'confidence: **HIGH**（`UiScreen_OpenChild` の静的条件と停止中実機byteの精密再読を照合）'
date: '2026-08-24'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9380992
- 9385744
- 5368920
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5141-5164
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-86: parent拒否説を撤回。`ScStage` と`BsMenuTab`はいずれもchild gateを通る

confidence: **HIGH**（`UiScreen_OpenChild` の静的条件と停止中実機byteの精密再読を照合）

初版adapterを停止中にstatus読出しした結果は次だった。

| field | value |
|---|---:|
| adapter state / saved parent | `2` / `0x32C851B8` |
| owned `BsFtrMgr` / preview status | `0` / `3`（create failed） |
| `g_BsFtrMgr` / `g_CatalogPreview+0` | `0` / `0` |
| `g_RoomSceneParent` | `0x3308638C` |

`g_RoomSceneParent` のvptr `0x8F2480` はRTTI `ScStage`、saved parentのvptr `0x8F3710` は
RTTI `BsMenuTab`。精密再読した実機byteは**両方とも** `+14=1 / +15=0` だった。
`UiScreen_OpenChild` (`0x51EC58`) は `!parent || parent[15] || parent[14]==2` なら0を返すため、
両parentはgateを通る。以前の `ScStage +14=0/+15=1` という記録とfactory前拒否の結論は誤り。

第2版はsaved `BsMenuTab` parentへ変更したが、ユーザー目視は3Dなしで、再読結果も
`owned=0/status=3/g_BsFtrMgr=0/actor=0` のままだった。従って失敗点はparent gateより後、
新規UiScreenのgeneric create phase内である。

---

