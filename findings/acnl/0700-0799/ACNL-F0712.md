---
id: ACNL-F0712
aliases: []
title: "DrawInfo・Layout ノード・LayoutMgr の描画用構造"
summary: "DrawInfoはLayout+0x30に内包され、+0x80はLayoutMgr+0x1Cの文字作業体を指す。Layoutノードのroot・記録範囲・画面と上下リスト、管理者holderへ型を付けた。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x008FC17C, 0x0096FC38, 0x00133A64, 0x001B71C4, 0x001322F0, 0x00569180, 0x0012D2BC, 0x005686D4, 0x005682DC]
tags: ["layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

`NwLytDrawInfo` (0x8C)、`SsysMaLayoutNode` (0x14C)、上下の `SsysMaLayoutList`、管理者の既知先頭 `SsysMaLayoutMgr`、文字作業体の既知範囲を型にし、`g_LayoutMgr` (0x0096FC38)を管理者へのポインタとして設定した。getterは管理者ポインタを返す。`Frame_DrawPass1024` は引数なし、意味のある戻り値を消費しない描画処理としてvoid型にした。
確度 MEDIUM：ctor/生成・登録と、独立した行列計算・木の記録・文字の提出・各画面再生が整合。実機なし。

| 対象 | 欄 |
|---|---|
| DrawInfo | +4投影4×4、+0x44 view3×4、+0x74位置補正倍率2、+0x7C alpha、+0x80文字作業体、+0x88 flags |
| Layout node | +4/+8 prev/next、+0xC優先度、+0x20 root、+0x28/2C幅高さ、+0x30 DrawInfo |
| 同nodeの記録 | +0x100 ID、+0x104開始offset、+0x108バイト長、+0x10C/110 GX開始/数、+0x118容量、+0x11C replay引数、+0x11D再記録要求 |
| 同nodeの画面 | +0x11F投影生成済、+0x120立体視条件、+0x121投影mode、+0x134 display |
| 管理者 | +4上LayoutList、+0x10下LayoutList、+0x1C文字作業体、+0x364 Drawer先頭 |

node+0x134のdisplayは登録用screen引数と異なる。登録は0=上/1=下、各描画パスがdisplay=0x400/0x410/0x401をnodeへ書く。文字作業体へのポインタはnode+0xB0 (=DrawInfo+0x80)。

## 根拠

一次証拠：`_local/evidence/98/primary.txt`、`primary-index.json`、`type-verification.json`。上下・record/replayの既存A格付け再解析 [ACNL-F0693] [ACNL-F0694] [ACNL-F0699] [ACNL-F0700] に従う。

- `0x569184` の管理者全体確保は0xA08。`0x569198..AC` は+4と+0x10に同じLayoutListを置き、+0x1Cで `0x4B4960`、+0x364でDrawer ctorを呼ぶ。最後に `0x5691C4..CC` で大域へ保存。`0x133A64` はその大域を読む。
- 管理者型は必要な+0x368までの**部分型**。0xA08全体やDrawer全体を解明した型ではない。文字作業体も確認した0x2E4範囲のうち、+0x13Cの一時batchと+0x164のPane行列だけを名付け、他は不明バイトで保持する。`0x4B7CE0` は前者を一時設定して提出後に消し、`0x4B6AD0` は後者へPane大域行列12語を転記する。
- `0x12D2BC` は内包nw::lyt::Layoutを+0x10、DrawInfoを+0x30で構築し、node+0xB0へgetter戻り+0x1Cを保存。`0x1322B4` の内包Layout root+0x10と、`0x4D7190` のroot読取りはouter+0x20で一致する。
- `0x1322F0` はDrawInfo vptrを設定、+0x74/78/7Cを1.0、+0x80/84/88を0にし、+0x44へ単位3×4をコピー。`0x4B6154` の親なし行列・補正・alphaと `0x4B7CE0` の文字作業体読取りが独立した消費側。投影送出は [ACNL-F0693] [ACNL-F0696]。
- `0x5686D4` はnode+0x11Dを検査して専用IDを選択し、Drawer、内包Layout、DrawInfoを `0x4D7174` へ渡す。保存範囲は+0x104..110、最後にdirtyを0へ戻す。`0x5682DC` は+0x108>0で保存範囲を再生。ID・範囲・dirtyを混同しない。
- `0x56928C` はscreenに従い+4または+0x10のリストへ登録する。既存 [ACNL-F0694] が優先度とlink、[ACNL-F0693] が各パス・解除を独立に確認している。
- `0x1B71C4` は入力を保存せず状態getterから始まり、BaseObj draw、Scene、LayoutMgr_RenderTopへ進む。引数の無いFrame処理型である。戻りR0は早期終了getter/末尾処理で変わるため結果型は作らない。

## 反証条件・未確認点

- 管理者・文字作業体・Drawerは部分/不透明型で、全体の未知メンバーを命名しない。
- 投影modeの全Enum、全派生Layoutの追加欄、実フレーム順、省略・二重登録時の動作は今回追加確認していない。パス登録やGPU完了の実測は行っていない。
