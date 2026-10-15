---
id: ACNL-F0517
aliases:
- IDA-opus-5.5-F014
title: 選んだ建物の青＋透明度の揺れ（gohan BuildingHighlight）が実機で動いた（2026-09-23、HIGH）
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。gohan `58701ac`（work/grid-cursor）。F011〜F013 の方法をプラグインへ移した。'
date: '2026-09-23'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2539-2547
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F014: 選んだ建物の青＋透明度の揺れ（gohan BuildingHighlight）が実機で動いた（2026-09-23、HIGH）

解析ソフト: IDA / 解析モデル: opus-5.5。gohan `58701ac`（work/grid-cursor）。F011〜F013 の方法をプラグインへ移した。
- 1 回目（`f9e1116`）は SIGSEGV: PC=`0x0700F2C0`（gohan の `ClassName`、`LDR R3,[R2]`）、R2=`0x3F800000`（float 1.0）。
  **番地の判定を範囲（0x08000000〜0x40000000・4 の倍数）だけで行っていた**ため、建物のデータの小数を番地として読んだ。
  → `svcQueryMemory` で読めるか問い合わせる（1 フレームの領域キャッシュ）に直した
- 2 回目: 利用者確認「光りました。透明度も問題なく動作しています」
- 検査 `tools/models3d/verify_highlight.py`: 定数の照合と、TEV の組み替え（C++ をホストの g++ で組む）が tint_building.py と 3,024 件一致

