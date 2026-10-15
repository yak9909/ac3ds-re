## 結果

中断。旧 FINDINGS の全 711 節を一節一記録で取り込み、再実行・索引・lint・audit を検証した。取り込めなかった節は 0 件。コミットだけ未了。Git 管理領域が書込可能なルート外にあり、`git add` は `index.lock: Permission denied` で拒否された。

## 結論と根拠の要約

対象の ID は ACNL-F0001〜ACNL-F0691、HHD-F0001〜HHD-F0020。原本 711 節と生成本文を全件照合し、公開用の伏せ字 1 箇所を除く差分は 0 件。SHA256 と伏せ字の ID・行・種類は archive/legacy-findings/sources.toml に記録した。

| 出所 | 件数 |
|---|---:|
| v1:RE/FINDINGS.md | 415 |
| IDA:work/FINDINGS.md | 223 |
| IDA:work/hhd/FINDINGS.md | 20 |
| Ghidra:work/FINDINGS.md | 53 |

| scope | 件数 |
|---|---:|
| acnl | 691 |
| hhd | 20 |

| category | 件数 |
|---|---:|
| _product | 204 |
| _triage | 336 |
| actor | 10 |
| field | 5 |
| input | 4 |
| item | 35 |
| network | 4 |
| render | 37 |
| sound | 7 |
| system | 9 |
| text | 24 |
| ui | 36 |

| confidence | 件数 |
|---|---:|
| HIGH | 434 |
| MEDIUM | 189 |
| LOW | 2 |
| 空欄 | 86 |

| by | 件数 |
|---|---:|
| unknown | 482 |
| opus-5.5 | 128 |
| gpt-sol-5.6 | 53 |
| gpt-6 | 30 |
| gpt-6.1-sol | 18 |

IDA ブランチの work/FINDINGS.md と project_v2 作業ツリーの同名ファイルはバイト一致。採用した出所は IDA ブランチ。再実行時は 711 件を既存 source と照合して更新し、件数・sources.toml は不変。`kb.py index`、`kb.py lint --strict`、`audit.py` は通過した。

## 訂正の提案

なし。本文の事実の再解析は行っていない。

## 統合・重複の提案

v1 の F-1〜F-29 と v2 IDA の V2-F001〜V2-F029 は番号が重なる 29 組の候補。対応表は v2 内の V2-F と IDA-unknown-F の対応だけを示し、v1 との同一性は示さない。番号のみでは同一記録と判断できないため、両方を残した。節本文の完全一致は 0 組。

## 新しいタグの提案

なし。

## 未確認点

_triage 336 件と製品記録の分類は機械的な暫定判定。重複候補 29 組の内容同一性も未確認。実機検証は今回の移行では行っていない。

## 次の1手

Git 管理領域に書き込める環境で `findings/`、`tools/legacy/`、`archive/legacy-findings/` をステージし、`audit.py --staged` を通してコミットする。その後、v1 と v2 の未解決対応を確認し、_triage の分類を必要に応じて個別に見直す。
