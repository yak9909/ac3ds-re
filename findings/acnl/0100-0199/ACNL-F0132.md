---
id: ACNL-F0132
aliases:
- F-94
title: 'F-94: 描画スタックの同定と GSP IPC 層'
summary: 'confidence: **MEDIUM**（RTTI 実測 + IPC パターンを逆コンパイルで確認。**静的解析のみ**）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9418792
- 4809012
- 9418480
- 4773652
- 9423220
- 5075992
- 9420548
- 5075988
- 4771840
- 5079040
- 1250460
- 1250736
- 1250640
- 1250532
- 1274456
- 1291940
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5465-5520
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0133", "ACNL-F0139"]
---
## F-94: 描画スタックの同定と GSP IPC 層

confidence: **MEDIUM**（RTTI 実測 + IPC パターンを逆コンパイルで確認。**静的解析のみ**）

> ★F-101 で訂正: CLAUDE.md の `HIGH` は「静的解析と動的観測の双方」。
> 本項は実機観測をしていないので `MEDIUM` が正しい。

### 描画は NintendoWare for CTR (nw4c)

RTTI 全 2,895 クラス（F-53）の名前空間を集計して確定:

`nn::nex` 466 / `nn::pia` 223 / **`nw::gfx` 63** / `nw::snd` 52 /
`nn::fs` 22 / **`nw::lyt` 15** / `nw::anim` 11 / **`nw::font` 7** /
`g3d` 29 / `gui` 29 / `lyt` 16 / `sead` 346

**`nn::gr` は RTTI 0 件** = 仮想関数を持たない静的 API。クラス名からは辿れない。

主要 vtable:

| クラス | vtable | 実装位置 |
|---|---|---|
| `nw::gfx::RenderContext` | `0x8FB828` | `0x496134` |
| `nw::gfx::MeshRenderer` | `0x8FB6F0` | `0x48D714` |
| `nw::font::RectDrawer` | `0x8FC974` | `0x4D7418` |
| `nw::lyt::Drawer` | `0x8FBF04` | `0x4D7414` |

nw4c 本体は **`0x48D000`-`0x4D8000`**。

### GSP IPC スタブ 6 本

IPC ヘッダ定数で走査 → リテラルプールを `xrefs_to` して関数を特定。
6 本すべて `MRC p15,0,Rd,c13,c0,3`（TPIDRURO）+ `SVC 0x32` を持つことを確認。

`GSPGPU_WriteHWRegs`(`0x13149C`) / `WriteHWRegsWithMask`(`0x1315B0`) /
`SetLcdForceBlack`(`0x131550`) / `AcquireRight`(`0x1314E4`) /
`RegisterInterruptRelayQueue`(`0x137258`) / **`FlushDataCache`(`0x13B6A4`)**

詳細は `DOCS/rendering.md`。

### ★定数走査の偽陽性を 1 件踏んだ

`sub_14A9C8` は `TriggerCmdReqQueue`(`0x000C0000`) の一致で GSP 関数に見えたが、
中身は **YUV→RGB 変換**（`QADD16`/`USAT16`、YCbCr 係数 11277/29033）。
直後の `dword_14AAE4` がたまたまその値を持つデータ表だった。

**教訓: 定数が一致しただけで断定せず、必ず中身を読む。**
IPC スタブのヘッダ定数は関数本体の**直後**のリテラルプールにある。

### 未解明

- コマンドリストの構築・提出経路。**静的な PICA コマンドヘッダは 0 件**なので実行時生成
- `SetBufferSwap`(`0x00050200`) / `TriggerCmdReqQueue` のスタブ未発見
- 毎フレーム描画ループの入口

---

