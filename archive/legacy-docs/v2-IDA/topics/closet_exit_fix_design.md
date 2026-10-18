# クローゼット検索: native chat退場と復帰へ修正

追加訂正（IDA-gpt-6-F008/T011）: 利用者実機でT010はcloset表示へ到達したが、間にmap/BsMenuTabが復帰してから退場していた。新[直通設計](closet_direct_design.md)はCancel前から既存GameListのmenu-close handoffでtab Return/MapSyncを省き、native parent/keyboardの実退場は保持する。slot消耗・occupied pocket拒否・B/C hitboxだけhideも新仕様へ訂正。T010の元artifact/解析は来歴として保持する。

記録: IDA-gpt-6-F007/T010、IDA/GPT-6、2026-10-12。JPN無印＋更新/code SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。native契約MEDIUM、今回修正の成功実機表示は未確認。

## 実機報告と原因

T009/SHA47603800...で検索すると背景だけになり入力停止、後に「クローゼットを開けませんでした。」。この文言はWaitFieldの180frame経過のみ。T009はparent/kbdを凍結・listからdetachしてGameListのFieldIdle（tab calc0x6D474C）を待ったが、普通chatのtabはnative state13「チャット終了待ち」/0x6D5510。フラグやpointerを外すだけではこの出口を進めない。前PC試験はtabを初めからidle/hiddenに置き、この経路を省略していた。

## 実際の退場処理

- 普通BsSkbのCancelは0x57B778の2button branch（決定index0）。+4424が真なら0x949D3B=0、keyboard+4580=1、TextInput_PublishResult(ready1,result1)。送信は別index/ready1,result2であり、cancelはチャット文を送らない。
- Parent0x193764はresult1でOutへ、enter0x193988がchild vt17→0x57B238を呼ぶ。button-out/window-out→0x57CF04がアニメ完了後Actor破棄を要求。
- Kbd release0x57F944は資源を返し、live0x94A654=0、MENU_FLAGS &=0xFFFFFFC7（0x08/0x10/0x20消去）、共通button label登録をreset。Parent0x1938D0はlive消滅後に自分をdestroy、release0x193C3Cがmanager+492=0/child=0/0x800消去。
- Tab0x6D5510は0x949D3B=0でReturn0x6D5FB0へ。tab-out＋native menu idle/emptyを待ち、chat-tab-in0x6D5AB8へ。MENU_FLAGS 0x10が消えるとMapSyncTabsInへ進み、元field/tabを戻す。
- ready/resultだけを発行するとtabの0x949D3B出口を欠く。nativeのcancel通知を揃える必要がある。

## 設計（実装前に作成、T010で実装）

- 検索開始のBegin受付→即検索/Publishを維持。ゲームthreadで通常chatのCancel通知を1回発行し、native parent/kbdのCalc/Draw/Release/Detachをそのまま進める。凍結vtable/手動listdetach/元pointer復元は撤去。
- Parent slot/kbd live/native listが空になるまでWaitChat。続いて既存HoldFieldで正常field/tabを退場させ、native closet61を1回requestする。slot providerとnative取得を保持。
- 終了/生成失敗はown holdだけを返す。キー/タッチ解放、GameListの復帰と現物FieldIdleを確認後、tab index6＋native state9（0x6D6214）を起動。enter0x6D6440→exit/menu-empty/flag4待ち→0x6D72C0がtab→menu表0x85080C[6]=5、Menu_RequestOpen(5,1)を発行。初期化0x787004はmenu5をscreen0x23Fへ、RTTI/factory/0x193C90と照合。新普通chatはnative生成し、古いpointerを再利用しない。
- 新chatの通常Wait状態/入力bindingを確認して独自の入力遮断を返す。失敗・scene変更では要求を再送せず、native fieldへ戻して入力を返す。起動前/退場待ちはB取消も扱う。
- FieldReadyをGameListの現物idle条件として公開し、復帰開始がキャッシュ上Shownというだけではchatを起動しない。
- hair/styleはT008の直接Showを保持。元list/native pager/保存closet/正常版/全旧成果物は保持。

## 根拠と検証

既存system_keyboard_normal_chat.md/F383、menu_system.mdのnative状態名、IDA ARMと抽出原bytes/生tableで独立照合。新概念/関連確認をDBへ反映してsave、公式XMLで読戻す。旧artifactでtab13/flag2を保持した180frameタイムアウトと描画抑制を再現し、新版では原keyboard Cancel/ParentOut/Release/TabReturnの連鎖からrequest61へ到達すること、終了からnative menu5へ戻ることを検証する。slot/ページ/取得・list/style回帰、全linked branches/LDR/ABI/SP/VFP/領域/hash/しずえも検査。

nativeGPU/FS/生成・破棄の一部はCPU fixture endpoint。実機での成功表示・timingは未確認、今回版をmainへ入れない。新artifact gohan_closet_exit_fix1、根拠work/evidence/gohan_closet_exit_fix。Gitは全修正/検証完了後一括、実機/SDは操作しない。

### 最終PC検証結果

旧T009を実chatのtab13/flag2から始め、180frameでWaitField timeout/起動要求なしを再現。新版は20case（原Cancel通知一致、原parent/keyboard close・WindowOut/Release/Detach、原Tab13→Return→TabsIn、closet61要求一度、終了後native tab6→menu5、新chat Wait/binding確認、B解放/owner隔離/scene/復帰失敗、ctor/allocator/検索順）と原保存索引180枠がPASS。PMF遷移・アニメ完了・map復元・actor factory/schedulerは明示endpointであり、GPU/実機timingの証拠にはしない。既存list20/repeat12/scroll/style6もPASS。prebuild4334/40anchor/15CPP、linked617funcの全分岐/PC参照/ABI/SP/VFP/hash/しずえPASS。

DB13名/24注記/result enum＋publisher型を保存、公式XMLの13新名/37旧名/enum/T/fullbytes/hashを読戻した。Exporterがfunction宣言を出さない部分はsavedDBのidalib再読で確認してclose(savefalse)、hash不変。正常ELF・全旧8配布版保持、34source hashと14frame owner対16の上限PASS。3gx SHA c8ff8fed0d2045949d999e7f6d171f73346352541e25a38b08617530ebde84c6、ELF83a5bd5f80b81e8a671ed52bcef9a63c28ba5badb7b81a8f5a92c12716f3d6b5。最終保存版はmanifest/publication。
