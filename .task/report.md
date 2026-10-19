## 結果

完了。指定の作業用IDBに名前・型を適用し、symbolsへ書き出した。新規34型（ほかに不透明型の前方宣言1）、24関数の型、4大域、指定8 vtableの型を設定。確度はMEDIUM、実機操作なし。対象ごとの範囲と保留理由は下表。

| 対象 | 名前・型を付けた結果／保留理由 |
|---|---|
| 0x00121B34 | `GpuCmd_CreateLists`。`void (int count, unsigned int *ids)`。件数分の生成であり1本限定ではない |
| 0x00121988 | `GpuCmd_AllocateListStorage`。`void (unsigned int command_bytes, int gx_capacity)` |
| 0x00127D98 | `GpuCmd_DestroyLists`。`void (int count, const unsigned int *ids)` |
| GpuCmd_GetProperty 0x00127EDC | 既存名維持。`void (unsigned int property, unsigned int *output)`。caseにより2語出力あり |
| GpuCmd_SelectList 0x001216BC | 既存名維持。`void (unsigned int id)`。疑似Cの余分な引数を採用しない |
| nw_lyt_AllocMemory 0x004B8CF0 | 既存名維持。`void *(unsigned int bytes, int alignment)` |
| ssys_ma_Allocator_Free 0x00569B44 | 既存名維持。`void (SsysMaAllocator *allocator, void *pointer)`。R1を尾呼出しへ引き継ぐ |
| ssys_ma_lyt_LayoutMgr_GetInstance 0x00133A64 | 既存名維持。`SsysMaLayoutMgr *(void)` |
| Frame_DrawPass1024 0x001B71C4 | 既存名維持。`void (void)` |
| 0x0096FC38 | `g_LayoutMgr` / `SsysMaLayoutMgr *` |
| 0x0096F150 | `g_LayoutAllocator` / `SsysMaAllocator *` |
| 0x0097C0B4 | `g_DefaultWideTagProcessor` / `NwFontTagProcessor`。vptrを持つ実オブジェクトでありholderではない |
| 0x0097C0B0 | `g_DefaultWideTagProcessorGuard` / `unsigned int`。4B語のbit0を検査するためboolにしない |
| Pane | `NwLytPane` 0xD4。子の循環リスト・親・寸法・移動回転縮尺・局所/大域行列・可視を含むflags・アンカー・元/計算後alpha |
| Picture | `NwLytPicture` 0x158。UV結果、別確保の座標セット、Material、四隅の色 |
| TextBox | `NwLytTextBox` 0x108。UTF16文字列・バイト容量/実文字数・書体・Material・batch・配置・dirty |
| 文字描画batch | `NwFontTextBatchPrefix`。先頭0x28のみ。可変長の全体サイズと未判明flagsは型に固定しない |
| Material | `NwLytMaterial` 0x50。七色・容量bits・使用数bits・可変領域ポインタ・flags。可変領域全体を固定型へ重ねない |
| ResFont | `NwFontResFont` **0x18**。依頼の0x20は採用しない。通常確保と別クラス内の埋込み境界がともに0x18。詳細はACNL-F0711 |
| FINF | `NwFontFinf` 本体0x18。正規化後のポインタ・既定幅・寸法・encoding等。chunkヘッダ8Bは含まない |
| TGLP | `NwFontTglp` 本体0x18。cell・sheetの寸法/枚数/書式/データ |
| CWDH | `NwFontCwdh` 固定先頭8Bと `NwFontCharWidths` 3B。後続は可変長であるため固定長列にしない |
| CMAP | `NwFontCmap` 固定先頭0xC。後続は方式依存なので詰め物/別解釈。方式の分岐は記録した |
| DrawInfo | `NwLytDrawInfo` 0x8C。投影/view行列・補正倍率・alpha・文字作業体・flags |
| Layoutノード | `SsysMaLayoutNode` 0x14C。root・内包DrawInfo・優先度/リンク・記録ID/範囲/容量・dirty・display等。作業体はDrawInfo+0x80を介して参照 |
| Layout管理者 | `SsysMaLayoutMgr` は+0x368までの部分型（全確保0xA08）。上下リスト、文字作業体+0x1C、Drawer先頭+0x364 |
| 文字作業オブジェクト | `NwLytTextWork` の確認範囲0x2E4。+0x13C一時batch・+0x164 Pane行列のみ命名。その他のメンバーは未解明のためunkで保持 |
| アロケータ | `SsysMaAllocator` 8Bとvtable。heap*、alloc/free。Alloc本体にも3引数の型を追加 |
| ExpHeapと空き一覧 | `SeadExpHeapPrefix` 先頭0x98、`SeadExpHeapList`、`SeadExpHeapBlock`。free/usedの番兵・件数・link offset、ブロック次/前・整列ずれ・payload長。全体サイズは未確定 |
| Pane vtable 0x008FBE7C | `NwLytPaneVtable`。28 slotの形、calculate_mtx/draw_selfのABI。その他のslotは個別契約を網羅していないためvoid* |
| Picture vtable 0x008FBFFC | `NwLytPictureVtable`。30 slot、Pane部分を内包。追加2 slotのABIは保留 |
| TextBox vtable 0x008FC07C | `NwLytTextBoxVtable`。32 slot、共通描画と文字列確保/解放。残りの固有slotはABI照合未了でvoid* |
| Material vtable 0x008FC18C | `NwLytMaterialVtable`。11 slotの形のみ型付け。各slotの完全なABIは今回網羅せずvoid* |
| ResFont vtable 0x008FCAAC | `NwFontResFontVtable`。27 slot。幅/高さ/line feed/glyph/encoding/filter/sheet数を型付け。未確認slotはvoid* |
| DrawInfo vtable 0x008FC17C | `NwLytDrawInfoVtable`。2 slotの形のみ。破棄関数等のABIを推定していない |
| TagProcessor vtable 0x008FCA24 | `NwFontTagProcessorVtable`。4 slot、process/calc_rectを型付け。先頭2 slotはABI保留 |
| ExpHeap vtable 0x008FFEF8 | `SeadExpHeapVtable`。27 slot、try_alloc/free/get_free_size/get_max_allocatable_sizeを型付け。残りはABI保留 |

