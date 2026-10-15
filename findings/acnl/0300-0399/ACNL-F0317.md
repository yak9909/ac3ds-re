---
id: ACNL-F0317
aliases:
- F-293
title: F-293 (HIGH・実機) — ★★★正規の手順で描けた。**自前の記録ケーブ 205 語を撤去**
summary: F-292 の設計を実装し実機で成功した。道具は `PATCHES/build_pane_tree.py`。
date: '2026-09-04'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10183936
- 5670612
- 5667776
- 9942788
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:18658-18727
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-293 (HIGH・実機) — ★★★正規の手順で描けた。**自前の記録ケーブ 205 語を撤去**

F-292 の設計を実装し実機で成功した。道具は `PATCHES/build_pane_tree.py`。
全文は `scratchpad/MEMO_f293_native_draw.md`。

**コードケーブを 1 語も足していない。`.bss` に nw::lyt のオブジェクトを組んだだけ。**

1. root Pane 2 個 / Picture 3 枚 / Material 3 個 / texMap 3 個を `.bss`（`0x9B6500`〜）に**自前で組む**
   （捕獲も複製もしない。boot 依存はアトラスの番地 1 つだけ）
2. Picture を root の循環双方向リストへ（番兵 = `root+0x14`、節 = `child+4`）
3. ノードの `+0x20` = root Pane、`+0x30` = DrawInfo の vptr
4. **vtable `+0x14` を CAVE_Q(`0x838200`) から `0x005686D4`（ゲームの `Layout_RecordPaneTree`）へ**
5. vtable `+0x18` も基底の `0x00567BC0` へ

### 実機の結果

- 上画面に 3 枚とも描かれた。**下画面の旧ケーブの残骸（白帯）も消えた**
- `list=44 記録長=0x3C0` / `+0x11D=0` / `+0x11F=1`
- 投影は `+0x38 = 2/240`、`+0x44 = -2/400` … **基底の SetupProjectionMatrix が正しく作った**
- UV キャッシュが保たれ `sub_73B650` は呼ばれていない

**★位置は画素単位で完全一致**

| 与えた値 | 期待 | 実測 |
|---|---|---|
| (120, 60) 60x40 | 中心 (320, 60) | **x 290..349 / y 40..79 / 中心 (320, 60)** |
| (120, -60) 60x40 | 中心 (320, 180) | **中心 (320, 180) / 60x40** |

F-290 の写像（`画面x = X + 画面幅/2` / `画面y = 画面高/2 - Y`、1 単位 = 1px）が
**正規経路・自前で組んだ Picture でもそのまま成立**する。

### ★色は頂点カラーで制御する — **F-280 の制約が消えた**

`mat+16`（reg 0x0DB）を赤にしても**変わらず**、
**`Picture+0x140` の頂点カラー 4 個**を赤／緑にしたら**そのとおりになった**。

理由: 自前マテリアルは **tevStage 数 = 0** なので `Material_EmitState` は既定雛形
（`0x97B704` の 18 語 = TexEnv3/4/5 のみ）を使う。その構成は
`TexEnv5 = Modulate(PrimaryColor, Previous)` で **PrimaryColor = 頂点カラー**が支配的。
F-289 段 3 で `mat+16` が効いたのは**借り物マテリアル（実 TEV 設定つき）**だったため。
**矛盾ではなく、マテリアル構成の違いによる帰結。**

→ **「色はチャンク（7 枚）単位でしか変えられない」（F-280）は完全に消滅。**
Picture ごとに `+0x140` を書けば 1 枚ずつ自由に色を付けられる。

### 消えたもの

**CAVE_Q 205 語** / 自前 TEV 36 語 / テクスチャ 7 組の手書き /
スプライトの手書きループ・色・カウンタ / チャンクと色の制約。
**残るコードケーブは A1・A2（ノード登録）と F・T（drawctx 記録）だけ。**

### 実機で動いた最小構成（`MEMO_f293_native_draw.md` 4 章に全欄）

要点だけ: Pane/Picture は `+0x14/+0x18` の自己参照、`+0x48/+0x4C` size、
`+0x80` の 3x4 行列、`+0xB5` alpha、**`+0xB6 = 0x14`（中央揃え）**、`+0xB7 = 1`（可視）。
Picture は `+0xD4=1` / `+0xD8=1` / `+0xDC..` UV / `+0x13C` Material / `+0x140` 頂点カラー。
Material は `+0x2C = +0x30 = 0x15`、`+0x34` ブロック、**`+0x4D = 0x04`**
（**bit1 を立てると `Material_EmitState` が早期 return して描画が止まる**）。

### F-293 追記 — ★ロード・操作を跨いでも正常（利用者確認）

利用者が実機でロードを跨ぎ、町で操作した結果 **「常に描画され、異常はありませんでした」**。
こちらの計測でも 25 秒連続で木・Picture とも健全、矩形の位置は寸分違わなかった。

★ただし **記録長は一定ではない**（0x3C0 → 0x440 と変動）。
`Material_EmitState` / `TextBox_UpdateDrawState` の状態キャッシュ次第で積む量が変わるため。
旧経路も同じ性質。リストは `0x8000` あるので余裕は十分だが、**容量は固定と仮定しないこと**。

---

