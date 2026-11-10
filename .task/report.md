（ワーカーの最終の返答を司令塔が保存した）
**未確認点**
- Picture の vtable（`vtbl_nw_lyt_Picture` 0x8FBFFC）の slot 2（+8）が 0x73CB34 を指すかは未確認です。`get_int` が失敗して中身を読めませんでした。
- 0x96F160 が Picture の型情報だという結論は、隣接関数と静的初期化からの推定です。
- ルート pane の vt+0x2C が FindPaneByName であることは、引数 `(name, 1)` と使われ方からの推定です。実体の関数は追っていません。
- 0x8C9B9C の型情報（コンパイラが作る cxxabi 側）と 0x96F160（nw 自前の実行時型情報）が同じ Picture クラスを指すことを、番地の直接の参照では確かめていません。
- 実機での実測はしていません。

**迷った判断**
- 名前は `SsysMaLayoutNode_FindPicture` にしました。`SsysMaLayoutNode` は `local_types.h` にあった前方宣言を借りたもので、node の実クラス名は確定していません。
- 0x96F160 の名前は、`ti_nw_lyt_Picture` が 0x8C9B9C で使用済みだったため `nw_lyt_Picture_runtimeTypeInfo` にしました。
- 確度は MEDIUM にしました。独立した静的根拠は隣接関数と静的初期化の 2 本で、実測はありません。
- 兄弟の 0x567EA0（型 ID 0x96F164）と 0x567EFC（型 ID 0x96F14C）は、名前を付けず記録で触れるだけにしました。
- `lyt_Object_FindPane` 0x7461D0 は、ルート pane の探し方は同じでもレイアウトのクラスが違うので、同一視していません。

**依頼の範囲外の変更**
- 範囲外の変更はありません。
- 名前を付けたのは 0x567E44 と、そこから参照する型情報 0x96F160 です。
- `python tools/kb.py index` を実行し、索引（`findings/INDEX.md`、`findings/acnl/INDEX.md`、`findings/acnl/by-category/ui.md` など）が作り直されました。

**使ったゲームの事実**
- 0x567E44 は `NwLytPicture *(SsysMaLayoutNode *node, const char *name)` で、MEDIUM です。
  - `node+0x20` のルート pane に vt+0x2C(name, 1) を呼びます。
  - 結果の型情報（vt+8）の親鎖に 0x96F160 があればその pane を、なければ 0 を返します。
- 0x96F160 は nw::lyt::Picture の実行時型情報で、MEDIUM です。根拠は次の 3 点です。
  - 0x73CB34 が返し、Picture 系メソッド群に隣接しています。
  - 0x7917B0 が親の 0x96F15C を書き込みます。
  - 0x8C9B9C の `N2nw3lyt7PictureE` と対応する前提です（上記の未確認点を参照）。
- ItemIconWidget_SetItem 0x2B8EAC の 0x2B9014 で、`P_itemIcon` を `widget+0x134` から探すのに使われます（HIGH）。これは ACNL-F0484 と同じ事実です。
- 呼び元は約 40 か所あります。
- lyt_Object_FindPane 0x7461D0 は、`obj+0x48` のルート pane の vt+0x2C(name, 1) を呼ぶだけで、型の絞り込みはありません。
- 記録は ACNL-F0751（category=ui、tags=layout）です。
- `kb.py lint` と `audit.py` はどちらも問題 0 件でした。

**訂正の提案／統合・重複の提案／新しいタグの提案**
- 旧版 gohan の注記「(layout, name) -> pane、先頭の語 0xE92D4070」は妥当です。足りないのは、名前が見つかっても Picture でなければ NULL を返す点だけです。訂正までは要りません。
- 統合・重複の提案、新しいタグの提案はありません。
