---
id: ACNL-F0709
aliases: []
title: "GPU コマンドリストの生成・領域確保・削除と引数型"
summary: "GPU コマンドリストの生成は件数と出力ID配列、領域確保は選択中リストのコマンドバイト数とGX容量、削除は件数とID配列を受け取る。SelectList の入力はID一つで、Propertyの結果は出力配列に書かれる。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x00121B34, 0x00121988, 0x00127D98, 0x00127EDC, 0x001216BC]
tags: ["layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

上記5関数へ引数型を付け、未命名3関数を `GpuCmd_CreateLists`、`GpuCmd_AllocateListStorage`、`GpuCmd_DestroyLists` と命名した。公開SDKとの同一性を断定する名前ではなく、ゲームの生産・消費の役割に基づく解析名である。
確度 MEDIUM：各本体の命令と、独立した Layout Build・破棄・主リスト初期化が整合。実機なし。

| 番地 | 宣言の要点 |
|---|---|
| 0x00121B34 | `void (int count, unsigned int *ids)`。1本に限定せずcount本を生成 |
| 0x00121988 | `void (unsigned int command_bytes, int gx_capacity)`。現在選択中の領域を確保し直す |
| 0x00127D98 | `void (int count, const unsigned int *ids)` |
| 0x00127EDC | `void (unsigned int property, unsigned int *output)` |
| 0x001216BC | `void (unsigned int id)`。疑似Cのa2/a3は入力ではない |

戻りレジスタに残るアドレス等は分岐により異なり、戻り値として扱わない型にした。

## 根拠

一次証拠：`_local/evidence/98/primary.txt` の各関数全文、`primary-index.json` の原本code.bin範囲ハッシュ。書き出しの基点は commit `65293c69e61e182196200b92414beff86f647a98`、現在の名前は symbols と照合した。

- 生成 `0x121B3C/40` がR1=出力配列、R0=符号付き件数を保存。`0x121B68..78` はcallbackへheaderサイズ0x44を渡し、`0x121BBC` 等が `ids[index]` を書く。`0x121C44..50` はcountまで反復する。Layout Build `0x568620` はcount=1とLayout+0x100を渡す。既存 [ACNL-F0700] の寿命・ID0例外をそのまま適用する。
- storage `0x1219E0..F4` が `command_bytes + 28*gx_capacity` を確保。`0x1219FC` にコマンド容量、`0x121A18` にbase、`0x121A1C..2C` にGX領域と容量を保存する。Layout Build `0x568630..38` は第4引数と1を渡す。主リストの `0x4E9818..30` も生成→選択→同じstorage。容量の解釈は [ACNL-F0701] と一致する。
- 削除 `0x127D98` はR0を件数として保存し、R1の配列からIDを読み、bucketから外してstorage/headerを解放する。ID0はスキップする。Layout破棄で非ゼロIDを渡すことは [ACNL-F0700] に独立した命令根拠がある。
- 選択 `0x1216BC` の入口で意味を持つ入力はR0のみ。後のR2は本体で定義され、疑似Cに残るa2/a3は呼出し契約に入れない。旧offsetの保存と新cursor/endの復元は [ACNL-F0701]。
- Property `0x127EDC` はR0から0x200を引いて分岐しR1の先へ書く。0x202はcursor-baseを保存、0x208はlive cursor。0x20Dは条件付きで2語を書くためoutputは単語1個に限定しない。範囲外・不成立caseで出力が更新されるとは限らない。

## 反証条件・未確認点

- 実行時の容量不足、callback失敗、GPU完了時点は未測定。生成headerの確保失敗を安全に扱えるとは確認していない。
- 呼出し元が意味のある戻り値を消費する別経路が確認された場合はvoid型を再検討する。propertyの全定数にEnum名を推定追加していない。
