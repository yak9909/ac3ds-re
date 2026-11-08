---
id: ACNL-F0745
aliases: []
title: "8 バイト暗号化値の復号・暗号化と検査和"
summary: "8 バイト値は u32 暗号文・u16 salt・u8 rotation・u8 検査和。復号は検査和不一致なら 0、暗号化は暗号文本体を返す。検査和は salt と rotation を保護しない。"
date: 2026-11-09
category: save
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA (export), IDAPython, codebytes, Unicorn
addresses: [0x00303530, 0x00303404, 0x002FA8E8, 0x0061325C]
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

`0x303530` を `Save_DecryptValue`、`0x303404` を `Save_EncryptValue` とする。
既存 `AcnlEncryptedValueF010` を再利用する。両関数を逆向きに照合し、独立した加算・減算処理でも同じ式を確認したため MEDIUM。実機未確認。

| offset | 型 | 欄 |
|---|---|---|
| +0 | u32 | ciphertext |
| +4 | u16 | salt |
| +6 | u8 | rotation |
| +7 | u8 | checksum |

prototype は `unsigned int Save_DecryptValue(const AcnlEncryptedValueF010 *value)` と
`unsigned int Save_EncryptValue(AcnlEncryptedValueF010 *value, unsigned int plaintext)`。
暗号化の返り値は暗号文本体。値の用途による上限検査は両関数には無い。

## 根拠

- 全関数書き出し `_local/builds/acnl_jpn_v15/export/index.txt`（元 commit `4914ab98f271092df116b05c38a6183939b88b16`）、対応する `functions/00300000/00303404_vc_MONEYSET.txt`、`00303530_vc_MONEYGET.txt`、`functions/00200000/002FA8E8_sub_2FA8E8.txt`。
- `0x303410..0x303434`: RNG 補助 `0x2FF3A8` に `0x10000` と `0x1A` を渡し、返り値を +4 の半語と +6 のバイトへ保存する。補助は `0x13C924` の S0 を範囲に掛けて整数化する。`0x13C954..0x13C960` は仮数を組み込んだ 1 以上 2 未満の float から 1.0 を引くので、正常生成の rotation は 0..25。
- `0x303438..0x303450`: `plaintext + salt + 0x8F187432` を u32 で加算。`R1=0`, `R2=rotation+4` として `0x2FA8E8` へ渡す。
- `0x2FA8E8` は `R0:R1` の 64 ビット左シフト。暗号化側の直後の `ADD R0,R0,R1` は上下半分を合わせ、正常な rotation 0..25 では `ROL32(sum, rotation+4)` になる。疑似 C は R1 戻り値を取り落とすため命令列を採用した。
- `0x303454..0x303468`: `checksum = (ciphertext の 4 バイトの和 + 0xBA) & 0xFF`。+7 に保存した後も R0 は暗号文本体のまま。
- `0x303534..0x303560`: 同じ検査和と +7 を比較し、不一致なら R0=0 で返る。一致すると `0x303564..0x303584` で `ROL32(ciphertext, 28-rotation) - salt - 0x8F187432` を u32 で返す。
- `0x61325C` と `0x613308` は復号・検査和判定を別に持ち、同じ式の後に上限付き加算または下限 0 の減算を行い、`0x303404` で保存する。
- `_local/evidence/122/verify_arm.py` は `tools/codebytes.py` の読み取りを使って元 ARM を Unicorn で実行。RNG のみ置換し、salt 4 種・rotation 26 種・平文 7 種の 728 条件で式・返り値・往復・検査和破損時 0 を照合した。結果は `arm_validation.json`。エミュレーションを実機実測には数えない。
- salt を 0 から 1 に変えた例では検査和が通ったまま復号値が 99999 から 99998 へ変わった。検査和の対象は暗号文だけで、salt/rotation の改変を検出しない。
- 旧名 `vc_MONEYGET` / `vc_MONEYSET` は参考資料由来の未検証ラベルだった。金銭以外の共通暗号化値にも使われるため役割名へ変更する。この 2 番地に結論の旧記録は無く `supersedes: []`。

## 反証条件・未確認点

実機での呼出し・乱数状態の変化は未確認。破損した rotation の安全性は保証しない。
返り値 0 は正常な平文 0 と検査和不一致を区別できない。salt/rotation まで含む整合性検査ではない。
