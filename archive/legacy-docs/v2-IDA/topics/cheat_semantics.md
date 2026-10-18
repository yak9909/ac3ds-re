# 収録済みチートの意味コメント — 中断時の引継ぎ

更新: 2026-10-11。意味レビューは **TreeSitter-gpt-6-F003 / T003**、バイナリ照合・DB反映は **IDA-gpt-6-F001**。実担当モデルgpt-6。元の収録・旧解析者の帰属は保持する。

## 最新指示と進捗

利用者の「一旦整理を中断、続きは今度、諸々の文書化」により中断。利用者の再開指示までレビューを増やさない。JOKER/他CTRPFの新規収録と共有設定callbackの統合も中断を維持する。Gitのcommit/pushは全作業後の一括指示に従い保留。

| 項目 | 中断時点 |
|---|---:|
| 既存の収録関数 | 2700 |
| 個別意味レビュー・関数内コメント反映済み | 1360 |
| 意味レビュー未完了 | 1340 |
| 既存収録が対応する原候補 | 3417 |
| 新規収録の保留グループ（意味レビューとは別） | 899 |
| 非実行メタデータ | 32 |

レビューの目的は、資料・消費側・近いコードから「ゲーム内で何を変えるか」を推測すること。「アドレスを保持」「固定値上書き」「OFFは実行停止」などの自明な機構説明は却下済み。根拠が不足するものを原名の言い換えで埋めない。

## ファイルの所在

- ソース/ヘッダ: `src/gohan/reference/cheat_collection/Sources/`。通常プラグインへ未統合。
- 公開側の個別根拠: 同フォルダの `semantic_notes.json`。確度、原資料、照合内容、未確認点を記録。
- 公開側の進捗・完全逆差分: `status_semantics.json` / `semantic_manifest.json`。意味コメント層を剥がすとF002の最適化済みソースへ完全復元する。
- 調査台帳: `work/evidence/cheat_semantics/reviewed_notes.json`。中断時点で公開側と1360件一致。
- 全件索引: `catalog.json`。全資料検索DB: `work/cache/cheat_semantics/materials.sqlite`。同SHAのコピー資料を独立証拠に数えない。
- 未レビュー全1340関数・ファイル別件数・入力byte照合: `work/evidence/cheat_semantics/paused_checkpoint.json`。
- 完了ログ: `work/logs/cheat_semantics_publish_1360.log`。

中断文書の更新で可変 `work/FINDINGS.md` の全体hashが変わったため、参照していたF071節を `f071_motion_argument_excerpt.md` へ固定保存し92関数の根拠参照だけを更新した。意味/comment/ソースhash/レビュー数は不変。最終 `cheat_semantics_paused_source_validation.log` は1360/1340・token/完全逆復元/根拠hash PASS。元の解析者opus-5.5への帰属を保持する。

全資料の対応形式はtext/PDF/SQLiteを索引化済み。詳細は `materials.json`。抽出エラー0だが、未対応のbinary/IDA内部形式を全文読了した意味ではない。既存解析・原sourceから不足する部分だけバイナリで照合した。

## 最新のレビュー

| 対象 | 照合・区別 | 根拠（work/evidence/cheat_semantics内） |
|---|---|---|
| 店舗商品selector 20 | 全選択肢をARM実保存Item配列へ照合。出品、外装商品、解禁状態、用途未確定のリメイク関連配列を区別 | `native_shop_item_reviews.json` / `save_layout.json` |
| native施設8＋高額買取1 | 独立施設editorと段階を照合。まめつぶの別状態欄は変更しない。高額買取は出品欄ではない | `native_facility_reviews.json` |
| 効果音引数9 | C4が音ID/再生frameを読みActor_PlaySoundへ渡す。音源表の実名を注記。動作開始/即再生は保証しない | `sound_argument_reviews.json` / `play_sound_c4_{static,consumers}.json` |

