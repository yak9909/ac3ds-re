# 現行TODO（V2、2026-09-12新設）

- [x] IDA-gpt-6-T017: T016実機trash未表示のhidden座標残留を原ARM再現/force matrix更新で訂正。追加2項目はCHEATS native分岐NOP/原BEQ復元へ置換、自作descriptor撤去。build・native57/75anchor21CPP4334parser/font欠字0/linked/scroll/最新DB公式XML122名73注記14構造体2Enum/hash PASS、最後一括保存結果はSESSION/publication参照。修正版実機未確認/main/実機/SD/正常旧15版/中断整理保持。

- [x] IDA-gpt-6-T016: 初/再入場trash・消去音・A後青訂正、6checkbox（食べる/じめんにおく）、chat2項目keyboard移設/旧path設定復元、font667codes欠字0。最新専用build/4334・71anchor21CPP/linked/halfscroll/native60case/公式XML121名67func注記13構造体+enum/global/T/hash PASS。最終source/normal旧14版保持gate・最後一括作業枝保存結果はSESSION/publication参照。新版実機未確認/main/SD/中断整理保持。

- [x] IDA-gpt-6-T015: 通常A→個別checklist表示、pocket再入場trash/背景より前、trashdrag禁止・click/drop/音保持、青selectedとDPad移動後旧行解除、manualcloset3cheat削除。runtime53/69anchor21CPP・4334parser/linked/scroll/最新DB公式XML116name59comment12type/T/hash、44source/normal旧13版保持PASS。最後一括作業枝保存結果はSESSION/publication参照。新3gx実機未確認/main/SD未操作、製品の次は利用者実機確認。

- [x] IDA-gpt-6-T014: T013実機報告のletterhide/trash・pocketclick/個別checkbox/selected行1tap・色保持を修正。native46case/旧UI・closet/半scroll/4334・68anchor・21CPP/最新linked/公式XML3名10注記3型PASS。最終hash/保持gate後に一括作業枝保存。新3gx b77445c0…は実機未確認、main/SD未操作。

- [x] IDA-gpt-6-T013: list/候補2tap・音anim、owned thumb0.5/track維持、closet200/1500/50ms、pocket trash/native全削除窓、Vapecord参考追加4操作を実装。39operation/half6/timing-memory7/旧list20・repeat12・style6・4334/68anchor19CPP/linked PASS。DB24name/35注記/10型保存、最新table-head XML読戻し・最終一括Git保存はSESSIONを参照。実機未確認/main未操作。利用者の実機検証が次の製品操作。
- [x] IDA-gpt-6-T012: 画像32pin/両dtor、帰還直通・退出高速化、page即切替/決定・repeat待機撤去、検索バッファ返却/ERROR2 stage1分類。新29＋timing/memory7/旧24・list20/repeat12/style6、4334parser/49anchor/17CPP/linked ABI/hash/しずえ、DB16名21注記/876B型3prototype/XMLとF008周辺全読戻しPASS。37source/正常旧10版保持/14owner対16。最後一括作業枝保存、gohan_closet_followup1/manifest、実機未確認/T002/main禁止。

- [x] IDA-gpt-6-T011: chat→closet直通・検索項目の無限取得、pocket移動/交換/stackとclosetへ消去、0xFF以下/非pocket品ID/flags保持、B/C親・影hide。新22case/native180/旧5再現・pager/ctor/search/list20/repeat12/scroll/style6、4334/44anchor/15CPP/linked ABI/hash/しずえ・DB7name/17注記/50旧名/型/XML PASS。正常・旧9版/34source hash/14owner対16保持。最終保存版/hashはgohan_closet_direct1/manifest・publication、実機未確認/T002/main禁止。設計closet_direct_design.md。

- [x] IDA-gpt-6-T010: T009のnative chat退場を解析して修正。凍結/detach撤去→native cancel/破棄/tab復帰・終了後native chat再起動。旧Tab13 timeout再現、新20case/native180/既存list20/repeat12/scroll/style6、4334parser/40anchor/15CPP・linked ABI/hash/しずえ、DB13name/enum/prototype/旧37name/公式XML/全bytes PASS。正常・全旧8配布版/34source hash/14owner対16保持。新成功表示は実機未確認/T002/main禁止。最後一括保存と版/hashはgohan_closet_exit_fix1/manifest・publicationを参照。設計closet_exit_fix_design.md。
- T009の元chat保持/復帰と初期field idle fixtureは実機不具合で否定、T010へ引継ぎ。native slot/provider/転送解析は保持し、成功表示を確認済みとしない。

- [x] IDA-gpt-6-T009: nativeクローゼット解析・指定slot/items/検索list/closet切替を実装/PC検証。名前hitのみ、ID1tab/動的page/前後/0x、begin→search、native取得/元chat復帰。4334parser/33anchor/15CPP・native180/Closet18case/既存一覧20/repeat12/scroll/style6・linked ABI/しずえ/hash/DB37name/5型公式XML PASS。Source codeaf118fa/解析checkpointc2f6ba13を最後一括保存/push・各独立remote一致。最終hash/版はgohan_closet_search1/manifest、実機確認はT002/main禁止。設計closet_search_design.md。

- [x] IDA-gpt-6-T008: hair/style/eye/eyesは直接HHD Show、TimeMenuだけCloseChat/AfterClose。4alias実chat bound即呼出し/再要求/失敗/time分離6caseと旧予約版再現、一覧20/連続12/native回帰/4330parser・14CPP/linked ABI/DB3注記訂正・公式XML PASS。source9d3e65e/root checkpointc4f74150を最後一括push/各独立remote一致。gohan_chat_style_direct1、SHA/詳細manifest。fix2リスト実機PASS、直接呼出し新版実機確認はT002/main未変更。設計chat_style_direct_design.md。

- [x] IDA-gpt-6-T007: ITEMNAME/listの画素座標/vtable訂正とhairのparent/kbd退場待ち・HHD待機B/timeout/復帰を実装、元幾何で旧版再現/新版全回帰・ABI/hash・F005DB公式XML読戻しPASS。source3b1e8e1/root artifact checkpoint1f7b2340を最後一括push/各独立remote一致。背景遮断/連続取得/B終了保持、fix2 artifact/SHAはmanifest。修正版実機確認はT002へ、成功GPU表示・hair実機原因全体未確定/main未変更。設計chat_scroll_style_followup_design.md。

