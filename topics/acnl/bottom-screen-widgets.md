# ACNL / 下画面ウィジェットの登録と入退場（#164）

対象は acnl_jpn_v15。確度は MEDIUM（生成側・命令消費側・完了側の独立した静的根拠、実機追試なし）。
今回の修正根拠は _local/evidence/164/revision-evidence.json に保存した（export の命令列・xref、symbols、旧版ソースの rg 結果）。
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
要求成功や生成成功だけでこの状態を横取りすると、要求消費・通常の終了契約を失う。
終了待ち0x6D7194 は0x08が消えると0x20を立てて地図復帰を開始するため、
カタログ用の汎用「画面が閉じるまで待つ」関数ではない（F0115〜119の失敗経路）。

## 3. 最も単純な退場・復帰と適用条件

通常フィールドが静止し、チャット/メニューが開いておらず、同じ部屋のままなら、旧版が使う最小の組合せは次。

1. +484 があれば地図命令0、+488 があれば部屋命令0、タブ命令7。
2. 毎フレームゲーム自身の更新・actor破棄を進める。命令の消費だけでは完了としない。
   タブ・地図・部屋の命令（0x949D24・0x949D25・0x949D29）がそれぞれ11/2/2へ戻ったことに加え、
   タブ calc=0x6D474C/adjustor0、+6580=0、+6578=0、地図/部屋参照（manager+484/+488）が0を確認する。
   manager+56 の更新ゲートも開いていることが適用条件。0x6D35C4〜0x6D35D4でタブ+6416へ写され、
   0x6D7F58はその値が0なら命令消費・calc更新を行わない。
   この完了判定には背景・手カーソル・+492・+504の退場状態とメニューリストが空であることは含まれない。
   チャット/メニューが開いていないという前提は別に確認する。
3. 自前の使用終了後、タブ命令2を一度発行する。
4. 状態18 enter0x6D701C → 地図1/部屋1。
   calc0x6D6F60 が0x01を待ち、状態7 enter0x6D6AC4がタブ入場を始める。
   calc0x6D67F0 はアニメ完了と0x02を待ち、0x20解除、+6422=1、+6427=-1、BsMenuTab_TabSelectUpdateへ戻す。

これは同一ポインタ・任意の旧タブmask・チャットの入力文字を保存して復元する機能ではない。
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

チャットを閉じず一覧を重ねる経路と、チャットを退場させ下画面を使う経路は別契約。
前者は旧版GameListのover-chat分岐のようにfield退場をしない。
後者でタブ命令7を出すだけではkeyboardは消えず、calc0x6D5510の終了監視も上書きされる。
元のチャットactorを保存して復帰させず、必要ならタブindex6の通常要求から新しいactorを生成する。
入力文字の保存/再注入まで含む「元どおり」はこのstock復帰命令2の保証外。

## 5. 部屋移動・ゲームからの再表示

0x6D34AC は毎フレーム部屋/ステージ状態から +56/+57 を再計算し、地図/部屋命令処理を実行する。
ステージが対象外なら既存地図/部屋を破棄要求し低位を4へ、通常なら自動生成条件も処理する。
部屋フラグ8では地図を引っ込め、部屋メニューを候補にする。
0x6D1E14 は一部部屋で条件により byte_949D29 を1へ上書きする。
外部の「隠した」という履歴はゲームに登録されない。

既に+484があり+488が無い時の地図命令1は、新規入場を開始せず消費される（0x6D1428）。
0x01が消えていれば、その後の状態18は待ち続け得る。0x02だけでは18を通らない。
ゲームが戻した実物を検出せず命令2を重ねるのは、F0771/F0772の待機条件に反する。
部屋変化後は古いポインタ/表示mask/復帰義務をそのまま適用できない。
特殊部屋（0x4000/0x20000000 等）では命令2が18→7に入らず別通知で終わるため、通常屋外の完了式を一般化しない。

## 6. 旧版と現行main 0596153との照合

前ワーカーが照合したソースは旧版 Sources/Gui/GameList.cpp・GuiMenu.cpp・OwnGui.cpp・ChatKanji関係、
現行 src/game/bottom_screen*.cpp と src/ui/lease/。今回再読できたソースは旧版GameList.cpp。ソースそのものは本記録へ転載しない。
旧版が全場面で問題なかったことを今回実測したわけではない。

| 手順 | 旧版 | 現行mainと静的評価 |
|---|---|---|
| 静止フィールド退場 | map0/other0/tab7 | 同じ組合せ。ここは誤りではない。現行は部屋命令の消費・+488の消滅も待つ（差(A)） |
| 通常復帰 | tab2、18→7→選択と0x02待ち | 同じ。地図が既にある時の二重復帰を避ける必要は両者共通 |
| 開いた下メニューの終了 | stock状態6/7の後処理の一部を手動で行い、地図の再入場を省く | 同系統。フラグ (flags & ~0x27)|4 は退場通知と終了要求の整合でありactor破棄ではない |
| チャット上への一覧 | over-chatならfield退場処理自体を通らない | over-chat ownerを退場対象から除外する。全ウィジェット退場の意味には使えない |
| ゲームが自分で戻す場合 | 実物を見てShownへ戻す | 現行は再出現判定に+488も含む（差(A)）。履歴のみでの命令2再発行は避けている |
| チャットの完全退場/再開 | 専用の親/keyboard寿命を持つ経路が別にある | snapshotは+492/keyboardを表現せず、汎用menu判定に依存。完全退場・元チャット再開をこのAPI単独で保証できない |

