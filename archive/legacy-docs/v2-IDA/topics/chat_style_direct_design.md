# hair/style/eye/eyesを既存HHD画面へ直接渡す

記録: IDA-gpt-6-T008、GPT-6、2026-10-12。修正版実機未確認。

## 利用者の訂正

fix2（3gx SHA `e2afb75ae0d8c3ce9a95e82a36a2cd865c063cc739ea771c264533f90c5adf2e`）のリスト修復は利用者が実機確認した。一方hairは未修復。利用者は「HHD式スタイル変更自身が退場処理と完了待ちを含むので、コマンドはそれを呼ぶだけ」と明示した。

T007の外部chat退場/親・keyboard消滅待ちはstyleコマンドに適用しない。native chatのlifetime観察自体は維持するが、それをHHD起動の前提と解釈した点と、旧CPU試験の早期Showを不具合扱いした点は撤回する。旧試験は加えた待機条件を検証していたにすぎず、実機での修復を証明していなかった。

## 実装

- Parserが同じKind::Styleへ解決する`hair`/`style`/`eye`/`eyes`を、Tick内で直ちに`HhdScreen::Show()`へ渡す。失敗結果だけ既存のLastErrorから表示する。
- `Post(CloseChat)`/AfterClose/ChatRetired/FieldShownはstyle起動経路から外す。HHDのShow自身がHoldFieldとCopyで下画面の退場・待機・組立を所有する。起動済みの再要求もShowの既存処理へ任せる。
- `time set`のネイティブ時刻窓は従来の独立CloseChat/AfterCloseを保つ。AfterCloseからStyleを再分岐する処理は除去する。
- HHD本体/GameList/scrollの製品sourceは変更しない。待機中B/失敗時の資源返却等はHHD既存機能として保持する。

## 根拠・試験

既存Show/GUI actionのsource所有経路と、リンク済みParse/Tick/Show/HoldField/Copy後片付けを独立照合する。新試験は通常chat bindingと親窓/keyboardが生きている状態で呼ぶ。SD/pool/clone/OS/GPUはfixture endpointであり、成功画面描画と実機timingは未確認。

- 旧fix2で4aliasともShowを呼ばず、CloseChat op2/Style afterClose6を予約することを再現。
- 新版は同frameでShowへ到達、chat/keyboard/bindingは存続、外部op/AfterClose予約なし。4alias・表示中再呼出し・Show失敗時の戻りと通知・TimeMenu経路の分離を検査する。
- 既存のリスト20case/連続取得12case、元native viewport/matrix/hit-testによるscroll操作/入力全復元・vtable不変、arc/全ID順/Map/hotkey/time復帰を併せて検査する。
- ビルド前4330parser/23anchor/14CPP、組立後の全分岐/LDR/ABI/SP/VFP/領域/hashとしずえhookを検査する。
- F005のHHD要件を述べた3注記（`0x1939B8`/`0x94A654`/`0x949D4C`）へT008訂正を追記しsave/close/公式XMLで読戻す。native names/types/code bytesを変更しない。

成果物: `artifacts/plugins/gohan_chat_style_direct1/`、根拠: `work/evidence/gohan_chat_style_direct/`。確定hash/保存commit/試験結果はmanifest/publicationを参照。正常・全旧配布版を保持し、完成後まとめてgohan作業枝と解析IDA枝へ保存する。実機/SD/mainは操作しない。

次の実機確認: 通常チャットからhair/style/eye/eyes実行→HHD画面表示、B閉鎖と再実行、失敗時の操作復帰。新直接呼出し版の確認前にmainへ入れない。
