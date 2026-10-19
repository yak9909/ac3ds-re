---
id: ACNL-F0710
aliases: []
title: "Pane・Picture・Material の描画用構造と vtable 型"
summary: "Pane 0xD4、Picture 0x158、Material 0x50 の既知メンバーとvtableを型にした。描画はcursor・DrawInfo・描画contextを4引数で受け渡し、Pictureの座標セットは別確保である。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x008FBE7C, 0x008FBFFC, 0x008FC18C, 0x004B6154, 0x0073B524, 0x0073CB58]
tags: ["layout", "rtti"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

[ACNL-F0705] [ACNL-F0706] [ACNL-F0707] [ACNL-F0708] の構造・所有・描画契約を再利用して `NwLytPane`、`NwLytPicture`、`NwLytMaterial` とvtable型を付けた。既存の型・名前は削除していない。
確度 MEDIUM：資源工場・初期化・行列計算と、独立した木走査・Picture描画・vtable原本データが一致する。実機なし。

| 型 | 確認した欄 |
|---|---|
| Pane (0xD4) | +4自身の次/前link、+0xC親、+0x14子の循環番兵、+0x28移動、+0x34回転、+0x40縮尺、+0x48/4C幅高さ、+0x50局所/80大域行列、+0xB4/5元/計算後alpha、+0xB6基準位置、+0xB7 flags |
| Picture (0x158) | +0xD4 UV計算済み、+0xD8出力数、+0xDC計算結果6×4float、+0x13C Material*、+0x140四隅の色、+0x150/151座標セット容量/使用数、+0x154配列 |
| Material (0x50) | +0x10七色、+0x2C容量bits、+0x30使用数bits、+0x34可変領域、+0x4D flags |

可視はPane flags bit0であり、独立したboolメンバーには分割していない。base_positionの下位ニブルはアンカー、bit4はalpha0時の自身の描画省略。flags bit1はalpha影響、bit3は標準破棄時の非所有を表す条件として既存再解析に従う。Material flags bit0/1/2の所有・状態送出・UVキャッシュ条件も独立したboolにしない。

## 根拠

一次証拠：`_local/evidence/98/primary.txt`、`primary-index.json`。vtable原本はtools/codebytes.py経由で読んだ。サイズ・全メンバーoffsetのIDA照合は `type-verification.json`。

- 工場 `0x4B8D14` がPane/Pictureへ0xD4/0x158を確保し、`0x4B6B58` と `0x4BAA68` がそれぞれのvptrを保存する。Materialは `0x4BAB74..94` の0x50別確保。
- Pane ctorの `0x4B6B58` は子の番兵を自身+0x14へ設定。`0x4B6154` は親+0x80またはDrawInfo+0x44を使って行列を合成し、元alphaから計算後alphaを作る。`0x73B524` はlink+0を次へ辿り、childはlink-4として可視bitを検査する。
- `0x4D7190..B0` はrootを取得し、R0=Pane、R1=cursor、R2=DrawInfo、R3=描画contextで木走査を呼ぶ。`0x73B52C/34` はR2/R3を保存し、`0x73B580/84` で子へ再設定、`0x73B550..5C` はvslot+0x68から戻るR0を次のcursorにする。旧の3引数推定のままではR3が脱落するため4引数型にした。
- 原本vtableのPane/Picture +0x5Cは共に `0x4B6154`、+0x68はPaneがcursor素通しの `0x73B5BC`、Pictureが `0x73CB58`。型のdraw_selfは共通基底Pane*を受ける。
- `0x73CB58` はPicture+0x13Cと+0x154を読み、結果を+0xDCへ作り、+0xD8に個数を保存。矩形の色・行列・寸法は各Pictureから得る。座標セットの32B配列は `0x4BD694/0x4BD5C8` の別確保/転記と一致する。
- Material容量の配置順は [ACNL-F0705] の訂正済み `TexMap→TexSRT→TexCoordGen→AlphaCompare→BlendMode→TEV`。可変領域は単一の固定配列型へ誤って重ねずvoid*で残した。

## 反証条件・未確認点

- 未判明メンバーはunk_オフセット、未判明vslotはvoid*である。未知の関数ABIや正式メソッド名を推定していない。
- 自前Paneの表示、四隅と色配列indexの実画面対応、共有Material更新の発生頻度は今回実測していない。
