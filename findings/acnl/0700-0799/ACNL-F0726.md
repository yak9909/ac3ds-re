---
id: ACNL-F0726
aliases: []
title: "描画の確保先は 2D UI・graphic FCRAM・VRAM A/B に分かれる"
summary: "2D_UI_Heap は 3,866,624 B、graphicHeap は別の 7,008,256 B。MemoryMgr は種別 0x10000/0x20000/0x30000 を FCRAM/VRAM A/VRAM B へ振り分け、対応する解放関数も持つ。"
date: 2026-10-21
category: system
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: "全関数export・RomFS・公開ソース"
addresses: [0x00616460, 0x005691F4, 0x0011DA78, 0x006165A8, 0x00616510, 0x00121DDC, 0x00121DA0, 0x0011CE64, 0x004E97CC]
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

描画用メモリは一つではない。`g_LayoutAllocator` の `2D_UI_Heap`、MemoryMgr の FCRAM `graphicHeap`、VRAM A/B は別管理である。ゲーム自身の MemoryMgr に VRAM を含む確保・解放の経路がある。
確度 MEDIUM：初期化の代入、独立した確保/解放の振分け、実際のコマンド・画像・描画面の呼出しを照合。今回の実機測定なし。

| 管理域 | 初期値・用途の一次証拠 |
|---|---|
| 2D_UI_Heap | `0x616460` が `0x3B0000` = 3,866,624 B を `0x5691F4` へ渡す。UI実体・arc写し・後述の便箋画像 |
| graphicHeap | `0x11DA78` が `0x6AF000` = 7,008,256 B のExpHeapを作り、MemoryMgr+8と+0x14へ保存。主/個別のコマンド領域、表示用バッファ等 |
| dG3d | `0x4E97CC` が `0x39800` = 235,520 B を作り、g_GfxAllocatorの+4へ結ぶ。nw::gfxのrender context、queue、traverser、loader等。主コマンド領域は別経路 |
| rootVramA/B | MemoryMgr+0xC/+0x10（現在の確保先+0x18/+0x1Cも同じ）。描画面・深度面、VRAM指定の画像転送先 |
| VRAM管理用のCPUヒープ | A/Bそれぞれ `0x7800` = 30,720 B を `0x11ECD4` で作る。VRAM画素の容量ではない |

## 根拠

一次証拠は `_local/evidence/107/0x<8桁アドレス>.txt`。元exportの相対ファイル名・SHA256・symbols commitは同所 `exports.json`、数値は `calculations.json`。export内の既存コメントは根拠に数えず、命令を使用した。

- `0x5691F4` は一度作った同じheapを2つのAllocator+4へ設定。`0x568FDC` → `0x4B37DC` → `0x4B8EBC` が一方を大域 `0x96F150` へ設定する。arc用 `0x96FC40` とのheap共有を確認した。
- `0x6165A8` は `(this,memoryType,kind,未使用,size)`。sizeは入口でSPからR1へ読み、0x10000なら+0x14のheap vslot+0x18、0x20000/0x30000なら+0x18/+0x1CのVRAM heap vslot+8へ渡す。**kindから整列へ変換**し、0x100→4、0x103→64、0x102/104/105→16、0x101および範囲外→128。疑似Cの既定分岐でkindがそのまま残る形は採らない。ジャンプ表を `codebytes.py` で照合（`codebytes.txt`）。
- `0x616510` は同じ種別でFCRAM vslot+0x1C、VRAM vslot+0xCへ解放する。pointerは第5引数からR1へ移す。原本vtable `0x904FA4` のalloc/free欄とも一致。
- `0x121988` と `0x120A18` はコマンド領域を種別0x10000で確保する。`0x11CE64` は表示用バッファを0x10000、共通描画面をA、深度面をBへ要求。`0x5676C8` は画像の指定種別を使い、FCRAMなら元資源を参照、VRAMならMemoryMgr callbackで別確保しDMAを積む。
- `0x4E97CC` はdG3dとは独立に `0x121988(0x96000,10)` を2回呼ぶ。主コマンドの画素以外の容量だけでも1,228,800 B（GX欄・管理費は別）となる。大きなgraphicHeapを全て余った画像用メモリとはみなせない。
- `0x121DDC` と `0x121DA0` のVRAM範囲は以下。flagは `0x9778B9`（`0x12ACA0`）、設定側 `0x1200E4` は1を書く。機種だけからflagを決めない。

| flag | Aの開始…終端値 | Bの開始…終端値 | 作成時のsize引数（A / B） |
|---|---|---|---|
| 0 | 0x1F000000…0x1F2FFFFF | 0x1F300000…0x1F5FFFFF | 3,145,727 / 3,145,727 B |
| 1 | 0x1F180000…0x1F2FFFFF | 0x1F380000…0x1F5FFFFF | 1,572,863 / 2,621,439 B |

size引数は命令どおり「終端値−開始」。包含区間のバイト数と1 B違う。これは初期の管理範囲であり空きではない。

公開資料 `STUDY107_PUBLICS` の [3dbrew Memory layout](https://www.3dbrew.org/wiki/Memory_layout) はVRAMのVA/PAと6 MiBの物理容量、FCRAMを説明する。[libctru vram.cpp](https://github.com/devkitPro/libctru/blob/master/libctru/source/allocator/vram.cpp) のvramInitは全VRAMを自身のpoolへ入れる。これはゲームの使用中範囲を知らないため、ゲーム内MemoryMgrの代用品にはできない。

## 反証条件・未確認点

- 手紙・HOME・ロード中のFCRAM/VRAM総空きと最大連続空きは今回未採取。全VRAMが空きという結論ではない。正規関数の存在と、その時点で必要量が取れることは別。
- 実行時に「現在の確保先」3欄が子heapへ変更される可能性、GPU完了待ち、画像再配置、Old/Newの実測は未検証。0x7800の管理用ExpHeapへ画素を置く結論ではない。
