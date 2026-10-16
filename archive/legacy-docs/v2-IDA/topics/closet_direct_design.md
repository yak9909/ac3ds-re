# クローゼット直通・反復取得と持ち物操作

IDA-gpt-6-F008/T011、IDA/GPT-6、2026-10-12。日本語無印＋更新、code SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。T010の利用者実機でcloset起動を確認、今回変更の実機動作は未確認。

## 要件・実装前の設計

- チャット退場→closetへ直接移る。T010のnative Cancel/parent・keyboard Releaseは保持し、BsMenuTab Return→MapSyncによるfield再表示を省く。既存GameListのBeginMenuClose/FinishMenuClose（メニューが消えるまでtabをnative待機へ置き、地図を戻さずfield hiddenへ）を開始直後から利用するAPIを追加。HoldField所有とnative cancelの前にtabを待機へ置き、FrameStepのタイミングに依存してmap復帰が先に始まる競合を避ける。終了時のchat再起動と失敗/scene/OFFのowner返却を保持。
- 検索/指定slotは不変の表示源とする。native WaitInputはGet→4byteローカルcopy→swap/stack→両側Setの順。storage setterを無視し、native icon refreshは元providerから行うため、何個取り出しても同じ項目を残す。
- pocketは埋まった枠の独自無効化を撤去し、owned closetのnativeLoadStepが除外した項目も操作可能にする。pocket同士のswap/stackは元コード。pocket→storageでsourceが書き戻される時は空へ、storage書込みは無視して消去する。storage→pocketはnative決定した値をそのまま書く。
- 追加指示: 0xFF以下/本来ポケットに入らない項目も消さない。PocketItem（没アイテム表示/F048）とnative Inventory_WriteSlotChecked→Item_NormalizeForPocket/Inventory_GetSlotの除外を照合。owned closetのsetterだけはcurrentSave+27600の16slotへraw4byte＋slot flag0を書く。Inventory_GetSlotはowned LoadStep/Calc/Setter呼出しscopeだけraw pointerを返し、元のBEQ/NOP設定や別画面は変更しない。原getterは変換でなく表示除外、原setterはnormalizeでIDを書き換えるので両方を扱う。
- B/Cのbound pane B_btn_01/B_btn_02だけを隠しても絵は消えない。change.arc/cng_base実物のN_btn_01/02にはboundと絵/文字が属し、影P_btn_sh_01/02は別の兄弟。親と影を非表示にして継続アニメの後も維持する。groupはAのみbindしnative前後ページは保持。

## 根拠・検証計画

既存F006/F007・PocketItem/F048、IDA caller/RTTI/状態遷移と原code.bin命令・DARC/CLYT pane-treeを独立照合。rawgetter/setter MITMは先頭PUSHを含むABI/元wordsを確認し、失敗時は入れたhookを戻す。未知のitem意味は推測renameしない。判明概念はDBへ名前/型/注記を適用して保存、公式XML＋全bytes/hashを検証する。

PCでは旧T010のmap再入場/slot消失/占有pocket無効化/低ID normalize・hidden fallback/親絵残留を再現。新版のnative parent/key release→field close bypass→request61をmap restore命令なしで検査し、原WaitInputによる連続取得/slot不変/実pocket同士swap・stack/cloneへの消去/低ID+flags/別menu・scope外への元挙動を確認。元pager/list/style/ABI/分岐/LDR/hash/しずえと正常・全旧9配布版を保持。FS/GPU/animation・actor schedulerのendpointは明示し、成功実機表示とは区別する。Gitは完了後一括、work枝のみ、SD/実機/mainへ操作しない。

## 最終PC検証

- 旧T010のslot消失/occupied無効/lowID空化成功/raw hidden getter/ChatReturn→map再入場を5caseで再現。新script SHA一致で22case PASS: 原WaitInputの連続取得・pocket移動/swap/stack・空/満slotへの消去、0/1/0xFD/0xFE/0xFF/0x2000/0x7FFDのID/flagsとicon read、scope/outflag/bounds/別inventory・actor/外部BEQ/NOP保持、親+影hide、原parent/keyboard WindowOut/Release/Detach→map復帰命令なしでcloset61、終了chat/timeout、原storage180/pager6超/constructor allocator/deletion/search順・集合。
- PMF/アニメ完了・actor scheduler・icon texture upload・カタログレコード/field低ID remapは明示endpoint。native checked-write/normalizeとtransfer/stack/get/setは原ARM。fixtureの未初期化empty sentinelや旧mockと原PUSH trampolineの衝突・Unicorn cacheを訂正した。製品を実機成功と認定しない。
- 4334parser/date・44anchor・15CPP/専用BuildClosetDirect、623linkedfunc/37523命令/7057branch/3508PC参照/ABI/SP/VFP/全領域/hash/しずえPASS。既存list20/repeat12/scroll/style6もPASS。
- DB7rename/partial endpoint型+4prototype/17注記save/close→所有0、公式XML7新名/17注記/50旧名/全型member/T/fullbytes/input/DB hash PASS。34source hash/14frame owner対16、正常・全旧9配布版保持PASS。
- 成果物gohan_closet_direct1: 3gx 1403318B/SHA1e9d238eaf6847d374d8ea673267112e844aeb17b40d482ddccdbf596549d27b、ELF7bf7fd9b707b112fb15854320eed1eabed1e8a914ab0bab37efad5f1a84c76d3。最終保存版はmanifest/publication。次は利用者の直通・反復取得・pocket操作/消去・低ID・B/C非表示とB→chat復帰の実機確認のみ。

最終DB監査で、原数量merge/predicate（0x4DD030/0x4DD4A4）も原ARM＋native実行で役割が定まっていたため2renameと周辺9注記を追加した。合計9rename/26注記。lookup0x4B4328/4B4330の全ABI・class、0x1C2FF8/1C39F4のruntime PMF・数量action意味、0x2BFE8Cのstack第5引数等は未確定で、DBへ理由と次の照合を記し推測名へしない。製品コード・3gx・runtime scriptは不変、最新公式XMLを更新して同最終batchへ保存。
