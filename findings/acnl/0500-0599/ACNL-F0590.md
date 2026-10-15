---
id: ACNL-F0590
aliases:
- IDA-opus-5.5-F074
title: 'HHD の顔の画面が ACNL の下画面の最前面に予想どおり出る・必要なメモリ（2026-10-05、HIGH: 実機の画面と designer の予想の照合 + 実機のメモリ）'
summary: 解析ソフト IDA（ida-pro-mcp）、解析モデル opus-5.5。T013 段 1。gohan `work/hhd-charcreate` eb79ee7、3gx SHA-256 0021cca0…3cc6、SD /hhd_charcreate.arc 333,096 B。
date: '2026-10-05'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4461-4474
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F074: HHD の顔の画面が ACNL の下画面の最前面に予想どおり出る・必要なメモリ（2026-10-05、HIGH: 実機の画面と designer の予想の照合 + 実機のメモリ）

解析ソフト IDA（ida-pro-mcp）、解析モデル opus-5.5。T013 段 1。gohan `work/hhd-charcreate` eb79ee7、3gx SHA-256 0021cca0…3cc6、SD /hhd_charcreate.arc 333,096 B。

- 利用者の目視: 下画面全体が顔の画面（目 12・色見本 6+8・ボタン 2 と文字）、状態の通知、OFF で戻る — 全部 PASS。
- Chokistream（work/evidence/screens/hhd_t013/face_on_running.png、run_timed 6000 ms の走行中）を designer の予想（acnl-ui-designer out/hhd/hhd_face_mode_bottom.png）と比べると、
  **輝度で平均差 1.60・差 24 超 0.0%**。RGB の差（平均 11.7）は Chokistream の JPEG の色間引きによるもの（compare.py の注記）。→ 変換（F072 と設計 §3.2 の 5 項目）と designer の描画規則が実機と一致。
- 優先度 0xFF で、ゲームの地図・タブ・下のボタンより手前に描かれる（AddLayout の昇順挿入、F-253）。
- 実機で測った量（gohan の .bss を IDA で読んだ）:
  - 描画命令（記録した長さ / 確保）: 地 784 / 8,192、顔 13,344 / 65,536、目 23,104 / 32,768（**目は 70%**）、髪は未描画。
  - 読み込みヒープ（sead::ExpHeap 0x32C45F78）の空き: 組む前 925,364 B → 後 336,748 B（使用 588,616 B = arc 333,096 + レイアウトの部品など 255,520）。
    カタログ表示中の記録（空き 1,456,124 B、旧 SESSION）より少ない場面なので、ほかの UI と同時に開くときは残りに注意。
- 未確認: 画面遷移をまたいだとき、髪のモード（命令量）、入力（いまは下のゲーム UI がタッチに反応する見込み、未確認）。

