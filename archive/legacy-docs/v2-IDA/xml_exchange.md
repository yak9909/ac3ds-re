# IDA/GhidraのXML交換

acnl_disassembleは **commit・push前に必ずXMLを書き出す**。IDAはGhidra付属のIDA XML Exporter、Ghidraは標準XML Exporterを使用する。対象はそのブランチで変更した各解析DB。解析内容を更新したら再出力し、XMLと付随ファイルを一緒に登録する。

| 作成側 | 保存先 | 操作 |
|---|---|---|
| IDA / IDAブランチ | artifacts/exchange/ida/<DB名>.xml | Edit → Plugins → XML Exporter（Ctrl+Shift+X） |
| Ghidra / Ghidraブランチ | artifacts/exchange/ghidra/<Program名>.xml | File → Export Program → XML（Memory Contentも出力） |

名前・関数・型・コメント・メモリ・ARM/Thumbのregister ranges等を出力する。XMLが参照する.bytesを同じフォルダに保持。生成物はGitで版管理し、日付ごとの重複バックアップを増やさない。出力の途中で失敗したXMLを正常版に上書きしない。

保存後にXMLをparseし、PROGRAMルート・関数/シンボル・メモリ範囲・付随ファイル参照とSHAを確認する。source DB/Program・バイナリSHA・Exporter版と生成物SHAをmanifestに記録。XML/bytes/manifestを揃えてcommitし、push前にも最新の解析が反映されているか確認する。

共通検証例（project_v2内）：`python tools/xml_exchange.py artifacts/exchange/ida/acnl_jpn_v15.xml --source ida/db/acnl_jpn_v15_annotated.i64 --input artifacts/update/exefs/code.bin`。Ghidra側も対応するXML・Program名・原本binaryを指定する。

## IDAへの導入

現在のIDAは9.3。ローカルGhidra11.0.1の7xx版は非対応のため、[公式Ghidra12.1.3付属9xx版](https://github.com/NationalSecurityAgency/ghidra/tree/Ghidra_12.1.3_build/GhidraBuild/IDAPro/Python/9xx)を使用。原本・license・SHAはtools/vendor/ghidra_ida_xml。idaxml.pyはユーザーpython、xml_exporter.pyはユーザーpluginsへ配置する。Program Files・MCP・3gxは変更しない。

`python tools/install_xml_exporter.py plan` → `apply` → `verify`。導入済みならverifyのみ。復元は対象IDAを閉じ、rollbackでmanifestの2ファイルだけを除去する。Ghidra本体の更新は行わない。

IDBがGUI/MCPで開かれていないことをidb_list等で確認してから、PowerShell・project_v2内で実行：

```powershell
tools/python/idalib/Scripts/python.exe tools/ida/export_xml.py --db ida/db/acnl_jpn_v15_annotated.i64 --out artifacts/exchange/ida/acnl_jpn_v15.xml --replace
```

--replaceは内部の一時出力を検証してから既存出力を置き換える。GUIでの手動出力でも必ず構文/参照/hashを検証する。CLIは保存済みIDBを変更せずXMLと.bytesとmanifestを出力する。

## Ghidraからの出力

File → Export ProgramでXML形式を選び、Memory Contentを含める。headlessではtools/ghidra/ExportExchangeXml.javaをpostScriptとして指定可能。出力時にProgramを変更しない。相手のXMLを使うときはTitleID・入力SHA・セグメント番地を照合し、最初は別の検証用DBへimportする。

ACNL XMLをheadless importする場合は `-loader XmlLoader -processor ARM:LE:32:v6 -cspec default` を明示する。自動言語選択に依存しない。Ghidra11.0.1の検証にはJDK17を使用。

XMLは交換用であり、ネイティブIDB/Ghidraプロジェクトも保存する。Hex-Rays/Ghidraの内部解析・全型・全注釈の完全再現を仮定せず、import後に必要な名前・型・関数・コメントを照合する。XMLの来歴EXE_PATH等が旧絶対パスでも依存先として辿らず、同梱.bytesを使用する。
