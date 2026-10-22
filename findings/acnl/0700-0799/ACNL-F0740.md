---
id: ACNL-F0740
aliases: []
title: "パッドbit13は正常読取りで除去されコントローラー保持に転写されない"
summary: "正常なReadPadState経路はheld bit13を常に除去し、装置入力の保持転写にもbit13の対応はない。bit12は保持0x80へ転写されるが、物理ZLの実機同定は未確認である。"
date: 2026-10-22
category: input
build: acnl_jpn_v15
confidence: "MEDIUM"
tool: 全関数書き出し / codebytes / IDA型位置検査
addresses: [0x003533D0, 0x00540870]
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

パッドheldのbit13（0x2000）は正常読取りで除去され、ここで確認したcontroller保持の転写にも対応が無い。bit12（0x1000）は保持0x80へ転写される。
確度 MEDIUM。上流の除去と独立した下流の全bit転写を照合。bit12/13を物理ZL/ZRとする対応の実測は無く、特にZLの物理同定はLOWの仮説に留め、型やEnumにZL/ZR名は加えない。

## 根拠

- ReadPadState `0x0035346C..0x00353474` は `LDR R0,[R4]; BIC R0,R0,#0x2000; STR R0,[R4]`。正常読取りからここを迂回する経路はなく、その後の全体ゼロ化もbit13を立てない。
- `0x00353478..0x00353490` は除去済みheldと前回heldからedgeを生成する。初期シードなどで前回heldにbit13があれば、released bit13が一時的に現れる可能性はある。「三語すべてが必ず0」は結論に含めない。
- 後続MergeSelectIntoStartが変えるのはbit2/3で、bit13を再生成しない。
- UpdateFromDevice `0x00540914..0x00540A94` が入力として参照するのはパッドbit0..12と28..31で、bit13を使う命令は無い。
- うち `0x00540A10..0x00540A24` はpad mask 0x1000、右シフト12を条件に、controller held mask0x80を設定/消去する。
- タッチの保持bitは別途SetPointerStateから来るため、pad bit13の受け皿ではない。

## 反証条件・未確認点

物理ZL/ZRを押してpadとcontrollerを同時観測する実機検証は未実施。New 3DS固有の入力が別の装置・経路で扱われる可能性までは否定しない。
読取り失敗経路ではこのBICを実行せずに戻るので、出力バッファ単体にbit13が残る可能性はある。ただし同時にpad成功旗が偽となり、ここで確認した転写は行われない。

一次資料は `_local/evidence/109/exports/` の関数先頭アドレス別ファイル。元の全関数書き出しは symbols commit `65293c69e61e182196200b92414beff86f647a98`。対応と SHA-256 は `_local/evidence/109/manifest.json` に保存した。今回、実機操作はしていない。
