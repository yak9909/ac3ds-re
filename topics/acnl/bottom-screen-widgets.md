# ACNL / 下画面ウィジェットの登録と入退場（#164）

対象は acnl_jpn_v15。確度は MEDIUM（生成側・命令消費側・完了側の独立した静的根拠、実機追試なし）。
今回の修正根拠は _local/evidence/164/revision-evidence.json に保存した（ゲームの根拠は export の命令列・xref と symbols の rg 結果）。
一次資料は export/all_functions.txt・xrefs.tsv、表のバイトは tools/codebytes.py の read_bytes で確認する。
根拠抜粋と検索結果は _local/evidence/164/selected_functions.txt・additional_functions.txt・widget_functions.txt・xrefs.tsv、表と計算は tables.json・calculations.json。
export の symbols_commit は 4914ab98f271092df116b05c38a6183939b88b16。書き出しの過去コメントは一次根拠に数えない。

## 1. 登録先とウィジェットの範囲

「登録」は、画面ファクトリ、actor の親子、メニューのリスト、manager の参照欄、描画 Layout の登録を区別する。

- 0x1D3A84 は descriptor 0x94DFC8（12 byte/ID）・factory 0x94FDBC（8 byte/ID）・件数 669 を 0x96F2AC/B0/B4 へ登録する。
- 0x528C60 UiScreen_OpenById → 0x51EC58 UiScreen_OpenChild。親子 actor と生成フェーズを作る。0x81EE98の破棄フェーズはvt+76/+80/+84を呼び、戻り3では待つ。戻り非ゼロは生成要求が成立したことを示し、入場アニメ完了ではない。actor+15 に破棄要求が立つ場合は戻り0。
- メニューのリストは 0x9864FC、head=0x986500。0x6D102C が node を追加、0x6D1B34 が除去する。node は actor+20、node+12 が actor。常設タブ自身の state machine も +20 であり、全 actor の +20 をリスト node と同一視してはいけない。
- 0x6D1074 は open state 0x949D1E==1 かつ head==0 のみ。地図・タブ・背景の復帰完了を意味しない。
- Layout の上下描画リストは別（既存 F0693/F0694）。そこから外すだけでは actor の退場・破棄にならない。

manager は *0x949D4C。0x6D3144 が次の常設参照を初期化する。

| manager の欄 | 対象・生成 | 退場/破棄の根拠 |
|---|---|---|
| +472 (0x1D8) | BsMenuMain、screen 0x217、factory 0x7EA9E4、vtbl 0x8E53A8。制御主体 | リセット 0x1A0DD4、manager Release 0x6D3924 |
| +476 (0x1DC) | BsMenuBg、screen 0x260、factory 0x7F1C24、ctor 0x6949C0、vtbl 0x8F2C90 | 種類変更/leave 0x693EE8、reset 0x694124。タブ命令7の対象外 |
| +480 (0x1E0) | BsMenuTab、screen 0x218、factory 0x7F22A4、ctor 0x6D80AC、vtbl 0x8F3710 | 全退場は actor を残す。Release 0x6D808C、dtor 0x6D8284、delete wrapper 0x6D8274 |
| +484 (0x1E4) | 地図ラッパ screen 0x219、ctor 0x7F21EC、vtbl 0x8F3658 | 命令処理 0x6D1428、種類別退場 0x6D0B54、ラッパ終了 0x6D0E30 が欄を0にする |
| +488 (0x1E8) | BsMenuRoomMgr、screen 0x261、ctor 0x7EC834、vtbl 0x8E82CC | 退場要求 0x2257E8、監視 0x2252E8、Release 0x225778 が欄を0にする |
| +492 (0x1EC) | BsMenuChat、screen 0x23F、factory 0x7EA97C、ctor 0x193C90、vtbl 0x8E5120。LoadStep 0x193A40 が自身を公開 | 0x193988 → keyboard vt+68、0x1938D0 → Actor_RequestDestroy、Release 0x193C3C で欄0 |
| +496 (0x1F0) | BsMenuReaction（screen601=0x259、factory0x7ED424）が 0x25E5FC で公開する。vtbl 0x8E926C。チャット窓専用欄ではない | 0x25D4D4/0x25F4B8 側で解除。全型・全終了経路は未確認 |
| +500 (0x1F4) | BsHandCursor、screen 0x216 | factory 0x7EBC58、vtbl 0x8E7388、dtor 0x1FABFC/delete 0x1FAB98。show 0x1FA7A8 / hide 0x1FA86C、manager+64 も同期。タブ命令7だけでは隠さない |
| +504 (0x1F8) | BsMenuRandomHeadsUp、screen 0x266、factory 0x7F0024、vtbl 0x8EE174。通信状態かつ room 101 で生成（0x6D34AC） | 同更新関数が別条件で破棄要求・欄0。0/7/2 の一般退場対象ではない |

