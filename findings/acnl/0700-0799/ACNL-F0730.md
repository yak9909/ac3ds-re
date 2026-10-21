---
id: ACNL-F0730
aliases: []
title: "nw::lyt は最大6段のTEVと3組の通常テクスチャ・UVを記録へ送る"
summary: "MaterialはTEV最大6段、通常TexMap/SRT/UV生成は各最大3。Pictureの記録経路でTEV・Repeat・UV変換・blendを送出できるが、6段は6回の独立テクスチャ参照を意味しない。"
date: 2026-10-21
category: render
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: "全関数export・RomFS・公開ソース"
addresses: [0x004B8790, 0x004B7864, 0x004B7F80, 0x004B7DEC, 0x0073CB58, 0x0073B650, 0x004B541C, 0x004B9830, 0x004BB5E0]
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

nw::lyt MaterialからTEV・混合・リピート・UV SRTを指定できる。最大6段のTEVと、最大3組の通常画像/独立UVは別の上限である。6層の異なる座標のサンプリングを、TEVの6段だけで実現できるという読み方は成立しない。
確度 MEDIUM：Materialの確保/生産、独立したPicture描画・座標計算・GPU状態送出、公開レジスタ定義を照合。今回のGPU実測なし。

## 根拠

一次証拠は `_local/evidence/107/0x004b8790.txt`、`0x004b7864.txt`、`0x004b7f80.txt`、`0x004b7dec.txt`、`0x0073cb58.txt`、`0x0073b650.txt`、`0x004b541c.txt`、`0x004b9830.txt`、`0x004bb5e0.txt`。元exportは `exports.json`。

- `0x4BB5E0` の容量bitsはTexMap/TexSRT/TexCoordGen各2 bit。`0x4B8790` はTEV数を6に制限して、レジスタ0xC0/0xC8/0xD0/0xD8/0xF0/0xF8へsource/operand/combine/constant/scaleを送る。
- 入力表は `{3,4,5,6,14,0,15,13}`（tex0/1/2/3、定数、頂点色、前段、buffer）。演算表は `{0,1,2,3,4,5,9,8}`（Replace/Modulate/Add/AddSigned/Interpolate/Subtract/AddMultiply/MultiplyAdd）。scaleは1/2/4、RGBとalphaは別指定。
- RGB成分には色/反転/alpha/反転/r/g/b系を指定。各段の定数色はMaterialの7色からRGB/alpha別に選ぶ。最後にbuffer初期色も送る。**tex3が表にあることは4枚目の通常画像をbindする仕組みではない**。
- `0x4B7DEC` はTexMap件数だけ通常texture0…2のアドレス・寸法・sampler状態を送出。新しいTEV段が同じtexture0を読むと同じサンプル値を読む。段ごとのUVオフセットをtexture samplerへ渡す欄はない。
- `0x73B650` は各TexCoordGen+1のUV組番号を読み、各SRTの移動/回転/拡大、使用寸法/全体寸法比とV反転を適用する。UV行列はこのCPU計算から頂点データへ焼かれる。`0x4B541C` のCLTSはそのSRT要素へHermite補間値を書き、描画キャッシュを落とす。CLTPはTextureInfoを差替える別の機構。
- `0x4B9830` はsampler wrapをGPUへ写像し、`0x4B7F80` はBlendModeのoperation/src/dst/logicを送る。Materialのalpha比較も `0x4B7864` から別送出。
- `0x73CB58` はMaterial_EmitState→texture状態→UV計算→quad登録を通る。したがってLayoutの板の記録経路そのものがTEVを排除しているわけではない。既存の単一画像用・中立化した材質のままでは追加機能は指定されない。

公開資料 `STUDY107_PUBLICS` の [3dbrew GPU registers](https://www.3dbrew.org/wiki/GPU/Internal_Registers)、[libctru enums.h](https://github.com/devkitPro/libctru/blob/master/libctru/include/3ds/gpu/enums.h)、[citro3d texenv.c](https://github.com/devkitPro/citro3d/blob/master/source/texenv.c) は通常texture0…2、procedural texture3、6組のTEVレジスタと対応する。

演算の意味から、二色補間 `C1*L + C0*(1−L)` はInterpolateで表せる（定数と頂点色を二端点に使える）。A4ならalpha operand、L4なら色operandを使う。従って「二色化自体がGPUで不可能」は根拠がない。一方、6個の独立サンプルの合成後に非線形clampを置く処理は、3サンプルの上限や中間精度を解決せず同一視できない。この全再現の可否はLOWの仮説として残す。

## 反証条件・未確認点

- GPUの飽和/丸めの実測、gohanのCPUのclamp式・量子化・サンプリングとの画素比較は未実施。二色補間の表現と全処理の画素一致は別。
- 素材の対称性や同じサンプルになる条件を利用して実効サンプル数を減らせるかは未検証。3組という一般上限から、特定素材の単一パス化が数学的に不可能だと断定していない。
- 通常レンダーターゲット書式にはL4/A4がない（[citro3d texture.c](https://github.com/devkitPro/citro3d/blob/master/source/texture.c) とlibctruのtexture/render formatを参照）。オフスクリーン案では通常16/32 bpp面・GPU完了待ち・テクスチャ化転送を別に数える。既存UIの板追記だけでターゲット切替まで安全とはしない。
- 公開 [NW4R material header](https://github.com/doldecomp/ogws/blob/master/include/nw4r/lyt/lyt_material.h) はTexSRT/TEV/Blendの概念と容量/使用数の区別の参考。Wii用の構造・上限・GX APIをCTRへ移植する証拠には使わない。
