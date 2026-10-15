---
id: ACNL-F0263
aliases:
- F-237
title: 'F-237: Layout の再生順は `LayoutList_SetDisplay` で局所的に制御できる — `MEDIUM`（静的＋実機 no-draw）'
summary: '`REFERENCES/TEXTS/render.txt` の gokiro 氏は、描画コマンド追加・再生順変更・コマンド'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5664248
- 5664304
- 1798596
- 1798800
- 5664416
- 1798804
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:14093-14133
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-237: Layout の再生順は `LayoutList_SetDisplay` で局所的に制御できる — `MEDIUM`（静的＋実機 no-draw）

`REFERENCES/TEXTS/render.txt` の gokiro 氏は、描画コマンド追加・再生順変更・コマンド
バッファ拡張を分ける設計を示している。これは実装設計として高信頼度の参考情報として採用するが、
本作 JPN 無印の番地・ABI・効果はゲーム自身の静的／動的根拠で独立に確認した。

### 静的根拠

- `LayoutMgr_RenderTop(0x566DF8)` は `root+4` の LayoutList 仮想 slot `+0x08` を先に呼び、
  表示サイズを `(0x190, 0xF0)` に設定してから、`R1=0x400` で `0x566E30` を tail-call する。
  `Frame_DrawPass1024(0x1B71C4)` からの唯一の xref は `0x1B7290` である。
- `LayoutList_SetDisplay(0x566E30)` は `list+4` から node `+8` を辿る。各 Layout について
  `Layout+0x134 = display` を書き、vtable slot `+0x08`
  (`Layout_ReplayRecordedList`) を呼んでから次 node に進む。従ってこのループは、記録処理とは
  別の、各画面の record-list 再生順を決める箇所である。
- これは `LayoutList_RecordChildren(0x566EA0)` が node vtable slot `+0x14` を呼んで記録を作る
  F-236 の経路とは別であり、外部説明の「command-add hook」と「ordering hook」を分ける構造と一致する。

### 動的照合と限定プローブ

software breakpoint を `0x566E30` にだけ置き、予約付き走行で上画面呼出を実測した。
停止時の `R0=root+4`、`R1=0x400`、`LR=0x001B7294` は上の静的 call-site と一致した。
breakpoint はその場で削除し、再開前に元語 `0xE92D4070` を読み戻した。

`PATCHES/probe_layout_reorder.py` は描画コマンドを一切増やさない。top display (`0x400`) の時だけ
LOG が指す Layout を traversal 中には一度保留し、リストの他 node の後に再生する。node の `+4/+8`
リンクは変更せず、現在の list 内でその pointer が見つかった時だけ再生するため、古い heap pointer を
直接呼ばない。

title 場面で既に tail だった Layout を意図的に対象にして 1200 ms 走らせた。`count=0x72`、
累積 top-target match `0x26` を記録し、無クラッシュで停止した。これは保留／末尾 replay が上画面で
複数回実行されたことを示すが、対象が元から tail なので出力順は stock-equivalent である。
よって「非 tail の UI画像（スプライト）がロード画像 id `0x10` より前面になる」という視覚効果は
まだ立証されていない。hook・46-word cave・8-word LOG は直後に撤去し、独立 read-back で
`state=-1`、BP 0、`0x566E30=0xE92D4070`、cave/LOG zero を確認した。

このため再生ループの役割は `HIGH` 相当の静的＋BP 根拠を持つが、順序変更を最終 UI 経路として
採用する判断は非等価な画面での視覚／replay trace が未取得なので `MEDIUM` に留める。

---

