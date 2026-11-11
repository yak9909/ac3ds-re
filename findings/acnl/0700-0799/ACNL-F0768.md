---
id: ACNL-F0768
aliases: []
title: "ArcResAccReaderの584バイトと埋込みアクセサ"
summary: "ArcResAccReader は584バイト。+4は埋込みaccessor(+0xC)を指し、+8はDARC、+0x158は読み込み完了側のDARC pointer。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x120d54, 0x567244, 0x567310, 0x568cfc]
tags: ["layout"]
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

`ArcResAccReader` の全体境界は584B（0x248）。確度 MEDIUM（ctor と独立した複数の配置・ロード・破棄側。実測なし）。確定したpointerとvptrのみを公開し、それ以外はunkとする。

## 根拠

ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名は symbols を併読した。命令位置・呼び元は書き出しから引き、実バイトは `tools/codebytes.py` の `read_bytes` と Capstone で原本 code.bin を読む。原本 SHA256 は台帳と一致。命令列は `_local/evidence/149/original-asm.txt`、直接呼出の前後は `caller-asm.txt`、vtable/状態表の実値は `data-evidence.json`。IDB は指定の作業用コピーで型の適用・保存・読み戻しにだけ使用した。

```c
#pragma pack(push, 4)
/// [ACNL-F0768] MEDIUM: complete object extent; unverified fields remain unk_.
struct ArcResAccReader
{
  void * vptr;
  void * resource_accessor;
  void * arc_data;
  void * accessor_vptr;
  unsigned char unk_10[328];
  void * loaded_arc;
  unsigned char unk_15C[236];
};
#pragma pack(pop)
```

- `0x120D54..D70`: this+4 に this+C、this+8 にNULLを保存し、this+Cにaccessor ctor `0x12BF04` を呼ぶ。`0x120D90/D94`で先頭をArcResAccReader vptrへ、`0x120D98`で+158=NULL、`0x120D9C`でthis+15CにLoadSplit ctor `0x12D3B4`を呼び元thisを返す。
- `0x12D3B4` は内部+EAまで書く。配置側 `0x11DDC0` と `0x11DDCC` はreaderの戻りthisに0x248を加えて次を構築する。これがctor最終書込のalignmentを含む584B境界を独立確認する。
- LoadArcStep `0x5672A4/AC` はLoadSplit+ D0（reader+22C）のbuffer pointerをreader+158へ、`0x5672C0` は+8へ保存して `0x5672C4`でthis+CのaccessorにAttachする。+158は単なるloaded boolではない。
- `UiAnim_Load 0x568A98` はreader+4からaccessorを得る。`RegisterTextures 0x568D0C` は+8のDARCを読む。`0x568E68`は埋込みthis+CをGetTextureへ渡す。Dtor `0x567318`は+15Cを破棄した後、`0x56732C`は+Cを破棄し、元thisを返す。
- +148の既定word、+14CのTexBufList、+15CのLoadSplitの配置は命令から分かるが、今回はそれらの全field型を定義しない。+Cのaccessorもvptr以外はunk。resource_accessor/arc_data/loaded_arcは対象の完全型未登録のためvoid *。
- 旧 `GameList.cpp` の584Bと `DecorLayout.cpp` の `kHolderArc=8`、`kHolderAccessor=C` は一致。旧 `kHolderArcLoaded=158` は実体がpointerであることを明記する。ctor/dtorの旧汎用CtorFnをreader pointer引数・戻りへ絞り、追加引数なし。

参考資料は依頼指定の旧版 gohan（`_local/legacy-src/gohan-legacy/Sources/Gui/GameList.cpp`・`GameLabel.cpp`・`Sources/Cheats/DecorLayout.cpp` の冒頭の型宣言。出所は依頼文、meta/references.toml の既存キーなし）。未検証の手がかりとして照合し、結論は命令列と独立したゲーム内の呼び元・消費側または vtable の実値に基づく。

## 反証条件・未確認点

- 内部loaderの全ABI、ロード失敗復旧、テクスチャの寿命・GPU完了は未確認。+158にpointer以外を要求する独立した使用側、0x248と異なる配置間隔があれば再検討する。
