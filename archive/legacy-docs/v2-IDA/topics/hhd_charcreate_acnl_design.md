# HHD のキャラクリ画面を ACNL の下画面で再現する設計 / IDA-opus-5.5-D005

2026-10-05、IDA（ACNL 主 IDB・HHD IDB）/ 解析モデル opus-5.5。**設計のみ。gohan への実装・実機適用はまだ。**
HHD 側の解析は [docs/hhd/chara_create_screen.md](../hhd/chara_create_screen.md)（HHD-F001〜F007）。

## 1. 目的と範囲

- 利用者（2026-10-05）: 髪型変更チートを有効にすると、カタログショップを開いたときのようにフェードのトランジションが入り、上画面を背景で隠し、
  下画面に HHD のキャラクリ画面を作る。**今回は上画面に触らず、下画面の再現だけ**を設計する。
- 段階:
  - **1（この設計）**: 下画面に HHD と同じ見た目・同じ触り心地の画面を出し、閉じられる。プレイヤーのデータはまだ変えない。
  - 2: 上画面の背景とフェード（カタログと同じトランジションの解析が要る）。
  - 3: 選んだ髪型・色などをプレイヤーへ反映（ACNL 側の見た目データと HHD の番号の対応づけが要る。§8）。

## 2. 方式の比較

| 案 | 中身 | 長所 | 短所 |
|---|---|---|---|
| **A（推奨）** ゲームのレイアウト機構に自前のアーカイブを渡す | HHD の絵を BCLIM にし、画面を BCLYT で組み、DARC に詰めてメモリに置き、ACNL 自身の `ArcResourceAccessor::Attach` → `Layout` 組み立て → `LayoutMgr` 登録で描かせる | 描画・テクスチャの VRAM 転送・文字・アルファはゲームそのもの。gohan の GameLabel / GameList と同じ経路（実機で動いている） | BCLIM・BCLYT・DARC を作る道具が要る。メモリ上のアーカイブを Attach した実績はまだ無い |
| B gohan の自前描画（GuiV2 の Picture / TextBox を自前で組む） | 今のチートメニューと同じ方式でペインをデータで組む | 実機の実績がある | テクスチャの GPU 可視領域の確保・マテリアルの白黒補間・ウィンドウ枠などを自前で全部持つ。100 枚近い部品には重い |
| C ACNL 既存のレイアウトを借りて差し替え | 共通ボタン・一覧などを借りて絵だけ替える | 新しい形式の作成が要らない | HHD の部品（肌の板＋目＋黒目の重ね、色見本）に合う既存レイアウトが無い |

**A を採る。** 根拠（ACNL 主 IDB、静的）:
- レイアウトの組み立て `sub_5685A4` は、置き場の資源アクセサ（holder+4）の vt[2]（'blyt', 名前）でデータを引くだけ（F039 の注記）。
- gohan が使う置き場 `ArcResAccReader_Ctor 0x120D54`（RTTI: `ssys::ma::lyt::ArcResAccReader` ＋ `ArcResourceAccessorVRAM`）は、
  読み込み後に **`sub_4B5900`（= `nw::lyt::ArcResourceAccessor::Attach(アクセサ, アーカイブ先頭, ルート)`）** を呼ぶ（`ArcResAccReader_LoadArcStep 0x567244`）。
  Attach は DARC を `sub_4B3EAC` で解き、ルート名を +60 に写すだけ → **メモリ上の DARC を直接 Attach できる見込み**（未実機）。
- テクスチャは描く時に `ssys_ArcResourceAccessorVRAM_LoadTexture 0x567530` → `ssys_LoadBclimToVram 0x5676C8` で VRAM に載る（非同期 DMA）。
- 書体は ACNL にも `Font/Garden_msg_size16.bcfnt` がある（HHD は同名の .bffnt）。

## 3. 資源の作り方（道具は既存を優先。利用者指示 2026-10-05）

