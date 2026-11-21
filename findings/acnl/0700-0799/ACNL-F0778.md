---
id: ACNL-F0778
aliases: []
title: "共通UIの呼出契約と生成時の未設定prototype"
summary: "共通UIの呼出側とARM命令から、未設定だった23関数のprototypeを部分型とVFPレジスタ指定で表す。全体不明のクラスはvoid *のまま公開する。"
date: 2026-11-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: export ARM
addresses: [0x002F7B04, 0x002F6AE4, 0x002F6E78, 0x002F6B1C, 0x00722A6C, 0x00722B40, 0x002F6810, 0x002F6694, 0x002F7744, 0x001B07D8, 0x001C58D0, 0x001C59C8, 0x001C55B4, 0x001C5A58, 0x001C5660, 0x001B0288, 0x001B0314, 0x00568C18, 0x00568928, 0x001280B4, 0x004D7164, 0x007B0694, 0x005FC344]
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

共通UIの未設定prototypeを表の範囲で付ける。確度はMEDIUM（命令と独立した呼出・所有欄・対応する処理の照合）。実機なし。
void戻り値の処理は、経路ごとのR0がscratchや仮想呼出結果であり、確認した呼出元が値を利用しないもの。
構造体の全体や独立した返却契約が未確定のものは勝手に命名しない。
UiAnim_Setのflagsは呼出側に3があるためboolにしない。

## 根拠

表の通常の関数は整数・ポインタをR0から順に渡す。表中では呼出規約の注記を省き、symbolsには正確なABI指定を保存する。UiAnim_SetだけはVFPを併用し、個別にレジスタを明記する。