- [x] IDA-gpt-6-T006: ITEMNAME検索は決定で閉じず連続取得、通常終了Bのみ。command list/背景遮断を保持。別build/linked ARM追加12case・旧20case/native scroll/arc/ID順/Map/hotkey/ABI/hash/32source SHA/正常・全旧artifact/最新DB公式XML不変 PASS。最後一括保存/最終hashはgohan_chat_search_repeat1/manifest、設計chat_search_repeat_design.md。実機未確認/main未変更。

- [x] IDA-gpt-6-T005: リストscroll不動をnative Controller touch入力の限定差込みで修正。style arc一時CTRPF pool/取消・失敗解放、fgobj含む検索全ID順/unique/ページを実装。旧版再現・元native scroll/前回20case/arc/検索/linked/ABI/しずえ/DB公式XML PASS。別artifact gohan_chat_scroll_fix1、実機未確認/main未変更。最終hash/commitはmanifest、設計chat_scroll_style_fix_design.md。Gitは最後一括。

- [x] IDA-gpt-6-T004: chat listはDPad focus/Aかtouch決定、背後入力遮断、検索ID左prefix、time menu終了後field復帰/OFF中も終了監視を実装。新gohan_chat_lists_fix1/元native20case/23anchor/13CPP/4330parser/linked/ABI/しずえ/hash/DB20concept・公式XML PASS。作業枝へ最後一括保存、実機未確認/T002で確認、main変更なし。設計chat_lists_fix_design.md/根拠gohan_chat_lists_fix。
- [x] IDA-gpt-6-T003: MapEditor入力停止/ChatCommands hotkeyを修正。旧実Start/HoldField停止再現、新実Tick移動/touch/blockとnative Wait hotkey/保持/release/rebind/OFF・linked/ABI/しずえPASS。3gx gohan_editor_chat_fix1、codeadf6669＋メモec1e8d1を最後一括作業枝push/remote一致、31source SHA/Git一致。今回root記録も最終batch保存。修正実機未確認/T002で確認、mainへ入れない。DB変更なし。
- [x] IDA-gpt-6-T001: gohanのFOXXY idle/気絶/Vapecord消失抑制・§14chat・メニュー再編を実装/PC検証し作業枝保存。最新両editorはaction/B/再実行/排他、公共事業設定全削除、time単独=分、cursor90/120/60、自前GUI自動openなし。最終font/build/native/ABI/parser4330/22anchor/13CPP/XML PASS、code8137d2e＋メモ9285ebaをwork/gohan-chat-and-portsへpush/独立remote一致。旧整理は中断、実機/main変更なし。
- [ ] IDA-gpt-6-T002: 今回配布版の実機確認後、利用者の結果とSHAを記録。特にB/再実行/両editor切替・catalogゴミ箱・チャット通常/IME/時間/検索・翌日の植物。未確認のためmainへ入れない。実機をこちらから操作しない。
- 最新指示（2026-10-11）: 利用者が整理・意味調査を一旦中断し、文書化して次回へ引継ぐよう指定。再開指示待ち。JOKER/他CTRPF新規収録と共有設定関数統合も中断・撤回維持。全2700関数/3417原候補/新規収録pending899を保持、Gitは全作業後一括のため未実行。
- [ ] TreeSitter-gpt-6-T003 **中断中**: 全2700チートのゲーム内の意味を全project_v2資料・近いチート・アドレス・CTRPF sourceから個別に推測し、関数内コメントと根拠/確度/未確認点を記録。台帳/公開1360、未レビュー1340、全件未完了。token不変/完全逆復元PASS、判明した概念はDBへ反映・保存。次回は島地形16/建物16の予備証拠から個別レビュー。入口docs/topics/cheat_semantics.mdとpaused_checkpoint.json。新規収録/共有統合/Git途中操作/実機は再開しない。
- [x] TreeSitter-gpt-6-T002: 収録済み2700関数の挙動保持リファクタリング。構造最適化/20cpp ARM/host466548/元資料・逆差分復元/現hash・旧stage hash/全partition・ヘッダ・関数外状態PASS、refactor_final_gate/status_refactor=VERIFIED_SOURCE_REFACTOR。ARM object40のtext15228B減/rodata319B増/入口stack最大72B減。追加した汎用コメント2970件は最新訂正で却下、意味コメント要件はT003で未完了。現build/実機適合は未確認。

- 最新作業範囲（利用者 2026-10-11）: CTRPF PROJECTS由来の集約は中断。利用者の明示再開まで継続しない。CHEATS由来だけを整理・検証する。既存全scope/未処理を削らず、commit/pushは最後一括のまま保留。CHEATS3097候補のうちmessage(5).cppの施設文章変更8callbackが未処理、AR3033/template6収録、metadata50（原候補単位）。
- [ ] TreeSitter-gpt-6-T001: 参照CHEATS/CTRPF PROJECTS全チートの大分類.hpp/.cpp集約（元IDA-gpt-6.1-sol-T005/F018）。CHEATSは55file/3097候補→2381関数/3047原候補＋metadata50、未処理0、source scope gate PASS。原CPP8は欠落CHARS_U8_MAP/itemsを局所補完しReview、原file対2仮定host320＋個別/結合ARM。AR runtime/実機/原型・build一致は未検証。全体2652関数/3369原候補/947pending、CTRPF部分は利用者指示で中断し明示再開まで作業しない。中断位置: Language/startup host246＋ARM、Lifecycle31失敗0採用、共用CurrAddress selector2は4consumer証拠で撤回。RuntimeContext/PlayerClass/共用設定消費側/旧SDKは未完了として保持。main/統合無し、関数内完結・重複/出典の条件を維持、Gitは最後一括のまま保留。

> 既存記録の解析ソフト: IDA / 解析モデル: unknown（利用者指定）。2026-09-19のID移行・文書編集: gpt-6-astra。本文の解析結果と確度は変更していない。新規記録は実際の担当モデルを記載する。規則: [record_ids](../docs/record_ids.md)、対応表: `record_ids.IDA.json`。

旧版は `reference/old_project/RE/TODO.md`。過去の項目を自動的に未完了として再開しない。

