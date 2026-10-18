# 「どこでも掘れる」改造パッチ

すべて仮想アドレス。`.code` のファイルオフセットは **仮想アドレス − 0x100000**。

## 描画実験（boot限定・IPS化しない）

### native 2D Picture/TextBox clone panel（F-149、検証後にuninstall済み）

`PATCHES/cave_ui_picture_clone.py` は `0x4D71B8` の `POP {R4-R6,LR}` を一時caveへ分岐させる。
list id 32の場合だけ、live `P_bg_L_00` / `P_bg_R_00` / `P_soft_L/R/T/B`をそれぞれprivate
cloneへ0x158 bytes、`T_msg_00`を0x108 bytesコピーする。背景からの移動差分を各cloneの
transform `+0x8C/+0x9C`へ加え、Picture 6枚とTextBoxを順にnative drawへ渡す。元Pane、Layoutの
linked list、所有権、永続ファイルは変更しない。stock commitへ更新cursorを返すため、追加panelは
通常のlist 32→main list replayへ載る。話者名Pane/TextBoxは含めない。

- hook: `0x4D71B8`, stock `0xE8BD4070`
- cave: `0x01E81A00-0x01E81C57`、Picture clone: `0x01E81000-0x01E81837`、TextBox clone: `0x01E81840-0x01E81947`
- 適用: `py_exec_file` または `runpy.run_path` に `MODE_OVERRIDE='install'`
- 復元: 同じスクリプトで `MODE_OVERRIDE='uninstall'`。hook/cave/cloneを全てstock/zeroへ戻す。

`SRC_PICTURE`は実機再起動で無効になる。`trace_picture_range.py`で再取得した上で、scriptの
vtable/name検証を通してから使う。現段階では会話中の既存materialを借りる実験であり、IPS化不可。

## パッチ一覧（9件、実機動作確認済み）

| # | アドレス | 元 | 新 | IPSオフセット | 効果 |
|---|---|---|---|---|---|
| 1 | `0x595B00` | `0A00006F` | `E320F000` | `0x495B00` | スコップ使用時の早期 `return -1` を無効化 |
| 2 | `0x598294` | `0A000095` | `EA000095` | `0x498294` | 空マスの地面種別ゲートを無条件化 |
| 3 | `0x598478` | `0A000042` | `EA00001C` | `0x498478` | cat10 の空振り分岐を掘る経路へ転送 |
| 4 | `0x5984EC` | `0A000019` | `E320F000` | `0x4984EC` | 汎用チェーンの「掘れない」分岐を無効化 |
| 5 | `0x598550` | `13A0401A` | `E320F000` | `0x498550` | 掘る(19)がアクション26に上書きされるのを阻止（**必要性未検証**） |
| 6 | `0x662E88` | `0A000150` | `E320F000` | `0x562E88` | 「対象なし」ゲートを無効化（段差対策） |
| 7 | `0x663294` | `0A000028` | `EA000028` | `0x563294` | 全状態を掘る経路へ無条件転送 |
| 8 | `0x680F10` | `0A00000A` | `E320F000` | `0x580F10` | 「掘れる」フラグ(`[player+0x171]` bit5)のチェックを無効化 |
| 9 | `0x5982C4` | `0A000017` | `EA000017` | `0x4982C4` | 埋設フラグを無視（掘り出しイベントを起こさない） |

この 8 件を**まとめて適用した状態で** 岩・アイテム・木・低木・構造物・段差
すべてに対して穴を掘れることを実機確認した。
**個々のパッチの必要性は未検証**（TODO-05）。特に #4 と #5 は、
確認できた経路では通っていない可能性がある。

## 各パッチの根拠

### #1 `0x595B00`
`Player_BeginFieldObjAction` 内。`unk_59FAF4(x,y,165)` が何かを検出し、かつ道具が
スコップ (`R6==2`) のとき問答無用で `return -1` していた。

