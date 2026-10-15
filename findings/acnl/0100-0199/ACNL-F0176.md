---
id: ACNL-F0176
aliases:
- F-138
title: 'F-138: ida-pro-mcp の実機接続経路を復旧・検証 — `HIGH`'
summary: IDA GUI の Remote GDB 接続や RPC 自体が壊れていたのではなく、Codex のMCP設定から
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4603428
- 1048576
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9032-9059
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-138: ida-pro-mcp の実機接続経路を復旧・検証 — `HIGH`

IDA GUI の Remote GDB 接続や RPC 自体が壊れていたのではなく、Codex のMCP設定から
実機用 proxy server が欠落していた。確認結果は次の通り。

- `netstat` で `127.0.0.1:13337` は GUI IDA (`PID 42156`) が LISTENING。
- `ida-pro-mcp --ida-rpc http://127.0.0.1:13337` を直接起動すると、MCP initialize と
  `tools/list`（66 tools）が成功し、`server_health` は `status=ok`、module は
  `<GDB remote process>`、Hex-Rays は ready だった。
- 同じ proxy の `py_eval` で `ida_dbg.get_process_state()` は `-1`（停止中）、
  `ida_dbg.get_reg_val('PC')` は `0x00463E24`、`idaapi.dbg_read_memory(0x00100000,16)` は
  `070000eb2b7300ebf3a900eb467300eb` を返した。これは GUI 側の実機プロセスを実際に
  読めている証拠である。
- 初回の自動起動が失敗した原因は、Codex の sandbox 環境に `APPDATA` がなく、
  `ida-pro-mcp` の instance discovery (`get_instances_dir`) が `KeyError` になったこと。
  `--ida-rpc` で明示指定すれば discovery を迂回できる。

対策として、プロジェクト `.codex/config.toml` に `mcp_servers.ida_pro_mcp` を追加した。
Anaconda の `python.exe` から `ida_pro_mcp/server.py` を起動し、`--ida-rpc` で
`http://127.0.0.1:13337` を固定する。これにより次回Codex起動時は `py_eval`、
`py_exec_file`、デバッグAPIを通常のMCPサーバーとしてロードできるはずである。
現在のCodexプロセスは起動時のツール一覧を保持するため、設定反映には新規セッションまたは
Codex再起動が必要。実機・IDA GUIは再起動していない。

---

---

