# gohan：普通チャットの漢字候補

2026-09-13更新。F394の正常プラグインへF407の変換エンジンを統合。**PC検証済み。漢字変換・リストボックス表示・ACNL内蔵フォント描画は利用者が実機確認済み**。現行統合ソースのmain反映を明示承認。

> **2026-09-25 変更（gohan 9992934、work/sim-0925、実機未確認）**: 「漢字変換」はトグルになり、下画面のリストボックスではなく
> **チャットの下画面の候補欄**（Simulator 670e44f）で選ぶ。項目のホットキーで未確定（無ければ選択範囲）を変換し、Enter で確定、
> Backspace で読みへ戻す。「コンポジション」トグルでかな入力に未確定を付ける。仕様は gohan.md §12、実装は `Sources/ChatKanji/ChatIme.cpp`、
> 根拠は FINDINGS IDA-opus-5.5-F043 / F044。エンジン（Request / Poll / worker）は下の記述のまま使い、読みを渡す `RequestText` を足した。
> 以下の「使い方」はリストボックス版（F394 / F407）の記録。

## 使い方
1. 新しい `gohan.3gx` を導入した状態で、自前メニューを有効にする。
2. ACNLの**普通のチャット**を開き、`かんじ` などを入力したままにする（送信しない）。
3. SELECTで自前メニューを開き、ルートの **「チャット漢字候補」** をAで実行。
4. 下画面に候補を順位付きで表示。十字上下でスクロール、BまたはAで閉じる。変換中もBで閉じられる。

実行時点の入力を1回取得する。入力変更後はもう一度実行する。本文への書戻し・送信は行わない。フレンドチャットは使用しない。ホットキーを割り当てれば、普通チャット内から単発実行も可能。

最大300件、8行表示。上限到達時は `+ (LIMIT)` と表示。行は幅と28文字の制約で末尾を `...` に省略する場合がある。保持する候補自体は最大55 UTF-16単位。学習履歴・ユーザー辞書は取り込まない独立contextなので、個人学習済み内蔵キーボードの順位とは異なり得る。エラー時は通知に理由またはERROR/STAGEを表示し、候補を公開しない。

## 構成と根拠
- `src/gohan/Sources/ChatKanji.cpp` が読取り・worker・結果の寿命を管理。`GuiMenu.cpp` の既存下画面リストへ接続。ゲームのチャット入力処理に新しいフックは追加しない。
- 普通チャットは `[0x949D4C]+0x1EC` のBsMenuChat。vtable=`0x8E5120`、`+0x50`のポインタが自身`+0x58`、容量65、child`+0xDC`、`[0x94A654]`と共有入力`[0x958108]`を照合し、入力上限32と二重読取りの一致を確認。共有入力だけでは別画面を誤認する。ctor/init/exitのMCP assemblyと抽出codeで照合した。
- TitleID `0x0004000000086200` と6地点の16bytesを照合し、別版は拒否。アンカーは `Includes/ChatKanjiAnchors.h`、原本照合は `work/evidence/chat_kanji/anchors_ida.json`。
- F407のEngine/Probe/EngineCall/Relocationsは6ファイル同一bytes。FS bridgeもクラス名以外同一。内蔵タイトルから辞書と元codeをRAMへ読む。**SD/3gxに辞書・元codeを同梱せず、内蔵キーボード画面・APTを起動しない**。5 MiB arena、315再配置、専用64 KiB stack、cache SVC `0x92/0x94` を使用。
- 変換は1 workerだけ。GUIスレッドは読取り済み文字列を渡し、worker完了通知後、**threadJoinの戻り値が厳密に0**の場合だけ解放・公開。3DSの正のtimeout ResultをR_FAILEDだけで判定すると早期解放し得るため禁止。閉鎖ではworkerを強制停止せず結果を破棄。終了時にjoin。
- 候補漢字は常駐 `Garden_msg_size16` を使用。`[0x94C9C8]+0x188`のResFont、phase`+0x1A1==3`、vtable`0x8FCAAC`を検査。6wordsを私有コピーしlookup cacheだけ独立、ゲームの辞書表/フォントを書き換えない。
- 日本語フォントは154枚のA4シートを使うため、既存の単一シート用Batch容量を流用しない。専用8枠×28文字にゲーム標準 `(78*n+57)&~3` wordsを確保（元関数`0x4D76A8`/`0x4D5480`）。記録リストも312B/文字で見積もる。既存UI枠は従来の圧縮式を維持。私有配置487328B/容量589824B。ゲームからのatlas借用は0x9000のまま。
- 3gxの予約を10 MiBへ。最終成果物の実行領域1409024B、heap9076736B。既知の内部領域・フレームバッファを差し引く保守的計算で7327744Bが残る。実行時の確保失敗も処理する。この計算は実機の空き最大連続領域を保証するものではない。

