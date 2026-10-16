---
id: ACNL-F0703
aliases: []
title: "loader ID の十進10と0x10は異なり、旧bucket照合は0x0Aを指す（再解析）"
summary: "0xAD9904はID 10（0x0A）のbucketであり、ID 0x10は0xAD991Cを使う。F0261の同ID・同managerという照合は成立しない。"
date: 2026-10-16
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x1216bc, 0xad98c0, 0x5685a4, 0x845fd8]
tags: [layout]
supersedes: ["ACNL-F0261"]
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

再解析で確認。十進10は `0x0A` であり `0x10` とは異なる。`GpuCmd_SelectList` の命令式で **ID `0x0A` のbucketは `0x00AD9904`、ID `0x10` のbucketは `0x00AD991C`** になる。F0259が挙げた前者を、F0261で「ID 0x10 のbucket」とした箇所は誤り。

確度 MEDIUM：bucket算出とexact-ID比較の二段の命令、独立したBuild→可変ID生成 [ACNL-F0700] が整合する。旧標本の実IDを今回読み出したわけではない。

## 根拠

一次証拠：`_local/evidence/26/ida-final-evidence.txt`（命令・計算結果）、`ida-primary.txt`。

- `0x1216C0` は要求IDをR5へ保持。`0x1216C4 AND R0,R0,#0x1F`、`0x1216C8` はbase=`0xAD98C0`、`0x1216CC ADD R7,R6,R0,LSL#2`、`0x1216D0 LDR R4,[R7,#0x1C]`。
- `0x1216DC/E0/E4` は `manager+0` とR5を等値比較し、一致しなければ `0x1216E8` がmanager `+0x40`を辿る。下位5bitが同じでも同一IDとは扱わない。今回の二つはbucket自体が違う。
- ツールによる計算：

```python
bucket = lambda i: 0xAD98C0 + ((i & 0x1F) << 2) + 0x1C
hex(10)       # 0xa
bucket(10)    # 0xad9904
bucket(0x10)  # 0xad991c
```

- F0259のtrace/本文の十進10、F0261冒頭の `0x08→0x0A`、bucket=`0xAD9904` は数値として整合する。F0261後半で同じ旧Layout `0x3225A2B4`を `id 0x10`とした記述は、その整合する組と矛盾する。
- Build `0x5685A4`→`0x121B34` はIDを生成する [ACNL-F0700]。Fadeもloaderも固定IDを引数で渡して生成していない。画像の種類欄 `BlackWait+0xA12`、描画display `Layout+0x134`、記録ID `Layout+0x100` は別物である。

## 主張ごとの判定・訂正

| F0261の主張 | 判定 | 再解析の結果 |
|---|---|---|
| F0259の10と0x0Aは同じ | 確認 | 数値変換・bucket計算が一致 |
| 0xAD9904はID 0x10のbucket | 反証 | 0x10は0xAD991C。0xAD9904は0x0A |
| F0259のloader `0x3225A2B4` はID 0x10 | 反証 | F0259の値の引用としては誤記。原記録自身は10/0x0Aとする |
| `0x3225B070` は本当にID 0x10だった | 一部訂正 | 旧生バイトを今回取得していない。0x0Aへの一括置換もできない。別個体のID0x10だった可能性を残す |
| ゼロ長nodeと非ゼロmanagerが同じIDだった | 一部訂正 | bucketの誤同定があるため未証明。manager先頭のexact IDとLayout+0x100を同一標本で読む必要がある |
| 0x400と0x410は異なる画像フェーズの証拠 | 一部訂正 | [ACNL-F0693]では上左右目のdisplay。画像種類や状態遷移の同定根拠にはしない |
| list id／固定heapポインタだけで現在の画像源は決まらない | 確認 | ID生成・解放・再利用 [ACNL-F0700] と、状態別の資源選択 [ACNL-F0702] による。旧同ID衝突標本を根拠には数えない |
| 二停止標本・no-drawのcalls=0x5D/reorder=0は複数フェーズの実証 | 一部訂正 | 旧計測コードと実行値は未追試。状態の複数性は[ACNL-F0702]の状態表から独立に確認。各標本への対応付けは未確認 |
| manager検索・切替の静的契約 | 確認 | exact ID検索、旧offset保存、新base+offset復元は命令で確認。[ACNL-F0701]とも一致 |
| ゼロ長ならGPU処理全部が止まる／旧nodeは表示中の直接画像源でない | 一部訂正 | [ACNL-F0704]。シザー発行は残り、停止時の長さから過去の提出元は排除できない |

訂正：採用する表記は「F0259の旧loader IDは十進10（0x0A）」。「F0261の旧current nodeの実ID」は未確認として残し、「両者は同ID」という結論を撤回する。これはLayout非一意性を理由に数値の矛盾を解消するものではない。

F0261全体のゲーム側結論は本記録・[ACNL-F0702]・[ACNL-F0704]で置き換えるためsupersedesに入れた。旧記録は変更していない。

## 反証条件・未確認点

- 旧停止標本の元ログ・生バイトを再採取していないため、0x10が単なる十進表記への誤った接頭辞か、別nodeの実値かは決められない。静的に決着したのは二つのIDとbucketが別物であること、および「同IDを照合した」という推論の不成立である。
- 実機で確認する場合、Layout pointer/+0x100、bucket pointer、manager先頭ID/base/size/offset、display、時刻を同じ標本に残す。画像源はさらに記録・再生・提出との対応で確かめる。