直前のAddress系64では、Grassの版別の日本語対象が異なること、fruitStaysが引数準備だけを飛ばしてcallは残ること、CLUB444という原名のコードがReddを対象とすること等を記録した。`address_patch_reviews.json` を参照。原の挙動は修正せず実行tokenを保持する。

## 保存した最新DB概念

対象は日本語更新版 `ida/db/acnl_jpn_v15_annotated.i64`。入力SHA-256: `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。静的照合MEDIUM、固定heap/現boot一致はLOW。実機操作なし。

- C4 entry/updateを `PlayerState_PlayMotionAndSound_Enter` / `Update` と命名。`PlayerC4ArgumentBlock` はpacked 12B: motion `+0`、sound `+2`、再生frame `+6`、signed duration `+7`、exit state `+9`、意味未確定2byte。C5の後続motionと同bufferの別用途。
- 島runtime getter/constructor/acre/building/item quadrant accessorの5関数を命名。`IslandRuntimeData` はpacked `0x102A`: 先頭未知2byte、`+0x2`の4×4 u16区画、`+0x22`のItem 4×256個、`+0x1022`の建物2個。既存 `vc_ISLPOINTER` 名は保持して型だけ反映。
- 保存/readback成功。C4 local型適用2件は失敗・変更なし。後のlocal rename3件は成功/readback/save。型全体がlocalへ適用済みとはしない。島のbuilding constructorはno-opで、空IDを初期化するとは扱わない。

主IDBはsave/closeして所有者0。最新XML/付随bytesは `artifacts/exchange/ida/acnl_jpn_v15.xml` と同フォルダのmanifest/validationへ保存。公式Exporter、構文/参照/原入力全bytes/hash検査PASS。最新7関数名・4型のXML読戻しは `paused_xml_readback.json` に保存。進行中・成否不明の操作なし。

## 途中の島調査 — 個別レビューへ未採用

`island_runtime_{static,consumers,accessors,initializers,bytes}.json` にassemblyと原入力照合を保存。地形16・建物16候補はまだ意味台帳/commentへ追加していない。

1. u16区画16個はheap候補 `0x301A9D12` から。全word版は未知headerと配列末尾の次の領域も変える場合がある。現bootのheap一致は未確認。
2. heap候補 `0x301AAD34` のfullwordは建物1のx/zと建物2のIDにまたがる。`0x301AAD36` のbyte変更は建物2のID下位だけ。原名「ハニワ」と単一建物変更を同一視しない。
3. 平地化の追加書込み `[0x928548,0x92856A)` は現行日本語版では `AcNpcSpExhibitionIn` 等の名前文字列に重なる。区画配列と断定しない。
4. 建物IDは既存 `work/evidence/strc/building_catalog.json` とBuilding_GetNameの索引で照合する。原名「駅」0x51は `sobj_officeB`、0xAEは `fobj_bench_wst`、0xB1は `fobj_drinking`、0xBCは `fobj_clock_wst`。原名の日本語名称は追加照合が必要。
5. 原RGBA順でプレビュー36個を復号し `acre_preview_contact_sheet.png` / `acre_preview_evidence.json` へ保存。0x9F/0xA0/0xA8等のhalf-acreは短い原ファイルなので不足pixelを透明と明記した。vendorの視覚資料であり実機地形の確定証拠ではない。

## 再開手順

利用者の再開指示後、STATE→SESSION→本書を読み、公開側と調査台帳の件数・hash・非comment token不変を確認する。新規収録の再開指示と意味調査の再開を区別する。

次は上記の島32候補を全原body/byte集合・consumer・既存建物表・プレビューと照合し、LOWのまま個別意味台帳へ記す。取得済み関数を新証拠なしに再解析しない。実行中publisherがないことを確認して台帳を編集し、`semantic_annotations.py --publish` でtoken/完全逆復元を検査して反映する。

全件完了時は全2700の意味coverage、原資料/全partition/復元と必要な最終検証を行い、最新DBのXMLを出力・検証してからGitを一括保存する。構造最適化ゲートPASSは、未完了1340件のゲーム効果確認を意味しない。
