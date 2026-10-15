---
id: ACNL-F0581
aliases:
- IDA-unknown-F006
- V2-F006
title: IDA9.3のGhidra XML Exporter導入・主IDB出力
summary: ローカルGhidra11.0.1の7xx版はIDA9のAPIに非対応。公式Ghidra12.1.3付属9xx版（Exporter 5.0.2）を原本のままユーザーIDAのpython/idaxml.pyとplugins/xml_exporter.pyへ配置。原本manifestと配置先SHAが一致する。IDA SDK930でplugin読み込み・XML出力を確認。
date: '2024-07-12'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1048576
- 1056768
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4373-4380
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F006: IDA9.3のGhidra XML Exporter導入・主IDB出力

ローカルGhidra11.0.1の7xx版はIDA9のAPIに非対応。公式Ghidra12.1.3付属9xx版（Exporter 5.0.2）を原本のままユーザーIDAのpython/idaxml.pyとplugins/xml_exporter.pyへ配置。原本manifestと配置先SHAが一致する。IDA SDK930でplugin読み込み・XML出力を確認。

主IDB `ida/db/acnl_jpn_v15_annotated.i64` の保存SHAは前後一致。出力XMLの44,190関数はIDA APIの関数数と一致し、32,049シンボルを含む。独立XML parserでPROGRAM・全付随.bytes参照の存在/範囲・SHAを検証PASS。既存出力を検証済み新bundleへ置換する経路も実行確認。根拠は `artifacts/exchange/ida/acnl_jpn_v15.{manifest,validation}.json`、`work/evidence/xml_exchange/install.json`、`work/sessions/xml_exchange_20260913.md`。

Ghidra11.0.1では [0x100000,0x102000) の限定XMLをimportし、標準Exporterで再出力した63関数/23シンボルと8192bytes一致を独立検証PASS（sample/roundtrip.json）。ARMでFunctionPurgeAnalysisCmd非対応の警告は残る。全DBの完全往復は未確認。大規模importは-noanalysisでも関数stack解析を実行するため、構文検証と全解析の再現を区別する。XMLとネイティブDBを保持。実機・gohan・3gxは変更していない。

