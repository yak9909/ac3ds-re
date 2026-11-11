---
id: ACNL-F0769
aliases: []
title: "InstSelect8のコンストラクタと4812バイトの境界"
summary: "InstSelect8_Ctor はthisのみを受け取りthisを返す。基底の後に8個ずつの28B/224B要素を構築し、全体境界は4812Bである。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x7c6eb0, 0x1c7a44]
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

`InstSelect8_Ctor` は `InstSelect8 *f(InstSelect8 *list)`。this以外の入力はない。全体境界4812Bの型を登録し、確定したvptr、行数、二つの行配列pointerだけに名前を付けた。確度 MEDIUM（ctor と配列構築helper・独立した派生ctor。実測なし）。

## 根拠

ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名は symbols を併読した。命令位置・呼び元は書き出しから引き、実バイトは `tools/codebytes.py` の `read_bytes` と Capstone で原本 code.bin を読む。原本 SHA256 は台帳と一致。命令列は `_local/evidence/149/original-asm.txt`、直接呼出の前後は `caller-asm.txt`、vtable/状態表の実値は `data-evidence.json`。IDB は指定の作業用コピーで型の適用・保存・読み戻しにだけ使用した。

```c
#pragma pack(push, 4)
/// [ACNL-F0769] MEDIUM: complete object extent; unverified fields remain unk_.
struct InstSelect8
{
  void * vptr;
  unsigned char unk_4[540];
  void * row_layouts;
  unsigned char unk_224[1948];
  int row_count;
  unsigned char unk_9C4[56];
  void * row_nodes;
  unsigned char unk_A00[2252];
};
#pragma pack(pop)
```

- `0x7C6EB4` はR0のthisをSelectBase_Ctorへ渡す。`0x7C6EC4`でvptrをInstSelect<8>へ変更し、this+AECを `0x301C7C`へ渡す（ctor=0x1C86C0、stride=1C、count=8）。次の `0x7C6EE0`はthis+BCCにButtonActionNode（stride=E0,count=8）を構築する。
- `0x301C7C` は各要素のctorを呼んだ後、元の配列先頭を返す。したがって `0x7C6EE4/EE8` の減算は元thisへ戻す操作。`0x7C6EFC`は+9C0=8、`0x7C6F04`は+220=this+AEC、`0x7C6F08`は+9FC=this+BCCを書き、R0=thisで返る。
- 28*8 と224*8、各開始位置からの境界計算はスクリプトで行い、`AEC + 8*1C = BCC`、`BCC + 8*E0 = 12CC`。独立した `0x1C7A44` と `0x7F3354` の派生ctorはこのctorの戻りthisを使い、派生の追加オブジェクトをthis+12CCから構築する。
- row_layoutsは28B要素群、row_nodesは224B要素群へのpointer。各要素の完全型は今回未定義のためvoid *。本型は確定した全体境界を持つが、SelectBase/CatalogBaseの全欄や配列の埋込み型を解析し尽くした意味ではない。
- 旧 `GameList.cpp` の `CtorFn(void*) -> void*`、`kInstSelectBytes=4812` は引数数と境界が一致し、型付きthisへ絞った。関数名 `InstSelect8_Ctor` は変更しない。

参考資料は依頼指定の旧版 gohan（`_local/legacy-src/gohan-legacy/Sources/Gui/GameList.cpp`・`GameLabel.cpp`・`Sources/Cheats/DecorLayout.cpp` の冒頭の型宣言。出所は依頼文、meta/references.toml の既存キーなし）。未検証の手がかりとして照合し、結論は命令列と独立したゲーム内の呼び元・消費側または vtable の実値に基づく。

## 反証条件・未確認点

- 全派生型と8行以外のtemplate instanceの互換性は未確認。共有SelectBaseの関数はInstSelect8専用と断定せず、未登録の基底オブジェクトをvoid *で受ける。別の境界・隠れ引数が必要な呼び元があれば再検討する。
