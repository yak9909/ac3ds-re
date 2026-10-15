---
id: ACNL-F0629
aliases:
- IDA-opus-5.5-F109
title: 'T022 の窓が開かないのは読み込みのヒープ不足（2026-10-08、HIGH: 実機の値＋静的）'
summary: 'decor_catalog2 の実機（ida-pro-mcp、停止中に s_win_state ← Loading を書いて観測）: 窓の arc は読めている（s_catFile あり、517,032 B）。OpenWindow のレイアウト 3 つ・アニメ 9 つ・格子のペイン 45 は全部できていて、'
date: '2026-10-08'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9894976
- 5492212
- 1798688
- 5666504
- 1186184
- 9892612
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:4954-4967
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F109: T022 の窓が開かないのは読み込みのヒープ不足（2026-10-08、HIGH: 実機の値＋静的）

- decor_catalog2 の実機（ida-pro-mcp、停止中に s_win_state ← Loading を書いて観測）: 窓の arc は読めている（s_catFile あり、517,032 B）。OpenWindow のレイアウト 3 つ・アニメ 9 つ・格子のペイン 45 は全部できていて、
  アイコンの枠 45 × 4,096 = 184,320 B の HeapAlloc だけが失敗（FreeWindow の入口で s_iconSlots == 0）。読み込みのヒープ（[[0x96FC40]+4]、sead::ExpHeap 0x32C45F78、全体 3,866,624 B）の空き（自由リストを歩いた。ブロック 1 個）:
  模様替えの上段タブだけのとき 1,258,052 B → 窓を組んだ後 52,144 B（窓で約 1.2 MB）。
- 失敗すると Stage::Failed → 片付け → Tick が s_enabled を立て直す → 上段タブを作り直す。利用者の見た「タブが一度引っ込んで同じタブがすぐ出る」はこれ（ゲームのボタンが反応したのではない）。
- 順序（BP 3 点、同じ boot）: 入力の更新 0x53CDF4 → エディターの Neutral calc → gohan のフレームフック 0x1B7220。
- テクスチャの置き場（静的、ssys_LoadBclimToVram 0x5676C8）: 置き場の指定が既定（0x2010000 & ~0x3000000 = 0x10000 = FCRAM）なら arc の中のテクスチャをその場で GPU に読ませる → arc はゲームの（線形の）ヒープに置く必要がある。VRAM 指定なら GxQueue_AddRequestDma で VRAM へ写す。ArcResourceAccessorVRAM がどちらを渡すかは未確認。
- 次: 内訳（arc / レイアウト / アニメ）を s_heapLog で測る（decor_catalog3）。削る候補はコマンドの器（未実測の大きめ）、窓用 arc の分割（家具 / 壁紙で別）、アニメの数。
- 追記（F109、2026-10-08、decor_catalog3 の実機、ida-pro-mcp）: s_heapLog = 組む前 1,257,444 / arc を写した後 728,252（arc 517,032 B で 529,192 減）/ レイアウト 3 つの後 52,776（675,476 減）/ アニメ 9 つの後 51,504 / 返した後 1,257,444（漏れなし）。
  レイアウトのコマンドの器は別のヒープ（CmdlistStorage 0x121988 → 0x96F304 の割り当て係 sub_6165A8、0x10000 → a1[5] = 0x3228A7C8）なので、読み込みのヒープを食っているのはペインと材質そのもの。
  格子の bclyt はマス 45 × ピクチャ 5（P_Type / P_Empty / P_Tum / P_Type_01 / P_New）。P_Empty・P_Type_01 は資源で非表示で HHD のコードに名前が無い（v1.1 code.bin を検索）、P_New は移植で出さない方針 → make_catalog_arc の CELL_DROP で省いた（ペイン 379 → 244、材質 228 → 93、arc 517,032 → 439,464 B）。decor_catalog4 で実測する。
- 追記（F109、2026-10-08）: decor_catalog4 の実機で窓が開いた（利用者）。