| 物 | 元 | 作り方 | 道具 |
|---|---|---|---|
| 絵（PNG） | HHD v1.1 の BFLIM | 3DSkit で PNG（済み。`tools/hhd/extract_layouts.py`） | 3DSkit |
| BCLIM | BFLIM の画素 | 末尾 0x28 バイトだけ CLIM 形式で書き直す（形式番号は同じ並び） | `tools/hhd/bflim_to_bclim.py`（3.1） |
| BCLYT | acnl-ui-designer の場面（§5） | 設計 → 組み立てプログラム → BCLYT | **Clypo のライブラリ**（pleonex、MIT）を使う C# の組み立てプログラム（3.1） |
| アニメ | HHD の BFLAN の値（`Face_anims.txt`） | 段階 1 は **gohan 側のコードで再生**（y −2・拡大・色の段替えだけなので小さい）。BCLAN は段階 2 以降に検討 | — |
| DARC | 上の全部 | 1 本に詰める | `tools/hhd/darc_pack.py`（3.1） |

置き場所: 作った DARC は SD（gohan の設定フォルダ）に置き、チートを開くときに読む。**任天堂の素材を含むので Git に入れない**（acnl-ui-designer の assets と同じ扱い）。

### 3.1 道具の確認結果（T010、2026-10-05、`work/evidence/hhd/tools_t010.md`）

- **BCLYT**: Clypo の CLI の import は既存ペインの位置・大きさ・文字の書き換え専用で、ペインや材質を足せない。
  ライブラリの読み書きは ACNL の bclyt 8/10 本でバイト一致（残り 2 本はペインのユーザーデータの不具合）→ **Clypo のライブラリを使う小さな C# の組み立てプログラム**で作る。ユーザーデータは使わない。
- **BCLIM**: 既存の書き出し道具は無かった。BFLIM の画素はそのまま末尾 0x28 バイトだけ書き直す `tools/hhd/bflim_to_bclim.py` で 103/103 枚が全画素一致。
  **アイコン 80 枚は保存の向きが 90° 回転（swizzle 4）・回転＋上下反転（8）** なので、BCLIM は保存の向きのまま（幅と高さが入れ替わる）にして、
  **目・黒目・髪のペインの UV で向きを直す**（目 = 8、黒目と髪 = 4。差し替える全アイコンで同じ値なので UV は固定でよい）。
- **DARC**: 既存の 2 つは使えず（3DSkit は表の大きさの不具合、DARCTool は Python 2 専用）、`tools/hhd/darc_pack.py` を作った。ACNL の Layout の arc 102/110 本でバイト一致。

### 3.2 組み立てと designer での照合（T015 / T011、2026-10-05）

- **組み立て**: `tools/hhd/make_acnl_layouts.py`（HHD の JSON → LayoutBuilder の JSON）→ `tools/hhd/build_hhd_arc.py`（BCLYT・BCLIM・DARC）。
  出力 `work/cache/hhd/out/hhd_charcreate.arc`（333,096 B、レイアウト 4・テクスチャ 96）。LayoutBuilder（`tools/hhd/LayoutBuilder`）の往復は ACNL の bclyt 124 本中 97 本バイト一致（残りは Clypo のユーザーデータ・名前の不具合）。
- **designer 照合**: `tools/hhd/make_designer_scenes.py` がスクショ 6 枚と同じ状態（肌・目・髪の色、顔/髪、髪のページ）の場面を作り、描いて画素比較する。
  状態を入れない部分（選択枠・押せない/決定ボタンの見た目・背景の流れる位相・ボタンの絵記号）を除くと一致。顔の一覧（選択中のマスを除く範囲）で 24 超の画素 1.0〜1.1%。
