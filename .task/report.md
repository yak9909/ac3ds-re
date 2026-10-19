## 結果

完了。8項目を一次証拠で判定し、確認できた名前・型を指定の作業用IDBへ適用した。確度はすべてMEDIUM（生産側と独立した消費側の静的根拠、実機なし）。推定だけの名前は追加していない。

| 項目 | 判定と名前・型 | 付けなかった名前・型と理由 |
|---|---|---|
| 1 Layout vptr・仮想関数 | SsysMaLayoutNodeVtable*を適用。Replay/Record/Setupはvoid(Layout*)。Setupはthisの幅・高さ・projection_modeを読み、内包DrawInfoへ書く。投影済flagの更新はRecord側 | 先頭2slotのABIとBuildのresource_holder具体型は確証不足。Build slotは4引数であり、単一this callbackに統一しない |
| 2 有効・画面・記録設定 | +F0のview_eye[3]（+F8はfloat Z）、+FC animation_flags、+114 replay_state_mask。+118 command_capacity_bytesの名前を確認して維持。上下はAddLayout引数0/1 | +F8=有効/+FC=画面という説は反証。+114をGX容量と呼ばない。有効フラグは今回の欄に見つからず推定追加しない |
| 3 Material可変領域 | TexMap/TexSrt/TexCoordGen/AlphaCompare/BlendMode/TevStage要素型とgetter、容量・件数mask名。配列境界は容量欄、巡回は件数欄。variable_dataは先頭TexMap列のポインタ | TexMap+0、Genの未確認byte、TEV内部bitsはunknown。容量0のTexMap実在を保証しない |
| 4 ResFont/CWDH/CMAP | 0x14のsheet descriptor型。+4 font、+8変換後物理番地>>3、+C高さ/+E幅、+10 u8 GPU書式。CWDH widths[]は+8/stride3、CMAP方式2 pairs[]は+E/stride4、件数u16は+C | LA4という成分名と9の対応は一次命令から独立証明できずEnum名を追加しない。descriptor末尾3Bも未確認 |
| 5 文字バッチ | 固定ヘッダー0x28、glyph_count(+4)、draw_glyph_limit(+6)、初回色command語offset(+24)、44Bのglyphs[]、bitmap・整列・必要量式を型と記録へ反映 | +6は確保上限ではなく描画制限（初期0xFFFF）。+Aの2Bとflags全bitsは未命名。ゲームの必要量関数を任意先頭アドレスの保証としない |
| 6 Pane補助リスト | Pane+1C/Material+4を件数＋8B循環番兵型へ。実リンク0x10にはtransform/target_index/disabled。評価・解除・検索の関数/vslot型を反映 | 番兵を16Bの実リンクと重ねない。実リンク+FとAnimTransform本体は未確認のため不透明 |
| 7 既定TagProcessor | nwfont_InitDefaultTagProcessorsと起動時相対表の該当語を命名。start→初期化表巡回→0x79B70C。guardはStaticGuardAcquire内でvptr書込み前に1となる | TextBox描画時の遅延初期化とは呼ばない。TextWriter ctorは既定オブジェクトへのポインタを置くだけ。並列安全性は未確認 |
| 8 storage失敗 | void型を維持し、現在managerの既知先頭型を適用。+4が確保結果。確保結果null検査なしでGX領域ゼロ埋めへ進むことを記録 | bool/status戻り値の根拠なし。失敗すると復帰前に障害になり得るため、復帰後のnull確認を一般的な失敗通知方法としない |

検証：作業用IDBへの現行symbols取込みは失敗0。21型の固定sizeofと主要offsetを照合し、CWDH・CMAP方式2・文字バッチの柔軟配列もsize0と先頭offsetを検証した。指定コピーからsymbolsを書き出した。kb.py lintはエラーなし（索引生成後の再検査も実施）。全体audit.pyの初回は1002ファイル中CRLFの8件だけを検出し、LFへ修正後、変更後の現物24ファイルをaudit.scan_fileで再検査して問題0。

## 結論と根拠の要約

- ACNL-F0714：Layoutの仮想表とメソッドABI、視点/アニメーション/再生mask/容量。ctor・原本表・計算・記録・再生・上下登録が一致。
- ACNL-F0715：Materialの要素型と容量による実配置。予約処理・getter・UV/状態送出が一致。
- ACNL-F0716：Pane/Materialのアニメーション番兵。二つのctor、評価、検索、件数を減算する解除処理が一致。
- ACNL-F0717：シート記述子と正規化されたCWDH/CMAPの可変配列。初期化・glyph取得・二分探索・command構築が一致。
- ACNL-F0718：文字バッチ全固定ヘッダーと字形レコード。蓄積側・command構築側・確保式から型と必要量を確認。
- ACNL-F0719：既定processorは起動時初期化表から作られる。相対語の原本値とstart/巡回/guard/ctorの命令を照合。
- ACNL-F0720：storageには失敗status返却がない。nullでもゼロ埋めする分岐と、戻りを検査しないBuild側を確認。

## 訂正の提案

既存ACNL-F0709〜F0713の結論と矛盾する訂正はなし。依頼の未検証の手がかりには、+F8/+FC、+114、バッチ+6、既定processorの初期化時点について表のとおり訂正がある。

## 統合・重複の提案

ACNL-F0714〜F0720はACNL-F0709〜F0713の型を補う。topics/acnl/ui.mdの「Layoutの記録・再生・容量」「Picture・Material・TexMap」「TextBoxと文字バッチ」へ、視点/flagsと容量の区別、可変配列と起動時初期化の契約を統合できる。

## 新しいタグの提案

なし。

## 未確認点

実機操作なし。LA4の色成分と数値9の対応、残したunknown欄、全flags/TEV内部、OOMとcallback失敗、実際のバッチ先頭整列・使用量・寿命・GPU完了は未確認。

文字バッチのゲームの必要量関数と実command先頭の式には先頭アドレス依存の差がある。N=15/B%16=4の算術例ではcommand先頭の実offset716に対して必要量関数の前半704。実機のbuffer超過を観測したという結論にはしていない。

記録の自己モデル記入は `kb.py stamp --self` を実行したが、環境のAC3DS_MODELが未設定で失敗した。by:autoを維持し、モデル名を推定して管理項目へ書き込んでいない。仕上げ側で実モデル名の記入が必要。

## 次の1手

仕上げ側で7記録の実モデル名をstampし、索引を再生成する。

実機調査を別途許可された作業で、実バッチの先頭整列と最終command使用量を採取し、必要量式との差が実際に問題となるか確認する。残した書式EnumはTGLPの実資源とテクスチャ内容/表示を組み合わせて確かめる。
