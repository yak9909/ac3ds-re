---
id: ACNL-F0115
aliases:
- F-77
title: 'F-77: catalog表示後にstock「上タブをすべてアウト」を走らせる構成'
summary: 'confidence: **HIGH**（状態record・enter/update・遷移callを `code.bin.i64` で確認）、'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8718988
- 9484486
- 7170744
- 7168824
tags:
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:4912-4940
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-77: catalog表示後にstock「上タブをすべてアウト」を走らせる構成

confidence: **HIGH**（状態record・enter/update・遷移callを `code.bin.i64` で確認）、
**LOW**（新patchの実機結果は確認待ち）

状態record `0x850A8C` はname `0x90B8C6` =「上タブをすべてアウト」、enter
`sub_6D6B88`、update `sub_6D6A98`。enterはmanager `+0x19B2` の有効タブbitを
`+0x19B4` の退場maskへ全てコピーし、`sub_6D5DA8` で退場animationを開始する。
updateは毎frame `sub_6D6528` を呼び、animation終了時に各tab actor/button、有効bit、
退場maskをstock処理で片付ける。その後の `0x6D6AB8` は通常tab選択state
`sub_6D474C` へ遷移するcallである。

`PATCHES/cave_catalog_inventory_tabs_out.py` は、表示成功済みのlate hook `0x6D6338` で
catalog mode 0を要求した直後、lower-menu stateを `sub_6D6A98` へ変更する。
これによりstock enter `sub_6D6B88` とupdateの両方を使う。退場完了call `0x6D6AB8` は
private cave flagが1のときだけ `sub_6D7194`「メニュー終了まで待機」へ向け、flagを消費する。
flagが0なら元の遷移先を保つため、同じstock退場stateを使う他画面には影響しない。
catalog要求が拒否された場合は通常持ち物へfallbackする。復旧確認後、両hook・cave・flagを
読戻して設置し、breakpoint 0件を確認してContinueした。

実機ではplayer `0x16`、全タブ退場animationまでは動いたがcatalogは表示されず、直後に
player `0x06` とタブ再入場へ戻った。地図上に無反応な「閉じる」buttonだけが残り、通常Xも
開けなくなった。停止時はprivate flag=0（退場完了hookで消費済み）、
`g_MenuOpenState/Id/Arg=1/0x7C/0`、`vc_MENU_FLAGS=0x82` でbit `0x08`は立っていなかった。
要求直後にlower stateを退場へ変えたため、`Menu_PollOpen` が要求を画面へ変換する前に
通常「メニュー切り替え」updateを奪ったことが原因。両hook/caveはstockへ復元済み。

---

