---
id: ACNL-F0738
aliases: []
title: "パッド履歴保存前の共通境界は全体ゼロ化の合流後にある"
summary: "0x003534C8は成功経路の全体ゼロ化分岐が合流した後、読み替え前heldの履歴保存と条件付きSELECT統合の前にある。LDR R0,[R4]自体は無条件・非PC相対だが、既にゼロ化された値を読む場合がある。"
date: 2026-10-22
category: input
build: acnl_jpn_v15
confidence: "MEDIUM"
tool: 全関数書き出し / codebytes / IDA型位置検査
addresses: [0x003533D0, 0x009778D8]
tags: ["button", "sead"]
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

`0x003534C8` は正常読取り経路の共通点で、`0x003534CC` の履歴保存前・`0x009778D8` の条件判定前にある。ただし合流するのは**パッド全体ゼロ化の有無の分岐**であり、SELECT読み替えの二経路ではない。読み替え自体はこの後にある。
確度 MEDIUM。ReadPadStateの制御フローと呼出し先MergeSelectIntoStart、呼出し元の成功判定を独立に照合し、codebytesの命令バイトも確認。実機未確認。

## 根拠

- `0x003533D4 MOV R5,R0`、`0x003533E0 MOV R4,R1`: R5がreader、R4がpad出力。
- `0x00353494..0x003534B0` の条件により、直接 `0x003534C8` へ進むか、`0x003534B4..0x003534C4` でheld・pressed・released・circle_x/yを全て0にしてから合流する。
- `0x003534C8 LDR R0,[R4]`（元バイト `00 00 94 E5`）、`0x003534CC STR R0,[R5,#8]`: その時点の読み替え前heldをreaderの前回保持へ保存する。全体ゼロ化を通れば保存値も0。
- `0x003534D0 LDR R0,=byte_9778D8`（`24 00 9F E5`）はPC相対literal load。`0x003534D4 LDRB`、`0x003534D8 CMP #0`、`0x003534E0 BLEQ 0x00483020` の順。
- MergeSelectIntoStart `0x004830AC..0x004830C0` がheldのSELECTをSTARTへ変換するので、C8はその前である。
- 成功経路は `0x003534E8 MOV R0,#1`。事前の失敗分岐は `0x003534F0..0x003534F8` へ直接戻り、C8を通らない。呼出し元 `0x0053F574..0x0053F58C` はこの成否を装置旗bit0へ反映する。
- codebytesの結果は `_local/evidence/109/codebytes.txt`。C8はR4基準の無条件命令で、D0と異なりPC相対データ参照はない。

ACNL-F0723のD0は共通点として正しいが、C8にも共通点があり、こちらは履歴保存前かつ非PC相対であるという補足になる。既存記録の書換えはしない。

## 反証条件・未確認点

ゲーム側の命令属性の確認に限る。CTRPF標準Hookの移設・実行順・実機での動作は今回確認していない。
この地点のheldを「生HIDのまま」と呼ぶのは不正確。bit13除去、再計算、条件による全体ゼロ化が済んでいる。0x009778D8の意味・書き手は未追跡。

一次資料は `_local/evidence/109/exports/` の関数先頭アドレス別ファイル。元の全関数書き出しは symbols commit `65293c69e61e182196200b92414beff86f647a98`。対応と SHA-256 は `_local/evidence/109/manifest.json` に保存した。今回、実機操作はしていない。