- [x] IDA-gpt-6.1-sol-T004: F016実機のチップ長押し窓未表示/縞アニメ振動を修正して作業枝保存・配布。原ARM旧版再現と新版7条件/全225関数ABI・分岐/しずえ/保存DB・XML PASS。gohan code a006467/メモa517f19をwork/chip-longpress-fixへpush、chip_longpress_fix1配布/hash/source remote読戻しPASS。新版実機未確認、実機操作/main変更なし。根拠F017/work/evidence/chip_longpress_fix。

- [x] IDA-gpt-6.1-sol-T003: Editor全UIフェード修正・list中カメラ/3倍速度・chip長押し複製・内装8枠保存/読み込み/枠との交換を実装/検証/作業枝保存して配布。build3/linked11条件・全必要PC検査PASS、gohan work/interior-presets code9d606dd push、interior_presets1保存/hash/remote読戻しPASS。根拠F016/work/evidence/interior_presets、実機操作なし・新変更は未確認/main未反映。

- [x] IDA-unknown-T001: 自立化の検証を完了し、Git/LFS・参照先・symlinkの整合を記録する（現在の依頼）。
- [x] IDA-unknown-T002: 利用者が漢字変換・リストボックス・ACNL内蔵フォント描画を実機確認し、現行統合ソースmain pushを明示承認（2026-09-13）。今回こちらで実機操作はしていない。
- [x] IDA-unknown-T003: 更新版CRO/CRSをartifactsへ独立照合して配置。現行gohan/specを独立Gitへ分離しmainへpush、解析Gitから除外。根拠work/evidence/gohan_split/。
- [x] IDA-unknown-T004: 未確認変更は必ず作業branchへpushする規則を記載。現行統合版は利用者確認に従いmainへ反映。重複ソースバックアップを整理し固定Git baselineと復元成果物へ集約。

- [x] IDA-unknown-T005: src を `gohan` / `gohan-gui-simulator` / `SwkbdEngineProbe` に整理。旧 2 フォルダを削除し、simulator を GitHub の最新へ同期。romfs・SOUND を gitignore（2026-09-13）。
- [x] IDA-unknown-T006: node の多行 `-e` が Volta shim で切れる問題を stdin 方式で恒久対策（IDA-unknown-F005）。検証は PowerShell から行う（2026-09-13）。
- [x] IDA-unknown-T007: `gohan-gui-simulator` の食い違いを解消（IDA-unknown-F004）。利用者の判断で**ローカル版を優先**し、
      `82adf284` の 29 ファイルを simulator の main へ戻して push（`4083d70`、履歴は保持）。
      `verify_plugin_port_v2` の群5 を含め `verify.py` は Prebuild PASS（2026-09-13）。
- [ ] IDA-unknown-T008: 公開版 simulator にあった新しい preview（`c0251cd` 以前）の機能を、**利用者が**あらためて実装し直す。
      前提: 差分は `git -C src/gohan-gui-simulator diff 4083d70 c0251cd` と `web/*-v10-part-*.js` の復号で取れる。
      確認方法: 実装後に `python tools/chat_kanji/verify.py` が PASS のままであること。

- [x] IDA-unknown-T009: `gohan.txt` を `gohan.md` へ移行（49 項目・Desc 35 件を逐語照合）。項目の挙動仕様
      `gohan-menu.md` を新設し、**メニュー項目の ON/OFF と関数内の ON/OFF を分離**して定義（2026-09-13）。
      gohan `work/spec-md` = `b7b6ff8` へ push。main は無変更。
- [ ] IDA-unknown-T010: `gohan-menu.md` §9 の残件を決める。
      Simulator で詰める 2 件（「実行した」表示／連動型の読み取り失敗時の見せ方）、
      設計 3 件（**CLAUDE案 `ItemSpec` の採否**／既定ホットキーの割り当て／効果の既定値と元命令の保存先）、
      機能 2 件（PlayerStyles の選択 UI／`セーブ実行` の扱い）。
      確認方法: 決めた内容を `gohan-menu.md` の【確定】へ移す。

新規項目には目的・前提・次の確認方法・根拠パスを付ける。作業を中断する場合はSTATE/SESSIONも更新する。

- [x] IDA-gpt-6.1-sol-T001: HHD/ACNL室内カメラを調査→設計→実装。493 frame＋20条件、build/linked/ABI/しずえ/字形、両DB/XML保存、作業枝push。F014、work/evidence/hhd_room_camera/。2026-10-10利用者がF013同梱hhd_room_camera1を実機PASSと報告（端末SHA/個別ケース再測定なし）。main未反映。
- [x] IDA-gpt-6.1-sol-T002: リスト背後UIのフェード、Xで最後のリスト、B保持、カテゴリ音、模様替えUI中だけyawに沿うスライドパッドX/Z移動。設計→実装→build/linked、DB保存と最新XML検証完了。gohan work/catalog-camera-controls / 9792469、配布catalog_camera_controls1。F015、新追加は実機未確認なのでmainへ反映しない。

- [x] IDA-unknown-T011: IDA/Ghidraのcommit/push前XML規則と手順を記載、Ghidra公式IDA9用Exporterを導入。IDA9.3主IDBの全XML・bytes・元DB不変を検証。Ghidra側の互換試験の詳細はwork/sessions/xml_exchange_20260913.md。

- [x] IDA-unknown-T012: ゲーム内モデルの共通生成・姿勢・破棄、木の資源lookupと画面固定候補を静的調査。元bytes/独立ARM/RTTI照合PASS、旧レイヤー名とscene 2の誤解を訂正。docs/topics/models3d.md、IDA-unknown-F007/F008。
- [ ] IDA-unknown-T013: 木1種類の独立instanceでワールド配置を検証。**2026-09-20追記 / IDA-gpt-6-astra-F001: 独立生成・曲面変換・scene0表示・OFF消去は実機成功。** 別位置/倍率0.5・1.0も成功。残りは任意回転、専用heap容量/OOM、GPU参照終了後かつ資源解放前の破棄、場面遷移と常用3gx。旧F009–F011の静的結果と新tree_live_plan.mdを併用。IDの出自はunknownのまま保持。
- [ ] IDA-unknown-T014: 独立カメラによる画面固定3D表示。**2026-09-20 / IDA-gpt-6-astra-F003: 専用view/projectionの直接描画、20秒移動中の固定、pixel(320,180)/倍率0.6、alpha併用/OFF復元に成功。** 残りは左右目個別画像、自己遮蔽depth、照明、下画面/UI順序、場面遷移・寿命管理と常用3gx。テクスチャ合成は未実装の候補。根拠docs/topics/alpha_screen_plan.md、reboot1/。scene 2流用禁止。

