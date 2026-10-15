---
id: ACNL-F0178
aliases:
- F-141
title: 'F-141: TextWriter wrapper のコピー範囲と reset の実体 — `HIGH`（静的命令列）'
summary: '`sub_7E7F48` (`0x7E7F48`) は caller が渡した writer から **0x64 bytes 全体**を stack-local'
date: '2026-08-24'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8290120
- 5076784
- 4960888
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9084-9100
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-141: TextWriter wrapper のコピー範囲と reset の実体 — `HIGH`（静的命令列）

`sub_7E7F48` (`0x7E7F48`) は caller が渡した writer から **0x64 bytes 全体**を stack-local
writer へ `Mem_Copy` し、`nwfont_TextWriter_DrawString(local,R1,R2)` を呼ぶ。その後に caller
へ戻すのは local `+0x2C/+0x30`（cursor x/y）の 8 bytes だけで、4番目の引数 `R3` は関数内で
読まれない。従って自前描画では、毎回 writer の cursor を初期化してこの wrapper を呼ぶか、
直接 `DrawString` を呼んで caller 側で cursor を管理できる。

`sub_4D7730` (`0x4D7730`) は引数無しで channel index 0〜3 を `sub_7A7F74` に渡す。
同関数は各 channel の dirty byte `+0x46D` を 0 にし、必要時に共通 command state の bit
`0x40` を立てる。これは「描画後にテクスチャだけを戻す」処理ではなく、native TextBox
経路が次の部品へ進むための channel dirty/reset 処理である。

**根拠**: `0x7E7F48` と `0x4D7730` の全命令列、`Mem_Copy(dst,src,0x64)` の引数、及び
`sub_7A7F74` の channel-index ループ。実機での状態値と自前 callback からの安全な再利用可否は
`0x4BB278` の live capture 後に判定する。

