---
id: ACNL-F0714
aliases: []
title: "Layoutの仮想関数型と視点・アニメーション・再生状態欄"
summary: "Layoutのvptrと7slotの仮想表型を付けた。+0xF8は視点Z、+0xFCはアニメーションflags、+0x114は再生状態マスク、+0x118はコマンドのバイト容量である。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # 静的な生産側と独立した消費側。実機なし
tool: IDA
addresses: [0x00900608, 0x00567BC0, 0x00568030, 0x005685A4, 0x005682DC, 0x005686D4, 0x0056928C, 0x007B0A28]
tags: ["layout"]
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

`SsysMaLayoutNode::vptr` と `SsysMaLayoutNodeVtable` を型にした。確度 MEDIUM：ctor・原本の仮想表、独立したrecord/replay・計算・登録側の命令が一致。実機なし。

| offset | 名前・型 | 契約 |
|---|---|---|
| node+0 | `SsysMaLayoutNodeVtable *vptr` | 表は0x900608、7slot |
| vtbl+8 | `void replay_recorded_list(Layout*)` | 0x5682DC |
| vtbl+C | `void calculate(Layout*)` | 0x568030、実名でない既存名vc_ACSYSTEM_DATA2は維持 |
| vtbl+10 | `bool build(Layout*,const char*,void*,u32)` | 0x5685A4。単一thisのcallbackではない |
| vtbl+14 | `void record_pane_tree(Layout*)` | 0x5686D4 |
| vtbl+18 | `void setup_projection_matrix(Layout*)` | 0x567BC0 |
| node+BC | `float inverse_view_mtx[3][4]` | 通常視点更新の逆行列 |
| node+F0 | `float view_eye[3]` | +F8はZ値 |
| node+FC | `u32 animation_flags` | Paneアニメーション評価に渡す |
| node+114 | `u32 replay_state_mask` | 再生第6引数 |
| node+118 | `u32 command_capacity_bytes` | バイト容量。既存名を維持 |

node+F8を有効フラグ、+FCを画面指定とする説は反証された。登録する画面はAddLayoutの引数0=上/1=下。node+134のdisplayは別の描画パス値である [ACNL-F0712]。

## 根拠

一次証拠は `_local/builds/acnl_jpn_v15/ida/work/100/primary.txt`、原本コード範囲と仮想表は `_local/builds/acnl_jpn_v15/ida/work/100/primary-index.json`、型のサイズ/offsetは `_local/builds/acnl_jpn_v15/ida/work/100/type-verification.json`。

- 0x12D2CC/D0がnode+0へ0x900608を保存。原本7語は0x5688A0,0x568854,0x5682DC,0x568030,0x5685A4,0x5686D4,0x567BC0。
- 0x5686EC..F8はvptr+18をロードし、R0=nodeで呼ぶ。0x567BC4でthisを保存、0x567BD8はnode+10から幅/高さ+28/+2Cを取得。0x567BDCは+121を読み、0x567C84/88は内包DrawInfoへ投影を書き込む。rootやPane木は読まない。+11Fの検査・設定は呼出し側0x5686E0..700で行う。Setup単独呼出しはこのflagを立てない。
- 0x12D304は+F8へVSTRでfloat 1.0、0x12D308は+FCへword 0。0x568030の冒頭0x568048は+FCをR1にロードし、Layout_AnimatePanesへ渡す。その先0x4B9718→Pane virtual+34→0x4B6A64/0x4B6014でflags bit0と可視条件を評価する。
- 0x568030の通常視点枝は+F0/+F4/+F8をfloatとしてlook-at計算し、view_mtxを書き、0x568030内のMtx34_InvertAffineへ+BCを渡す。stereo/projection modeによってZの別入力もある。単一有効boolとしては整合しない。
- 0x568600は+114を0、0x568634はBuild第4引数を+118へ保存。直後0x56862C..638はR0=同バイト数、R1=1でstorageを呼ぶ。
- 0x5683C8..E4は+114をstack第2語（全体第6引数）へ積む。0x7B0A28はこの値と描画contextのmaskを差分化し、各GPU状態dirty bitを立てる。GX記録件数は別の+110、第5引数。+114へ16を入れても容量16にはならない。
- 0x56928Cはscreen引数によって管理者+4/+10を選ぶ [ACNL-F0694]。node+FCはここで読まれない。

## 反証条件・未確認点

- 仮想表先頭2slotの関数ポインタ型、Buildのresource_holderの具体型は確定しきらずvoid*を維持。全派生LayoutのABIを統一する型ではない。
- 独立したLayout有効フラグは今回の対象欄に見つからなかった。全オブジェクト/全メンバーに存在しないという主張ではない。
- 実機表示と任意の状態mask値の効果は未測定。0x118をキュー容量へ改名しない。
