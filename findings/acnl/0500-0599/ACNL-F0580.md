---
id: ACNL-F0580
aliases:
- IDA-unknown-F005
- V2-F005
title: Volta の shim が引数を改行で切り落とす（このPC全体の問題）
summary: '`node` の実体は `C:/Program Files/Volta/node.exe`（Volta 2.0.2 の shim）。'
date: '2024-07-12'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4357-4372
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F005: Volta の shim が引数を改行で切り落とす（このPC全体の問題）

`node` の実体は `C:/Program Files/Volta/node.exe`（Volta 2.0.2 の shim）。
**引数の最初の改行以降が捨てられる**。空白・タブ・引用符は正常に通る。改行だけの問題。

| 呼び方 | shim | 実体 `%LOCALAPPDATA%/Volta/tools/image/node/24.14.0/node.exe` |
|---|---|---|
| `-e "console.log('a b c')"` | OK | OK |
| 2 行以上の `-e` | **出力なし・rc=0** | OK |

- 上流未修正: `volta-cli/volta#1791`「Newlines in arguments passed to `node -e ...`」は **open**（2024-07-12 起票、最新 release は v2.0.2 / 2024-12-05）。**更新しても直らない。**
- このPCでは `codex` / `openweb` / `opencode` も Volta 経由で動くため、**多行引数を node へ渡す他プロジェクトでも同じ症状が出る**。
- 恒久対策（採用）: **スクリプトを引数で渡さず stdin（`node -`）かファイルで渡す。** どの node／shim でも動く。
  `tools/patches/export_keyboard_layout.py` をこの形へ変更した。プロジェクト内で多行 `-e` を使っていたのはここだけ。
- 回避が要る場合は実体を直接呼ぶ（`%LOCALAPPDATA%/Volta/tools/image/node/<版>/node.exe`）。PATH で shim を追い越すと Volta の版切替が壊れる。

