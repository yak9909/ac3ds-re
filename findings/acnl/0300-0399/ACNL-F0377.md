---
id: ACNL-F0377
aliases:
- F-351
title: 'F-351（2026-09-07）: 入力遮断をプラグインへ実装し、下画面ロックへ一本化した'
summary: '**confidence: HIGH（実機で機構を確認）/ MEDIUM（プラグイン版は実機未確認）**'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5492212
- 10186768
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:22740-22807
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-351（2026-09-07）: 入力遮断をプラグインへ実装し、下画面ロックへ一本化した

**confidence: HIGH（実機で機構を確認）/ MEDIUM（プラグイン版は実機未確認）**
前提: F-350（解析）。実機で**デバッガから入れて動作確認済み**
利用者確認: 「スライドパッドのみ操作でき、その他のボタンは効きません。成功です。」

### 決めた仕様（利用者の指示）

| 対象 | 挙動 |
|---|---|
| スライドパッド | **常に許可** |
| SELECT | **常に不可**（旗に関係なく、ケーブが常時落とす） |
| タッチパネル | **下画面ロックが立っているときだけ不可** |
| その他のボタン | **自前メニューを開いている間だけ不可** |

### 実機での確認（デバッガ版）

ケーブ `0x00838020`（18 語）+ フック `0x0053CDF4` を入れ、
制御ブロック `0x009B7010` を `01 01` にして操作してもらった。
**スライドパッドだけ効き、他は全部死ぬ**ことを確認。10 秒オフ→再適用も正常。
確認後、フック→ケーブの順で撤去し、素に戻した。

### プラグインへの実装

| ファイル | 変更 |
|---|---|
| `PATCHES/input_block_cave.py` | **新規**。ケーブの生成元（`Asm` は `textwriter_cave` を借りる） |
| `PATCHES/export_gui_v2.py` | 入力遮断ケーブを `GuiCavesV2.h` へ出す（`kGuiInput*`） |
| `Sources/OwnGui.cpp` | `InstallInputBlock()` / `RemoveInputBlock()`。Enable の最後に入れ、Disable の最初に外す |
| `Includes/GuiV2.hpp` / `Sources/GuiV2.cpp` | **下画面ロック**（`SetBottomLock` / `BottomLocked` / `DrawBottomDim` / `SetButtonBlock`） |
| `Sources/GuiMenu.cpp` | `SyncInputLock()` を **毎フレーム**呼ぶ。下画面の暗幕を廃止し `DrawBottomDim` へ一本化 |
| `Sources/GuiKeyboard.cpp` | 自前の暗幕を廃止。`DimColor()` / `DimFadeMs()` を公開 |
| `PATCHES/verify_plugin_port_v2.py` | 群 4 に 8 検査を追加（語列の一致・フック・SELECT/スライドパッドの命令・暗幕が 1 箇所・ボタン遮断の連動） |

### ★下画面ロック（暗幕の一本化）

```cpp
void GuiV2::SetBottomLock(bool on, u32 color = 0xB8111410, int fadeMs = 180);
void GuiV2::DrawBottomDim(u32 now);     // BuildBottom の先頭で呼ぶ
```

- **暗幕は 1 箇所からしか出さない。** キーボードもリストボックスも自前で描かない
- 色とフェード時間は**引数で変えられる**（キーボードは `DimColor()` / `DimFadeMs()` を渡す。
  文字入力は薄め `0x61000000`、数値入力とリストボックスは `0xB8111410`）
- **ロックが立つと同時にゲーム側のタッチを遮断する**（暗くなる前に触れないように）
- 状態は `GuiMenu::SyncInputLock()` が**毎フレーム条件から決める**。
  ★開閉のたびに呼ぶ形にすると経路が増えたとき取りこぼす

```
下画面ロック = 下画面リストボックス（閉じ始めるまで） or 入力待ち or キーボード
ボタン遮断   = 自前メニューが開いている（g_visible）
```

### 検査

`verify_plugin_port_v2.py` 8 群 異常 0 件 / `verify_spec_v3.py` 8 群 異常 0 件 / `make` 成功。

### ★実機未確認

プラグイン版はまだ実機で動かしていない。確認すること:
1. メニューを開くとゲームのボタンが死に、閉じると戻る
2. SELECT がメニュー開閉以外でゲームに届かない（常時）
3. キーボード／下画面リストボックスで暗幕が**フェードして**出て、タッチが死ぬ
4. 暗幕が二重に濃くなっていない（一本化できているか）
5. GUI を OFF にすると `0x0053CDF4` が素に戻る

---

