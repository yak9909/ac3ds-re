---
id: ACNL-F0538
aliases:
- IDA-opus-5-F030
title: グリッドカーソルを gohan へ。起動時クラッシュの診断とケーブ衝突（2026-09-22、HIGH、静的＋クラッシュダンプ）
summary: '解析ソフト: IDA / 解析モデル: opus-5。利用者の指示で、試験チートを**独立プラグインではなく'
date: '2026-09-22'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3636-3722
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F030: グリッドカーソルを gohan へ。起動時クラッシュの診断とケーブ衝突（2026-09-22、HIGH、静的＋クラッシュダンプ）

解析ソフト: IDA / 解析モデル: opus-5。利用者の指示で、試験チートを**独立プラグインではなく
gohan の自前メニューの「テスト」フォルダ**として作り直した。併せて、独立版が起動時に落ちた件を診断した。

### 1. 起動時クラッシュの正体（独立版 `gridcursor.3gx`）

症状は「3DS ロゴの段階で、3gx 読み込みの青フラッシュの直後に上下画面が赤く光って停止」。
Luma のクラッシュダンプ（`work/evidence/gridcursor/crash_dump_00000012.dmp`）を解いた:

| 欄 | 値 |
|---|---|
| 例外種別 | **3 = データアボート**、ARM11 |
| PC / LR | どちらも **`0x07023A9C`**（プラグイン領域） |
| r0 | **0** |
| 落ちた命令 | `ldr r3, [r0, #0x138]` |
| 関数 | **`CTRPluginFramework::ThreadExit()`**（`0x07023A94`） |

`ThreadExit` は直前で `threadGetCurrent()` を呼び、その戻り値の `+0x138` を読んで
「そのスレッドの入口が `0x07000000` 以上か（＝プラグインのスレッドか）」を見る。
**`threadGetCurrent()` が 0 を返した**のでそこで落ちている。

**`ThreadExit` は CTRPF の後始末経路**で、初期化に失敗したときに行き着く先でもある。
つまりこれは「自前のコードがゲームを壊した」ではなく「**枠組みが起動に失敗して畳んでいる**」形。

**原因はほぼ `plgInfo` の `MemorySize: 2MiB`。**

- Luma の `file_loader.c` は **5 / 2 / 10 MiB** の設定を持ち、`heapSize = 総量 − exeSize`
  （旧 F-404 の実測と公式ソース）。
- CTRPF は**内部ヒープに 1 MiB** を newlib から予約する（旧 F-404）。
- 独立版の実行像は約 570 KB。2 MiB だと残りは 1.4 MiB ほどしかない。
- **このプロジェクトで動いた実績のあるプラグインは全部 5 MiB か 10 MiB。** gohan は 10 MiB。
  `2MiB` は gohan との唯一の実質的な差だった。

**利用者の見立て「組み込みが速すぎる可能性」は、この証拠とは合わない。**
独立版はメニューを操作するまでゲームへ一切触らず、落ちた時点で自前のコードは 1 行も走っていない
（`PatchProcess` は空、フックは未設置）。症状の出る早さからは自然な読みだが、
落ちているのは枠組み自身の後始末だった。
**なお実験で確かめてはいない**（独立版は廃止したため）。gohan は 10 MiB のままなのでこの問題は消える。

### 2. ケーブの衝突（こちらの方が今後効く）

独立版のスタブは `.text` の空き `0x00838600` に置いていた。
**gohan は同じ番地を field hook cave（`0x00838600`–`0x0083863C`）で既に使っている。**
番地も大きさも完全に重なる。独立プラグインとして動かしている限り顕在化しないが、
gohan へ入れた瞬間に互いのコードを上書きしていた。

`GuiCaves.h` と `FieldHookCaves.h` から gohan の占有範囲を引き直すと:

| 範囲 | 何 |
|---|---|
| `0x00838020`–`0x008380A0` | 入力ケーブ A |
| `0x00838100`–`0x00838200` | 確保／解放ケーブ |
| `0x00838200`–`0x00838310` | 入力ケーブ B |
| `0x00838400`–`0x008384A0` | field hook cave |
| `0x00838500`–`0x008385A8` | field hook cave |
| **`0x00838600`–`0x0083863C`** | **field hook cave（ここに置こうとしていた）** |
| `0x00838680`–`0x008386CC` | field hook cave |
| `0x00838950`–`0x00838AB4` | GuiCave A1 |
| `0x00838CE8`–`0x00838E4C` | GuiCave A2 |
| `0x00838E60`–`0x00838E8C` | GuiCave N |

空きで一番大きいのは **`[0x008386CC, 0x00838950)` の 644 B**。スタブはその中の **`0x00838700`** へ移した。

**`tools/gridcursor/verify_gridcursor.py` が毎回この表をヘッダから引き直して重なりを検査する**ので、
どちらかが動いたらビルド前に落ちる。実機で気付く類の失敗ではなくなった。

### 3. gohan への移植で分かった設計上の制約

- **`GuiMenu::SetToggleHandlers` は大域に 1 組しか持てない。** あとから登録したものが
  前のものを黙って潰す。PlayerMove が占有していたので、**配り手を `Cheats.cpp` に一本化**し、
  各チートは `〜Tick(index, held)` / `〜Disable(index)` を出して「自分の項目でなければ偽を返す」
  取り決めにした。チートが増えるたびに踏む罠だったので、増える前に直した。
- **`GuiMenu::BlockGameDpad()`** があるので、十字キーでカーソルを動かす間プレイヤーを歩かせない、が
  1 行で済む。独立版で自前に作りかけていたものは要らなかった。
- フックは**一度入れたらプロセス終了まで置いたまま**にした。`Hide` は状態を Off にするだけで、
  そのときスタブがやるのは数え上げと比較が数回。**実行中のスタブを別スレッドから消しに行かない**ための
  取り決めで、取り外しは `OnProcessExit`（`GridCursor::Shutdown`）でやる。

根拠: `work/evidence/gridcursor/crash_dump_00000012.dmp` と `crash_analysis.json`、
`gridcursor.elf` の逆アセンブル（`0x07023A94` の `ThreadExit`）、
`src/gohan/Includes/Gui/GuiCaves.h` と `Includes/Cheats/FieldHookCaves.h`、
`work/evidence/gridcursor/verify_gridcursor.json`（76 検査 PASS）、
旧 `reference/old_project/DOCS/system_keyboard_plugin_probe.md` の F-404。
反証条件: 2 MiB でも動く（未実験）、CTRPF の内部ヒープ予約が版によって違う、
gohan のケーブ表がヘッダ以外の場所にもある。

