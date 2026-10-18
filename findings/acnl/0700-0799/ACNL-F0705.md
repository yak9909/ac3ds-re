---
id: ACNL-F0705
aliases: []
title: "Picture・Material の別確保と可変長ブロックの実配置（再解析）"
summary: "Picture は 0x158 バイトで、Material 0x50 バイトと座標配列を別に確保する。Material の可変長領域は容量欄で区切られ、TEV は AlphaCompare・BlendMode より後ろにある。"
date: 2026-10-16
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x4b8d14, 0x4baa68, 0x4bcea8, 0x4bd694, 0x73d000, 0x73d0a0, 0x73d0c8, 0x73d060, 0x73d014, 0x73cb04, 0x73cb14, 0x73cb40, 0x4b6b58, 0x4b6154]
tags: [layout]
supersedes: ["ACNL-F0315"]
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

再解析で確認。資源から作る `nw::lyt::Picture` は `0x158` バイトの Pane 派生で、`+0x13C` に別確保の Material を持つ。Material 本体は `0x50` バイト。その `+0x34` の可変長ブロックと、Picture の `+0x154` の座標配列も別確保である。連続したメモリの一括コピーから独立した所有・寿命は導けない。

確度 MEDIUM：工場と各 ctor の確保命令、独立した getter・描画消費側、RTTI データが一致する。実機操作なし。既存コメント・型は証拠に数えない。

| 対象 | オフセット | 確認した意味 |
|---|---|---|
| Pane | +0x04/+0x08 | 自身の子リンク（次/前） |
| Pane | +0x14/+0x18 | 子リストの番兵（空なら両方 pane+0x14） |
| Pane | +0x28/+0x34/+0x40 | translate[3] / rotate[3] / scale[2] |
| Pane | +0x48/+0x4C | ローカル幅/高さ |
| Pane | +0x50/+0x80 | ローカル/大域の3×4行列。大域は計算結果 |
| Pane | +0xB4/+0xB5/+0xB6/+0xB7 | 元alpha/計算後alpha/basePosition/flags |
| Picture | +0xD4/+0xD8/+0xDC | UV計算済みバイト/出力数/計算済み出力領域 |
| Picture | +0x13C/+0x140 | Material* / 四頂点の色4語 |
| Picture | +0x150/+0x151/+0x154 | 資源座標セットの容量/使用数/配列ポインタ（1セット32バイト） |
| Material | +0x10..+0x28 | 色7語（リトルエンディアンの各語は 0xAABBGGRR） |
| Material | +0x2C/+0x30/+0x34 | 容量ビット欄/使用数ビット欄/可変長領域ポインタ |

容量欄 `C=*(u32*)(mat+0x2C)` と使用数欄 `N=*(u32*)(mat+0x30)` は同じビット配置を持つが役割が異なる。bits0–1=TexMap、2–3=TexSRT、4–5=TexCoordGen、6–8=TEV stage数、bit9=AlphaCompare有無、bit10=BlendMode有無。各配列を区切るオフセットは **C** から作る。使用中だけを巡回する個数には N を使う。

`B=*(mat+0x34)`、容量をそれぞれ T,S,G、bit9/10を A,L とすると実行時の配置は次の順である。

```
B                            TexMap[T]        (32 bytes each)
B + 32*T                     TexSRT[S]        (20 bytes each)
B + 32*T + 20*S              TexCoordGen[G]   (4 bytes each)
B + 32*T + 20*S + 4*G        AlphaCompare[A]  (8 bytes)
B + 32*T + 20*S + 4*G + 8*A  BlendMode[L]     (4 bytes)
B + 32*T + 20*S + 4*G + 8*A + 4*L  TEV stages (12 bytes each)
```

## 根拠

一次証拠は `_local/evidence/28/ida-primary.txt`、`ida-followup.txt`、`ida-final.txt`、`ida-data.txt`、`ida-xrefs-rtti.txt`、`ida-rtti.txt`、`ida-extra.txt`。数値計算は同所 `calculation.json`。主要関数の IDB original byte との差が空であることは `ida-verification.json`。

