---
id: ACNL-F0518
aliases:
- IDA-opus-5.5-F013
title: 役場・リサイクルショップも集め方どおり全体が青。全段使用の材質は近似、モデルビューアは汎用の書き出し（2026-09-23、HIGH（役場・店）／MEDIUM（モデルビューア、静的））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「役場とリサイクルショップで確かめる」「使われている材質への対応」「モデルビューアの自前モデル」。'
date: '2026-09-23'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:2548-2581
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F013: 役場・リサイクルショップも集め方どおり全体が青。全段使用の材質は近似、モデルビューアは汎用の書き出し（2026-09-23、HIGH（役場・店）／MEDIUM（モデルビューア、静的））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「役場とリサイクルショップで確かめる」「使われている材質への対応」「モデルビューアの自前モデル」。
道具 `tools/models3d/tint_building.py`（survey / apply / restore、F012 の集め方を実装。元値 `work/evidence/models3d/tint_building_state_office.json`）。

### 1. 集め方（F012）の結果

- 役場（0x50、AcStrcOffice、ブロック 0x4D8）: 子プロセス無し、SkeletalModel 2 個（材質 2 + 1）
- リサイクルショップ（0x58、AcStrcRecycleShop、0x5F4）: 子プロセス 2（看板・営業時間の会話 AcSimpleTalk、モデル無し）、SkeletalModel 2 個（材質 3 + 1）
- どちらも SimpleMaterialActivator → 汎用へ差し替え

### 2. 6 段すべて使う材質（7 材質中 5）

形は共通: 段 3 がバッファを更新（更新語 0x900）、段 4 = `0x033F0FE4` Modulate（テクスチャ 1 × 定数色、**倍率 2 倍**）、
段 5 = `0x033F0DEF` オペランド 0x20 MultiplyAdd（前段 × 定数色アルファ（0xFF）＋ 前段バッファ）。= **下地（段 3）＋ 光る部分（テクスチャ 1 × 色 × 2）**。
段 4 の倍率 2 倍が出力全体に掛かるため段 4・5 を 1 段に正確にはまとめられない（1 段の定数色は 1 つ、演算は 3 入力 1 式）。
→ **近似**: 段 5 を `MultiplyAdd(バッファ, 1 − 定数.a, 定数)` に置き換え、Constant5 に 青 × 強さ（前乗算）を入れる = lerp(下地, 青, 強さ)。
ハイライト中は光る部分（夜の役場の窓明かり、リサイクルショップのハートの看板）が消えて青になる。戻せば元どおり光る。

「段を詰める」方法（段 k が素通しなら k+1..5 を 1 つずつ前へ。ヘッダは位置に残す。更新ビットが k..4 で 0 のときだけ）も実装したが、今回の材質では該当なし。

### 3. 実機（画像 `work/evidence/screens/tint_20260923/office_{b0,restored}.png`）

- **役場とリサイクルショップの本体が全体に薄い青**。近似の材質と段 5 が空いている材質の見分けはつかない
- 役場前の**旗（紫の布）は青くならない** → 役場の実体とその子プロセスの外（別のオブジェクト）。選択表示に含めるかは未決
- restore で窓明かり・看板の光を含めて元どおり（29 か所）

### 4. モデルビューアの自前モデル（静的）

`sub_4A9A04`（モデル生成の最後）が書き出し関数を選ぶ: **作成情報 +16 が 0 か 0x1000 なら SimpleMaterialActivator（`sub_4A1780`）、それ以外は汎用（`sub_49C054`）**。
作成情報 +16 は `ModelInstance_Create` の第 5 引数（材質の複製マスク、既存 V2-F023）。gohan のモデルビューアは **0x834 → 汎用**（木は 0 → 簡易版で F002 と一致）。
0x834 は 0x800（本体＝色の部分をインスタンスごとに複製）を含み、0x780（TEV）を含まない → TEV は gohan が読んだ自前の資源のもの。
描画は `Submit(scene 0)` でゲームの通常経路 → 同じ方法で色を変えられるはず。**実機は未確認**（モデルビューアを出していない）。建物エディターの設置プレビューで確かめる。

