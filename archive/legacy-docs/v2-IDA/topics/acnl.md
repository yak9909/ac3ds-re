# ACNL固有の解析判断

## RTTI・vtable

旧F-43/F-53でRTTIを実機照合し、2895クラスの実名をIDBへ反映済み。これはVTable Explorerの検出行数とは別の数。
本作にはItanium C++ ABI系のRTTIがある。通常のaddress pointは最初の仮想関数で、`vtable-8`がoffset-to-top、`vtable-4`がTypeInfo、TypeInfoの`+4`がマングル名。**単一継承の `__si_class_type_info`** では `+8` が基底TypeInfo。無継承・多重継承を同じ構造と決めつけない。

IDBは `ti_<Class>` / `vtbl_<Class>` や既存のマングル名を検索する。名前がない場合は更新版の `0x8CD000..0x8E5000` のRTTI文字列を探す。RTTIの実名が取れるものを用途から推測命名しない。
VTable Explorerはヘッダ側のアドレスを返す場合がある。例えば検証したAABB行の `0x905530` は0のoffset-to-top、次がTypeInfoで、関数ポインタはその後。プラグインが返すaddressをそのままオブジェクトvptrと比較しない。

根拠: 旧 [rtti.py](../../reference/old_project/rtti.py)、[rtti_apply.py](../../reference/old_project/rtti_apply.py)、`RE/FINDINGS.md` F-43/F-53。旧 `find_class.py` は狭い走査範囲と旧dump依存があるので、見つからない結果を全域の不在と扱わない。

## CROと資源

CROは実行時再配置される。静的ファイルのoffset、解析用仮想配置、実機load baseを分ける。インポートはcode/dataどちらのsegment基準かを確認する。PlayerSelectではゲーム `.data` の基準 `0x0093F000` が重要（F-362）。
`3DS-Code-Loader` はCROをまとめて仮想配置する設計で、今回の実機IDBへその番地を混ぜない。必要なモジュールを抽出して再配置とimportを解決し、実機のmodule情報と照合する。再現例は旧 [HANDOFF_MESSAGE.md](../../reference/old_project/HANDOFF_MESSAGE.md) と [DOCS/skip_isabelle.md](../../reference/old_project/DOCS/skip_isabelle.md)。

今回のCIA由来RomFSは `artifacts/{base,update}/romfs.bin`。更新版に存在しない資源は本体側も調べる。旧 `NCCH/romfs/` の別ゲーム混入と、新しく検証した入力を混同しない。
音は旧 [sounds.csv](../../reference/old_project/SOUND/index/sounds.csv)、アニメ/状態はゲーム内部名を優先。公開チートの名称・地域・余分な行を仕様と見なさない。

## 実装前の切り分け

正常/異常双方でcaller・全引数・オブジェクト生成時期を比較する。描画関数のような共有入口をフックする前に他経路からの呼出しを確認する。観測用リングは使用中のsprite表やcaveと重ねない。構成変更ごとに「効いた処理/効かなかった処理」を表で残す。
