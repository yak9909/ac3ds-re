---
id: ACNL-F0732
aliases: []
title: "VRAM ExpHeap の空き・使用中リストと整列後の最大枠"
summary: "ssys::ma::VramExpHeap は24 BのCPU側ノードでVRAM領域を管理する。free/usedは+0x48/+0x3Cの別リストであり、sead::ExpHeapの+0x78/+0x88を当てられない。総空きと整列後の最大枠はノードだけから計算できる。"
date: 2026-10-21
category: system
build: acnl_jpn_v15
confidence: MEDIUM
tool: "全関数export・実RomFS・提供停止ログ・公開ソース"
addresses: [0x00120C58, 0x00120BE0, 0x00565DAC, 0x00565D20, 0x0074F2A8, 0x0074F2EC, 0x001263A8]
tags: ["heap"]
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

MemoryMgrが使う `ssys::ma::VramExpHeap` の管理構造は、FCRAMの `sead::ExpHeap` と異なる。VRAM本体を読むことなく、CPU側のfree/usedノードから空き・占有・最大連続枠を得られる。
確度MEDIUM：コンストラクタ、独立したalloc/free、総空き/最大枠の走査を照合。実機の残量は今回測っていない。

## 根拠

一次証拠 `_local/evidence/107/0x<8桁アドレス>.txt`、出所/ハッシュ `exports.json`。vtableのバイトは `resume-codebytes.txt`。

`0x120C58` は同じthisを最終的にvptr `0x900484`のVramExpHeapへする（+0xCは埋込みCriticalSectionであり、内側heapのthisではない）。`0x11ECD4` はこの戻り値を公開する。

| heapからのoffset | 内容 |
|---|---|
| +0 | vptr、標準のVramExpHeapは0x900484 |
| +0x28 | 親側/所有元heapへの欄 |
| +0x2C / +0x30 | 管理範囲のsize / 開始VA |
| +0x34 / +0x38 | CPU管理heap / 24 Bノード用VramBlockHeap |
| +0x3C | usedリスト。+0 vptr、+4 head、+8 tail |
| +0x48 | freeリスト。同じ12 B形式、sentinel無し、末端0 |
| +0x54 | 小さい残りを選ぶ探索の有効フラグ |

| 24 B nodeからのoffset | 内容 |
|---|---|
| +0 / +4 / +8 | vptr / prev / next |
| +0xC | 占有size。usedでは先頭paddingを含む |
| +0x10 | 先頭padding。freeでは0 |
| +0x14 | 領域の開始VA。返す画像VAはこれ+padding |

- `0x120BE0` はsize/startを1ノードへ写しfreeへ登録。`0x1263A8` はhead/tailとprev/nextを操作する。
- alloc `0x565DAC` は要求を4 Bへ切上げ、alignmentを最小4・非2冪なら4へ正規化。free head `[heap+0x4C]` からnode+8をたどる。`padding=align_up(node.start,a)-node.start`、`available=max(0,node.size-padding)`。分割後にusedへ登録し `start+padding` を返す。
- free `0x565D20` はused head `[heap+0x40]` から `start+padding==pointer` を探し、paddingを0に戻してfreeへ移す。
- `0x74F2A8` はfree headから `node+0xC` を合算。`0x74F2EC` は同じリストで `max(size-(align_up(start,a)-start),0)` の最大を返す。どちらもCriticalSectionを取得/解除するため、**関数呼出しはメモリを読むだけではない**。

正規の画素確保/返却はF0726のMemoryMgr type 0x20000/0x30000。VRAMに空きがあっても、分割用のCPUノードheapが枯れるとallocが0を返す分岐がある。freeの数値だけで成功を断定しない。

## 反証条件・未確認点

現在のMemoryMgr+0x18/+0x1Cが別型の子heapなら、このoffsetを適用しない。rootとcurrentを両方読み、同じpointerは重複集計しない。子heap分を親のusedとさらに足すと二重計上になる。
手紙/HOMEでの総空き・最大枠・ノードheap余力は未測定。VRAMの全範囲が未使用という意味ではない。
