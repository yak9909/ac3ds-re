---
id: ACNL-F0576
aliases:
- IDA-unknown-F001
- V2-F001
title: 正常版と統合版の区別
summary: F394は利用者が描画復帰・しずえスキップを実機確認した復元基準。ソースはgohanのcommit `fa76dfc05bcc8b362829f53ce48b1593c4099a38`、復元成果物は `artifacts/plugins/f394_verified/`。重複バックアップはGitへ集約済み。
date: '2026-09-13'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4316-4322
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F001: 正常版と統合版の区別

- F394は利用者が描画復帰・しずえスキップを実機確認した復元基準。ソースはgohanのcommit `fa76dfc05bcc8b362829f53ce48b1593c4099a38`、復元成果物は `artifacts/plugins/f394_verified/`。重複バックアップはGitへ集約済み。
- 現行gohanのチャット漢字候補はPC検証に加え、2026-09-13に利用者が漢字変換・一覧・ACNL内蔵フォント描画を実機確認しmain反映を承認。3gx SHA-256は `201af7e973b3175b7995d18aa7f92eeace5a08280debbd146099dcc794101455`。当初の「統合UI未確認」はこの報告で解消。
- 根拠: `artifacts/plugins/chat_kanji/manifest.json`、`reference/v2_before_reorganization/work/evidence/chat_kanji/`。移設後の検証は `work/evidence/chat_kanji/` と `work/evidence/reorganization/`。
- 元F407単体の結果と統合UIの利用者確認は別の根拠として保持。今後の変更を自動的に実機確認済みと扱わない。