### #2 `0x598294`
空マスのとき `unk_300A84` の戻り値が 0/1 なら掘れる、2 なら何もしない、それ以外は
`return -1`。無条件分岐にして常に掘る経路へ。

### #3 `0x598478`
cat10 経路の末端。`unk_767D80` と `unk_2FE984` が両方 0 を返すオブジェクトが
`action 16`（何も起きない）に落ちていた。化石やジャイロイドの掘り出しは
`0x5983D8` の手前で分岐するため影響を受けない。

**岩・構造物の両方がこれで直った**（実機）。どちらも cat10 と見られる。

### #4 `0x5984EC`
`FieldObj_ResolveDigAction` の汎用判定チェーンの末端。`Item_IsId(a1,204)` が
偽のとき `0x598558`（カテゴリ判定 → 多くは action 16）へ分岐していた。
NOP により `0x5984F0`（掘る）へフォールスルーする。

**ただし cat10 のオブジェクト（岩・構造物）は `0x59836C` で手前に分岐するため、
このチェーンに到達しない。** 確認できたケースでは通っておらず、不要かもしれない。

### #5 `0x598550`
掘る経路 (`0x5984F0` で `R4=19`, `R1=158`) に入った**後**、`unk_7237D8` が
非0を返すと `MOVNE R4, #0x1A (26)` でアクションIDが上書きされる（assembly で確認）。

**当初これを「岩の跳ね返りの原因」と判断したが、実機では否定された。**
本パッチ適用後も岩は掘れず、岩が掘れるようになったのは #3（cat10 経路）を
当てた後。岩も cat10 だった可能性が高い。
このパッチが何に効くのかは未確認で、不要かもしれない。

### #6 `0x662E88`
`[player+0x171]` bit5 が 0 のとき `0x6633D0` へ飛び、状態を設定せずに
振り下ろしアニメだけ再生して終了していた（段差での素振り）。
**リスク**: bit5=0 では対象マス座標が未更新の可能性がある。

### #7 `0x663294`
状態選択 `[player+0xBDE]` の分岐を無条件化し、`0x4B`(空振り) `0x4C`(跳ね返り)
`0x4D`(跳ね返り) を含む全状態を `0x66333C`（状態74=掘る振り下ろしへの遷移）へ流す。

### #8 `0x680F10`
振り下ろしハンドラ `0x680EBC` 内の bit5 チェック。0 だと
`Player_BeginFieldObjAction` を呼ばずに終了していた。

## 復元

各アドレスに「元」の値を書き戻す。
`PATCHES/apply_patches.py` の先頭の `MODE` を `"revert"` に書き換えて実行すれば一括復元できる
（`"status"` で現在の適用状況を表示、`"apply"` で適用）。

## 未適用・実験中

### 3x3 掘り（クラッシュするため無効）

| アドレス | 元 | 新 | 内容 |
|---|---|---|---|
| `0x598688` | `EB0017C9` | `EB032B37` | `BL Player_StartFieldAction` → `BL 0x66336C`（コードケーブ） |
| `0x66336C`〜 | 元コード236B | ケーブ本体188B | 3x3 ループ |

**クラッシュ確認済み。使用しないこと。** 詳細は `PATCHES/cave_3x3.py`。

## 恒久化

`code.ips` を作って `luma/titles/<TitleID>/code.ips` に置く。
ファイルオフセットは上表の「IPSオフセット」列。

メモリパッチのままだとゲーム再起動で消える。


---

## #9 `0x5982C4` — 埋設フラグを無視（セッション3 追加）

`FieldObj_ResolveDigAction` 内:

```
005982B4  MOV  R0, R6                  ; R6 = 対象アイテム
005982B8  BL   Item_IsBuriedFlag
005982BC  CMP  R0, #0
005982C4  BEQ  loc_598328              ; 埋設でなければ通常経路へ  ← ここを無条件 B に
005982C8  MOV  R0, R6                  ; 埋設ならここから掘り出し処理
005982CC  BL   unk_2FCB64
```

