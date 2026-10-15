---
id: ACNL-F0307
aliases:
- F-282
title: 'F-282: CTRPF プラグインへ移植した。**ビルド環境なしで移植の正しさを照合できる** — `HIGH`（静的のみ・未ビルド）'
summary: '`Plugin/CTRPluginFramework-BlankTemplate-0.8.0` の描画まわりを全部書き直した。'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10161408
- 10161664
- 10163200
- 10164736
- 10167808
- 10178560
- 10178816
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:17535-17698
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-282: CTRPF プラグインへ移植した。**ビルド環境なしで移植の正しさを照合できる** — `HIGH`（静的のみ・未ビルド）

`Plugin/CTRPluginFramework-BlankTemplate-0.8.0` の描画まわりを全部書き直した。
見た目は `Plugin/CTRPF-GUI-Simulator` の設計に合わせた。**最低限の移植**である。

### 書き直したもの

| ファイル | 役割 |
|---|---|
| `includes/GuiCaves.h` | **自動生成**（`PATCHES/export_gui.py`）。ケーブ 6 本・フック 3 本・vtable・`.bss` 配置・自前 TEV・書式定数 |
| `Sources/GuiRender.cpp` | **スプライト表を書くだけ**。GPU の作法は知らない。座標変換と、色ごとのチャンク分けを持つ |
| `Sources/OwnGui.cpp` | 確保 → アトラス配置 → ケーブ書き込み → `.bss` 初期化 → フック 3 本 |
| `Sources/GuiMenu.cpp` | シミュレータの色と寸法をそのまま写したメニュー。Select で開閉、十字上下で移動 |
| `includes/GuiFontAtlas128.h` | **自動生成**（`PATCHES/make_font_atlas.py`） |

**ケーブは C++ へ書き直さない。** 書き直した瞬間に
`audit_node_cave.py` / `verify_literals.py` / IDA での検証が無効になる。
実行時に差し替えるのは**テクスチャの番地 2 語だけ**で、その位置も生成器が出す。

```
kGuiCaveQ[kGuiTexPaIndexQ] = (VA - 0x10000000) >> 3   … reg 0x085
kGuiCaveN[kGuiTexVaIndexN] = VA                        … キャッシュ吐き出し
```

### ★`PATCHES/verify_plugin_port.py` — ビルドせずに移植を照合する

devkitPro が無くても移植の正しさは確かめられる。
`GuiMenu.cpp` / `GuiRender.cpp` のロジックを Python で書き直し、
生成される **20 語 x N のスプライト表**を `build_table()` の出力と 1 語ずつ突き合わせる。

**寸法・色・文字列は C++ のソースから正規表現で抜く**ので、
片方だけ直したらここで落ちる。

```
C++ から読んだ値: X=0 W=160 見出し=23 行高=18 行数=6 下帯=216
  題名='ACNL MENU'  項目 6 件  ヒント='SELECT = MENU   SELECT+UP = LEGACY'
C++ 再現: 上 119 枚 17 チャンク / 下 28 枚 4 チャンク
★ 移植の照合 OK。C++ が作る表は Python 側と 1 語も違わない。
```

### この照合が実際に見つけた不具合（4 件）

1. **色配列の上限超過。** 枠・見出し帯・下帯・縁・選択帯をそれぞれ別の色にすると、
   **色ごとに 1 チャンク（7 枚）を食う**ので 17 チャンクになり、
   当時の上限 16 を超えて内容が黙って落ちていた → `COLORS_MAX` を 24 へ
2. **表の容量超過。** 上画面のメニューは 119 枚要る（枠だけで 35 枠を食う）→
   表を上画面優先に組み替え（下 38 枚 / 上 134 枚）
3. **記録リストの不足。** 119 枚 x 約 127 バイト = 約 15KB で `LIST_SIZE = 0x4000` に収まらない
   → `0x8000` へ
4. **埋め草スプライトの座標が Python と C++ で違った**（どちらも不可視だが照合が効かない）
   → 両方「大きさ 0・位置 0」に統一

**1 と 3 は実機に入れたら「一部が描かれない」「GPU が止まる」になっていた。**

### `.bss` の配置（F-282 時点）

```
0x9B0D00  LOG         0x100
0x9B0E00  COLORS_BOT  0x600   24 チャンク x 0x40
0x9B1400  COLORS_TOP  0x600   24 チャンク
0x9B1A00  TABLE       0x0C00   38 枚（下画面。ヒント 1 行）
0x9B2600  TABLE_TOP   0x2A00  134 枚（上画面。メニュー本体）
0x9B5000  （予備 0x100）
0x9B5100  NODE_TOP / VTBL / NODE_BOT / MATBUF / RING / MATCMD
```

`LIST_SIZE = 0x8000`（自前ノード 1 個あたりの記録リスト）。

### メニューのレイアウト（シミュレータの MENU と同じ）