地図ラッパの +64 は種類0〜5。0x6D0928 が room 条件に従い子 screen を作る。
種類/子ID/global は 0/0x21A/0x949C34、1/0x21C/0x949C38、2/0x21B/0x949C3C、
3/0x21D/0x949C40、4/0x21F/0x949C44、5/0x21E/0x949C48。
種類名は村 / 島 / 選択 / ロビー / モデルホーム / 商店街（profile表のBsMenuMapVillage/Island/Select/Lobby/ModelHome/ShoppingStreet）。factoryは同順に0x7EE9EC/0x7EE078/0x7EE118/0x7ED204/0x7EF96C/0x7F0E38。村地図vtblは0x8EBA24。
退場要求は種類別に 0x2B3A98、0x150374、0x15037C、0x150384、0x15038C、0x150394 へ分配する。

部屋メニューは byte_949D2A=1/2/3 で自分の +56/+60/+64 に子 screen 594/606/612（BsMenuRoomLightSwitch/BsMenuModelHomeBoard/BsMenuCamper、factory0x7F0AE0/0x7F042C/0x7EBE08）を持つ（0x22556C）。
+69 は退場要求済み、+68 は終了の契機。単に +488 を0にして完了を偽装する手順ではない。
全子の内部ボタン・資源破棄関数までは今回網羅していない。

常設画面のvt+12は初期化、vt+24はRelease、vt+36は更新。タブは0x6D7E58/0x6D808C/0x6D7F58、地図は0x6D0928/0x6D0E30/0x6D0BF0、部屋は0x22556C/0x225778/0x2256D8、チャットは0x193A40/0x193C3C/0x193BAC。表の先頭slot0/1はdtor/delete wrapperで、Releaseと別。mainは0x1A13B0/0x1A1514/0x1A1474。
背景の完了は0x693F60でchangeアニメ終了後に+1554=+1553、待機へ。vc_MENU_FLAGSやタブmaskへ背景完了を通知するわけではない。
RandomHeadsUpは+972/+1012のin/out、0x2F3010/0x2F30C8で完了を判定し、0x2F31C8/+1580の時間待ちを挟む。0x2F3240で下Layout登録する。表示の切替とmanagerによる破棄は別。

profile534〜617の84件の名前/factoryは _local/evidence/164/widget_profiles.tsv に列挙した（これ自体を全画面の入退場契約とはしない）。

タブは独立した11個の screen ではない。BsMenuTab 内にボタン配列 +1948、stride388、11要素、
group +6432 と pane +6476 の配列を持つ（0x6D3B98）。
index0〜10 は itm / Dsin / rfrnc / frnd / list / plus / chat / manp / post / call / back。
上/下の名前はゲームのタブ配置を指し、3DSの上画面 screen を意味しない。

## 2. 命令・状態・完了通知

| byte | 値と処理 |
|---|---|
| 0x949D24 | 11=消費済み。0x6D3F04 は現在状態に関わらず読み、先に11へ戻す（呼出元0x6D7F58自体にはtab+6416の更新ゲートがある）。7=全タブ退場、2=地図同期タブ入場、3=メニューアウト、0=退場後待機、1=タブ入場、6=上タブ入場、その他は同関数の switch |
| 0x949D25 | 0=地図退場、1=地図生成/部屋側の処理、2=待機。消費側0x6D1428。部屋条件・manager+57・vc_MAPBOOL のゲートがあり、常にすぐ2へ戻るわけではない |
| 0x949D29 | 0=部屋メニュー退場、1=生成、2=待機。消費側0x6D1E14。0 は +488 と byte_949D34 の ready 条件、1 は部屋/既存actor/別画面のゲートを持つ |

vc_MENU_FLAGS 0x949D68 の低位は通知であって actor ポインタではない。
0x01=地図側入場開始、0x02=入場完了、0x04=退場完了/対象なし。
村地図 0x2B2720 は (flags & ~7)|1、0x2B266C は (flags & ~3)|2。
地図ラッパ0x6D0E30/部屋 Release0x225778 は (flags & ~6)|4。
部屋子0x326720 も完了2を書き、タブ0x6D6AC4 も地図なしなら2を補う。
よって地図の物理表示だけのフラグではなく、低位三ビットが常に排他的でもない。