無条件 `B` にすることで埋設フラグに関係なく通常経路へ流れ、
掘り出しイベントが発生せず「何も無い所を掘る」のと同じ挙動になる。

**副作用**: 埋設アイテム（化石・ベルなど）は掘り出せなくなり、掘ると消える。
この挙動が不要なら `PATCHES/apply_patches.py` の `PATCHES` から該当行を外す。

---

# コードケーブ（3x3 マス掘り / 木の伐採）

パッチとは別に、3 箇所のフックで周囲 8 マスを同時に掘る。
木にぶつかって切り倒す改造は `PATCHES/cave_tree.py` が別に 1 箇所フックする。
**すべて `0x663294`（パッチ #7）で死んだ領域か CTRPF の空ページを使う。**
**パッチ #7 を revert する前に必ずケーブを uninstall すること。**

| スクリプト | ケーブ | 範囲 | 命令 | フック | フック元の値 |
|---|---|---|---|---|---|
| `PATCHES/cave_3x3.py` | 穴 | `0x66336C`-`0x663413` | 42 | `0x5A09EC` | `EBFFE245` |
| `PATCHES/cave_particle.py` | 抉れ | `0x6632F0`-`0x66332B` | 15 | `0x65BD58`, `0x65BDEC` | `EB004E09`, `EB004DE4` |
| `PATCHES/cave_particle.py` | 土しぶき | `0x01E81000`-`0x01E8104B` | 19 | `0x65BD2C` | `EB041950` |
| `PATCHES/cave_tree.py` | 伐採 | `0x01E81200`-`0x01E8129F` | 40 | `0x59BBB0` | `EBFFF93F` |
| `PATCHES/cave_hair_instant.py` | オフラインA即時髪型 | `0x01E81400`-`0x01E8145F` | 23 + literal | `0x682AA8` | `EBFF26F6` |

`0x663454` 以降は literal pool（`0xADF864` / `0.2f` / `0x880EFC` / `0x880EF8` / `1.0f`）。
**絶対に上書きしないこと。**

## 恒久化 (`code.ips`) にあたっての注意

- **`0x01E81000` は CTRPF の空ページであり `.code` の一部ではない**。
  IPS には含められないので、恒久化するなら `.text` 内の死にコードへ移す必要がある。
  候補: 領域D `0x598298`-`0x5982B3` (7命令) / 領域E `0x59847C`-`0x5984AF` (13命令)。
  ただし土しぶきケーブは 19 命令なので、分割して橋渡しするか
  他の死にコードを新たに探すことになる。
- パッチ #9 を入れると `0x5982C4`-`0x598327` が新たに死ぬので、
  そこも領域として使える可能性がある（**未走査**）。
- `PATCHES/cave_tree.py` の `0x01E81200` も同じ理由で IPS に含められない。
  こちらは 40 ワード必要。土しぶきケーブ（19 ワード）と合わせて **59 ワード分**の
  死にコードを `.text` 内に確保する必要がある。

## 木にぶつかって切り倒す（`PATCHES/cave_tree.py`、セッション5）

**パッチは 1 つも当てない。** `MODE = "install" / "uninstall" / "status"`。

| アドレス | 元の値 | 新しい値 | 内容 |
|---|---|---|---|
| `0x59BBB0` | `EBFFF93F` | `BL 0x01E81200` | `FieldObj_FellObject` の引数を差し替えるフック |

ケーブ（40 ワード）がやること:

1. スタック引数 `kind` が **0（ぶつかった）以外なら素通し**。揺すり（`kind`=2）は素の挙動
2. そのマスの打撃カウンタ `dword_9AE504` の 2 bit を 3 にする → `R6=1` になり
   **アクション側がマスを切り株へ置換する**
3. `Player_BeginFieldObjAction(X, Y, 1)` を呼ぶ。**`mode 1` は素で
   `FieldObj_ResolveAxeAction` へ行く**ので mode 0 側を書き換える必要はない
