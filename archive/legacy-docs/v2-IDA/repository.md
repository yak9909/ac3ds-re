# 配置と直接Git操作

`project_v2` が作業・Gitのルート。現在のブランチは `IDA`、originは非公開 `yak9909/acnl_disassemble`。既存IDA履歴を親として構成変更を記録する。main/Ghidraは維持し、force pushしない。

| 対象 | 正本 |
|---|---|
| 指示 | AGENTS.md（CLAUDE.mdは相対symlink） |
| 現在地・中断対策 | work/STATE.md、SESSION.md |
| 次の作業・新しい知見 | work/TODO.md、FINDINGS.md |
| 実装 | src/gohan、src/gohan-gui-simulator、src/SwkbdEngineProbe、src/acnl-ui-designer |
| 現行の検証・生成 | tools/chat_kanji、tools/patches、tools/keyboard、tools/ida |
| 原本と解析対象 | inputs/、artifacts/、ida/ |
| 旧版資料・全原本・キャッシュ | reference/old_project/、reference/v2_before_reorganization/ |

旧資料は内容と来歴のhashを残すため書き換えない。古い絶対パスは実行先ではなく、`reference/old_project/` を旧ルートに見立てて読む。必要な旧スクリプトは現行toolsへ移し、パスと副作用を検証してから使う。

## 保存と送信

このフォルダで `python tools/workspace_audit.py` を実行し、`python tools/repository.py stage` で原本・キャッシュも含むステージ内容を検証する。コピー用作業場は作らず、現在のファイルを直接Gitに登録する。バイナリ・大容量ファイルはGit LFSを使用。

**commit・pushの前に必ず [XML交換](xml_exchange.md) を行う。** IDAブランチではIDA XML Exporter、GhidraブランチではGhidra XML Exporterで変更した各DBの最新XMLを出力し、付随.bytesと検証manifestも登録する。再解析後は再出力する。XMLが失敗/未更新なら送信しない。IDA/Ghidraで同じネイティブDBを共有せず、各ツールのDBと交換用XMLを両方保持する。

```powershell
git status --short
git diff --cached --stat
git commit -m "Describe the verified change"
git push origin IDA
```

このPCではMSYS版Gitとの混同を避け、必要なら `& 'C:/Program Files/Git/cmd/git.exe'` を使う。`tools/repository.py` もWindows版Gitを選ぶ。ブランチ切替は作業ファイルを入れ替えるため、Ghidra作業は別のclone/worktreeで行う。

認証設定は `.git/` 内部に置き、コミットには含めない。既存のアップロード用コピーは今後参照しない。Git管理データや認証以外は明示的に列挙し、原本・キャッシュの除外漏れを検査する。

clone後は `git lfs pull`。Windowsではsymlinkを使用可能にし、`core.symlinks=true` を設定する。CLAUDEのGitモードは `120000`、内容は `AGENTS.md`。ショートカットや複製で代用しない。

## gohanは別リポジトリ

`src/gohan/` は独立Git、originは `https://github.com/yak9909/gohan.git`、ブランチmain。仕様も その中の `gohan.md`（機能一覧）と `gohan-menu.md`（項目の挙動）が現行。旧 `gohan.txt` は `gohan.md` へ移行した。ソースのcommit/pushはこのフォルダから行う。acnl_disassembleのルート `.gitignore` が現行・旧版gohanソースを除外し、登録器もその除外を維持する。submoduleではなく独立clone。

新しい解析cloneではproject_v2内で次を実行する：

```powershell
git clone https://github.com/yak9909/gohan.git src/gohan
git clone https://github.com/yak9909/gohan-gui-simulator.git src/gohan-gui-simulator
```

`src/gohan-gui-simulator` も独立Git（`yak9909/gohan-gui-simulator`、ブランチmain、GitHub Pages配信）。
現在の main は素の開発ツリーで、`ui-model.js` と `app.js` が直下にある。検証器は
`tools/patches/simulator_source.py` 経由で読む。`c0251cd` 以前の Pages 版は同じ 2 つを
`web/*-v10-part-*.js` へ base64+gzip で分割していたので、その版を checkout した場合は
同じヘルパが `work/cache/simulator/` へ展開する。

**未確認変更はmainからwork/<内容>を作り、そのブランチへpushする。** 当該成果物のSHAと利用者の実機確認結果を記録してからmainへ反映。現行漢字変換・リストボックス・内蔵フォント描画は利用者確認済みでmainへ反映済み。

Git保存済みソースはcommitから復元し、コピー/zipのバックアップを増やさない。最近追加したgohan/reference/acnl_archiveとwork/backups/chat_kanji_f394、source.zipは重複を照合して削除。旧原本の固有履歴はreferenceに保持。F394ソースはcommit fa76dfc05bcc8b362829f53ce48b1593c4099a38、必要な復元3gx/ELFはartifacts/plugins/f394_verifiedに1組。検証はtools/chat_kanji/baseline.pyでGitから直接読む。登録器は旧/vendorのignoreで原本キャッシュを欠落させず現行ルートの明示的除外だけを適用する。

## CRO・CRS

更新版38 CROとstatic.crsは `artifacts/update/modules/`、索引・SHAは同フォルダのmanifest。base索引には対象なし。`tools/copy_cro_assets.py` はctrtool再抽出と旧抽出物を照合する。配置はIDBへのロード・再配置の実行を意味しない。

## アプリ依存と移動時

IDA・CPython 3.12・devkitPro/MSYS2・Git/Git LFS・Nodeはインストール済みアプリとして必要。親プロジェクトには依存しない。IDA用venvは `tools/python/idalib/`、選定Pythonパッケージは `tools/python_deps/`。

別PCやパスへ移す場合はvenvのPython本体の場所、`.codex/config.toml` の起動パス、IDAへ導入したshimを更新する。`tools/install_ida.py` の検証手順を守り、同じDBをGUIとheadlessで二重に開かない。今回の配置変更では実機書込み・Resume・3gx再ビルドを行わない。

`src/acnl-ui-designer/` も独立Git（2026-09-25 作成、ブランチmain、**リモートなし**）。ゲームの UI 素材（bclyt / bclim / bclan / bcfnt）をそのまま描いて設計する道具。取り出した素材（`assets/`）と描画結果（`out/`）は任天堂の著作物を含むので、そのリポジトリの `.gitignore` で除外し、公開しない。GitHub に置くかどうか（置くなら非公開）は利用者に確認してから決める。
