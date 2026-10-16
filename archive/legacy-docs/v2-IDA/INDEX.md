# 必要な資料だけ読む

| 内容 | 入口 |
|---|---|
| CPU、入力の由来、ExHeader、IDBの使い分け | [platform.md](platform.md) |
| プラグイン全候補の採否、代替、AI API | [plugins.md](plugins.md) |
| 静的/動的解析、型・差分、導入/復元 | [operations.md](operations.md) |
| IDAの時間制限ResumeとChokistream画面観測 | [dynamic_observation.md](dynamic_observation.md) |
| commit/push前のIDA/Ghidra XML交換 | [xml_exchange.md](xml_exchange.md) |
| Codex CLIをサブエージェントとして使う | [codex_subagent.md](codex_subagent.md) |
| ACNL固有のRTTI/CRO・アドレス判断 | [topics/acnl.md](topics/acnl.md) |
| 収録済みチートの意味コメント・中断/再開 | [topics/cheat_semantics.md](topics/cheat_semantics.md) — 個別根拠、1360/2700、未完了と次の照合 |
| 通信パケット種別番号 `0x00`～`0x84` | [topics/network_packets.md](topics/network_packets.md) |
| 自前描画・正常3gx・しずえスキップ | [topics/gui.md](topics/gui.md) |
| ゲーム内3Dモデルのワールド/画面固定配置 | [topics/models3d.md](topics/models3d.md) |
| モデルの一生（Setup・写し・後片付け）と借りた資源を壊さない規則 | [topics/gfx_model_lifecycle.md](topics/gfx_model_lifecycle.md) |
| 家具の範囲表示を屋外へ出す設計 | [topics/unit_cursor_outdoor.md](topics/unit_cursor_outdoor.md) |
| 任意モデルの読み込み→描画（設計・未適用） | [topics/arbitrary_model_draw_plan.md](topics/arbitrary_model_draw_plan.md) |
| 木の透明度・画面固定の実機結果 | [topics/alpha_screen_plan.md](topics/alpha_screen_plan.md) |
| プレイヤーの複製プレビュー（PlayerModel・部品バンク・髪型だけ変える） | [topics/player_clone_preview.md](topics/player_clone_preview.md) |
| 内蔵辞書の取得・画面なし変換 | [topics/keyboard.md](topics/keyboard.md) |
| gohanの普通チャット漢字候補・ビルド/復元 | [topics/chat_kanji.md](topics/chat_kanji.md) |

現在の仕事は `work/TODO.md`、新しい知見は `work/FINDINGS.md`。旧資料の詳細が必要な場合だけ `python tools/project.py search --legacy "語句"` で以下を検索する。

| 旧資料 | 用途 |
|---|---|
| `reference/old_project/RE/FINDINGS.md`, `reference/old_project/RE/FUNCTIONS.md` | F番号の根拠、解析済み関数。履歴全体は初期読込みしない |
| `reference/old_project/DOCS/structures.md`, `reference/old_project/DOCS/state_tables.md` | 構造/状態名と関数の索引 |
| `reference/old_project/DOCS/rendering.md`, `reference/old_project/DOCS/input_block.md` | 描画、入力遮断。現行GUIはtopics/guiを先に読む |
| `reference/old_project/HANDOFF_MESSAGE.md` | メッセージ/CRO |
| `reference/old_project/DOCS/sound.md`, `reference/old_project/SOUND/index/sounds.csv` | 音IDと素材。ゲーム内IDを名前から逆引き |
| `reference/old_project/DOCS/patches.md`, `reference/old_project/DOCS/ar_codes.md`, `reference/old_project/PATCHES/` | 改造・復元・生成器。古い版の無条件実行は禁止 |

旧 `RE/STATE.md` 冒頭は移行時F407、以降は大量の過去状態。現在の環境作業は `../work/STATE.md` を正とする。資料が矛盾したらIDA/実測の証拠で解決し、該当トピックを修正する。

- [記録ID・解析モデル・確度・頻繁なcommit](record_ids.md)
- [ゲームのリスト UI を借りる汎用部品 GameList](topics/game_list.md) — InstSelect<8>・枠 ctlg_list・アニメ・入力・メモリ（IDA-opus-5.5-F036）
- [建物一覧 BsMenuMapList とマップエディターのモード一覧](topics/map_mode_list.md) — 生成・選択・開いたまま（部屋 164）・行のボタンとタッチ・形の変え方（IDA-opus-5.5-F062）
- [SVC（システムコール）一覧と使い道](topics/svc.md) — ゲームが使う 32 種類・745 か所、Luma の独自 SVC、チートへの応用案（IDA-opus-5.5-F034）

## 別作品

