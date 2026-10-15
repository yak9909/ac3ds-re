<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / item

| ID | 題 | summary | 確度 | 格付け | 訂正 |
|---|---|---|---|---|---|
| ACNL-F0040 | F-02 アイテムは 4 バイト構造 — `HIGH` | ``` | HIGH | ? |  |
| ACNL-F0045 | F-07 アイテムID 158 は「穴」 — `MEDIUM` | **根拠**: 多くの掘る系アクションの結果として 158 が生成され、 | MEDIUM | ? |  |
| ACNL-F0050 | F-12 `Field_GetItemAtXY` はポインタを返す — `HIGH` | `Field_GetItemAtXY(mapmgr, x, y, 0)` → そのマスのアイテム(4B)への**ポインタ**。 | HIGH | ? |  |
| ACNL-F0071 | F-33 `Item_Copy` ではオブジェクトが破棄されない — `HIGH` | マップデータに直接 `Item_Copy` で書き込むと、**元々そこにあった物のオブジェクトが | HIGH | ? |  |
| ACNL-F0082 | F-44 `Item_PlaceItem` (0x59E5B4) — 資料と逆コンパイルが完全一致 — `HIGH` | 出典: `REFERENCES/TEXTS/drop_method.txt`。**実機の逆コンパイルと行単位で一致した。** | HIGH | ? |  |
| ACNL-F0094 | F-56 `ACNL_ID_Lists-master` との照合 — 4 件確定・1 件は資料側が誤り — `HIGH` | Vapecord 作者による ID 一覧 `REFERENCES/IDS/ACNL_ID_Lists-master` と、 | HIGH | ? |  |
| ACNL-F0107 | F-69: 通常カタログは屋外表示可能。壊れる根因は店内限定の検索 `DICT` | confidence: **HIGH**（画面・注文・部屋分岐は `code.bin.i64` で静的確認。屋外起動の実機試験だけ未実施） | HIGH | ? |  |
| ACNL-F0108 | F-70: 標準カタログの家具3Dは `BsFtrMgr` 経路。stock屋外はmanagerを生成しない | confidence: **HIGH**（生成経路と屋外許可は静的確認、室内オブジェクトは実機確認）、 | HIGH | ? |  |
| ACNL-F0112 | F-74: field持ち物の開始点はplayer state `0x16`。同位置で公式catalog要求へ置換可能 | confidence: **HIGH**（制御フロー・命令・戻り値と第1版の停止状態を `code.bin.i64`・実機で照合）、 | HIGH | ? |  |
| ACNL-F0115 | F-77: catalog表示後にstock「上タブをすべてアウト」を走らせる構成 | confidence: **HIGH**（状態record・enter/update・遷移callを `code.bin.i64` で確認）、 | HIGH | ? |  |
| ACNL-F0119 | F-81: constructor成功同期版はCatalogを生成後、`0x20`で表示前に自己終了させる | confidence: **HIGH**（3 hookの静的制御フロー、`MENU_FLAGS`契約、直近実機症状を照合） | HIGH | ? |  |
| ACNL-F0120 | F-82: Catalog終了はfield X ownerを戻さず、3D経路には屋外hard rejectがない | confidence: **HIGH**（Catalog end、field X開始、通常持ち物終了の静的比較）、 | HIGH | ? |  |
| ACNL-F0123 | F-85: CameraCatalog、Catalog専用3灯、3つのrenderer layerはroom 0にも存在する | confidence: **MEDIUM**（各ctor/createとroom分岐、global renderer loopを静的照合） | MEDIUM | ? |  |
| ACNL-F0127 | F-89: 2回目の同一SIGSEGVはmanager phase 3の屋外map走査。Catalog選択品とは別 | confidence: **HIGH**（2回目のstack、Item request、phase 3逆アセンブル、命令stepを照合） | HIGH | ? |  |
| ACNL-F0128 | F-90: 3回目は選択Item `0x2EA3` のtype `0xBC`。基底`AcFtr`置換でgeneric create完了 | confidence: **HIGH**（例外register/stack、ItemParam record、3 virtual targetとreturnを命令stepで照合し、 | HIGH | ? |  |
| ACNL-F0130 | F-92: rev7は家具3Dには成功。壁紙・絨毯は非表示、服カテゴリは`ModelInstance_SetRenderLayer`でSIGSEGV | confidence: **HIGH**（家具表示結果とcrash PCを既解析の静的関数へ照合）、 | HIGH | ? |  |
| ACNL-F0419 | 持ち物・trash・selected行の実機不具合訂正（2026-10-13） | GPT-6/idalib、MEDIUM（原JPN ARM＋caller/RTTI/CTRPF/Vapecord＋PC、実機未確認）。CommitのnestedCopyはTLS[15]をCOPYへ変更し、旧GetCurrent再取得がCOMMIT引数でCOPYへ戻る。入口ctx保持で修正。script::WordFix65のnativeCtor/Appendを検証し、row172内word156/UTF16bufferを型に適用。 | MEDIUM | ? |  |
| ACNL-F0420 | list再tap・drag倍率・pocket操作（2026-10-13） | IDA（idalib）/GPT-6、MEDIUM。selectedrowをnative待機が毎回node217=0へして再tapを禁止する。owned行だけ戻し、別touchfocusを持つと初tap選択/再tap実行になる。A/再tapはnativeStartDecideで音と2anim。scroll pressのknob/trackは別経路、dragだけ初期localpointから0.5倍へ変換すると原8→4、track9→9。指を止めても動かない。原ARM＋native | MEDIUM | ? |  |
| ACNL-F0473 | 持ち物の選択窓（ItemSelectWindow）のキー操作 — 十字・A・B の実装（2026-09-28、MEDIUM: 静的のみ。gohan d6b8470 で使用、実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: 一覧が出ている間、ゲームと同じく十字で選択・A で決定・B でやめる（推測で自前実装しない）。 | MEDIUM | S |  |
| ACNL-F0480 | 模様替えの範囲選択・移動の吸着と音、持ち物の選択窓（ItemSelectWindow）の正しい使い方（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 手直しは実機未確認） | 解析ソフト: IDA（主 IDB）＋ CRO の逆アセンブル（tools/patches/cro_rtti.py）/ 解析モデル: opus-5.5。利用者の指摘（範囲がマスに吸着しない・音が無い・ | MEDIUM | S |  |
| ACNL-F0481 | 持ち物の選択窓（ItemSelectWindow）と模様替えの範囲の枠（CollectChip）の作り（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 は実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。マップエディターの範囲選択（利用者の決定: 案 B）のため。 | MEDIUM | S |  |
| ACNL-F0483 | 模様替え UI（BsMenuInteriorEditor）の作りと、持ち物欄の名前の吹き出し（ItemSelectNameWindow）の使い方（2026-09-27、MEDIUM: 静的のみ（逆アセンブル＋romfs）。実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「マップエディター（gohan Issue #16）」の下調べ。 | MEDIUM | S |  |
| ACNL-F0484 | アイテムの名前とアイコンの決まり方、没アイテムの割り出し（2026-09-27、MEDIUM: 静的＋ROM の実データ。Ghidra-gpt-sol-5.6-ITEM-T011 と独立一致。gohan の名前差し替えは実機未確認） | **名前** `ItemName_ResolvePhrase 0x56D274`(phrase, &item, a3): phrase を空に（vt+28）→ 通常の ID は `STR_Item_name` の (ID&0x7FFF)−0x2000 番 | MEDIUM | S |  |
| ACNL-F0485 | ゲームの「持ち物に入れる」は 0xFD 以下の ID を写し替え、空に写しても成功を返す／没アイテムを隠す分岐（2026-09-27、MEDIUM: 静的＋利用者の実機報告と整合。修正版は実機未確認） | 利用者の実機報告（F047 の版）: ポケットアイテムで 0xFF 以下などが入らないのに「入れました」と出た。 | MEDIUM | S |  |
| ACNL-F0486 | 持ち物へアイテムを入れるゲーム自身の処理と、持ち物画面のアイコンの作り直し（2026-09-26、MEDIUM: 静的＋実機実績のある外部実装と独立一致。gohan の実装は実機未確認） | ポケットアイテム（gohan.md §17.5）の下調べ。資料の ID 一覧に頼らず、ゲーム自身の処理を使う（2026-09-17 の利用者判断）。 | MEDIUM | S |  |
| ACNL-F0615 | ゲームのカタログのプレビューは 2 枠を交互に使い、替えた前の枠は 1 フレーム後にすぐ壊す（2026-10-06、MEDIUM: 静的） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | MEDIUM | S |  |
| ACNL-F0618 | ACNL の部屋の家具の持ち方と「かざる」「拾う」の入口（2026-10-06、LOW〜MEDIUM: 静的 + 先行資料。途中） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022 の ACNL 側の下調べ。 | LOW | S |  |
| ACNL-F0620 | 家具をその場で消すゲーム自身の手順（2026-10-06、MEDIUM: 静的。実機は試験 4 待ち） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022。 | MEDIUM | S |  |
| ACNL-F0621 | 模様替え UI のドラッグ・離す・チップと家具の記録の関係（2026-10-07、MEDIUM: 静的のみ。ModuleIndoor.elf / ModuleFtr.elf と主 IDB） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022（ゴミ箱・家具リスト）の前提。番地は cro_to_elf の便宜上の基準（text 0x00B00000）。名前は work/cache/cro_elf の両 IDB に付けた（キャッシュは再生成で消えるのでここが正）。 | MEDIUM | S |  |
| ACNL-F0623 | 模様替え UI を開いたまま家具を出す材料（2026-10-07、MEDIUM: 静的のみ。途中で打ち切り） | 解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_spawn.md）。利用者の 5 時間枠の都合で途中で打ち切り、同じセッションを再開してまとめさせた（IDB には触れさせず）。記録・採番・照合は親（opus-5.5）。 | MEDIUM | A |  |
| ACNL-F0624 | HHD と ACNL の品の名前での突き合わせと、ACNL の Item.bin のカテゴリ（2026-10-07、MEDIUM: 静的 + ROM の実データ） | 解析ソフト: IDA（capstone で code.bin を直接）/ 解析モデル: opus-5.5。T022 の品の対応（F101 の「曖昧な 1,410 件」）。 | MEDIUM | S |  |
| ACNL-F0625 | 模様替え UI を開いたまま家具を出す手順の詰め（2026-10-07、MEDIUM: 静的のみ。利用者の 5 時間枠で打ち切り） | 解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_spawn2.md、F001 の続き）。採番・照合・記録は親（opus-5.5）。 | MEDIUM | A |  |
| ACNL-F0627 | 服・ワンピース・K.K. の曲を部屋に置くときの品番（2026-10-07、MEDIUM: 静的 2 経路） | 解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_pair_ids.md、アプリサーバー経由）。採番・照合・記録は親（opus-5.5）。根拠 **work/evidence/t022_pair_ids/report.md**。主 IDB に命名 13 関数・2 表、型 19、構造体 2、カテゴリの Enum、コメント 58（ID  | MEDIUM | A |  |
| ACNL-F0631 | 家具が置けない・壁紙が張り替わらない原因（2026-10-08、HIGH: 実機 BP＋静的） | 解析: 親（opus-5.5）が ida-pro-mcp の BP で測定、Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix2、--allow-gohan）が静的解析と修正。根拠 **work/evidence/t022_catalog_fix2/report.md**。gohan 1746df8。 | HIGH | A |  |
| ACNL-F0646 | カスタム風船drop中にinventory Player stateが0x16→0x06へ遷移する | **確度: HIGH（実機挙動）。旧FieldAction原因仮説は棄却。** | HIGH | B |  |
| ACNL-F0648 | inventory drop完了はFieldAction handleのstatus 2待ちで成立する | **確度: HIGH（添付bytesの命令列＋実機症状が一致）。** | HIGH | B |  |
| ACNL-F0650 | synthetic completion handleでinventory完了契約だけをエミュレートする | **確度: MEDIUM（静的検証済み、実機未検証）。** | MEDIUM | B |  |
| ACNL-F0651 | custom balloon drop中のinventory state 0x16→0x06をmenu-open guardで抑止する | **確度: MEDIUM（静的検証済み、実機未検証）。** | MEDIUM | B |  |
| ACNL-F0656 | stock inventory dropはPlayer stateを変更しない。state 0x16はmenu open時に明示設定される | **確度: HIGH（main .textのcall chainを入口からcompletionまで静的追跡）。** | HIGH | B |  |
| ACNL-F0665 | terminal landingをcustom AcBalloon identityで識別し、元Inventory Itemをpayloadにする | Ghidra-gpt-sol-5.6-F025実機成功後、fieldへ落ちるItemがなお 0x2036 のプレゼント（中身ランダム）だった。 |  | B |  |
| ACNL-F0667 | custom Item substitutionをstock landing persistence経路へ戻す | Ghidra-gpt-sol-5.6-F027 hardware result: |  | B |  |
| ACNL-F0668 | direct falling visualを維持し、impact時だけground itemを確定 | Ghidra-gpt-sol-5.6-F028 hardware result: |  | B |  |
| ACNL-F0675 | stock inventory-call signature for native queue interception | Ghidra-gpt-sol-5.6-F034 hardware result: |  | B |  |
| ACNL-F0690 | item name/icon resource pipeline | Normal Item ID index: `((id & 0x7FFF)-0x2000)`, valid for index < `0x172B`. |  | B |  |
| ACNL-F0691 | low field-object display fallback | User hardware observation: Item IDs 0x0000..0x00FA appear with one shared furniture/default icon and name `???`. |  | B |  |
