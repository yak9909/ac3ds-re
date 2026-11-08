---
id: ACNL-F0747
aliases: []
title: "所持金・貯金・メダル・ふるさとチケットのセーブ欄と加算上限"
summary: "プレイヤーセーブ +0x6F08/+0x6B8C/+0x6B9C/+0x8D1C は所持金/貯金/メダル/ふるさとチケットの 8 バイト値。確認した上限は所持金 99999、貯金 999999999、メダル・チケットの加算 99999。"
date: 2026-11-09
category: save
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA (export), IDAPython, codebytes, Unicorn
addresses: [0x001AD9A8, 0x002C0178, 0x00305A6C, 0x006BD258, 0x006BC478, 0x006CC4D8, 0x0062FD58, 0x006BCBF4]
tags: [save-data, player]
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

`AcnlPlayerSave` に下表の欄を作る。読み手と書き手、および別の初期化処理を照合した MEDIUM。実機未確認。
上限は確認したゲーム内の操作経路の検査値であり、共通暗号化 setter 自体の制約ではない。

| offset | 欄 | 意味 | 確認した上限と処理 |
|---|---|---|---|
| +0x6B8C | bank | 貯金 | 999999999: `0x305A6C` → `0x61325C` |
| +0x6B9C | medals | 島のメダル | 加算 99999: `0x6BD258` → `0x61325C` |
| +0x6F08 | wallet | 所持金 | 99999: `0x2C0178`、`0x2BFF9C` |
| +0x8D1C | meow_coupons | ふるさとチケット | 加算 99999: `0x6BC478`、`0x2B87BC` → `0x61325C` |

欄の型はいずれも `AcnlEncryptedValueF010` (8 バイト)。ほかは `unk_<offset>` の詰め物とする。
既存の `AcnlPlayerInventoryFinanceF010` は既存 prototype の互換性のため残す。本記録で、その pocket/storage/loan 等を新たに保証はしない。

## 根拠

- 全関数書き出し `_local/builds/acnl_jpn_v15/export/` の以下の番地の ARM と疑似 C を照合。
- `BellBox_SetKind 0x1AD9A8` の `0x1AD9D0..0x1ADA60` は [0xAA914C] から kind0 で +0x6F08、kind2 で +0x6B9C、kind4 で +0x8D1C を復号する。`0x29546C` の値更新にも同じ kind 分岐と offset がある。これは三つが別の表示通貨である根拠。
- 所持金: `0x19AE60` はベル袋の金額 (`vc_GETMONEYFUNC`) を現在の所持金へ加え、持ち物先頭 player+0x6BD0 を `0x2C0178` に渡す。`0x2C0178` は inventory+824、すなわち player+0x6F08 に `min(amount,99999)` を保存し、余りを返す。
- `0x2BFF9C` は同じ +824 の財布と category2 のベル袋をまとめ、空き枠へ袋を戻した後の財布を 99999 以下へ収める。`0x2C01BC` は同じ値から支払う。
- 貯金: `Player_UpdateBankRewardsAndInterest 0x62FD58` は player+0x6B8C を復号し、`Mail_SP_Postoffice` の貯金報酬と月利 0.005 の計算に使う。`0x630064` は `0x305A6C` で利息を加算。
- `0x305A6C..0x305A78` は player+0x6800+0x38C と上限 `0x3B9AC9FF` を `0x61325C` へ渡す。ATM の `0x6CC4D8` は財布からの預け入れに同じ補助を呼び、逆操作では `0x6132FC` で貯金から減らして財布へ戻す。入力上限も `0x6CCEBC` で残り容量を検査する。
- メダル: `0x6BD258..0x6BD264` は player+0x6800+0x39C、上限 `0x1869F` を加算補助へ渡す。独立した `0x6BD318` は同じ欄から減算する。表示元は BellBox kind2。初期化 `0x6BCD90` / `0x6BD4E0` も貯金・借金とは別の +0x6B9C を暗号化した 0 にする。
- チケット: `0x6BC478..0x6BC4AC` は +0x8D1C の未回収分を `0x2BF41C` でまとめ、player+0x8AE0 から算出した報酬を上限 `0x1869F` で加算する。`0x2B87BC` にも同じ欄・同じ加算上限がある。`0x6BCBF4` は新規初期化で 10 を付与する。
- `0x1E4D48` は kind5 の交換処理でこの残高を価格と比較し、成功時 `0x613308(player+0x8D1C,price)` で支払う。ATM の `0x6CC4D8` case59 は同じチケットを減らし、枚数×3000 を貯金へ移す。kind4 の表示と、収入・支出・別通貨への交換が同じ欄を参照する。
- `0x61325C` は unsigned の 64 ビット加算結果を cap と比較し、繰り上がり時も cap に収める。`0x613308` は下限 0 の減算。式と境界の ARM 実行検証は ACNL-F0745 および `_local/evidence/122/arm_validation.json`。
- 旧資料のメダル/チケット 9999 は上の加算命令の 99999 と一致しない。今回の結論は一次命令列から得たもの。ACNL-F0420 の欄距離の記述は整合するが、格付け ? のため根拠には使用しない。

## 反証条件・未確認点

99999 は確認した加算経路の値。別経路や UI の桁数が 9999 に制限する可能性を排除しない。
共通 setter は任意の u32 を暗号化し、復号関数も用途別の上限検査は行わない。
実機での表示桁数、メダル・チケットの極端な値とセーブ再読込みは未確認。
