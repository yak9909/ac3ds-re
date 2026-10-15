---
id: ACNL-F0349
aliases:
- F-323
title: 'F-323（2026-09-07）: パネルの縁がフェード途中で濃く残る（A案で修正）'
summary: '**confidence: MEDIUM**（静的根拠 + 検証器 + プレビュー + ビルド。**実機の目視は未確認**）'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21353-21394
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-323（2026-09-07）: パネルの縁がフェード途中で濃く残る（A案で修正）

**confidence: MEDIUM**（静的根拠 + 検証器 + プレビュー + ビルド。**実機の目視は未確認**）

利用者の報告:「リストボックスや適用ダイアログなど、背景+縁取りパネルの
登場・退場で透明度が変わるとき、縁取りだけ濃く出る」。

### 原因

`GuiMenu.cpp` の `Frame1px()` が「外枠フル + 内地フル」の 2 枚重ねだった。
内地の範囲は縁の上に背景を重ねてブレンド（二重）するので、
`Fade()` で両方のαを掛ける現方式は「合成してからフェード」と一致しない。
縁（α 0.9〜不透明）と地（α 0.82）の比が `amount` で変化し、縁だけ残る。
Simulator（`app.js`）は `fillRect` + `strokeRect`（縁が地の上に乗る）で、
重ね順も逆だった。

### 直し（A案。色比は残し、二重だけ消す）

縁 4 辺と内地 1 枚の 5 枚・重なりゼロにした。各画素が単一層なので、
層ごとのフェード == 一枚絵のフェードと等価になる。
不透明時は同じ絵。`Outline()` が既にこの形だった。

```
Frame1px: 外枠フル+内地フル(重なる) -> 縁4辺+内地(重ならない)
```

w <= 2 / h <= 2 の潰れた寸法だけ旧経路（FillRect が非正を捨てるため）。

### 予算

`Frame1px` 2 枚 -> 5 枚（+3/箇所）。説明+インライン+ダイアログが
同時に開く最悪値 34 枚に合わせ `GuiV2.cpp` の `kMaxRect` 24 -> 36、
`kMaxRectAll` 48 -> 72。借用 370,176 B / 393,216 B（94%）、
記録 上 68,928 B / 78,643 B（87%）・下 10,752 B / 26,214 B で収まる。
`verify_plugin_port_v2.py` 8 群 0 件、`verify_spec_v2.py` 8 群 0 件、
`preview_menu.py --sel 3` 出力、`gohan.3gx` 再ビルド済み。

### 実機で確かめること

インラインリスト・ダイアログ・説明パネルの開閉途中で縁が浮かないこと。
メインメニューの地・縁・帯は `Fade` なし（スライドのみ）なので対象外。

