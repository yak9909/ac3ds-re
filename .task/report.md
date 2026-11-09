（ワーカーの最終の返答を司令塔が保存した）
対象の命名・型付けと symbols 反映を完了しました。

## 未確認点

実機未測定です。遷移引数それぞれの意味、枯死アイテム ID 3/4 の樹種は未確定です。

## 迷った判断

樹種を推測せず、成長関数名に `ToItem3`・`ToItem4` を使いました。日次処理ラッパーは安定した返値を確認できないため `void` としました。

## 依頼の範囲外の変更

なし。

## 使ったゲームの事実

すべて MEDIUM（本体・独立した呼出元・転送先の静的照合）。

- `0x30C994`：無引数の住民日次処理。`Villager_RunDailyUpdateOnce`。
- `0x309F18`：セーブポインタから番号 0〜3、不一致/null は 4。`PlayerSave_GetSlotIndex`。
- `0x5B464C`：現在部屋の出口を使用。`Room_UseExit`。第6引数は整数。
- `0x956231`：処理開始前に立つ u8 ガード。`g_VillagerDailyUpdateGuard`。
- `0x316344`・`0x3163C4`：苗を ID 3/4 に置換。両関数の範囲は各 `0x64` byte。

## 訂正の提案

[ACNL-F0749](/A:/Disassemble/ac3ds-workspace/_local/worktrees/ac3ds-re/127/findings/acnl/0700-0799/ACNL-F0749.md) で ACNL-F0388 の第6引数 `float` 説を訂正しました。

`0x316392`・`0x316412` は BLX 命令先頭です。次命令は `0x316396`・`0x316416`、Thumb の LR はそれぞれ `0x316397`・`0x316417` です。
