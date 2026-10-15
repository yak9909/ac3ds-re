---
id: ACNL-F0316
aliases:
- F-292
title: F-292 (HIGH・静的のみ) — ★F-291 を別関数で再検証（矛盾なし）。**正規の手順なら記録ケーブは丸ごと不要**
summary: 全文は `scratchpad/MEMO_f292_proper_way.md`。
date: '2026-09-04'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7588612
- 7588628
- 7588672
- 7582712
- 7583012
- 7588696
- 7583164
- 9438728
- 5669596
- 5670612
- 5667776
- 9438584
- 4951316
- 9438548
- 9420412
- 9420796
- 8388640
- 2097280
- 9421196
- 9379668
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:18539-18657
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-292 (HIGH・静的のみ) — ★F-291 を別関数で再検証（矛盾なし）。**正規の手順なら記録ケーブは丸ごと不要**

全文は `scratchpad/MEMO_f292_proper_way.md`。

### F-291 の独立な裏付け 7 件（矛盾 0）

| 検証に使ったもの | 分かったこと |
|---|---|
| Picture vtable スロット 10（`0x73CB04`） | `GetMaterial`: `this[0x13C]` を返す → **+0x13C = Material\*** |
| 同 スロット 3 / 7（`0x73CB14`/`0x73CB40`） | `this[0x140 + 4*i]` → **+0x140 = 頂点カラー 4 個** |
| Pane vtable スロット 10（`0x73B3F8`） | `return 0` → Material は **Picture 固有**（F-291 の「別途確保」と整合） |
| `nwlyt_Pane_DrawRecursive`（`0x73B524`） | vtable **`+0x68`（スロット 26）** を呼ぶ → **`0x73CB58` は `Picture::DrawSelf`** |
| `Pane::DrawSelf`（`0x73B5BC`） | `MOV R0,R1 / BX LR`（カーソルを素通し） |
| 子走査 | 番兵は **`pane+20`**、実体は節の 4 バイト前、可視は **`child[183] & 1`** |
| **本物の `ssys::ma::lyt::Layout` vtable（`0x900608`）** | **`+0x08=0x5682DC` / `+0x14=0x5686D4` / `+0x18=0x567BC0`** = **自前ノードの vtable と完全一致** |

**細かい訂正**: `+182(0xB6)` = basePosition（res+9）、`+183(0xB7)` = フラグ（**bit0 = 可視**、res+8）。
Picture vtable は 30 スロット、Pane は 28 スロット。

### ★正規の手順 — `Layout_RecordPaneTree` が読むのは 10 個ほどのフィールドだけ

```c
if (!this[0x11F]) { (vtable+0x18)(this); this[0x11F] = 1; }     // 投影
if (this[0x11D]) {
    GetProperty(519,&saved); SelectList(*(this+0x100));
    ClearCmdlist(); StartCmdlistSave();
    drawer = LayoutMgr_GetInstance()+868;  (drawer+0x0C)(drawer,1);   // DrawBegin1
    nwlyt_DrawPaneTreeToCurrentList(drawer, this+16, this+48);
    (drawer+0x14)(drawer,1);                                          // DrawEnd1
    CommitListAndCaptureDelta(this+0x104,+0x108,+0x10C,+0x110);
    SelectList(saved);  this[0x11D] = 0;
}
```

`nwlyt_DrawPaneTreeToCurrentList` は `root = *(layout+32)` を取り、
可視なら `nwlyt_Pane_DrawRecursive` を回して `g_GpuCmdPtr` へ書き戻すだけ。

**レイアウト側で必要な欄**: `+0x00` vtable / `+0x0C` 優先度 / **`+0x20` root Pane\*** /
`+0x28,+0x2C` 画面寸法 / **`+0x30` DrawInfo（`+0x34` が投影 16 語）** /
`+0x100` list id / `+0x104〜0x110` Commit 結果 / `+0x11D` 記録要求 / `+0x11F` 投影済み / `+0x134` display。

### ★結論 — CAVE_Q（205 語）は要らなくなる

自前の記録ケーブがやっていることは **`0x5686D4` の写し**である。
**vtable `+0x14` をゲーム自身の `0x5686D4` に向け、`+0x20` に自前の Pane 木を置けば、
記録ケーブは丸ごと不要**になる。必要なのは「オブジェクトを正しく組むこと」だけで、
**描画のためのコードケーブは 1 語も要らない。**

木は循環双方向リスト。番兵は `root+0x14` そのもの、実体は節の 4 バイト前、
可視は `child[0xB7] & 1`。root の `DrawSelf` は本物の Pane vtable を使えば素通しになる。

### 未確定

- **DrawInfo（`+0x30` 以降）の中身は投影行列以外まだ不明。**
  `Picture::DrawSelf` は DrawInfo を**使っていない**ので Picture だけなら問題ないが、
  TextBox / Window を使うなら要調査。
  （設計メモの「a3 はデッド」は **Picture の実装に限った話**で、契約ではない。）
