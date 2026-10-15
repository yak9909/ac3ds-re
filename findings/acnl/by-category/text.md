<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / text

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0017 | F-397: 予測モードにも複合候補の文節リストがある | HIGH（今回の未確定入力について）。実機「わたしはねこがすきです」はmode0/予測6件。 | HIGH | ? |
| ACNL-F0019 | F-395: UI単文節経路と直接連文節APIの区別 | MEDIUM。UI caller 0x10996Cは111FD4(ctx,1,text,0,0,55)を呼ぶが、最下層1145ACの | MEDIUM | ? |
| ACNL-F0024 | F-383: 通常チャットのキーボード生成入口（2026-09-09） | MEDIUM。利用者指定でフレンドチャットを除外、通常チャットを対象にする。 | MEDIUM | ? |
| ACNL-F0025 | F-382: とび森キーボード入口フックと結果返却の契約（2026-09-09） | MEDIUM。利用者依頼の2点を静的IDBと原本ARMのPC実行で確認。実機アクセスなし。 | MEDIUM | ? |
| ACNL-F0163 | F-125: ★★★テキストを画面に描画した。タイル内 Morton スウィズル順も確定 | confidence: **HIGH**（実機。文字が読めた＝スウィズル順が正しいことの証明） | HIGH | ? |
| ACNL-F0165 | F-127: ★★`nw::lyt::TextBox` の構造を実機で確定 — 位置・色・サイズを自由に変えられる | confidence: **HIGH**（実機。1 項目ずつ A/B で目視確認） | HIGH | ? |
| ACNL-F0166 | F-128: ★★★ドロップシャドウの正体 — フォントではなく「もう 1 枚のペインを 1 ドットずらして描く」 | confidence: **HIGH**（実機。2 枚を緑と赤に塗り分けて目視で確定） | HIGH | ? |
| ACNL-F0167 | F-129: `TextBox+224` は `nw::font::ResFont*`。実機には少なくとも4種の初期化済みCFNUがある | confidence: **HIGH**（静的 Ctor / RTTI・vtable / 実機オブジェクト・CFNU ヘッダを照合） | HIGH | ? |
| ACNL-F0168 | F-130: ResFontのCMAP代替処理を確定。全liveフォントは2種の線形フィルタflagがON | confidence: **CMAPと代替処理 HIGH** / **filter flagの意味 HIGH** | HIGH | ? |
| ACNL-F0169 | F-131: TextBoxの折り返しはpane幅、縦方向は非clip。右端欠けの境界はCWDH glyphWidth | confidence: **折り返し・縦方向非clip・描画矩形 HIGH** / **右端の見た目の最終原因 MEDIUM** | HIGH | ? |
| ACNL-F0170 | F-132: 非整数倍率が右端の不均一さを生む — `HIGH` | F-131 の折り返しを除くため `T_time_0` の pane width を 40.0px にした状態で、同じ | HIGH | ? |
| ACNL-F0171 | F-133: ResFont の CFNU/CFNT glyph-sheet atlas 経路を静的再監査 — `MEDIUM`（静的構造）/ `LOW`（再利用手順） | `nwfont_ResFont_ParseAndAttachResource` (`0x4D8048`) は、既に正規化済みの | MEDIUM | ? |
| ACNL-F0174 | F-136: atlas flush wrapper の同一視を撤回 — `MEDIUM`（呼び出し規約）/ `LOW`（command 名） | 再監査で、従来 `0x143718` を `GSPGPU_FlushDataCache`、`0xFFFF8001` を「flush command」と | MEDIUM | ? |
| ACNL-F0178 | F-141: TextWriter wrapper のコピー範囲と reset の実体 — `HIGH`（静的命令列） | `sub_7E7F48` (`0x7E7F48`) は caller が渡した writer から **0x64 bytes 全体**を stack-local | HIGH | ? |
| ACNL-F0180 | F-142: EmitGlyphQuad は会話外 UI でも共有される — `HIGH`（実機） | 会話を開いていない状態で `0x4D4EAC` に software breakpoint を置くと実際に停止した。 | HIGH | ? |
| ACNL-F0181 | F-139: ResFont→CMAP→batch quad の実機経路を確認 — `HIGH`（経路・引数・構造） | 2026-08-28、Remote GDB を停止／再開し、文字更新中の同一呼び出しを breakpoint で採取した。 | HIGH | ? |
| ACNL-F0193 | F-167: ★★★テキストのグリフは「定数から四角形を生成するシェーダ」で描かれる。頂点データが存在しない — `HIGH`（実機の batch を解読） | 適用: `scratchpad/decode_text_batch.py` | HIGH | ? |
| ACNL-F0311 | F-287 (HIGH) — ★明滅と「文字が板になる」の真因は **観測リングが自前 TEV を毎フレーム潰していた**こと | F-283 の「真っ黒」、F-285 の「板＋明滅」、F-286（F-282 へ巻き戻したもの）の | HIGH | ? |
| ACNL-F0318 | F-294 (HIGH・静的のみ) — ★自前フォントで `TextBox` を使えることを確認。`Glyph` 構造を確定 | 利用者の要望は「ゲームのフォントではなく**自前フォント**で描くこと」。**可能**である。 | HIGH | ? |
| ACNL-F0323 | F-299 (HIGH・静的＋実機の実データ照合) — ★F-298 の検証と**訂正 2 件**。バッチの確保元を特定（残件 1） | \| 主張 \| 裏取り \| | HIGH | ? |
| ACNL-F0324 | F-300 (HIGH・静的＋実機) — ゲーム内フォントを流用しても **TextBox は自前で要る**。ただしフォント側の合成は丸ごと不要になる | 「ゲーム内フォントを流用する形でも、同様に TextBox を独自で用意する必要があるか？」 | HIGH | ? |
| ACNL-F0325 | F-301 (HIGH・静的のみ) — ★F-300 の訂正。**TextBox は必須ではない。**文字描画の本体は `TextWriter` | 利用者の指摘を受けて詰め直したところ、F-300 の | HIGH | ? |
| ACNL-F0328 | F-304 (HIGH・実機) — ★`FINF+0x07` は**文字ストリーム読み取り器の選択**。1 以外だと PC=0 で落ちる | 自前フォント資源（F-303）で実機が 2 回落ちた。**原因は 2 つあり、片方は解析結果、片方は私の操作ミス。** | HIGH | ? |
| ACNL-F0329 | F-305 (HIGH・実機) — ★★★自前フォントで実機に描けた。`nw::font` の構造を**全欄**確定 | F-303 / F-304 の 2 度のクラッシュを受けて、**推測を一切残さず**構造を確定してから適用した。 | HIGH | ? |
| ACNL-F0330 | F-306 (HIGH・実機) — ★★★TextWriter 直呼びで描けた。TextBox の DrawSelf を通さない | F-301 で「TextBox は必須ではない」と結論した経路を実機で成立させた。 | HIGH | ? |
| ACNL-F0332 | F-308: 大量の文字を登録したときの天井（TextWriter 直呼び方式の評価） — HIGH | > 問い: 自前チートメニューで**自前フォントの文字を大量に登録**する可能性がある。 | HIGH | ? |
| ACNL-F0337 | F-311 追記 2: 文字が乱れた原因は「中央整列での半画素」（2026-09-06）— HIGH | メニューは出たが文字が乱れた。実機の画素を読むと | HIGH | ? |
| ACNL-F0338 | F-312: Simulator の 2 フォントを `nw::font` へ載せた（日本語 275 字を含む）— HIGH | `PATCHES/make_font_ui.py`。Simulator が使う 2 フォントを**1 枚のシートに同居**させ、 | HIGH | ? |
| ACNL-F0346 | F-319（2026-09-06）: UI フォントを CTRPF プラグインへ組み込む | **confidence: HIGH**（静的検証 8 群 + **実機で描画を確認**） | HIGH | ? |
| ACNL-F0348 | F-322（2026-09-07）: 文字ペインの**横**にも半画素問題があった | **confidence: HIGH**（実機の画と、idalib による経路の逆アセンブル。**直しも実機で確認**） | HIGH | ? |
| ACNL-F0363 | F-337（2026-09-07）: 共有バッチ（§3.2）へ移る前の静的解析 | **confidence: MEDIUM〜HIGH**（すべて idalib で逆アセンブル。実機の裏取りはこれから） | MEDIUM | ? |
| ACNL-F0364 | F-338（2026-09-07）: 記録量の式を実機で確定 | **confidence: HIGH**（実機 4 点 + 見せる本数 4 通り。コードは新規注入なし） | HIGH | ? |
| ACNL-F0365 | F-339（2026-09-07）: ★実機ゲート通過「1 本のバッチに複数の文字列」 | **confidence: HIGH**（実機で描画・画で確認） | HIGH | ? |
| ACNL-F0366 | F-340 — 色替え・書体替えの費用を分解し、記録量の式を完成させた（2026-09-07・実機） | **confidence: HIGH**（実機 15 点で誤差 0。うち 2 点は**式を作ったあとに予言してから測った**） | HIGH | ? |
| ACNL-F0367 | F-341（2026-09-07）: 費用の式を「当てはめ」から「逆アセンブルの写し」へ | **confidence: HIGH**（実機 19 点で誤差 0。うち **3 点は式を書いたあとに予言してから測った**） | HIGH | ? |
| ACNL-F0384 | F-358: 3DS内蔵ソフトウェアキーボードのAPIとCTRPFの条件（2026-09-08） | 詳細・出典・次の確認順は **`DOCS/system_keyboard.md`**。 | MEDIUM | ? |
| ACNL-F0389 | F-362: 内蔵日本語辞書6本の取得・主要辞書75,770件の読み/候補を抽出（2026-09-08） | **confidence: MEDIUM**。複数静的証拠とPC内での元ARM命令実行で検証。 | MEDIUM | ? |
| ACNL-F0390 | F-363: 内蔵キーボードの候補順位・文節変換・学習を原本ARMで再現（2026-09-08） | **confidence: MEDIUM。** SWKBD専用idalib IDBの静的解析＋PC上のUnicorn実行。 | MEDIUM | ? |
| ACNL-F0409 | F-384: 通常チャットから内蔵ソフトウェアキーボードを呼ぶケーブを適用（2026-09-09） | 通常チャットの `0x001938AC` をフックし、元の `UiScreen_OpenById(0x23E)` を必ず呼んで | HIGH | ? |
| ACNL-F0410 | F-385: 通常チャットから内蔵SWKBDの起動・キャンセル復帰に成功（2026-09-09） | F-384を適用した実機で通常チャットを開くと、内蔵ソフトウェアキーボードが起動した。 |  | ? |
| ACNL-F0411 | F-386: 内蔵SWKBDの漢字確定文字を共有メモリから回収（2026-09-09） | F-384のパッチを残したまま通常チャットを再度開き、利用者が `漢字テスト` を入力して |  | ? |
| ACNL-F0412 | F-387: SWKBD実機の表示候補キャッシュ位置と読取器（2026-09-09） | **confidence: MEDIUM（SWKBD原本の静的解析2経路＋オフラインfixture。実機値は未取得）。** | MEDIUM | ? |
| ACNL-F0414 | F-389: 実機SWKBDから「かんじ」の全17候補と順位を回収（2026-09-09） | **confidence: HIGH（実機の表示cache・全候補record、原本ARMのローカル実行、F-363の独立PC実行を照合）。** | HIGH | ? |
| ACNL-F0423 | 普通チャットのキャンセル・実退場とタブ復帰（2026-10-12） | IDA（idalib）/GPT-6、MEDIUM。更新SHA/load/ARM/T/元bytesを再照合。普通keyboard Cancelは決定index0→byte0x949D3B=0（self+4424が真）、self+4580=1、TextInput_PublishResult(1,1)。親0x193764→Out enter0x193988→child vt17/0x57B238→button-out/window-out。0x57CF04はアニメ完了後破棄要求、R | MEDIUM | ? |
| ACNL-F0428 | chat listの決定と時刻窓からのfield復帰（2026-10-12） | 担当 GPT-6 / IDA（idalib）、更新原入力SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ARM32LE/imagebase0。native assembly、source、既存F036/F062を照合。確度MEDIUM、新修正版実機未確認。 |  | ? |
| ACNL-F0487 | ソフトウェアキーボードのキーの「次の入力までの待ち」の正体（2026-09-26、MEDIUM: 静的のみ（逆アセンブル＋成果物の照合）。実機未確認） | 利用者の指示「ゲーム内のキー入力で、一度入力してから次に入力できるまでの短い待ちを無くす」の下調べ（gohan で対応、下記）。 | MEDIUM | S |
| ACNL-F0488 | キーボードのキーの見た目・テクスチャの取り方・開閉アニメ・切り替え音・カーソル設定の引数（2026-09-26、MEDIUM: 静的＋romfs。実機未確認） | チャットの自前キー（全選択・左右）をゲームのキーで描き、開閉アニメに追従させるための下調べ（gohan 058e1a5）。 | MEDIUM | S |
| ACNL-F0489 | 文字の挿入・削除・選択・確定、キーの経路、チャットの送信、入力欄の「未確定」と「選択」の飾り（2026-09-25、MEDIUM: 静的のみ。実機未確認） | F043 の続き。かな入力のコンポジションと漢字変換（利用者の依頼）の土台。 | MEDIUM | S |
| ACNL-F0490 | 文字入力（チャット・手紙・掲示板共通）の sys::TextManager の欄とカーソル・未確定の扱い（2026-09-25、MEDIUM: 静的のみ。実機未確認） | 漢字変換の候補欄とかな入力のコンポジション（利用者の依頼）の下調べ。取っ掛かりは AnimalBytes `Sources/ACNL/Chat.cpp`（入力欄の UTF-16 = [0x958108]、文字数 = [0x958114]+8）。 | MEDIUM | S |
| ACNL-F0495 | 一覧の行の文字の TagProcessor は script::RenderMain。タグ 0x0E/0/2 = 大きさ（縦横）、タブは 4 × 文字幅（2026-09-25、MEDIUM: 静的のみ。実機未確認） | 一覧の組み立て段 1（`sub_1C513C`）: 行ごとにメッセージ箱（196 B、`sub_5E24B0(箱, *(list+2504))` = 文字数の器）を作り、`vc_ACMESSAGEBOX_FUNC1 0x5E2020(箱, T_itm_%02d, 0)` で結ぶ。FUNC1 は TextBox vt[28] で器を取り、**TextBox+244（TagProcessor）に箱自身**を入れ、箱+12/+16 = 文字の大きさ ÷ 書体の幅／高さ（元の拡大率） | MEDIUM | S |
| ACNL-F0602 | プレイヤー本人の目の形をその場で変える手順・レイアウトの色の 1 要素の読み書き・書体の私用領域の記号（2026-10-06、MEDIUM: 静的のみ。gohan は実機未確認） | 解析モデル opus-5.5。IDB: `nwlyt_Pane_GetColorElement 0x73B508` / `nwlyt_Picture_GetVtxColorElement 0x73CB40` / `nwlyt_Material_SetColorElement 0x4BCC7C` / | MEDIUM | S |
| ACNL-F0612 | ゲームのフォント（Garden_msg_size16）で描けない文字 = 代わりの字形 0xE03A（2026-10-06、MEDIUM: 実機の写し + 元の ARM との照合。候補の除外は実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0681 | remote chat Size/Color tags survive transport and render | **確度: HIGH（JPN v1.5 raw bytes / fresh Ghidra ProgramDB）。実機remote decoration testは未実施。** | HIGH | B |
| ACNL-F0682 | local/self and inline tag scope | **確度: HIGH (static JPN v1.5 path analysis; hardware tagged-chat test still pending).** | HIGH | B |
| ACNL-F0683 | 0x958108 is pointer storage | `0x958108` is a global dword pointer slot, not inline UTF-16 storage. |  | B |
| ACNL-F0684 | direct 0x958108-pointee test negative; parse is still post-submit | **Hardware observation:** a valid Color-tag sequence written to the current pointee read from `0x958108` did not visibly decorate chat. |  | B |
| ACNL-F0685 | normal chat strips embedded tags | **Hardware-confirmed.** |  | B |
| ACNL-F0686 | mode1 sender bypass preserves tags on hardware | **Hardware-confirmed.** |  | B |
| ACNL-F0687 | sender local Color render hardware success | **Hardware-confirmed.** |  | B |
| ACNL-F0688 | player/town name tag sanitizer | group5/type0 current player name -> Insert method 0x5ECAB8. |  | B |
| ACNL-F0689 | dedicated ruby font | Conversation ruby/furigana uses a dedicated logical font resource `Garden_ruby`, separate from `Garden_msg_size16`. |  | B |