- [x] IDA-opus-5-T001: 任意モデルの読み込み→描画を実機で1体成立させる。**2026-09-20 成立（IDA-opus-5-F004）。**
      `Other/book.bcres` が上画面に出た。runs 49 / submits 49。**ただし OFF の画像は未取得**（T004 へ）。
      旧記述: 設計は arbitrary_model_draw_plan.md §4（IDA-opus-5-D001、実機未適用）。
      一発目は `Other/book.bcres`（Model・1メッシュ・レイヤー0・完全不透明・instance 1,396 B）、生成引数は木と同じ `(0, 0, 1)`、
      配置は必ず `FieldPosition_ToRenderSpace 0x0052CDD8` を通し、書込み前に float32 で到達座標を確かめる。
      **同じ座標へ `fg_treeA_4` を置く対照を最初から用意する**（出ないときに資源側か座標側かを即断するため）。
      確認方法: 上画面に不透明な物体が1個現れ、OFFで消えること。Chokistream＋時間制限Resume。
- [x] IDA-opus-5-T004: `enable=0` で消えることの画像証拠を取る。**2026-09-21 取得（run2 と run3 の両方）。**
      旧記述: 
      2026-09-20 は利用者が Chokistream 起動のため ACNL を再起動し、ON の画像しか残っていない。
      確認方法: 同一 boot・同一カメラで ON と OFF を連続で撮り、物体の有無だけが違うこと。
- [ ] IDA-opus-5-T006: `continue_process()` の直接呼び出しを塞ぐ。`tools/dynamic/run_timed.py` 経由を必須にし、
      park 用 BP の番地を `0x1B7220` へ寄せる（IDA-opus-5-F007）。tree_live の `PARK` を触る前に他エージェントの
      `tree_pose`/`tree_screen` への影響を確認すること。
- [ ] IDA-opus-5-T007: ヒープ量を `model_preflight` の値とファイル長から決める補助を `arbitrary_model.py` に入れる。
      `0x40000`/`0x20000` の既定は 35 倍過大で、2 体目で親ヒープを使い切った（IDA-opus-5-F006）。
- [x] IDA-opus-5-T008: アニメのフレームを進めて見た目を変える。**達成（IDA-opus-5-F012 + F013）。**
      適用段は `sub_48A844(binding, phase) 0x0048A844`。画面でカーソルの色が変わった（縞 42〜69%、対照 0%）。
      旧記述: **前半のみ達成（IDA-opus-5-F012）。**
      フレームは実機で毎フレーム進み、150でループも折り返す。**画面は変わらない**（画素で確認、
      カーソルの変化は静止物より小さい）。**残り: 評価結果をマテリアルへ書く「適用」段の特定。**
      手掛かりは `0x004CF460`〜`0x004D1054`（`node+0x228` を読み書きする一群）。
      `AnimBinding` の vtable は破棄2スロットのみ、`g3d::MaterialAnim` の残りスロットも破棄系だった。
      旧記述: `sub_4EDC74 0x004EDC74` は
      `vmov.f32 s16, s0` で **VFP s0 引数**を取るので、いまの呼び出しハーネスでは呼べない。
      案A: call guard に VFP 引数を足す。案B: `AnimFrameController`（anim本体+?）の欄を直接書く。
      確認方法: 同一 boot・同一カメラで2フレーム分を撮り、模様が変わること。結線済みの証拠は F011。
- [x] IDA-opus-5-T011: `ModelInstance_Create` の a5/a6/a7 を分離する。**完了（IDA-opus-5-F015）。**
      a5=bufferOption、**a6=isAnimationEnabled が機構を作る**、a7=maxAnimObjectsPerGroup。旧記述: ヘッダでは
      a5=`Model::Description::bufferOption`、a6=`SceneNode::Description::isAnimationEnabled`、
      a7=`maxAnimObjectsPerGroup`。**IDA-opus-5-F009 の A/B は3つ同時に変えていて分離できていない。**
      検証法: 同じ `UnitCursor` 資源を `(0, 1, 3)` で作り、`node+0x28`（AnimBinding）と
      `node+0x148`（m_MaterialAnimGroup）が埋まるかを見る。埋まれば a6 が enabler、
      埋まらなければ a5 が効いている。親ヒープの残量を先に測ること。
- [x] IDA-opus-5-T012: ACNL 専用資料 CGFXModel を読む。**完了。アニメは明示的に非対応で使えず、**
      **代わりに自前資源を直接解いて22メンバと駆動メンバを確定（IDA-opus-5-F016）。** 旧記述: https://github.com/captainsouthbird/CGFXModel を読む
      （villager 編集）。**別タイトルのヘッダより本作に近い**ので優先度が高い。
      マテリアルアニメのメンバ22個が何の欄かを詰める手掛かりになりうる（F013 で未特定のまま）。
- [x] IDA-opus-5-T010: 12体の同時描画を実機で確かめる。**2026-09-21 成立（IDA-opus-5-F017）。**
      12体で **46 run/1500ms（30.67fps＝実機上限）・submit12・advance12・apply24/フレーム**。
      4体との差は測れず、Unicorn の `twelve_with_anim` の予測と一致した。
      submit 先の配列は満杯かつ成長不可なら書かずに拒否するので溢れない（実機は容量1024・使用34/11/15）。
      **ただし画像証拠は未取得**（下の T014 を参照）。
- [ ] IDA-opus-5-T015: `tools/dynamic/inspect_ida_dialog.ps1` は捕まえたダイアログを
      **`work/evidence/models3d/alpha_screen_20260920/ida_warning.png` に固定で上書きする**。
      これは IDA-gpt-6-astra の証拠ファイルで、無関係な実行が他人の記録を壊す。
      2026-09-21 に一度上書きしてしまい `git checkout` で戻した。出力先を引数にするか、
      実行ごとの一時ディレクトリへ書くように直す。
- [x] IDA-opus-5-T014: 画像証拠。**2026-09-21 解決。** Chokistream の映像は復旧し、
      `capture_chokistream.ps1` が新しいフレームを返すようになった。そして撮ってみたところ
      **12体は本当に見えていなかった**（利用者の指摘）。原因は IDA-opus-5-F020（骨格の更新漏れ）で、
      直したら全部出た。**止まっている間の3枚（`many04_top.png` / `many12_on_top.png` /
      `many12_off_top.png`）は引き続き証拠に使わない。** 以下は当時の記録:
