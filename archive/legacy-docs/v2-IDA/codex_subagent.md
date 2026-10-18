# Codex CLI をサブエージェントとして使う

2026-10-07 制定（利用者指示）。親エージェント（Claude Code）が、独立して進められる調査を Codex CLI へ任せる。

## 使い方

```
python tools/codex/codex_sub.py --name <依頼名> --task-file work/codex/tasks/<依頼名>.md [--idb <Codex が開いてよい IDB> ...]
echo "依頼文" | python tools/codex/codex_sub.py --name <依頼名> -
```

- モデル: **gpt-6.1-sol / 推論 xhigh**（利用者指定。当初 max、5 時間枠の消費が大きいため 2026-10-07 に xhigh へ）。サイバーセキュリティ等の制限で断られた・異常終了・最終回答が空のときは **gpt-6-sol / xhigh** で 1 回だけ自動でやり直す（`--no-fallback` で止める）。
- 権限: 利用者の指示により承認なし・サンドボックスなし（`--dangerously-bypass-approvals-and-sandbox`）。代わりに `codex_sub.py` が依頼の前に共通の前提を付けて縛る: AGENTS.md の規則、開いてよい IDB、実機に触れない、git を操作しない、src/gohan を変えない、出力先 `work/codex/out/<依頼名>/`、記録 ID の書式、最終回答の形。
- Codex はプロジェクトの `.codex/config.toml` の MCP（idalib / ida_pro_mcp）を使える。idalib のワーカーは親と共有され、互いのセッションが `idb_list` に見える。
- 記録: 全ログ `work/logs/codex/<依頼名>_<日時>_<モデル>.log`（git に入れない）、最終回答 `.md`（必要なら登録）。
- 長い依頼は Bash の `run_in_background` で走らせ、親は別の作業を進める。並列は IDB が重ならない範囲で。

## 親の責任

- **IDB は同時に 1 所有者。** Codex に IDB を渡すときは、親のセッションで `idb_close` してから `--idb` に書く。Codex は最後に保存して閉じる。終わるまで親はその IDB を開かない。
- 記録 ID の採番・FINDINGS / SESSION への記入・XML 書き出し・commit は親が行う。Codex の結果を採るときは ID を `IDA-gpt-6.1-sol-F<番号>`（予備で走った場合は `gpt-6-sol`）にし、解析モデルを正しく残す（docs/record_ids.md）。
- Codex の結論も無条件に信じない。番地・根拠を親が 1 か所以上独立に照合してから採る。
- 実機の操作・3gx の配置は Codex に任せない。gohan のソース修正は利用者の指示（2026-10-08「修正は Codex を利用」）により `--allow-gohan` を付けた依頼でだけ任せる（ファイルを依頼に明記。git 操作・push・配置・実機は親）。親は差分を読んで検証してから commit する。

## 途中で止めるとき（2026-10-07 の教訓）

- **プロセスを強制終了しない。** 2026-10-07 に TaskStop で止めたら、Codex が開いていた IDB が保存前の展開ファイル（.id0 など）を残して止まり、親が退避と再保存で後始末をすることになった。
- 止めるときは、同じセッションを再開して「新しい調査をやめ、IDB を保存して閉じ、ここまでを report.md にまとめよ」と指示する。依頼文は**引数で渡す**（`codex exec resume` は標準入力の `-` を受け付けなかった）:
  `codex exec resume <session id> "<指示>" -m gpt-6.1-sol -c 'model_reasoning_effort="xhigh"' --dangerously-bypass-approvals-and-sandbox -o <最終回答.md>`
  session id は `work/logs/codex/<依頼名>_*.log` の先頭にある。
- 既に強制終了してしまった場合は、展開ファイルを退避してから、最後に保存した `.i64` と Codex の変更記録（idb_*.json）を突き合わせ、欠けたものは親が当て直す。

## 止め方（2026-10-07 改訂。利用者の指摘「IDB の保存やクローズも Codex にやらせたほうが安全では」）

- 走っている `codex exec` には指示を送れず、プロセスを止めると Codex の IDB の作業プロセスも消える（止めた後に再開させても、保存すべき開いた IDB はもう無い）。
- そこで **停止要求ファイル** を使う: `codex_sub.py` の前提文が「区切りごとに `work/codex/STOP_<依頼名>` を確かめ、あれば調査をやめて全 IDB を idb_save → idb_close し、report.md と SESSION.md を書いて終わる」と指示する。
  親は `touch work/codex/STOP_<依頼名>` するだけで、プロセスは止めない。終わりの通知を待つ。急ぐときでもまず置いて、一定時間（例 10 分）待ってから考える。
- 前提文でこまめな idb_save と SESSION.md の更新も求めている（2026-10-07 の t022_spawn2 は止める前に 4 つの IDB を自分で保存・閉鎖済みで、失ったものは無かった）。

## 途中で指示を送る・止める（2026-10-07 再改訂。利用者の指摘「Codex には途中で指示を送れるフォローアップがあるはず」）

- 上の「走っている codex exec には指示を送れない」は `codex exec` に限った話だった。`codex queue --thread` も exec には届かなかった（試験: sleep 60 の間に送った合言葉が答えに入らなかった）。
- アプリサーバーのプロトコル（`codex app-server generate-json-schema` で確認）には **turn/steer**（走っている依頼に指示を足す）と turn/interrupt がある。
  `codex_sub.py` は 2026-10-07 から **tools/codex/codex_app.py 経由**（codex app-server を stdio で起動し thread/start → turn/start）で動かす。試験: sleep 60 の最中に送った合言葉が答えに入った（「完了 ひまわり」）。MCP（idalib）も使える。
- **途中の指示**: `work/codex/STEER_<依頼名>.md` に文を書いて置くと、2 秒以内に turn/steer で届き、ファイルは消える。
- **止める**: 同じく STEER で「停止: 新しい調査をやめ、開いている IDB を全部 idb_save → idb_close し、report.md と SESSION.md を書いて終われ」と送り、終わりの通知を待つ。プロセスは止めない。
  最後の手段は `work/codex/INTERRUPT_<依頼名>`（turn/interrupt）。前提文には予備として STOP_<依頼名> の確認も残してある。
- ログ: `<依頼名>_<日時>_app.jsonl`（全通知）、最終回答は `.md`。
