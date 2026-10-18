# 描画・正常プラグイン・しずえスキップ

現役の通常プラグインは `src/gohan/`。2026-09-12に[チャット漢字候補](chat_kanji.md)を追加しビルド・PC検証済み（統合版の実機確認は未実施）。実機確認済みの復元基準は**F394、利用者が復帰としずえスキップを実機確認済み**。
`gohan.3gx`: 846070 bytes、SHA-256 `157c3159aff40fa54168ed53faa11dfe09941f424d16f1d0e5a1c79a01d77095`。
F394の現行復元ソースはgohan Gitのmain commit `fa76dfc05bcc8b362829f53ce48b1593c4099a38`。復元用3gx/ELFは `artifacts/plugins/f394_verified/` に集約。ソースの重複バックアップは削除済み。旧確定知見は `reference/old_project/BACKUP/plugin_f394_hardware_confirmed/`。上記SHAは復元用で、作業ブランチの統合gohanとは区別する。

失敗例を繰り返さない:

- F391はMITM hookが元関数を呼ばずフレーム処理を途中終了し、画面停止・音継続。
- F393はOFF判定でもcallbackがR0を破壊し、ゲームthisが0になった。F394でARMレジスタを保存して修正。
- **しずえスキップOFFでもフックは通る。** ONだけ動けばよいという試験にしない。
- 必須検査は`tools/patches/verify_shizue_hook_registers.py` と `--artifact`。**検証は PowerShell で実行する**。新ビルド時はソース段階とリンク済み経路を両方検査する。

現行メニューv2の設計は [HANDOFF_CHEATMENU.md](../../reference/old_project/HANDOFF_CHEATMENU.md) の冒頭を読む。`【v1の記録】` 以降や引退済み `OwnGui.cpp` を現行の入口にしない。描画フックを無関係なチート追加で変更しない。

描画の基礎には旧F253–F256（下画面を含む3パス、ノード方式、ゲームがそのパスを描かないフレームのゲート）がある。ケーブを扱う場合は`tools/patches/audit_node_cave.py` でリテラル・分岐・領域を監査する。現役の生成器がどれかはhandoff先頭で確定する。

ビルドは **devkitPro MSYS2ログインシェル**。Git Bash経由の環境変数継承を当てにしない。Makefileの再リンク漏れもあるため、生成物の時刻だけでなくhashとリンク済み命令を確認する。
環境の詳細: [DOCS/ctrpf_plugin.md](../../reference/old_project/DOCS/ctrpf_plugin.md)。しずえスキップはPlayerSelectの既存出口を使う処理で、起動時セーブを省く副作用がある。仕様・最新修正は [DOCS/skip_isabelle.md](../../reference/old_project/DOCS/skip_isabelle.md) のF394節を確認する。
