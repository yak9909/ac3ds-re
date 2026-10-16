# 実行手順

## IDBとAI接続

主IDBは `ida/db/acnl_jpn_v15_annotated.i64`。旧 `code.bin.i64` の注釈を継承し3DS Local Typesを追加したもの。
GUIかheadlessか、同じIDBの所有者は1つだけ。`idb_list` で状態を確認し、静的解析は次で開く。

```json
{"input_path":"A:/Disassemble/acnl/project_v2/ida/db/acnl_jpn_v15_annotated.i64","mode":"force_headless","preferred_session_id":"acnl_v2","run_auto_analysis":true,"idle_ttl_sec":3600}
```

新規の `acnl_base_cxi.i64` と `acnl_update_cxi.i64` はそれぞれ本体/更新の比較用。旧注釈は自動移植していない。
`idb_save` / `idb_close(save=true)` で保存・解放する。開いているDBの `.id0/.id1/.nam/.til` を削除しない。worker終了/到達不能では再度 `idb_list/open` で接続先を確認する。

GUI側MCPは現在のGUI DBを操作する。動的GDB DBに静的用スクリプトを誤適用しない。GUIの `py_eval` から追加APIを使う例:

```python
import acnl_api, json
print(json.dumps(acnl_api.status()))
print(json.dumps(acnl_api.scan_svc(0x56AD0C, 0x56AD40)))
```

**idalib-mcpは任意プラグインAPIを自動公開しない。** プラグイン専用処理のheadless実行には保存済みCLIを使い、先に対象DBをMCP/GUIで閉じる。
PowerShell、カレント `project_v2` の例:

```powershell
tools/python/idalib/Scripts/python.exe tools/ida/run.py --db ida/db/acnl_jpn_v15_annotated.i64 --out work/evidence/status_new.json status
tools/python/idalib/Scripts/python.exe tools/ida/run.py --db ida/db/acnl_jpn_v15_annotated.i64 --out work/evidence/svc_new.json --start 0x560000 --end 0x580000 svc
tools/python/idalib/Scripts/python.exe tools/ida/run.py --db ida/db/acnl_jpn_v15_annotated.i64 --out work/evidence/export_new.json --sqlite work/evidence/diff_new.sqlite --start 0x100000 --end 0x101000 export
```

出力は新しい名前を指定。`types` だけはLocal Typesの変更を保存する明示的な操作。それ以外はDB変更を保存しない。Diaphoraの全体exportは時間とファイル容量を要するので目的の範囲から始める。
本体/更新の出力を比較するにはIDA外で次を実行する（出力先は新しい名前）。

```powershell
tools/python/idalib/Scripts/python.exe tools/vendor/diaphora/diaphora.py work/evidence/base_sample.sqlite work/evidence/update_sample.sqlite -o work/evidence/comparison_new.diaphora
```

保存済みの実比較結果は `work/evidence/base_vs_update_sample.diaphora`、検証要約は `diff_roundtrip.json`。対応候補はassembly/xref等で裏取りしてから名前・型を移す。export APIは未命名の `sub_*` も含む設定を明示している。

この環境では制限されたshell内のidalib起動が即終了したため、通常権限での起動が必要だった。GUI内に `idapro` をimportして回避しない。

## CIA・資源

`tools/bin/ctrtool.exe` は既存のCTRTool 1.3.0をhash一致で複製。[公式配布元](https://github.com/3DSGuy/Project_CTR/releases/tag/ctrtool-v1.3.0)。
`tools/extract_cias.py` がCIA→CXI/ExHeader/ExeFS/RomFS→codeを抽出する。既存出力は再利用するため、原本を交換した場合は別label/出力先とmanifestを作る。元の入力に上書きしない。
`tools/index_artifacts.py` はExHeaderとCXI内bytesを照合し、RomFSファイル索引を作る。`rg "ModulePlSelect" artifacts/update/romfs_index.txt` のように検索できる。全RomFS展開は必要になったときだけ別サブフォルダへ行う。
ローダー修正は `tools/prepare_loader.py`、新規読み込み試験は `tools/check_loader.py base|update`。同名DBがあれば拒否する。既存成果物を再生成のため勝手に消さない。

## プラグイン導入・復元

実導入先は `%APPDATA%/Hex-Rays/IDA Pro/{plugins,loaders,cfg}`。Program Files、既存MCP設定、3gxは変更しない。
`tools/install_ida.py plan` → `apply` → `verify`。applyは成功済みなので通常は **verifyだけ**。現物のhashが変わっていれば勝手に上書きしない。
復元はGUI/関連headlessを閉じて `python tools/install_ida.py rollback`。manifestに載る8ファイルだけを戻す/除く。既存MCPは対象外。必要なファイル権限は実行環境に従う。
Python shimは `project_v2` の固定パスを参照する。**project_v2を移動するときは再ステージ・検証・再導入が必要**。選定vendorやpython_depsを一時ファイル扱いで消さない。

## commit/push前のXML

IDAはXML Exporter、Ghidraは標準XML Exporterで最新解析結果を出力。XMLと.bytesを検証・登録してからcommit/pushする。手順・保存先・専用導入器は [xml_exchange.md](xml_exchange.md)。本体の再ビルドや実機操作は不要。

## 動的解析・実機適用

1. ida-pro-mcpで対象プロセス、停止状態、PC/SP/LR/CPSR、BP、runtime mapを確認。以前のbootのアドレスを使わない。
2. 静的IDBと命令列・相対位置を複数点照合。実験対象の初期化・ABI・所有者を確認し、元bytes/確保範囲/復元値を保存。
3. ビルド前のソース検査と、ビルド後の全分岐・LDRリテラル・定数境界・stack/VFP・cave/`.bss`重複検査を行う。
4. 停止中に最小変更だけ適用し、別読取りで全bytesを照合。走らせるなら `tools/dynamic/run_timed.py` でResume前に停止を予約し、自動停止後に状態を再確認する。
5. 戻り値・副作用・guard・解放/復元を確認。成功と失敗の両方を記録。未完了操作をSTATEへ残す。

画面が判断材料なら [dynamic_observation.md](dynamic_observation.md) に従いChokistream PNGも必ず保存・実見する。Image Sequenceを優先し、Visualウィンドウは対象HWNDを直接取得する。旧版のデスクトップ切り取りは使わない。実機やIDAを動かす前に `python tools/dynamic/verify.py` を通す。

タイムアウトは操作不成立の証明ではない。二重実行せず現在値を確認する。音だけ動くfreezeは描画だけが原因とは限らず、フレーム入口や呼出し規約も調べる。cache処理の例外は [keyboard.md](topics/keyboard.md) のF405/F406を参照。