- [ ] IDA-opus-5-T014-old: **（解決済み・記録）Chokistream の映像が止まって画像証拠が取れない。**
      `capture_chokistream.ps1` の PNG が Resume 2回を挟んでも sha256 `25fcb833…5390e` で同一。
      `docs/dynamic_observation.md` が「映像用 JFrame への PrintWindow 経路は Image Sequence と未照合」と
      警告していた件に当たる。利用者に (a) Chokistream の再接続、または (b) `Output Format = Image Sequence`
      への切り替えを頼む。切替後は `tools/dynamic/latest_chokistream_frame.py --max-age-sec` で鮮度を検査する。
      **それまで既存の3枚（`many04_top.png` / `many12_on_top.png` / `many12_off_top.png`）を証拠に使わない。**
- [ ] IDA-opus-5-T013b: `SceneTraverser` の配列#14（`ctx+232`）の用途。積まれる条件が
      `node+0x28`（`m_AnimBinding`）非0 なので、アニメを結んだ自前 instance も submit だけで載る。
      誰が読むかは未追跡。読み手がアニメを再適用するなら、ケーブの apply と二重になる可能性がある。
- [x] IDA-opus-5-T009: 骨アニメを結線する。**2026-09-21 完了（IDA-opus-5-F018 + F019）。骨が動き、12体のカーソルと同時に描画まで通した（13体・30.67fps）。**
      `node+0x228` が非0になる条件は確定した: **モデル資源が `CMDL+0x2C` の群 DICT で
      `"SkeletalAnimation"` を宣言していること**。`UnitCursor` は宣言していないので 0 のままだった
      （「骨アニメが無いから」ではない。骨は1本持っている）。
      **資源の組も決まった**: `MiniGame0/character/esc_spider.bcres`（155,776 B、モデル `esc_spider_bq`
      `type 0x40000092`・骨21本・群3つ全部を宣言、同ファイルの `esc_spider_wait1_bq` は
      `SkeletalAnimation` 群・21/21骨・30フレーム）。`tools/models3d/survey_skeletal.py` が
      8,818ファイルから選んだ。次点は `esc_scorpion.bcres`（324,352 B、骨54本）。
      残りの手順: 資源ヒープ 0x40000 では足りるが**instance ヒープは別に取る**（IDA-unknown-V2-F025）。
      `0x4EC1E4(anim)` → `0x4EBFFC(anim, holder, canm, allocator, 0)` → `0x4ECD1C(holder, anim)`。
      **`0x4ECD1C` は node が SkeletalModel でないと null 参照で落ちる**ので、呼ぶ前に
      `node` の vtable と `node+0x228` を必ず確かめる。ケーブの表はそのまま使える（entry の `anim` 欄）。
- [x] IDA-opus-5-T005: 自前で確保した資源・instance・ヒープの解放。**2026-09-21 成立（IDA-opus-5-F022）。**
      カブトムシ1体を6段で完全に解放し、**親ヒープ2本とも作る前の値へバイト単位で戻った**。ゲームは無傷。
      **続けて全オブジェクトへ広げ、親ヒープへ 467,056 B が戻った（IDA-opus-5-F023）。画面は素の村に戻った。**
      `g3d::MaterialAnim` の後始末も **vtable スロット5 `0x4EBDF8`**（骨アニメと同形）。
      孤児 ExpHeap は**親ヒープごと回収された**ので名指しで破棄してはいけない。
- [x] IDA-opus-5-T016: `0x4F0184` が資源側へ書く条件。**ほぼ解明（IDA-opus-5-F023）。**
      `+0x170`/`+0x174` は instance 自身の mesh 配列の begin/end で、等しい＝**空**。
      空なら `resModel+0xB8`/`+0xB4` へ落ちるが、**mesh 数 0 のモデルでは個数も 0 なので何も書かれない**
      （9,081 モデル中 71 個が mesh 数 0。`esc_loc_*` などの位置決めダミー）。
      残る危険は「mesh を持つのに instance の配列が空」だけで、観測6体では一度も起きなかった。
      **それを作る条件は未解明**なので、破棄前の `+0x170 != +0x174` 検査は残す。
- [ ] IDA-opus-5-T020: 親ヒープ `0x301668EC` の空きが F023 時点より **96 B 少ない**（503,224 → 503,128）。
      `getMaxAllocatableSize` が 371,852 なので**空きは2ブロック以上**に分かれている。
      `sead::ExpHeap` は空きブロックのヘッダを空き容量に数えないので断片化で説明は付くが、
      **自由リストを歩いて確かめていない**。`probe_lyt_heap.py`（旧F-309）と同じ手で歩けば決着する。
- [x] IDA-opus-5-T021: gohan の「テスト」フォルダのグリッドカーソルを実機で確かめる。
      **2026-09-22 利用者確認済み**。実寸は **1 マス = world 32**、モデル素寸も 32 x 32、
      原点は quad の中心（IDA-opus-5-F033。実機と `UnitCursor.bcres` のボックスが独立に一致）。
      45 度傾けも意図どおり動作（IDA-opus-5-F034）。

- [x] IDA-opus-5.5-T004: **公共事業の消す・動かす・当たり判定の作り直しを実機で確かめる**（IDA-opus-5.5-F002）。
      **2026-09-23 利用者確認: 3 項目とも期待どおり**。当たり判定は操作直後に更新、読み直しは描画のためだけ。
      gohan `work/grid-cursor` の「テスト」フォルダ。手順: 「近くの公共事業を選ぶ」→「選んだ公共事業を消す」→
      消えた場所を歩いて通れるか。動かす場合は古い場所を通れ、新しい場所でぶつかるか。
      ★区画の属性を素に戻すので、**道（マイデザインの地面）や橋などの別の変更が消えないか**も見る。

- [x] IDA-opus-5.5-T006: **F009 の版を実機で確かめる**。**2026-09-23 利用者確認済み（意図どおり）**。(1) 店などを置き続けると「メモリの空きがありません」で断られ、落ちない
      (2) 地図の A 枠を超えて置くと、その場で星アイコンが出る（画面遷移後と同じ） (3) 地図がゲームでも落ちる数になる設置は
      「地図のアイコンが…上限」で断られる (4) 公共事業などの種類 30 超えは「種類が多すぎます」 (5) 画面遷移しても落ちない
