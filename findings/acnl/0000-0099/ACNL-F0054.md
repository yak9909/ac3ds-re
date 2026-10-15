---
id: ACNL-F0054
aliases:
- F-16
title: F-16 v1 の 3x3 ケーブがクラッシュした原因 — バグの存在は `HIGH` / 因果は `MEDIUM`
summary: '**原因A（コード上は確定）**: テールジャンプ前に R0-R3 を復元していなかった。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6697836
- 6698024
- 6697932
- 6697936
- 6698064
- 6696552
- 6619136
- 6815744
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:955-987
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-16 v1 の 3x3 ケーブがクラッシュした原因 — バグの存在は `HIGH` / 因果は `MEDIUM`

**原因A（コード上は確定）**: テールジャンプ前に R0-R3 を復元していなかった。

v1 は
```
POP {R4-R11,LR}
B   Player_StartFieldAction
```
で中心マスへテールジャンプするが、`POP` は R0-R3 を復元しない。
到達時点で R0 は直前の `BL sub_5A16B0` の戻り値、R1-R3 はループの残骸である。
`Player_StartFieldAction` は a2/a3/a4 をアイテムポインタとして
`Item_Copy(v12, a2)` で参照するため、不正アドレス読み出しになる。

v1 は R0-R3 を R4-R7 へ退避していたが、その R4-R7 も `POP` で
PUSH 時の値に戻ってしまうため、退避は無意味だった。

**原因B（可能性、未確定）**: ケーブ範囲の取りすぎ。
v1 は `0x66336C` から 188 バイト(47命令)を書き `0x663428` まで潰していた。
死にコードと確認できるのは `0x66336C`-`0x6633CC` (96B) までで、
`0x6633D0`-`0x663450` は `Shovel_DecideState` (`0x662E68`-`0x663450`) の一部
（`Actor_PlayAnim` 呼び出しを含む）。
ただし `0x6633D0` への分岐は `0x650000`-`0x680000` の 192KB 走査で **0 件**
だったため、到達不能で無害だった可能性もある。

**訂正**: v1 のコメントが挙げていた「疑わしい点」4 件
（a8/a9/a10 を 0 で渡した、mapmgr の取得方法、呼び出し前提、処理順序）は
いずれも主因ではないと考えられる。`FieldObj_ApplyDigRecord` は
a10 == NULL を明示的に処理しており、a8 は自プレイヤー番号なので
シングルプレイなら 0 で正しい。

---