```
上画面 左 160px にパネル、見出し帯 0..23、下帯 216..240、右に 2px の縁
行の高さ 18、見える行 6（★最低限の移植。シミュレータは 10）
色は rgba をそのまま 0xAABBGGRR へ写した
  パネル C70D100C / 縁 E6A4E463 / 見出し帯 BD222B1C / 選択帯 A3374529
  下帯   C2171B15 / 見出し文字 FFA4E463 / 本文 FFB1B9AE / 選択中 FFFFFFFF
下画面は 1 行のヒントだけ
```

文字は **8px を等倍**で描く（`scale = 1`）。整数倍なので線幅が割れない（F-281）。

### まだ入れていないもの（最低限の移植なので）

- アニメーション（登場・退場・選択帯の追従と明滅）
- スクロール、フォルダ、値項目、スライダー、リストボックス、キーボード、通知
- 日本語（美咲ゴシック）。いまのアトラスは ASCII 61 文字
- 表の書き換えとゲームの描画スレッドの排他（チャンク数を最後に書いて緩和はしている）

### 検証（7 本すべて通した。**未ビルド・未適用**）

```
1) 配置検査      下 28 枚 2240/3072B  上 119 枚 9520/10752B  色 4/17（上限 24）
2) 監査          総異常 0 件
3) リテラル検査  異常 0 件
4) アトラス      画素照合の不一致 0 件
5) プレビュー    下 28 枚 4 チャンク / 上 119 枚 17 チャンク
6) 書き出し      ケーブ 6 本 / フック 3 本 / TEV 36 語
7) 移植の照合    ★1 語も違わない
```

### 再検査で見つけた不備 3 件（ビルド前に潰した）

コードを頭から読み直したところ、`GuiRender::Flush` に 3 つの不備があった。

**1. 表からはみ出す（メモリ破壊）**

`Push` は枚数を `Cap()` で頭打ちにするが、`Flush` が書く数は
**埋め草を含む `written`** であって枚数ではない。
色が頻繁に変われば `written = チャンク数 x 7` まで膨らみ、
`COLORS_MAX = 24` で止めても `24 x 7 = 168 枚` になる。
上画面の表は 134 枚なので**隣（ノードや vtable）を踏み潰す**。

→ 止まる条件に `written + kGuiChunk <= cap` を足した。

**2. 何も描かないとき、前の絵が消えない**

チャンク数 0 を書くと、記録ケーブは**記録そのものを見送る**
（`LOG_CUR_CHUNK == 0` で `skip` へ飛ぶ。これは `SelectList` の前）。
その結果ノードの `+0x108`（記録長）が前フレームのまま残り、
**前の絵が replay され続ける**。メニューを閉じられない。

→ 描くものが無くても**大きさ 0 のダミーだけで 1 チャンク出す**ようにした。

**3. 上限に達したときチャンク数を二重に数える**

`if (chunk >= kGuiColorsMax) break;` のあと `open` が真のままなので、
末尾の `if (open) chunk++` で **上限 + 1** になり、
色を書いていないチャンクを「ある」と申告していた。

→ ループを「同じ色が連続する範囲を 7 枚ずつ詰める」形に書き直し、
`open` のような状態変数を無くした。止まる条件を 3 つとも `while` の頭に書いた。

**1 と 2 は実機に入れたら壊れていた。**（1 はメモリ破壊、2 はメニューが閉じられない）

書き直したあとも `verify_plugin_port.py` は**1 語も違わない**ままだった
（照合器も同じ形に直して突き合わせた）。

### ビルドした

```
/c/devkitPro/msys2/usr/bin/bash -lc 'cd "/a/Disassemble/acnl/Plugin/..." && make clean && make'
→ linking CTRPluginFramework-BlankTemplate-0.8.0.elf
  creating CTRPluginFramework-BlankTemplate-0.8.0.3gx
```

**警告 0 件・エラー 0 件。** 途中 `main.cpp` の文字列に生の改行が入っていて
一度失敗したが（スクリプトで `\n` を書き込むときのエスケープ漏れ）、直して通した。

成果物に正しいデータが入ったかをバイト列で確かめた。

| 探したもの | 結果 |
|---|---|
| `kGuiCaveQ` 先頭 8 語 | 見つかった @0x72904 |
| `kGuiCaveA1` 先頭 8 語 | 見つかった @0x73178 |
| `kGuiCaveA2` 先頭 8 語 | 見つかった @0x73030 |
| `kGuiCaveN` 先頭 8 語 | 見つかった @0x72F14 |
| `kGuiTev` 先頭 12 語 | 見つかった @0x72F40 |
| フォントアトラス 先頭 256 バイト | 見つかった @0x6C667 |
| 文字列 `ACNL MENU` / `WALK SPEED` / `SELECT = MENU` | いずれも有り |

`CTRPluginFramework-BlankTemplate-0.8.0.3gx` 779,785 バイト。**実機ではまだ試していない。**

---