## 検証・再現
すべて `project_v2` を作業ディレクトリとして **PowerShell で**実行する（Git Bash から起動すると g++ の子プロセスが無言で rc=1 になる）。本文のパスも、明記しない限りこのルートからの相対パス。実機へ接続しない。

```powershell
python tools/chat_kanji/verify.py
python tools/chat_kanji/build.py
python tools/chat_kanji/artifact.py audit
python tools/chat_kanji/artifact.py emulate
python tools/chat_kanji/frontend.py
python tools/patches/verify_shizue_hook_registers.py --artifact
python tools/chat_kanji/package.py
```

ソース検査→ビルド→生成物検査の順を守る。`verify.py` は既存UI配置/ケーブ、しずえレジスタ、キーボード10943遷移・15描画場面の検査も呼ぶ。新規ヘルパーのUTF16/UTF8境界、FS失敗時解放、全65536コードポイントの字形/幅と元ACNL ARM、stockサイズ65件を検証する。`font_tables_sparse.bin` は読取り観測したヘッダとCMAP/CWDHだけを残した疎なfixtureで、画像シートは含まない。

`artifact.py` はF407検証器を**実際のgohan.elf**へ適用し、展開した検査スクリプトと出典SHAを保存する。再配置後の原本ARMは元VAを未マップにし、2種類のarenaで原本候補列/順位・ABI・stack guard・辞書の不変性を照合。入力は `かんじ`、`わたしはねこがすきです`、`か`、32文字の`あ`、`漢字テスト`（準備のみのケースも実施）。cache SVCは模擬、GPU/実機スケジューラは対象外。

`frontend.py` はリンク済みRequest/Poll/Dismissを実行。ゲーム領域をCPU読取り専用にして、所有者/版/入力境界/二重起動/タイムアウト/取消/300件/フォント消失等24ケースを検証。OS・thread・TitleID・newlib reentの境界は模擬。エンジン実行試験とは別の検査であり、実機での全体動作を保証しない。

根拠は `work/evidence/chat_kanji/` の `prebuild.json`、`artifact.json`、`emulation.json`、`frontend.json`、`font_oracle.json` とログ。成果物とソーススナップショットは `artifacts/plugins/chat_kanji/`。ゲーム内の表示・キャンセル・再実行・しずえ遷移は今後の最小実機確認項目。

## Simulator との対応（2026-09-13）

`src/CTRPF-GUI-Simulator`（ローカル専用コピー）を廃止し、独立Git `yak9909/gohan-gui-simulator` の clone へ統一した。
公開版にはチャット漢字候補UIが入っていなかったため、**利用者の判断でローカル版を優先**し、
解析Git `82adf284` の内容を simulator の `main`（`4083d70`）へ反映した。公開版にあった新しい preview は
`c0251cd` 以前から参照でき、後日あらためて実装し直す。

検証器は `tools/patches/simulator_source.py` 経由で `src/gohan-gui-simulator/{ui-model.js,app.js}` を読む。
`verify_plugin_port_v2` の群5 を含め `verify.py` は **Prebuild PASS**。

## 正常版へ戻す
復元用 `artifacts/plugins/f394_verified/gohan.3gx`（846070bytes、SHA-256 `157c3159aff40fa54168ed53faa11dfe09941f424d16f1d0e5a1c79a01d77095`）を導入し直して再起動。ソースはgohan Gitの旧F394 commit `fa76dfc05bcc8b362829f53ce48b1593c4099a38` から復元する。baseline.jsonに元SHAとGit参照を保存。作業ソースへ部分上書きせず、対象commitの別worktree等で検証してビルドする。

2026-09-13更新: 利用者が漢字変換・リストボックス表示・ACNL内蔵フォントによる変換結果描画を実機確認済みと明示し、現行ソースのmain反映を承認。main=d189cd6da66128e7742988cdaf661e00dd0a3470。今後の未確認変更は必ず作業用ブランチへpushする。
