---
id: ACNL-F0109
aliases:
- F-71
title: 'F-71: 通常Xの実入口は `sub_6D62AC` の動的menuId呼出し `0x6D6338`'
summary: 'confidence: **HIGH**（`code.bin.i64` の制御フローと実機breakpoint・引数・LRを照合）'
date: '2026-08-24'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7168824
- 1498816
- 7148336
- 7168828
- 7168684
- 7168844
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4704-4736
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-71: 通常Xの実入口は `sub_6D62AC` の動的menuId呼出し `0x6D6338`

confidence: **HIGH**（`code.bin.i64` の制御フローと実機breakpoint・引数・LRを照合）

最初に候補とした `sub_16DDA8` → `sub_5C1E40` の `0x16DEC0` は、通常Xで到達しなかった。
フック設置中でも通常の持ち物欄が開いたため、この仮説を棄却し同パッチを完全復元した。

`Menu_RequestOpen` (`0x6D1330`) に一度だけsoftware breakpointを置き、屋外でXを押した実測値は
`R0=0`, `R1=1`, `LR=0x6D633C`, `PC=0x6D1330`。呼出し命令は `sub_6D62AC`
(`0x6D62AC`) 内の `0x6D6338` と確定した。ここでは次の動的表引きを行う。

```c
index = *(s8 *)(a1 + 6427);          // 実測 0
menuId = byte_85080C[index];         // table[0] = 0
Menu_RequestOpen(menuId, 1);         // 0x6D6338
sub_693EE8(dword_949718, index);      // 持ち物UI G_base_01の準備
```

修正版は `0x6D6338=EBFFEBFC` を `EB5EAC70` (`BL 0x01E81500`) へ差し替える。
ケーブはmenuId 0だけ `vc_CFUNCTION(0)` を呼び、持ち物専用 `sub_693EE8` を飛ばして
共通後処理 `0x6D634C` へ戻る。menuIdが非0なら、R0/R1を変えず元の
`Menu_RequestOpen` へtail-callするため他メニューを維持する。

ケーブは28バイト、予約は `0x01E81500-0x01E815FF`。hookは関数呼出し位置なので
`B` ではなく `BL` が必須。設置時に旧設定由来の `B` を読戻しで検出し、未実行のまま解除後、
`BL` へ修正した。最終読戻しはhook `70ac5eeb`、cave
`000050e30300001a10402de9aa41a1eb1040bde88c53a1ea843fa1ea` で一致した。

実機ではこの版でカタログ画面そのものは開いた。ただしF-72の通り、ここは通常持ち物UIと
プレイヤー状態`0x16`の準備後なので、完成した差替え位置としては棄却した。patchは完全復元済み。

---