- `0x4B8DAC..0x4B8DC0` がサイズ `0x158`、align=4でアロケータを呼び、`0x4B8DD4` から Picture ctor。Pane 単体の分岐 `0x4B8D80..0x4B8DA4` は `0xD4` を確保し Pane ctorを呼ぶ。旧「Pane単体のサイズは工場で読めない」も訂正する。
- `0x4BAA78` は Pane ctorを先に呼び、`0x4BAA7C..88` で Picture vtableを置く。vtable直前のtypeinfo→文字列は `N2nw3lyt7PictureE` / `N2nw3lyt4PaneE` / `N2nw3lyt8MaterialE`。Picture typeinfo `0x8C9B9C+8` は Pane `0x8C9B68` を指す。Pane `+8` は `0x8C9BD0` の基底typeinfoを指す（internal::PaneBase）。
- `0x4BAABC` は座標セット予約。`0x4BD6CC..D8` は1セット32バイトを要求し、`0x4BD708/70C` は配列ポインタと容量を書く。`0x4BAB74..94` は `Alloc(0x50,4)`、Material ctor、Picture+0x13Cへの保存。これらは別の呼出しであり、一定の隣接距離を保証する命令はない。
- `0x73CB04` は +0x13Cを返す。`0x73CB14/40` は +0x140から色を選ぶ。`0x4BAB20` は四つの色を書き、`0x4BCF7C` は七つの色を書いている。`0x4BD8D8` は座標配列ヘッダの初期化。
- `0x4B6C20..48` は資源の translate/rotate/scale/size を転記。`0x4B69DC/0x4B6A44` は両行列の初期化。`0x4B6194..0x4B61A0` は親+0x80 または DrawInfo+0x44を選び、同関数の合成処理は一次値から+0x80を書く。`0x73CC80..88` は描画時に+0x80を読む。
- `0x4BB67C..0x4BB6A8` は `32*T+20*S+4*G+8*A+4*L+12*TEV` を別確保し、+0x34へ保存。`0x4BB6B0..0x4BB720` が容量欄を作る。`0x4BCF8C` 以降の資源内の配置計算と、実行時ブロックの配置は区別した。
- `0x73D000` は容量+0x2Cで `B+32*T`、`0x73D0A0` は `B+32*T+20*S`、`0x73D0C8` はさらに `4*G`、`0x73D060` はさらに `8*A`、`0x73D014` はさらに `4*L`。独立した消費側はそれぞれ UV計算、AlphaCompare送出、BlendMode送出、TEV送出から呼ぶ。

## 主張ごとの判定・訂正

| 旧記録の主張 | 判定 | 結果 |
|---|---|---|
| F0313 Picture約0x320、Material埋込、コピーだけで材質も独立 | 反証 | 本体0x158と複数の別確保。浅いコピーはポインタを共有する |
| F0313 +0xB5は色の数、+0x80を一次位置として直接変更 | 一部訂正 | +0xB5は計算後alphaであり色数ではない。+0x80は一次変換から再計算される結果。旧木にない複製の表示は未追試 |
| F0315 RTTI・継承、Picture0x158/Material0x50、別確保、工場のTextBox0x108/Window0x16C/他0xD4 | 確認 | 上記命令・RTTIと一致 |
| F0315 一次変換と計算行列、アンカー | 確認 | 合成側・描画側が一致。中央アンカー/画素換算は [ACNL-F0696] の条件に従う |
| F0315 一括コピーは隣のペインも含む、自己参照25個 | 一部訂正 | 本体を越える読取と外部リンクの誤再配置は一般に危険。旧捕獲領域の全バイトと25個の内容は未再採取 |
| F0315 七色と texMap数による既定色分岐 | 確認 | [ACNL-F0707] の使用側でも確認。任意TEVで同じ色になるとは言わない |
| F0315 可変領域はTexMap/SRT/Gen/TEV/Alpha/Blend順、個数は+0x30 | 一部訂正 | 先頭三種は合う。実配置の後半はAlpha/Blend/TEV。オフセットは+0x2Cの容量による |
| F0315 TexMap派生・書式の写像 | 確認 | [ACNL-F0706] で一次命令から確認 |
| F0315 「隣接しただけ」/F0316 「常に+0x1A0、344+72+80順」 | 一部訂正 | 別確保は確認。座標配列等を間に確保する順はあるが固定距離は保証されず、4個体の旧観測は未追試 |
| F0316 Material getter、四頂点色、PaneはMaterial getterで0 | 確認 | getterとvtableデータが一致。ただしMaterial所有はWindow/TextBox等にもあり「Pictureだけの材質」には一般化しない |
| F0316 Paneのサイズが工場から読めない | 反証 | Pane分岐は0xD4を確保する |
| F0315 旧IDBにコメントを書いて保存した | 一部訂正 | 既存コメントの存在は見えるが過去の保存操作の証明にはしない。現在の命令を証拠とした |

F0315 の構造・キャッシュ・アンカーの結論を本記録と [ACNL-F0706] [ACNL-F0707] [ACNL-F0696] で置き換えるため supersedes に含める。他記録の旧実験は各主張の部分訂正であり全体置換ではない。

## 反証条件・未確認点

- 資源からの通常生成経路の確保サイズ。別の派生クラス・コピー構築・失敗時の動作を網羅していない。構造体の新規型付けは行っていない。
- 実行時のヒープ配置・固定距離・旧ダンプの隣接物の全内容は未確認。Picture本体/Material/配列/テクスチャ実データの寿命は別である [ACNL-F0708]。
