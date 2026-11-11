---
id: ACNL-F0767
aliases: []
title: "UiAnimの40バイト全体と結合状態欄"
summary: "UiAnim は40バイト。先頭はvptr、+0x18はAnimTransform、+0x1Cは結合状態、+0x1E/+0x20はcontent作業器の件数とポインタである。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x1261ec, 0x568a04, 0x568cac, 0x4b8ecc, 0x568840]
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

`UiAnim` は40バイト全体の型であり、従来の28バイトの登録は途中までだった。先頭の旧 `res` は vptr、旧 `sub` は AnimTransform pointer。確度 MEDIUM（ctor と複数の独立した配置・使用側。実測なし）。

## 根拠

ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名は symbols を併読した。命令位置・呼び元は書き出しから引き、実バイトは `tools/codebytes.py` の `read_bytes` と Capstone で原本 code.bin を読む。原本 SHA256 は台帳と一致。命令列は `_local/evidence/149/original-asm.txt`、直接呼出の前後は `caller-asm.txt`、vtable/状態表の実値は `data-evidence.json`。IDB は指定の作業用コピーで型の適用・保存・読み戻しにだけ使用した。

```c
#pragma pack(push, 4)
/// [ACNL-F0767] MEDIUM: complete object extent; unverified fields remain unk_.
struct UiAnim
{
  void * vptr;
  float total_frames;
  float cur_time;
  float prev_time;
  float rate;
  unsigned char flags;
  unsigned char unk_15[3];
  NwLytAnimTransform * transform;
  unsigned char bound;
  unsigned char unk_1D[1];
  unsigned short content_count;
  void * content_work;
  unsigned char unk_24[4];
};
#pragma pack(pop)
```

- ctor `0x1261EC` は `+0` に `vtbl_ssys_ma_lyt_Animation`、`+4/+8/+C=0.0`、`+10=1.0`、`+14/+18/+1C/+1E/+20/+24=0` を書く。別の呼び元 `0x11DD2C` の `0x11DDEC/0x11DDF8/0x11DE04/0x11DE10` は 0x28 間隔。`CatalogBase_Ctor 0x1C5AC8` も同じ40B間隔。
- `UiAnim_Init 0x568B94` が `+18` にtransformを保存。`0x73B3EC` はtransformの資源+8からframe数を読み、Initが `+4` にfloatで保存。`UiAnim_Step 0x568964` の `+8/+C` は現在・前回の時間、`+10` はrate、`+14` は再生flags。`SetFrame 0x568C00` が `+8/+C` とtransform+10に同じfloatを保存する。
- `Layout_BindAnim 0x4B8ECC` と `vc_ACSYSTEM_DATA1 0x567A50` が `+1C=1`、解除側 `0x568840/0x567DA4` が0にする。独立消費側 `BsHandCursor_Hide 0x1FA86C` の0x1FA8C4はこのbyteを読んで解除を選ぶ。
- Load の `0x568B28/B2C` はtransformの資源+Eのu16を `+1E` に保存し、件数×0x10Bを確保・構築して `0x568B58` で `+20` に保存。Dtorの `0x568CE4/CE8/CEC` はこの器を破棄してNULL化。要素の全体型は未確認のためcontent_workはvoid *。
- `+24` にはLoadが資源由来のbitを保存するが、本記録ではゲーム内の意味を確定せず `unk_24` に含める。`+15..17/+1D/+25..27` も未解明。
- 旧版3ファイルの40B確保・`kAnimBound=28` は一致する。旧symbolsの28B登録、先頭 `res`、`sub` の汎用pointerと相違し、全体型と正しいvptr/transformの意味に訂正した。関数名は維持し、fieldはnaming規則のsnake_caseにした。

参考資料は依頼指定の旧版 gohan（`_local/legacy-src/gohan-legacy/Sources/Gui/GameList.cpp`・`GameLabel.cpp`・`Sources/Cheats/DecorLayout.cpp` の冒頭の型宣言。出所は依頼文、meta/references.toml の既存キーなし）。未検証の手がかりとして照合し、結論は命令列と独立したゲーム内の呼び元・消費側または vtable の実値に基づく。

## 反証条件・未確認点

- 実機の寿命・結合競合は未確認。content_work要素の全構造、+24の意味、unk領域は未確定。別のstride、+28以降の隣接オブジェクトへのアクセスが見つかれば全体境界を見直す。
