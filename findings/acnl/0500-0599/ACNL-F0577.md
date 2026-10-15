---
id: ACNL-F0577
aliases:
- IDA-unknown-F002
- V2-F002
title: 旧プロジェクトの内部保存
summary: 旧原本・資料・キャッシュ32395ファイル、7271181421 bytesをコピー元とSHA-256照合して保存。
date: '2026-09-13'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4323-4329
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F002: 旧プロジェクトの内部保存

- 旧原本・資料・キャッシュ32395ファイル、7271181421 bytesをコピー元とSHA-256照合して保存。
- 根拠: `work/evidence/reorganization/archive_manifest.json`。旧AGENTS/CLAUDEは `.legacy.md`、内包Gitメタデータは `_git_metadata/` に改名しただけで原本bytesは保持。
- 保存成功は旧資料の仮説が正しいことの証明ではない。