検証：IDAが保持する34型のサイズ・全命名メンバーのoffsetを機械照合済み。一次資料は74関数の全書き出しと、codebytes経由の8 vtable。`kb.py lint` は全733件エラーなし、関連テスト99件通過、最終 `audit.py` は996ファイル問題0件。変更後の実ファイルにも監査を適用して問題0件。

vtable構造体の適用型が書き出し時に落ちる既存仕様を修正し、既存のglobals形式でも型を保存して復元時に保持するようにした。監査の型ヘッダ中の関数ポインタ宣言に対する誤検出も、宣言だけを区別する修正と検出の維持を確認するテストを加えた。

復元往復も一致。作業IDBを検証用に複製し、8 vtableの適用型を除去してから全symbolsを取り込み、8構造体型の復元と再書き出しを確認した。関数1767・大域8658・コメント2644・vtable2586・lvar9行、型261件が一致（IDB外のmetadata列を除く）。結果は `_local/evidence/98/roundtrip-result.json`。code.binからの新規IDB全自動解析は長時間待機のため停止し、その検証は完了扱いにしていない。

## 結論と根拠の要約

- ACNL-F0709：GPUリストの件数/ID配列とstorage契約。本体の命令とLayout Build/破棄・主リスト生成を照合した。
- ACNL-F0710：Pane/Picture/Materialの既知配置を既存A格付け再解析と一次資料から型化。木走査の描画ABIはR0 Pane/R1 cursor/R2 DrawInfo/R3 context。
- ACNL-F0711：TextBox/batch、フォント資源本体、既定wide TagProcessor。ResFontの0x18は通常確保と独立した埋込み境界で確認。
- ACNL-F0712：DrawInfo、Layoutの記録・画面・root、管理者上下リストと文字作業体の対応。生成/初期化と使用側が整合する。
- ACNL-F0713：アロケータの尾呼出しABI、ExpHeapのfree/usedリストとpayload走査。総空きは最大連続空きと異なる。

## 訂正の提案

- 依頼文のResFont 0x20は、本ビルドの通常実体について0x18へ訂正する。既存記録本文の同じサイズ誤記は今回特定していないため、supersedesを推定で付けない。
- 既存のPane描画関連プロトタイプで省略されていたR3を補った。既存名は変更していない。資料の旧3引数表示をABIの根拠にしない（ACNL-F0710/F0712）。

## 統合・重複の提案

ACNL-F0709/F0710/F0712/F0713の基本配置・寿命の多くは既存のACNL-F0693～F0708と一致する。今回の型名・部分型の範囲とABI、およびACNL-F0711のフォント/既定processor/ResFontサイズを topics/acnl/ui.md へ統合できる。

## 新しいタグの提案

なし。

## 未確認点

実機での自前Pane/Picture/TextBoxの上下画面表示、資源とheapの寿命、GPU完了・容量不足、各vtableの保留slot、文字作業体/Drawer/ExpHeap全体の未知メンバー。今回の型付けから表示成功や安全な再確保を主張しない。

## 次の1手

残ったvslotのABIが必要になった時点で、そのslotの実装と独立した呼出し元を照合する。実機検証が別途許可された場合は上下パス・記録/再生・文字/画像・解放前後を同時に観測する。