| 番地・既存名 | prototype（通常のABI指定を省略） | 命令と照合先 |
|---|---|---|
| 0x002F7B04 ButtonActionControl_Ctor | `void *(void *self)` | 0x2F7B14 STR vtable、連続UiAnim ctor後0x2F7B38 SUB R0,#0x88。SelectBase_Ctor 0x1B0804–0x1B0808 は戻り先頭を使用。 |
| 0x002F6AE4 ButtonActionControl_ClearTouchSelection | `void (void *self)` | 0x2F6AEC LDR node、vt+0x1Cへ0、0x2F6B10 STR null。独立caller 0x1AF868–0x1AF870はself+0xA00を渡し結果不使用。 |
| 0x002F6E78 ButtonActionControl_ClearAllTouches | `void (void *self)` | 0x2F6E88/8C node巡回、0x2F6EDC BLX、0x2F6EE8 STR null。対応するClearTouchSelectionと同じ制御体+0xB4。 |
| 0x002F6B1C ButtonActionControl_CheckShortcuts | `bool (void *self)` | 0x2F6B28 LDRH self+0xD0、node key照会とvirtual決定通知、0x2F6C18側false/決定側trueのR0。 |
| 0x00722A6C ButtonActionControl_IsNextKey | `bool (void *self)` | 0x722A74 LDR self+0xC4、0x722B2C MOV R0,#1 / 0x722B34 MOV R0,#0。IsPrevKeyが独立した対称経路。 |
| 0x00722B40 ButtonActionControl_IsPrevKey | `bool (void *self)` | 0x722B48 LDR self+0xC4、0x722C00 MOV R0,#1 / 0x722C08 MOV R0,#0。IsNextKeyが独立した対称経路。 |
| 0x002F6810 ButtonActionControl_StateWait | `void (void *self)` | 0x2F6818 self+0xD4、0x2F6868/78 node/control virtual、巡回後戻りR0は非契約。Ctorが+0xB8/+0xBCに登録しUpdateが1引数で呼ぶ。 |
| 0x002F6694 ButtonActionControl_StateDecideAnim | `void (void *self)` | 0x2F66A4 LDRNE R1,[self+0xB4]でR1は入力前に定義される。+0xD4更新とnode virtual。UpdateのPMF呼出はR0 selfのみ、結果はSelectBase_Updateで不使用。 |
| 0x002F7744 ButtonActionControl_Update | `void (void *self)` | 0x2F7744–0x2F7764 はself+0xB8のPMFをBX R1。独立caller 0x1B033C–0x1B034Cはself+0xA00を渡し戻り値不使用。 |
| 0x001B07D8 SelectBase_Ctor | `void *(void *self)` | 0x1B07DC BL CatalogBase_Ctor、0x1B07E4 vtable、0x1B0808先頭をR0に戻し返却。ButtonActionControl ctorのself返却と連鎖。 |
| 0x001C58D0 SelectBase_Draw | `void (void *self)` | 0x1C58D8 self+0x2C、0x1C58F0 tail AddLayout。独立caller 0x1C73C4–0x1C73CCがR0 selfでtail call。 |
| 0x001C59C8 SelectBase_EnterCalc | `void (void *self)` | 0x1C59D0–D4 self+0x178で終了照会、elseはStep、完了はStateMachine_ChangeTo。UpdateのPMF呼出0x1B0428–0x1B0440は結果不使用。 |
| 0x001C55B4 SelectBase_EnterEnter | `void (void *self)` | 0x1C55BC–C4 self+0x178と+0x2CをBind、S0=0でSetFrame、0x1C55F0 vt+0x4CへBX。EnterCalcと同じアニメ所有欄。 |
| 0x001C5A58 SelectBase_LeaveCalc | `void (void *self)` | 0x1C5A60–64 self+0x1A0で終了照会、else Step、完了ChangeTo。UpdateのPMF呼出は結果不使用。 |
| 0x001C5660 SelectBase_LeaveEnter | `void (void *self)` | 0x1C5668–70 self+0x1A0と+0x2CをBind、S0=0でSetFrame、0x1C56A0 vt+0x54へBX。LeaveCalcと同じ欄。 |
| 0x001B0288 SelectBase_Finalize | `void (void *self)` | 0x1B02B4–C4 embedded layout/scrollを解体、0x1B0308–10自分の+0x21Cをfreeへtail call。Ctor・Drawと同じself欄。 |
| 0x001B0314 SelectBase_Update | `void (void *self)` | 0x1B0340 ButtonActionControl_Update、0x1B043C PMF BLX、0x1B0484以降はバイトかclear経路のscratch R0で意味のある結果なし。Ctorで作る+0xA00と一致。 |
| 0x00568C18 UiAnim_Set | `void __usercall(UiAnim *self@<R0>, float frame_count@<S0>, float rate@<S1>, float frame@<S2>, unsigned char flags@<R1>)` | 0x568C1C/2C/34 VSTR S0/S2/S1、0x568C38 STRB R1。独立caller 0x69403C–0x69404Cと0x6940DC–ECはS0/S1/S2とR0/R1を設定。flagsは1と3なのでboolにしない。 |
| 0x00568928 UiAnim_SetFrameToEnd | `void (UiAnim *self)` | 0x568934 VLDR S0,[self+4]、VSUB 1.0、vt+8へSetFrame。0x568954/58はself+8をanim+0x10に転記。SelectBaseとUiAnim_Setが同欄のframeを独立使用。 |
| 0x001280B4 GpuCmd_Advance | `void *(unsigned int bytes)` | 0x1280B8ロード、0x1280BC ADD R0,R0,R2、0x1280C0格納。GetCurrentWritePtrの独立getterと4B8C34のcursor消費がポインタを支持。 |
| 0x004D7164 GpuCmd_GetCurrentWritePtr | `void *(void)` | 0x4D7164–6C LDR R0,[g_GpuCmdPtr]してBX LR。独立caller 0x4B8C44–5Cは戻りをdrawerのcursorとしてvirtualへ渡す。 |
| 0x007B0694 GpuCmd_CommitListAndCaptureDelta | `unsigned int (unsigned int *start, unsigned int *bytes, unsigned int *queue_start, unsigned int *queue_count)` | 0x7B06E8/704/70C/720がR0/R1/R2/R3宛に32bit STR。0x7B0718–1Cの件数差分R0を返す。書き出し内Layout欄の独立使用と一致。 |
| 0x005FC344 script_WordRes_Ctor | `void *(void *self, const unsigned short *text)` | 0x5FC344 STR R1,[R0,#4]、+8=0x3FFFFFFF、先頭にscript_WordRes vtable、R0を維持。独立caller ItemName_ResolvePhrase 0x56D434、旧ソースのUTF16リソース参照と一致。 |

全対象の対応は `_local/evidence/162/manifest.json`、追加前の穴は `_local/evidence/162/holes-before.json`。
元specを保存し、依頼表のワイルドカードを既存名へ展開、旧ソース中の16進番地をsymbols先頭と照合した。
生成器の本体は変更せず、読み込むsymbolsだけを作業ツリーへ切り替えた。
再現: 指定Pythonで `_local/evidence/162/sweep.py after`。
関数の書き出し・全関数索引・データ参照索引を使用。各関数の保存は `_local/evidence/162/<関数名>.txt`。

## 反証条件・未確認点

実機ABIの追試は未実施。voidとした関数のR0を意味のある返値として利用する独立callerが見つかれば再検討する。
初期specから継承する別機能の未設定prototypeも含め、確定しないものはsymbolsを変更せず
`_local/evidence/162/holes-after.json` に残す。
生成の成功と全関数が呼べることは同じではない。prototypeなし関数は道具がaddrだけを出して警告する。

## 生成照合

対象 281 名: {'functions': 176, 'globals': 42, 'types': 54, 'vtables': 9}
追加prototype 23、追加global型 1。残存 38。

## 残存

| 番地 | 名前 | 生成器の診断 | 未確定点 |
|---|---|---|---|
| 0x0064C688 | Actor_SetState | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x002F7A08 | ButtonActionControl_AddNode | prototypeなし | node/descriptor引数の全契約、仮想戻り値またはtail先の戻り値を未確定 |
| 0x002F7448 | ButtonActionControl_LoadAnims | prototypeなし | node/descriptor引数の全契約、仮想戻り値またはtail先の戻り値を未確定 |
| 0x002F5EF4 | ButtonActionControl_TouchInput | prototypeなし | node/descriptor引数の全契約、仮想戻り値またはtail先の戻り値を未確定 |
| 0x004B8360 | DrawCtx_FlushBatch | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00762274 | Effect_DigDirt | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x0066F584 | Effect_ScoopScrape | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00599308 | FieldObj_SpawnActor | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x002FEE38 | Field_GetItemAtXY | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x003159A5 | Field_GrowUpWiltBushSapling | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00315A11 | Field_GrowUpWiltSapling | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00316345 | Field_GrowUpWiltSaplingToItem3 | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x003163C5 | Field_GrowUpWiltSaplingToItem4 | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x0059DA7C | Field_MarkDirty | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00168E08 | Field_SetItemAt | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x002FC950 | Field_SetItemAtWorldXY | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x006A68E4 | Field_XYToWorld | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x001280CC | GpuCmd_SplitAndSubmit | prototypeなし | dispatch/tail先を含む返却契約を未確定 |
| 0x00723604 | Inventory_FindEmptySlot | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x0056D274 | ItemName_ResolvePhrase | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x002FCBB4 | Item_InitWithId | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x002FCB24 | Item_IsEmpty | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00676284 | PlayerState_FaintEnter | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00595A8C | Player_BeginFieldObjAction | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x002FB900 | Save_GetCurrentPlayer | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x006165A8 | graphic_MemoryMgr_AllocByMemoryType | prototypeなし | スタック引数・未使用R3を含む全ABIを未確定 |
| 0x0055D050 | sead_ExpHeap_AllocHeadAligned | prototypeなし | 内部allocator、ブロック・ヒープの全型と各引数の符号/所有権・callerの一致を未確定 |
| 0x00133564 | sead_ExpHeap_Ctor | prototypeなし | 内部allocator、ブロック・ヒープの全型と各引数の符号/所有権・callerの一致を未確定 |
| 0x0074DB48 | sead_ExpHeap_FindFreeBlockHeadAligned | prototypeなし | 内部allocator、ブロック・ヒープの全型と各引数の符号/所有権・callerの一致を未確定 |
| 0x0055D424 | sead_ExpHeap_Free | prototypeなし | 内部allocator、ブロック・ヒープの全型と各引数の符号/所有権・callerの一致を未確定 |
| 0x0012CC4C | sead_ExpHeap_TryCreate | prototypeなし | 内部allocator、ブロック・ヒープの全型と各引数の符号/所有権・callerの一致を未確定 |
| 0x0055D528 | sead_ExpHeap_adjust | prototypeなし | 内部allocator、ブロック・ヒープの全型と各引数の符号/所有権・callerの一致を未確定 |
| 0x00305F6C | vc_A_GETONLINEPLAYERINDEX | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x002FB354 | vc_D_GARDEN | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x0026DB1C | vc_LOADICON | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x005C27D8 | vc_PLAYERINSTANCE | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x00308110 | vc_ROOMDAT | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |
| 0x005BFCE4 | vc_WORLDCOORDS | prototypeなし | 元spec継承分。独立callerを含む全引数/戻り値のABIを未確定（逆コンパイルの見かけのみで付けない） |

残存する関数は生成器が警告してaddrだけを出す。型なし大域のエラーは解消。
全対象は game_api.toml、全出所は manifest.json、初回/最終の穴は holes-before.json / holes-after.json。
