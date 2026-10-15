---
id: ACNL-F0553
aliases:
- IDA-unknown-F029
- V2-F029
title: 行列経路は正常だった。残る差は node+0x228 / +0x22C（2026-09-19、HIGH、実機＋対照）
summary: 設計（`docs/topics/unit_cursor_hw_plan.md` §9）→ 検証（51 件 ok）→ 実装 → 検査（0 failed）→ 適用の順で測定した。
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4141-4156
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F029: 行列経路は正常だった。残る差は node+0x228 / +0x22C（2026-09-19、HIGH、実機＋対照）

設計（`docs/topics/unit_cursor_hw_plan.md` §9）→ 検証（51 件 ok）→ 実装 → 検査（0 failed）→ 適用の順で測定した。

**(1) 仮説「行列がシェーダへ届いていない」は棄却**。`sub_48D34C` は `reg 0x02C0`（VSH の float 定数）へ 3x4 行列を積み、行列は `model+544` の行列プールから来る。プールを更新する `sub_4EF624` は `node+561`（`LDRB R0,[R4,#0x231]`）が 1 なら何もせず帰る。実機では **`node+561 = 0`**（＝更新は飛ばされない）、`node+544` は有効、`pool+24 = 0`。識別しやすい平行移動 (1111, 2222, 3333) を設定して `UpdateWorldAndSkeleton` を呼ぶと、**`node+0xBC` のワールド行列にその値が正しく入った**。

**(2) 「行列プールが空」も棄却（対照で）**。プールが持つ 2 本のベクタは `{alloc, alloc, begin, end, capacity}` 形式で `begin == end`、すなわち要素 0 だった。しかし**いまゲームが実際に描いている 3 つのモデル**（0x3054AF88 / 0x30898058 / 0x30887A68、いずれも同じ `nw::gfx::SkeletalModel`）も **gate=0・begin==end・要素 0 で我々と同一**。よって空であること自体は正常で、原因ではない。**対照を取らずに「空だから異常」と書かなくて済んだ。**

**(3) 生成引数の A/B も棄却**。動作中のモデルとの語単位の差分で `node+0x48` / `+0x144` が「我々 3、相手 1」であり、これは `ModelInstance_Create` の第 7 引数そのもの（IDA-unknown-F023）。そこでゲームの野外モデルと同じ `(0, 0, 1)` で作り直したところ、**`node+0x48` は 1 になったが `+0x228` は 0 のまま、`+0x22C` は 0xFFFFFFFF のまま**だった。つまり生成引数はこの欄に関係しない。

**(4) 残る構造的な差（次の対象）**: 動作中のモデルは **`node+0x228` にヒープのポインタ**（例 0x3054BCD8）を持ち **`+0x22C` は 0**。我々は **`+0x228` が 0、`+0x22C` が 0xFFFFFFFF**（-1＝未設定/無効を思わせる値）。この 2 語は行列プール（+0x220）と更新ゲート（+0x231）の間にあり、同じ skeleton 関連の区画に属する。生成時には埋まらないので、**生成後に別の呼び出しが設定している**と考えられる。

**(5) これまでに正常と確認済みの範囲**（実機または対照つき）: 資源の読み込みと Setup、モデル検索、インスタンス生成と活性化子、マテリアル（色・テクスチャ・ブレンド・深度・レイヤー）、メッシュの可視判定とボーン番号と材質番号、2 本のコマンド列の存在と大きさ、頂点バッファの束縛（基底＋差分が bcres 内を指す）、シーンへの登録、`Scene_DrawLayers` のふるい、ワールド行列、行列プールのゲートとベクタ。**それでも画素が出ない。**

反証条件: 動作中のモデルでも `+0x228` が 0 の個体がある、あるいは `+0x228` が描画に関与しない。根拠 `work/evidence/unit_cursor/probe_result.json`、`docs/topics/unit_cursor_hw_plan.md` §9。