**旧版との差(A): 部屋メニューの待機条件。** 旧版GameList.cppのFieldIdleはタブ命令11・地図命令2を待つが、
部屋命令0x949D29の消費は待たない。StepFieldのExitingも+488の消滅を待たず、
FieldOnScreenの再出現判定もタブmaskと+484だけで、+488を含めない。現行gohanはこの3つを含める。
したがって命令の組合せが同じでも、部屋側の待ちによって進行が変わり得る。
現行のこの3条件は依頼文の比較結果を採用したもので、今回共有された範囲では現行ソースを再確認できていない。

ゲーム側では0x6D1E14の入口がsub_565794()==0またはmanager+57!=1なら戻る。
命令0の分岐は+488!=0かつbyte_949D34!=0のときだけ0x2257E8へ退場要求を出し、命令を2へ戻す
（0x6D1FE8〜0x6D20EC）。byte_949D34==0の間は一時的に保留され得る。
1にする経路は0x31630Cの参照から0x316310の書込み、および0x326D20の参照から0x326D30の書込み。
0に戻す書込みは0x6D156C・0x6D20E4・0x6D3560。生成直後などの0を恒久停止とは断定しない。
部屋条件により命令を上書き/消費する別分岐もあるため、部屋命令2だけで+488の消滅を代用しない。

現行についての問題/適用限界（現行実装の説明は前ワーカーの照合結果を引き継ぐ）:
1. DecodeBottomScreenのmenu_openはopen state==1かつ0x08無しならfalse。
   Catalogのように登録済みでも0x08を書かない画面を取り逃がす。
   screen_list_emptyはmenu_goneにだけ使われ、Shownでの退場開始を防がない。
   よって「全メニューが無い」としてフィールド退場を始め得る。これは生成/登録と開始通知の混同。
2. hidden判定には+492/+496/+504/手カーソル/背景の状態が無い。
   tab7/map0/other0だけで全ウィジェットが退場済みという解釈は不成立。
   ゲームのメニュー空や部屋ゲートを通って通常フィールドに限定するなら成立範囲がある。
3. LeaseMachine::DrainedはRestoringもtrueとする。ResourcesReturned後、命令2を出し18の0x01待ちの途中でも
   ShutdownがFrameStepを外し得る。これは実際の復帰完了（0x6D67F0→選択/0x02）を保証しない。
   ゲーム自身の更新が続けば完了する可能性はあるため「必ず停止」とは言わない。
   対して旧版ShutdownはStage::OffかつField::Shownになるまで最大90フレーム相当
   （90回を上限にsvcSleepThread(16666667LL)）待つ。Restoringのまま待機を終え得る現行Drainedとは終了条件が違う。
   旧版も上限到達時には戻るため、必ず復帰完了まで待つ保証ではない。
4. restore_doneの「tabs_presentかつ0x02かつBsMenuTab_TabSelectUpdate」は通常屋外向け。
   特殊部屋で命令2が18→7を通らない場合や表示タブが0の場合、戻ったのに完了判定を満たさない可能性がある。
5. Begin/FinishBottomMenuCloseはstockの完全な呼出しではなく手動合成。
   特に0x6D4E5Cのback退場待ち0x6D5110を省き、メニュー空だけでFinishへ進む。
   後続のtab7で片付く場合はあるがstockと同じ時点の完了ではない。これだけで連打不具合の原因とは断定しない。

**誤りとしない点:** 持ち物の入場完了に0x08|0x10を要求することは一次命令と整合する。
通常チャットでもbutton-in enterが0x10を立てるので、0x80を見ないことだけを不具合の確定原因にしない。
main 0596153にない#108の差分は調べていない。

## 未確認点

- 全部屋・通信参加/離脱・連打・チャット入力中の実機追試はしていない。確度HIGHにはしない。
- +496の全型/+504を含む全関連vtableの全slot解釈・全map子/部屋子の最終解放までの網羅は未完。
  フィールドmanagerの参照欄を列挙したことを、669 profile全体の全下画面actorの網羅とは呼ばない。
- 任意の旧タブ構成・チャット入力内容・選択中メニューを完全に同じ状態へ戻すstock汎用APIは未確認。
- 現行gohanのソースと深い検証報告164.mdは今回の共有範囲では読めず、差(A)の現行側3条件は依頼文による。現行Shutdown/Drainedの説明も前ワーカーの照合結果を引き継ぎ、今回のソース再照合は未完。
- 「旧版で問題なし」の実機条件、現行の連打不良の動的因果、修正後の実機成立は未確認。

## 関連記録

- [ACNL-F0779](../../findings/acnl/0700-0799/ACNL-F0779.md) — 登録と所有欄
- [ACNL-F0780](../../findings/acnl/0700-0799/ACNL-F0780.md) — 通常フィールドの退場・復帰
- [ACNL-F0781](../../findings/acnl/0700-0799/ACNL-F0781.md) — チャットの寿命と通知
- [ACNL-F0782](../../findings/acnl/0700-0799/ACNL-F0782.md) — F0770の0x08/0x10排他説の訂正

[ACNL-F0782](../../findings/acnl/0700-0799/ACNL-F0782.md) は supersedes: [ACNL-F0770] による部分的な訂正。対象は0x08/0x10のビットの説明だけで、0x72294C ButtonActionControl_GetDecidedIndexの戻り値解析は訂正しない。旧記録本文は変更しない。
