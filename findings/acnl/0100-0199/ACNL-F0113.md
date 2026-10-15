---
id: ACNL-F0113
aliases:
- F-75
title: 'F-75: 「メニュー切り替え」enter入口なら持ち物UI初期化前に差替えられる'
summary: 'confidence: **HIGH**（状態記述子・関数入口・命令を `code.bin.i64` と実機で照合）、'
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8718588
- 8718688
- 9484439
- 8718692
- 7168684
- 8718700
- 7168096
- 7168824
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:4849-4882
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-75: 「メニュー切り替え」enter入口なら持ち物UI初期化前に差替えられる

confidence: **HIGH**（状態記述子・関数入口・命令を `code.bin.i64` と実機で照合）、
**LOW**（画面と終了挙動は実機確認待ち）

lower-menu状態記述子は `0x8508FC` から20バイト単位の
`[UTF-8 name, enter, 0, update, 0]`。対象recordは次の通り。

| addr | value | meaning |
|---|---:|---|
| `0x850960` | `0x90B897` | 「メニュー切り替え」 |
| `0x850964` | `0x6D62AC` | enter callback |
| `0x85096C` | `0x6D6060` | update callback |

旧hook `0x6D6338` は同じenter内だが、`vc_ACSYSTEM_DATA1`、button bit、UI animation開始後だった。
新しい `PATCHES/cave_catalog_inventory_switch_entry.py` は関数先頭
`0x6D62AC: E92D41F0` を `EA5EAC93 (B 0x01E81500)` に差し替える。
caveは `MOV R0,#0; B vc_CFUNCTION` の8バイト。hookもcaveからcatalogへの分岐も
non-linkingなので、state-machine callerのLRを保ったまま公式catalog関数から直接戻る。
これにより `sub_6D62AC` の持ち物用処理は一命令も実行しない。

本patchはテスト中、同enterを通る全lower-menu遷移をcatalogへ向ける一時版である。
install前にprocess SUSPENDED、breakpoint 0件、旧patch原状、cave全ゼロ、状態record、
catalog prologueを照合し、設置後hook/caveを読戻した。

実機ではcatalog表示に成功したが、持ち物/My Design UIは依然重なり、3Dも出なかった。
Bでcatalogを閉じるとplayer `0x16`、field controller state 5、下画面が残留した。
停止値は `g_MenuOpenState/Id=1/0x7C`、`vc_MENU_FLAGS=0x84`、player state `0x16`。
従ってタブ/UI生成は `sub_6D62AC` より前の「メニューイン」stateで完了している。
patchを撤去後、`sub_6D27E8()` とstock `sub_650F3C(player)` をone-shot実行した。
player移動は戻ったが地図は即時復帰せず、通常持ち物を一度開閉すると完全復帰した。

---

