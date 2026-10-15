---
id: ACNL-F0116
aliases:
- F-78
title: 'F-78: タブ退場開始条件は要求成功ではなく実画面のmenu flag `0x08`'
summary: 'confidence: **HIGH**（`sub_6D6060` / `Menu_PollOpen` を `code.bin.i64` で確認、'
date: '2026-08-24'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7147688
- 7168824
- 7168096
- 7168100
- 7170744
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:4941-4969
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0118"]
---
## F-78: タブ退場開始条件は要求成功ではなく実画面のmenu flag `0x08`

confidence: **HIGH**（`sub_6D6060` / `Menu_PollOpen` を `code.bin.i64` で確認、
失敗時globalを実機照合）、**LOW**（改訂版の実機結果は確認待ち）

「メニュー切り替え」update `sub_6D6060` は `vc_MENU_FLAGS & 8` が立つまで何も進めず、
立った後にlower-menuの開場animationや次stateを処理する。一般menu manager側の
`Menu_PollOpen` (`0x6D10A8`) は要求state 2を読み、fieldではmenu flag bit `0x04` が
準備された後に `UiScreen_OpenById` を呼ぶ。従ってcatalog要求直後のstate変更は早すぎる。

改訂した `PATCHES/cave_catalog_inventory_tabs_out.py` は3 hook構成とする。

1. `0x6D6338`: catalog要求成功時はprivate pending flagだけを立て、通常
   `sub_6D6060` updateを維持する。
2. `0x6D6060`: pendingかつ `vc_MENU_FLAGS & 8` のときだけstock全タブ退場stateへ変更する。
   条件未成立なら移設した元prologueを実行し `0x6D6064` へ戻る。
3. `0x6D6AB8`: 退場完了後、pendingを消費してstock「メニュー終了まで待機」へ接続する。

これならcatalogの実体生成を待ってからタブだけを隠し、閉じた後のstock復帰経路も維持できる
と予想し、残留buttonのstock復旧後に改訂版を設置した。

実機ではcatalog表示には成功したがタブは退場せず、3Dも出なかった。終了後はplayer `0x16`、
地図なし・下画面操作不能となった。停止時private pendingは`1`のままで、退場完了hookは未到達。
`g_MenuOpenState/Id=1/0x7C`、終了後flags=`0x84`。catalogを生成するとlower-menu update
`sub_6D6060` 自体が停止するため、同関数入口では表示中bit `0x08`を後から観測できない。
3 hook/caveはstockへ復元し、manager/player復旧one-shotを実行中。

---

