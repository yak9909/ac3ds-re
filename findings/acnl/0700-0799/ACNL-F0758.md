---
id: ACNL-F0758
aliases: []
title: "タブ復帰で呼ぶ3関数は音の再開ではなくメニューフローの完了確認と通知"
summary: "0x316E7Cは現在のメニューフロー要求の種別を検査する。0x52B678と0x52B644は種別7/13の要求の状態バイトへ1を書き、対応する処理の完了を通知する。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x316e7c, 0x52b678, 0x52b644]
tags: ["menu"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x316E7Cは現在のメニューフロー要求の種別を検査する。0x52B678と0x52B644は種別7/13の要求の状態バイトへ1を書き、対応する処理の完了を通知する。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x00316E7C` | `MenuFlow_IsCurrentKind` | `bool f(unsigned int kind, bool require_running);` |
| `0x0052B678` | `MenuFlow_SignalKind7Complete` | `bool f(void);` |
| `0x0052B644` | `MenuFlow_SignalKind13Complete` | `bool f(void);` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 根拠 |
|---|---|
| 0x316E7C | 0x94B6B8の現在要求を読む。NULLはfalse。R1が非ゼロなら+24==3かつ+26!=2を要求。その後R0==14なら任意の存在中要求をtrue、それ以外は+25と比較。 |
| 0x52B678 | 0x52B684で(7,0)を上記へ渡し、trueなら0x52B69CのSTRBでcurrent+0x1Aへ1を書きtrueを返す。 |
| 0x52B644 | 0x52B650で(13,0)、trueなら0x52B66Cで同じ+0x1Aへ1。 |

- タブ側の独立した利用者 `0x6D67F0` は7/13の順で調べ該当する通知関数を呼ぶ。`0x6D68A0` も7の通知を呼ぶ。
- 要求管理の生産側 `0x52AEBC` はpool/list0x9A5150から条件成立の要求を取り外して0x94B6B8へ公開し、+24=2にする。`0x52ADCC→0x52CA2C→0x52C930` がphase2→3→4→削除を進める。表0x8584FCは種別ごとに4関数。
- 原本の表でkind7の処理群は0x165B40/0x16571C/0x189ABC/0x189428、kind13は0x165B10/0x16570C/0x189AAC/0x189424。0x165B40はMenu_IsIdleAndEmpty待ちの後Menu_RequestOpenを呼ぶ。calc0x189ABC/0x189AACはともにrequest+26==1を返す。その結果を0x52CA2Cがphase4移行へ使う。
- 旧版 `GameList.cpp:742,756` の「音の状態・音の再開A/B」は命令列と一致しない。今回の3関数は音APIを呼ばず、メニューフローの要求レコードを判定/更新する。最終的なゲーム効果が完了通知以外にも及ぶ可能性は否定しない。
- 7/13のゲーム内名称は未確定なので、名前には確定したkind番号と完了通知だけを入れる。14は「要求無し」を返す値ではなく、存在している任意要求に一致する。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- メニューフロー全14種の意味や音側への間接効果は未追跡。3関数の実測は無い。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
