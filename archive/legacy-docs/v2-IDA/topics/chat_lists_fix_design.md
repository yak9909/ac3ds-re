# チャット一覧の決定・入力遮断と時刻メニュー復帰

記録: IDA-gpt-6-T004 / IDA-gpt-6-F003、担当 GPT-6、2026-10-12。実機報告を受けた修正。新修正版の実機確認は未実施。

## 根拠と設計

訂正（T005、2026-10-12）: 下記の「scrollも40Bだけで受ける」という前提は実機報告とnative ARM照合で撤回。scrollはControllerのedge/hold/float pointerも必要。追加修正は [chat_scroll_style_fix_design.md](chat_scroll_style_fix_design.md)。前回20caseのscroll endpointはmockであり、scroll成立を検証していなかった。

- 十字移動で決定される原因は GameList::MoveSelect の s_decided 通知。公共事業ではプレビュー更新として必要なので、普通チャット上のモードだけ focus 移動へ変える。A は明示的な決定要求にする。
- タッチ決定は SelectBase_WaitCalc（0x1B0698）が BAC+212 bit0 を拾って消す。選択 index の変化だけでは、十字で合わせた同じ行のタッチを検出できない。vt[24] をラップし、元の待機計算前に決定旗を読み、元関数後に確定行を通知する。元の native 描画/選択処理を保持。
- 背後の native キーボードへ touch が通るという利用者の訂正を正とする。chat list中と退場中は GuiMenu の入力遮断、開始/終了時は指を離すまで capture。GameList の native update の間だけ CTRPF の raw touch から作る40Bの Touch state を差し込み、全bytesを戻す。既存 MapModeList と同じ方式。スクロールと BAC は同じ入力を受け、keyboard は遮断された入力のまま。開く前から押していた指は使わない。
- ID は名前の文字列から除き、SetItems の後で SetItemPrefixes（0x%04X、6文字）へ渡す。前/次候補のprefixは空、ページ切替後も再設定。
- Menu_RequestOpen（0x6D1330）は要求state2を置く。Menu_PollOpen（0x6D10A8）は MENU_FLAGS bit4（field退場済み）を待って画面を作る。BsMenuSetupTime_Update（0x28C5C0）の終了は vc_UPDATE_MENU（0x51F4C0）経由の画面破棄だけ。通常タブの MenuOut calc（0x6D4E5C）は MenuGone（0x6D1074）後に背景退場と MapSyncTabsIn へ移る。この別経路の復帰が直接要求にはない。
- 時刻窓用の HoldField owner を設け、field退場→request一度→native MenuGone→owner解放→既存StepFieldのcommand2で復帰。待機中の失敗/OFF/場面変更はownerを返す。窓が開いた後はOFFでも閉じ終わりまで監視を続ける。ほかのownerのbitは落とさない。

## 検証と確度

native assembly、既存F036/F062資料と実機で確認済みのfield退場/復帰契約、source実bodyを照合。新組合せの確度はMEDIUM（複数静的証拠）。根拠 work/evidence/gohan_chat_lists_fix/static_initial.json と round2〜11。ARM32LE/imagebase0/更新code SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。T値は保存XMLのregister rangesと対象ARM命令を照合。

ビルド前 source/anchor/ABI検査→隔離artifactへbuild→linked分岐/リテラルと実関数のPC fixture。DPad focus/A/same-row touch、背景へ入力を戻さない、B退場/指release、時刻request失敗/取消/確定/OFF/他owner/場面変更を確認する。GPU/実機の見た目・操作タイミングは未確認。DBに確認した概念を注記し保存・読戻し・close後に公式XMLを更新する。ソースと今回root scopeのGit保存は全作業終了後に一括、main/実機は操作しない。

## PC検証結果

- 最終ソース23anchor/13CPP構文・4330parser/date、欠字0、しずえsource PASS。隔離build2終了0、linked分岐/LDR/ABI/native日時/IME/エディター操作/しずえ PASS。GPU/OS/arc破棄は明示fixture。
- 最終新ELFで20case PASS: DPad focus/A、公共事業preview、元BAC/WaitCalcのsame-row touch、一覧外・開始時保持touch、背景40B復元、B退場/退場中OFF/keyboard復帰、独立ID欄、native request/pollとfield退場/復帰・窓中OFF・要求失敗/待ちOFF/部屋変更/timeout/他owner保持。runtime_verifiedとchat_lists_runtime.json。
- 初回runtime_finalは最終link前ELFで実行され、final hash gateが不一致を検出した。再実行はlink終了後の新ELFで一致PASS。fixture修正（native menuID table、node visual、UIntVector sret、TLS）は製品不具合として数えない。
- 保存DBの20conceptcomment、対象全T=0、2renameとbool型を読戻し、公式XML44209functions/32995symbols/全入力bytes/hash PASS。所有者0。31source SHA/正常ELF/旧2成果物不変/13frame callback対容量16 PASS。
- 新成果物 artifacts/plugins/gohan_chat_lists_fix1/gohan.3gx は1,386,333B、SHA29e3d382374a83eaf57b8198567ded9336ff83f9d6676db38cb3c8196b64f03f。ELF SHA76639d1450f7c1d20aa05e8c93b5b84bf74be98894b195d22b4be978d599809a。ソースの確定commitは同manifest/source_code_commitを参照。
- 実機確認待ち: list十字→A/touch（同じ行含む）、背後とじる/送信へtouchが漏れない、B終了後の入力復帰、検索IDの小欄/ページ、time setの取消/確定/OFF後の地図とタブ復帰。実機成功やmain反映承認は今回未受領。
