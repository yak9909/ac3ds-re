---
id: ACNL-F0065
aliases:
- F-27
title: F-27 地面更新のダーティビットマップ — `HIGH`
summary: '`sub_59DA7C(X, Y)` (`0x59DA7C`) と `sub_599814(X, Y)` (`0x599814`) は'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5888636
- 5871636
tags:
- map
supersedes: []
source: v1:RE/FINDINGS.md:1419-1437
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-27 地面更新のダーティビットマップ — `HIGH`

`sub_59DA7C(X, Y)` (`0x59DA7C`) と `sub_599814(X, Y)` (`0x599814`) は
どちらも同じ処理を行う（別実装）:

```
if (0 <= X < 0x70 && 0 <= Y < 0x60) {
    v = X + 112 * Y;
    dword_331110F0[v >> 5] |= 1 << (v & 0x1F);
}
```

**マップは 112 x 96 マス。** `X + 112*Y` のビットを立てて「このマスは更新が必要」と
マークする。アイテムを直接書き換えた後にこれを呼べば描画に反映される（F-26 で実証）。

`sub_59DA7C` は追加で `unk_753450` / `sub_5A1B28` / `unk_5A1A90` も呼ぶ。

---

