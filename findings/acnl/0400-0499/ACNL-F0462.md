---
id: ACNL-F0462
aliases:
- IDA-opus-5.5-F071
title: 'アニメ 0x1E1（seo_down1）を途中で切ると縮んだまま残る — 骨 root の拡大を書くアニメがほぼ無い（2026-09-30、MEDIUM: 資源の全数調査＋静的。実機未観測。ゲームの骨格更新が「書かれない骨を戻さない」ことは推定）'
summary: '解析ソフト: IDA（主 IDB）＋ romfs の HumanAnim / 解析モデル: opus-5.5。利用者の観察: 骨格アニメ 0x1E1 で小さくなっている途中にアクション解除（0x06）や他のアクションへ'
date: '2026-09-30'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6855792
- 6869228
- 6851096
- 8781744
- 1899500
- 1753656
- 5169336
- 5171784
- 6846696
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1357-1383
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F071: アニメ 0x1E1（seo_down1）を途中で切ると縮んだまま残る — 骨 root の拡大を書くアニメがほぼ無い（2026-09-30、MEDIUM: 資源の全数調査＋静的。実機未観測。ゲームの骨格更新が「書かれない骨を戻さない」ことは推定）

解析ソフト: IDA（主 IDB）＋ romfs の HumanAnim / 解析モデル: opus-5.5。利用者の観察: 骨格アニメ 0x1E1 で小さくなっている途中にアクション解除（0x06）や他のアクションへ
強制的に切り替えると、オンラインでも反映する縮小ができる。大きさのキーを初期化していないからではないか。
- **0x1E1 の流し方**: Vapecord の「Snake」= 状態 **0xC5**（g_PlayerStateTable）。始め **PlayerState_PlayAnimById_Enter 0x689C70** が引数ブロック +0x8CA（= pkt+0xE の u16）を
  そのまま Actor_PlayAnim（Vapecord の SNAKEFUNC 0x68D0EC）へ渡す。**終わり 0x688A18 は空関数**（何も戻さない）。アニメ番号 = g_AnimNameTable 0x85FFB0 の番号。
- **0x1E1 = seo_down1**（HumanAnim/humanAnimCommon.bcres、基本版・更新版とも。18 フレーム、要素 16 本）。**拡大（Scale）の曲線を持つのは骨 root だけ**で、
  X/Y/Z とも同じ曲線: キー (0, 1.0) (13, 1.0) (16, 0.01, 傾き −0.5242)（+ 16 の重複）。**フレーム 13→16 で 1.0 から 0.01 へ縮む**。
  途中の値の見込み（エルミート補間と仮定、LOW）: 14 ≈ 0.86、15 ≈ 0.50、15.5 ≈ 0.27、16 = 0.01。
  要素の形（tools/models3d/dump_skel_members.py で確認）: +0 flags / +4 名前 / +8 種類（5 = Transform）/ +0xC.. 曲線 10 個（0-2 拡大、3-6 回転、7-9 移動）、
  flags bit(16+i) = 曲線 i が無い、bit(6+i) = 定数。root（曲線 0-2 だけ、bit 19..25）・base（8/9 だけ、bit 16..23）・Lfoot3（定数 0.6981 と bit 10）の 3 通りで矛盾なし。
- **root の拡大を書くアニメの全数**（tools/models3d/survey_root_scale.py、HumanAnim 全 1,045 本 → work/evidence/player_scale/scale_channels.txt）:
  seo_down1（曲線）・**reset_in1（定数 1.0）**・ミニゲーム Escape の 11 本（定数 1.0）だけ。humanAnimCommon（更新版）の 403 本のうち **375 本は root の要素そのものが無く**、
  root を持つ 28 本も拡大は「無し」（seo_down1 と reset_in1 を除く）。handtool_wait1・nml_wait1・nml_walk1 も root 無し。
  → 縮んだあと普通のアニメへ移っても、**root の拡大に値を書くアニメが無いので縮んだ値が残る**、という説明になる。拡大 1.0 を明示して持つ reset_in1 があること自体、
  「アニメを替えても骨の値は戻らない」前提の作りを示す（状況証拠）。
- **利用者の仮説との関係**: 「大きさのキーを初期化していない」はほぼそのとおり。ただし初期化し忘れているのは状態の終わりではなく、**骨格アニメの切り替えで結び付かない骨を元へ戻さない**こと。
  切り替えの本体 0x1CFBEC → 0x1AC238 → 0x4EE0B8 → 0x4EEA48（アニメの差し替え）に、骨の姿勢を元へ戻す呼び出しは見当たらない（nw::gfx の評価器の中までは未読 → 推定）。
- **キノコ（F070）とは別の仕組み**: キノコ = モデル全体の拡大（TransformNode、状態が毎回 1.0 へ戻す）。0x1E1 = 骨 root の拡大（骨格アニメの値）。
  状態の関数が戻すのは前者だけなので、アクション解除（状態 0x06）では後者は戻らない。
- **オンラインで反映する理由**: 大きさの値は送られない（F070: 状態パケットは状態番号＋引数）。相手の端末も「0xC5 + 0x1E1」を受けて seo_down1 を自分で再生し、
  続く「0x06」などを受けた時点で切り替えるので、**相手の画面でも途中で止まって縮んだまま残る**。止まるフレームは相手側の受信時刻で決まるので、**自分と相手で大きさが少し違いうる**（見込み）。
- 見込み（未確認）: 切らずに最後まで再生すると root = 0.01 のまま残る（ほぼ見えない）。戻すには reset_in1 など root の拡大 1.0 を持つアニメを流す。
  root の要素を持つが拡大が「無し」のアニメ（例 chair_sitdownF1/L1/R1）で戻るかは nw::gfx の評価器しだいで未確認（戻るなら「無し」の曲線に元の値を入れている）。
- IDB: PlayerState_PlayAnimById_Enter / _Calc（0x6878E8）、注記 2（Actor_PlayAnim は Vapecord の注記を残して追記）。
- 反証条件: アクション解除で相手の画面の大きさが戻る、root の要素を持たないアニメへ切り替えても戻る、seo_down1 を最後まで流したあと普通のアニメで元の大きさになる。

