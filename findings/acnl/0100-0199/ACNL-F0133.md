---
id: ACNL-F0133
aliases:
- F-95
title: 'F-95: GPU コマンドバッファ `g_GpuCmdPtr` の特定'
summary: 'confidence: **MEDIUM**（逆コンパイルでヘッダ定数と書き込み手順を直接確認。**静的解析のみ**、F-101 で訂正）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9890452
- 4855736
- 1212596
- 1370292
- 1185468
- 1213000
- 1264936
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5521-5579
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-95: GPU コマンドバッファ `g_GpuCmdPtr` の特定

confidence: **MEDIUM**（逆コンパイルでヘッダ定数と書き込み手順を直接確認。**静的解析のみ**、F-101 で訂正）

### ★`g_GpuCmdPtr`(`0x96EA94`)

PICA200 コマンドバッファの**書き込み位置**を持つグローバル。
描画コードは専用の AddCommand 関数を通さず、**インラインで**
`(値, ヘッダ)` の 8 バイト対を積んでポインタを進める。

`nwgfx_SimpleMaterialActivator_Activate`(`0x4A17B8`) が最も読みやすい実例。

```c
v18 = (u32 *)g_GpuCmdPtr;
*(u32 *)(g_GpuCmdPtr + 8) = v15;
*(u32 *)(v19 + 4) = 65679;      // 0x0001008F
*v18   = !v15;
v18[1] = 65990;                 // 0x000101C6
g_GpuCmdPtr = v20;              // += 16
```

### ヘッダ形式と実測値

`header = reg | (mask << 16) | (extra << 20) | (consec << 31)`

`0x000F0083`(TEXUNIT0_PARAM) / `0x00020105`(BLEND_FUNC) /
`0x00020107`(BLEND_COLOR) / `0x0001006D`(DEPTHMAP_ENABLE) /
`0x0001008F` / `0x000100E0` / `0x00010149`(+16*i でライト別) /
`0x000101C6` / `0x00040284`

**★`mask` は `0xF` 固定ではなく、部分マスク（1/2/4）が主流。**

### 補助プリミティブ

- `GpuCmd_Advance(bytes)`(`0x1280B4`) … `g_GpuCmdPtr += bytes`
- `Copy24Bytes(dst, src)`(`0x14E8B4`) … コマンド 3 組を一括で積む
- `sub_12EC54` … ブロック転送（LUT など）

### `nn::gr` 相当の所在

`g_GpuCmdPtr` の参照元から **`0x1216BC`-`0x128248`** と **`0x134D28`**。
うち `sub_121E2C`(`0xCA4`) が最大で、状態更新かフラッシュの本命。

### ★F-94 の誤りを訂正

F-94 で「静的な PICA コマンドヘッダは 0 件」と書いたが、**走査条件がバグだった**。
`(w & 0xFFF00000) == 0x000F0000` は、`0x000F0000` の立っているビットが 16-19 で
上位 12 ビットのマスクに掛からないため**恒偽**。

正しく `(w >> 16) == 0x000F` で引くと 1192 件出る。ただし中身を確認すると
`0x001Fxxxx` のアドレス列（ジャンプテーブル）や `0x015F015F` の埋め値
（先頭が `0x00007FFE` = 空アイテムのマップ配列）が大半で、
**結論（実行時生成）自体は変わらない。**

そもそも実際の mask が 0xF 固定でない以上、この走査手法は筋が悪かった。
**構造から辿る（vtable → Activate → バッファ）ほうが正解だった。**

---

