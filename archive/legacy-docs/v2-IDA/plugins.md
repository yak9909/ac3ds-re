# プラグインの採否とAIからの使い方

調査日: 2026-09-11。実環境はIDA **9.3.0.260421 / CPython 3.12.11 / Qt 6**、対象は32-bit ARM。
名称が似ていても役割が異なるため、単純な「上位互換」とは扱わない。
固定コミットは `../work/evidence/*.upstream.json`、配布版情報は `*.releases.json`、実際の導入物は `install_manifest.json` が正。

## 導入した構成

| ツール | 用途・検証 | AIからの利用 |
|---|---|---|
| [3ds_ida](https://github.com/kynex7510/3ds_ida) `2e2b25e…`＋最小修正 | CXIからExHeaderに従って4セグメントを作成。base/update全bytes・権限一致。`types.h`読込みエラー0 | 新規IDB作成後はidalib-mcpから通常解析。`acnl_api.import_types` / `scan_svc`。対話式上流スクリプトの自動実行はしない |
| [Diaphora](https://github.com/joxeankoret/diaphora) `621ec269…` | 版間比較・SQLite出力。ARM IDBから範囲指定export成功、GUIメニュー登録成功。READMEとplugin metadataの版表記が揺れるためcommitで固定 | `acnl_api.export_diff`→SQLite。比較器はIDA外からも呼べる。名前・型のimportは別操作 |
| [Keypatch](https://github.com/keystone-engine/keypatch) 2.2 / `e7ecb93…` | GUIロード成功。KeystoneでARM命令生成→Capstone逆アセンブル→ARM11 Unicorn実行を照合 | AIはKeystoneでまずbytesを生成して検証。パッチは停止・元値・ABI等を確認した別段階 |
| [hrtng](https://github.com/KasperskyLab/hrtng/releases/tag/v3.9.114) 3.9.114 **IDA9.3専用DLL** | ARM Hex-Rays呼出し、GUI action登録を確認。型・間接呼出し・`__usercall`補助 | decompileへの作用はMCPからも利用可能。個別の型編集UIはGUI中心で、全機能がMCPの個別toolになるわけではない |
| [VTable Explorer](https://github.com/K4ryuu/IDA-VTableExplorer/releases/tag/2026.03.13) 1.3.0 | JSON Scan成功、既存IDBで1844行取得。クラス総数や完全性の保証ではない | `vtable_explorer.scan/entries/compare/hierarchy`。IDC JSON APIをPythonから呼べる。全クラスの継承正確性は未検証 |
| [Unicorn](https://github.com/unicorn-engine/unicorn) 2.1.4＋[flare-emu](https://github.com/mandiant/flare-emu) `6688c327…` | Unicorn ARM11 MPCoreで命令実行成功、flare-emuはARM・pointer幅4で初期化成功 | GUI不要のスクリプトが主用途。flare-emuの全API/複雑なゲーム関数を実機同等と主張しない |

依存は `../tools/python_deps/` に隔離: Capstone 5.0.3、Unicorn 2.1.4、Keystone 0.9.2、six 1.17.0。既存Python/MCPのパッケージを更新していない。
hrtngは `DISABLE_AUTORENAME=YES`。既存の正確な名前を守る設定で、一部の自動名前伝播機能は利用しない。IDBに保存されたhrtng設定はcfgより優先されるので、他所のIDBでは再確認する。
DiaphoraのML機能と任意高速化cdifflibは未導入。通常exportと比較は動作し、起動時の任意依存警告は導入失敗を意味しない。Keypatchの初回「configなし」は既定値使用の通知。

Diaphoraの実比較試験: 本体/更新の `[0x100000,0x102000)` を99件/137件出力し、比較器exit 0、対応候補84件を保存した。`acnl_api.export_diff` は `ida_subs=True` で未命名の `sub_*` も含める。Falseでは未命名関数が除外される。証拠は `../work/evidence/diff_roundtrip.json` と `base_vs_update_sample.diaphora`。これは出力・比較経路の動作確認であり、対応の正しさを全件確定したものではない。

## 他の提示候補と代替

Ghidra公式12.1.3付属の **IDA XML Exporter 5.0.2 / 9xx版** も導入。IDA9.3で実プラグインloadと主IDBの44190関数XML出力を検証。ユーザーpython/idaxml.py・plugins/xml_exporter.pyの2ファイル、詳細は [XML交換](xml_exchange.md)。commit/push前の交換用出力に使う。7xx版はIDA9で廃止されたAPIがあるため使わない。

| 候補・一次ソース | 判断・代替との関係 | AI利用/制約 |
|---|---|---|
| [3DS-Code-Loader](https://github.com/SinaMegapolis/3DS-Code-Loader) | 未導入。SDK7.6のC++ローダーで、CROも仮想配置してリンクする。3ds_idaの**上位/下位互換ではない**。ランダムな解析用配置を実機番地と混ぜないため、必要なCROを別途解析する | ロード済みDBならAI利用可。IDA9.3への再ビルド/検証とCRO再配置の裏取りが必要 |
| [Amnesia](https://github.com/duo-labs/idapython) | 未導入。Thumb未定義領域をヒューリスティックでコード化する2018年の処理。まずIDAのARM/Thumb解析＋限定範囲の命令/到達性確認を使用 | Pythonから呼べるが古いAPIの移植が必要。全バイナリへ推測でコード定義を適用しない |
| [uEmu](https://github.com/alexhude/uEmu) | 未導入。対話的な状態表示に有用。AIの再現可能な実験には今回検証したUnicorn/flare-emuを選択。MCUSecの同名uEmuとは別製品 | 拡張APIはあるが主な操作はGUI。上流はPyQt5設計。IDA9.3互換層があるため、それだけで動作不可とは断定しない |
| [Karta](https://github.com/CheckPointSW/Karta) | 未導入。2022年ソース、ライブラリのソース/ビルド対応コーパスが必要。今回は版間差分にDiaphora、既知ライブラリにIDA内蔵FLIRT/makesigを使用 | Python/Sark依存。Diaphoraがソース対応コーパス機能まで代替するわけではない |
| [BinDiff](https://github.com/google/bindiff) / [BinExport](https://github.com/google/binexport) | 未導入。ネイティブ比較器は有用だが、BinExport現行READMEはIDA9.4以上を要求。9.3専用ビルドを別途確保するより今回動作確認したDiaphoraを優先 | CLIとIDC exportで自動化可。将来の独立比較器候補でありDiaphoraの完全下位互換ではない |
| [Patching](https://github.com/gaasedelen/patching) / [Qt6対応fork](https://github.com/blue-devil/patching) | 未導入。ARM/Thumb対応のGUI改善版で、x86専用という説明は古い。派生v0.3はQt6対応を明示。今回のAI主体の組立/検査と重複するためKeypatch＋直接APIを選択 | 原作者版のPyQt5だけで非対応とは断定しない。派生版は未実動検証。ARM/Thumb正確性の課題はREADMEにも残る |
| [RetDec IDA Plugin](https://github.com/avast/retdec-idaplugin) | 未導入。ARM対応だが、既存Hex-Rays ARMが実動する環境では追加の重い逆コンパイル基盤を常設する利益が小さい | 別逆コンパイラでの照合には候補。IDA9.3専用バイナリは今回未検証 |
| [Rizzo](https://github.com/devttys0/ida/tree/master/plugins/rizzo) | 未導入。旧APIでの関数署名照合/rename。版間移行には現行Diaphoraの照合・コメント/型移行を優先 | スクリプト化できるが旧Python/IDA APIの移植が必要。自動rename前の対応証拠は省けない |
| Decode Instruction | **独立したプラグインをこの名称だけでは同定できなかった**。`idautils.DecodeInstruction` / `ida_ua.decode_insn` はIDA標準API | 標準decode＋Capstoneを利用。未知の配布物を名称だけでインストールしていない |
| [AMIE](https://github.com/NeatMonster/AMIE) / [FRIEND](https://github.com/alexhude/FRIEND) | 未導入。AMIEはFRIENDの軽量ARM向け再実装。AArch32/AArch64の命令・システムレジスタ資料表示。ARM11固有CP15との対応は別確認が必要 | GUIの表記/hover中心。リソースJSONは読めるがARMv8の記述をARMv6Kへそのまま転用しない。実装依存レジスタは上流でも未対応 |
| [Lighthouse](https://github.com/gaasedelen/lighthouse) | 未導入。coverage可視化器で、3DSトレース収集器ではない。まず実測traceからPC/基本ブロックのJSON/CSVを確立する | director等のPython APIはある。GUIはPyQt5系で9.3全UI未検証。実測traceがない状態でcoverageが取れるとは扱わない |

既存 **ida-pro-mcp＋idalib-mcp** は維持。別名のMCP/RPCを追加すると接続先・権限・IDB所有者が増えるため、今回の追加機能は既存GUIの `py_eval` または保存済みheadless CLIから呼ぶ。idalib-mcpにプラグインの全機能が自動公開されるわけではない。

## ローダー修正と実行上の注意

上流は `accept_file` のprocessor情報だけを返す。今回のidalibでは `set_processor_type()` がないまま止まったため、`load_file` 先頭にARM初期化を追加した。差分は `../work/evidence/ctr_loader_9.3.patch`、生成器は `../tools/prepare_loader.py`。上流ソースは未変更。
型追加は `ida_typeinf.parse_decls(None, path, None, ida_typeinf.HTI_FIL)`。IDA9.3では4引数であり、古い `PT_FILE` をそのまま渡す形と混ぜない。
SVC検出は定義済み命令だけをIDAでdecodeし、T値を反映したCapstone結果と照合する。型定義をLocal Typesへ追加しても、ゲームのSDK wrapperへSVCそのもののレジスタABIを一括適用しない。

検証根拠: `plugins_headless.json`、`loader_base.json`、`loader_update.json`、`annotated_types.json`、`gui_plugins.json`（いずれも `../work/evidence/`）。GUI/初期化成功は全機能・全入力の保証ではない。
