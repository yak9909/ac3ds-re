<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / render

| ID | 題 | summary | 確度 | 格付け | consolidated_into | 訂正 |
|---|---|---|---|---|---|---|
| ACNL-F0028 | F-155a: submit-descriptor recorder は描画前のレジスタ連鎖で例外 — `HIGH`（例外位置＋機械的監査） | `scratchpad/trace_main_text_submit_descriptor.py` の初版は | HIGH | ? |  |  |
| ACNL-F0029 | F-151: native TextBox draw の descriptor は `R2=0x330A605C` — `HIGH`（trace＋既存実測照合） | `scratchpad/trace_textbox_draw_args.py` を `nwlyt_TextBox_DrawToCommandList` | HIGH | ? |  |  |
| ACNL-F0033 | F-144: 会話 TextBox も batch writer 経路 — `HIGH`（静的＋実機） | 会話表示中に `0x4BAFFC`（`sub_4BAFB0` 内の `sub_7E7F48` 呼出し）へ software | HIGH | ? |  |  |
| ACNL-F0034 | F-145: TextBox batch は専用list 32で構築され、メインlistへ再生される — `HIGH`（静的＋実機） | software BPを使わず、`scratchpad/trace_text_batch_submit.py` で会話名TextBoxのbatch | HIGH | ? |  |  |
| ACNL-F0037 | F-147: `nw::lyt::Picture` は TextBox と同じ UI command-list 経路を使う — `HIGH`（静的＋実機） | `ti_nw_lyt_Picture=0x8C9B9C` / `vtbl_nw_lyt_Picture=0x8FBFFC` の Pane draw slot | HIGH | ? |  |  |
| ACNL-F0038 | F-146: TextBox batch は固定0x60-byte seedとglyph/state blockから構成される — `MEDIUM`（静的＋停止中live照合） | `TextBatch_BuildCommandStream` (`0x4D6570`) の命令列を、F-145 の同一会話名 | MEDIUM | ? |  |  |
| ACNL-F0122 | F-84: Catalog actor typeはItemParam由来。`AcFtr` はbank確保、model非同期読込、layer 2登録の3 phase | confidence: **MEDIUM**（Item.bin loader、family table、AcFtr vtableと各phaseの静的照合） | MEDIUM | ? |  |  |
| ACNL-F0132 | F-94: 描画スタックの同定と GSP IPC 層 | confidence: **MEDIUM**（RTTI 実測 + IPC パターンを逆コンパイルで確認。**静的解析のみ**） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0133 | F-95: GPU コマンドバッファ `g_GpuCmdPtr` の特定 | confidence: **MEDIUM**（逆コンパイルでヘッダ定数と書き込み手順を直接確認。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0134 | F-96: コマンドリストの終端・提出経路と GX API 一式 | confidence: **MEDIUM**（型値と引数位置を直接確認。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0135 | F-97: `GpuCmd_GetProperty` と、自前コマンド追加の定石 | confidence: **MEDIUM**（getter の switch を逆コンパイルで直接確認。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0136 | F-98: TODO-37 の否定と、描画解析の全体精査 | confidence: **MEDIUM**（各項目を逆コンパイル／RTTI で個別に検証。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0137 | F-99: 描画解析の再精査 — 数値変換 2 件とレジスタ名 3 件の誤りを訂正 | confidence: **MEDIUM**（機械的な検算は確実だが、`registers.h` は `REFERENCES/` 配下＝一次情報ではない。F-101 で訂正） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0138 | F-100: 再々精査 — GX 5 本の type バイト確定、「実装位置」表記の誤りを訂正 | confidence: **MEDIUM**（**静的解析のみ**、F-101 で訂正。表題の「HIGH 化」も撤回） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0140 | F-102: ★実機観測でコマンドバッファ構造を確定（初の HIGH） | confidence: **HIGH**（CLAUDE.md の定義どおり**静的解析と動的観測の双方**で確認） | HIGH | ? |  |  |
| ACNL-F0141 | F-103: ★GX キューを実機で直接読み、1 フレームの構成を観測 | confidence: **HIGH**（静的 + 動的。TODO-48） | HIGH | ? |  |  |
| ACNL-F0144 | F-106: ★`g3d::FuncNode` — 描画中に任意の関数を呼べるシーンノード | confidence: **MEDIUM**（静的解析のみ。CLAUDE.md の定義に従い実機未観測なので HIGH にしない） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0145 | F-107: ★`g3d::FuncNode` の実在を確認。コールバック登録 API まで判明 | confidence: **MEDIUM**（静的解析のみ。ただし独立した 2 経路から裏付け） | MEDIUM | ? |  | 訂正あり |
| ACNL-F0146 | F-108: FuncNode 解析の精査 — 前提の再検証と 1 件の見落とし | confidence: **MEDIUM**（静的解析のみ） | MEDIUM | ? |  |  |
| ACNL-F0147 | F-109: ★★実機で `g3d::FuncNode` の実在とコールバックを確認（HIGH 達成） | confidence: **HIGH**（CLAUDE.md の定義どおり**静的解析と動的観測の双方**で確認） | HIGH | ? |  |  |
| ACNL-F0149 | F-111: ★★TODO-60 解決 — ノードをシーンに載せる仕組み（`Scene_SubmitNode`） | confidence: **HIGH**（当初 MEDIUM。**F-112 の実機観測で昇格**） | HIGH | ? |  | 訂正あり |
| ACNL-F0150 | F-112: ★★実機で F-111 を検証（TODO-64 完了）— 確度 `HIGH` へ。配列 #5 の記述を訂正 | confidence: **HIGH**（静的解析と実機観測の双方で一致。CLAUDE.md の `HIGH` 定義を満たす） | HIGH | ? |  | 訂正あり |
| ACNL-F0151 | F-113: ★★TODO-68 完了 — `BsShadowViewMgr` が実例。フレーム描画の全体像と `1024`/`1040` の正体 | confidence: **HIGH**（静的解析と実機観測の双方。実機の `LR` とスタックで連鎖を確認） | HIGH | ? |  | 訂正あり |
| ACNL-F0152 | F-114: ★★TODO-71 完了 — 描画コールバックが積むものの全体像（自前描画の手本） | confidence: **HIGH**（静的解析と実機のメモリ直読みの双方。レジスタ名は `registers.h` で照合） | HIGH | ? |  | 訂正あり |
| ACNL-F0153 | F-115: ★F-110〜F-114 の精査（TODO-75 の前の検証）— 誤り 2 件・過剰主張 3 件を訂正 | confidence: **HIGH**（訂正内容はいずれも一次証拠で確認） | HIGH | ? |  |  |
| ACNL-F0159 | F-121: ★★TODO-84 第1段 — 積まれたコマンドを自分で解釈・書き換え、描画結果を狙って変えられた | confidence: **HIGH**（実機。数値と目視の双方で確認） | HIGH | ? |  |  |
| ACNL-F0160 | F-122: ★★★TODO-84 達成 — 完全自己完結の自前描画。あわせて TODO-83 も解決 | confidence: **HIGH**（実機。ユーザーの目視で単一インスタンスの同定まで一致） | HIGH | ? |  |  |
| ACNL-F0172 | F-134: EmitGlyphQuad の texture handle 選択と batch/immediate 分岐を静的再監査 — `MEDIUM` | `nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) の全分岐を静的に再読した。 | MEDIUM | ? |  |  |
| ACNL-F0175 | F-137: `SetGlyphTextureParams` の引数は decompiler 表示より多く使われる — `MEDIUM` | `0x4D8484` の逆コンパイル表示では `0x7ABDBC` 呼び出しの引数が省略され、texture | MEDIUM | ? |  |  |
| ACNL-F0177 | F-140: TextBox→TextWriter の描画入口と後処理 — `MEDIUM`（静的） | `nwlyt_TextBox_DrawText` (`0x4BB1E8`) の命令列から、標準テキスト描画を再利用する最小の | MEDIUM | ? |  |  |
| ACNL-F0179 | F-143: TextBox vtable の実描画入口は `0x73CF48` — `HIGH`（静的＋実機） | `nw_lyt_TextBox` vtable (`0x8FC07C`) の slot `+0x64` は `nwlyt_TextBox_DrawText` | HIGH | ? |  |  |
| ACNL-F0182 | F-156: ★★★submit descriptor を静的に全導出。F-155a の observer は不要になった | confidence: **HIGH**（静的。decompile とアセンブリの両方で照合） | HIGH | ? |  | 訂正あり |
| ACNL-F0183 | F-157: ★★★テキスト描画コマンドの投入を自前で駆動できた。色バイト順も確定 — `HIGH`（静的導出＋実機で視認） | 実機の会話ウィンドウで、住民名 `T_nam_00`（「ぺりお」）が | HIGH | ? |  |  |
| ACNL-F0186 | F-160: テキスト描画の座標系を確定。F-158 の「1.25 = 400/320」は誤り — `HIGH`（実機で基準行列を採取＋3 枚の配置と照合） | `0x4B7DCC` で `[R9-64, R9)` の 16 ワードを控えて得た: | HIGH | ? |  |  |
| ACNL-F0197 | F-171: ★TextBox の描画は歩行中ゼロ。相乗り方式には大きな穴がある — `HIGH`（実機で計測） | 適用: `PATCHES/measure_textbox_draws.py` | HIGH | ? |  | 訂正あり |
| ACNL-F0202 | F-176: Picture はコマンドを直接吐かず、描画コンテキストに四角形を溜めて一括で流す — `HIGH`（静的解析） | ```c | HIGH | ? |  |  |
| ACNL-F0204 | F-178: 描画コンテキストの四角形配列を解読。`+1648` は F-167 の `c[0x40]` そのもの — `HIGH`（実機で採取） | 適用: `PATCHES/cave_probe_drawctx.py` | HIGH | ? |  |  |
| ACNL-F0209 | F-183: ★索引エントリの `w3` は「色」。テクスチャはバッチ単位 — `HIGH`（静的解析） | F-180 で索引エントリの `w3` を「マテリアル関連」と書いたが、**誤り。** | HIGH | ? |  | 訂正あり |
| ACNL-F0210 | F-184: 頂点カラーはアルファだけが効いた。RGB は素材の TexEnv 次第 — `HIGH`（実機で A/B） | 適用: `PATCHES/cave_add_sprite.py` | HIGH | ? |  |  |
| ACNL-F0211 | F-185: ★★★フック地点で **`R1` がコマンドカーソル**。任意の GPU コマンドを発行できる — `HIGH`（実機のコマンド列で確認） | ``` | HIGH | ? |  |  |
| ACNL-F0212 | F-186: ★索引エントリの意味を静的に確定。色は複製先ではなく**複製元**に出る — `HIGH`（静的＋実機 A/B 多数） | ```c | HIGH | ? |  |  |
| ACNL-F0213 | F-187: ★ゲーム自身の「色つきスプライト」を実測。構造は自前と同一だった — `HIGH`（実機フック） | `PATCHES/probe_vertex_color.py`（`0x4B8348` と `0x73CD1C` の 2 点フック）で、 | HIGH | ? |  |  |
| ACNL-F0214 | F-189: ★★★色ブロックの並びを確定。4 隅は「左上→右上→左下→右下」 — `HIGH`（実機で直接可視化） | 色つきバッチ（カウンタ `+36=1 +37=7 +38=2`）で、 | HIGH | ? |  |  |
| ACNL-F0217 | F-192: ★★★★フラッシュは配列の `[0].w0` を破壊する。退避先はポインタ −4 — `HIGH`（静的＋実機） | `TextDraw_EmitStatePrefix`（`0x4D5CB0`）も `DrawCtx_FlushBatch`（`0x4B8360`）も、 | HIGH | ? |  |  |
| ACNL-F0218 | F-193: ★★★★★自前スプライトを独立したバッチで描画。テクスチャも独立 — `HIGH`（実機） | `PATCHES/cave_own_batch.py`。**「左上に白黒の市松模様の板が出て、背景は元のまま」**（ユーザー確認）。 | HIGH | ? |  |  |
| ACNL-F0219 | F-194: ★★★UV の座標系を確定。アトラスから切り出せる — `HIGH`（実機で 3 段階の A/B） | 追加幾何エントリ（索引エントリの `w2` が指す先）の 4 float が UV。 | HIGH | ? |  |  |
| ACNL-F0222 | F-197: ★★★コマンドバッファは 1 つではない。`g_GpuCmdPtr` と `g_GpuCmdEnd` は別リストのことがある — `HIGH`（GPU ハングで判明） | 「そのフレームの最後のフラッシュ」を予測する方式が破綻したので | HIGH | ? |  |  |
| ACNL-F0223 | F-198: ★★★★7 枚超の描画と、ドット絵をきれいに出すための 4 条件 — `HIGH`（実機） | `PATCHES/cave_draw_sprites.py`。**「ACNL GUI OK」11 文字（2 チャンク）を描画し、 | HIGH | ? |  |  |
| ACNL-F0225 | F-200: ★★★★★UI は「1 本のコマンド列」ではない。記録と再生に分かれている — 静的解析 | > **2026-09-01 訂正（F-233）:** 記録／再生の構造は維持するが、下の |  | ? |  | 訂正あり |
| ACNL-F0226 | F-201: F-200 の検証。**1 件の訂正と、GPU ハングの静的な説明** — 静的解析 | F-200 を疑って再検証した。**ユーザーの指示「confidence HIGH でも信用しきらない」に従う。** | HIGH | ? |  |  |
| ACNL-F0227 | F-202: ★★★メインリストの末尾に積んでも UI は描かれない。2 回目のクラッシュの原因 — `HIGH`（実機） | F-200 / F-201 の静的解析に基づき、**`Frame_DrawPass1024` の末尾** | HIGH | ? |  |  |
| ACNL-F0231 | F-206: ★★★★色とテクスチャの出所は「マテリアル」。自前で積まないと直前のペインのものになる — `HIGH`（実機） | `nwlyt_Picture_DrawToCommandList` は必ず先頭でこう呼ぶ。 | HIGH | ? |  |  |
| ACNL-F0232 | F-207: ★★★★★`drawctx+1692` が 0 だと UV が読まれずテクスチャ全面が貼られる — `HIGH`（実機） | `nwlyt_Picture_DrawToCommandList` より: | HIGH | ? |  |  |
| ACNL-F0236 | F-211: ★★★★マテリアルは「たまたま」ではなく条件で選ぶ — `HIGH`（実機） | F-206 では「そのフレームで最初のフラッシュ時点のマテリアル」を流用していた。 | HIGH | ? |  |  |
| ACNL-F0237 | F-212: ★★★★★マテリアルには名前と定数色が入っている — `HIGH`（実機） | 自前スプライトが「たまに別の色を拾う」症状の正体。 | HIGH | ? |  |  |
| ACNL-F0239 | F-214: ★★★★★中立なマテリアルが 1 つも無い場面がある。定数色は借りる側で中立化する — `HIGH`（実機） | プラグインで動くようになった後、**タイトル画面とロード画面だけ** | HIGH | ? |  |  |
| ACNL-F0240 | F-215: ★★★★★借りたマテリアルは 9 語まとめて中立化する。ただし描画後に積み直してはいけない — `HIGH`（実機） | F-214 の対策（`+0x10`/`+0x14`/`+0x18` の 3 語を中立化）では**しずえ会話の切り替わりで | HIGH | ? |  |  |
| ACNL-F0241 | F-216: ★★★★★`reg 0x082` は `(幅<<16)\|高さ`。正方形しか試していないと気付けない — `HIGH`（実機） | 自前 GUI はずっと `((TEX_H << 16) \| TEX_W, 0x082)` と書いていた。 | HIGH | ? |  |  |
| ACNL-F0243 | F-218: ★★★半透明（アルファブレンド）は使える — `HIGH`（実機） | OSD を避けた理由の 1 つが「アルファブレンドが使えない」ことだった（ユーザー指摘）。 | HIGH | ? |  |  |
| ACNL-F0252 | F-227: ★★★観測用の領域を、動いている描画の領域と重ねてクラッシュさせた — `HIGH`（実機） | フェードの調査のために `probe_replay_last.py` を仕掛けたらクラッシュした。 | HIGH | ? |  |  |
| ACNL-F0255 | F-230: ★★★★相乗り先は「候補のうち最後に再生されたもの 1 つ」。両方に積むと二重になる — `HIGH`（実機） | F-228 で「通常用（id 15 / id 16）とフェード用（id 9 / id 8）の**両方に積む**」ことにした。 | HIGH | ? |  | 訂正あり |
| ACNL-F0258 | F-233: 描画パス末尾と通常場面の実 replay を再監査 — `HIGH`（静的＋実機。ロード画像の順序は未測定） | `HANDOFF_CHEATMENU.md` と F-200 / F-230 の前提を、`code.bin.i64` と | HIGH | ? |  |  |
| ACNL-F0276 | F-253: ★★★★★描画パスは 3 本。`Frame_DrawPass1040` は下画面ではなく「上画面の右目」 — `HIGH`（静的＋実機の独立 2 系統） | F-252 で「Layout 用のリストは 1 本だけ」「投影は上下とも 400x240」と書いたのは**誤り**である。 | HIGH | ? |  |  |
| ACNL-F0279 | F-256: ★★★★★ゲームがそのパスで 1 枚も描いていないと、描画コマンドを積んだ瞬間に GPU が止まる — `HIGH`（実機で二分により確定） | 自前ノード方式にしてから、**「上画面のタイトルロゴが消えた瞬間」に必ず GPU が停止**した。 | HIGH | ? |  |  |
| ACNL-F0280 | F-257: ★★★★F-256 のゲートの正体は「ゲームが**記録し直した**フレームだけ描く」だった — `HIGH`（実機・目視） | > **★F-263 で説明を訂正した。** 「作業配列はフレームごとに使い回される」という説明は**誤り**。 | HIGH | ? |  | 訂正あり |
| ACNL-F0282 | F-259: ★★★★★UI 描画経路の完全な静的仕様。render.txt は本作と 1:1 で一致する — `HIGH`（静的のみ） | `REFERENCES/TEXTS/render.txt` の `ssys::ma::lyt::Layout::RenderFrame` を、 | HIGH | ? |  |  |
| ACNL-F0284 | F-261: ★★★★★Layout の初期化 `sub_5685A4` に「自前リストの正しい作り方」が全部書いてある — `HIGH`（静的のみ） | F-260 の実装を静的に検証する過程で見つけた。**私の実装には致命的な誤りが 2 つあった。** | HIGH | ? |  |  |
| ACNL-F0286 | F-263: ★★★★★F-257 / F-258 の説明は誤りだった。作業配列は Drawer の**固定メンバ**である — `HIGH`（静的） | Drawer（＝drawctx）のコンストラクタ `sub_4D7364`（`nw::font::RectDrawer` 派生）が | HIGH | ? |  |  |
| ACNL-F0289 | F-266: ★★★★★`SetupProjectionMatrix` は **`+0x28` / `+0x2C` しか読まない**。だから自前ノードでもそのまま呼べる — `HIGH`（静的のみ） | F-265 では投影行列を手で組み立てたが、その前提 | HIGH | ? |  |  |
| ACNL-F0291 | F-268: ★★★★★Drawer の既定コマンド列には **TEV 段が 1 つも無い**。色は必ずマテリアル由来 — `HIGH`（静的のみ） | 「`DrawBegin1` の既定 TEV で LA4 アトラス × 頂点カラーが合成されるか」（F-260 の未検証項目）に | HIGH | ? |  | 訂正あり |
| ACNL-F0293 | F-270: ★★★★DrawBegin1 は **テクスチャユニットを全部無効にする**。自前記録では立て直さないとテクスチャが読まれない — `HIGH`（静的 + 過去の実測列） | 自前記録の設計（F-259 以降）に残っていた穴。**これは `OWN_TEV` とは独立の問題である。** | HIGH | ? |  |  |
| ACNL-F0294 | F-271: ★★★★★`TextBox_UpdateDrawState`(`0x4B7DEC`) が「テクスチャ付き描画へ切り替える」全手順。実測列の全項目がこれで説明できた — `HIGH`（静的 + F-124 の実測列） | F-270 で reg `0x080` の穴を見つけたので、**同じ穴が他にもないか**を | HIGH | ? |  |  |
| ACNL-F0298 | F-274: `sub_2F858C` は **3 引数の memcpy**。decompiler が R1/R2 を落としていた — `HIGH`（アセンブリ） | `GpuCmd_ReplayRecordedListRange` の末尾を Hex-Rays で読むと | HIGH | ? |  |  |
| ACNL-F0299 | F-275: 自前ノードに対してゲームが呼ぶのは vtable `+0x08` と `+0x14` の 2 つだけ — `HIGH`（静的） | `CAVE_N`（安全スタブ、常に `R0 = 0` を返す）が危険なスロットに置かれていないかを確認した。 | HIGH | ? |  |  |
| ACNL-F0300 | F-276: ★★★★★【F-268 の訂正】既定ブロックは **記録時ではなく再生時**に出る。フラグで切り替わる — `HIGH`（アセンブリ） | F-268 で「Drawer の既定 begin ブロックは記録の先頭で出る」と書いたのは**誤り**だった。 | HIGH | ? |  |  |
| ACNL-F0301 | F-277: 記録 → Commit → 再生の連鎖を端から端まで静的に証明した — `HIGH`（静的のみ） | 「実装したものがどう影響するか」を、関数ごとに全部読んで繋いだ。 | HIGH | ? |  |  |
| ACNL-F0306 | F-281: ★★★★★実機で描画に成功した。ノイズの原因は**非整数倍の拡大** — `HIGH`（実機） | > あなたの想定通りに出ています。フリーズもせず、ロードやメニュー操作で消えず常に表示されています。 | HIGH | ? |  |  |
| ACNL-F0314 | F-290 (HIGH・実機) — CAVE_Q を `Picture_DrawToCommandList` 呼びへ置き換えた。**座標系は手書き経路と同一** | 2026-09-04 深夜〜2026-09-05。設計は `scratchpad/DESIGN_caveq_picture.md`、 | HIGH | ? |  |  |
| ACNL-F0316 | F-292 (HIGH・静的のみ) — ★F-291 を別関数で再検証（矛盾なし）。**正規の手順なら記録ケーブは丸ごと不要** | 全文は `scratchpad/MEMO_f292_proper_way.md`。 | HIGH | ? |  |  |
| ACNL-F0336 | F-311 追記: 実機で描画されなかった原因（2026-09-06）— HIGH | プラグインを ON にしても**何も描画されず、Select でメニューも開かない**。 | HIGH | ? |  |  |
| ACNL-F0342 | F-316: ★シート記述子 `+0x0C` は **`(幅<<16) \| 高さ`** — HIGH | 256x128 のシートに載せ替えたら、**文字が完全に化けた**（画素が散る）。 | HIGH | ? |  |  |
| ACNL-F0443 | アニメ本体は g3d の自前クラス。nw::gfx::AnimEvaluator を使うと落ちる（2026-09-21、HIGH、実機・自己訂正） | 解析ソフト: IDA / 解析モデル: opus-5。**F009 に「未検証の仮説」と書いた箇所を実機で突いて反証された。** | HIGH | ? |  |  |
| ACNL-F0444 | 自前資源のマテリアルアニメを生成し、自前instanceへ結線できた（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**自分で読み込んだ `UnitCursor.bcres` のアニメを、 | HIGH | ? |  |  |
| ACNL-F0447 | 外部 nw4c ヘッダとの照合。実測は全て一致し、引数の解釈を2点訂正（2026-09-21、HIGH、静的＋実機照合） | 解析ソフト: IDA / 解析モデル: opus-5。利用者提供の [SMBNext/nsmb2-headers](https://github.com/SMBNext/nsmb2-headers) | HIGH | ? |  |  |
| ACNL-F0448 | ModelInstance_Create の a5/a6/a7 を実機で分離（2026-09-21、HIGH、実機A/B/C） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-F014 の仮説を実機で検証。 | HIGH | ? |  |  |
| ACNL-F0449 | アニメが何を動かすかは資源から読める。UnitCursor は色定数2本とUV平行移動（2026-09-21、HIGH、静的） | 解析ソフト: IDA / 解析モデル: opus-5。外部資料（[captainsouthbird/CGFXModel](https://github.com/captainsouthbird/CGFXModel)）は | HIGH | ? |  |  |
| ACNL-F0450 | 骨アニメを実機で結線し、骨が動いた（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009。資源は IDA-opus-5-F018 が選んだ | HIGH | ? |  |  |
| ACNL-F0451 | 骨アニメが結線できる条件と、実機に触れずに選んだ資源の組（2026-09-21、HIGH、静的＋実機読み出し） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009 の前段。**実機へは一切書いていない**（読み出しのみ）。 | HIGH | ? |  |  |
| ACNL-F0454 | 場面転換。自前instanceは無傷で残り、ケーブは自分から描画を止める（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T018。**利用者に建物へ入ってもらって測定した。** | HIGH | ? |  |  |
| ACNL-F0455 | 描画中に instance を解放しても何も起きない。ただし理由は2つある（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017a。**意図的に安全手順を破った試験。** | HIGH | ? |  |  |
| ACNL-F0456 | 描画中に資源を潰しても落ちない。モデルが黙って消えるだけ（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017b。**意図的に安全手順を破った試験の第2段。** | HIGH | ? |  |  |
| ACNL-F0462 | アニメ 0x1E1（seo_down1）を途中で切ると縮んだまま残る — 骨 root の拡大を書くアニメがほぼ無い（2026-09-30、MEDIUM: 資源の全数調査＋静的。実機未観測。ゲームの骨格更新が「書かれない骨を戻さない」ことは推定） | 解析ソフト: IDA（主 IDB）＋ romfs の HumanAnim / 解析モデル: opus-5.5。利用者の観察: 骨格アニメ 0x1E1 で小さくなっている途中にアクション解除（0x06）や他のアクションへ | MEDIUM | S |  |  |
| ACNL-F0472 | UnitCursor を村の物体の下に描く — 地面に張り付く物の材質と、深度書き込みの出どころ（2026-09-28、MEDIUM: 静的のみ。gohan f47f5af、実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: マイデザイン等の極薄・地面に吸着したモデルに UnitCursor が被さる → 常に対象マスのモデルより下／背面。公共事業エディターも共通。 | MEDIUM | S |  |  |
| ACNL-F0474 | 1 つの体を行列だけ変えて何か所にも描く（描画ノード FuncNode）（2026-09-28、MEDIUM: 静的のみ。gohan 4fb9e33 で使用、実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示（2026-09-28）: ヒープの上限を越えたときの扱いを再設計。 | MEDIUM | S |  |  |
| ACNL-F0475 | 村の物体の描画の仕組み — 1 体ずつ色を変える入口と、カーソルが消えた原因（2026-09-28、MEDIUM: 静的＋停止中の実機の読み取り。赤の割り込みは実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的、停止中の実機を ida-pro-mcp で読み取りのみ）/ 解析モデル: opus-5.5。 | MEDIUM | S |  |  |
| ACNL-F0476 | モデルの資源の Setup と後片付け — 自前の体を壊すと元の資源の LUT 参照が外れる（2026-09-28、HIGH: 静的＋停止中の実機の読み取り） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的、停止中の実機を ida-pro-mcp で読み取りのみ）/ 解析モデル: opus-5.5。 | HIGH | S |  |  |
| ACNL-F0477 | 村の実体の材質は同じモデルで共有、書き換えるとゲームの書き出しが落ちる／参照表の安全条件（2026-09-28、HIGH: 実機のクラッシュと静的） | 解析ソフト: IDA（ida-pro-mcp で停止中の実機を読み取りのみ、主 IDB）/ 解析モデル: opus-5.5。gohan 165b571 の実機確認で「触っていない同じモデルも赤い」「しばらく使うと落ちる」。 | HIGH | S |  |  |
| ACNL-F0493 | nw::lyt / nw::font の描画規則（ウィンドウ枠・テクスチャ座標・合成・アルファ・文字配置・アニメ曲線）を静的に確定（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合） | UI 設計ツール `src/acnl-ui-designer`（利用者指示: 規則は静的解析で割り出し、画像は検証だけに使う）の描画器の根拠。全規則と番地の表は同リポジトリの `docs/verification.md`。 | HIGH | S |  |  |
| ACNL-F0498 | 複製の光＝BsLightMgr の組のフラグメント方向光・アンビエント・半球。向きはゲームのカメラの view で変換されるので専用カメラと食い違う。描く間だけ自前の組に差し替える（2026-09-24、MEDIUM（静的＋実機の読み取り）。gohan の直しは実機未確認） | **利用者の実機確認（gohan 8908f5d）**: ズボンは付いてくる、髪 -1 で戻る（F032 の 2 点は確認済み）。傾きは 45 度ぐらいが良い。傾けるとポリゴンがおかしい／影が変な所に出来る気がする。 | MEDIUM | S |  |  |
| ACNL-F0499 | 画面固定の複製でズボンが止まる＝部品のスキニング行列は Scene の更新が計算する。光はフラグメントライティングではない（★光の部分は F033 で訂正：読んだ組が違った）（2026-09-24、MEDIUM（実機の読み取り＋静的）。gohan 8908f5d は実機未確認） | **利用者の実機確認（gohan 246865a）**: 上画面の決まった位置に固定・世界の物に隠れない（2D UI には隠れる）・部品は欠けない・設定は全部効く。 | MEDIUM | S |  |  |
| ACNL-F0502 | 髪は毎フレームの部品更新が pm+548 から読む。複製は本物のプロフィールで作り pm+548/+552 を書くだけでよい（F028 の一部訂正）（2026-09-24、MEDIUM（静的。複製での実機確認は未実施）） | `PlayerModel_UpdateParts 0x1D0AEC`（旧 vc_UPDATETANOFFSET）: 各バンクの枠の部品と望む値を比べ、違えば入れ替え式で読み直す。頭の望む値は | MEDIUM | S |  |  |
| ACNL-F0503 | PlayerModel と部品バンク。複製はゲーム自身の作成・片付け関数と「プロフィールの写し」で作れる（2026-09-24、HIGH（静的＋実機 BP・実機の読み取り）。複製の作成は未実施） | **構造**: AcPlayer+436 = PlayerModel（RTTI 11PlayerModel、vtbl 0x8E5F74、624 B）。pm+548 髪型 / +552 髪色 / +556 目の色 / +512 服 8 枠。 | HIGH | S |  |  |
| ACNL-F0521 | モデル単位の色ハイライトは「TEV の空き最終段で定数色と混ぜる」でできる（2026-09-23、**HIGH（静的＋実機で表示確認）**。材質 1 つで確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「建物を含めた任意の 3D モデルで、そのモデルだけ全体の RGBA を操作できるか。 | HIGH | S |  |  |
| ACNL-F0523 | 建物の資源は 2 系統。共有 64 枠（公共事業など 7 クラス、1 種類 2 枠）と、役場・店の専用ヒープ（2026-09-23、HIGH（静的＋実機）） | 解析ソフト: IDA / 解析モデル: opus-5.5。F007 の版で「全建物が置くたびに読み直し」「公共事業を複数置いたらクラッシュ（ダンプ 3）」の報告を受けて、 | HIGH | S |  |  |
| ACNL-F0534 | マス数変更中のクラッシュと、縞模様の 45 度（2026-09-22、HIGH、クラッシュダンプ＋静的） | 解析ソフト: IDA / 解析モデル: opus-5。 | HIGH | ? |  |  |
| ACNL-F0535 | 村の 1 マス = world 32 単位。UnitCursor の原点は quad の中心（2026-09-22、HIGH、実機＋CGFX） | 解析ソフト: IDA / 解析モデル: opus-5。**独立な 2 経路が一致したので確定とする。** | HIGH | ? |  |  |
| ACNL-F0539 | 姿勢を直接書くだけでは描かれない。骨格の更新が要る（2026-09-21、HIGH、実機。**F017 の訂正**） | 解析ソフト: IDA / 解析モデル: opus-5。**利用者の指摘（「UnitCursor が画面内に描画されていない」）から判明した。** | HIGH | ? |  |  |
| ACNL-F0542 | 骨・アニメの構造。node+0x228 は AnimGroup で、F029 の2語の正体（2026-09-21、HIGH、静的＋実機） | 解析ソフト: IDA / 解析モデル: opus-5。**アニメを結線するには instance 側に「アニメ枠」が要る。** | HIGH | ? |  |  |
| ACNL-F0543 | SkeletalModelも描けた。node+0x228/+0x22C は不可視の原因ではない（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**`UnitCursor`（`0x40000092` = `nw::gfx::SkeletalModel`）を | HIGH | ? |  |  |
| ACNL-F0545 | park 用の BP は `0x1B721C` では張れなくなる。`0x1B7220` が同値（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。同じ boot の前半では `0x001B721C` への | HIGH | ? |  |  |
| ACNL-F0546 | 任意bcresの読み込み→ワールド描画が実機で成立（2026-09-20、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**ゲームが読んでいないファイルを自分で読み、画面に出した。** | HIGH | ? |  |  |
| ACNL-F0547 | モデルのクラスは資源が決める。ゲーム内のCMDLは2種類しかない（2026-09-20、MEDIUM、静的） | 解析ソフト: IDA / 解析モデル: opus-5。対象 `artifacts/update/exefs/code.bin`（VA=file+0x100000）。 | MEDIUM | ? |  |  |
| ACNL-F0548 | 屋外座標の曲面変換は部屋フラグで切り替わる。165部屋中37部屋（2026-09-20、HIGH、静的＋実機） | 解析ソフト: IDA / 解析モデル: opus-5。`FieldPosition_ToRenderSpace 0x0052CDD8` は | HIGH | ? |  |  |
| ACNL-F0549 | 不可視だった UnitCursor は生のゲーム座標に置かれていた（2026-09-20、HIGH、静的＋実機、自己訂正） | 解析ソフト: IDA / 解析モデル: opus-5。`tools/hw/unitcursor_hw.py:356` は node行列を | HIGH | ? |  |  |
| ACNL-F0550 | 木1体の専用材質で透明度変更（2026-09-20、HIGH） | 解析ソフト: IDA / 解析モデル: gpt-6-astra。ゲームのcopy関数0x4ADD44(mask0x800)で専用ResMaterialを作りMaterial+80をredirect。SimpleMaterialActivator0x4A17B8はMaterial+8のみを読むので、それだけでは無効。このinstanceのRTTI/vtable4slotを複製しActivateだけgeneric0x49C08Cへ替えると、constant-alpha RGB b | HIGH | ? |  |  |
| ACNL-F0552 | 独立した木を表示・非表示。ゲーム座標には曲面変換が必要（2026-09-20、HIGH） | 解析ソフト: IDA / 解析モデル: gpt-6-astra。実機の準備済みSeason資源から `fg_treeA_4` のordinary Modelを独立生成し、player右36・倍率0.5で表示、OFFで消去を確認。マップの設置データは変更していない。主題・限界は [tree_live_plan](../docs/topics/tree_live_plan.md)。 | HIGH | ? |  |  |
| ACNL-F0553 | 行列経路は正常だった。残る差は node+0x228 / +0x22C（2026-09-19、HIGH、実機＋対照） | 設計（`docs/topics/unit_cursor_hw_plan.md` §9）→ 検証（51 件 ok）→ 実装 → 検査（0 failed）→ 適用の順で測定した。 | HIGH | ? |  | 訂正あり |
| ACNL-F0554 | 実機測定で IDA-unknown-F027 を棄却。頂点バッファの束縛は正しい（2026-09-18、HIGH、実機） | 設計（docs/topics/unit_cursor_hw_plan.md）→ 検証（tools/hw/verify_unitcursor_hw.py、45 件 ok）→ 実装（tools/hw/unitcursor_probe.py） | HIGH | ? |  |  |
| ACNL-F0555 | 頂点バッファの番地は VA→GPU 変換を通り、対応外の領域では黙って 0 になる（2026-09-18、HIGH、静的） | IDA-unknown-F026 で「頂点属性コマンド列は sub_7E5710 が組み立てる」と分かったので中身を読んだ。 | HIGH | ? |  |  |
| ACNL-F0556 | メッシュのコマンド列は誰が作るか。「ジオメトリが欠けている」仮説の反証（2026-09-18、HIGH、静的） | IDA-unknown-F025 で「メッシュの GPU コマンド列は 2 本ある」と分かったので、1 本目（頂点属性・バッファ束縛）の出どころを追った。 | HIGH | ? |  |  |
| ACNL-F0557 | 過去の静的解析の誤り 2 件と見落とし 1 件（2026-09-18、HIGH） | 自前の UnitCursor が「描画経路のふるいを全部通るのに画素が 1 つも出ない」という実機結果を受けて、記録済みの静的結論を洗い直した。3 件の瑕疵が見つかった。 | HIGH | ? |  | 訂正あり |
| ACNL-F0558 | 描画順は静的に確定できる。描画状態は bcres の PICA コマンド列にある（2026-09-18、MEDIUM） | 利用者の見立て「描画順は静的解析で確認できるはず」は正しかった。(1) **描画順＝マテリアルのレイヤー**。Scene_DrawLayers 0x4EB840 は外側で i=0..3 を回し、メッシュごとに material→(+8 の元 ResMaterial)+32 の下位バイトが i と一致するときだけ sub_48D26C 0x48D26C で GPU コマンドを積む（FuncNode は i==0 で node[82]、i==1 で node[83] のコールバッ | MEDIUM | ? |  | 訂正あり |
| ACNL-F0559 | 屋外表示の未解明点のうち4件を解決（ホルダ型・Create引数・マス換算・フック候補）（2026-09-18、MEDIUM） | (1) 資源ホルダ: ScStage ctor 0x7F195C（ScStage は 3504B）から、ScStage+0x418 = ssys::ma::HeapAllocator（8B、ctor HeapAllocator_Ctor 0x5667E8 / dtor 0x317CBC）、ScStage+0x420 = G3D 資源ホルダ（g3d::ResourceLoader＋ResourceSet、**264B**、0x420〜0x528。ctor G3dResHolde | MEDIUM | ? |  | 訂正あり |
| ACNL-F0560 | Scene_SubmitNode のシーン番号は 0=通常描画・1=別モード・2=影マップ（2026-09-18、MEDIUM） | Render_InitGlobal 0x4E97CC が SceneContext/SceneTraverser を 3 本作る（g_SceneContexts 0x9C3098 / g_SceneTraversers 0x9C30A4）。Scene_DrawLayers 0x4EB840 の呼び出し元は 2 つで、Render_DrawScene2 0x4E976C が影マップ（g_SceneContext_2、IDA-unknown-F008）、Render_DrawSc | MEDIUM | ? |  |  |
| ACNL-F0561 | UnitCursor を屋外で出すための足場と不足（2026-09-18、MEDIUM） | 資源読み込みの入口を確定: G3dResHolder_RequestLoad 0x317920 → FileRes_RequestLoadAligned 0x569D94 → FileRes_RequestLoadAsync 0x569BA0。後者は**非同期**でホルダ+232 が状態（0未要求/1要求/2同期/3,4,5完了）、+68 パス・+204 ヒープ・+228 アライン・+233 非同期旗。戻り値は完了か。完了まで毎フレーム呼び直す必要があり（ScStage_Pr | MEDIUM | ? |  |  |
| ACNL-F0562 | 家具モデルは屋外でも出る（部屋ごとの収容数）。UnitCursor だけが屋内限定（2026-09-18、MEDIUM） | 利用者の指摘（オートキャンプは屋外判定で家具モデルを表示）を受けて IDA-unknown-F019 の表現を訂正。Room_GetFurnitureCapacity 0x5B5E18 が引く g_RoomFurnitureCapacity 0x8835BC は屋外でも非0で、村 0x00=38、Downtown 0x01=2、オートキャンプ場 0x9F/0xA0=10、カー内部 0xA1/0xA2=36、家1F 0x03=48。BsFtrMgr_CreateResource | MEDIUM | ? |  |  |
| ACNL-F0563 | 模様替えの家具の下の範囲表示は UnitCursor モデル、屋外では資源もクラスも無い（2026-09-18、MEDIUM） | 正体はパーティクルでなく 3D モデル romfs/Ftr/Chip/UnitCursor.bcres（モデル UnitCursor/UnitCursorLine/UnitCursorNG/UnitCursorRotate、m_UnitCursor の Visibility/MaterialColor アニメ）。読み込みは ScStage_LoadIndoorRes 0x611928 が部屋フラグ8（屋内、ItemIndoor.bin と同条件）のときだけ専用ヒープ Unit | MEDIUM | ? |  | 訂正あり |
| ACNL-F0571 | 木と家具の共通モデル生成・姿勢設定（2026-09-14、MEDIUM） | 木を含むfieldオブジェクトはItem_GetFieldObjDef→def+0xC→manager+0x414の22-byte shape表→名前+5→0x5992D4→0x4A5F20→0x58EEC0→0x4F048C。家具も同じModelInstance_Createに到達する。holder経由のtranslation/matrix/scaleと破棄入口を特定・命名。Create返値成功だけではholder+4非nullを保証しない。 | MEDIUM | ? |  |  |
| ACNL-F0572 | 木の実体とSeason資源を原本照合（2026-09-17、MEDIUM） | 更新Fg.binのItem0x26→shape0x25→base FgShape.binのfg_treeA_4。strideは元ARMの索引コードで決定。全23 Season00..22のモデル辞書と自身の名称が一致し、type0x40000012・mesh/material各1。ctrtool展開済み25資源を独立RomFS parserで原本bytesと照合PASS。base展開全体は10753/12938のPARTIAL、updateは4150/4150完了であり、全展 | MEDIUM | ? |  |  |
| ACNL-F0573 | Create全引数・instance共有範囲・更新/破棄（2026-09-17、MEDIUM） | 正常callerのR0=holder、R1=ResModel、R2/R3=HeapAllocator、stack=mask0/flag0/count1をassembly照合。普通Model本体0x220、holderのRTTIとは別。mesh記述子等はinstanceへコピーするがgeometry/textureとmask0のmaterial fieldは共有。Material_GetResourceForMaskが資源/privateを選ぶ。world更新→条件付き骨格更新 | MEDIUM | ? |  |  |
| ACNL-F0574 | サイズqueryとOOM・ready・owner寿命（2026-09-17、MEDIUM） | 元命令を原本codeと照合し、ARM11MPCoreでquery経路のみ実行。独立allocation ledgerと23 Season×mask0/0x10の46ケース一致。932/1664 bytes・最大alignment32はbuilder見積もりで、heap管理・size+align・資源/GPUメモリを除く。OOM時は0x4AB4A0でnull vtable参照、Setup結果も伝播されず事後検査だけでは安全でない。fgobj::ProcはSetup完了前にglo | MEDIUM | ? |  | 訂正あり |
| ACNL-F0575 | resource描画属性・scene番号・画面を区別（2026-09-14、MEDIUM） | 0x317BD0の旧名ModelInstance_SetRenderLayerは誤解を招く。0x58E978のcallerは資源lookup結果を渡した後でinstanceを作り、関数内も相対辞書を変更する。ResModel_SetRenderLayerへ改名。共有資源を個別instanceの設定として変更しない。 | MEDIUM | ? |  |  |
| ACNL-F0591 | ウィンドウの中身にテクスチャがあるなら UV の組が要る（無いと nwlyt_CalcTexCoordsForGpu が落ちる）（2026-10-05、HIGH: 実機のクラッシュ + 静的） | 解析ソフト IDA（ida-pro-mcp / idalib-mcp）、解析モデル opus-5.5。T013 段 2 の実機試験。 | HIGH | S |  |  |
| ACNL-F0592 | 実行時のテクスチャ差し替えと性別の読み方を実機で確認（2026-10-05、HIGH: 静的 + 実機） | 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。T013 段 3（gohan work/hhd-charcreate 4c6db33、3gx fda07ad4…d0c5）。 | HIGH | S |  |  |
| ACNL-F0598 | レイアウトの材質の TEV の段と座標生成の意味（2026-10-05、HIGH 相当: 逆アセンブル + ACNL の実在の材質 215 個と照合。実機の描画は未確認） | 解析モデル opus-5.5。IDB: `nwlyt_Material_EmitTevStages 0x4B8790`（命名・注記）、`nwlyt_CalcTexCoordsForGpu 0x73B650`（注記）。 | HIGH | S |  |  |
| ACNL-F0599 | 上画面の描画順と「メニューの 3D」モード（Scene 1）、美容室の小物の音、複製の帽子・肌の欄（2026-10-05、MEDIUM: 静的のみ。gohan での使用は実機未確認） | 解析モデル opus-5.5。IDB: `Player_SetHeadGoodsWithSound 0x68B238` を命名・注記。 | MEDIUM | S |  |  |
| ACNL-F0600 | 部屋の内部名の表、メッシュ 1 つを半透明で描く命令の挟み方、T018 第 1 段の実機（2026-10-05、HIGH（部屋の表: ID 一覧とゲームの表の 2 経路）/ MEDIUM（半透明: 静的、実機未確認）） | 解析モデル opus-5.5。IDB: `g_RoomInternalNames 0x9515F0`（命名・注記）、`gfx_DrawMesh 0x48D26C` に注記。 | HIGH | S |  |  |
| ACNL-F0617 | ACNL の品番 → モデル名の表と、HHD との品物の突き合わせ（2026-10-06、MEDIUM〜HIGH: 静的 2 本 + ROM の実データ） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022 の下調べ。 | MEDIUM | S |  |  |
| ACNL-F0645 | balloon ARの旧code caveが既存描画caveと衝突していた | **確度: HIGH（添付Ghidra XMLの既存allocation map＋crash_dump_00000007＋ユーザー実機挙動）。** | HIGH | B |  |  |
| ACNL-F0692 | AcObjUnitCursor の尺度は家具サイズ、Rotate アニメは UV 回転で決まる（F0563 再解析） | AcObjUnitCursor は家具サイズによる5種類の尺度と、家具角度による4種類のUV回転を別々に設定する。UnitCursor.bcres は1モデル・3本のマテリアルアニメを持ち、標準の読み込みは部屋フラグ0x8に依存する。追加・削除はModuleFtrのimport経由で呼ばれる。 | MEDIUM | A |  |  |
| ACNL-F0695 | Layout 再生時の主リスト記帳は条件付きで未提出範囲を取り込む（再解析） | 再生関数は主リストの現在位置と提出済み位置を比較し、条件により分割提出または最初のコマンドエントリへの結合を行う。主リストへの直接追記が常に提出・表示されるという保証ではない。 | MEDIUM | A |  |  |