- [x] IDA-opus-5.5-T008: **モデル単位の色ハイライトを実機で試す**（F010 §5）。**2026-09-23 成功（材質 0 が薄い青、強さ可変、元に戻る）**。
- [ ] IDA-opus-5.5-T009: **ハイライトの常用化**（F011）。灯り（実質そのままの Interpolate）と家（Simple → 汎用、Tent・Post まで辿る）は実機で成功済み。
      **F012 で解決**: 対応表は不要（スロット→実体→子プロセス→ヒープ見出しの範囲→モデル参照＋hobj::）、写しは gohan の静的配列でよい。
      残り: 他の建物（役場・店・住民の家など）でも規則で全部品が集まるかの確認、段 5 が本当に使われている材質、影などの別パス、
      モデルビューアの自前モデル、gohan への実装。
      先に PICA の TEV の入力元・オペランド・合成式の値を citro3d/libctru の定義と照合し、書く 28 B を検算する。
- [ ] IDA-opus-5.5-T007: **素のゲームの公共事業の上限（しずえの提案の判定）を特定する**。件数欄 garden+0x4BE84 は全建物の数で、
      直接読むのは 0x29EB08 と 0x758648（VillageBook+16）だけ。本体・CRO とも `cmp #0x1E` の近くに件数・スロット走査は無かった。
- [x] IDA-opus-5.5-T005: **地図アイコンと足元アイテムの即時更新、プレイヤーを動かさない**（F005）。**2026-09-23 利用者実機確認済み**（枠あふれは T006）。
      確かめること: (1) 置く・動かす・消すで下画面の地図のアイコンが増える／動く／消える（通知「地図も更新」）
      (2) 地図のアイコンをタッチしても落ちない・二重にならない (3) 足元に重なったアイテムの高さがその場で変わる
      (4) プレイヤーの位置が変わらない (5) 画面遷移のあとも正常。
- [x] IDA-opus-5.5-T001: **建物の見た目を設置直後に出す**（再ロードなし）。**2026-09-23 利用者実機確認済み（F004 HIGH）**。
      村の建物は BsStrcMgr の作成段 2 `0x6DE198` が 1 件ずつ作る。その 1 件分（位置 → 高さ → 生成 → 一覧）を
      gohan `SpawnVisual` に写し、消すは一覧から抜いて `0x5200B8`。特別 id などは部屋の読み直しへ退避。
      実機で確かめること: (1) 公共事業を置くと**その場で**出て通知が「その場で反映」 (2) 消す・動かすで古い見た目が
      消える (3) 橋の高さが合う (4) 落ちない（生成を `Frame_DrawPass1024` 内のフックから呼ぶのは初めて）
      (5) その後に建物へ入る・部屋を出入りしても二重に出ない。
- [ ] IDA-opus-5.5-T002: **公共事業プレビューを gohan へ**。部品は揃っている:
      名前は `Building_GetName`（表 `0x955700`）、モデルはモデルビューアの手順、
      半透明は IDA-gpt-6-astra-F002 の材質複製＋ Activate 差し替え、
      ★**テクスチャは別ファイル** `Strc/fobj/<名>/Textures/season00.bcres` を読んで Setup で結ぶ（IDA-opus-5.5-F003）。
      高さは実物と同じ `Field_GetGroundHeightAtWorld 0x6C69C0` の値、橋（分類 15）は +32（IDA-opus-5.5-F004）。
      足元は `Building_GetFootprint 0x1B1720` の戻り（もしくは romfs の `Strc/data`）の byte 8 非 0 のマスを
      グリッドカーソルで敷く。**足元のマス座標→world 座標の対応**（行→どの軸か）は
      実機で 1 回確かめる。
- [~] IDA-opus-5.5-T003: 足元の属性コード（byte 8、43 種類）のうち**どれが通行不可か**。
      **F017**: 分類表 byte_957B34（FieldAttr_CollisionClass 0x5CD3C0）の 0 以外を通行不可と解釈（MEDIUM）。実機の歩行で確かめる。
      **F019**: 利用者の定義に変更（物を置けない byte_957D32&2 == 0、または花を植えられない byte_957A35 == 0。無ければ一回り削る）。
      **F020**: 正解（利用者）と一致するのは byte_957A35 == 0（花を植えられない）だけ。これを採用。
      ゲームの属性表（プレイヤーの移動判定が引く表）を特定して決める。それまでは「書き込まれるマス」で囲む。

- [~] IDA-opus-5-T025: **IDA-opus-5.5-F022**: ゲームは ARCHIVE_ROMFS + {5,0,0} で更新 RomFS を開く。gohan を合わせた（実機未確認）。
      旧記述:  **更新タイトルの RomFS が開けない理由をまず「見える」ようにする**（IDA-opus-5-F038）。
      実機で `本体8629+更新0`。SD/カード/NAND の 3 通りとも失敗している。
      ★**直す前に、まず Result を出すこと。** `RomfsIndex::UpdateOpenResult()` に値はあるのに
      どの項目も表示していないので、今は推測しかできない（F031 と同じ罠）。
      「一覧を作る」の通知に `更新 0x........` を足すのが一番安い。
      そのあと: module/summary で分ける。権限なら `artifacts/update/exheader.bin` の
      ARM11 FS アクセス情報を読めば静的に裏が取れる。
      影響は限定的: 見えないのは amiibo+ 追加の 741 本だけで、base の 8,629 本は使える。

- [ ] IDA-opus-5-T024: **ゲームは update 側の .bcres をどう読んでいるのか**。
      `ARCHIVE_ROMFS` は base だけを返すのに（IDA-opus-5-F037、実機 8,629 件）、
      ゲームは update にしか無い 1,801 本（amiibo+ の住民・アイテム）を確実に読んでいる。
      目的: パス解決の実態を知る。モデルビューアがパスを渡したときに
      どちらの版が読まれるのかがこれで決まる。
      確かめ方: `ResHolderRequestLoad 0x00317920` から下のファイル層を辿る。
      ゲームが自分で 2 つのアーカイブを持っているのか、FS の別の仕組みなのか。

