（ワーカーの最終の返答を司令塔が保存した）
49/49 関数の prototype と指定3型を、IDB作業用コピー・symbolsへ反映しました。関数名と既存注記は保持しています。

## 未確認点

実機動作、`unk_` 欄、`void *` の参照先全体は未確認です。確度はすべて MEDIUM。

## 迷った判断

- 更新系の残留 R0 は戻り値に採らず、void としました。
- 未定義型は理由付き `void *` とし、VFP の引数・戻り配置を明記しました。

## 依頼の範囲外の変更

なし。

## 使ったゲームの事実

- 49関数の ABI：各番地・命令列・独立した呼び元は [F0766](findings/acnl/0700-0799/ACNL-F0766.md) の表。MEDIUM。
- UiAnim：40 B。ctor `0x1261EC`、結合・解除・破棄側で照合。MEDIUM。
- ArcResAccReader：584 B。ctor `0x120D54`、配置間隔・ロード側で照合。MEDIUM。
- InstSelect8：4812 B。ctor `0x7C6EB0`、配列構築・派生 ctor で照合。MEDIUM。
