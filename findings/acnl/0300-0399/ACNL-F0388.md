---
id: ACNL-F0388
aliases:
- F-361
title: 'F-361（2026-09-08）: ★★★ACNL は CRO 動的モジュールを使う — しずえ画面を静的に解いた'
summary: 'confidence: **HIGH（静的で完結。実機のバイト列と 1 命令も違わず一致）**。'
date: '2026-09-08'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8900608
- 1048576
- 3143980
- 3125064
- 5981772
- 3127552
- 3186456
- 3126100
- 3178768
- 11178316
- 9769786
- 9742044
- 5555236
- 5556296
- 11254088
- 9741264
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23495-23620
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-361（2026-09-08）: ★★★ACNL は CRO 動的モジュールを使う — しずえ画面を静的に解いた

confidence: **HIGH（静的で完結。実機のバイト列と 1 命令も違わず一致）**。
詳細は `scratchpad/MEMO_f361_cro_plselect.md`。

### 1. これまで「静的に読めない領域」と呼んでいたものの正体

**`NCCH/romfs v1.5/` に `Module*.cro` が 38 本**（+ `.crr/static.crr`）。
場面ごとに別モジュールが `0x00B00000`〜へロードされる。
★F-359 の「起動ごとに配置が変わる」は**「場面ごとに変わる」が正しい**（訂正）。

### 2. `NCCH/0004000E00086200.code` = 実機ビルドの完全な `.code`

アップデートタイトルの `.code`（8,900,608 B = 0x87D000）。
7 アンカー（各 20 バイト）が**すべて base `0x00100000` で一致**
（`Room_RequestChange` / `Room_UseExit` / `vc_ROOMDAT` / `Framework_MainLoop` /
`fgobj_Proc_Setup` / `BsSvMgr_initialize` / `Room_GetCurrentId`）。
→ **`code_runtime.bin`（10MB の切り詰め）の上位互換。VA = ファイルオフセット + 0x100000。**

★`NCCH/exefs/code.bin` は**別ビルド**で、同じ処理を**静的リンク**している。
論理を読むだけなら使えるが**番地は取らないこと**。

### 3. `ModulePlSelect.cro` = 部屋 `0x63`（しずえ画面）

`.text` file `0x180` / size `0x5030`。この起動でのロード先 **`0x00BE5180`**。
**`.text` をその番地に置くと実機から読んだバイト列と完全一致**（`cmp r0,#13` まで）。

インポート解決: 匿名インポート 450 件。
パッチ先 = `TEXT_LOAD + (patch.segOff>>4)`、参照先 = **`0x00100000 + (entry.segOff>>4)`**。
検算: `0xBE5294 -> vc_PLAYER_2_PPOFFSET(0x2FF92C)` / `0xBE529C -> Save_GetTownBase(0x2FAF48)` /
`0xBE54F8 -> Room_UseExit(0x5B464C、実機で読んだ値と一致)`。

### 4. イベントハンドラと「村へ行く」分岐

ハンドラは `.text+0x18B4`、直前のプールに `"SYS_Start"`。
`id = *(u16*)…; if (id >= 13) return; switch(id)` の 13 分岐。**[1] が「村へ行く」**。

```c
void *p = sub_2FB900();                          // 0x002FB900  ★準備完了ガード
if (!p) return;
int idx = sub_309F18(vc_D_GARDEN() + 0xA0, p);   // 0x00309F18 / 0x002FB354
Room_UseExit(vc_ROOMDAT(), idx, 1, 0, 1, 1.0f);  // 0x005B464C / 0x00308110
```

- `sub_2FB900` = `sub_6070CC()` が偽なら `*(u32*)0x00AA914C` を返す。
  **`0x00AA914C` = 選択されたプレイヤーのセーブへのポインタ**
- `sub_309F18(base, p)` = `p` が `base + n*42112`(0xA480) のどれかで **0..3** を返す
  （該当なしは 4）。**プレイヤー番号そのもの**
- 実機観測の `R1 = 0`（スロット 0）と一致

