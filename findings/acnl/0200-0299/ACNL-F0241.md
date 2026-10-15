---
id: ACNL-F0241
aliases:
- F-216
title: 'F-216: ★★★★★`reg 0x082` は `(幅<<16)|高さ`。正方形しか試していないと気付けない — `HIGH`（実機）'
summary: 自前 GUI はずっと `((TEX_H << 16) | TEX_W, 0x082)` と書いていた。
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:13029-13063
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-216: ★★★★★`reg 0x082` は `(幅<<16)|高さ`。正方形しか試していないと気付けない — `HIGH`（実機）

自前 GUI はずっと `((TEX_H << 16) | TEX_W, 0x082)` と書いていた。
**64x64 の正方形アトラスしか使っていなかったので、逆でも同じ値になり気付けなかった。**

TODO-130 で SD から任意の画像を読めるようにし、64x32 のテクスチャを貼ったところ
**「乱れている。単純なズレではない」**という見え方になった。
`(幅<<16)|高さ` に入れ替えたら直った。

```
reg 0x082 = (幅 << 16) | 高さ      ★これが正しい
```

### 切り分けの手順（そのまま再利用できる）

1. **タイル化を実機抜きで検算した。**
   動作実績のあるフォントアトラス（`PATCHES/font_atlas_64x64_la4.bin`）を
   自分の Morton 関数で**逆タイル化**したところ、`A C N L` と `K` が綺麗に出た。
   -> 並べ替えは正しい。疑いは形式か寸法へ絞れた。
2. **正方形（64x64 RGBA8）で試した。** 完璧に出た。
   -> RGBA8 の経路も正しい。**残るのは非正方形の扱いだけ**。
3. 非正方形で `(幅<<16)|高さ` に入れ替えて確認 -> 直った。

**★「正方形でしか試していない」ことに自覚的でないと、
この手の対称な誤りは何ヶ月でも残る。**
対称性のある値（幅と高さ、X と Y、u と v）は、**必ず非対称な入力で試す。**

### 影響範囲

`cave_draw_topmost.py` を修正し、プラグインと検証スクリプトも合わせた。
`cave_add_sprite2.py` / `cave_draw_sprites.py` / `cave_own_batch.py` は
64x64 の正方形しか使わないのでそのままだが、**注意書きを入れた**。

---

