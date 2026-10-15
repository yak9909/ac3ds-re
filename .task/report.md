## 結果
完了。両タイトルの復元試験は不一致0件・取り込み失敗0件。`python -m pytest -q tools/tests` は 114 passed（22.80秒）。正本の IDB は開いていない。指定の作業用 IDB は試しの取り込み後に保存して閉じた。

## 結論と根拠の要約
ゲームの新規解析・記録作成はない（道具の修正のみ）。

- 関数の範囲と重なる別関数を除き、先頭を含む既存関数は手前で終了させる。共有テールは全所有者から外して必要な前半を残す。境界が既存項目と合わず終端変更が失敗する場合は、対象範囲の項目を解除して関数を再作成する。再作成時に既存の関数コメントを保持する。ARM/Thumb は address の下位ビットから設定する。
- 0x001A31F8 の拡張失敗は後半が別関数だったため。0x002FEAAC の縮小は既存項目の再作成で解消。0x004A7420 は 0x0013F0F4 の本体ではなく共有テールだった。
- 0x00955FF4 は `struct ItemID` の解決も apply_tinfo も成功していた。IDA が付ける `stru_955FF4` は名前一覧に入らず、Names() だけを走査する書き出しで落ちていた。取り込み側だけでは解消できないため、対象に挙がっていなかった書き出し側も必要最小限修正し、データ項目に付いた利用者指定型も走査する。型表記は `struct ItemID` のまま復元できた。
- 全ヘッダーを集めて前方宣言後に依存順で型を取り込む。比較も local_types.h 以外を含む全ヘッダーを対象にした。復元試験は取り込み失敗があれば不一致として終了する。
- 復元試験に --work-root を追加した。通常の書き出しと同様、未ロード領域の行は既存 CSV から保持する。ACNL の関数5件・コメント5件は skipped として明示され、IDB に復元できた件数には含まない。HHD の skipped は0件。

証拠は `A:/Disassemble/ac3ds-workspace/_local/evidence/20/`。修正前の再現結果は acnl_baseline.log/json、最終結果は acnl_restore_final.log/json と hhd_restore_final.log/json。最終試験の作業 IDB・import_report.json・書き出し CSV は acnl_jpn_v15/restore_pf6laxk_ と hhd_jpn_v11/restore_1ofw5dyo に保存した。全 IDB は閉じている。

再実行: idalib の Python で `tools/sync/restore_test.py --build <ビルド> --symbols symbols/<ビルド> --work-root A:/Disassemble/ac3ds-workspace/_local/evidence/20 --keep --report <結果JSON>`。AC3DS_WORKSPACE は A:/Disassemble/ac3ds-workspace、TMP/TEMP は evidence/20 を指定した。

追加検査: `kb.py lint` は715件・エラーなし。全体 audit は804ファイルを検査し、作業メモの CRLF だけを指摘した。改行を LF に修正後、変更した道具・テスト・作業メモ・報告書の実ファイルを audit.scan_file で再検査し、問題0件を確認した。

## 訂正の提案
なし。

## 統合・重複の提案
なし。

## 新しいタグの提案
なし。

## 未確認点
ACNL の未ロード領域にある関数5件・コメント5件は保持だけを確認し、IDB への復元は未検証。両タイトルのロード済み領域には残る不一致なし。

## 次の1手
オーケストラ側で差分をレビューし、修正した道具で正本への取り込み・再書き出しを行う。
