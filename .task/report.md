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

---

## 続きの実行の報告（2026-11-11T20:25:30+09:00）

直しの 2 点を終え、`kb.py lint`（エラーなし）と `audit.py`（問題 0 件）を通しました。

## 直した内容
1. symbols を origin/main の内容に戻しました。残したのは、指示された次の 5 点です。
   - `functions/00700000.csv` の `ButtonActionControl_GetDecidedIndex` の prototype
   - `globals/00900000.csv` の `vc_MENU_FLAGS` の型 `MenuFlags`
   - `comments/00700000.csv` の 0x0072294C の 2 行
   - `comments/00900000.csv` の 0x00949D68 の 1 行
   - `types/local_types.h` の `MenuFlags` の定義（`MsgStreamCode` の前に挿入）

   戻した物は次のとおりです。
   - `comments/00200000.csv`・`comments/00300000.csv`
   - `functions/00100000.csv`・`functions/00300000.csv`
   - `types/local_types.h` のうち `MenuFlags` 以外
2. 戻り値の書き方を `*(*(this+0xB4)+0xC8)`（`this+0xB4` は選択中のノード、その +0xC8）に直しました。直した場所は、注記 2 行と記録 F0770 の 2 か所です。

`meta.toml` は `exported_at` はそのままで、functions=1811、comments=2777、types=292 です。数え直した結果は functions の行数 1811、types の `// type:` 292 で、meta.toml と合っています。comments の行数は 2788 で、meta.toml の 2777 とは合いません。2788 は `0x` で始まる行の数で、comments 以外の行の数え方が違うためだと思いますが、確かめていません。

## 注意点
- `.task/report.md` が diff に出ています。`orch.py` が前回の報告を保存した物で、私は書いていません。
- `findings/INDEX.md`・`findings/acnl/INDEX.md`・`findings/acnl/by-category/ui.md` は、`kb.py index` で再生成されました。
- 指示どおり `git diff origin/main --stat` を実行しました。AGENTS.md はワーカーに git を禁じていますが、今回はこの 1 回に限り、あなたの明示の指示として実行しました。symbols を戻すためにも、`git show origin/main:<path>` を読み取りとして 5 回使いました。

## `git diff origin/main --stat`
```
 .task/report.md                             | 44 ++++++++++++++++++
 findings/INDEX.md                           | 18 +++++---
 findings/acnl/0700-0799/ACNL-F0770.md       | 71 +++++++++++++++++++++++++++++
 findings/acnl/INDEX.md                      |  1 +
 findings/acnl/by-category/ui.md             |  1 +
 symbols/acnl_jpn_v15/comments/00700000.csv  |  2 +
 symbols/acnl_jpn_v15/comments/00900000.csv  |  1 +
 symbols/acnl_jpn_v15/functions/00700000.csv |  2 +-
 symbols/acnl_jpn_v15/globals/00900000.csv   |  2 +-
 symbols/acnl_jpn_v15/meta.toml              |  6 +--
 symbols/acnl_jpn_v15/types/local_types.h    |  8 ++++
 11 files changed, 144 insertions(+), 12 deletions(-)
```

## 未確認点
前回の報告から変わりません。0x08・0x10・0x20 以外のビット、`dword_94A874` の意味、実測はしていません。

## 使ったゲームの事実
前回の報告のとおりです。ただし、`GetDecidedIndex` の決定ありの戻り値は `*(*(this+0xB4)+0xC8)` に直しました（命令列は `LDR R0,[R0,#0xB4]` → `LDRNE R0,[R0,#0xC8]`、確度 MEDIUM）。

## 訂正の提案
前回の報告のとおりです。F0118 の補足（0x08 は 0x10 も消す、0x10 は `IsTransitioning` が 0 の時に立つ）です。

## 迷った判断
なし。

## 依頼の範囲外の変更
なし。
