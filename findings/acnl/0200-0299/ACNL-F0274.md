---
id: ACNL-F0274
aliases:
- F-251
title: 'F-251: 合成の 4 つの欠陥を実機との聴き比べで修正 — `HIGH`（利用者が実機一致を確認）'
summary: 全件バッチの成果物を聴いた利用者が 3 件の異常を報告し、そこから 4 つの欠陥が出た。
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:14616-14667
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-251: 合成の 4 つの欠陥を実機との聴き比べで修正 — `HIGH`（利用者が実機一致を確認）

全件バッチの成果物を聴いた利用者が 3 件の異常を報告し、そこから 4 つの欠陥が出た。
修正版（`B_zenbu`）が実機一致と判断された。

### (1) テンポ命令が初期値に負けていた

テンポ命令は tick 0 にあり、初期値 `(0.0, 120.0)` と同じ位置に積まれる。
`sorted(tempo_ev)` はタプルごと比較するので、**値の大小で初期値が後ろに回り 120 が勝つ**。
`SEQ_BGM_FNFR_GET` は tempo 70 が無視されて **1.71 倍速**で鳴っていた。
tick だけを鍵にした安定ソートへ変更。**初期テンポが 120 未満の 376 件**が該当。

### (2) 音量変更が鳴っている音に段差として当たっていた

`SE_SYS_PUBLIC_SET_PLACE` の末尾は `volume 30` → `10` の残響で、
倍率が一瞬で 1/9 になりプツッと鳴っていた。最短 4ms かけて動かす（`render.MIN_RAMP`）。

**適用条件を 2 段階で絞る必要があった**（絞らないと確認済みの音を壊す）:
- 次のイベントまで 4ms 未満なら鈍らせない
  → `WIN_TEXT_CLOSE` は tick 0 に音量イベントが 3 つ重なっており、1.4dB ずれた
- **その音が鳴り始める前（相対位置 <= 0）の音量は「始まりの音量」**なので鈍らせない
  → `DECIDE` / `MAP_LIST` の立ち上がりが甘くなっていた

### (3) 波形と包絡が 1 サンプルで 0 になっていた

`build_env` は release が 0.0005 を切ると `break` して残りを 0 のまま残す。
合成ループも `if ip >= ns: if not loop: return` で波形を断ち切る。
どちらも直前 2ms を直線で落とすようにした（`render.END_FADE`）。

### (4) `loop_start 0` を「1 回だけ」と解釈していた

`SE_SYS_BOOK_INSECT_MOSQUITO` は `note[127,0]` のあと
`loop_start[0]` … `loop_end` で pitch_bend と volume を揺らし続ける作り。
1 回で抜けると外側の `jump` が `volume 10` と新しい `note` を実行し、
**止まって鳴り直す**ように聞こえていた（利用者の報告と一致）。
**回数 0 は無限**（データ中 75 箇所。1 回だけなら書く意味がない）。
打ち切りは `visits` / `LOOP_LIMIT` が受け持つ。影響 46 件。
MOSQUITO は 8 個の鳴り直し → 1 個の持続音になった。

**比較のために構造の違いを押さえておく**:
蝉 `ABURAZEMI` は `note` → `jump` で同じ note へ戻るだけ（重なって繋がる）。
こちらは修正の影響を受けず、利用者も実機一致と確認している。

### 長さ 0（ノートオフ無し）＋ループ波形

`note [80, 0]` は長さ 0 = ノートオフ無し。該当 151 件。
`SE_SYS_BOOK_INSECT_*`（虫の声）や `SE_FUR_*`（家電）など**鳴り続けるのが正しい音**が
含まれるため、一律にワンショット化してはいけない。蝉が実機一致なので `hold` を維持。
`SE_SYS_AMIIBO_CAMERA_LIGHT_NORMAL` だけは正解不明のまま（TODO-139）。

---