- **HHD と ACNL の違いで、変換時に直したもの**（いずれもスクショで確認。根拠の強さは各項）:
  1. **透明度だけのテクスチャ（A4 / A8）**: ACNL は RGB = 0 で読み色は黒色の RGB（designer extract/clim.py、実機で確認済み）。HHD は白色の RGB が出る。
     → 変換時に **黒色の RGB = 白色の RGB**（α は黒色のまま）。**実行時に色を変えるとき（T013）も同じ規則で黒色も書く**こと（黒目・色見本など）。
  2. **テクスチャ SRT**: HHD の材質の SRT（色見本・ボタン = 平行移動 0.5・拡大 2 と mirror、背景の水玉 = 回転 45°・拡大 2）をそのまま写す（最初の版は捨てていた）。
  3. **文字の材質**: HHD の材質（黒色 α 0）を使う。ACNL の文字の TEV は α = tex.a×白α + (1−tex.a)×黒α なので、黒色 α 255 だと字の箱が塗られる。
  4. **ウィンドウ**: HHD の wnd1 flags 0x10（NW の Window の「中身を描かない」と読む。目・髪の枠は 0x13）。ACNL の `nwlyt_Window_DrawSelf 0x73BCBC` は中身を必ず描くので、中身の頂点色 α = 0 で消す。
     枠の大きさは HHD は欄（16）、ACNL は枠テクスチャの大きさ（`0x73BB44`）→ 一致を生成時に検査。1 枠のウィンドウは ACNL も描ける（IDA-opus-5.5-F072）。
  5. **背景の水玉の UV**: スクショの水玉は縦横 32 px 周期 = UV が「ペインの画素 / 64」× 拡大 2 のとき。HHD のレイアウトの UV は 0〜1 で、理由は未解明（HHD のコードに `P_Pattern` の文字列は無い。HHD-T006）。
     → **実測合わせ**で P_Pattern_00 の UV を画素単位（320/64, 240/64）にした（`UV_PIXEL_SCALE`）。周期は一致、位相は loop アニメの位置で変わる。
- **髪のページ**: 枠 pg0/pg1/pg2 は静的にページ 0/1/2 を持つ。選んだページの枠を中央へ回す。先頭ページでは左の枠が空く（利用者: 髪の画面はスクロールでき、スクショは端まで寄せた状態）。ページ 3（24〜31）は絵の差し替えが要る。
- 未対応: 材質のテクスチャ 2 枚目（縞。選択枠・決定ボタン）、ボタンの絵記号（はさみ・顔。HHD は文字列内の記号と見込み、未確認）、アニメ。

## 4. 画面の組み方（BCLYT）

NW4C の BCLYT には HHD の部品ペイン（prt1）が無い前提で、**部品を展開した平らな木**にする（要確認: ACNL の bclyt に部品があるか）。

| レイアウト | 中身（HHD の対応） | ペイン数の目安 |
|---|---|---|
| `hhd_bg` | 地の黄色と流れる柄（fce_BG_00） | 3 |
| `hhd_face` | 目の色 6・肌の色 8 の見本（fce_Color_00 × 14）、髪の色 16 の見本（× 16、髪モードで表示）、アイコン 3、下ボタン 2（fce_Btn_00 / cbn_Btn_00） | 約 150 |
| `hhd_eye` | 目の形ボタン 12（fce_Eye_00 × 12: 肌の板・目・黒目・枠） | 約 60 |
| `hhd_hair` | 髪のボタン 8 × 3 ページ（fce_Hair_00 × 24: 枠・頭・顔・髪）＋ページの当たり | 約 120 |

- 座標は HHD と同じく中心原点（下画面 320x240）。値は `work/evidence/hhd/layout/Face_trees.txt` の部品の位置 ＋ 部品の中の位置。
- 色: 色見本・ボタンの色は **マテリアルの白色・黒色を gohan が直接書く**（`palettes.json` から生成した表。HHD のアニメのフレーム = 色番号と同じ結果）。
- 目・髪の絵の差し替え: 置き場から名前でテクスチャを引き（`sh_fce_{B,G}Eye_NN` など）、ペインの texMap を差し替える。
  手段は ACNL の `nwlyt_ArcResourceAccessor_GetTexture 0x4B5844` / gohan の RegisterTex（0x568CFC）を調べてから決める。
- メモリ: 下画面のテクスチャ合計 約 242 KB（共通 34 KB・目 76 KB・髪 132 KB、`tools/hhd/extract_layouts.py` の出力から計算）。
  性別で半分にできる（目 38 KB・髪 66 KB）。カタログ表示中の実測では nw::lyt ヒープの空き 1,456,124 B（F036）。VRAM の空きは未測定。

## 5. acnl-ui-designer の役割

