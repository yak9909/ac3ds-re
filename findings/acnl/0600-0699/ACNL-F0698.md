---
id: ACNL-F0698
aliases: []
title: "Layout 投影 uniform の c4 は毎再生前に設定され初期化後のゼロ固定ではない（再解析）"
summary: "投影uniformのc4はDrawer+0x74..+0x80。再生直前のsetterが立体視変位・LayoutMgrの値・0・0を書き、初期化以降ずっとゼロという説は成立しない。"
date: 2026-10-16
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x4d5d1c, 0x4d5c9c, 0x5682dc, 0x4d6c90, 0x148d30]
tags: [layout]
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

再解析で確認。投影送出の追加4語 c4 は Drawer+0x74/+0x78/+0x7C/+0x80 であり、`+0x84` は詰め物。初期化ではゼロだが、非空 Layout の再生直前に `0x4D5C9C` が更新する。旧F0303の「初期化以降ずっとゼロ」、それを前提とした「影響しない」は反証された。

確度 MEDIUM：初期化側・setter側・呼出し側・uniformコピー側の独立した命令が一致。実機なし。非ゼロ値の存在可能性は確定するが、実行時の値やシェーダ内の作用は未確認。

## 根拠

一次証拠：`_local/evidence/22/ida-primary.txt`、`ida-followup.txt`。送出範囲の計算：同フォルダの `calculation.json`。

- 初期化 `0x4D64C4..0x4D64E0` は Drawer+0x28へ `0x80000000`、+0x2Cへ `0x000F02C0` を設定し、+0x74..+0x80をゼロにする。初期化時のゼロというF0303の部分主張は確認。
- `0x568368..0x568380` は display が0x400/0x410かつ `Layout+0x120==1` の場合だけ `+0x124` を採用し、それ以外は S17=0。`0x568574..0x568584` は0x400で符号反転、0x410でそのままにする。
- `0x56838C` の R5=mgr+0x300、`0x5683A0` の `VLDR S1,[R5,#0x50]` は mgr+0x350 のfloat。`0x568398/9C` は S2=0、S0=S17。`0x5683A4/A8` は Drawer=mgr+0x364 を `0x4D5C9C` へ渡す。
- `0x4D5C9C..0x4D5CA8` は `ADD R0,#0x74; VLDR S3,=0; VSTM R0,{S0-S3}`。戻り値は+0x74のポインタだが、別オブジェクトの取得ではない。既存名 `nwlyt_GetDrawCtxForList` はこの実体を表していない（今回は改名せず訂正コメントを付ける）。
- その直後 `0x5683C4` → `0x4B8C74` → `0x4D6C90` が投影を送る。`0x148D30` は16語を Drawer+0x34..+0x70 にコピーするので、c4を上書きしない。
- `0x4D6CB4` は m[0] を+0x30へ移し、`0x4D6CBC` は+0x34をheader `0x013F02C1` にする。extra=19、計20語のpayloadは m[0]が+0x30、m[1..15]が+0x38..+0x70、c4が+0x74..+0x80。
- `0x4D6CCC` の `STR R12,[R4,#0x50]` では、直前の2回のwritebackで R4=元Drawer+0x34。従ってゼロを書かれるのは元Drawer+0x84であり、c4の最後の語ではない。`0x4D6CD0` は+0x28から0x60バイトを送る。

## 主張ごとの判定・訂正

| 元記録・主張 | 判定 | 結果 |
|---|---|---|
| F0288 行列末尾+0x74、c4=+0x78..+0x84 | 反証 | 行列末尾+0x70、c4=+0x74..+0x80、+0x84は詰め物 |
| F0303 c4の範囲、初期化時に4語ゼロ | 確認 | 命令と一致 |
| F0303 コピーはc4を触らず、従って永久ゼロ | 一部訂正 | コピー範囲は正しいが別setterが更新するので永久ゼロの推論は反証 |
| F0303 自前ノードに一切影響しない | 反証 | ゼロ固定を前提に無影響とは言えない。実際のシェーダ作用は未確定 |

F0288の全体置換は [ACNL-F0696] が宣言する。F0303は他の捕獲列・スプライトの標本も含むため全体の supersedes にはせず、上記部分を訂正する。

## 反証条件・未確認点

- mgr+0x350の生成・意味・実行時の非ゼロ頻度、c4のシェーダ内の成分順・符号・単位・画素への影響は未確定。CPU上の4語の配置と送出を確認した段階である。
- 左右目・立体視オフセットの実画面差は未追試。次の実機作業ではS0/S1の元値、Drawerの4語、送出列を同一フレームで照合する。
