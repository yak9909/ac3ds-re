---
id: ACNL-F0493
aliases:
- IDA-opus-5.5-F040
title: 'nw::lyt / nw::font の描画規則（ウィンドウ枠・テクスチャ座標・合成・アルファ・文字配置・アニメ曲線）を静的に確定（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合）'
summary: 'UI 設計ツール `src/acnl-ui-designer`（利用者指示: 規則は静的解析で割り出し、画像は検証だけに使う）の描画器の根拠。全規則と番地の表は同リポジトリの `docs/verification.md`。'
date: '2026-09-25'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7584956
- 9420660
- 7584580
- 9930276
- 4945104
- 4945612
- 4945356
- 4944848
- 7583312
- 4946020
- 9942764
- 9942788
- 9942956
- 9943044
- 4954160
- 4940116
- 5067184
- 7589268
- 8288300
- 7838160
tags:
- layout
- font
supersedes: []
source: IDA:work/FINDINGS.md:2111-2127
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F040: nw::lyt / nw::font の描画規則（ウィンドウ枠・テクスチャ座標・合成・アルファ・文字配置・アニメ曲線）を静的に確定（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合）

UI 設計ツール `src/acnl-ui-designer`（利用者指示: 規則は静的解析で割り出し、画像は検証だけに使う）の描画器の根拠。全規則と番地の表は同リポジトリの `docs/verification.md`。

- ウィンドウ `nwlyt_Window_DrawSelf 0x73BCBC`（vt 0x8FBF74 slot 26）: 枠の大きさ `nwlyt_Window_GetFrameSize 0x73BB44`（texMap の画像 +8 幅 / +0xA 高さ。l = LB 幅, r = RT 幅, t = LT 高さ, b = RB 高さ）。LT (左,上) 大きさ (w−r,t)／RT (左+w−r,上) (r,h−b)／RB (左+l,上−h+b) (w−l,b)／LB (左,上−t) (l,h−t)。枠のテクスチャ座標は反転表 0x978624 と 0x4B74D0/0x4B76CC/0x4B75CC/0x4B73D0: 各枠がテクスチャの自分の角を保ち、クワッドの大きさ ÷ 画像の大きさだけ伸ばす（はみ出しはクランプで端の繰り返し）。中身は枠の内側＋inflation。
- テクスチャ座標 `nwlyt_CalcTexCoordsForGpu 0x73B650`: u = (u+tx)·比, GPU t = 1 − (v+ty)·比。回転・拡大は (0.5,0.5) 中心。レイアウトの v = 0 が画像の上（BCLIM は上下反転して保存されていない）。
- 合成 `Material_EmitState 0x4B7864`: マテリアル +0x4D bit1（資源の 0x800「テクスチャだけ」）は TEV・色を出さずに戻る（前の状態が残る）。テクスチャ 0 枚 = 頂点色（雛形 0x97B6EC）、1 枚 = 段3 c0·(1−tex) / 段4 c1·tex + 前 / 段5 頂点 × 前（0x97B704）。頂点色はペインの大域アルファ（+0xB5）を掛ける。2/3 枚は 0x97B7AC / 0x97B804。
- フィルタ・折り返し `0x4B9830`（reg 0x83）: 資源バイト bit0-1 = 折り返し（0 クランプ / 1 繰り返し / 2 反転）、bit2-3 = フィルタ（1 = 線形）。資源→実行時の変換は未読（この 1 点は MEDIUM）。
- アルファ `nwlyt_Pane_CalculateMtx 0x4B6154`: 大域 = (u8)(alpha × 係数)。子の係数は、影響フラグ（+0xB7 bit1）が立ち alpha ≠ 255 のときだけ alpha × 係数 / 255、ほかはそのまま渡る。
- 文字: 拡大率 0x4D51B0（sH = 大きさ.x ÷ FINF 幅 +0x15、sV = 大きさ.y ÷ FINF 高さ +0x14）。原点 `nwlyt_TextBox_GetTextOrigin 0x73CD94`（ペイン左上 + (0|w/2|w, −(0|h/2|h))、textPosition は +0xFC）。整列 0x7E782C（中央 x −= ceilf(W/2)、`ceilf 0x7799D0`、右 x −= W。縦も同じ。行揃え 1: + ceil(W/2) − ceil(行幅/2)、2: + W − 行幅）。カーソル Y = y + ascent（FINF +0x16）·sV（`0x743600`）。字の位置 = (cx + left·sH, cy − baseline（TGLP +2）·sV)、大きさ 字幅·sH × セル高·sV。送り = advance·sH、2 字目から字間を足す。改行 = 行間 + lineFeed（FINF +1）·sV（`0x8268A8`）。行の矩形の高さ = lineFeed·sV（`0x7E7A78` / `0x7E7E60`）。自動改行はペイン幅（writer +0x4C）。
- 文字の TEV（A4/A8、雛形 0x8ADAE0）: 段3 (1−tex.rgb)·c1, α = tex.a·c1.a／段4 tex.rgb·c0 + 前, α = (1−tex.a)·c0.a + 前／段5 文字色（頂点）× 前。定数のアルファはペインの大域アルファを掛ける。フォントシートは線形フィルタ（ResFont +0x10 = 6、`ResFontBase_Init 0x4D7590`）。
- アニメ曲線 `nwlyt_GetHermiteCurveValue 0x4B5EA0`: 1 個／最初以下 → 最初、最後以上 → 最後、二分探索（f ≤ key[mid] → hi）、|f − key[hi]| < 0.001 → key[hi]（次が同じフレームなら key[hi+1]）、ほかはエルミート（傾き × d）。段の曲線（CLVI/CLTP）は key[mid] ≤ f → lo、f − key[hi] ≤ −0.001 でなければ key[hi]。色（CLVC `0x4B5140` / CLMC `0x4B541C`）は +0.5・0..255 に切って切り捨て。
- 一覧 InstSelect の組み立て段 2（0x1C53A8–0x1C5410）: d = 行0.y − 行1.y（26）を一覧 +0x9CC、N_frame_00.y += d、シザー `sub_1C55F8`、ルートペイン（Layout +0x20）y −= d（F039 の続き）。
- 照合（設計ツールの描画 vs 実機の下画面 1 枚）: 枠の形と色（W_scrn_01 の LT 色 (205,160,0)）・中身・ロープ・文字の位置（上 89 / 下 99、横は一致）・7 行目の切り抜きが一致。差は場面に入れていないもの（ID・選択・スクロールバー）と 1 px の区切り線（PICA200 の塗りつぶし規則。ゲームのコードからは導けない）。
- 反証条件: 別の画面（上画面・別の arc）で枠や文字の位置が合わない／フィルタ・折り返しの資源値が逆になる場面が出る。
- IDB: 上の関数を命名・注記（`ida/db/acnl_jpn_v15_annotated.i64`）。

