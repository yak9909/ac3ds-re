---
id: ACNL-F0727
aliases: []
title: "手紙の画像生成は UI ヒープから別画像を確保し、結果を検査せず複製する"
summary: "手紙はモデル資源を読み、別に256×256の画像をUI用Allocatorから作って0x20000 Bを複製する。主リストや通常フォントは別ヒープであり、過去の3.37 MBを全て画像とみなせない。"
date: 2026-10-21
category: system
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: "全関数export・RomFS・公開ソース"
addresses: [0x001FC55C, 0x004A5F90, 0x005691E4, 0x00569B54, 0x00616460]
tags: ["heap", "layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

手紙の `0x1FC55C` は読込モデルをそのまま表示用の唯一の画像にするのではなく、同じUIヒープに別画像を生成し、`0x20000` = 131,072 Bを複製する。確保失敗を検査しないままコピーへ進める。
確度 MEDIUM：手紙の呼出し/命令、画像生成関数の独立した3確保、RomFS実ファイルの寸法・サイズに対応する量を照合。過去の実測記録F0370/F0371（格付け?）を確度の根拠には数えない。

## 根拠

一次証拠は `_local/evidence/107/0x001fc55c.txt`、`0x004a5f90.txt`、`0x005691e4.txt`、`0x00569b54.txt`、`letter_resource.json`、`arcs.json`、`calculations.json`。元exportは `exports.json`。

- 手紙入口は `0x5691E4` の戻りAllocator+4をロード先heapへ渡し、`0x536038` の戻りを検査せず `0x535A08` でモデル内データを得る。続いて幅高256、mipmap数1の記述から `0x4A5F90` を呼ぶ。
- `0x4A5F90` はAllocator vslot+8を `(60,4)`、`(32,4)`、`(画像バイト数,128)` で別々に呼ぶ。手紙は出来た相対参照をたどり、画像への `0x20000` Bコピーを行う。したがって「便箋131,072 Bだけ」が手紙全体の確保量ではない。
- `Item/Model/letter_shic.bcres` のbase実ファイルは131,456 B、SHA256は `letter_resource.json`。この資源とコピー先画素の合計は262,528 B。別モデルのサイズを全便箋へ一般化しない。
- `ssys::ma::Allocator::Alloc` は `size+alignment` をheapへ渡す。従って画素だけでも131,200 B要求で、さらにExpHeapヘッダ・整列の消費がある。60/32 Bのメタデータも別。payloadの合計は正確なheap消費量ではない。
- 実資源をDARCから列挙した結果：`Layout/Letter/ltr.arc` は72,104 B（BCLIM画素合計44,576 B）、`ltr_win.arc` は50,728 B（画素29,472 B）。画像登録 `0x568CFC` はarcの全timgを巡回する。FCRAM参照経路なら画素はarc内に既に含まれ、**arcと内包画素を二重に加算しない**。VRAM指定ならUIのarc写しに加え別領域の画素も要る。
- 上記2arcとモデル/コピー先のファイル・画素量の和385,360 Bは、これらが同時に居るとした場合の素材量。UI実体・TextBoxの文字列/バッチ・Material/UV配列・他の持ち物画面等を含む手紙場面の完全なlive内訳ではない。
- 初期UIヒープ容量3,866,624 Bは `0x616460` で再確認した。一方、主コマンド領域と通常のフォント本体は別のgraphicHeap/FontHeap（[ACNL-F0726][ACNL-F0729]）。したがって3.37 MBを通常フォントや全てGPU画素へ割り振る説明は支持しない。
- 画像以外の大口候補は文字の描画器。`0x13B9A8` は文字器と描画器を別確保し、`0x4D5480/0x4D76A8` の式はN=127字で45,744 B、N=255字で91,584 B（文字器込み、本体・Material・管理費は別）になる。`0x1FC3E0` は手紙に8つのメッセージboxを結び、`0x1FC55C` で各行を設定する。これは静的な費用の傾向であって、当該停止標本の8行がこの容量を持つという実測ではない。式と計算は `textbox-costs.json`。

依頼の停止標本は空き61,924 B、自作分297,728 B、未確保画素131,072 B。生ダンプや測定関数の出力は今回は渡されていない。式 `61,924 + 297,728 − 131,072 = 228,580 B` は再計算できるが、**新しい実測値ではない**。また列挙された画像payloadの和295,424 Bと297,728 Bには2,304 B差があり、全差額を管理費だとは断定しない。

## 反証条件・未確認点

- 3.37 MBのカテゴリ別/呼出し元別live集計は未取得。旧標本の使用量3,376,620 B、旧2要求後227,476 Bと今回概算228,580 Bは別標本であり、1,104 Bの差を誤差と消去しない。
- 合計空き、最大連続空き、wrapperの余分、領域返却によるfree block結合が未確認。228,580 Bを新規確保の上限と保証できない。
- 0x1FC55Cの全失敗例を実機で再現したわけではない。本文は一次命令が検査を欠く箇所の指摘である。
