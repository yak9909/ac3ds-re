---
id: ACNL-F0595
aliases:
- IDA-opus-5.5-F079
title: 'HHD の BFLAN を ACNL の BCLAN に変換できる（書き出しは ACNL の実物 727 本でバイト一致）・不透明度の伝播の旗（2026-10-05、HIGH: 実物との照合）'
summary: 解析モデル opus-5.5。段階 2 の遷移（開閉のアニメ）。
date: '2026-10-05'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4532-4545
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F079: HHD の BFLAN を ACNL の BCLAN に変換できる（書き出しは ACNL の実物 727 本でバイト一致）・不透明度の伝播の旗（2026-10-05、HIGH: 実物との照合）

解析モデル opus-5.5。段階 2 の遷移（開閉のアニメ）。

- 既存の道具: 3DSkit・Clypo に BCLAN の書き出しは無い。Switch Toolbox は GUI で BCLAN を編集・保存できるが、BFLAN からの変換は確認できず → `tools/hhd/clan_pack.py` を作った。
  検査: ACNL 更新版 romfs の Layout の arc の .bclan 739 本を acnl-ui-designer の read_clan で読み write_clan で書き戻し、**727 本バイト一致・不一致 0**（残り 12 本は
  pah1 区画を持つキーボードのアニメで対象外。HHD の出入りの BFLAN は pat1 / pai1 だけ）。
- FLAN（HHD v1.1、版 0x07020100）と CLAN（ACNL、0x02020000）の違い: pat1 のグループ名 36 B（CLAN 20 B）、pai1 の項目名 28 B（20 B）。情報・対象・キーの並びは同じ。印 FL** → CL**。
- 変換（make_acnl_layouts.py の convert_anims）: <src>_in / _out → hhd_<名前>_in / _out.bclan、ペイン名・グループ名はレイアウトと同じ規則（top_name）で付け替え、全部がレイアウトにあることを検査。
  HHD のグループ（grs1）もレイアウトへ写した（G_InOut / G_Kind / G_KindSex など）。
- **不透明度の伝播**: HHD の transmit alpha（ACNL のペインの旗 bit1 = influenced alpha、+0xB7 bit1）を写していなかったため、N_All の不透明度のアニメが子に効かなかった → 写すよう修正。
  静止画の比較値は変わらない。designer でフレームごとに描き、上画面は泡から吹き出しが膨らむ・下画面は地 → 目と色見本（フレーム 21〜23）→ ボタンの順に現れることを確認。
- gohan: GameLabel と同じ関数（AnimCtor / AnimLoad / FindGroup / GroupBind / AnimSetFrame / AnimStep / AnimFinished / GroupUnbind / AnimDtor）で開くとき in、閉じるとき out を再生（未実機）。