4. キューの `item1` を `a2` に、`flags` bit1 から求めた 4/5 を `kind` に差し替える
   → **`FieldObj_FellObject` が倒れる演出を正しい向きで出す**
5. **キューの `[14]`/`[15]` を解放する**

### やってはいけないこと（実機で副作用を確認済み）

| してはいけない変更 | 起きること |
|---|---|
| `0x595B1C` を `0A000082` に | **A ボタンで揺すっただけで木が倒れる** |
| `0x597D94` を `E1A00000`（NOP）に | **斧まで一撃になる** |
| キューを解放しない | 4 スロットが `act=14 state=2` で埋まり**斧も他の動作も効かなくなる** |
| `FieldObj_ApplyDigRecord` でレコード登録 | 32 件超で範囲外書き込み → SIGSEGV（F-39） |

上 2 つは `REFERENCES/CHEATS/trees.txt` 由来。**チートの行は「その機能が実現する」ことしか
保証しない。副作用は自分で確かめること。**

### 詰まったキューの手当て

```
キュー   0x9AE15C + i*18 + 14 <- 0x0000   (actionID と state)
進行中   0x9AE1A4 + i*5  + 2  <- 0xA5     (pNo = 165 = 空き)
レコード 0x9AE244 + i*22 + 17 <- 0x00     (state)
```

該当する `act` のものだけを選んで解放する。

アンカー:

| アドレス | 値 | 意味 |
|---|---|---|
| `0x59BAC4` | `E92D43F0` | `FieldObj_BumpFellCaller` 先頭 |
| `0x59A0B4` | `E92D4FFF` | `FieldObj_FellObject` 先頭 |
| `0x597D5C` | `E2400E51` | 打撃カウンタの index 計算 |
| `0x597D70` | `E7931101` | 同上 |
| `0x595B24` | `0A000080` | `mode 1` → `FieldObj_ResolveAxeAction` |

---

## オフラインA即時髪型（`PATCHES/cave_hair_instant.py`）

`MODE = "install" / "uninstall" / "status"`。JPN 旧版専用の実機ランタイムパッチ。
男「けだるいゆるさ」の内部値は `0x0C`。

オンライン用チートの状態 `0xB9` は使わない。既知のAアクション入口
`PlayerAction_TryBugNetSwing` の判定3箇所を迂回し、元の
`BL Actor_SetState` (`0x682AA8`) だけをケーブ呼び出しへ差し替える。

| addr | original | installed | 内容 |
|---|---|---|---|
| `0x682A20` | `0A000026` | `E1A00000` | Aアクション準備ゲートを迂回 |
| `0x682A68` | `1A000014` | `E1A00000` | 虫取り網種別ゲートを迂回 |
| `0x682A8C` | `1A000008` | `E1A00000` | 状態遷移直前の再判定を迂回 |
| `0x682AA8` | `EBFF26F6` | `EB5FFA54` | `BL 0x01E81400` |

ケーブは次を行う。

1. `g_NetGameMgr` (`0x94D648`) から `+0x1326F` のオンライン人数を読む。
2. 0以外なら保存した `R0-R4,LR` を戻し、元の `Actor_SetState(player,0x70,0,0)` へ
   テールジャンプする。オンライン中は髪型を変更しない。
3. オフラインなら `[player+0x1AC]` のプレイヤー番号を `vc_PSOFFSET` (`0x2FEB60`)
   へ渡し、返ったプロフィールの **HairStyle `+4` だけ**を `0x0C` にする。
4. `vc_UPDATE(player)` (`0x689DDC`) を直呼びし、プロフィールの現在の見た目を
   アクターへ即時再ロードする。

HairColor `profile+5` と Outfit `profile+10` 以降には書き込まない。
`vc_UPDATE` はその現在値を読むので、髪色を保ち、Hat / Accessory を含む装備を
EmptyItem にする状態 `0xB9` の経路を完全に避ける。

