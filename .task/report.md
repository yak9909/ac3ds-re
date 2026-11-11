（ワーカーの最終の返答を司令塔が保存した）
`vc_MENU_FLAGS` に型 `MenuFlags` を、`ButtonActionControl_GetDecidedIndex` に prototype を付け、symbols に書き出しました。根拠は記録 ACNL-F0770（確度 MEDIUM）です。書き出しの結果は `symbols/acnl_jpn_v15` に出ています。`kb.py lint` はエラーなし、`audit.py` は問題 0 件でした。

## 未確認点
- 0x08・0x10・0x20 以外のビットは意味を確かめていません。enum に入れていません。
  - 0x800: 入場の途中に立て、`BsMenuItem_OpenUpdate` で消します。
  - 0x40・0x80: `BsSkb_*` が使います。
  - 0x100・0x200・0x400。
  - 低位の 1・2・4: 排他的な段階値に見えます。
- `BsSkb_WindowInEnter`（0x57CDC8）は `& 0xFFFFFF67 | 8` で、0x08 を立てるときに 0x10 と 0x80 も消します。0x08 の意味が下画面メニュー以外でも同じかは確認していません。
- `dword_94A874` の意味、`this+0xB4` の型、`this+0xD4` のビット 0 の意味は未確認です。
- 実測（実機・エミュレータでの値の確認）はしていません。静的解析だけです。
- `ButtonActionControl` の型が IDB に無いため、this は `void *` にしました。

## 迷った判断
- 確度は MEDIUM にしました。書き手と読み手の命令列という 2 系統の静的根拠があるためです。
- 名前を付けたのは 0x08・0x10・0x20 の 3 つだけです。enum は `MenuFlags`（`__bitmask`、値は `MenuFlags_EnterStarted`・`MenuFlags_EnterDone`・`MenuFlags_CloseRequested`）です。
- F0118 は書き換えず、`supersedes` も付けていません。F0118 の結論と矛盾するのではなく、補足の訂正になるためです。補足は下の訂正の提案に書きました。
- `kb.py stamp --self` は環境変数 `AC3DS_MODEL` が無く使えなかったため、`--model claude-sonnet-5-5` で押しました。

## 依頼の範囲外の変更
なし。`kb.py index` で索引（INDEX.md など 24 ファイル）が再生成されました。

## 使ったゲームの事実
- `vc_MENU_FLAGS`（0x949D68）の 0x08＝入場を始めた、0x10＝入場し終えた、0x20＝終了要求。確度 MEDIUM。
  - 0x08 と 0x10 は互いに排他です。
  - 書き手: `BsMenuItem_OpenEnter`（0x199F9C）は 0x10 を消して 0x08 を立てます。`BsMenuItem_OpenUpdate`（0x199F44）は `IsTransitioning` が 0 のとき 0x800 を消して 0x10 を立てます。
  - 消す側: `BsMenuItem_CloseUpdate`（0x19AAC0）は `IsTransitioning` が 0 のとき 0x18 を消します。`BsMenuItem_CloseEnter`（0x19AB74）は 0x20 を消します。
  - 0x20 を立てる側: `BsMenuTab_WaitMenuEndUpdate`（0x6D7194）は 0x08 が消えたら 0x20 を立てます。
  - 読み手: `BsMenuTab_LowerMenuSwitchUpdate`（0x6D6060）は 0x08 を待ち、次に 0x10 を待ちます。
- `ButtonActionControl_GetDecidedIndex`（0x72294C）は `int __fastcall (void *this)` です。確度 MEDIUM（命令列のみ）。
  - 決定が無いときは -1 を返します。
  - `this+0xB4` が NULL のときは -2 を返します。
  - 決定があれば `*(this+0xB4+0xC8)` を返します。
  - `this+0xB4` を見る条件は、`this+0xD4` のビット 0 が立っている場合、または `dword_94A874` が 0 でなく `this+0xB8` が `ButtonActionControl_StateDecideAnim`（0x2F6694）で `this+0xBC` が 0 の場合です。

## 訂正の提案
- 対象は ACNL-F0118 です。
  - 「0x08 を立てる」には、0x10 も同時に消す（排他的な段階値）という補足が要ります。
  - 「0x10 は入場完了時に立つ」は、`IsTransitioning` が 0 になったときに立つ、と言う方が正確です。
  - 全体の結論（0x08＝入場を始めた、0x10＝入場し終えた）は命令列と合っています。

## 新しいタグの提案
なし。
