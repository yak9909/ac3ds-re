（ワーカーの最終の返答を司令塔が保存した）
DONE_WITH_CONCERNS

両変数に `unsigned int *` を設定し、symbols に反映しました。名前と既存コメントは維持しています。

## 未確認点

通常 audit は配布済み依頼資料の既存指摘 3 件で失敗します。`audit --ci` と `kb.py lint` は通過しました。新規の実機確認は行っていません。

## 迷った判断

指す先は 32 ビットのコマンド語列と判断しました。`GpuCmd_Advance` の引数単位はバイトのままです。

## 依頼の範囲外の変更

なし。

## 使ったゲームの事実

- `0x0096EA94`：`GpuCmd_SplitAndSubmit`（`0x001280CC`）で 32 ビット語を書き、カーソルを更新する。型判断 MEDIUM。
- `0x0096EA98`：`GpuCmd_SelectList`（`0x001216BC`）で `base + size` を設定し、書き込み位置との境界比較に使う。型判断 MEDIUM。
