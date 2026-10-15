---
id: ACNL-F0655
aliases:
- Ghidra-gpt-sol-5.6-F017
- G-F017
title: Ghidra-gpt-sol-5.6-F016 AR先頭E blockの最終行が1word欠けていた
summary: '**確度: HIGH（ARテキスト構文再検査）。**'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses: []
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:570-584
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F017: Ghidra-gpt-sol-5.6-F016 AR先頭E blockの最終行が1word欠けていた

**確度: HIGH（ARテキスト構文再検査）。**

Ghidra-gpt-sol-5.6-F016初版は `E0838424 0000004C` に19 wordのpayloadを置いたが、最終データ行が `00000000` の1wordだけになっていた。CTRPF ARの各コード行は2word形式で記述するため不完全。

修正版はblockを `0x50` bytesへ拡張し、末尾を `00000000 00000000` として4-byte paddingを明示。全AR行を再検査し、データ/通常コードとも全行が8hex+8hexの2word形式であることを確認済み。

修正guard block SHA-256: `2995fa6ffaf19ca981d2d74b73f2c986363a708cc549c0898be1138e1a235936`

main caveは不変: `9ecc906c807c162fb7ccecc3b31a8b1d5a99a8d944a790d7e22ddfe9751131d7`

combined: `7cd41fcf4282683bdc14d20a0e05a92d2c04be7fc8244d80e1f699238deb6c97`