- [ ] IDA-opus-5-T023: **描画更新中にマス数を頻繁に変えると、まだ instance やヒープが作れなくなる**。
      利用者報告（2026-09-22）。**クラッシュはしない**（F034 の事前検査が止めている）が、
      `Fail::kInstanceHeap` / `kCreateFailed` / `kHeapExhausted` で止まる。**利用者の判断で今回は直さない。**

      見立て（未検証の仮説。これを前提にしないこと）:
      1. **解放が非同期に見える**。`HeapAllocator_DestroyHeap 0x002F73F4` で親ヒープへ戻した直後に
         同じ大きさを再確保しているので、断片化が残ると入らなくなる。
         T020（親ヒープが 96 B 少ない）と同じ系統の問題の可能性。
      2. **4 フレームの静止待ちが足りない**。GPU がまだ古いコマンド列を読んでいる間に
         ヒープを戻している可能性。F025 は「描かれている instance を解放しても平気」を示したが、
         **ヒープごと戻してすぐに取り直す**場合は見ていない。
      3. **要求が取りこぼされる**。`s_request` は 1 語で、メニュースレッドと描画スレッドが共有する。
         連続して変えると Teardown 要求が Setup で上書きされ、ヒープと体数が食い違う経路が残っている可能性。

      確かめ方: 「状態を見る」で止まった理由を拾い、`s_resourceFree` / `s_instanceFree` と
      親ヒープの `getFreeSize` / `getMaxAllocatableSize` を並べる。断片化なら後者だけが落ちる。
      根拠: 利用者報告、`src/gohan/Sources/Cheats/GridCursor.cpp` の `RequestRebuild` / `TeardownAll`。
- [ ] IDA-opus-5-T022: `MemorySize: 2MiB` が本当に起動失敗の原因かは**未実験**（IDA-opus-5-F030）。
      独立プラグインを作る機会があれば 5 MiB で同じものを作って確かめる。gohan には影響しない。
- [ ] IDA-opus-5-T016b: 局所配列65要素の上限検査が無い件（mesh が多いモデル。最大は 58）。
- [x] IDA-opus-5-T017a: submit をやめずに **instance を**解放。**2026-09-21 実施（IDA-opus-5-F025）。何も起きない。**
      ケーブが `holder+4 == 0` で次フレームから飛ばし、instance の記憶は GPU から見えないため。
      `submits`/`applies` が解放の瞬間で凍結し `runs` だけ増え続けた。
- [x] IDA-opus-5-T017b: submit をやめずに資源を潰す。**2026-09-21 実施（IDA-opus-5-F026）。落ちない。**
      解放だけでは何も起きず（中身が残る）、**49,152 B を `0xDEADBEEF` で潰しても
      カブトムシが消えるだけ**。`0xDEADBEEF` は float32 で -6.26e18 なので頂点が視錐台の外へ出る。
      元のバイトを書き戻すとそのまま復帰した。**失敗の形は「落ちる」ではなく「黙って消える」。**
      一般化はしない（パターン1種類、`bufferOption 0x834` のみ）。
- [x] IDA-opus-5-T018: 場面転換での挙動。**2026-09-21 成立（IDA-opus-5-F024）。利用者に建物へ入ってもらった。**
      **自前 instance は一切触られない**（node 576 B がバイト単位で同一）。ヒープも資源も生存。
      **ケーブは所有者検査で自分から描画を止める**（manager が 0 → 別番地で再生成されるため）。
      描画を再開するには検査の値を焼き直す必要がある。**自前で資源を読み込んでいることが
      場面転換に対する守りになっている**（ゲームの Season 資源を借りていたら破棄で消える）。
- [x] IDA-opus-5-T019: `0x4B8CF0` の scratch を返す経路。**解決（IDA-opus-5-F023）。**
      `*(0x0096F150)` のアロケータから出ており、対の解放は `ssys::ma::Allocator::Free 0x00569B44`
      （旧 F-296 が実機確認済み、今回も形を照合して3本とも返した）。
      **★ケーブの制御ブロックが scratch A にあるので、先に `0x1B721C` のフック語を戻すこと。**
- [ ] IDA-opus-5-T005-old:
- [ ] IDA-opus-5-T005-old:
      **設計は [instance_teardown_plan](../docs/topics/instance_teardown_plan.md) に書いた（2026-09-21）。
      T0/T1 は実施済み、T3 以降は未実行で利用者の判断待ち。**
      わかったこと: (1) **instance・アニメは CPU しか読まないが、資源の頂点/テクスチャは GPU が
      番地で直接読む**ので、両者は危険度が別物。(2) ケーブから外せば次フレームには
      どの配列にも入らない（`Render_FrameEnd 0x4F1CE4` が毎フレーム全部捨てる）。
      実測で46フレーム走らせても node と骨配列が1バイトも変化しなかった。
      (3) GX キューは `mgr=*(0xAD9960)` の `mgr[8]`=提出数 / `mgr[9]`=発行済み /
      `byte_AD98D8`=完了待ち で測れる。ただし**必要条件であって十分条件ではない**。
      (4) park はフレームの途中なので、ゲーム自身が破棄する位置（Calc 相）とは違う。
      未調査: アニメの破棄関数、`G3dResHolder` の unload、`sead::ExpHeap` の破棄、
      **資源の GPU 参照終了の示し方**、場面転換（利用者の操作が要る）、OOM。
- [x] IDA-opus-5-T002: SkeletalModel 側を同じ手順で試す。**2026-09-21 成立（IDA-opus-5-F005）。**
      `UnitCursor` が出て、`node+0x228`/`+0x22C` も `a7` も原因でないことが確定した。旧記述: 
      `ModelInstance_Create` の第7引数は木と同じ `1` に戻して測り直し、IDA-unknown-F029 の `node+0x228`/`+0x22C` を再評価する。
- [ ] IDA-opus-5-T003: instance holder を `0x004ED008` で構築するよう `tools/hw/unitcursor_probe.py` を直す。
      不可視の原因ではないが（`holder+4` しか参照されない）、vtable が0のままの破棄は危険。
- [x] IDA-gpt-6-astra-T001: 木の専用材質で透明度255/128/0と復元を実機検証。F002、alpha_screen_plan.md。任意材質のalpha乗算・透明面ソートへの一般化は未完了。

## HHD のキャラクリ画面を ACNL で再現（設計 IDA-opus-5.5-D005、docs/topics/hhd_charcreate_acnl_design.md）

