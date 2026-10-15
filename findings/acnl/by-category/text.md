<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / text

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0025 | F-382: とび森キーボード入口フックと結果返却の契約（2026-09-09） | MEDIUM。利用者依頼の2点を静的IDBと原本ARMのPC実行で確認。実機アクセスなし。 | MEDIUM | ? |
| ACNL-F0166 | F-128: ★★★ドロップシャドウの正体 — フォントではなく「もう 1 枚のペインを 1 ドットずらして描く」 | confidence: **HIGH**（実機。2 枚を緑と赤に塗り分けて目視で確定） | HIGH | ? |
| ACNL-F0167 | F-129: `TextBox+224` は `nw::font::ResFont*`。実機には少なくとも4種の初期化済みCFNUがある | confidence: **HIGH**（静的 Ctor / RTTI・vtable / 実機オブジェクト・CFNU ヘッダを照合） | HIGH | ? |
| ACNL-F0171 | F-133: ResFont の CFNU/CFNT glyph-sheet atlas 経路を静的再監査 — `MEDIUM`（静的構造）/ `LOW`（再利用手順） | `nwfont_ResFont_ParseAndAttachResource` (`0x4D8048`) は、既に正規化済みの | MEDIUM | ? |
| ACNL-F0311 | F-287 (HIGH) — ★明滅と「文字が板になる」の真因は **観測リングが自前 TEV を毎フレーム潰していた**こと | F-283 の「真っ黒」、F-285 の「板＋明滅」、F-286（F-282 へ巻き戻したもの）の | HIGH | ? |
| ACNL-F0324 | F-300 (HIGH・静的＋実機) — ゲーム内フォントを流用しても **TextBox は自前で要る**。ただしフォント側の合成は丸ごと不要になる | 「ゲーム内フォントを流用する形でも、同様に TextBox を独自で用意する必要があるか？」 | HIGH | ? |
| ACNL-F0328 | F-304 (HIGH・実機) — ★`FINF+0x07` は**文字ストリーム読み取り器の選択**。1 以外だと PC=0 で落ちる | 自前フォント資源（F-303）で実機が 2 回落ちた。**原因は 2 つあり、片方は解析結果、片方は私の操作ミス。** | HIGH | ? |
| ACNL-F0337 | F-311 追記 2: 文字が乱れた原因は「中央整列での半画素」（2026-09-06）— HIGH | メニューは出たが文字が乱れた。実機の画素を読むと | HIGH | ? |
| ACNL-F0338 | F-312: Simulator の 2 フォントを `nw::font` へ載せた（日本語 275 字を含む）— HIGH | `PATCHES/make_font_ui.py`。Simulator が使う 2 フォントを**1 枚のシートに同居**させ、 | HIGH | ? |
| ACNL-F0346 | F-319（2026-09-06）: UI フォントを CTRPF プラグインへ組み込む | **confidence: HIGH**（静的検証 8 群 + **実機で描画を確認**） | HIGH | ? |
| ACNL-F0348 | F-322（2026-09-07）: 文字ペインの**横**にも半画素問題があった | **confidence: HIGH**（実機の画と、idalib による経路の逆アセンブル。**直しも実機で確認**） | HIGH | ? |
| ACNL-F0365 | F-339（2026-09-07）: ★実機ゲート通過「1 本のバッチに複数の文字列」 | **confidence: HIGH**（実機で描画・画で確認） | HIGH | ? |
| ACNL-F0384 | F-358: 3DS内蔵ソフトウェアキーボードのAPIとCTRPFの条件（2026-09-08） | 詳細・出典・次の確認順は **`DOCS/system_keyboard.md`**。 | MEDIUM | ? |
| ACNL-F0409 | F-384: 通常チャットから内蔵ソフトウェアキーボードを呼ぶケーブを適用（2026-09-09） | 通常チャットの `0x001938AC` をフックし、元の `UiScreen_OpenById(0x23E)` を必ず呼んで | HIGH | ? |
| ACNL-F0411 | F-386: 内蔵SWKBDの漢字確定文字を共有メモリから回収（2026-09-09） | F-384のパッチを残したまま通常チャットを再度開き、利用者が `漢字テスト` を入力して |  | ? |
| ACNL-F0412 | F-387: SWKBD実機の表示候補キャッシュ位置と読取器（2026-09-09） | **confidence: MEDIUM（SWKBD原本の静的解析2経路＋オフラインfixture。実機値は未取得）。** | MEDIUM | ? |
| ACNL-F0414 | F-389: 実機SWKBDから「かんじ」の全17候補と順位を回収（2026-09-09） | **confidence: HIGH（実機の表示cache・全候補record、原本ARMのローカル実行、F-363の独立PC実行を照合）。** | HIGH | ? |
| ACNL-F0423 | 普通チャットのキャンセル・実退場とタブ復帰（2026-10-12） | IDA（idalib）/GPT-6、MEDIUM。更新SHA/load/ARM/T/元bytesを再照合。普通keyboard Cancelは決定index0→byte0x949D3B=0（self+4424が真）、self+4580=1、TextInput_PublishResult(1,1)。親0x193764→Out enter0x193988→child vt17/0x57B238→button-out/window-out。0x57CF04はアニメ完了後破棄要求、R | MEDIUM | ? |
| ACNL-F0428 | chat listの決定と時刻窓からのfield復帰（2026-10-12） | 担当 GPT-6 / IDA（idalib）、更新原入力SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ARM32LE/imagebase0。native assembly、source、既存F036/F062を照合。確度MEDIUM、新修正版実機未確認。 |  | ? |
| ACNL-F0495 | 一覧の行の文字の TagProcessor は script::RenderMain。タグ 0x0E/0/2 = 大きさ（縦横）、タブは 4 × 文字幅（2026-09-25、MEDIUM: 静的のみ。実機未確認） | 一覧の組み立て段 1（`sub_1C513C`）: 行ごとにメッセージ箱（196 B、`sub_5E24B0(箱, *(list+2504))` = 文字数の器）を作り、`vc_ACMESSAGEBOX_FUNC1 0x5E2020(箱, T_itm_%02d, 0)` で結ぶ。FUNC1 は TextBox vt[28] で器を取り、**TextBox+244（TagProcessor）に箱自身**を入れ、箱+12/+16 = 文字の大きさ ÷ 書体の幅／高さ（元の拡大率） | MEDIUM | S |
| ACNL-F0612 | ゲームのフォント（Garden_msg_size16）で描けない文字 = 代わりの字形 0xE03A（2026-10-06、MEDIUM: 実機の写し + 元の ARM との照合。候補の除外は実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0681 | remote chat Size/Color tags survive transport and render | **確度: HIGH（JPN v1.5 raw bytes / fresh Ghidra ProgramDB）。実機remote decoration testは未実施。** | HIGH | B |
| ACNL-F0685 | normal chat strips embedded tags | **Hardware-confirmed.** |  | B |
| ACNL-F0689 | dedicated ruby font | Conversation ruby/furigana uses a dedicated logical font resource `Garden_ruby`, separate from `Garden_msg_size16`. |  | B |
