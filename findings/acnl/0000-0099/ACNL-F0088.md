---
id: ACNL-F0088
aliases:
- F-50
title: F-50 UI アニメと画面遷移（Wipe）— 調整点は `0x568BF8` 一箇所 — `HIGH`
summary: 「持ち物・マイデザを開くときの画面遷移を一瞬にしたい」の解析。**静的 IDB のみで実施。**
date: '2026-09-08'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5671928
- 9377920
- 9386340
- 9327136
- 1683456
- 1708032
- 9343080
- 2471236
- 9365464
- 9327528
- 1685696
- 1706192
- 5417420
- 5671428
- 5671828
- 5671960
- 5671876
- 5636096
- 5709824
- 7224152
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2674-2748
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-50 UI アニメと画面遷移（Wipe）— 調整点は `0x568BF8` 一箇所 — `HIGH`

「持ち物・マイデザを開くときの画面遷移を一瞬にしたい」の解析。**静的 IDB のみで実施。**

### 関係するクラス（RTTI 逆引き）

マングル名からの逆引き手順を `scratchpad/find_class.py` に落とした
（名前文字列 → その名前を指す `TypeInfo` → その `TypeInfo` を指す vtable）。

| クラス | vtable | 備考 |
|---|---|---|
| `Wipe` | `0x8F1880` | 画面遷移本体。`state::Base<Wipe>` / `state::Mode<Wipe>` |
| `FaderWipe` | `0x8F3964` | Wipe を駆動する fader タスク |
| `BsMenuItem` | `0x8E5220` | ポケット/持ち物。モジュールは `0x19B000`-`0x1A1000` |
| `BsMenuMyDesign` | `0x8E9068` | マイデザ。モジュールは `0x25B544` 付近 |
| `BsMenuMyDesignSelect` | `0x8EE7D8` | |
| `BsMenuMain` | `0x8E53A8` | |

`ui.txt` の「ポケット項目追加」系チート（`0x19B8C0`〜`0x1A08D0`）が
`BsMenuItem` のモジュール範囲に収まることも確認できた。

### 時間を決めているもの

```
Wipe_Init (0x52A9CC)
  UiAnim_Load(this+952 / +992 / +1032, リソース, レイアウト)   アニメスロット 3 つ
UiAnim_Load (0x568A04)
  ... 末尾で UiAnim_Init(a1, v11)                              ★ここでレートが入る
UiAnim_Init (0x568B94)
  this+16 = flt_568BF8 (= 1.0f)    ← ★g_UiAnimRate
  this+4  = 総フレーム数
  this+8  = 0.0 (現在時刻)
```

`UiAnim_Set` (`0x568C18`) が `S1 -> this+16`、`S2 -> this+8`、`S0 -> this+4` を設定する。
レートは「1 フレームあたり何フレーム進むか」。

### `0x568BF8` が唯一の調整点である根拠

1. **このリテラルを参照する命令は全域で 1 つだけ** — `UiAnim_Init` 内の
   `VLDR @0x568BC4`（LDR/VLDR の PC 相対を `0x560000`-`0x572000` で全走査）
2. **`Wipe` も同じ経路を通る** — `Wipe_Init` の 3 つの `UiAnim_Load` が
   末尾で `UiAnim_Init` を呼ぶ
3. **`FaderWipe_Update` (`0x6E3B58`) は固定フレーム待ちを持たない** —
   `Wipe_IsIdle` を見て state 2→1 / 3→0 と進めるだけ
4. **メニュー側に時間定数がない** — `BsMenuItem` モジュール
   (`0x19B000`-`0x1A1000`) の PC 相対リテラルを全部拾ったが
   **float 定数はゼロ件**。`BsMenuMyDesign` も `2.0` が 1 つあるだけ

`UiAnim_Init` の呼び出し元は 127 箇所あるが、**すべて低レベル UI ライブラリ領域**
（`0x13xxxx`-`0x34xxxx` と `0x4Dxxxx`）で、`BsMenuItem` / `BsMenuMyDesign` /
`Wipe` の各モジュールからの直接呼び出しは 0 件。
つまりメニューも Wipe も**フレームワーク経由で同じレートを共有している。**

### 値の選び方

`REFERENCES/CHEATS/speed.txt` は `7F7FFFFF`（FLT_MAX、高速メニュー表示）と
`77777777`（5.0e33、画面切り替え）を使っているが、**どちらも勧めない。**
現在時刻に毎フレーム加算される値なので 2 フレーム目で `inf` に達し、
`現在時刻 / 総フレーム` のような補間で `NaN` を生む余地がある。

**`43B00000` (352.0) で十分。** UI アニメは通常 60 フレーム以下なので 1 フレームで終端に届く。
`ui.txt` の「メニューアニメーションをカット」が使っている値でもある。

### カットできないもの

これはアニメの再生速度を変えるだけで、**レイアウトやリソースの読み込み時間は短くならない。**

### 副作用

グローバルなので**全 UI アニメが速くなる。** ポケットとマイデザだけに効かせるには
コードケーブが要る（未実装）。

---

