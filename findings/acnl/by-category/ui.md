<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / ui

| ID | 題 | summary | 確度 | 格付け | consolidated_into | 訂正 |
|---|---|---|---|---|---|---|
| ACNL-F0035 | F-149: 会話本文フレームを構成する6 PictureとTextBoxを、相対配置のまま複製できた — `HIGH`（静的＋実機） | F-148のcommit点を使い、list 32の末尾へ `P_bg_L_00` / `P_bg_R_00` / `P_soft_L` / | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0036 | F-148: 既存Pictureを非所有cloneして、任意座標の2D背景として追加できた — `HIGH`（静的＋実機） | F-147で確定したPane-treeのcommit直前、`nwlyt_DrawPaneTreeToCurrentList` (`0x4D7174`) の | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0087 | F-49 メッセージ表示の仕組みと「メニューアニメーションをカット」の副作用 — `HIGH` | `REFERENCES/CHEATS/ui.txt` の「メニューアニメーションをカット」で | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0088 | F-50 UI アニメと画面遷移（Wipe）— 調整点は `0x568BF8` 一箇所 — `HIGH` | 「持ち物・マイデザを開くときの画面遷移を一瞬にしたい」の解析。**静的 IDB のみで実施。** | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0089 | F-51 フェードの正体は `FaderColor`、`FaderMoment` に差し替えれば消える — `HIGH` | F-50 で「`0x568BF8` が唯一の調整点」と書いたが、**フェードには効かない。** | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0095 | F-57 ゲーム内メニューを ID で開く仕組み — 日付変更ウィンドウは `MenuID 0x2E` — `HIGH` | 「ゲーム内の時間変更ウィンドウを呼び出すチートがあったはず」という問いの答え。 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0109 | F-71: 通常Xの実入口は `sub_6D62AC` の動的menuId呼出し `0x6D6338` | confidence: **HIGH**（`code.bin.i64` の制御フローと実機breakpoint・引数・LRを照合） | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0116 | F-78: タブ退場開始条件は要求成功ではなく実画面のmenu flag `0x08` | confidence: **HIGH**（`sub_6D6060` / `Menu_PollOpen` を `code.bin.i64` で確認、 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0117 | F-79: 実画面生成成功の同期点は `Menu_PollOpen -> UiScreen_OpenById` の戻り | confidence: **HIGH**（`Menu_PollOpen` disassemblyと実機pending残留を照合）、 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0118 | F-80: `BsMenuCatalog` は通常下画面メニューの `0x08/0x10` handshakeを実装しない | confidence: **HIGH**（`code.bin.i64` の全直接xref、`BsMenuItem` と | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0121 | F-83: `BsFtrMgr` のglobal公開は生成完了より早く、完全readyはobject `+19` の下位2bit | confidence: **MEDIUM**（`code.bin.i64` のvtable、create wrapper、3 phaseを静的照合） | MEDIUM | ? | topics/acnl/ui.md |  |
| ACNL-F0124 | F-86: parent拒否説を撤回。`ScStage` と`BsMenuTab`はいずれもchild gateを通る | confidence: **HIGH**（`UiScreen_OpenChild` の静的条件と停止中実機byteの精密再読を照合） | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0161 | F-123: ★★TODO-87 — 影のテクスチャの実体を特定し、書き換えて画面に反映させた | confidence: **HIGH**（実機。A/B を 3 回切り替えて目視確認） | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0162 | F-124: ★★★TODO-90 達成 — 自前の画像を任意のフォーマットで画面に表示した | confidence: **HIGH**（実機。ユーザーの目視で「はっきりした市松模様の影が一つだけ」を確認） | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0201 | F-175: ★★★Picture は毎フレーム必ず描かれる。TextBox ではなく Picture に相乗りすべきだった — `HIGH`（実機で計測） | 適用: `PATCHES/measure_picture_draws.py` | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0203 | F-177: ★★★`nwlyt_Pane_DrawRecursive` は 1 フレームも欠けない。TODO-115 の答え — `HIGH`（実機で計測） | 適用: `PATCHES/measure_pane_draws.py` | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0207 | F-181: ★★★自前の UI 画像を毎フレーム 1 枚、画面に出せた。アルファブレンドも効く — `HIGH`（実機で視認） | 適用: `PATCHES/cave_add_sprite.py` | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0224 | F-199: ★★★★★UI の座標系を確定。**縦横で縮尺が違う（非等方）** — `HIGH`（実機で段階的に測定） | \| 項目 \| 値 \| | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0228 | F-203: ★★★★★最後に再生されるレイアウトは固定。注入点が確定 — `HIGH`（実機 301 フレーム） | `PATCHES/probe_layout_order.py`。 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0229 | F-204: ★★★レイアウトの記録は「記録要求フラグ」が立っているときだけ走る — `HIGH`（静的＋実機） | `0x568770` の NOP に相乗りしたのに **発火 0 回**だった。原因は入口の門番。 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0230 | F-205: ★★★★「最後に再生される」は画面（描画パス）ごとに違う — `HIGH`（実機 120 フレーム） | > **★F-253 で一部訂正した。単体で読まないこと。** 描画パスは 2 本ではなく **3 本**あり、 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0233 | F-208: ★★★★★レイアウトごとに投影が違う。相乗り先を変えたら縮尺を測り直す — `HIGH`（実機） | リスト id 15 のレイアウトの座標系は **等方で 1 単位 = 1px、原点は画面中央、320x240**。 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0249 | F-224: ★★★★★確定した対象を「0 以外のときだけ更新」してはいけない — `HIGH`（実機） | F-223 の対策を入れてもまだ落ちた。ただし条件がはっきりした。 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0251 | F-226: ★★★★★相乗り先は「素で記録し直される」ものから選ぶ。強制は廃止 — `HIGH`（実機） | F-223 / F-224 の対策を入れても、しばらく遊ぶとまだ落ちた。 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0253 | F-228: ★★★★フェードは id 8（上）/ id 9（下）が最後に描く。両方に積めば判別が要らない — `HIGH`（実機） | ロード時のフェードで自前 GUI も一緒に暗くなる、という報告から。 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0256 | F-231: ★★★★★リスト id 0 を「未設定」として弾かないと、id 0 のレイアウトと誤って一致する — `HIGH`（実機） | デバッガから入れたケーブでは正しく動くのに、**プラグインでは** | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0257 | F-232: ★★★★★レイアウトの記録リストには容量がある。積みすぎると落ちる — `HIGH`（実機） | 自前メニューを描かせたら、ロード画面へ入るところで落ちた。 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0259 | F-234: ロード画像は上画面で id 8 の後に replay される Layout id 10 — `HIGH`（静的＋実機＋リソース同定） | ユーザーがロード画像を目視した状態で Suspend し、再開すればロードが終わる条件だったため、 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0261 | F-238: ロード表示中でも top LayoutList の構成はフェーズで変わる — `MEDIUM`（独立した stopped snapshot＋no-draw 実行標本） | F-234 の replay ring は、ロード中の一つの上画面 pass で id `0x08 -> 0x0A` を記録した。 | MEDIUM | ? | topics/acnl/ui.md |  |
| ACNL-F0262 | F-241: lifecycle trace の block-copy emitter は loader Layout を破損する — `HIGH`（生成命令＋実機レジスタ＋破損メモリ） | `probe_loader_submit_lifecycle.py` の F-240 emitter は安全ではなかった。`LOG=0x009B3000` 自体は | HIGH | ? |  |  |
| ACNL-F0264 | F-236: Layout record-list のバッファ本体は安全に差し替える必要がある — `MEDIUM`（静的＋ゼロ長実機経路） | 外部会話ログ `REFERENCES/TEXTS/render.txt` は「描画コマンド追加・順番変更・コマンド | MEDIUM | ? | topics/acnl/ui.md |  |
| ACNL-F0275 | F-252: 2D レイアウトの描画は「1 本のリストを画面ごとに 2 回再生」する — `HIGH`（静的。動的照合は未実施） | > **★F-253 で大幅に訂正した。単体で読まないこと。** リストは 1 本ではなく 2 本（`mgr+0x04`=上画面 / `mgr+0x10`=下画面）、 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0277 | F-254: ★★★★★自前の Layout ノードを登録すれば、上下とも「最前面」に必ず入れる — `HIGH`（実機） | F-253 で分かった `LayoutMgr_AddLayout` を使い、**自前の偽 Layout ノード**を毎フレーム | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0278 | F-255: 自前 Layout ノードから実際に描けた。ロード画像より前面 — `HIGH`（実機・目視） | F-254 の空ノードに描画を載せた。`PATCHES/cave_node_draw.py` | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0287 | F-264: 自前ノードの幅・高さは雛形任せにせず画面実寸を明示する — `HIGH`（静的のみ） | `Layout_ReplayRecordedList`（`0x5682DC`）は scissor コマンドの値を | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0288 | F-265: ★★★★★UI の投影行列の出所を確定した。**Layout+0x34 の 16 語**であり、記録時ではなく**再生時**に GPU へ流れる — `HIGH`（静的のみ） | 長年「投影は直前の有効 Layout が Drawer に残した状態へ依存する」（F-233/F-234） | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0303 | F-278: 座標系を上下とも静的に確定した。**1 単位 = 1px、原点は画面中央**。`c4` は恒久的にゼロ — `HIGH`（静的、実機実測と一致） | `nwlyt_Drawer_EmitProjectionUniform` が吐く 24 語を機械的に展開した。 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0312 | F-288 — Chokistream の画面を AI が直接見られる（動的解析の目視確認を自動化） | **結論: 見られる。** `PATCHES/grab_screen.ps1` で PNG にすれば、そのまま読める。 |  | ? |  |  |
| ACNL-F0313 | F-289 (HIGH・実機) — ★`nwlyt_Picture_DrawToCommandList` に**自前 Picture** を渡して 1 枚描けた | `0x73CB58 nwlyt_Picture_DrawToCommandList(picture, cursor, a3, drawctx)` は | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0315 | F-291 (HIGH・静的のみ) — ★正体は **nw::lyt（NintendoWare Layout）**。Picture / Material の構造を静的に確定し、**既存文書の誤り 6 件を訂正** | `code.bin.i64` だけで詰めた（動的解析なし）。全文は `scratchpad/MEMO_f291_nwlyt_static.md`。 | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0317 | F-293 (HIGH・実機) — ★★★正規の手順で描けた。**自前の記録ケーブ 205 語を撤去** | F-292 の設計を実装し実機で成功した。道具は `PATCHES/build_pane_tree.py`。 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0319 | F-295 (HIGH・実機) — ★方式 (a) 完成。ヒープから借りて**メニュー全体を正規経路で描いた** | 道具は `PATCHES/alloc_lyt_heap.py`（確保）と `PATCHES/build_pane_tree.py`（組み立て）。 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0321 | F-297 (HIGH・実機) — ★下画面のペインツリーを組んだ。**上下 2 画面が独立した輪で同時に描かれる** | F-295 の時点では下画面のノード（`0x9B5400`）は用意だけされていて | HIGH | ? | topics/acnl/ui.md | 訂正あり |
| ACNL-F0326 | F-302 (HIGH・実機) — ★★TextBox が実機で描けた。**作業オブジェクト = `LayoutMgr + 0x1C`**。コードケーブ 0 語 | F-301 の結論を実機で検証し、残っていた「作業オブジェクト」を解明した。 | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0446 | アニメの適用段は sub_48A844。画面で動いた（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**F012 で欠けていた「適用」段を特定し、実機で絵が変わった。** | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0460 | ゲーム共通の 8 行リスト InstSelect<8> を下画面だけ借りる部品の作り（2026-09-25、MEDIUM: 静的＋実機の欄の読み取り。描画は未試験） | 公共事業のリストは `PWorkList : InstSelect<8> : SelectBase : CatalogBase`（RTTI）。`InstSelect<8>`（vtbl `0x8E54B4`、ctor `sub_7C6EB0`、4,812 B）は派生 10 種が共有する**ゲーム共通の 8 行リスト**で、純粋仮想は vt[13]（一覧を作る・件数 +2500）と vt[25]（i 行目の語）だけ。 | MEDIUM | S | topics/acnl/ui.md |  |
| ACNL-F0471 | 村の下画面の建物一覧（BsMenuMapList）の作りと、マップエディターのモード一覧への流用（2026-09-28、MEDIUM: 静的＋描画器での照合。gohan 実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示: 地図の右の建物一覧をマップエディターの下画面左端に出し、 | MEDIUM | S | topics/acnl/ui.md |  |
| ACNL-F0491 | 共通ボタン（cmn_btn / btn_pos）・時計とベルの箱（time_bel_win）の組み立てと状態の規則（2026-09-25、HIGH: 静的＋実機画像 2 枚） | 設計ツール `src/acnl-ui-designer`（ef9b19c）の `cmnbutton.mjs` / `timebel.mjs` の根拠。表は同リポジトリ `docs/verification.md`。 | HIGH | S | topics/acnl/ui.md |  |
| ACNL-F0492 | 一覧の選択中の行とスクロールバー（CommonScrollBar）の見た目の規則（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合） | 設計ツール `src/acnl-ui-designer`（3af30a5）の `instselect.mjs` / `scrollbar.mjs` の根拠。表は同リポジトリ `docs/verification.md`。 | HIGH | S | topics/acnl/ui.md |  |
| ACNL-F0494 | 一覧の切り抜きは N_frame_00 から作るシザー。一覧の Layout は自前のデータで先に組み立てられる（2026-09-25、MEDIUM: 静的＋利用者の見た目の報告。組み立ては実機未確認） | `sub_1C55F8`（組み立て段 2 から呼ばれる）: N_frame_00（一覧+536）の大域行列の位置と大きさから、一覧+356 = 1、+360/+364 = 画面の x/y（回した座標）、+368/+372 = 幅/高さを置く。一覧+356 は ssys Layout（一覧+44）の +312 にあたる切り抜き。行の 7 行目が半分隠れるのも、名前の左の空き（N_frame_00 の左端 62.5 より左）に置いた文字が見えないのもこの切り抜き（利用者は「リスト | MEDIUM | S | topics/acnl/ui.md |  |
| ACNL-F0526 | 足元のアイテムは Field_MarkDirty で、下画面の地図は作成段 9 の呼び直しで更新できる（2026-09-23、**HIGH（静的＋実機）**） | 解析ソフト: IDA / 解析モデル: opus-5.5。F004 の実機確認のあとの利用者の依頼 | HIGH | S | topics/acnl/ui.md |  |
| ACNL-F0551 | 専用view/projectionで画面固定、pixel配置・倍率・alpha併用（2026-09-20、HIGH） | 解析ソフト: IDA / 解析モデル: gpt-6-astra。replay直後NOP0x4EF1B0へ最小late passを設置。CameraBind0x494D3C(lowCtx,privateSource,1)→DrawMesh0x48D26C(**[0x94CA48]**,mesh,node)→CameraBind(lowCtx,元camera,1)。world登録OFF、global cameraへの書込みなし。sourceのview+328/projection | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0569 | しずえ画面「準備中」の仕事はSvProc種別4、中で日替わり処理と寝癖（2026-09-17、HIGH） | ModulePlSelect case0の記述子this+632（flags 0x24000942、+32 sub_5254C0）はsub_2388BCがthis+0x16Cへ入れ、talk driverはthis+0x168（vtbl 0x8F46D8→TalkSaveTask_Step 0x237868）を毎フレーム叩く（旧「this+632を叩く」を訂正）。StepがSvProc_StartThread 0x3046C0で「SvProc Thread」を作り、ProcT | HIGH | ? | topics/acnl/ui.md |  |
| ACNL-F0588 | nw::lyt の Window は 1 枠でも描ける（2026-10-05、MEDIUM: 静的 + designer の再現がスクショと一致） | 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。HHD の画面を ACNL で再現する作業（D005 / T011）の周辺で確認。 | MEDIUM | S | topics/acnl/ui.md |  |
| ACNL-F0589 | 自前の DARC をメモリから渡して下画面にレイアウトを出せる（2026-10-05、HIGH: 静的 + 実機） | 解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。D005 / T012 の最小の実機確認。 | HIGH | S | topics/acnl/ui.md |  |
| ACNL-F0593 | カタログを開くときの遷移は BsMenuBg の切り替え（クロスフェード）と画面自身の in アニメ。Fade / Wipe / Fader は使わない（2026-10-05、HIGH: 静的 + 実機の否定観測） | 解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。段階 2（上画面と遷移）の下調べ。**既存資料**: 旧 RE/FINDINGS.md F-50（Wipe、UiAnim のレート）/ F-51（Fade・Fader 9 個と Fader_SetKind の種類）、 | HIGH | S | topics/acnl/ui.md |  |
| ACNL-F0594 | HHD の「ペインに投影」の座標生成を ACNL の UV で再現する規則（HHD-T006 の水玉の謎の答え）（2026-10-05、MEDIUM: レイアウトのデータ 2 種と HHD のスクショの照合。HHD のコードは未読） | 解析ソフト: なし（3DSkit の BFLYT の読み + acnl-ui-designer の描画）。解析モデル opus-5.5。段階 2（上画面）の変換で判明。 | MEDIUM | S | topics/acnl/ui.md |  |
| ACNL-F0611 | Layout ノード 1 つにつき 1 枚のシザー（自前の候補欄の切り抜きに使う）（2026-10-06、HIGH: 静的 + 実機。縦の向きは実機で訂正） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | HIGH | S | topics/acnl/ui.md |  |
| ACNL-F0628 | HHD と ACNL でアニメのコマ数の数え方が 1 つ違う（2026-10-07、HIGH: 静的＋実機の症状） | ACNL の UiAnim_Step 0x568964: +0x14 bit0（ループしない）なら frame は frameSize(+4) − 1 で頭打ち、bit0 が無ければ frameSize で巻き戻す。UiAnim_IsFinished 0x74F58C も frame >= frameSize − 1。ACNL の BCLAN（ループしない）は最後のキーが frameSize − 1 に 527 件（frameSize ちょうどは 7 件）。 | HIGH | S | topics/acnl/ui.md |  |
| ACNL-F0693 | Layout 描画は上左右目と下の三パスで、上下の二リストを使う（再解析） | LayoutMgr は上の左右目に同じリスト、下に別リストを用いる。上左は記録巡回と再生、上右は再生後に上リスト解除、下は記録巡回と再生後に下リスト解除を行う。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0694 | Layout の優先度は安定な昇順挿入であり、末尾は登録時点に依存する（再解析） | LayoutMgr_AddLayout は Layout+0x0C の符号なしバイトで安定な昇順挿入を行う。最大優先度も後続の同値登録に先行するため、最後の再生や最前面の画素を無条件には保証しない。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0696 | Layout の正射影とペインから画素への換算は Layout 寸法と viewport の比で決まる（再解析） | 基底 Layout の正射影は自身の幅・高さから作る。無追加変換時の画素倍率は viewport 幅/Layout 幅、viewport 高/Layout 高であり、1 単位＝1 画素は寸法一致時の条件付きの結論である。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0697 | Layout 再生の通常シザーは mode 0 であり寸法不一致だけでは切り抜きを有効にしない（再解析） | Layout 再生は自身の寸法からシザー語を組むが、+0x138 が1でない通常分岐はmode 0を送る。寸法不一致だけを理由に切り抜きが有効になるとは言えない。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0698 | Layout 投影 uniform の c4 は毎再生前に設定され初期化後のゼロ固定ではない（再解析） | 投影uniformのc4はDrawer+0x74..+0x80。再生直前のsetterが立体視変位・LayoutMgrの値・0・0を書き、初期化以降ずっとゼロという説は成立しない。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0699 | Layout の記録要求と保存範囲の再利用（再解析） | 記録要求があるときだけ専用リストを消去して再記録する。再生は要求フラグと独立し、保存範囲を利用する。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0700 | Layout と記録 ID の生成・解放・再利用および ID 0（再解析） | Layout の ID は構築前に0で、Build時に生成し破棄時に非ゼロIDを解放する。解放IDは再利用でき、IDだけでは寿命を特定できない。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0701 | 記録 manager の容量・保存 offset と live cursor は異なる（再解析） | manager のbase・容量・保存offsetとglobal cursorは別である。記録/主リストに有限の領域があるが、旧クラッシュ原因と安全量は未確定。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0702 | Fade とロード画像の登録順・状態別の描画元（再解析） | Fade と BlackWait の loader は優先度0xFFを共有し、確認した更新経路ではFadeが先に登録される。loaderの登録有無は状態、画像資源は種類欄で変わる。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0703 | loader ID の十進10と0x10は異なり、旧bucket照合は0x0Aを指す（再解析） | 0xAD9904はID 10（0x0A）のbucketであり、ID 0x10は0xAD991Cを使う。F0261の同ID・同managerという照合は成立しない。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0704 | Fade の記録保持とゼロ長Layoutから画像源を判定する限界（再解析） | 保存長は記録要求やFade状態とは独立するが、Fade終了処理も再計算を要求する。ゼロ長guardが止めるのは記録範囲の再生であり、過去に表示された画像の出どころまでは決めない。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0705 | Picture・Material の別確保と可変長ブロックの実配置（再解析） | Picture は 0x158 バイトで、Material 0x50 バイトと座標配列を別に確保する。Material の可変長領域は容量欄で区切られ、TEV は AlphaCompare・BlendMode より後ろにある。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0706 | TexMap のレジスタ派生値と Picture の UV キャッシュ（再解析） | TexMap の +0x14/+0x18/+0x1C は再生成される値で、Picture の UV 結果は別の二つの有効フラグにより再計算する。CPU キャッシュ更新と GPU 状態送出は別処理である。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0707 | Pane 木の可視走査と Layout 記録・Picture 描画（再解析） | 基底 Layout は可視 root の Pane 木を子リンク順に記録し、Picture は材質状態と幾何・色・UVをバッチへ追加する。頂点色の入力と TEV 構成、バッチ残量の検査とコマンド領域容量は別である。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0708 | Picture の材質共有は無効化・所有と資源寿命の条件を持つ（再解析） | Picture は共有 Material を直接読む一方、UV 有効フラグを書き換える。標準破棄はフラグ次第で Material と別配列を解放するため、共有描画から安全な寿命や再確保は保証できない。 | MEDIUM | A | topics/acnl/ui.md |  |
| ACNL-F0709 | GPU コマンドリストの生成・領域確保・削除と引数型 | GPU コマンドリストの生成は件数と出力ID配列、領域確保は選択中リストのコマンドバイト数とGX容量、削除は件数とID配列を受け取る。SelectList の入力はID一つで、Propertyの結果は出力配列に書かれる。 | MEDIUM | A |  |  |
| ACNL-F0710 | Pane・Picture・Material の描画用構造と vtable 型 | Pane 0xD4、Picture 0x158、Material 0x50 の既知メンバーとvtableを型にした。描画はcursor・DrawInfo・描画contextを4引数で受け渡し、Pictureの座標セットは別確保である。 | MEDIUM | A |  |  |
| ACNL-F0711 | TextBox と ResFont の文字描画用構造および既定 TagProcessor | TextBoxと文字バッチ、ResFontと正規化されたFINF/TGLP/CWDH/CMAP、既定wide TagProcessorを型にした。ResFontは通常確保0x18と独立した埋込み境界が整合し、0x20にはしない。 | MEDIUM | A |  |  |
| ACNL-F0712 | DrawInfo・Layout ノード・LayoutMgr の描画用構造 | DrawInfoはLayout+0x30に内包され、+0x80はLayoutMgr+0x1Cの文字作業体を指す。Layoutノードのroot・記録範囲・画面と上下リスト、管理者holderへ型を付けた。 | MEDIUM | A |  |  |
| ACNL-F0714 | Layoutの仮想関数型と視点・アニメーション・再生状態欄 | Layoutのvptrと7slotの仮想表型を付けた。+0xF8は視点Z、+0xFCはアニメーションflags、+0x114は再生状態マスク、+0x118はコマンドのバイト容量である。 | MEDIUM | A |  |  |
| ACNL-F0715 | Material可変領域の要素型と容量・件数の区別 | Materialの可変領域先頭をTexMap*、各後続部分を要素型とgetterで表した。容量bitsによる配置と件数bitsによる巡回を区別する。 | MEDIUM | A |  |  |
| ACNL-F0716 | PaneとMaterialのアニメーションリンク番兵 | Pane+0x20/+0x24とMaterial+0x08/+0x0Cはアニメーションリンクリストの循環番兵であり、その直前のwordは件数である。 | MEDIUM | A |  |  |
| ACNL-F0717 | ResFontシート記述子とCWDH・CMAP可変長要素 | ResFontのシート記述子は0x14バイトで、変換後GPUアドレス>>3と高さ/幅を持つ。CWDH幅列は+8から3バイト刻み、CMAP方式2は+0xCのu16件数に続き+0xEから4バイトの文字/glyph対を置く。 | MEDIUM | A |  |  |
| ACNL-F0718 | 文字バッチのヘッダー・字形レコードと必要量 | 文字バッチは0x28バイトの固定ヘッダー、44バイトの字形列、処理済みビット列、16バイト境界のコマンド列を持つ。+4の件数と+6の描画制限は、+0の確保上限とは別である。 | MEDIUM | A |  |  |
| ACNL-F0719 | 既定TagProcessorは起動時の相対初期化表から構築される | 既定のchar/wide TagProcessorはstartから起動時の相対オフセット表を巡回して初期化される。TextWriterのコンストラクタはwide既定オブジェクトを参照するだけである。 | MEDIUM | A |  |  |
| ACNL-F0720 | GPUリスト領域確保は失敗を戻り値で通知しない | GpuCmd_AllocateListStorageは成功/失敗を返すAPIではなく、確保結果nullも検査せずGX領域を初期化する。void型を維持し、選択中managerの既知先頭へ型を付けた。 | MEDIUM | A |  |  |
