---
id: ACNL-F0742
aliases: []
title: "保持0x800はSTARTでありSELECTは読み替え前なら0x1000へ転写される"
summary: "装置入力はpad START bit3を保持0x800、SELECT bit2を保持0x1000へ別々に転写する。SELECT統合後の装置キャッシュはSTART bit3になり、旧記録のSELECT=0x800という観測を説明できる。"
date: 2026-10-22
category: input
build: acnl_jpn_v15
confidence: "MEDIUM"
tool: 全関数書き出し / codebytes / IDA型位置検査
addresses: [0x003533D0, 0x00483020, 0x00540870, 0x0053F550]
tags: ["button", "sead"]
supersedes: ["ACNL-F0379"]
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

ACNL-F0379の「SELECTは保持0x800、0x1000はSTARTと推定」という**ボタンの同定を訂正する**。転写自体はpad0x8→held0x800、pad0x4→held0x1000であり、既存ACNL-F0721/0723と一致する。入力上のSTART/SELECT対応ではSTART=0x800、読み替え前のSELECT=0x1000となる。
確度 MEDIUM。上流の条件付きSELECT統合と下流の独立したbit転写を照合。今回の実機測定は無く、旧実測の条件は再現していない。

## 根拠

- UpdateFromDevice `0x00540938 AND R2,R0,#8`、`0x0054093C MOVS R2,R2,LSR#3`、`0x00540944 ORRNE R2,R2,#0x800`、`0x00540948 BICEQ R2,R2,#0x800`、`0x0054094C STR ...held`。
- 同関数 `0x00540A28 AND R2,R0,#4`、`0x00540A2C MOVS R2,R2,LSR#2`、`0x00540A34 ORRNE ...#0x1000`、`0x00540A38 BICEQ ...#0x1000`、`0x00540A3C STR ...held`。
- 上流のMergeSelectIntoStart `0x004830AC..0x004830C0` はpad heldのbit2が立っていればbit2を消してbit3を立てる。ReadPadState `0x003534D0..0x003534E0` はbyte0x009778D8が0の時だけこの関数を呼ぶ。呼出し元は既に装置 `+0x15C0` 自体を出力先としている。
- 従って読み替え実行時のSELECT単独は `pad0x4 → pad0x8 → controller0x800`。読み替え無しなら `pad0x4 → controller0x1000`。物理START相当のpad0x8はどちらでもcontroller0x800へ来る。
- ACNL-F0379の測定箇所は装置 `+0x15C0` であり、同記録の「SELECT時に0x8」は**読み替え後のキャッシュ**の観測と整合する。「生HIDがbit3を出す」「nn::hidはSELECT/STARTが逆」とする根拠にはならない。
- 数値の転写は当該命令列から直接確定する。入力ボタンの名称とbit2/3の関係はACNL-F0723（格付けA、独立した静的解析と元ARMの状態遷移照合）を併せて根拠にし、旧記録?だけを採用していない。

## 反証条件・未確認点

旧測定が実際にどのglobal byte値・時点・パッチ状態だったかは不明で、「読み替え後を測った」は静的経路からの説明であり再現実測ではない。旧記録の実測値0x8そのものや利用者の報告を否定していない。
実機で読み替え前pad・装置キャッシュ・controller heldを同時に観測すれば物理ボタン名まで独立に検証できる。別ビルドのbit配置は未確認。

一次資料は `_local/evidence/109/exports/` の関数先頭アドレス別ファイル。元の全関数書き出しは symbols commit `65293c69e61e182196200b92414beff86f647a98`。対応と SHA-256 は `_local/evidence/109/manifest.json` に保存した。今回、実機操作はしていない。
