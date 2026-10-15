対象は記録の管理項目と道具の変更。precheck では `kb.py search superseded_by` を確認した。旧記録には `superseded_by` があり、`corrected_by` は無い。ゲームの事実を新たに解析する作業ではない。

pytest は指定された `.pytest-tmp` をサンドボックス下で参照・削除できず、試験セットアップで PermissionError になった。構文検査と main の全記録に対する `kb.py lint --quiet` は成功した。
