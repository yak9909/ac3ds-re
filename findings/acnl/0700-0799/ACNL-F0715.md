---
id: ACNL-F0715
aliases: []
title: "Material可変領域の要素型と容量・件数の区別"
summary: "Materialの可変領域先頭をTexMap*、各後続部分を要素型とgetterで表した。容量bitsによる配置と件数bitsによる巡回を区別する。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # 静的な生産側と独立した消費側。実機なし
tool: IDA
addresses: [0x004BB5E0, 0x004BCEA8, 0x004B9830, 0x0073D000, 0x0073D0A0, 0x0073D0C8, 0x0073D060, 0x0073D014, 0x0073B650]
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

Materialのvariable_dataを `NwLytTexMap *` とし、TexMap/TexSrt/TexCoordGen/AlphaCompare/BlendMode/TevStageの要素型とgetter型を付けた。固定配列が一つ続くという意味ではない。確度 MEDIUM：確保・初期化と、独立したgetter・UV計算・GPU送出が一致。既存A記録 [ACNL-F0705][ACNL-F0706] を再利用。実機なし。

| 要素型 | stride | 既知欄 |
|---|---|---|
| NwLytTexMap | 0x20 | +4未シフトのGPUアドレス、+8/A使用幅高、+C/E全体幅高、+10 sampler_bits、+14/+18/+1C GPU派生値 |
| NwLytTexSrt | 0x14 | translate[2], rotate, scale[2] |
| NwLytTexCoordGen | 4 | +1 coordinate_set、ほか未命名 |
| NwLytAlphaCompare | 8 | +0 compare_function、+4 float reference |
| NwLytBlendMode | 4 | operation, source_factor, destination_factor, logical_operation 各u8 |
| NwLytTevStage | 0xC | 3語。細部は未命名 |

`NwLytMaterialCountMask` は両bits欄のmask名。bits0–1=T、2–3=S、4–5=G、6–8=TEV、bit9=A、bit10=L。容量Cを用いる配置は `TexMap[T] → TexSrt[S] → TexCoordGen[G] → AlphaCompare[A] → BlendMode[L] → TevStage[TEV]`。各開始offsetは順に0、32T、32T+20S、そこへ4G、さらに8A、さらに4L。T=0でもvariable_dataは同じ可変ブロックの基底であり、先頭TexMapの実在を保証しない。使用数はcount_bitsから取る。

## 根拠

- `_local/builds/acnl_jpn_v15/ida/work/100/primary.txt` の0x4BB5E0、0x4BCEA8、0x73D000/0x73D0A0/0x73D0C8/0x73D060/0x73D014。確保量は `32T+20S+4G+8A+4L+12TEV`。初期化はSRTの移動/回転0・拡大1を保存し、AlphaCompareの初期語7とfloat 0を保存する。
- 0x73B650はcount_bitsからGen数を取り、Gen+1のUVセット索引を読む。SRT+0/+4はUV平行移動、+8はsin/cos計算の回転入力、+C/+10は拡大、TexMapの使用/全体寸法比を掛ける。
- 0x4B9830はsampler_bitsを抽出し+14/+18/+1Cを作る。0x4B7DECはアドレス+4を>>3し、派生値を独立に読む。入力のnw::lyt書式とGPU書式は別 [ACNL-F0706]。
- 0x4B7864はAlphaCompare+0を比較方式表へ、+4のfloatを255倍して閾値へ変換する。0x4B7F80はBlendModeの四つのbyteをblend/logic送出表へ使う。
- getter型は上記各要素へのポインタを返す。オフセットにcount_bitsを使う型へ変更していない。

## 反証条件・未確認点

- TexMap+0、Genの+0/+2/+3、TEVのpacked内部、mask上位の未確認bitsには名前を付けない。各書式・比較方式・blend方式の正式Enum名を推定していない。
- 予約容量の変更・失敗で旧ブロックが破棄される経路がある。variable_dataの型は非ゼロ・要素存在・GPU参照寿命の保証ではない。
