---
id: ACNL-F0315
aliases:
- F-291
title: F-291 (HIGH・静的のみ) — ★正体は **nw::lyt（NintendoWare Layout）**。Picture / Material の構造を静的に確定し、**既存文書の誤り 6 件を訂正**
summary: '`code.bin.i64` だけで詰めた（動的解析なし）。全文は `scratchpad/MEMO_f291_nwlyt_static.md`。'
date: '2026-09-04'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9420796
- 9420412
- 9421196
- 4951316
- 4942168
- 4954160
- 4194432
- 8388672
- 7583172
- 7583280
- 4958824
- 4942680
- 4968104
- 7589888
- 7590048
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:18446-18538
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-291 (HIGH・静的のみ) — ★正体は **nw::lyt（NintendoWare Layout）**。Picture / Material の構造を静的に確定し、**既存文書の誤り 6 件を訂正**

`code.bin.i64` だけで詰めた（動的解析なし）。全文は `scratchpad/MEMO_f291_nwlyt_static.md`。

### 正体（RTTI）

| vtable | マングル名 |
|---|---|
| `0x008FBFFC` | `N2nw3lyt7PictureE` = **`nw::lyt::Picture`** |
| `0x008FBE7C` | `N2nw3lyt4PaneE` |
| `0x008FC18C` | `N2nw3lyt8MaterialE` = **`nw::lyt::Material`** |

継承は **`Picture` ← `Pane` ← `internal::PaneBase`**。
我々が叩いているのは ACNL 固有ではなく**任天堂の nw::lyt 標準構造**。

### ★訂正 1 — `Picture` は **344 バイト (0x158)**

ペイン工場 `0x4B8D14` が種別ごとに確保サイズを決めている
（Picture 344 / TextBox 264 / 他 364・212）。
文書の「実体は約 `0x320` バイト」は**誤り**。
`0x320` は `pic+0x004` が `pic+0x328` を指すことからの推測だったが、
**あれは隣の別ペインを指す連結リストのポインタ**だった。

### ★訂正 2 — `+0x80` の行列は一次データではない

`0x4B6958` が **`+0x50` と `+0x80` の両方を単位行列に初期化**する。
一次は `translate(+0x28) / rotate(+0x34) / scale(+0x40)`、`+0x80` はそこから計算される世界行列。
我々が `+0x80` を直接書いて動くのは、**クローンがレイアウト木に無く誰も再計算しないから**。
形式は 3 行 x 4 列・行優先、平行移動は各行の第 4 列（`+0x8C`=X / `+0x9C`=Y / `+0xAC`=Z）。

### ★訂正 3 — `Material` は**埋め込みではない**（80 バイトを別途確保）

`Picture` の ctor が `sub_4B8CF0(80, 4)` で確保して `+0x13C` に入れる。
実機で `pic+0x13C == pic+0x1A0` に見えたのは**確保が隣接しただけ**。
F-289 の「Picture を複製すればマテリアルも自分のものになる」は
結果としては成立するが**理由が違う**。

### ★訂正 4 — 「0x400 複製＋自己参照 25 個の張り替え」は原理的に誤り

0x400 は `Picture(344) + Material(80) + 座標配列 + **隣のペインの一部**`。
張り替えた 25 個には**正当に外を指すポインタ（連結リストの前後）が混ざっていた**。
偶然動いていたに過ぎない。本番は**必要なフィールドだけを組み立てる**べき。

### ★訂正 5 — `mat+16` / `mat+20` は「色配列 7 個の [0] と [1]」

`Material` ctor は `+0x10` から **u32 の色を 7 個**書く。
`Material_EmitState` が `*(mat+48) & 3`（= **texMap 数**）で分岐してどれを出すかを決める。

### ★訂正 6 — TexMap の `+0x14/+0x18/+0x1C` は**派生キャッシュ**

`nwlyt_TexMap_UpdateGpuRegs`(`0x4B9830`) が `+0x0C`/`+0x10` から作り直す。

```
+0x00 ?          +0x04 ★テクスチャ番地
+0x08/+0x0A 使う幅・高さ      +0x0C/+0x0E 全体の幅・高さ
+0x10 ★bits0-1 wrapS / 2-3 wrapT / 4-6 minFilter / bit7 magFilter / bits8-11 書式
--- 以下は派生 ---
+0x14 reg 0x083   +0x18 reg 0x082 = ROR32(+0x0C,16)   +0x1C reg 0x08E（書式表で写像）
```

書式表: `0->7 1->8 2->9 3->5 4->6 5->3 6->1 7->2 8->4 9->0 A->12 B->13 C->10 D->11`
→ **LA4(PICA 9) は nw::lyt 書式 2**。実測の `+0x1C=0x0D` は nw::lyt 書式 `B` 由来。

数値検証（スクリプト）: `ROR32(0x00400080,16) = 0x00800040` = 実測の `+0x18` と一致。
`+0x0C` 下位 u16 = 128（幅）/ 上位 = 64（高さ）で、元の Picture が 128x64 なのと整合。

**我々が `+0x14/+0x18/+0x1C` を直接書くやり方は動くが、
`sub_4B9830` が呼ばれた瞬間に消える「その場しのぎ」である。**
本来は `+0x04 / +0x08..+0x0E / +0x10` を書いて `sub_4B9830` を呼ぶ。

### Material の可変長ブロック（取得子の実装から確定）

`*(mat+52)` から `texMap[]32B → texSRT[]20B → texCoordGen[]4B → tevStage[]12B → alphaCompare8B → blendMode4B`。
個数は `*(mat+48)` の bits0-1 / 2-3 / 4-5。

### ★アンカーの旧コメントを訂正

`nwlyt_Pane_GetAnchorOffset`(`0x73B5C4`) は
`code = pane[0xB6] & 0xF`、横 `code%3`（0→0 / 1→-幅/2 / 2→-幅）、
縦 `code/3`（0→0 / **1→+高さ/2** / 2→+高さ）。
**IDB の旧コメントは「1 → 高さ*0.5」の分岐を書き落としていた**（`0x73B630` に実在）。
中央揃え（code=4）なら `(-幅/2, +高さ/2)` となり、
**行列の平行移動がそのまま矩形の中心**になる。
これが F-290 で実測した `screen_x = X + 画面幅/2` の内訳の片側（もう片側は投影）。
→ **雛形は `+0xB6` の下位ニブルを 4 に明示すること。**

### IDB へ反映済み

`0x4B8D14` / `0x4BAA68` / `0x4B6B58` / `0x4B6958` / `0x4B9830` / `0x4BCEA8` /
`0x73B5C4` / `0x73D000` / `0x73D0A0` に上記をコメントとして記入し保存した。

---

