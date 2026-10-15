# 命名規則

IDA・Ghidra・symbols に付ける名前の規則です。監査が書式を検査します。

## 基本

- 英数字と `_` だけを使う（先頭は英字）。ASCII 以外は使わない。
- 確度 LOW の段階では名前を付けない。分かったことはコメントに書く。
- 見た目（疑似C の形）だけから名前を付けない。役割の根拠がある物だけに付ける。
- 既に実名がある物（RTTI のクラス名、SDK・ライブラリの公開名、マングル名）は、それを使う。用途から推測した名前で置き換えない。

## 関数

| 種類 | 形 | 例 |
|---|---|---|
| クラスのメソッド（実名のクラスが分かる） | `<Class>_<Method>` | `PlayerState_PlayMotionAndSound_Enter` |
| クラスが分からない関数 | `<Subsystem>_<Verb><Object>` | `Item_GetParamCategory` |
| SDK・ライブラリ | 公開名（名前空間は `_` でつなぐ） | `sead_Controller_UpdateEdges` |
| 呼び出しをつなぐだけの小関数 | 元の名前 ＋ `_thunk` | `Item_GetParamCategory_thunk` |

- 動詞は `Get`・`Set`・`Is`・`Has`・`Create`・`Destroy`・`Init`・`Update`・`Draw`・`Calc`・`Open`・`Close` などから選ぶ。
- 同じ名前が既にあるときは、意味の違いを名前に入れる（`_2` などの連番は使わない）。

## 変数・データ

| 種類 | 形 | 例 |
|---|---|---|
| 大域変数 | `g_<Name>` | `g_PlayerManager` |
| 定数の表 | `k<Name>Table` | `kItemParamTable` |
| vtable / TypeInfo | `vtbl_<Class>` / `ti_<Class>` | `vtbl_SelectBase` |
| 既存の旧名 | そのまま残す（`vc_` で始まる物など） | `vc_ISLPOINTER` |

## 型

- 構造体・クラスは `PascalCase`（`IslandRuntimeData`）。分かっている部分だけの型は、大きさが全体と違うことをコメントに書く。
- メンバーは `snake_case`。分からないメンバーは `unk_<オフセット16進>`（`unk_1C`）。
- Enum は型を `PascalCase`、値を `<型名>_<値名>`（`ItemCategory_Bell`）。

## スコープ

- ACNL と HHD は別のビルドなので、同じ名前を付けてよい。ただし ACNL の名前を HHD へ、根拠なしに写さない。