- `nw::lyt::Pane` 単体の確保サイズは工場関数から読めなかった（Picture 344 / TextBox 264 は確定）。
- `nw::lyt::Layout` / `DrawInfo` / `Drawer` / `Group` は **RTTI 名だけで vtable が無い**。
  `DummyLayout`（vtable `0x900578`）が `nw::lyt::Layout` を継承し、
  スロット 16 が `nwlyt_BuildPaneByKind`（`0x4B8D14`）＝ペイン生成の仮想。

### F-292 追記 — ★実機で全結論を検証した。**矛盾ゼロ**

一度も触っていないゲーム自身のレイアウト（`0x3225B070`）を読んで突き合わせた。

**当たった予測**

- `mgr+0x04 = 0x00900554` … 静的に「LayoutList の vtable」と予測した番地そのもの
- レイアウトの `+0x0C` 優先度 / **`+0x20` root Pane** / `+0x28,+0x2C` = **400.0, 240.0** /
  **`+0x30` = DrawInfo の vptr**（typeinfo 名 = `N2nw3lyt8DrawInfoE`）/ `+0x100` list id /
  `+0x104`〜`+0x110` Commit 結果 / **`+0x11D` 記録要求 = 0** / **`+0x11F` 投影済み = 1** / `+0x134` display
- `+0x10 = 0x00900578` = **`DummyLayout` の vtable**＝ `nw::lyt::Layout` 部分オブジェクトの vptr
- Pane 木を**予測どおりの規則で歩けた**（番兵 = `pane+0x14`、実体 = 節の 4 バイト前）

```
RootPane(Pane 400x240) → N_bg(Pane) → P_base_L/R(Picture) → P_icon_L/R(Picture)
```

- root の vtable = `0x008FBE7C`（`nw::lyt::Pane`）/ Picture = `0x008FBFFC` … 静的特定と一致
- RootPane の `+0x48` size = **(400, 240)** ＝ 画面
- **`+0xB6` basePosition = `0x14`（下位ニブル 4 = 中央揃え）** → アンカー `(-幅/2, +高さ/2)`。
  「行列の平行移動が矩形の中心」という読みが裏付けられた
- `+0xB7` bit0 = 可視 / `+0xB8` 名前 = `'RootPane'`

**★TexMap の式を触っていない実データで検証（`P_base_L`）**

```
+0x04 = 0x1804BF80  +0x08 = 0x00800020  +0x0C = 0x00800020
+0x10 = 0x00000290  +0x14 = 6  +0x18 = 0x00200080  +0x1C = 9
```

| 検証 | 式 | 実測 | 結果 |
|---|---|---|---|
| 1 | `ROR32(+0x0C,16)` = `0x00200080` | `+0x18` | **一致** |
| 2 | 書式表`[(+0x10>>8)&0xF]` = 表`[2]` = 9 | `+0x1C` = 9 | **一致** |
| 3 | UV 倍率 = 32/32, 128/128 | 1.0, 1.0 | 整合 |

**「nw::lyt 書式 2 = LA4(PICA 9)」が実データで確定。**
マテリアルも vtable `0x008FC18C` 一致、**色 7 個**、`+0x30 = 0x15` →
texMap 1 / texSRT 1 / texCoordGen 1（bits0-1 / 2-3 / 4-5）で**ビット割りが的中**、
名前 `'P_base_L'`、`+0x4D` bit2 が落ちている（未描画）ことも `+0xD4/+0xD8` = 0 と整合。

### 新しく分かった 3 点（いずれも結論を否定しない）

1. **実物は `ssys::ma::lyt::Layout` の派生 `6Layout`**（vtable `0x8F1F54`、typeinfo `0x8C65F0`）。
   `+0x08/+0x0C/+0x10` は基底と一致するが、**`+0x18`（投影）を `0x5BE984` で上書き**している
   （そこからは `0x73BAC0` を呼び、基底の `0x567BC0` は呼ばない）。
   **我々のノードは基底の `0x567BC0` を使っており、それで 400x240 の投影が正しくできている。**
2. 派生の `+0x14` は **`0x5686D0`**。実機で見ると `0xE1A00000`（`MOV R0,R0` = 整列 NOP）で
   `0x5686D4`（`PUSH {R3,R4,R5,LR}`）へ落ちるだけ。
   **`Layout_RecordPaneTree` を `0x5686D4` として読んだのは正しい。**
3. **Material の位置は「偶然」ではなく規則的** — 4 つの Picture すべてで **Picture + 416 (0x1A0)**。
   F-291 の「確保が隣接しただけ」という表現を訂正する
   （Picture 344 バイト＋72 バイト＋Material 80 バイトの順に確保される）。
   **「Material は Picture の一部ではない」という結論は変わらない。**

---

