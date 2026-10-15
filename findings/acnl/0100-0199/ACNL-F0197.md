---
id: ACNL-F0197
aliases:
- F-171
title: 'F-171: ★TextBox の描画は歩行中ゼロ。相乗り方式には大きな穴がある — `HIGH`（実機で計測）'
summary: '適用: `PATCHES/measure_textbox_draws.py`'
date: '2026-08-28'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4947404
- 5184740
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:10330-10389
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0201"]
---
## F-171: ★TextBox の描画は歩行中ゼロ。相乗り方式には大きな穴がある — `HIGH`（実機で計測）

適用: `PATCHES/measure_textbox_draws.py`

### 1. 測り方

2 つのケーブでフレーム単位の時系列を取った。

- **A: `0x4B7DCC`**（TextBox 1 枚の描画ごと）— 総数++、このフレームの数++、
  textbox ポインタをリング（64 件）へ
- **B: `0x4F1CE4`（`Render_FrameEnd`）** — フレーム数++、
  このフレームの数が 0 なら「ゼロフレーム」++、最大値を更新、
  **このフレームの数を 1 バイトでリング（256 件）へ**、作業カウンタを 0 に戻す

`Render_FrameEnd` は関数入口なので `R0-R3` は引数かもしれない。
`PUSH {R0-R3,R12,LR}` / `POP` で退避した。

### 2. 結果（25 秒、「UI が何も出ていない状態で村を歩き回る」）

```
総フレーム数 748          → 30 fps（ACNL の想定どおり）
総描画数     451
描画ゼロのフレーム = 627 / 748  (83.8%)
1 フレームあたり平均 0.60 枚、最大 14 枚
直近 256 フレーム（約 8.5 秒）は 256/256 すべて描画ゼロ
```

**歩行中は TextBox が 1 枚も描かれない。**
穴は散発的ではなく**まとまって空く**。

### 3. 検出された TextBox（14 種）

| pane | 何のとき |
|---|---|
| `S_itm_na` / `T_itm_na` | アイテム名 |
| `T_month` / `T_slsh` / `T_day` / `T_yobi` | 時計の日付 |
| `S_time_0` / `T_time_0` / `S_coron_` / `T_coron_` | 時計の時 |
| `S_minute` / `T_minute` / `S_time_a` / `T_time_a` | 時計の分・AM/PM |

**アイテム名と時計だけ。** どちらも常時は出ない。

### 4. 結論

**相乗り方式は「たまたま UI が出ている間」しか使えない。**
自前 GUI としては成立しない。

**TODO-115（TextBox に依らない発行点）は優先度の高い本当の課題である。**
F-170 で確認したとおり CTRPF に移しても解決しないので、
**自前のコマンドリストを組んで再生させる経路**（F-145 の list 32 と
`GpuCmd_ReplayRecordedListRange`、TODO-110 / TODO-112）へ進む必要がある。
F-166 で GPU 可視メモリは確保できるようになっているので条件は揃っている。

### 5. 手法として残しておく価値

**「総数」と「フレームあたり」を分けて数え、時系列をリングバッファに残す**設計は、
「効く／効かない」ではなく**いつ効くのか**を答えるのに向いている。
1 フレーム 1 文字で並べると変化の瞬間が目で見える。

---

