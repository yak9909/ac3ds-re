<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / ui

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0088 | F-50 UI アニメと画面遷移（Wipe）— 調整点は `0x568BF8` 一箇所 — `HIGH` | 「持ち物・マイデザを開くときの画面遷移を一瞬にしたい」の解析。**静的 IDB のみで実施。** | HIGH | ? |
| ACNL-F0116 | F-78: タブ退場開始条件は要求成功ではなく実画面のmenu flag `0x08` | confidence: **HIGH**（`sub_6D6060` / `Menu_PollOpen` を `code.bin.i64` で確認、 | HIGH | ? |
| ACNL-F0117 | F-79: 実画面生成成功の同期点は `Menu_PollOpen -> UiScreen_OpenById` の戻り | confidence: **HIGH**（`Menu_PollOpen` disassemblyと実機pending残留を照合）、 | HIGH | ? |
| ACNL-F0161 | F-123: ★★TODO-87 — 影のテクスチャの実体を特定し、書き換えて画面に反映させた | confidence: **HIGH**（実機。A/B を 3 回切り替えて目視確認） | HIGH | ? |
| ACNL-F0162 | F-124: ★★★TODO-90 達成 — 自前の画像を任意のフォーマットで画面に表示した | confidence: **HIGH**（実機。ユーザーの目視で「はっきりした市松模様の影が一つだけ」を確認） | HIGH | ? |
| ACNL-F0207 | F-181: ★★★自前の UI 画像を毎フレーム 1 枚、画面に出せた。アルファブレンドも効く — `HIGH`（実機で視認） | 適用: `PATCHES/cave_add_sprite.py` | HIGH | ? |
| ACNL-F0228 | F-203: ★★★★★最後に再生されるレイアウトは固定。注入点が確定 — `HIGH`（実機 301 フレーム） | `PATCHES/probe_layout_order.py`。 | HIGH | ? |
| ACNL-F0229 | F-204: ★★★レイアウトの記録は「記録要求フラグ」が立っているときだけ走る — `HIGH`（静的＋実機） | `0x568770` の NOP に相乗りしたのに **発火 0 回**だった。原因は入口の門番。 | HIGH | ? |
| ACNL-F0233 | F-208: ★★★★★レイアウトごとに投影が違う。相乗り先を変えたら縮尺を測り直す — `HIGH`（実機） | リスト id 15 のレイアウトの座標系は **等方で 1 単位 = 1px、原点は画面中央、320x240**。 | HIGH | ? |
| ACNL-F0256 | F-231: ★★★★★リスト id 0 を「未設定」として弾かないと、id 0 のレイアウトと誤って一致する — `HIGH`（実機） | デバッガから入れたケーブでは正しく動くのに、**プラグインでは** | HIGH | ? |
| ACNL-F0257 | F-232: ★★★★★レイアウトの記録リストには容量がある。積みすぎると落ちる — `HIGH`（実機） | 自前メニューを描かせたら、ロード画面へ入るところで落ちた。 | HIGH | ? |
| ACNL-F0259 | F-234: ロード画像は上画面で id 8 の後に replay される Layout id 10 — `HIGH`（静的＋実機＋リソース同定） | ユーザーがロード画像を目視した状態で Suspend し、再開すればロードが終わる条件だったため、 | HIGH | ? |
| ACNL-F0261 | F-238: ロード表示中でも top LayoutList の構成はフェーズで変わる — `MEDIUM`（独立した stopped snapshot＋no-draw 実行標本） | F-234 の replay ring は、ロード中の一つの上画面 pass で id `0x08 -> 0x0A` を記録した。 | MEDIUM | ? |
| ACNL-F0262 | F-241: lifecycle trace の block-copy emitter は loader Layout を破損する — `HIGH`（生成命令＋実機レジスタ＋破損メモリ） | `probe_loader_submit_lifecycle.py` の F-240 emitter は安全ではなかった。`LOG=0x009B3000` 自体は | HIGH | ? |
| ACNL-F0264 | F-236: Layout record-list のバッファ本体は安全に差し替える必要がある — `MEDIUM`（静的＋ゼロ長実機経路） | 外部会話ログ `REFERENCES/TEXTS/render.txt` は「描画コマンド追加・順番変更・コマンド | MEDIUM | ? |
| ACNL-F0277 | F-254: ★★★★★自前の Layout ノードを登録すれば、上下とも「最前面」に必ず入れる — `HIGH`（実機） | F-253 で分かった `LayoutMgr_AddLayout` を使い、**自前の偽 Layout ノード**を毎フレーム | HIGH | ? |
| ACNL-F0278 | F-255: 自前 Layout ノードから実際に描けた。ロード画像より前面 — `HIGH`（実機・目視） | F-254 の空ノードに描画を載せた。`PATCHES/cave_node_draw.py` | HIGH | ? |
| ACNL-F0287 | F-264: 自前ノードの幅・高さは雛形任せにせず画面実寸を明示する — `HIGH`（静的のみ） | `Layout_ReplayRecordedList`（`0x5682DC`）は scissor コマンドの値を | HIGH | ? |
| ACNL-F0288 | F-265: ★★★★★UI の投影行列の出所を確定した。**Layout+0x34 の 16 語**であり、記録時ではなく**再生時**に GPU へ流れる — `HIGH`（静的のみ） | 長年「投影は直前の有効 Layout が Drawer に残した状態へ依存する」（F-233/F-234） | HIGH | ? |
| ACNL-F0303 | F-278: 座標系を上下とも静的に確定した。**1 単位 = 1px、原点は画面中央**。`c4` は恒久的にゼロ — `HIGH`（静的、実機実測と一致） | `nwlyt_Drawer_EmitProjectionUniform` が吐く 24 語を機械的に展開した。 | HIGH | ? |
| ACNL-F0312 | F-288 — Chokistream の画面を AI が直接見られる（動的解析の目視確認を自動化） | **結論: 見られる。** `PATCHES/grab_screen.ps1` で PNG にすれば、そのまま読める。 |  | ? |
| ACNL-F0315 | F-291 (HIGH・静的のみ) — ★正体は **nw::lyt（NintendoWare Layout）**。Picture / Material の構造を静的に確定し、**既存文書の誤り 6 件を訂正** | `code.bin.i64` だけで詰めた（動的解析なし）。全文は `scratchpad/MEMO_f291_nwlyt_static.md`。 | HIGH | ? |
| ACNL-F0321 | F-297 (HIGH・実機) — ★下画面のペインツリーを組んだ。**上下 2 画面が独立した輪で同時に描かれる** | F-295 の時点では下画面のノード（`0x9B5400`）は用意だけされていて | HIGH | ? |
| ACNL-F0326 | F-302 (HIGH・実機) — ★★TextBox が実機で描けた。**作業オブジェクト = `LayoutMgr + 0x1C`**。コードケーブ 0 語 | F-301 の結論を実機で検証し、残っていた「作業オブジェクト」を解明した。 | HIGH | ? |
| ACNL-F0446 | アニメの適用段は sub_48A844。画面で動いた（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**F012 で欠けていた「適用」段を特定し、実機で絵が変わった。** | HIGH | ? |
| ACNL-F0494 | 一覧の切り抜きは N_frame_00 から作るシザー。一覧の Layout は自前のデータで先に組み立てられる（2026-09-25、MEDIUM: 静的＋利用者の見た目の報告。組み立ては実機未確認） | `sub_1C55F8`（組み立て段 2 から呼ばれる）: N_frame_00（一覧+536）の大域行列の位置と大きさから、一覧+356 = 1、+360/+364 = 画面の x/y（回した座標）、+368/+372 = 幅/高さを置く。一覧+356 は ssys Layout（一覧+44）の +312 にあたる切り抜き。行の 7 行目が半分隠れるのも、名前の左の空き（N_frame_00 の左端 62.5 より左）に置いた文字が見えないのもこの切り抜き（利用者は「リスト | MEDIUM | S |
| ACNL-F0526 | 足元のアイテムは Field_MarkDirty で、下画面の地図は作成段 9 の呼び直しで更新できる（2026-09-23、**HIGH（静的＋実機）**） | 解析ソフト: IDA / 解析モデル: opus-5.5。F004 の実機確認のあとの利用者の依頼 | HIGH | S |
| ACNL-F0551 | 専用view/projectionで画面固定、pixel配置・倍率・alpha併用（2026-09-20、HIGH） | 解析ソフト: IDA / 解析モデル: gpt-6-astra。replay直後NOP0x4EF1B0へ最小late passを設置。CameraBind0x494D3C(lowCtx,privateSource,1)→DrawMesh0x48D26C(**[0x94CA48]**,mesh,node)→CameraBind(lowCtx,元camera,1)。world登録OFF、global cameraへの書込みなし。sourceのview+328/projection | HIGH | ? |
| ACNL-F0569 | しずえ画面「準備中」の仕事はSvProc種別4、中で日替わり処理と寝癖（2026-09-17、HIGH） | ModulePlSelect case0の記述子this+632（flags 0x24000942、+32 sub_5254C0）はsub_2388BCがthis+0x16Cへ入れ、talk driverはthis+0x168（vtbl 0x8F46D8→TalkSaveTask_Step 0x237868）を毎フレーム叩く（旧「this+632を叩く」を訂正）。StepがSvProc_StartThread 0x3046C0で「SvProc Thread」を作り、ProcT | HIGH | ? |
| ACNL-F0589 | 自前の DARC をメモリから渡して下画面にレイアウトを出せる（2026-10-05、HIGH: 静的 + 実機） | 解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。D005 / T012 の最小の実機確認。 | HIGH | S |
| ACNL-F0594 | HHD の「ペインに投影」の座標生成を ACNL の UV で再現する規則（HHD-T006 の水玉の謎の答え）（2026-10-05、MEDIUM: レイアウトのデータ 2 種と HHD のスクショの照合。HHD のコードは未読） | 解析ソフト: なし（3DSkit の BFLYT の読み + acnl-ui-designer の描画）。解析モデル opus-5.5。段階 2（上画面）の変換で判明。 | MEDIUM | S |
| ACNL-F0611 | Layout ノード 1 つにつき 1 枚のシザー（自前の候補欄の切り抜きに使う）（2026-10-06、HIGH: 静的 + 実機。縦の向きは実機で訂正） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | HIGH | S |
