# クローゼットの画像保持・帰還直通・即時ページ

IDA-gpt-6-F009 / T012、GPT-6、2026-10-12。JPN無印＋更新SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。ARM11/32bit/LE、imagebase0、T=0/セグメントはF008と一致。acnl_v2単独所有。実機操作なし。

## 実装前設計

### 追加指示の設計（同T012/F009）

退場高速化・ページ間隔待機の撤去・closet後のERROR2/STAGE1を追加。Engine::Loadのfailure2/stage1はNativeFsApi::memalignによる5MiB確保失敗で、資源破損とは未確定。native検索へIDをコピーした後normal名前fileとmatches容量を返し、actor破棄後にitems/pending容量も返して連続領域の再確保を妨げる保持を除く。list backendのnormal cacheは保持する。workerを中断・解放しない。

原control touch/handは+216 counter/+220 threshold（初回11、repeat3）を使う。owned page arrow source、非dragだけcounter=-1/threshold1へ毎Calc更新し、node112/152のdecide animを終端へ。親WaitPage1C38A0も同Calcで完了させる。一般品drag/他窓/一般入力は既存のnative経路。

原closet WaitLeave Enter1C3274はchild outer-state2B79C4のanim996とpocket out-state26EC94のactive anim1988を始め、1C3214が完了を待ってActor_RequestDestroyする。owned退出時だけ両animを終端へ進め、元unbind/状態変更/破棄要求へ通す。actor破棄後のキー全release待機も除く。nativechatの実生成・旧actor/資源解放は待つ。

- 旧16枠LRUはmaterial TexMapにPAを保持したまま枠を再利用する。原SetItemのPA格納＋ソースの画像上書きを照合。widgetごとに参照保持、SetItem/dtorで解放する。32枠/128利用者の上限ではnative画像を使い、参照中画像を上書きしない。GPU cache32KiB、借用合計0x1B000（16KiB増）。spare/キー/atlas境界を検査。実機余裕は未確認。
- RTTI ItemDragIconNodeの両dtor0x2B99CC/0x2B9974は別bodyでLayoutを解放。先頭PC相対LDRはCTRPF MITMで再配置不可なのでPUSH0x2B99D0/0x2B9978へhook、先行R1も元処理へ渡す。
- 旧BeginReturnはhold解放→command2でmap/tab復帰。chatへ戻る場合はholdのままmenu5を要求し、tab待機のままchat readyまで待つ。ready時にGameListへ所有を引き渡して通常chat待機へ戻す。失敗/room変更はholdを解放してnative復帰。chatを後で閉じる経路も保持。
- 原0x267A50はrel4/5のpage循環更新→0x267788のscroll待ち。原0x1C38A0はchild idle0x267878で入力復帰。owned childだけpage更新→0x297BA0の10項目/0x267660のcounterを即更新。foreign childは原処理。PUSH0x267A54へMITMし先行LDRのR2を第3引数でforward。

MEDIUM: 原assembly＋RTTI/状態表/caller/ソースの独立照合。新GPU表示・遷移成功は実機未確認。PCで旧LRU破損/旧map復帰/旧scroll待ち、新長期page・共有/dtor/容量・帰還command2なし・chat閉鎖後復帰・page wrap/入力復帰を検査する。

## 保存

## 実装と検証

HiddenIconsの32枠参照保持、両dtor・pageのPUSH位置hook、GameList::ReleaseFieldToMenuを実装。native widget型876B/3prototype・7name/11注記を保存。旧版の画像上書き・field復帰・scroll待ちと新版の長期page/pin共有/枠不足/native両dtor/atlas・spare整列/直接chat帰還/通常chat閉鎖の復帰をPCで照合。保存SHA・確定件数はgohan_closet_followup1/manifestとfollowup_runtime/linked_checks/db_xml_readbackに記録する。型のunknown領域/削除後return値の意味は未確定、追加renameなし。

F008 export88446終了0/9名26注記と旧50名XML読戻しPASS。追加完了までGit保留。専用gohan_closet_followup1、正常/全旧版保持、main/SD/実機/中断中の整理未操作。