2026-08-24 の Remote GDB セッションでは、ARM / image base 0、アンカー7件、
オンライン人数0、ケーブのゼロを確認してから設置した。4パッチと96バイトのケーブは
読戻し一致、ケーブの分岐先もIDA逆アセンブルで確認済み。
実機ではA入力直後に髪型が反映され、衣装8枠が全て維持されることを確認した。
オンラインでは未検証。確認後に `uninstall` を実行し、4箇所の元命令とケーブ全ゼロを
再読込して復元を確認した。スクリプトの現在の既定値は安全な `MODE="status"`。

**制約**:

- Aアクション入口を占有するため、髪型変更を確認したら `MODE="uninstall"` で外す。
- CTRPFの実行可能空ページを使うため、ゲーム再起動で消え、IPSには含められない。
- `vc_UPDATE` は送信処理を持たない。このパッチは意図的にオフライン専用。

---

## 持ち物起動→通常カタログ（`PATCHES/cave_catalog_inventory.py`）

JPN旧版用の一時ランタイムパッチ。`MODE = "install" / "uninstall" / "status"`。
スクリプトの現在の既定値は安全な `status`。

**実機試験で設計不成立と判明したため、現在はuninstall済み。再installしないこと。**

| addr / range | original | installed | 内容 |
|---|---|---|---|
| `0x6D6338` | `EBFFEBFC` (`BL 0x6D1330`) | `EB5EAC70` (`BL 0x01E81500`) | 実測した通常Xのmenu open呼出し |
| `0x01E81500-0x01E8151B` | 全ゼロ | 28バイト | menuId 0→catalog mode 0ケーブ |
| `0x01E8151C-0x01E815FF` | 全ゼロ | 全ゼロ | 競合防止の予約領域 |

通常Xでは実機breakpointで `R0=0`, `R1=1`, `LR=0x6D633C` を確認した。
ケーブはmenuId 0なら `R4,LR` を保存して `vc_CFUNCTION(0)` (`0x6D1BBC`) を呼び、
持ち物専用 `sub_693EE8` を飛ばして `0x6D634C` へ戻る。menuIdが非0なら
R0/R1を保ったまま元の `Menu_RequestOpen` へtail-callする。

初版の `0x16DEC0` フックは通常Xで到達しなかったため棄却し、原分岐とケーブを復元済み。
修正版hookはcall siteなので、ケーブへは必ず `BL` を使う。

installはケーブを先に書いて検証し、入口フックを最後に設置する。uninstallは逆に
入口を最初に原命令へ戻してから、ケーブ28バイトだけをゼロへ戻す。別データがあれば消去しない。

**初回試験の制約**:

- 屋外検索ガードはまだ無い。検索カテゴリは選ばない。
- 家具3D生成はstockのまま。屋外でモデル、位置、カメラ、照明を観察する。
- CTRPFの空ページを使うため再起動で消え、IPSにはそのまま移せない。

### 実機結果と撤回理由

カタログ自体は開いたが、持ち物/マイデザインUIが重なり、X/B終了不能、全カテゴリの3D非表示、
カタログ終了後のplayer state `0x16`と空の下画面残留が発生した。`0x6D6338` は状態名
「メニュー切り替え」の途中であり、持ち物UIの準備後なので差替え位置として遅すぎる。
hookは `EBFFEBFC`、`0x01E81500-0x01E815FF` は全ゼロへ復元した。

下画面復旧用 `PATCHES/recover_bottom_ui_manager.py` は、stock `sub_6D27E8()` をTID 220で
一度だけ実行する専用script。実機で地図と通常X持ち物開閉の復旧を確認後、payloadもcleanup済み。

---

## 持ち物owner統合Catalog adapter（`PATCHES/cave_catalog_inventory_adapter.py`）

JPN旧版用の実験ランタイムパッチ。現在の既定値は `MODE="status"`。
`0x6D6338` のCatalog要求、`0x6D1154` のscreen生成完了、`0x6D6AB8` のタブ退場完了、
`0x21A9FC` のpreview更新、`0x21D078` のCatalog終了、`0x68FD2C` の一時manager容量、
`0x68F4F8` のphase 3 map取得、`0x690FF8` のpreview actor openを、
`0x01E81500-0x01E817FF` のadapterへ接続する。

