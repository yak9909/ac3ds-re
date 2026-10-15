---
id: ACNL-F0033
aliases:
- F-144
title: 'F-144: 会話 TextBox も batch writer 経路 — `HIGH`（静的＋実機）'
summary: 会話表示中に `0x4BAFFC`（`sub_4BAFB0` 内の `sub_7E7F48` 呼出し）へ software
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4960252
- 4947168
- 7589704
- 5066412
- 5067276
- 4960176
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:438-483
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-144: 会話 TextBox も batch writer 経路 — `HIGH`（静的＋実機）

会話表示中に `0x4BAFFC`（`sub_4BAFB0` 内の `sub_7E7F48` 呼出し）へ software
breakpoint を置いて採取した。停止時の register/string/pane identity が会話名 TextBox
そのものだったことが対象の根拠であり、breakpoint condition は根拠に含めない。
後の再起動セッションでは、非定数の条件式は IDA 上で `compiled=True` でも偽の時計
TextBox で停止した一方、定数 `0` は停止しなかった。Luma GDB stub の software-BP
step-over 制約と条件評価の組合せは信頼できないため、対象選別にはゲーム内トレースケーブを使う。
停止時の実値は次の通り。

| 項目 | 実値 |
|---|---:|
| TextBox (`R4`) | `0x32D20220` |
| UTF-16 pointer (`R1`) | `0x32D22FB0` |
| UTF-16 (`R1`) | `あんこ` |
| length (`R2`) | `3` |
| local TextWriter (`SP`) | `0x0FFFFCC0` |
| ResFont (`writer+0x3C`) | `0x3302ABE0` (17×24) |
| immediate context (`writer+0x40`) | `0` |
| batch buffer (`writer+0x44`) | `0x32D22FD8` |
| batch capacity (`+0`) | `9` |
| batch count直前 (`+4`) | `0` |
| TextBox pane width | `96.0f` |
| TextBox font size | `18.0f × 24.0f` |

続く `0x4B7CE0` 入口も同じ会話フレームで捕捉した。`R0=0x32FF62EC`（描画補助）、
`R1=0x327DEA78`（GPUコマンド書込み位置）、`R2=0x32D20220`（TextBox）、
`R3=0x32D2033C`（material）、stack引数=`0x330A605C` で、batch は
`+4` の glyph count=3、`+0x1C` の生成済み command dword count=`0xB6`（728 bytes）
になっていた。これは `sub_4D6570` が glyph instance から batch command stream を組み立て、
`0x4B7CE0` がそれを command bufferへ取り込む直前の値である。

静的には `0x73CF48` → `sub_4BAFB0` → `sub_7E7F48` → `0x4D4EAC` →
`sub_4B7CE0` → `sub_4D520C` の順で、`0x4B7CE0` が `TextBox+0x104` の batch
カウントを検査し、`0x4D520C` が batch descriptor/instance を GPU コマンド列へ
コピーする。会話実測でも `writer+0x40==0` / `+0x44!=0` なので、会話経路で
immediate 描画へ強制するのは null context 参照になり危険である。

この結果は「glyph instance の生成」と「GPU コマンド列への batch 取り込み」までを
裏付けた。後段のcommand-list接続は F-145 で追跡した。atlas handle materialize の時点は
引き続き未観測である。

**根拠**: `0x4BAFFC` 停止時の PC/register、TextBox/string/writer/batch の停止中メモリ、
`0x73CF48`/`0x4BAFB0`/`0x4B7CE0`/`0x4D520C` の `code.bin.i64` 静的命令列。
取得スクリプトは停止前にBPを削除しており、ゲームメモリへの書込みは行っていない。

