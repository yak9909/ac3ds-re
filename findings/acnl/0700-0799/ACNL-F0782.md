---
id: ACNL-F0782
aliases: []
title: "通常メニューの0x08と0x10は入場完了時に併存する"
summary: "BsMenuItem OpenUpdateのmask0xFFFFF7EFは0x08を保存する。F0770の排他的段階値という説明を訂正し、開始8→完了0x18→終了で両方解除という通常経路を採用する。"
date: "2026-11-22"
category: "ui"
build: "acnl_jpn_v15"
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: "exports+codebytes"
addresses: [0x199f9c, 0x199f44, 0x19aac0, 0x949d68]
tags: ["menu", "inventory"]
supersedes: ["ACNL-F0770"]
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

F0770の「0x08/0x10は互いに排他的」は誤り。通常持ち物の入場完了では両方が立つ。MEDIUM（開始・完了の異なるARM書き手と0x6D6060の待ちを照合）。訂正はこのビットの説明に限り、F0770のButtonActionControl戻り値の解析を否定しない。

## 根拠

- 0x199F9C OpenEnter: flags = (flags & 0xFFFFFFE7)|8。
- 0x199F44 OpenUpdate: flags = (flags & 0xFFFFF7EF)|0x10。後者は0x08を消さない。
- _local/evidence/164/calculations.jsonで8から後者の演算結果が24（0x18）と検算。
- CloseUpdate0x19AAC0の0xFFFFFFE7は8と0x10を共に落とす。
- 0x6D6060は外側に0x08のgateを置き、その中で0x10を待つ。完了時に開始bitが消えるという説ではこの読み手が進まない。
- チャットもWindowInEnter0x57CDC8で10を落とすが、button-in enter0x57CC9Cが10を立てる。updateだけを見て「チャットでは10が無い」としてはいけない。
- 一次抜粋: _local/evidence/164/selected_functions.txt。関連集約: topics/acnl/bottom-screen-widgets.md §2/4。

## 反証条件・未確認点

任意の画面がこのhandshakeを持つわけではない（Catalogは不実装）。実機値の新しい追試はしていない。
