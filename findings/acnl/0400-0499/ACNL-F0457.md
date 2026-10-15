---
id: ACNL-F0457
aliases:
- IDA-opus-5-F027
title: '`G3dResHolder_Dtor` はヒープ破棄の**前**に呼ぶこと。逆にすると SIGILL（2026-09-21、HIGH、実機）'
summary: '解析ソフト: IDA / 解析モデル: opus-5。**こちらの手順ミスで踏んだ。再現条件と復帰手順ごと残す。**'
date: '2026-09-21'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 3243260
- 9229972
- 1283860
- 1798700
- 7657648
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:1167-1222
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F027: `G3dResHolder_Dtor` はヒープ破棄の**前**に呼ぶこと。逆にすると SIGILL（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。**こちらの手順ミスで踏んだ。再現条件と復帰手順ごと残す。**

### 何が起きたか

T017b の後片付けで、**資源ヒープを破棄したあとに** `G3dResHolder_Dtor 0x00317CFC` を呼んだ。

```
PC  0x008CD694   ← シンボルテーブル領域。コードではない
LR  0x00139714
SP  0x0FFFFC38
tid 267（＝call harness の park スレッド）
IDA のダイアログ: "8CD694: got SIGILL signal (Illegal instruction) (exc.code 4, tid 267)"
```

dtor は `holder+0x1C` の FileRes 側を辿って後始末する。その参照先は**資源ヒープの中**にあるので、
ヒープを先に壊すと**宙に浮いた関数ポインタを呼ぶ**。番地がデータ領域だったので SIGILL になった。

**IDA-opus-5-F022 の全面解放が無事だったのは、そのときは正しい順序（dtor → ヒープ破棄）だったから。**
この順序は守るべき規則であって、たまたまではない。

### 復帰できた

call harness は呼び出し前にレジスタ一式と SP 直下 0x1000 バイトを保存している。
`finish_call()` は **PC がトラップでないと復元を拒む**（故障時の状態を保つ設計）ので、
中身を確認したうえで手で同じ復元を行った:

1. IDA の Warning ダイアログを閉じる（**閉じるまで MCP は全てタイムアウトする**）
2. 故障時のレジスタ・SP 周辺・`pending` を証拠として保存（`t017_cleanup_fault.json`）
3. `del_bpt(TRAP)` → 保存したスタックを書き戻す → CORE レジスタを書き戻す → 読み戻して一致を確認
4. `pending` を消して再開

結果、PC は park（`0x1B722C`）・SP は `0x0FFFFE20` に戻り、**ゲームは無傷で動き続けた**。
**dtor は再試行しない**（同じ場所でまた落ちる）。半分だけ進んだホルダは scratch ごと解放した。

### タイムアウトの読み方

MCP が連続してタイムアウトしたが、**対象がフリーズしたのではなく IDA のモーダルダイアログが
メインスレッドを塞いでいた**。`tools/dynamic/inspect_ida_dialog.ps1` は IDA 側に触れずに
窓を見つけられるので、**タイムアウトが続いたらまずこれを撃つ**。

### 後片付けの数字

instance ヒープと scratch を返した後、親ヒープ `0x301668EC` の空きは **503,128 B**。
IDA-opus-5-F023 の時点（503,224 B）より **96 B 少ない**。
`getMaxAllocatableSize 0x0074D8B0` は **371,852 B** を返すので、
**空きは少なくとも2つのブロックに分かれている**。`sead::ExpHeap` は空きブロックのヘッダを
空き容量に数えないため、**断片化が増えた分だけ合計が減る**のは筋が通る。
ただし自由リストを歩いて確かめてはいないので、96 B が本当に断片化由来かは**未確定**。

根拠: `t017_cleanup_fault.json`、`events.jsonl` の `resholder_dtor_sigill` /
`resholder_dtor_recovered` / `t017_cleanup_done`、IDA の警告文面、`0x317CFC` の逆アセンブル。
反証条件: 資源ヒープを残したまま dtor を呼べば落ちない（F022 で確認済み）、
96 B を自由リスト走査で説明できる。

