---
id: ACNL-F0106
aliases:
- F-68
title: 'F-68: オフラインなら profile の HairStyle だけを書いて `vc_UPDATE` すれば即時・装備保持にできる'
summary: 'confidence: **HIGH**（静的経路に加え、オフライン実機で即時反映・衣装8枠維持を確認）'
date: '2026-08-24'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6826388
- 6826664
- 9754184
- 3140448
- 6856156
- 6828776
- 6828788
- 6838180
- 6838192
- 6826528
- 6604424
- 6826600
- 6826636
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4575-4638
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-68: オフラインなら profile の HairStyle だけを書いて `vc_UPDATE` すれば即時・装備保持にできる
confidence: **HIGH**（静的経路に加え、オフライン実機で即時反映・衣装8枠維持を確認）

男「けだるいゆるさ」は `REFERENCES/CHEATS/player.txt` の対応から HairStyle `0x0C`。
状態 `0xB9` を短縮するのではなく、既知のAアクション入口
`PlayerAction_TryBugNetSwing` (`0x682994`) の `BL Actor_SetState` (`0x682AA8`) を
CTRPF空ページ `0x01E81400` のケーブへ差し替えた。

ケーブの本体は次の最小経路である。

```c
if (*(u8 *)(*(u32 *)0x94D648 + 0x1326F) != 0) {
    return Actor_SetState(player, 0x70, 0, 0); // オンライン時は元処理
}
profile = vc_PSOFFSET(player->playerNo);       // 0x2FEB60
if (!profile) {
    return Actor_SetState(player, 0x70, 0, 0);
}
profile->HairStyle = 0x0C;                     // profile+4 だけ
vc_UPDATE(player);                             // 0x689DDC
return 1;
```

`profile+5` の HairColor、`profile+10` からの Outfit には書き込まない。
`vc_UPDATE` は同じプロフィールから髪色・衣装を読み直すため、通常の装備値を保ったまま
アクターの `+0x942/+0x944` と描画を即時更新する。Hat / Accessory を空にする
`0x6832E8/0x6832F4` と `0x6857A4/0x6857B0` は状態 `0xB9` 内にしかないため通らない。

### 実機設置時の確認（2026-08-24）

- processor `ARM`、debug IDB image base `0`、process state suspended
- `g_NetGameMgr = 0x320051D8`、`[manager+0x1326F] = 0`（オフライン）
- `0x682A20/68/8C` と `0x682AA8` は全て元命令
- `0x01E81400-0x01E817FF` は全てゼロ
- 設置後はゲート3箇所 `E1A00000`、hook `EB5FFA54`
- ケーブ96バイトの読戻し一致。IDAで `BL 0x2FEB60`、`BL 0x689DDC`、
  オンラインfallback `B 0x64C688` を逆アセンブル確認
- `dbg_continue` でゲームを再開

実装は `PATCHES/cave_hair_instant.py`。`MODE="uninstall"` は最初にhook、次にゲートを
元へ戻し、最後にケーブ96バイトをゼロ復元する。Aアクションを占有するため使用後は外す。

### 動作確認と復元（2026-08-24）

ユーザー実機確認では、Aボタンを押すと男「けだるいゆるさ」が即時反映され、
**衣装枠は8枠全て変更されなかった**。狙いどおり状態 `0xB9` の装備消去と
2段アニメ待ちの両方を回避できた。オンラインでは検証していない。

確認後に同スクリプトの `MODE="uninstall"` をida-pro-mcpから実行した。
復元後の実機読戻しは次のとおり。

| addr / range | 復元後 | 状態 |
|---|---|---|
| `0x682A20` | `0A000026` | original |
| `0x682A68` | `1A000014` | original |
| `0x682A8C` | `1A000008` | original |
| `0x682AA8` | `EBFF26F6` | original `BL Actor_SetState` |
| `0x01E81400-0x01E8145F` | 全ゼロ | cave解放済み |

髪型のプロフィール値 `0x0C` 自体は戻していない。UninstallはA入力フックだけを外す。
スクリプトの既定モードは誤設置を避けるため `status` に戻した。

---

