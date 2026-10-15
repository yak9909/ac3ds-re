---
id: ACNL-F0267
aliases:
- F-244
title: 'F-244: seq 型サウンド 2,839 件を WAV に合成 — `MEDIUM`（構造は HIGH、包絡の時定数は近似）'
summary: '`SOUND/synth.py` + `SOUND/render.py`。CSEQ を実行してボイスを取り出し、'
date: '2026-09-01'
category: sound
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:14309-14351
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-244: seq 型サウンド 2,839 件を WAV に合成 — `MEDIUM`（構造は HIGH、包絡の時定数は近似）

`SOUND/synth.py` + `SOUND/render.py`。CSEQ を実行してボイスを取り出し、
CBNK で program -> 波形・原音キーを引き、CWAR の CWAV を音程変化させて包絡を掛けて混ぜる。
出力は `SOUND/out/seq_wav/<分類>/<名前>.wav`（2,839 本 / 100.2 分 / 741 MB）。

### 素朴に鳴らすと実機と別の音になる（利用者の指摘から判明）

`SE_ACT_ITEM_CMN_PICK_UP` と `SE_ACT_SCOOP_DIG_OUT_ITEM` が違うとの指摘で発覚した。

| 命令 | 何が起きるか | BGM 除く 3,365 件中の使用率 |
|---|---|---|
| `tie` (0xC8) | ON の間、続く note を**鳴らし直さない**。音程だけ変わる | 12.5% |
| `porta_key` (0xC9) | ポルタメント。**`porta_time`=0 なら「その音符の長さ」で滑る** | 14.6% |
| `attack/decay/sustain/release` | 音量包絡 | 23.7 / 10.8 / 18.5 / 28.5% |
| variable 接頭辞 (0xA1) | 最後の引数は**値ではなく変数番号**。`ex` sub 0x80 が代入する | — |

- `SE_ACT_ITEM_CMN_PICK_UP` は `porta_key 33` → `note 83` の上昇スイープだった
- `SE_ACT_SCOOP_DIG_OUT_ITEM` は `tie 1` で 9 個の note が 1 つの音として繋がる。
  鳴らし直すと 9 回アタックが入って別物になる
- **note の長さ 0 = ノートオフ無し**（サンプル終わりまで鳴る）。
  1 と誤ると `SE_ACT_SCOOP_DIG_IN` が無音になる
- **包絡の既定値は楽器側（CBNK の葉 `+0x28` attack / `+0x29` decay / `+0x2A` sustain /
  `+0x2C` release、いずれも 0..127 で既定 127）**

### 見送った 526 件は正当

`note` を 1 つも持たない制御用シーケンスが 521 件。
`SE_MELODY_*` 489（村メロ = 実際の音符はセーブデータ側）、
`SE_MU_CTRL_*` / `SE_DJ_CTRL_*`（音楽プレイヤーの制御）など。

### 確定していないこと

- **包絡の時定数は近似。** 0..127 -> 速度の変換は任天堂系で共通の形
  （127 = 即座、下げるほど急に遅い）を使ったが、実機の変換表そのものではない。
  耳で確かめて調整する余地がある
- `ex` の sub の**意味**（0x90 / 0x95 等）は未確定。引数長は確定したので復号は正しく、
  条件分岐の判定だけが近似。変数分岐に依存する音は経路が実機と異なりうる
- 合成結果のうち 46 本 (1.6%) が無音同然。未調査


---

