---
id: ACNL-F0247
aliases:
- F-222
title: 'F-222: ★★★★★自前チートメニューが実機で動いた。ゲームは止まらない — `HIGH`（実機）'
summary: TODO-134 の目的そのもの。**メニューを開いている間もゲームが進行する。**
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:13273-13324
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-222: ★★★★★自前チートメニューが実機で動いた。ゲームは止まらない — `HIGH`（実機）

TODO-134 の目的そのもの。**メニューを開いている間もゲームが進行する。**

ユーザー報告:

> Select で上画面の左からメニューが滑り込み、ゲームも動き続け、
> DPad 上下で選択が動き、選択帯が追従・明滅しています。
> A でチェックが切り替わり黄色になり、X で適用されています。
> Select + DPad Up では従来のメニューも開きます。

### ホットキーの切り分けに CTRPF 本体のパッチは要らない

`PluginMenu::OnOpening`（`bool (*)(void)`）が **false を返すと CTRPF のメニューが開かない**。
CTRPF は Select で開こうとするので、そこで DPad Up の有無を見て振り分ける。

```
Select 単独        -> 自前メニュー（false を返して CTRPF を止める）
Select + DPad Up   -> 従来の CTRPF メニュー（true を返す）
```

### 構成

| もの | 役割 |
|---|---|
| `Sources/GuiRender.cpp` | GPU 経路の 2D 描画器。`FillRect` / `DrawText` |
| `Sources/GuiMenu.cpp` | メニューの状態機械と描画。専用スレッドで毎 16ms |
| 段 B のケーブ | 表・チャンク数・色を .bss から読む（F-220） |

- グリフアトラスは **128x128 LA4**（8x8 セル 256 個）。**出てきた文字から順に割り当てる**
- 表は **プラグインの `new`** で確保。CPU が読むだけなので物理アドレスは要らない
- 表は 2 面 + 全域ダミー埋めで、ちらつきと読み過ぎを同時に防ぐ
- 色はチャンク（7 枚）単位なので、`Flush()` が同色をまとめて詰める

### ★書き出したケーブのテクスチャ寸法は必ず直す

ケーブは 64x64 の値を持っている。グリフアトラスは 128x128 なので、
`kGuiTexSizeWord` / `kGuiTexFmtWord` を差し替える。忘れると別物として読まれる。

### ★「未適用」を旗で覚えてはいけない

最初は `dirty` という旗を立てていたので、**ON にしてから OFF に戻しても黄色のまま**だった
（実機で指摘された）。設計（`ui-model.js` の `isDirty`）は
**「今の値 != 適用済みの値」**で判定している。旗ではなく比較にすると、
戻したときに自然に黄色が消える。

**状態を「変化した」で覚えると、戻ったことが表せない。**
「基準の値」を持ち、差で判定すること。


---

