---
id: ACNL-F0234
aliases:
- F-209
title: 'F-209: ★★★★★TODO-131 完了。自前 GUI が常に最前面に描かれる — `HIGH`（実機）'
summary: '`PATCHES/cave_draw_topmost.py`。フックは 4 つ。'
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4946020
- 5670612
- 5670768
- 4948832
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12706-12728
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-209: ★★★★★TODO-131 完了。自前 GUI が常に最前面に描かれる — `HIGH`（実機）

`PATCHES/cave_draw_topmost.py`。フックは 4 つ。

| フック | 番地 | 役割 |
|---|---|---|
| マテリアル捕獲 | `0x4B7864` | `Material_EmitState` の `R2` を控える（F-206） |
| 記録要求フラグ強制 | `0x5686D4` | 対象リスト id を毎フレーム記録し直させる（F-204） |
| 描画 | `0x568770`（NOP） | 記録本体の直後に自前スプライトを積む |
| drawctx 記録 | `0x4B8360` | `DrawCtx_FlushBatch` の `R0` と、最初のフラッシュ時のマテリアル |

実機での確認（ユーザー報告）:

> ACNL GUI OK ははみ出さず、ノイズも無く、メニューを開閉しても常に最前面のままです。
> 線幅も均一です。

**メニュー開閉で描画順が変わる問題（F-199）も同時に解決した。**
記録ではなく再生の順序が描画順を決めており、対象を「そのパスで最後に再生される
レイアウト」に固定したため、UI の構成が変わっても順序が動かない。


---

