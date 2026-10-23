# Issue 114 作業メモ

## precheck
- kb.py search: 金のオノ / g_axe は一致なし。道具 / model / Setup / 読込で関連を確認。topics/acnl は ui.md のみ（モデルの topics は未整備）。
- ACNL-F0476・F0477 は S、材質の Setup と LUT 参照の流れを利用できる。F0533・F0547・F0447・F0449・F0542・F0122 は ? のため単独の根拠にはしない。全関数 export と入力ファイルで一次証拠を再確認する。
- 全関数 export は共有 workspace の _local/builds/acnl_jpn_v15/export にあり、作業ツリー内には無い。symbols_commit は 65293c69e61e182196200b92414beff86f647a98。現在の symbols と照合する。
- 入力は共有 _local/inputs/g_axe、作業生成物はこの作業ツリーの _local/evidence/114 に限定。git/gh、IDB、実機は未使用。
- 既存道具を公開検索済み。SPICA の Gfx.Open を数値比較に利用する。自作は読込器ではなく計測値を JSON にする薄いラッパー。Ohana3DS は主に viewer/exporter、CTR-Studio は編集機能を持つ。
