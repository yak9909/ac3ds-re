---
id: ACNL-F0336
aliases:
- F-311@v1:RE/FINDINGS.md:20459
title: 'F-311 追記: 実機で描画されなかった原因（2026-09-06）— HIGH'
summary: プラグインを ON にしても**何も描画されず、Select でメニューも開かない**。
date: '2026-09-06'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:20459-20534
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-311 追記: 実機で描画されなかった原因（2026-09-06）— HIGH

### 症状

プラグインを ON にしても**何も描画されず、Select でメニューも開かない**。

### 実機ログが原因を確定させた

```
上ノード list=40 記録長=0 / 32768 B (0%)
下ノード list=41 記録長=0 / 32768 B (0%)
```

`list` が 0 でない＝**A1/A2 のケーブは動いてコマンドリストを作れている**。
なのに**記録長が 0**。これは基準仕様 v2 §5.2 の「detach」と同じ状態で、
**`node+0x20`（root Pane）が 0** であることを意味する。
（比較: v1 のログは `記録長=1072`）

### 真因 — `.bss` の初期化が後から上書きしていた

`OwnGui::Enable()` の順序が

```
1. 借用  →  2. GuiV2::Install()（node+0x20 に root Pane を書く）
         →  3. ケーブ  →  4. InitBss()  →  5. フック
```

で、**4 の `InitBss()` がノード 0x140 バイトを `memset` する**ため、
2 で書いた `node+0x20`（root Pane）と `node+0x30`（DrawInfo）が消えていた。

**正しい順序**（修正後）:

```
1. 借用  →  2. InitBss()  →  3. GuiV2::Install()  →  4. ケーブ
         →  5. ★node+0x20 の検査  →  6. フック
```

★教訓: **「あとから全体を初期化する処理」を、個別の欄を書いたあとに置かない。**
`.bss` の初期化は必ず個別設定より前。

### ついでに直した 5 件（同じ型の事故を予防）

| | 内容 |
|---|---|
| 1 | **`Commit()` が生きているオブジェクトを `memset` していた。** `memset` は vtable を 0 にするので、描画スレッドが子リスト経由で `DrawSelf` を呼ぶと `BLX 0` で死ぬ。→ Install で全 Picture を有効な状態（不可視）で作り、Commit は位置・大きさ・色・可視だけ書く |
| 2 | **輪の公開順。** `root+0x14`（先頭）を最後に書くようにした。途中の鎖を見せない |
| 3 | **`node+0xB0`（DrawInfo+0x80）を Install でも設定。** 従来は Commit で文字があるときだけだった |
| 4 | **矩形の塗り潰し UV が 1 テクセルしかなかった。** `make_font_nwfont.py` にマス 255（列 15 / 行 15）の塗り潰しを足し、その内側を使う（v1 と同じ方式）。CMAP は 0x20..0x7E しか写像しないので字形には影響しない |
| 5 | **`FillSlot` が TextBox の `+0xFE`(dirty) を立て直していなかった**（§3.1）。一度描いたあと文字を変えても組み直されない恐れがあった |

さらに、**組み込んだ直後はメニューを開いた状態**にした（ON にした時点で描画が出るので
動作確認がその場でできる。Select で閉じられる）。

### ★検証器が捕まえられなかったので群 8 を足した

`verify_plugin_port_v2.py` の 7 群は**全部通っていたのに実機で描画されなかった**。
番地も数値も一致していたが、**呼ぶ順序**は見ていなかった。

群 8「実装の順序と禁止事項」を追加した:

1. `Enable()` の中で `InitBss()` → `GuiV2::Install()` → `InstallHooks()` の順であること
2. `Commit()` とそこから呼ぶ関数が `memset` しないこと
3. `Install()` が `node+0x20` / `+0x30` を書くこと
4. **塗り潰しの UV 範囲がアトラスで全部点灯していること**（実際にアトラスを読む）

★この群自体も 1 度誤判定した（説明コメント中の `GuiV2::Install()` を拾った）。
**ソースを検査するときはコメントを落としてから探す。**

### 状態

- `verify_plugin_port_v2.py` 8 群 / `verify_own_font.py` / `verify_spec_v2.py` すべて 0 件
- `gohan.3gx` 784,878 B（クリーンビルド、警告 0）
- **実機での再確認はこれから**

---

