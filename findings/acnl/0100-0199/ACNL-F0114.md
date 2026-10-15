---
id: ACNL-F0114
aliases:
- F-76
title: 'F-76: stock「メニュー終了まで待機」はcatalog終了の橋渡し候補'
summary: 'confidence: **HIGH**（状態recordとupdate処理を `code.bin.i64` で確認）、'
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8719068
- 9484562
- 7173032
- 7163060
tags:
- menu
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:4883-4911
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-76: stock「メニュー終了まで待機」はcatalog終了の橋渡し候補

confidence: **HIGH**（状態recordとupdate処理を `code.bin.i64` で確認）、
**HIGH**（入口から直接接続する案が不成立であることを実機確認）

状態record `0x850ADC` はname `0x90B912` =「メニュー終了まで待機」、
enter `0x6D73A8` はnull、updateは `sub_6D7194`。updateは
`vc_MENU_FLAGS & 8` が立っている間は待機し、消えると次を行う。

```c
sub_693EE8(dword_949718, 10);        // lower-menu index 10 = none
*(u16 *)(manager + 6576) |= 1;
State_Change(manager + 20, sub_6D6F60, 0);
```

新しい `PATCHES/cave_catalog_inventory_wait_state.py` は一段前の「メニューイン」enter
`sub_6D4CB4` を入口で置換する。この位置はタブenable/animationより前。公式catalog要求が
成功した場合はmenu flag `0x08` を先に立てて早期退出を防ぎ、embedded state machineを
`sub_6D7194` へ直接遷移させる。hookは `0x6D4CB4: E92D4010 -> EA5EB211`、
caveは68バイト。catalog終了後のbit 8 clearからstockのindex 10復帰経路へ合流する狙い。

実機ではplayer state `0x16` になったがcatalogも持ち物も表示されず、閉じることもできない
操作不能状態になった。停止時はcatalog要求 `state/id=2/0x7C` と強制したmenu flag `0x08` が
残っていた。したがって「メニューイン」から終了待機へ直接飛ぶと、要求を消費する
「メニュー切り替え」までの通常state列も飛ばしてしまう。強制bit `0x08` は未消費要求を
永久待機させるだけだった。本patchは撤去し、`0x6D4CB4` とcaveを読戻し済み。

---

