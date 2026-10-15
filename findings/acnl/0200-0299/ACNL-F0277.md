---
id: ACNL-F0277
aliases:
- F-254
title: 'F-254: ★★★★★自前の Layout ノードを登録すれば、上下とも「最前面」に必ず入れる — `HIGH`（実機）'
summary: F-253 で分かった `LayoutMgr_AddLayout` を使い、**自前の偽 Layout ノード**を毎フレーム
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1798596
- 1798288
- 5664248
- 5672856
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:14906-14982
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-254: ★★★★★自前の Layout ノードを登録すれば、上下とも「最前面」に必ず入れる — `HIGH`（実機）

F-253 で分かった `LayoutMgr_AddLayout` を使い、**自前の偽 Layout ノード**を毎フレーム
リストへ入れられるかを実機で確かめた。`PATCHES/probe_own_layout_node.py`。
**GPU コマンドは 1 語も積んでいない**（描画はまだしない）。

### 仕掛け

| もの | 番地 | 中身 |
|---|---|---|
| 上画面ノード | `.bss` 0x140 バイト | `+0x00` vtable / `+0x04` prev / `+0x08` next / `+0x0C` 優先度 / `+0x134` display |
| 下画面ノード | 同上 | 同上 |
| 自前 vtable | `.bss` 16 スロット | 既定は安全スタブ、**`+0x08` だけ replay ケーブ** |
| 登録ケーブ | `.text` | `AddLayout(mgr, node, screen)` を優先度 `0xFF` で呼ぶ |

replay ケーブは `MOV R0,#0 / BX LR` で返るだけ。`+0x14`（記録）を含む他のスロットも
数えて返るだけのスタブ。**ゲームの描画は一切変えていない。**

### ★フック位置は「パスの入口」ではなく `RenderTop` / `RenderBottom` の入口

最初は `Frame_DrawPass1024`(`0x1B71C4`) と `Frame_DrawPass1025`(`0x1B7090`) の入口に置いた。
上画面は末尾になったが、**下画面は `next = 0x3225AF24` で末尾にならなかった**。
パス入口のあとに走る `sub_2E3190` / `sub_60B930` などが更にレイアウトを登録するためである。

`ssys_ma_lyt_LayoutMgr_RenderTop`(`0x566DF8`) と
`ssys_ma_lyt_LayoutMgr_RenderBottom`(`0x568F98`) の入口へ移したところ、
**上下とも `next = 0`＝リストの末尾**になった。ここはそのフレームの登録が出揃ったあと、
記録と replay の直前である。

### 二重挿入を防ぐ検査（これが無いとリストを壊す）

`sub_13F84C`（PushBack）は `node+0x04` と `node+0x08` が両方 0 のときしか動かない保護を持つ。
そこでケーブ側は **prev / next を書き換えず**、次の 3 つを検査して 1 つでも当たれば見送る。

1. そのリストの tail（上は `mgr+0x0C`、下は `mgr+0x18`）== 自前ノード
2. `ノード+0x04`（prev） != 0
3. `ノード+0x08`（next） != 0

これで「単独で末尾に居る」「末尾だが前に他が居る」「途中に居る」の全部を捕まえられる。
リストはフレーム末尾で `sead_List_UnlinkAll` されるので、次フレームには必ず 0 に戻る。

### 実測（タイトル画面、1000 ms）

```
AddLayout 上画面 成功 = 31   見送り = 0
AddLayout 下画面 成功 = 31   見送り = 0
replay(+0x08) 呼び出し = 93   record(その他スロット) 呼び出し = 62
display 別 replay: 0x400 = 31   0x410 = 31   0x401 = 31
最後の next = 0x00000000   ← リストの末尾（最前面）
上ノード: 優先度=0xFF display=0x410
下ノード: 優先度=0xFF display=0x401
```

- **毎フレーム 1 回ずつ登録でき、見送りは 0。** ゲームが確実に外してくれている。
- **replay は 1 フレームに 3 回**（`0x400` / `0x410` / `0x401`）。
  ケーブ内で `ノード+0x134` を読めば、**上下の描き分けも左目・右目の描き分けも取れる。**
- **上下とも `next = 0`。** 優先度 `0xFF` で必ず末尾＝最前面になる。
- クラッシュなし。撤去後、フック語・ケーブ域・`.bss` を独立に読み戻して全て素／zero を確認した。

### この方式が解く問題（`HANDOFF_CHEATMENU.md` §2 の 3 件）

| 問題 | この方式でどうなるか |
|---|---|
| ロード画面クラッシュ（F-232 容量超過） | 積む先が Layout の記録リスト（`0x1000` 級）ではなく主リスト（残量 `0xF6000` 超、F-253） |
| 上画面のロード画像に隠れる（F-234） | 全 Layout の後に呼ばれるので、ロード画像 Layout より後になる |
| 候補ごとに座標系が違う（F-230） | 相乗り先が無い。投影は自分で設定する |

### まだ未検証

**描画そのもの。** replay スロットから主リストへ GPU コマンドを積んで、
正しく提出されるかはこれから。F-235 では `Frame_EndDrawPass1024` の主リスト末尾に
積んだときに画面更新が止まっているので、安全とは言えない。
必要な材料は F-206（マテリアル）/ F-207（UV セット数）/ F-214・F-215（定数色の中立化）/
F-191・F-216（テクスチャレジスタ）に揃っている。

---