実機で次を確認済み。

- XでCatalog mode 0を表示できる。
- field上部タブが退場し、Catalogと重ならない。
- 「やめる」後にplayer、タブ、地図、上下画面背景が正常復帰する。
- 第2版までは一時 `BsFtrMgr` の即時失敗でもクラッシュ・freezeはしない。
- 第3版は容量1でphase 1に成功したが、phase 1公開後のpreview競合でSIGSEGVになった。

### 3D manager生成の第2版失敗と容量制限版

初版preview hookはtype `0xEE` の一時 `BsFtrMgr` をroom scene parent下へ生成し、
第2版はsaved `BsMenuTab`下へ変更した。しかし精密再読では両parentとも
`+14=1 / +15=0` で、`UiScreen_OpenChild` のgateを通る。以前記録した
`ScStage +15=1` とfactory前拒否の判定は誤りだった。

第2版でも `owned=0 / status=3 / published=0 / actor=0` が再現した。静的経路ではroom 0容量38により、
phase 1がCPU 3,648,000 bytes、VRAM 988,000 bytesをlate allocationする。CPU bank heapが1件でも
nullならphase 1は失敗し、新規UiScreenは同一呼出し中に破棄される。

第3版sourceは `0x68FD2C` をhookし、adapter activeかつpreview status 0のmanager生成中だけ
容量を1へ制限する。通常の室内manager生成はtable値のまま。完全ready
`(byte[19] & 3) == 3` 待ちとselection cacheの1回再試行も維持する。
sourceの構文・cave sizeを検証し、停止中実機へ適用した。`ftr-capacity` hookは
`0x68FD2C = EA5FC647`、private preview stateは `manager=0/status=0` へ移行し、
全読戻し一致・breakpoint 0件を確認して再開済み。

容量1版ではmanager `+24=1`、create flag `+19=1`、`g_BsFtrMgr`公開まで成功した。
ただし第3版は未ready時もstock preview bodyへ戻っていたため、type `0xBC` actorを早期生成し、
`sub_51FF8C` の仮想call targetがARM命令語 `0xE1A04000`になってSIGSEGVした。

第4版はmanager生成を要求したframe、およびpreview status 1で
`(manager[0x13]&3)!=3` の全frameについて、stock bodyへ入らずpreview updateから直接returnする。
完全ready後だけselection cacheを無効化する。例外停止中に第3版private stateを保持したまま
第4版caveへ移行し、失敗actorの4 vptrを基底 `AcFtr` 値へ戻してstock破棄経路へ渡した。

第4版再開直後の2回目のSIGSEGVは、manager phase 3がfield mapを走査して屋外Item `0x2090`を
type `0xBC`として生成した別経路だった。第5版は `0x68F4F8` の
`Field_GetMapManager` callをguardし、adapter-owned managerのphase 3だけ0を返す。
common初期化とphase 3末尾は実行し、map配置actorのpopulateだけを省く。進行中の例外はactor破棄後
`0x68F8C8`へ送り、manager create flagが`3`になるところまでstep実測した。

manager完成後の3回目は、選択Item `0x2EA3`のItemParam family 1が正規にtype `0xBC`
(`AcFtrLoop`)を選び、同じgeneric createの `vptr+8=0xE1A04000`で停止した。例外objectの
4 vptrを基底`AcFtr`へ戻して再実行すると、pre/create/postの3 virtual callは全て成功し、
create result 2、`g_CatalogPreview+0=0x30C51C70`まで進んだ。

第6版は `0x690FF8=EB5FC17C` (`BL 0x01E815F0`)を追加する。wrapperはadapter state 2かつ
type `0xBC`の時だけR0を基底type `0xBB`へ置換して、本来の `sub_57ADFC`へtail branchする。
Item requestとmanagerは変更せず、通常の室内Catalogや他typeには作用しない。

