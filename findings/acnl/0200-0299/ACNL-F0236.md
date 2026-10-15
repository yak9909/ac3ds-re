---
id: ACNL-F0236
aliases:
- F-211
title: 'F-211: ★★★★マテリアルは「たまたま」ではなく条件で選ぶ — `HIGH`（実機）'
summary: F-206 では「そのフレームで最初のフラッシュ時点のマテリアル」を流用していた。
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12772-12789
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-211: ★★★★マテリアルは「たまたま」ではなく条件で選ぶ — `HIGH`（実機）

F-206 では「そのフレームで最初のフラッシュ時点のマテリアル」を流用していた。
これは動作実績のある文脈を再現しただけで、**条件になっていなかった**。
場面が変わると別のものになり、自前スプライトが見えなくなった。

`nwlyt_Picture_DrawToCommandList` と `DrawCtx_PushVertexColors` から条件を導ける。

| 条件 | 根拠 |
|---|---|
| `*(picture+216)`（UV セット数）≥ 1 | 0 なら UV 属性が構成されない（F-207）。テクスチャを使わないペイン |
| 4 隅の色（`*(picture+320..332)`）が全部 `0xFFFFFFFF` ではない | 全部白だと `DrawCtx_PushVertexColors` は索引経路を使わず、`drawctx+1636` に**アルファ値**を入れて帰る（F-183 / F-186）。頂点カラーを読まない設定のマテリアルになり得る |
| マテリアルの定数色が中立（F-212） | 色付きだとその色が出る |

**「動いた文脈を再現する」ではなく「なぜ動くのか」を条件式にする。**

---

