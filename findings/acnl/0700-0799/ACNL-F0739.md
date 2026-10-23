---
id: ACNL-F0739
aliases: []
title: "装置パッドの読取りは成功旗に従いボタンとタッチを別々に更新する"
summary: "装置入力はpad成功bit0が真の時だけpadのheldとcircle_x/yを読み、padのedge語は読まない。touch成功bit1は独立であり、bit0が偽でもSetPointerStateが保持内pointer bitを変更し得る。"
date: 2026-10-22
category: input
build: acnl_jpn_v15
confidence: "MEDIUM"
tool: 全関数書き出し / codebytes / IDA型位置検査
addresses: [0x00540870, 0x0053F550, 0x00542D78]
tags: ["button", "touch", "sead"]
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

`sead_CtrController_UpdateFromDevice` は、装置 `+0x1634` のbit0に従ってパッドのボタン・軸を更新し、bit1に従ってタッチを独立に更新する。bit0偽を「held全体が更新されない」と一般化できない。
確度 MEDIUM。装置更新の成功旗の書込み、controllerの読取り分岐、SetPointerStateのheld書込みという独立した静的根拠。実機未確認。

## 根拠

- `0x0053F560..0x0053F568` は装置 `+0x15C0` をReadPadStateへ渡し、`0x0053F56C..0x0053F58C` で装置 `+0x1400+0x234` のbit0を成否で更新する。
- タッチ出力は `0x0053F57C..0x0053F598` の装置 `+0x1400+0x1D4`。`0x0053F59C..0x0053F5B4` は読取り成否を同旗bit1へ更新する。
- `0x005408F0..0x00540900` は装置 `+0x1634` を読み、bit0偽なら `0x00540ACC` へ飛ぶ。ボタン転写・軸書込み `0x00540904..0x00540AC8` は飛ばされる。
- 真の時だけ `0x00540904 ADD R1,R5,#0x15C0`、`0x0054090C LDR R0,[R1]` でheldを取得。`0x00540A98 LDRSH R0,[R1,#0xE]` と `0x00540A9C LDRSH R3,[R1,#0xC]` が軸を読む。同関数にpad `+4/+8` のpressed/released読取りはない。
- `0x00540ACC..0x00540AD4` は独立に旗bit1を検査し、真なら `0x00540AD8..0x00540B1C` で装置 `+0x15D4` のuint16 X/Yと `+4` の接触byteを読み、`SetPointerState(controller, contact==1, 1, pixels)` を呼ぶ。
- SetPointerState `0x00542E08..0x00542E48` はpointer_flags bit0だけでなく `controller+0x108` の番号を使って `held=controller+0x110` のpointer bitも更新する。
- よってbit0偽・bit1真なら、ボタン・軸は前値でもpointerの保持bitは変わり得る。bit1偽ならこのタッチ更新も飛ぶ。装置が見つからない経路も全体を飛ぶ。

全関数の命令オペランドを `#0x15C0/15C4/15C8/15CC/15CE/15D4/15D8/1634` で検索した結果を `_local/evidence/109/device_direct_offsets.txt` に保存した。padキャッシュを直接指す候補は書き手0x0053F550と読み手0x00540870で、他の0x15C0一致は別オブジェクトだった。タッチは分割加算も別途照合した。検索した形式の範囲で、装置pad/touchキャッシュの読み手として確認できたのは同関数だけである。

## 反証条件・未確認点

定数の別の組合せ・別名ポインター・計算された添字・間接呼出しによる別の読み手はこの検索で網羅しない。「全ゲームの読取りがこの1関数だけ」とは断定しない。
読取り失敗の頻度・実機での前値残留・場面別の挙動は未測定。旗bit0とbit1の独立性に反する別のwriterがあれば追加照合が必要。

一次資料は `_local/evidence/109/exports/` の関数先頭アドレス別ファイル。元の全関数書き出しは symbols commit `65293c69e61e182196200b92414beff86f647a98`。対応と SHA-256 は `_local/evidence/109/manifest.json` に保存した。今回、実機操作はしていない。
