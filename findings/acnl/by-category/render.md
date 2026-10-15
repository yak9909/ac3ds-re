<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / render

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0028 | F-155a: submit-descriptor recorder は描画前のレジスタ連鎖で例外 — `HIGH`（例外位置＋機械的監査） | `scratchpad/trace_main_text_submit_descriptor.py` の初版は | HIGH | ? |
| ACNL-F0132 | F-94: 描画スタックの同定と GSP IPC 層 | confidence: **MEDIUM**（RTTI 実測 + IPC パターンを逆コンパイルで確認。**静的解析のみ**） | MEDIUM | ? |
| ACNL-F0136 | F-98: TODO-37 の否定と、描画解析の全体精査 | confidence: **MEDIUM**（各項目を逆コンパイル／RTTI で個別に検証。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |
| ACNL-F0137 | F-99: 描画解析の再精査 — 数値変換 2 件とレジスタ名 3 件の誤りを訂正 | confidence: **MEDIUM**（機械的な検算は確実だが、`registers.h` は `REFERENCES/` 配下＝一次情報ではない。F-101 で訂正） | MEDIUM | ? |
| ACNL-F0144 | F-106: ★`g3d::FuncNode` — 描画中に任意の関数を呼べるシーンノード | confidence: **MEDIUM**（静的解析のみ。CLAUDE.md の定義に従い実機未観測なので HIGH にしない） | MEDIUM | ? |
| ACNL-F0151 | F-113: ★★TODO-68 完了 — `BsShadowViewMgr` が実例。フレーム描画の全体像と `1024`/`1040` の正体 | confidence: **HIGH**（静的解析と実機観測の双方。実機の `LR` とスタックで連鎖を確認） | HIGH | ? |
| ACNL-F0152 | F-114: ★★TODO-71 完了 — 描画コールバックが積むものの全体像（自前描画の手本） | confidence: **HIGH**（静的解析と実機のメモリ直読みの双方。レジスタ名は `registers.h` で照合） | HIGH | ? |
| ACNL-F0159 | F-121: ★★TODO-84 第1段 — 積まれたコマンドを自分で解釈・書き換え、描画結果を狙って変えられた | confidence: **HIGH**（実機。数値と目視の双方で確認） | HIGH | ? |
| ACNL-F0160 | F-122: ★★★TODO-84 達成 — 完全自己完結の自前描画。あわせて TODO-83 も解決 | confidence: **HIGH**（実機。ユーザーの目視で単一インスタンスの同定まで一致） | HIGH | ? |
| ACNL-F0172 | F-134: EmitGlyphQuad の texture handle 選択と batch/immediate 分岐を静的再監査 — `MEDIUM` | `nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) の全分岐を静的に再読した。 | MEDIUM | ? |
| ACNL-F0175 | F-137: `SetGlyphTextureParams` の引数は decompiler 表示より多く使われる — `MEDIUM` | `0x4D8484` の逆コンパイル表示では `0x7ABDBC` 呼び出しの引数が省略され、texture | MEDIUM | ? |
| ACNL-F0177 | F-140: TextBox→TextWriter の描画入口と後処理 — `MEDIUM`（静的） | `nwlyt_TextBox_DrawText` (`0x4BB1E8`) の命令列から、標準テキスト描画を再利用する最小の | MEDIUM | ? |
| ACNL-F0179 | F-143: TextBox vtable の実描画入口は `0x73CF48` — `HIGH`（静的＋実機） | `nw_lyt_TextBox` vtable (`0x8FC07C`) の slot `+0x64` は `nwlyt_TextBox_DrawText` | HIGH | ? |
| ACNL-F0183 | F-157: ★★★テキスト描画コマンドの投入を自前で駆動できた。色バイト順も確定 — `HIGH`（静的導出＋実機で視認） | 実機の会話ウィンドウで、住民名 `T_nam_00`（「ぺりお」）が | HIGH | ? |
| ACNL-F0186 | F-160: テキスト描画の座標系を確定。F-158 の「1.25 = 400/320」は誤り — `HIGH`（実機で基準行列を採取＋3 枚の配置と照合） | `0x4B7DCC` で `[R9-64, R9)` の 16 ワードを控えて得た: | HIGH | ? |
| ACNL-F0197 | F-171: ★TextBox の描画は歩行中ゼロ。相乗り方式には大きな穴がある — `HIGH`（実機で計測） | 適用: `PATCHES/measure_textbox_draws.py` | HIGH | ? |
| ACNL-F0202 | F-176: Picture はコマンドを直接吐かず、描画コンテキストに四角形を溜めて一括で流す — `HIGH`（静的解析） | ```c | HIGH | ? |
| ACNL-F0204 | F-178: 描画コンテキストの四角形配列を解読。`+1648` は F-167 の `c[0x40]` そのもの — `HIGH`（実機で採取） | 適用: `PATCHES/cave_probe_drawctx.py` | HIGH | ? |
| ACNL-F0218 | F-193: ★★★★★自前スプライトを独立したバッチで描画。テクスチャも独立 — `HIGH`（実機） | `PATCHES/cave_own_batch.py`。**「左上に白黒の市松模様の板が出て、背景は元のまま」**（ユーザー確認）。 | HIGH | ? |
| ACNL-F0223 | F-198: ★★★★7 枚超の描画と、ドット絵をきれいに出すための 4 条件 — `HIGH`（実機） | `PATCHES/cave_draw_sprites.py`。**「ACNL GUI OK」11 文字（2 チャンク）を描画し、 | HIGH | ? |
| ACNL-F0240 | F-215: ★★★★★借りたマテリアルは 9 語まとめて中立化する。ただし描画後に積み直してはいけない — `HIGH`（実機） | F-214 の対策（`+0x10`/`+0x14`/`+0x18` の 3 語を中立化）では**しずえ会話の切り替わりで | HIGH | ? |
| ACNL-F0252 | F-227: ★★★観測用の領域を、動いている描画の領域と重ねてクラッシュさせた — `HIGH`（実機） | フェードの調査のために `probe_replay_last.py` を仕掛けたらクラッシュした。 | HIGH | ? |
| ACNL-F0279 | F-256: ★★★★★ゲームがそのパスで 1 枚も描いていないと、描画コマンドを積んだ瞬間に GPU が止まる — `HIGH`（実機で二分により確定） | 自前ノード方式にしてから、**「上画面のタイトルロゴが消えた瞬間」に必ず GPU が停止**した。 | HIGH | ? |
| ACNL-F0282 | F-259: ★★★★★UI 描画経路の完全な静的仕様。render.txt は本作と 1:1 で一致する — `HIGH`（静的のみ） | `REFERENCES/TEXTS/render.txt` の `ssys::ma::lyt::Layout::RenderFrame` を、 | HIGH | ? |
| ACNL-F0294 | F-271: ★★★★★`TextBox_UpdateDrawState`(`0x4B7DEC`) が「テクスチャ付き描画へ切り替える」全手順。実測列の全項目がこれで説明できた — `HIGH`（静的 + F-124 の実測列） | F-270 で reg `0x080` の穴を見つけたので、**同じ穴が他にもないか**を | HIGH | ? |
| ACNL-F0306 | F-281: ★★★★★実機で描画に成功した。ノイズの原因は**非整数倍の拡大** — `HIGH`（実機） | > あなたの想定通りに出ています。フリーズもせず、ロードやメニュー操作で消えず常に表示されています。 | HIGH | ? |
| ACNL-F0336 | F-311 追記: 実機で描画されなかった原因（2026-09-06）— HIGH | プラグインを ON にしても**何も描画されず、Select でメニューも開かない**。 | HIGH | ? |
| ACNL-F0454 | 場面転換。自前instanceは無傷で残り、ケーブは自分から描画を止める（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T018。**利用者に建物へ入ってもらって測定した。** | HIGH | ? |
| ACNL-F0455 | 描画中に instance を解放しても何も起きない。ただし理由は2つある（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017a。**意図的に安全手順を破った試験。** | HIGH | ? |
| ACNL-F0456 | 描画中に資源を潰しても落ちない。モデルが黙って消えるだけ（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017b。**意図的に安全手順を破った試験の第2段。** | HIGH | ? |
| ACNL-F0521 | モデル単位の色ハイライトは「TEV の空き最終段で定数色と混ぜる」でできる（2026-09-23、**HIGH（静的＋実機で表示確認）**。材質 1 つで確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「建物を含めた任意の 3D モデルで、そのモデルだけ全体の RGBA を操作できるか。 | HIGH | S |
| ACNL-F0546 | 任意bcresの読み込み→ワールド描画が実機で成立（2026-09-20、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**ゲームが読んでいないファイルを自分で読み、画面に出した。** | HIGH | ? |
| ACNL-F0547 | モデルのクラスは資源が決める。ゲーム内のCMDLは2種類しかない（2026-09-20、MEDIUM、静的） | 解析ソフト: IDA / 解析モデル: opus-5。対象 `artifacts/update/exefs/code.bin`（VA=file+0x100000）。 | MEDIUM | ? |
| ACNL-F0558 | 描画順は静的に確定できる。描画状態は bcres の PICA コマンド列にある（2026-09-18、MEDIUM） | 利用者の見立て「描画順は静的解析で確認できるはず」は正しかった。(1) **描画順＝マテリアルのレイヤー**。Scene_DrawLayers 0x4EB840 は外側で i=0..3 を回し、メッシュごとに material→(+8 の元 ResMaterial)+32 の下位バイトが i と一致するときだけ sub_48D26C 0x48D26C で GPU コマンドを積む（FuncNode は i==0 で node[82]、i==1 で node[83] のコールバッ | MEDIUM | ? |
| ACNL-F0617 | ACNL の品番 → モデル名の表と、HHD との品物の突き合わせ（2026-10-06、MEDIUM〜HIGH: 静的 2 本 + ROM の実データ） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022 の下調べ。 | MEDIUM | S |
| ACNL-F0645 | balloon ARの旧code caveが既存描画caveと衝突していた | **確度: HIGH（添付Ghidra XMLの既存allocation map＋crash_dump_00000007＋ユーザー実機挙動）。** | HIGH | B |
