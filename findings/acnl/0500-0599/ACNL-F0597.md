---
id: ACNL-F0597
aliases:
- IDA-opus-5.5-F081
title: 'HHD のキャラクリ画面から ACNL のプレイヤーの見た目を変えられる（実機 全 PASS）（2026-10-05、HIGH: 静的 F080 + 実機）'
summary: '解析モデル opus-5.5。gohan work/hhd-charcreate ce17e54、3gx SHA-256 e25dfca4…d8b3、SD /hhd_charcreate.arc 358,184 B。利用者の目視で全項目 PASS:'
date: '2026-10-05'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6856156
tags:
- player
supersedes: []
source: IDA:work/FINDINGS.md:4565-4575
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F081: HHD のキャラクリ画面から ACNL のプレイヤーの見た目を変えられる（実機 全 PASS）（2026-10-05、HIGH: 静的 F080 + 実機）

解析モデル opus-5.5。gohan work/hhd-charcreate ce17e54、3gx SHA-256 e25dfca4…d8b3、SD /hhd_charcreate.arc 358,184 B。利用者の目視で全項目 PASS:
- 開くとき背景（上下）が 5 フレームでフェードイン（kBgFadeFrames）。
- 開いたとき今の見た目（髪型・髪色・目の形・目の色・肌）が選択されている（LoadCurrentLook）。
- 「けってい」で髪型・髪色・目の色・肌がその場で反映、帽子などの装備は外れない。**肌も pm+448 を書いてその場で変わる**（F080 追記の見込みが実機で成立）。
- 目の形は建物の出入りの後に変わる（顔の絵はモデルを作るときだけ読む、F080 追記と一致）。
- B で閉じると変わらない。状態の通知に結果が出る。
- **vc_UPDATE 0x689DDC はフレームフック（描画フェーズの後）から呼んでも問題が出なかった**（旧 F-68 は行動の入口から呼んでいた）。
- 対応（HHD → ACNL）: 髪 k → k / 17+(k−16)、髪色・目の形・目の色はそのまま、肌 s → 日焼け 2s（HHD-F008 / F080）。通信中は書かない（オンラインは未対応）。