通常メニューは 0x08=開始、0x10=入場完了、0x20=終了要求。
**0x08 と 0x10 は排他ではない。** 持ち物 BsMenuItem_OpenEnter0x199F9C は (flags & 0xFFFFFFE7)|8、
BsMenuItem_OpenUpdate0x199F44 は (flags & 0xFFFFF7EF)|0x10。後者は0x08を残す。F0770の排他という説明だけを [ACNL-F0782](../../findings/acnl/0700-0799/ACNL-F0782.md) で訂正する。
カタログはこの開始/完了 handshake を書かず0x20を読む（F0118の契約を今回も採用）。

タブの +6578 (0x19B2) は表示/有効 mask、+6580 (0x19B4) は入退場の対象 mask と bit15 のアニメ進行印。
方向は mask だけで決めず、calc と +6418/+6420 も見る。
+32/+36 は PMF の関数/adjustor。+36==0 の場合に限り単純な関数番地比較ができる。

命令7 → calc 0x6D6A98、enter 0x6D6B88。
enter は現在有効な11タブの bit を +6580 に OR し、0x6D5DA8 が out animation を始める。
0x6D6528 は完了時に animation を解除し、ボタン・pane可視を片付け、
+6578 &= ~mask、+6580=0、+6420/+6418/+6425=0。
0x6D6AB8 は完了後の **state変更 call site**。先頭番地の関数でも全UI完了フラグでもない。
通常の行き先は BsMenuTab_TabSelectUpdate0x6D474C。

メニュー切替0x6D6060 は0x08の後にback index10を表示し0x10を待つ。
この状態の進行条件は0x08・0x10の通知であり、要求受付や画面生成成功とは別。
終了待ち0x6D7194 は0x08が消えると0x20を立てて地図復帰を開始するため、
0x08を書かないカタログの寿命を待つ条件にはならない。

## 3. 最も単純な退場・復帰と適用条件

通常フィールドが静止し、チャット/メニューが開いておらず、同じ部屋のままなら、最小の組合せは次。

1. +484 があれば地図命令0、+488 があれば部屋命令0、タブ命令7。
2. 毎フレームゲーム自身の更新・actor破棄を進める。命令の消費だけでは完了としない。
   タブ・地図・部屋の命令（0x949D24・0x949D25・0x949D29）がそれぞれ11/2/2へ戻ったことに加え、
   タブ calc=0x6D474C/adjustor0、+6580=0、+6578=0、地図/部屋参照（manager+484/+488）が0を確認する。
   manager+56 の更新ゲートも開いていることが適用条件。0x6D35C4〜0x6D35D4でタブ+6416へ写され、
   0x6D7F58はその値が0なら命令消費・calc更新を行わない。
   この完了判定には背景・手カーソル・+492・+504の退場状態とメニューリストが空であることは含まれない。
   チャット/メニューが開いていないという前提は別に確認する。
3. 退場後の復帰はタブ命令2で始まる。
4. 状態18 enter0x6D701C → 地図1/部屋1。
   calc0x6D6F60 が0x01を待ち、状態7 enter0x6D6AC4がタブ入場を始める。
   calc0x6D67F0 はアニメ完了と0x02を待ち、0x20解除、+6422=1、+6427=-1、BsMenuTab_TabSelectUpdateへ戻す。

これは同一ポインタ・退場前の任意のタブmask・チャットの入力文字を保存して復元する機能ではない。
地図/部屋actorを再生成し、現在の部屋/セーブ/通信条件からタブを再評価する。
全ウィジェットを原子的に一命令で退場・完全復元する関数は、調べた直接xrefには無い。

ゲーム自身の経路:
- メニューイン0x6D4CB4: 一部タブの退場maskを設定し、メニューが空なら地図0/部屋0、空でなければ0x20。
- メニューアウト（命令3）: enter0x6D4EE8で0x20とback退場、calc0x6D4E5Cでbackアニメと0x6D1074を待ち、18→7へ。
- BsMenuMain 0x1A0C64 / 0x1A0F80 は地図0/部屋0、チャット/Reactionがあれば0x20・背景leave、タブ命令0を併用。
  対応待ち0x1A0F28は地図/部屋が無いこととメニュー空を待つ。命令0は0x6D4C88→待機0x6D4444であり、命令7とは終了後の状態が違う。
- 会話系0x6D6B18/0x6D6F90は0x6D6BD8でタブを退場し、地図/部屋側へ別命令を出す。
  0x6D68A0の後半は地図1/部屋1を再発行しタブと0x02を待つ。ゲーム自身が表示を戻す経路がある。

