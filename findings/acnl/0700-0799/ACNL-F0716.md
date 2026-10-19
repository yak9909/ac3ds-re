---
id: ACNL-F0716
aliases: []
title: "PaneとMaterialのアニメーションリンク番兵"
summary: "Pane+0x20/+0x24とMaterial+0x08/+0x0Cはアニメーションリンクリストの循環番兵であり、その直前のwordは件数である。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # 静的な生産側と独立した消費側。実機なし
tool: IDA
addresses: [0x004B6B58, 0x004BCEA8, 0x004B6014, 0x004BCE2C, 0x004BDCB4, 0x004BDC44]
tags: ["layout"]
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

`NwLytAnimationLinkList {u32 count; NwLytPaneLink sentinel;}` をPane+1CとMaterial+4へ適用した。空リストの番兵アドレスはPane+20、Material+8。これは子Paneの番兵とは別である。確度 MEDIUM：二つのctor、独立した評価と解除/検索が一致。実機なし。

実リンクは0x10バイトの `NwLytAnimationLink`。+0/+4は次/前、+8は `NwLytAnimTransform *`、+Cはtarget_index(u16)、+Eはdisabled(u8)、+Fは未知。番兵にはリンク本体の後半8Bは存在せず、8Bのlinkとして保持する。AnimTransformは不透明型であり全体サイズを定義しない。

## 根拠

- `_local/builds/acnl_jpn_v15/ida/work/100/primary.txt` の0x4B6B58はPane+1Cを0、+20/+24をPane+20へ設定。0x4BCEA8はMaterial+4を0、+8/+CをMaterial+8へ設定。
- Pane評価0x4B6014は+20から巡回し、番兵+20で止まる。link+Eが0ならtransformのvslot+8を `(transform,target_index,pane)` で呼ぶ。
- Material評価0x4BCE2Cは+8から同じ形で巡回し、transform vslot+Cを `(transform,target_index,material)` で呼ぶ。両評価関数と関連vtable slotへ型を付けた。
- 0x4BCCBCはMaterial+4、0x4BDC44はPane+1CをAnimationLinkList_Unbindへ渡す。0x4BDCB4はtransform一致（nullなら全リンク）を選び、0x13756Cが次/前を繋ぎ直し、list先頭wordを減算。解除後はtransform・target_index・disabledを0にする。
- 0x4BDBA0の検索はlink+8を指定transformと比較し、見つかったリンク又はnullを返す。0x4B6738の有効化はlink+Eへenabled^1を書き、評価のゼロ条件と一致する。

## 反証条件・未確認点

- Link+F、AnimTransform全体、別のリスト型の全ABIは未確認。汎用のNwLytPaneLinkを8Bリンクの表現に再利用するが、アニメーションリンクが子Paneを指す意味ではない。
- 動的にバインドされた全インスタンスの実測は行っていない。
