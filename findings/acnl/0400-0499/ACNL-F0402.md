---
id: ACNL-F0402
aliases:
- F-375
title: 'F-375（2026-09-08）: タイトルで即クラッシュ — 空リスト＋陳旧リンクの永久スキップ'
summary: 利用者の申告： タイトル画面で自前メニューONにしただけで動かなくなる。
date: '2026-09-08'
category: system
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 5664260
- 10178816
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24164-24205
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-375（2026-09-08）: タイトルで即クラッシュ — 空リスト＋陳旧リンクの永久スキップ

利用者の申告： タイトル画面で自前メニューONにしただけで動かなくなる。
実機値： PC=`0x00566E04`（`LDR R1,[R0,#8]`。`RenderTop`+0xC）、R0=`0x0`、
R4=`0x32FF7910`（正常）。`[mgr+4]`（head）が 0 のままだった。
フォールトではなく停止に見えたが、利用者の申告（Resume 不可・
デタッチでクラッシュログ）を正とし、フォールトとして扱った。

### 機序（証拠完備）

- 自前ノード（`0x009B5100`）は prev=`0x32C4CBCC`（死んだリストの残骸）、
  next=0、優先度 `0xFF` で、**別の死んだリストに残っていた**。
- `build_a` の見送り条件 (b)（prev != 0）が真になり、挿入を永久に見送る。
  前提「外れたら prev/next は 0 に戻る」は、UnlinkAll されない
  死んだリストには効かない。
- 対象（タイトル上リスト）は空（head=0）のまま。
- `LayoutMgr_RenderTop` の +0x00〜+0x14 に空検査は無い
  （PUSH / MOV / LDR / LDR / ADD / BLX）。head=0 → +0x0C で落ちる。
- 村では起きない（リストが詰まっているため）。タイトル初回テストで発覚。

### 対策（`PATCHES/cave_node_record.py` の `build_a`）

対象 head（`tail_off - 8`＝上 +4／下 +0x10）== 0 なら、
自前ノードはその中にいないので stale prev/next を消して挿入へ直行。
非空なら従来の (a)(b)(c) のまま。正常系の振る舞いは不変。

### 配置の修正（副作用）

A1 が 94 語へ伸びて A2/N と重なった（監査で検出）。
M/B/U/F/T（退役含む）は動かさず、A2=`0x00838CE8`・N=`0x00838CF0` へ。
A1 は据え置き（RenderTop 側の分岐語が変わらない）。
※監査は clear_mat=True 版（94 語）で見る。実機は False 版（89 語）。

### 検証

`export_gui_v2.py` 再生成 → `audit_node_cave.py` 0 件 →
`verify_literals.py` 0 件 → objdump で分岐先・リテラルを目視 →
ビルド → 検証器 2 種 0 件 → プレビュー。

実機で見ること： タイトルでチートON（メニューが自動で開く）→
落ちずにメニューが出ること。しずえ画面への遷移も含めて再試行。

