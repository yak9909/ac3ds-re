---
id: ACNL-F0589
aliases:
- IDA-opus-5.5-F073
title: '自前の DARC をメモリから渡して下画面にレイアウトを出せる（2026-10-05、HIGH: 静的 + 実機）'
summary: 解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。D005 / T012 の最小の実機確認。
date: '2026-10-05'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5665348
- 9894976
- 9436920
- 9894956
- 5672188
tags:
- layout
supersedes: []
source: IDA:work/FINDINGS.md:4447-4460
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F073: 自前の DARC をメモリから渡して下画面にレイアウトを出せる（2026-10-05、HIGH: 静的 + 実機）

解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。D005 / T012 の最小の実機確認。

- 手順（静的に ArcResAccReader_LoadArcStep 0x567244 の読み込み後の処理を写した）: ゲームの読み込みヒープ [[0x96FC40]+4]（RTTI `sead::ExpHeap`、vtable 0x8FFEF8、+24 確保 / +28 解放）に
  アライン [0x96FC2C]=0x80 で確保 → 写す → sub_12D294 で flush → ArcResAccReader_Ctor → holder+0x158 / +8 = arc → Attach(holder+0xC, arc, ".") →
  `ArcResAccReader_RegisterTextures 0x568CFC`（命名）→ Layout を組み、毎フレーム LayoutCalc + AddLayout(mgr, layout, 1)。
- 実機（gohan `work/hhd-charcreate` 29050a7、3gx SHA-256 3e8bf95b…fcf7、SD の hhd_bg_only.arc 5,416 B）: 利用者の目視で下画面に黄色の地と橙の水玉、OFF で元に戻る（PASS）。
  IDA で停止中に読んだ値: arc=0x32F14100（先頭 darc）、holder の 3 か所とアクセサ+0x20 が同じ arc、優先度 0x80。
  Chokistream（work/evidence/screens/hhd_t012/on_running.png、走行中に撮影）: 地 (254,215,0)・水玉の周期 22.5 / 45.2 px は HHD のスクショ（255,215,0、23 / 45 px）と一致し、
  水玉の位置は designer の予想画像と一致（列 x=9/54、行 y=54.3/99.5…）。
- 見え方: 優先度 0x80 では、ゲームの下画面の UI（地図・上のタブ・下のボタン）がこの地の**手前**に描かれる。全画面を覆うには、ゲームの下画面 UI を隠すか優先度を変える必要がある（未調査）。
- 反証条件: 画面遷移（建物の出入り・地図の切り替え）をまたいで出し続けたときに壊れれば、寿命の扱いが足りない（未試験。今回は同じ場面だけ）。

