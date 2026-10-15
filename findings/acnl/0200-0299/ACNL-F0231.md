---
id: ACNL-F0231
aliases:
- F-206
title: 'F-206: ★★★★色とテクスチャの出所は「マテリアル」。自前で積まないと直前のペインのものになる — `HIGH`（実機）'
summary: '`nwlyt_Picture_DrawToCommandList` は必ず先頭でこう呼ぶ。'
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7588716
- 7588740
- 4946020
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12618-12644
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-206: ★★★★色とテクスチャの出所は「マテリアル」。自前で積まないと直前のペインのものになる — `HIGH`（実機）

`nwlyt_Picture_DrawToCommandList` は必ず先頭でこう呼ぶ。

```c
cursor = Material_EmitState(drawctx, cursor, *(picture + 316));      // 0x73CB6C
cursor = TextBox_UpdateDrawState(drawctx, cursor, *(picture+316), 1); // 0x73CB84
```

記録の末尾に相乗りすると、**直前のペインのマテリアルが残ったまま**になる。
テクスチャレジスタ（F-191 の 4 組）だけ上書きしても、TEV が定数色を使う設定なら
そちらが勝つ。実機では自前スプライトが**持ち物欄ボタンの色**になり、
**ボタンをタッチしたときの色変化まで追従した。**

### 対策

「良いマテリアル」を捕まえて、描く直前に自分で 2 つとも呼ぶ。

- `Material_EmitState`（`0x4B7864`）入口をフックして `R2` を控える
- そのフレームで**最初のフラッシュ**の時点の値を採用する
  （＝`cave_draw_sprites` が正しく描けていた文脈のマテリアル）
- ゲーム自身の関数を呼ぶので、`drawctx` 内のキャッシュとも整合が取れる

実測: マテリアル `0x32C96428` を捕獲。上画面の残像も消え、色が自前のものになった。

---

