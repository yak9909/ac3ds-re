# アイテム名検索の連続取得

記録: IDA-gpt-6-T006、GPT-6、2026-10-12。修正版は実機未確認。

## 利用者の指定と実装

- かなのアイテム名検索は、Aまたは行のタッチで取得後も一覧と選択位置を保つ。同じ候補を再度決定でき、通常終了はBのみ。
- `ChatCommands::Tick` の決定時の `CloseList` をコマンド一覧分岐へ移す。アイテム検索は既存 `PocketItem::Request` と通知だけを行う。取得失敗でも検索一覧は維持する。
- コマンド `list` は決定後に閉じ、文字をチャットへ挿入する。検索ページは従来通り切り替える。Bは保留中の決定に優先し、退場が終わるまで背景入力を遮断する。
- チャット消失・一覧エラー・機能OFF時は従来の資源解放を行う。無効になったゲーム画面を維持しない。

## 検証と範囲

- `tools/gohan_chat_ports/verify_search_repeat.py` はリンク済みTick/FrameStepと元native BACを使い、連続A・A保持・同じ行touch連続・十字focus・満杯/再取得・ページ切替・B優先/退場/キーボード復帰・command list/画面消失を検査する。取得と通知/ダイアログは明示endpointで、実際の持ち物書込み・描画・実機タイミングの保証にはしない。
- 同じ実行でT003入力/hotkey、T004一覧/時刻窓、T005元native scroll/arc解放/検索ID順を回帰検査する。ソース検査後に専用 `BuildChatSearchRepeat` でビルドし、リンク済み分岐/LDR/ABI/SP/VFP/hashを検査する。
- 成果物: `artifacts/plugins/gohan_chat_search_repeat1/`。根拠/最終hash: `work/evidence/gohan_chat_search_repeat/`。正常版と全旧配布版を保持。実機/SD/mainへ適用せず、実装・検証後に最後一括で作業枝へ保存する。
- 新たなnative概念の解析/DB編集はない。T005の保存DBと最新公式XMLのhash一致を最終gateで照合する。

結果: 追加12caseと既存20case/native scroll/arc/検索順/Map/hotkey PASS。4330parser・23anchor・13CPP、linked570関数/35655命令/6617直接分岐/3333PC参照とABI/SP/VFP/しずえ/hash PASS。32製品source hash、正常ELF/全旧配布artifact、保存DB/最新公式XML不変を確認した。実機確認は利用者の次の操作。
