<!-- 生成物。編集しない（kb.py index が作り直す） -->

# hhd / ui

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| HHD-F0008 | キャラクリ画面のコード — 組み立て・絵の差し替え・色の反映・選択グループ（2026-10-05、MEDIUM: 静的のみ。実機未観測） | 解析ソフト: IDA 9.3（idalib、`ida/db/hhd_jpn_v11.i64`）＋ objdump / 解析モデル: opus-5.5。根拠は逆アセンブル・文字列・静的初期化と資源の照合。 | MEDIUM | S |
| HHD-F0009 | キャラクリ画面の資源 — レイアウト・部品・色の表・状態アニメ（2026-10-05、HIGH 相当: ファイルそのものを 3DSkit で読み、2 本のスクショと配置・色が一致） | 解析ソフト: 3DSkit（Tyulis、commit 2fb6077）＋要約スクリプト / 解析モデル: opus-5.5。 | HIGH | S |
| HHD-F0011 | HHD は G_Loop と loop を持つレイアウトで繰り返しのアニメを常に再生する（2026-10-05、MEDIUM: 静的のみ） | 解析モデル opus-5.5。`LayoutObj_StartLoopAnim 0x354170`（命名）は `FindGroup(G_Loop)` と anim `"loop"` があれば結んで再生し、+600/+604 に引数を残す。 | MEDIUM | S |
| HHD-F0014 | 模様替え画面の状態とゴミ箱への落とし（2026-10-06、MEDIUM: 静的のみ。途中） | 模様替え画面（家具を置く画面）の本体は 0x3EA990〜0x3F2xxx のクラス。vtable は 0x6EF998〜0x6EFAB4（手前 2 語 0,0。直後に offset-to-top −8 の第 2 vtable）。 | MEDIUM | S |
