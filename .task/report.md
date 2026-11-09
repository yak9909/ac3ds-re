（ワーカーの最終の返答を司令塔が保存した）
`vc_MAPBOOL` に型を付け、`g_NetGameMgrPtr` にも型を付けました。`python tools/audit.py` は問題 0 件、`python tools/kb.py lint` はエラーなしで通っています。`kb.py index` で索引も作り直しました。

型欄とコメントが `symbols/acnl_jpn_v15` に出ているのは、書き出しの CSV で確かめました。型は次のとおりです。

- `vc_MAPBOOL` は `unsigned __int8` です。
- `g_NetGameMgrPtr` は `void *` です。

記録は `findings/acnl/0700-0799/ACNL-F0750.md` の 1 件です。`python tools/kb.py stamp --self` が「モデル名が無い」で失敗したので、`by` は `auto` のままです。

## 未確認点
- `vc_MAPBOOL` の地図が下画面かどうかは、画面の割り当てを追っていないので未確認です。依頼文の「下画面の地図が開いているか」という言い方は採りませんでした。
- `0x6D0928` の部屋条件（`Room_HasFlags` の各値）と、画面 ID `0x21A..0x21F` の意味は未確認です。`0x219` が村の地図（`BsMenuMapVillage`）かどうかも、型との直接の対応を取っていません。
- 実機で旗の 0/1 の遷移を見ていません。2 件とも静的解析だけです。
- `NetGameMgr` の構造体は無いので、`g_NetGameMgrPtr` は `NetGameMgr *` にできていません。大きさは 0x13300 以上が要ります。別作業です。
- `export_symbols.py` の出力は、`git` を使えないため差分の範囲を確かめていません。

## 迷った判断
- `vc_MAPBOOL` は名前を変えず、型だけにしました。`docs/naming.md` の「`vc_` で始まる既存の旧名はそのまま残す」に従っています。`g_NetGameMgrPtr` も規則に合っていたので据え置きです。
- 役割の言い方は「村の地図メニュー作成完了の旗」としました。確度は MEDIUM です。
- `by` の欄は、`stamp` が失敗した（上記）ので `auto` のままにしています。仕上げでの記入をお願いします。
- `audit.py` が記録の CRLF を指摘したので、LF に直しました。

## 依頼の範囲外の変更
- `kb.py index` で、`findings/INDEX.md`、`findings/acnl/INDEX.md`、`findings/acnl/by-category/ui.md` などの索引（24 ファイル）を作り直しました。
- `export_symbols.py` は IDB 全体を書き出す道具です。作業ツリーの `symbols/acnl_jpn_v15` にある functions・globals・comments・`meta.toml`・`types/local_types.h` が更新対象でした。今回の目的以外の差分が混じっていないかは、司令塔が差分で見てください。
- `export_symbols.py` は既定の Python では動きませんでした（`idapro` が無い）。`_local/venv/idalib` の Python で実行しました。

## 使ったゲームの事実
- `0x949C30` `vc_MAPBOOL`（1 バイトの旗、MEDIUM）
  - 書き込みは 1 バイト（STRB）です。
    - `0x2B3A04..0x2B3A0C` `BsMenuMapVillage_CreateStep` の最終段で 1 を入れます。
    - `0x2B3CA8` `sub_2B3C64` の破棄段で 0 にします。
    - `0x6D0928` `sub_6D0928` が別種の地図画面を `UiScreen_OpenById(0x21A..0x21E)` で開くときに 0 にします。
  - 読み取りは 1 バイト（LDRB）の真偽判定です。
    - `0x6D0B54` `BsMenuMgr_MapOutByKind`
    - `0x6D1428` `BsMenuMgr_ProcessMapCommand`
    - `0x6D1E14`
    - `0x6D34AC`
    - `0x6D474C` `BsMenuTab_TabSelectUpdate`
- `0x94D644` `g_NetGameMgrPtr`（`NetGameMgr` 本体へのポインタ、MEDIUM）
  - 書き込みは 3 か所です。
    - `0x616D8C` `sub_616D8C` は、未設定のときに `sub_618614` の返値を保存します。
    - `0x61769C` と `0x6176EC` は、破棄時に `sub_618868` を呼んだあと `nullptr` を入れます。
  - `0x182488` は `*(g_NetGameMgrPtr + 0x229) = 1` を書きます。
  - 隣の `0x94D648`（`vc_GAMEPOINTER`）は `SingletonDisposer`（vtable `0x904FC4`）で、本体ではありません。既存の ACNL-F0633 の周辺訂正と一致します。

## 訂正・統合・タグの提案
- なし。
