---
id: ACNL-F0110
aliases:
- F-72
title: 'F-72: `0x6D6338` はカタログ起動確認点として正しいが、持ち物全体の置換点としては遅すぎる'
summary: 'confidence: **HIGH**（実機画面結果、実行時オブジェクト、`code.bin.i64` のstock初期化/終了経路を照合）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7168824
tags:
- inventory
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:4737-4767
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-72: `0x6D6338` はカタログ起動確認点として正しいが、持ち物全体の置換点としては遅すぎる

confidence: **HIGH**（実機画面結果、実行時オブジェクト、`code.bin.i64` のstock初期化/終了経路を照合）

`sub_6D62AC` は状態名「メニュー切り替え」のenter処理である。`0x6D6338` より前に既に
`mvmnt_undscrn` のパネル設定、ボタン側bit、アニメーションを持ち物用へ切り替えている。
その後の `sub_693EE8` だけを飛ばして `vc_CFUNCTION(0)` を呼んでも、持ち物UIの所有権と
プレイヤーの窓開き状態は消えない。

実機結果は次の通り。

- mode 0カタログ画面は開く。
- 持ち物/マイデザイン等の下画面UIが重なり、ボタンは反応せずX/Bでも閉じない。
- 全カテゴリで3Dアイテム表示が出ない。
- 「やめる」でカタログだけ閉じ、プレイヤーは状態`0x16`、下画面は空の持ち物背景に残る。
- `player+0x1A9 = 0x06` で移動だけは戻るが、下画面は戻らない。

`sub_693EE8(dword_949718,0)` のone-shot後、`BsMenuBg` の埋込みstate callbackは
`nullsub_2169`、`+1553/+1554=0/0` だった。一方、`g_MenuOpenState/g_MenuOpenId` は
`1/0x7C` のまま。従って残留の本体は背景アニメではなく上位 `BsMenuMgr` の所有状態である。

stock wrapper `sub_6D27E8()` は `off_949D4C` に対して `sub_6D2910` を呼び、
`BsMenuMgr+472` のボタン画面を `sub_1A0DD4`、`+476` の背景を `sub_694124` で戻し、
menu IDを非表示値`0x8C`へ初期化する。実機でこのone-shot後に地図復帰と通常X持ち物開閉を確認した。

次版は `0x6D6338` のcall差替えを再利用しない。X入力から「メニュー切り替え」状態へ入る前を捕捉し、
持ち物UIと状態`0x16`を開始させずにcatalogを要求する必要がある。終了時もcatalog ID `0x7C` の
完了をfield側へ橋渡しするstock相当の後処理が必要である。

---