### 5. チート（安定番地のみ・推測ゼロ・★実機未検証）

```c
if (*(u8*)0x0095133A != 0x63) { fired = 0; return; }
if (fired) return;
void *p = sub_2FB900();                 // 0x002FB900
if (!p) return;                          // ゲーム自身のガード
int idx = sub_309F18(vc_D_GARDEN() + 0xA0, p);
if (idx > 3) return;
Room_UseExit(vc_ROOMDAT(), idx, 1, 0, 1, 1.0f);
fired = 1;
```

**「N フレーム待つ」等の当てずっぽうが不要**。ゲーム自身の準備完了判定と
プレイヤー番号計算を借り、`SYS_Start` イベントを待たずに case[1] を実行するだけ。

### 6. 未確認

- **実機未検証**（静的のみ）
- 他の 12 分岐が何か（飛ばして困るものがないか）
- 「準備しています」が `BsSvMgr` mode 7 か（`*(u32*)0x0094A6DC` と `byte[+168]` で決着）

### F-361 追記（2026-09-08）: ★★実機で成功 — しずえ会話スキップ

**利用者確認: 「準備中のロードすら挟まらず、そのままロードして村に出ました。成功しています」**

手順・番地・後始末は **`DOCS/skip_isabelle.md`**（これ 1 本で再現できる）。
ケーブの生成元は `PATCHES/plselect_earlystart.py`（41 語・自己監査つき）。

#### やったこと

ゲームのコードは**1 語も書き換えず**、未使用の `0x00838100` にケーブを置き、
`Framework_ProcOneFrame`(`0x0054C424`) の bp で**メインスレッドのフレーム境界**に止めてから
PC を 1 回だけケーブへ向け、終了後に**全レジスタと PC を完全復元**した。

ケーブは `ModulePlSelect.cro` の分岐 [1] と同じ手順:

```
p   = sub_2FB900()                        0x002FB900  ★ゲーム自身の準備完了ガード
idx = sub_309F18(vc_D_GARDEN()+0xA0, p)   0x00309F18 / 0x002FB354
Room_UseExit(vc_ROOMDAT(), idx, 1, 0, 1, 1.0f)   0x005B464C / 0x00308110
```

#### 実機で得た値

```
注入前   room = 00 5E 63 A5 00 / 0x00AA914C = 0x31F49AA0
停止点   PC = 0x0054C424  LR = 0x0054C848  SP = 0x0FFFFEA8
実行後   CTL+0=1(到達) CTL+1=0 CTL+2=0 CTL+4=0(プレイヤー番号) CTL+8=0x00ABB948
         room = 00 5E 63 00 00（★次の部屋 = 村） / req 0x0094A3D0 = 0x0001
復元後   Resume -> 村へ出た
```

★引数 `(mgr, idx, 1, 0, 1, 1.0f)` は推測ではなく、**ゲームが呼んでいた実引数を bp で読んだもの**。

#### ★分かった副作用（正直に）

**「準備しています」のロードが一度も出なかった。**
つまりこの近道は、本来の「はじめる」経路が走らせている
`BsSvMgr` mode 7「成長処理後のセーブ関係処理」を**飛ばしている**。

- 飛ばしているのが**起動時のセーブだけ**なら実害は小さい
- **成長処理（日付が変わったときの処理）まで**飛ばしているなら、
  草・カブ・住民の更新が走らないおそれがある

**未確認。** 日付をまたいで使って挙動を見るか、
`BsSvMgr`（`*(u32*)0x0094A6DC`）の `byte[+168]`（mode）を通常経路と比べれば決着する。

#### 検証の三本立て（ケーブを実機へ入れる前に必ず）

1. `python PATCHES/plselect_earlystart.py` の自己監査（全 LDR のリテラル・全分岐先）異常 0 件
2. **objdump**（`--adjust-vma=0x00838100`）
3. **実機へ書いたあと ida-pro-mcp で実バイトを逆アセンブル**（BL 5 本の飛び先・リテラル・分岐）

3 本とも一致してから走らせた。

