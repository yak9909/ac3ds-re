---
id: ACNL-F0203
aliases:
- F-177
title: 'F-177: ★★★`nwlyt_Pane_DrawRecursive` は 1 フレームも欠けない。TODO-115 の答え — `HIGH`（実機で計測）'
summary: '適用: `PATCHES/measure_pane_draws.py`'
date: '2026-08-28'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7583012
- 7589704
- 7588696
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:10788-10857
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-177: ★★★`nwlyt_Pane_DrawRecursive` は 1 フレームも欠けない。TODO-115 の答え — `HIGH`（実機で計測）

適用: `PATCHES/measure_pane_draws.py`

### 1. 経緯 — ユーザーの観察が正しかった

F-175 で Picture のゼロフレームが 1.1% あり、
「ロード中でも通知を出したいので、常に描ける手段が要る」という要求が出た。

**ユーザーの観察**: 建物の出入りで、直後は真っ暗で何も描かれないが、
**しばらくすると「ロード中」を示す画像が表示される**。
「それは毎フレーム必ず実行される描画箇所の存在を示すのでは」

**そのとおりだった。**

### 2. 見落としていた手がかり

F-175 の計測で **Pane 走査 161251 回に対し Picture 描画 65315 回**、
つまり **2.5 倍の差**があった。Picture 以外の Pane 型が描かれている証拠が
既に手元にあったのに、Picture のゼロフレームだけを見て結論しかけていた。

### 3. 計測結果（60 秒。建物の出入り・メニュー開閉を含む）

```
総フレーム数 = 1785

           総数     ゼロフレーム   ゼロ率   最大/フレーム
Picture   23825         59        3.31%        80
Pane      68739          0        0.00%       258
```

**`nwlyt_Pane_DrawRecursive`(`0x73B524`) は 1 フレームも欠けない。**

時系列が完全に対応する:

```
Picture: 1............222221111...   12 フレーム連続でゼロ
Pane:    +999999999999+++++++++...   ちょうどその区間で 9
```

**Picture がゼロの区間で Pane は 9 枚描かれている。**
これがユーザーの言う「ロード中を示す画像」であり、
**ロード画面は Picture ではない Pane 型で描かれている。**

### 4. 結論 — TODO-115 の相乗り点が確定した

| 経路 | 関数 | ゼロフレーム |
|---|---|---|
| TextBox | `sub_73CF48` (`0x73CF48`) | 83.8%（F-171） |
| Picture | `nwlyt_Picture_DrawToCommandList` (`0x73CB58`) | 3.3%（本項） |
| **Pane 走査** | **`nwlyt_Pane_DrawRecursive` (`0x73B524`)** | **0.00%** |

F-147 より、この関数は cursor を `R1` で受け取り、各 Pane の draw slot(+0x68) へ渡し、
戻り `R0` を次の可視 child へ渡す。**UI command stream を伸ばす走査本体そのもの。**

**「いついかなる時も描ける」要件を満たす。**

### 5. 教訓 — 3 度目の同じ失敗

F-171 で TextBox を測って「相乗りは不可」と一般化しかけ、
F-175 で Picture を測って「1.1% の穴は許容」と結論しかけた。
**どちらも、隣の経路を測れば済む話だった。**

しかも **F-175 の時点で「Pane 走査が Picture の 2.5 倍」という
反証データが自分の出力の中にあった。**

**総数の内訳に差があったら、その差自体を次の仮説にすること。**

---