第6版で「0のランプ」と「12つぶのぶどう」の3D表示に成功した後、family 3/type `0xBD`の
「1UPキノコ」も同じ `vptr+8=0xE1A04000`で停止した。第7版は同じhook/cave位置を保ち、
adapter state 2かつtype `0xBC..0xEB`の場合だけR0を基底type `0xBB`へ置換する範囲guardへ
拡張する。hookはCatalog preview actor open callだけなので、室内Catalog、field actor、
family 0の基底`0xBB`には作用しない。旧第6版caveも識別してprivate stateを保持したまま移行できる。

実機では第7版により1UPキノコを含む家具が一通り3D表示された。ただし壁紙・絨毯は非表示で、
服カテゴリは `ModelInstance_SetRenderLayer` (`0x317BD0`) でSIGSEGVになった。従って第7版は
家具カテゴリ用の実験patchであり、全カテゴリ対応版ではない。原因解析とguard修正までは服カテゴリで
使用しないこと。3DSを電源断すればruntime hook/caveは消えるため、この終了時点でUninstallは不要。

CameraCatalog、Catalog専用3灯、render layer 2はroom 0にも存在するため、これらを
一時生成・pointer移植するpatchは不要。詳細は `DOCS/furniture_rendering.md`。

スクリプトの既定値は再び安全な `MODE="status"` に戻してある。

### `PATCHES/resfont_filter_once.py` — live ResFont filter 2-bit一回設定（F-130）

`BsShadowViewMgr_SubmitToScene`(`0x28FE0C`)を一時フックし、1回だけ
`nwfont_ResFont_SetLinearFilter(font, atSmall, atLarge)` (`0x4D7474`)を呼ぶ。
実行後は必ず`MODE="cleanup"`でhook/caveを撤去する。
`set_nearest`はbit2/bit1を0、`set_linear`は両方1（`ResFont+16=0x6`）へ戻す。

- hook stock: `0x28FE0C = 0xE92D4010`
- cave: `0x01E81000-0x01E810FF`（cleanup後は全ゼロ）
- 現在の起動の7px ResFont: `0x3302AD78`（再起動ごとに取り直す）
- filterだけを戻すのではなく、対象TextBoxを通常フォントへ戻してから`set_linear`すること

両bit OFFで拡大7px glyphがくっきりしたドット表示へ変化することを目視確認済み
（F-130 HIGH）。折り返しやCWDH幅は変えないため、字形filterだけの比較に使う。

### `PATCHES/textbox_font_width_test.py` — 7px glyphを一行化する比較（F-131 / TODO-101）

時計本文 `T_time_0` だけを7px ResFontへ替え、pane widthをstock 26.0から40.0へ広げる。
要求font sizeは18 x 24のままなので、glyph geometryは前回と同一。2文字advance 36が
pane幅40に収まり、折り返しだけを除ける。

- `MODE="install"`: normal font / width 26.0 → 7px font / width 40.0
- `MODE="uninstall"`: normal font / width 26.0へ両方復元
- `MODE="status"`: 読み取りのみ（既定）
- 実行前にprocess停止、TextBox vptr、pane名、両ResFont vptr、pane/font sizeを検証
- NEARESTは別途 `resfont_filter_once.py` で設定・cleanupする
- runtime pointerは再起動ごとに再探索し、スクリプト定数を検証する

### `PATCHES/textbox_font_integer_scale_test.py` — 7px glyphの整数倍率比較（F-131 / TODO-101）

`textbox_font_width_test.py` の状態（7px font / pane width 40.0）を前提に、
TextBox `+228/+232` だけを `18 x 24` → `14 x 14` へ変更する。
7px glyphに対して横・縦2倍の整数scaleとなるため、`18/7` の非整数拡大による
NEAREST端部の不均一さを分離できる。

- `MODE="install"`: `14.0 x 14.0` へ変更
- `MODE="uninstall"`: `18.0 x 24.0` へ復元
- `MODE="status"`: 読み取りのみ（既定）
- 実行前にprocess停止、TextBox identity、7px font、pane width 40、現sizeを検証

