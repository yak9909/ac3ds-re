---
id: ACNL-F0650
aliases:
- Ghidra-gpt-sol-5.6-F012
- G-F012
title: synthetic completion handleでinventory完了契約だけをエミュレートする
summary: '**確度: MEDIUM（静的検証済み、実機未検証）。**'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: Ghidra
addresses:
- 5860484
- 5857672
- 5868524
tags:
- inventory
supersedes: []
source: Ghidra:work/FINDINGS.md:290-348
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F012: synthetic completion handleでinventory完了契約だけをエミュレートする

**確度: MEDIUM（静的検証済み、実機未検証）。**

Ghidra-gpt-sol-5.6-F010で必要なのは、BsMenuItemへ「後でstatus=2になる非負handle」を返すことだと確認済み。stock `Item_PlaceItem` が返すhandleは0..3なので、Ghidra-gpt-sol-5.6-F012では未使用値 `4` をsynthetic handleとして予約する。

custom成功:
- AcBalloon / falling ObjectPresentを生成
- `Item_PlaceItem` は呼ばない
- `Player_DropItem` callerへ `r0=4` を返す

`FieldAction_PollAndFinalize @ 0x596C84` を入口hookし:

```
if (handle == 4)
    return 2;
else
    stock FieldAction_PollAndFinalize(handle);
```

とする。

これによりBsMenuItemはstock同様のstatus-2完了経路:
- selected slot -> g_EmptyItem
- icon refresh
- drag/drop state advance

へ進める一方、FieldAction slot本体は一切allocate/改変しない。

fallbackは修正し、元引数とLRを復元後:

```
LDR r12,=Item_PlaceItem
BX  r12
```

でtail-callする。これによりstock `Item_PlaceItem` は直接 `Player_DropItem+0x108` へreturnする。

現行cave:
- `0x838200-0x83832F`: spawn/fallback
- `0x838330-0x83837F`: custom landing
- `0x838380-0x8383BF`: state helper
- `0x8383C0-0x8383D7`: completion poll hook
- `0x8383D8-0x8383FF`: unused

hooks:
- `0x596188 -> 0x838200`: `EB0A881C`
- `0x598BEC -> 0x838330`: `EA0A7DCF`
- `0x596C84 -> 0x8383C0`: `EA0A85CD`

payload:
- size `0x1D8` (472 bytes)
- SHA-256 `9ecc906c807c162fb7ccecc3b31a8b1d5a99a8d944a790d7e22ddfe9751131d7`

**実機未確認:** drag&drop後のItem消去、icon解放、UI継続操作、Player state 0x16->0x06。

根拠: `docs/balloon_drop_action_replay.md`、`docs/inventory_menu.md`、`work/evidence/balloon_drop_ar_20260915.md`。


