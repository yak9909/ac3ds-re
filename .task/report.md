## 結果

完了。完了条件1〜4について、旧3件を一次証拠から再解析し、訂正を含む新記録を作成した。指定IDBコピーへ関数名・プロトタイプ・部分構造体・フック位置の契約を反映し、公式export_symbolsでsymbolsへ書き出した。実機は操作せず、確度はMEDIUM。

書誌上の残件: byは、このセッションの明示情報である系列名gpt-6をstamp --selfで記入した。詳細な実行モデル名は環境に無く、問い合わせにも現時点で返答がないため、台帳上の格付けは?のまま。正確な実行名が分かるオーケストラ側で確認・再stampが必要。格付け台帳の変更や詳細名の推測はしていない。

検証: codebytes元語とvtable・書き出しを照合。元ARMのCPU実行でSELECT/START全16遷移、本体とWrapperのrelease残留3条件、pointerの二重表現、28対象bitのrepeat保持カウンター消去を確認。IDB保存後の公式再exportで型のサイズ・欄位置と注記を読戻した。kb lint --strictは743件・エラーなし、auditは1005ファイル・問題0件。更新実ファイル15件もaudit.scan_fileで補完検査し問題0件。git/ghコマンドは実行していない（道具内部を除く）。

## 結論と根拠の要約

- ACNL-F0721: Calc+0x24は入力更新後・旧状態を引数へ複製する前。現在値に加えてR8/R9の旧状態を整合させると、本体と登録Wrapperのheld/pressed/released/repeatとpointer edgeをまとめて除去できる。旧位置+0x30でもR1/R2だけの除去ではWrapperにreleaseが残る。
- ACNL-F0722: タッチはpointer validとheld内bitの両方で読まれる。除去は共有TouchState、スクロール、全登録Wrapper、入力idle判定へ及ぶ。下画面UIだけのロックではない。アナログ軸・過去のgesture状態は別である。
- ACNL-F0723: GameInput_ReadPadState+0x110のBLEQはbyte0x009778D8==0の場合だけ。読み替え前pad三語のSELECT bit2を除去すればSTARTを保持できる。両フラグ経路に共通する加工境界は+0x100であり、元PC相対LDRの意味保持が必要。

## 訂正の提案

- ACNL-F0376: 一部訂正。現在holdを消すだけではreleaseが発生することを元命令・本体/WrapperのCPU実行で反証。0x002E08F8はCommonButtonSingleのpane付替えであり、これだけから旧実機ButtonActionNodeEx配列の+0xD9の意味を移せない。旧object実測値は未確認として切り離す。
- ACNL-F0377: 一部訂正。ゲームの入力処理を確認したが、下画面ロックはゲームの画面別機構ではない。過去の製品実装・暗幕仕様・実機成功報告は今回の証拠には含めない。0x009B7010をゲームのlock変数と扱わない。
- ACNL-F0381: 一部訂正。SELECT→STARTは条件付き。pressed/releasedのSTART統合も実行され、単純なheld書換えだけではない。SELECTとSTARTを同時に入れ替える場合にはSTART pressedが出る。非実行経路まで「seadでは区別不能」とする一般化を撤回する。

## 統合・重複の提案

ACNL-F0721〜0723を将来topics/acnl/input.mdへ統合できる。F0380の二重タッチ表現、F0426/F0427のcontroller座標・scroll部分は今回独立に照合した範囲と重なるが、各旧記録全体の再解析完了とは扱わない。

## 新しいタグの提案

なし

## 未確認点

- 正確な実行モデル名によるbyの確定（解析結果とは独立した書誌項目）。
- byte0x009778D8のwriter・意味・場面別の値。未知のため推測名を付けていない。
- 実機での遮断開始・解除、押したまま解除、SELECT/START重ね押し・同時入替え、ドラッグ途中の状態。
- 全scene・全Wrapper・全raw HID読取りの網羅、旧実機objectの同定、特定プラグインのHID読取り順と旧報告の再現。
- 全heldを消してもスライドパッドのfloat値は残る。これはゲーム進行や描画そのものの停止ではない。

## 次の1手

実行モデルの詳細名を確認して新3件を再stampし、索引を更新する。その後、byte0x009778D8のwriterを指定exportで追う。実機操作が別途許可された場合は、Calc+0x24前後とWrapper出力を境界フレームで読み、ボタン四状態・pointer三状態・軸・TouchState履歴を照合する。
