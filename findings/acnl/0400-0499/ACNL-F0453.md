---
id: ACNL-F0453
aliases:
- IDA-opus-5-F023
title: セッションで作った全部を解放。親ヒープへ 467,056 B が戻った（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-F022 の手順を**このセッションで作った全オブジェクト**へ広げた。'
date: '2026-09-21'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9424104
- 9423988
- 9424028
- 9438524
- 5160440
- 5161364
- 5177732
- 9438216
- 3243260
- 4951280
- 9892176
- 5675844
- 5675860
- 1798684
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:949-1032
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F023: セッションで作った全部を解放。親ヒープへ 467,056 B が戻った（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-F022 の手順を**このセッションで作った全オブジェクト**へ広げた。
終了時、画面は素の村に戻り、**ヒープを抱えているアロケータはゼロ**になった。

### 対象の洗い出しは番地ではなく形でやる

走らせるたびに状態ファイルが分かれていて取りこぼしが出るので、scratch 領域
`[0x32F41900, 0x32F42F00)` を語単位で走査し、**vtable で種類を見分けて**数えた。

| 探すもの | 目印 | 見つかった数 |
|---|---|---|
| instance holder | `+0` が `0x8FCCE8` | 17（うち生存 4、解放済み 13） |
| `g3d::MaterialAnim` / `SkeletalAnim` | `+0` が `0x8FCC74` / `0x8FCC9C` | 14（うち生存 1） |
| `HeapAllocator` | `+0` が `0x90053C`、`+4` が非0なら生存 | 23（うち生存 8） |

この走査で、状態ファイルに記録が残っていなかった `cursorC`（参照用）と `cursorE` も拾えた。

### 解放した内訳

| 対象 | 数 | 返却 |
|---|---:|---:|
| `many_instances` の12体（instance + MaterialAnim） | 12 | **61,080 B**（1体 5,090 B） |
| 本 / cursorB / cursorC / cursorE | 4 | ヒープごと回収 |
| `cursorC` の MaterialAnim | 1 | 同上 |
| ヒープ（資源2・instance 4・アニメ2） | 8 | — |
| **親ヒープ `0x301668EC` の空き** | | **36,168 → 503,224（+467,056 B）** |

A の instance ヒープは 12体解放後に 131,072 中 **129,672** が空き（残り 1,400 B は本の instance で、
これも次に解放した）。

### 分かったこと

- **`g3d::MaterialAnim` の後始末も vtable スロット5**（`0x4EBDF8`）で、骨アニメ（`0x4EC194`）と同じ形。
  `a1[5]=0` / `a1[6]=0` → AnimObject を自分のアロケータで free → `HeapAllocator_DestroyHeap(anim+12)`。
  **デストラクタ（スロット1）では解放されない**のも同じ。
- **`bufferOption = 0` の instance でも自前の mesh 配列を持っていた**（本・cursorB・cursorE の3体で確認）。
  `0x4F0184` が資源側へ書く分岐（`node+0x170 == +0x174`）は、少なくとも今回見た6体では**一度も起きなかった**。
  条件は bufferOption ではない。**何が条件かは未解明**。
- **孤児 ExpHeap（IDA-opus-5-F013 の `0x30C51E7C`）は親ヒープごと回収された。**
  あれは `cursorC` の instance ヒープ `0x30C50DA8` の中にあったので、そのヒープを破棄した時点で消えている。
  **孤児を名指しで破棄してはいけない**（解放済み領域に対する操作になる）。
  解放後もその番地には vtable らしき語（`0x900408`）が残って見えるが、ただのゴミ。
- 資源ホルダは**ヒープを破棄する前に** `G3dResHolder_Dtor 0x317CFC` を通す。2件とも vtable が
  `vtbl_g3d_ResourceSet` へ戻った。

### scratch も返した。ただし順序が要る

`0x4B8CF0(size, align)` は `*(0x0096F150)` のアロケータの vtable スロット2 を尾呼びするだけで、
**対の解放は `ssys::ma::Allocator::Free 0x00569B44(allocator, ptr)`**（旧 F-296 が実機で往復確認済み）。
実機で形も確かめた: `*(0x96F150)` = `0x32C46020`、`+4` にヒープ `0x32C45F78`、
その vtable スロット7（`+0x1C`）が free、ラッパの vtable スロット2 が `0x569B54` ＝ alloc の相方。

**★順序**: scratch A の `+0x280` には**ケーブの制御ブロックが載っている**。先に解放すると
ケーブが毎フレーム解放済み領域を読み、再利用されて `enable` がゴミで非0になれば暴走する。
だから **`0x1B721C` のフック語を元の NOP（`0xE320F000`）へ戻してから** scratch を返した。
戻した直後にケーブの `runs` が 92 で止まったことで、フックが実行されなくなったことを確認している。

scratch 3本（各 `0x800`）を返し、holder/anim の配列もその中にあったので一緒に消えた。
これらは nw::lyt のヒープから出ているので、親ヒープの 467,056 B とは別勘定。

**いま実機に残っているのは `.text` 末尾だけ**: call guard `0x838100`（まだ使う）、
表示ケーブ `0x838400`、アニメケーブ `0x838600`。**どこからも到達しない。**

### `0x4F0184` の「資源側へ書く」分岐（IDA-opus-5-T016 の答え）

`node+0x170` と `+0x174` は **instance 自身の mesh 配列の begin / end** で、
等しいのは「**配列が空**」という意味。空のとき `sub_4F024C` も `0x4F0184` も
`resModel+0xB8`（表）と `resModel+0xB4`（個数）へ落ちる。

romfs 2本・**9,081 モデル**を走査したところ、**mesh 数 0 のモデルが 71 個**あった
（`MiniGame0` の `esc_loc_*` や `dummy_attach` など、位置決め用のダミー）。
この種のモデルでは分岐に入るが**個数も 0 なので何も書かれない**。

危ないのは「**mesh を持つモデルなのに instance の配列が空**」という組み合わせだけで、
今回観測した6体（`bufferOption` 0 と 0x834、Model と SkeletalModel）では**一度も起きなかった**。
**何がその状態を作るのかは未解明**。破棄の前に `node+0x170 != node+0x174` を確かめる守りは残す。

根拠: `events.jsonl` の `free_*` / `many_destroy` / `many_release` / `final_cleanup_*`、
`final_cleanup.json`、`many_state.json`、画像 `after_everything_freed_top.png`、
`0x4EBDF8` の逆アセンブル。
反証条件: 場面転換で何か起きる（**未検証**）、scratch を返さずに繰り返すと枯れる、
`0x4F0184` の資源側分岐が別条件で起きる。