1. HHD の PNG を取り込み、`scenes/hhd_charcreate_*.json` に 4 枚のレイアウトを場面として書く（目モード / 髪モード、選択中・押下などの状態）。
2. PNG に描いて、利用者のスクショ（`inputs/hhd/screenshots/*_bottom.png` 相当）と画素で比べる（`tools/compare.py`）。
3. 場面（JSON）から BCLYT を作る組み立てプログラム（Clypo のライブラリ）→ DARC。
4. 書き出した BCLYT を designer 自身の読み取りで読み戻して同じ PNG になることを確かめる（往復の照合）。

designer に足りないもの（`docs/status.md`）: ブラウザの設計画面は無いが、場面 JSON を手で書いて PNG にする流れはある。
BCLYT の書き出し・HHD 素材の取り込みは新規。

## 6. gohan 側の作り（段階 1）

| 部品 | 役割 | 手本 |
|---|---|---|
| `HhdCharaScreen` | DARC を読み込みゲームのヒープへ写す → `ArcResAccReader_Ctor` → `Attach` → `Layout` 4 枚を組み `LayoutMgr` に登録。閉じるときは逆順に片付け | `GameLabel.cpp`（Layout・Anim・AddLayout の手順）、`GameList.cpp`（出入りと下画面の表示状態） |
| `HhdButton` | HHD の `ButtonBaseActor` の部分写し: Wait / Select / TouchSelect / TouchUnSelect / TouchDecide / Decide / Invalidate。枠の中で押す → 沈む（y −2）、枠の中で離す → 決定（touch_ok ＋ select_ok の明滅）、外へ → 戻す、A → 決定 | HHD-F004 |
| `HhdSelectGroup` | 1 つだけ選ばれる組（目の色 6 / 髪の色 16 / 肌の色 8 / 目の形 12 / 髪 8×ページ）。選択中の枠は白 → 橙と縞の流れ | HHD-F003 / F004 |
| `HhdHairPager` | 髪 32（男の子 0〜15 / 女の子 16〜31）を 8 個ずつ 3 枚の枠で回す。L / R・左右の端・ドラッグで送る | HHD-F005 / F007 |
| 流れ | 「かみがた / かお」で目 ↔ 髪を入れ替え、色の変更を全ボタンへ、目か髪を選ぶと「けってい」が有効、「けってい」で閉じる | HHD-F006 |
| 入力 | 開いている間はゲームへの入力を塞ぐ（既存の入力遮断）。タッチ・A・B・L・R・十字を gohan が読む | `DOCS/input_block.md`（旧 F-350〜F-355） |

- 開く・閉じる: 段階 1 はフェード無しで `in` / `out`（HHD の値: 28 フレームのアルファ）だけ。
- 実装は gohan の**作業用ブランチ**（実機確認前に main へ入れない）。

## 7. 進め方と確かめ方

1. 道具の確認（**済み**、3.1）。
2. 最小の実機確認: 地（`hhd_bg`）だけの DARC をメモリから Attach して下画面に出す（Attach・VRAM 転送・LayoutMgr の 3 点を一度に確かめる）。
   実機での確認は利用者に依頼し、画面は Chokistream の画像で確かめる（`docs/dynamic_observation.md`）。
3. 全ペインの静止画 → 色の反映 → ボタンの状態と入力 → 髪のページ送り、の順に足す。各段で designer の PNG と実機の画像を比べる。

## 8. 未確定・利用者に確かめること

- **ACNL の見た目データとの対応（段階 3 で必要）**: HHD は髪 32・髪の色 16・目の形 12（×性別）・目の色 6・肌 8。ACNL 側の髪型の数・顔（目）の種類・日焼け（肌）の段階との対応は未調査。
  段階 1 の画面は HHD の絵と数のまま作り、対応は段階 3 で決める。
- メモリ上の DARC の Attach と VRAM 転送は静的な見込みで、実機では未確認。
- ACNL の BCLYT に部品ペイン・HHD の材質（白黒 2 色の補間・2 枚のテクスチャ）と同じ表現があるか（designer の描画器で確かめる）。
- 反証条件: Attach が romfs 以外の置き場を受け付けない、VRAM 転送が gohan の確保したバッファから失敗する、Clypo の往復で BCLYT が一致しない。
