---
id: ACNL-F0748
aliases: []
title: "カブ売却価格 12 個の暗号化配列と週次生成"
summary: "カブ売却価格は全体先頭 +0x6ADE0 の 8 バイト暗号化値 12 個。8 バイト刻みの連続配列で、週次生成は暗号化 setter を使う。"
date: 2026-11-09
category: save
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA (export), IDAPython, codebytes, Unicorn
addresses: [0x00103A18, 0x001146AC, 0x00313CA0, 0x00303510, 0x005CCB5C, 0x0070B488]
tags: [save-data, player]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

`AcnlGardenSavePrefix.turnip_prices[12]` を全体先頭 +0x6ADE0 に置く。要素は `AcnlEncryptedValueF010`。
末端は +0x6AE40。曜日名・午前午後の表示順との対応は未実測。
日付更新・初期化の二経路と読み取り用の添字式を照合した MEDIUM。実機未確認。

## 根拠

- 書き出し `_local/builds/acnl_jpn_v15/export/functions/00100000/00103A18_Town_OnDayChangeLate.txt`、`001146AC_sub_1146AC.txt`、`functions/00300000/00313CA0_sub_313CA0.txt`、`00303510_sub_303510.txt`、`functions/00500000/005CCB5C_sub_5CCB5C.txt`。
- `0x103B36..0x103B40` は `Save_GetTownBase()+401872` を `0x1146AC` へ渡す。`0x1146E2..0x1146EC` はさらに +0x8B78 して `0x313CA0` で価格表を生成する。
- `Save_GetTownBase` は全体+0x80。従って生成する構造の先頭 S は `0x80 + 401872 + 0x8B78 = 0x6ADC8`。
- `0x313CB0..0x313CBC` は RNG(21)+90 を S+0 に暗号化する。これは別欄で、今回の売却価格 12 個に含めない。
- `0x313D88..0x313DA0` は 14 要素を暗号化した 0 に初期化し、`0x313DB4..0x313DC4` は先頭二期間を基準値にする、その後は `S + 8*i + 8`、`i=2..13` に価格を暗号化して入れる。12 要素の先頭は `S+0x18=0x6ADE0`。
- `0x313F9C..0x313FA4` 等の末尾条件は i<14。生成する範囲は +0x6ADE0..+0x6AE38、各 8 バイト。末端 +0x6AE40 は次のデータを含めない境界。
- `0x303510` は日番号 day<7 なら `S + 8*(half+2*day)+8` を復号し、day>=7 なら S+8 を読む。day=1..6、half=0/1 が今回の 12 個に対応する。添字の順序は `2*(day-1)+half`。この補助の直接呼出し元は書き出しの callers に無く、実際の曜日名・午前午後との対応は追加確認が必要。
- 価格を使う別経路: `0x71CE84` と `0x322214` は `Save_GetTownBase()+437576` (=S) を `0x70B488` へ渡し、先頭 S+0 の復号値×10×購入数と所持ベルを比較する。購入側が基準値を使うことを確認し、S 自体を売却配列と混同しない。
- 初期化は `0x5CA674` → `0x5CCB5C(town+401872)` → `0x313C78(+0x8B78)`。`0x313C78` は 0x80 バイトをゼロ化、価格型を初期化し、`0x313CA0` へ続く。同じ位置に表を作る独立した経路。
- `0x313CA0` は基準値・倍率から価格を生成する。参照した生成/読出し経路に「既存の売却価格が特定の最大値を超えたら拒否する」処理は見つからない。暗号化 setter の一般性から、生成範囲と任意書込み時の上限検査を同一視しない。

## 反証条件・未確認点

実機で曜日・正午をまたぐ表示との照合は未確認。配列添字と月曜午前から土曜午後までの対応は想定と整合するが、今回の根拠では確定扱いにしない。
12 個を一括して同じ値へ設定するゲーム内関数を確認したものではない。価格生成時には個別に書く。
別経路に価格の妥当性検査があるかは未確認。全体セーブの型は prefix で、全保存領域のサイズではない。