- [x] IDA-opus-5.5-T010: 道具の選定と往復の確認。BCLYT = Clypo のライブラリ（CLI の import は不可）、BCLIM・DARC = 自作して ACNL の実物で照合（work/evidence/hhd/tools_t010.md）。
- [x] IDA-opus-5.5-T015: BCLYT の組み立てプログラム（C#、Clypo のライブラリ）。**完了**: tools/hhd/LayoutBuilder・make_acnl_layouts.py・build_hhd_arc.py。ACNL 124 本の往復で 97 本一致。設計 §3.2。
- [x] IDA-opus-5.5-T011: acnl-ui-designer に HHD 素材を取り込み、下画面 4 レイアウト（bg / face / eye / hair）の場面を作ってスクショと画素比較。**完了**（tools/hhd/make_designer_scenes.py、設計 §3.2）。状態の見た目（選択枠・ng・縞）とボタンの絵記号は T013 へ。designer の Window を 1 枠対応（F072）。
- [x] IDA-opus-5.5-T012: 最小の実機確認 — 地だけの DARC をメモリから Attach して下画面に出す（Attach・VRAM 転送・LayoutMgr）。gohan 作業ブランチ。**完了（F073、実機 PASS）**。ゲームの下画面 UI が手前に出るので、隠し方・優先度は T013 で調べる。
- [x] IDA-opus-5.5-T013: 全ペイン → 色 → ボタンの状態と入力 → 髪のページ送り（段階 1 の完成）。**実機 PASS（F074〜F076）**。残り（後回し）は T016。
- [x] IDA-opus-5.5-T016: 段階 1 の残り — 髪の自由スクロール（漢字変換の候補欄と同じ算法）・L/R と端で隣のページへ滑る・押したときのアニメ・選択枠とボタンの縞と loop。**実機 全 PASS（2026-10-05、gohan 6ad1443）**。命令の実測: 地 784/8192・顔 15,104/65,536・目 35,904/65,536（前の器 32,768 を超えていた）・髪 69,xxx/131,072。
- [x] IDA-opus-5.5-T014: 段階 2（上画面の背景とフェード）、段階 3（プレイヤーへの反映と HHD ⇔ ACNL の番号の対応）。**完了（F077〜F081、実機 PASS。オフラインのみ）**。
- [x] IDA-opus-5.5-T017: オンラインでの反映（髪型・髪色・目の色・帽子とアクセサリー保持）。2026-10-06 hhd_t017c 実機 全 PASS（F087 / F088）。目の形は T020 で調査。★0x0C は使わない（利用者）。
- [x] IDA-opus-5.5-T020: 目の形を通信相手へ（種別 11 を相手ごとに送る。見る側の建物の出入りで反映）。2026-10-06 hhd_t020c 実機で両方向確認（F089〜F092）。
- [x] IDA-opus-5.5-T021: gohan の他機能の 0xAA7994 → 自分の枠（FieldCamera・GridCursor・ModelViewer）。gohan main 8ea5325（F093）。マージ後の実機確認は未。
- [ ] IDA-opus-5.5-T019: **モデルの回転（利用者 2026-10-05）**: HHD の「十字キーでまわす」は ACNL では**スライドパッド**に変える。回転は自由（角度の上限なし、押している間は傾きに比例した速さで回り続ける）。
  T018 第 1 段で実装・実機 PASS 済み。2026-10-06: 「まわす」の記号をスライドパッド U+E049 に（F086、hhd_t018e_test で実機確認待ち）。確認後に完了にする。
  スライドパッドは入力遮断で塞いでいるので、ゲームへ渡さずこちらだけが読む（GuiMenu::BlockGameAll はスライドパッドも塞ぐ）。
- [ ] IDA-opus-5.5-T018（第 1 段 実機 全 PASS（hhd_t018d まで: 複製・位置・目の色と形の即切り替え・音・Y）。第 2 段 2026-10-06 実装・未実機 hhd_t018e_test: ボタンの押下中の色・音の差し替え・けっていで本人の目の形・上画面の記号と 2 行。F086）: 上画面の吹き出しに複製したモデルを置く（gohan の PlayerClone の画面固定。利用者の将来の希望 2026-10-05）。顔と髪の切り替え時のアニメ（HHD の EyeBase/HairBase の in/out）。
- [ ] IDA-opus-5.5-T022: HHD の家具リスト・壁紙/床紙リスト・ゴミ箱を ACNL の模様替え UI へ移植（利用者 2026-10-06）。
  最新（2026-10-09、IDA-gpt-6.1-sol-F013）: decor_catalog12は全実機PASS、decor_catalog13で壁かけリスト追加。外観誤判定を室内機能判定へ変更したdecor_catalog14（work/decor-room-capabilities / be72724）はPC・ビルド・リンク検査PASS、実機未確認。次は改造外観の普通の部屋で壁かけ家具1個/壁紙床各1回、通常室内と配置不可壁の回帰確認。SD資源はdecor_catalog13から変更不要。根拠work/evidence/t022_room_capabilities/report.md。
  範囲（利用者の補足）: 「模様替え UI を開いている時」に (1) 家具リストを開くタブと家具リストのメニュー (2) 壁紙／床紙リストを開くタブとリストのメニュー (3) ゴミ箱（家具を掴んで左下のゴミ箱に重ねて離すと消える）。挙動・押している間のテクスチャ変更なども忠実に。
  家具: HHD と ACNL の両方にあるものだけ（一致したものだけ HHD のプレビュー画像を持ってくる。利用者提案）。出した家具はプレイヤーに近い部屋の空いた所へ（ACNL の「かざる」を流用し、HHD の置ける場所の計算を自前で再現）。
  参考スクショ 11 枚: inputs/hhd/screenshots/decorate_menu/。HHD の資源: Layout/Catalog/Catalog.arc（ctl_*、tum_15、scl_Bar）、Layout/Main/Main.arc（min_Trash_00）、Layout/IconItem/NNNN.arc（5,831 本）、Item/Param/{Item,ItemSort,Kind}.bin。
  **要件（必要/不要/未確定）は docs/topics/t022_decorate_port_requirements.md が正**（2026-10-07）。模様替え UI の選択・掴む・上の物の優先は触らない。
  段取り: (a) HHD の品番 → モデル名・アイコン・分類の表 (b) ACNL の品番 → モデル名 (c) 一致表 (d) HHD のリスト UI の状態機械・タッチ・アニメの割り出し (e) ACNL の模様替え UI（F050）へタブ・リスト・ゴミ箱を足す入口 (f) 置き場所の計算（HHD）と ACNL のかざる処理。