- [HHD（ハッピーホームデザイナー）の資料](hhd/INDEX.md) — ACNL とは分けた入口。キャラクリ画面の解析（IDA-opus-5.5-HHD-F001〜F007）
- [T022 HHD の家具・壁紙/床紙リストとゴミ箱の移植 — 必要なもの・不要なもの](topics/t022_decorate_port_requirements.md) — 模様替え UI 自体は触らない。作る物・作らない物・未確定・確認事項（IDA-opus-5.5、2026-10-07）
- [HHD式室内カメラの移植設計](topics/hhd_room_camera_design.md) — ACNL家の十字キーを連続回転/奥行き変更へ置換（IDA-gpt-6.1-sol-F014、2026-10-10利用者実機PASS）
- [リスト操作と模様替えカメラ移動の設計](topics/catalog_camera_controls_design.md) — 背景UIのフェード、X/B、カテゴリ音、模様替えUI中だけyawに沿ったスライドパッドX/Z移動（IDA-gpt-6.1-sol-F015、新追加は実機未確認）
- [模様替えUI修正・チップ複製・内装保存の設計](topics/interior_presets_design.md) — F015本体非表示の訂正、list中カメラ/3倍速度、native長押し窓、8保存枠への保存/読み込み/交換と即反映/復元（IDA-gpt-6.1-sol-F016、実機未確認）
- [チップ長押し窓と選択アニメの修正](topics/chip_longpress_fix_design.md) — F016の実機不具合を受け、static家具記録の検査と選択カウンタの維持を修正（IDA-gpt-6.1-sol-F017、修正版実機未確認）
- [gohan機能移植とチャットコマンド](topics/gohan_chat_ports_design.md) — FOXXY idle/気絶/Vapecord消失抑制、§14chat、メニュー再編、両editor action/B/排他・公共事業設定全削除（IDA-gpt-6-F002/T001、実機未確認）
- [チャット一覧の入力と時刻窓からの復帰](topics/chat_lists_fix_design.md) — DPad focus/Aかtouch決定・背後入力遮断・検索ID左prefix・time menuのfield ownership（IDA-gpt-6-F003/T004、修正版実機未確認）
- [持ち物UIの再実機訂正](topics/inventory_ui_followup_design.md) — actor singleton/全list取得・消去音・本物のA決定、食べる/置くcheckbox、chat2項目keyboard移設と欠字font再生成（IDA-gpt-6-F013/T016、実機未確認）
- [ゴミ箱の入場座標とCHEATSの既存選択肢](topics/pocket_trash_visibility_design.md) — hidden subtreeの画面外座標残留を原ARM再現・描画を隠してmatrix更新、追加2項目を既存分岐NOP/復元へ訂正（IDA-gpt-6-F014/T017、実機未確認）
- [リストscroll・スタイルarc・検索順の追加修正](topics/chat_scroll_style_fix_design.md) — native scroll用Controller入力の限定差込み、arc一時pool、fgobj含む全ID順（IDA-gpt-6-F004/T005、実機未確認）
- [アイテム名検索の連続取得](topics/chat_search_repeat_design.md) — A/行touch取得後も一覧維持、通常終了B、command listと背景遮断/退場を保持（IDA-gpt-6-T006、実機未確認）
- [チャット一覧の座標とstyle退場待ちの再修正](topics/chat_scroll_style_followup_design.md) — F004中心座標/vtable解釈の訂正、元viewport/hit-test、hairの親chat/keyboard全退場・待機中B/復帰（IDA-gpt-6-F005/T007、実機未確認）
- [hair等からHHD画面を直接呼ぶ訂正](topics/chat_style_direct_design.md) — fix2リスト実機PASS/hair未修復、外部chat退場待ちを撤回して4aliasは直接Show、time経路を分離（IDA-gpt-6-T008、新版実機未確認）
- [クローゼット解析とアイテム検索](topics/closet_search_design.md) — native10slot、動的page/1tab、指定slot/items、検索list/closet切替（IDA-gpt-6-F006/T009）
- [チャットの実退場とクローゼット起動修正](topics/closet_exit_fix_design.md) — nativeキャンセル/親・keyboard破棄/tab復帰、閉じた後native chat再起動（IDA-gpt-6-F007/T010、新版実機未確認）
- [クローゼット直通と反復取得・持ち物操作](topics/closet_direct_design.md) — map/tab再表示を省く、項目残留/pocket移動・消去、低ID保持、B/C親・影非表示（IDA-gpt-6-F008/T011、今回変更は実機未確認）
- [クローゼットの画像保持・帰還直通・即時ページ](topics/closet_followup_design.md) — 自前没iconの参照保持、closet→chat直通、pageアニメ省略（IDA-gpt-6-F009/T012、新版実機未確認）
- [リスト再タッチ・持ち物操作](topics/inventory_controls_design.md) — 現在selected行1tap/色保持、個別checkbox、nested hook/ゴミ箱の実機不具合修正、thumb半変位・closet加速（IDA-gpt-6-F010/T013・F011/T014、新版実機未確認）
- [持ち物の再入場と非ドラッグのゴミ箱・青選択](topics/inventory_ui_fix_design.md) — 実GUI入口、actor寿命と背景priority、trashdrag禁止/click・drop保持、旧行解除、manualcloset3cheat削除（IDA-gpt-6-F012/T015、実機未確認）
- [HHD のキャラクリ画面を ACNL の下画面で再現する設計](topics/hhd_charcreate_acnl_design.md) — 自前 DARC をゲームのレイアウト機構に Attach（IDA-opus-5.5-D005）