実機A/Bで `18 x 24`（非整数倍率）と `14 x 14`（整数2倍）を比較した結果、整数倍率で
右端の欠け・不均一さが改善した（F-132）。CWDH `glyphWidth`を書き換える追加パッチは
不要と判断し、このスクリプトは診断用のまま残す。

---

## `PATCHES/cave_node_record.py` — ★自前 GUI を上下画面に常時・最前面で描く（F-259〜F-281）

**2026-09-04 実機で完成。** 上下画面とも、ロード中・メニュー中・フェード中も消えず、
常に最前面に描かれ、ゲームは止まらない。

### 適用するもの

| 種別 | 番地 | 素の値（復元用） | 内容 |
|---|---|---|---|
| フック | `0x566DF8` | `0xE92D4010` | `RenderTop` 入口 → `CAVE_A1`（上ノード登録） |
| フック | `0x568F98` | `0xE92D4010` | `RenderBottom` 入口 → `CAVE_A2`（下ノード登録） |
| フック | `0x4B8360` | `0xE92D41F0` | `DrawCtx_FlushBatch` 入口 → `CAVE_F`（drawctx を控える） |
| ケーブ | `0x838200`-`0x838CF0` | 全部 0 | `.text` の空き（この範囲は元から 0） |
| データ | `0x9B0D00`-`0x9B5E00` | 全部 0 | `.bss`。LOG / 色 / 表 / ノード / vtable / MATCMD |
| テクスチャ | `g_GfxAllocator` から 0x4000 | — | 128x128 LA4 の ASCII アトラス |

`MODE = "install"` / `"uninstall"` / `"status"` / `"log"` / `"ring"` / `"export"`。

**`uninstall` の順序は「登録フックを素へ戻す → ノードをリストから外す → 全部ゼロ」。**
リンクしたまま vtable を消すと描画スレッドが死ぬ（実際に踏んだ）。

### 前準備 — テクスチャ用のリニアメモリ

CTRPF からは linear を確保できない（F-163）ので、ゲームの `g_GfxAllocator` から借りる。

```
PATCHES/cave_gfxalloc_probe.py（ALLOC_SIZE = 0x4000）を install
→ run_timed.py で 3 秒走らせる
→ 0x009B0010 に確保先（実測 0x329D8500。0x80 境界・リニア窓内）
→ プローブのフックとケーブを撤去
→ PATCHES/font_atlas_128x128_la4.bin 16384 バイトを書いて読み戻し照合
```

### 見た目だけを変えるとき

**`PATCHES/update_tables.py`。** ケーブもフックも vtable も触らず、
`.bss` のスプライト表・色配列・`LOG` のポインタだけを書き換える。
登録ケーブが毎フレーム記録要求を立てるので次のフレームで反映される。

### 適用前に必ず通す検証（5 本 + IDA）

```
1. _check_layout()                      容量・色の本数・.bss の重なり
2. python PATCHES/audit_node_cave.py cave_node_record.py
3. python PATCHES/verify_literals.py    全 LDR が読むリテラルの「値」まで
4. python PATCHES/make_font_atlas.py    アトラスの画素照合
5. python PATCHES/preview_layout.py     見た目（実機なし）
6. ケーブ 1 本を丸ごと IDA へ
   ★0x838200-0x839000 は code.bin.i64 に未マップ。マップ済みの空き
     （例 0x836700）へ相対位置ごと移して当て、直後に元バイトへ戻す
```

### 制約

- **拡大率は元テクセル 8px の整数倍**（F-281）。1.75 倍で線幅が割れる
- **色はチャンク（7 枚）単位**（F-280）
- 記録リストは `LIST_SIZE = 0x4000`。下画面 91 枚で 11536 バイト使う
- 座標は 1 単位 = 1px、原点は画面中央。上 x=±200 / 下 x=±160 / y=±120 が端
