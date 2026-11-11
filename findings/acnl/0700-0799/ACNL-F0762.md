---
id: ACNL-F0762
aliases: []
title: "fgobj の公開 Proc と view 行列、BaseMgr のプロセス表は別の大域資源である"
summary: "fgobj Procは公開/破棄で変わるポインタ、描画カメラはview行列を含むインライン実体、BaseMgrはプロセス表を持つ管理体へのポインタである。"
date: 2026-11-11
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x948e70, 0xabd380, 0x96f2a4]
tags: ["model", "camera"]
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

fgobj Procは公開/破棄で変わるポインタ、描画カメラはview行列を含むインライン実体、BaseMgrはプロセス表を持つ管理体へのポインタである。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x00948E70` | `g_FgobjProc` | `void *` |
| `0x00ABD380` | `g_FgobjRenderCamera` | `CameraViewPrefix` |
| `0x0096F2A4` | `g_BaseMgr` | `void *` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 根拠 |
|---|---|
| 0x948E70 | fgobj_Proc_Setupの先頭は0x59C974（旧資料0x59CDD0は内部のFuncNode構築付近）。Setupがthisを公開しthis+17840へFuncNodeを作る。fgobj_Proc_Destroyの先頭0x59D878は同じholderを破棄し、0x59D980で大域を0へ戻す。FieldObj_FellObject0x59A0B4が読みfgobj_DestroyObjectsAtへ渡す。完全型は無いのでvoid*。 |
| 0xABD380 | fgobj_DrawList0x59A918は `Camera_GetViewMatrix(&object,1024)` を呼び、返った12floatをコピー。0x711A8CはR1==1024ならR0+164、他ならR0+324を返す。実体の型CameraViewPrefixは+164に3x4float、+324にもう一つ、末尾372byteまでの部分型。 |
| 0x96F2A4 | 0x51FBFCは20byte×1024のプロセス表等を初期化してこの大域へthisを公開。getter0x51EE40が返す。BaseMgr_CreateProcess0x51EF38は20*slotの先頭へ生成したプロセスを保存し0x520AF4へ親子リンクを渡す。完全型は無いのでvoid*。 |

- 型の配置とサイズはevidence内で計算し、CameraViewPrefixをCameraGame/部屋カメラの既存型へ誤って割り当てない。0xABD380自体をポインタ型にしない。
- `ACNL-F0474`（S）・F0478（S）・F0519（S）・F0526（S）と整合する。F0454/F0537は格付け?なので、その実機標本だけを命名の根拠にしない。
- 旧版 `InstancedDraw.cpp:14,34,46`・`BuildingHighlight.cpp:20` と用途は一致。Setup/Destroyの記載番地は内部命令であり、上記が全関数書き出しの開始番地。カメラの意味はfgobj描画に使う範囲に限定した。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- カメラ実体の完全クラス/全体サイズは未確定。prefixの372byteを全体サイズとして使わない。Procやheapの場面間の寿命、複数描画の実機結果は追試していない。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
