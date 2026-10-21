---
id: ACNL-F0736
aliases: []
title: "手紙停止標本の空きと使用中合計、所有量の逆算条件"
summary: "2026-10-21の手紙停止ログはUI heapのfree 61,924 B、used 3,725,592 B/4,819塊を記す。コピー先nullは実装と一致するが、別領域の空きや全usedの分類はこのログから得られない。"
date: 2026-10-21
category: system
build: acnl_jpn_v15
confidence: MEDIUM
tool: "全関数export・実RomFS・提供停止ログ・公開ソース"
addresses: [0x002FBB8C, 0x001FC55C, 0x0096F150, 0x00569B54]
tags: ["heap", "layout"]
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

追加提供された停止時観測は、便箋の別画像の確保失敗後にnullへコピーしている命令と一致する。UI heapの大きな消費は確認できるが、観測ログは全メモリダンプではなく、各塊の所有者や他heapの空きは確定しない。
確度MEDIUM：提供された実機観測の転記と、画像作成/コピー命令を照合。元の全ノード/バイトの再読取りはしていないため、今回採取のHIGH測定とはしない。

## 根拠

一次資料 `_local/evidence/107/device-2026-10-21.txt`（利用者提供の停止時観測、停止版main 1a09557）。SHA256/来歴は `resume-materials.json`。

- PC=0x2FBBA4（Mem_Copy内STM）、R0=0、R1=0x32FC6D20、R2=0x1FFE0、LR=0x1FC68C。`0x1FC688` のコピー呼出しと一致し、F0727の画像payload要求は131,072 B。
- `g_LayoutAllocator [0x96F150]=0x32C46020`、heap=0x32C45F78。
- freeは1塊61,924 B。usedは4,819塊、payload合計3,725,592 B。大きい塊の例511,528 / 208,296 / 198,784 / 131,456 / 101,928 / 98,944 B。131,456 Bの0x32FC6B54はletter_shic.bcresと報告されている。
- used合計+free合計+16 B×全4,820塊=3,864,636 B。heap作成引数3,866,624 Bとの差1,988 Bはheap本体/整列等が含まれ得るが、全ダンプ無しに配賦しない。
- 198,784+98,944=297,728 Bを自作部分とするのはログ作者の**所有推定**。これを仮定したゲームのused payloadは3,427,864 B。従前の「3.37 MB」を別の正確な実測値として採用しない。
- 61,924+297,728−131,072=228,580 Bは所有推定とpayloadのみの逆算。未確保画像のallocator要求は `0x569B54` によりさらに128 B増え、ExpHeap header/整列も関係する。実際の便箋後空きを再測定した値ではない。

## 反証条件・未確認点

2塊のどちらかが別所有なら逆算予算も変わる。最大raw塊とalignment込みの最大確保量は同一でない。静止画資源/文字器/Pane/arc/管理費の全件分類、graphicHeap、VRAM A/B、確保前後の差は未採取。