## 4. チャットの寿命

通常チャットはタブ状態13/calc0x6D5510。byte_949D3B==0でBsMenuTab_ChatReturnUpdate0x6D5FB0へ進む。
BsMenuTab_ChatReturnUpdateはタブoutとメニュー空を待ちBsMenuTab_ChatTabsInUpdate0x6D5AB8へ進む。
チャット入場側は BsMenuTab_ChatTabsOutUpdate0x6D6214 → BsMenuTab_WaitChatTabsUpdate0x6D70F8、
enter0x6D72C0が tab index6を表0x85080Cでmenu5へ変換し、0x787004のmenu→screen表から0x23Fを要求する。

チャット親0x193A40はmanager+492へ公開し、0x193890で子keyboard screen0x23Eを自分の+220へ生成する。
0x193764は0x20を受けても直ちに親欄を0にしない。Out enter0x193988が子vt+68で閉じ、
keyboardのBsSkb_WindowOut_Calc0x57CF04のアニメ完了→破棄→Release0x57F944で0x94A654=0/flags &=0xFFFFFFC7。
親0x1938D0がそれを待って自分の破棄を要求し、0x193C3Cで+492を0にする。
したがって共有入力binding解除、子消滅、親消滅、メニューリスト空、タブ復帰は別々。

**既存コメントの読み違いに注意:** BsSkb_WindowInEnter0x57CDC8は0x10/0x80を消し0x08を立て、
BsSkb_WindowInUpdate0x57CB20がBsSkb_ButtonsInUpdateへ進む。その enter0x57CC9Cは0x10を立て、
update0x57CA00は完了で0xC0を立てる。親0x193850は0x80を待つ。
「BsSkb_ButtonsInUpdateが0x10を書かない」から「通常チャットには0x10が無い」と結論してはいけない。
書き出しに残る F008 コメントはその推論を含むため不採用。

タブ命令7だけではkeyboardは消えず、calc0x6D5510のチャット終了監視も別状態へ切り替わる。
タブindex6の通常要求は新しいチャットactorを生成する。既存actorや入力文字を保存して復元する処理ではない。
地図同期復帰のタブ命令2にも、チャット入力文字の保存・復元処理は確認されていない。

## 5. 部屋移動・ゲームからの再表示

0x6D34AC は毎フレーム部屋/ステージ状態から +56/+57 を再計算し、地図/部屋命令処理を実行する。
ステージが対象外なら既存地図/部屋を破棄要求し低位を4へ、通常なら自動生成条件も処理する。
部屋フラグ8では地図を引っ込め、部屋メニューを候補にする。
0x6D1E14 は一部部屋で条件により byte_949D29 を1へ上書きする。

既に+484があり+488が無い時の地図命令1は、新規入場を開始せず消費される（0x6D1428）。
0x01が消えていれば、その後の状態18は待ち続け得る。0x02だけでは18を通らない。
部屋変化後の地図/部屋actorとタブの構成は、現在の部屋条件から再評価される。
特殊部屋（0x4000/0x20000000 等）では命令2が18→7に入らず別通知で終わるため、通常屋外の完了式を一般化しない。

## 未確認点

- 全部屋・通信参加/離脱・連打・チャット入力中の実機追試はしていない。確度HIGHにはしない。
- +496の全型/+504を含む全関連vtableの全slot解釈・全map子/部屋子の最終解放までの網羅は未完。
  フィールドmanagerの参照欄を列挙したことを、669 profile全体の全下画面actorの網羅とは呼ばない。
- 退場前の任意のタブ構成・チャット入力内容・選択中メニューを完全に同じ状態へ戻すstock汎用APIは未確認。

## 関連記録

- [ACNL-F0779](../../findings/acnl/0700-0799/ACNL-F0779.md) — 登録と所有欄
- [ACNL-F0780](../../findings/acnl/0700-0799/ACNL-F0780.md) — 通常フィールドの退場・復帰
- [ACNL-F0781](../../findings/acnl/0700-0799/ACNL-F0781.md) — チャットの寿命と通知
- [ACNL-F0782](../../findings/acnl/0700-0799/ACNL-F0782.md) — F0770の0x08/0x10排他説の訂正

[ACNL-F0782](../../findings/acnl/0700-0799/ACNL-F0782.md) は supersedes: [ACNL-F0770] による部分的な訂正。対象は0x08/0x10のビットの説明だけで、0x72294C ButtonActionControl_GetDecidedIndexの戻り値解析は訂正しない。旧記録本文は変更しない。
