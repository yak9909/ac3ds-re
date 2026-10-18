下書き。オーケストラが取り込みのときに見直す。

# 用語集

検索の入口となる主な呼び名を、記録・symbols に現れる表記で並べた。例は記録 ID または `functions.csv`・`globals.csv` にある名前。英語欄は検索に使う英語表記。タグは `meta/tags.toml` の登録語のみを記す。

## UI・画面遷移

| 日本語の呼び名 | コード上の名前 | 英語 | タグ | スコープ | 例 |
| --- | --- | --- | --- | --- | --- |
| メニュー管理 | `BsMenuMgr` | Menu manager | menu | acnl | `BsMenuMgr_MapOutByKind` |
| メニュー要求 | `Menu_` | Menu request | menu | acnl | `Menu_Setup` |
| メニュータブ | `BsMenuTab` | Menu tab | menu | acnl | `BsMenuTab_ConsumeCommand` |
| メニュー背景 | `BsMenuBg` | Menu background | menu、layout | acnl | `BsMenuBg_StartLeave` |
| 持ち物メニュー | `BsMenuItem` | Item menu | menu、inventory | acnl | `BsMenuItem_EatSelectedItem` |
| カタログ画面 | `BsMenuCatalog` | Catalog menu | menu、catalog | acnl | `BsMenuCatalog_UpdatePreview` |
| 村の地図画面 | `BsMenuMapVillage` | Village map menu | menu、map | acnl | `BsMenuMapVillage_FillListRows` |
| 地図の一覧 | `BsMenuMapList` | Map list | menu、map | acnl | `BsMenuMapList_SelectById` |
| 日付変更画面 | `BsMenuSetupTime` | Time setup menu | menu | acnl | `BsMenuSetupTime_Update` |
| 収納画面 | `BsMenuChest` | Chest menu | menu、storage | acnl | `BsMenuChest_WaitEnter` |
| チャット画面 | `BsMenuChat` | Chat menu | menu、chat | acnl | `BsMenuChat_LoadStep` |
| 部屋の照明スイッチ画面 | `BsMenuRoomLightSwitch` | Room light switch menu | menu、building | acnl | `BsMenuRoomLightSwitch_BuildLayouts` |
| 画面生成 | `UiScreen_` | UI screen | menu | acnl | `UiScreen_RegisterFactoryTable` |
| 一覧の基底 | `SelectBase` | Selection base | menu | acnl | `SelectBase_Finalize` |
| 項目一覧 | `InstSelect` | Instance selection | menu | acnl | `InstSelect_SetSelectVisual` |
| 一覧の変更 | `ChangeListBase` | Change list | menu | acnl | `ChangeListBase_UpdatePageCounters` |
| 共通ボタン | `CommonButtonSingle` | Common button | button、menu | acnl | `CommonButtonSingle_SetMessage` |
| ボタン操作 | `ButtonActionControl` | Button action control | button、touch | acnl | `ButtonActionControl_TouchInput` |
| ボタン部品 | `ButtonActionNode` | Button action node | button、layout | acnl | `ButtonActionNode_SetPanes` |
| スクロールバー | `CommonScrollBar` | Scroll bar | menu、touch | acnl | `CommonScrollBar_AttachTo` |
| 手カーソル | `BsHandCursor` | Hand cursor | menu、touch | acnl | `BsHandCursor_Show` |
| 時計とベルの表示 | `BsTimeBelWindow` | Time and Bells window | menu | acnl | `BsTimeBelWindow_UpdateClockTexts` |
| ベルの箱 | `BellBox` | Bells box | menu | acnl | `BellBox_Init` |
| 文字入力欄 | `TextManager` | Text manager | keyboard | acnl | `TextManager_InputChar` |
| ソフトウェアキーボード | `BsSkb` | Software keyboard | keyboard | acnl | `BsSkb_Wait_Calc` |
| キャラクター作成 | `CharaCreate` | Character creation | player、menu | hhd | `CharaCreate_RefreshHairBaseFromPlayer` |
| キャラクター作成画面 | `CharaFaceLayout` | Character face layout | layout、player | hhd | `CharaFaceLayout_BuildColorGroups` |
| 目の選択部品 | `CharaEyeBaseLayout` | Eye selection layout | layout、player | hhd | `CharaEyeBaseLayout_SetPlayerInfo` |
| 髪の選択部品 | `CharaHairBaseLayout` | Hair selection layout | layout、player | hhd | `CharaHairBaseLayout_SetPlayerInfo` |
| 髪のページ | `HairPageLayout` | Hair page layout | layout、player | hhd | `HairPageLayout_SetHairColorAll` |
| ページスライダー | `PageSlider` | Page slider | touch、menu | hhd | `PageSlider_MoveBy` |
| ドラッグ範囲 | `DragArea` | Drag area | touch | hhd | `DragArea_NextStateFromDragOrSlide` |
| 選択グループ | `SelectGroup` | Selection group | menu、button | hhd | `SelectGroup_SetSelected` |
| ボタン基底 | `ButtonBaseActor` | Button base actor | button | hhd | `ButtonBaseActor_DecideNextStateFromInput` |
| カタログ画面 | `CatalogWindow` | Catalog window | menu、catalog | hhd | `CatalogWindow_BuildStep` |
| カタログタブ | `CatalogTab` | Catalog tab | menu、catalog | hhd | `CatalogTab_CountKinds` |
| カタログ一覧 | `CatalogList` | Catalog list | menu、catalog | hhd | `CatalogList_OnDecide` |
| 家具一覧のセル | `HHD_Tum15_` | Fifteen cell list | menu、catalog、furniture | hhd | `HHD_Tum15_GetSelectedCell` |
| 品名ウィンドウ | `HHD_WinItem_` | Item name window | menu、catalog | hhd | `HHD_WinItem_ReplaceNameInstant` |
| 上段タブ | `HHD_MainTop_` | Main top tab | menu | hhd | `HHD_MainTop_Wait_Exec` |
| 模様替え画面 | `MainScreen` | Main screen | menu、furniture | hhd | `MainScreen_CreatePartActor` |
| 模様替え管理 | `MainEditMgr` | Main edit manager | furniture | hhd | `MainEditMgr_BuildKindLists` |

## レイアウト・描画

| 日本語の呼び名 | コード上の名前 | 英語 | タグ | スコープ | 例 |
| --- | --- | --- | --- | --- | --- |
| レイアウト | `Layout_` | Layout | layout | acnl | `Layout_BindAnim` |
| レイアウト | `LayoutObj_` | Layout object | layout | hhd | `LayoutObj_BaseCtor` |
| レイアウトアニメ | `UiAnim_` | UI animation | layout | acnl | `UiAnim_Ctor` |
| レイアウトアニメ制御 | `LayoutAnimCtrl` | Layout animation control | layout | hhd | `LayoutAnimCtrl_BindSlot` |
| テキストボックス | `nwlyt_TextBox_` | TextBox | layout、font | acnl | `nwlyt_TextBox_AllocStringBuffer_0` |
| テキスト描画 | `TextDraw_` | Text drawing | font | acnl | `TextDraw_EmitStatePrefix` |
| フォント資源 | `nwfont_ResFont_` | Resource font | font | acnl | `nwfont_ResFont_SetGlyphSheetTable` |
| GPU コマンド | `GpuCmd_` | GPU command | model | acnl | `GpuCmd_SelectList` |
| 描画文脈 | `RenderContext` | Render context | model | acnl | `RenderContext_ResetState` |
| シーン描画 | `Render_` | Render | model | acnl | `Render_DrawScene2` |
| 描画パス | `Frame_` | Frame draw pass | model | acnl | `Frame_DrawPass1025` |
| シーン | `Scene_` | Scene | model | acnl | `Scene_ResetAllContexts` |
| モデル実体 | `ModelInstance` | Model instance | model | acnl | `ModelInstance_BindSkeletalAnim` |
| モデル資源 | `ResModel` | Resource model | model | acnl | `ResModel_SetRenderLayer` |
| 3D 資源管理 | `G3dResHolder` | 3D resource holder | model | acnl | `G3dResHolder_RequestLoad` |
| カメラ | `CameraGame_` | Game camera | camera | acnl | `CameraGame_UpdateEye` |
| 部屋カメラ | `HhdCameraGame_` | Room camera | camera | hhd | `HhdCameraGame_ControlRoomContinuous` |
| カメラ補間 | `HhdCameraSpline_` | Camera spline | camera | hhd | `HhdCameraSpline_BuildNaturalCubic` |
| フェード | `Fade_` | Fade | layout | acnl | `Fade_UpdateAndRegisterLayout` |
| フェーダー | `Fader_` | Fader | layout | acnl | `Fader_SetDurationAndStart` |
| 色フェード | `FaderColor` | Color fader | layout | acnl | `FaderColor_Update` |
| 瞬時フェード | `FaderMoment` | Moment fader | layout | acnl | `FaderMoment_Update` |
| ワイプ | `Wipe_` | Wipe | layout | acnl | `Wipe_CreateSingletons` |
| 背景レイアウト | `CharaBgLayout` | Character background layout | layout | hhd | `CharaBgLayout_Ctor` |
| ボタンレイアウト | `ButtonLayout` | Button layout | button、layout | hhd | `ButtonLayout_BindStandardAnims` |

## 持ち物・家具・カタログ

| 日本語の呼び名 | コード上の名前 | 英語 | タグ | スコープ | 例 |
| --- | --- | --- | --- | --- | --- |
| 持ち物 | `Inventory_` | Inventory | inventory | acnl | `Inventory_AddItem` |
| ポケット | `Pocket_` | Pocket | inventory | acnl | `Pocket_DecorateInHouse` |
| 持ち物操作 | `ItemMenu_` | Item menu action | inventory、menu | acnl | `ItemMenu_UpdateActionFlags` |
| 持ち物選択欄 | `ItemSelectWindow` | Item selection window | inventory、menu | acnl | `ItemSelectWindow_LayoutRows` |
| 選択品名欄 | `ItemSelectNameWindow` | Item name window | inventory、menu | acnl | `ItemSelectNameWindow_FitWidth` |
| 持ち物ドラッグ欄 | `ItemDragWindow` | Item drag window | inventory、touch | acnl | `ItemDragWindow_ExitUpdate` |
| 持ち物アイコン | `ItemIconWidget` | Item icon widget | inventory、layout | acnl | `ItemIconWidget_SetItem` |
| 品物 | `Item_` | Item | inventory | acnl | `Item_CanPlant` |
| 品物 | `Item_` | Item | furniture | hhd | `Item_GetModelName` |
| 品物パラメータ | `ItemParam_` | Item parameters | inventory | acnl | `ItemParam_GetModelName` |
| 品物パラメータ | `ItemParam_` | Item parameters | furniture | hhd | `ItemParam_LoadFiles` |
| 品物モデル | `ItemModel` | Item model | model、inventory | acnl | `ItemModel_BuildPath` |
| 家具管理 | `BsFtrMgr` | Furniture manager | furniture | acnl | `BsFtrMgr_PopulateRoom` |
| 家具 | `AcFtr_` | Furniture | furniture | acnl | `AcFtr_CreateFinalize` |
| 家具の占有範囲 | `FurnitureFootprint` | Furniture footprint | furniture | acnl | `FurnitureFootprint_Init` |
| 家具格子 | `FtrGrid` | Furniture grid | furniture | acnl | `FtrGrid_SetCells` |
| 家具操作 | `FurnitureActor` | Furniture actor | furniture | hhd | `FurnitureActor_ExecutePushPullMove` |
| 家具配置格子 | `FtrObjectGrid` | Furniture object grid | furniture | hhd | `FtrObjectGrid_GetActorAtWorldXZ` |
| 家具自動配置 | `HHD_Room_` | Room furniture placement | furniture | hhd | `HHD_Room_RequestFurnitureAutoPlacement` |
| 壁紙変更 | `HHD_Room_` | Wallpaper change | furniture | hhd | `HHD_Room_RequestWallpaperChange` |
| 床材変更 | `HHD_Room_` | Flooring change | furniture | hhd | `HHD_Room_RequestFlooringChange` |
| 家具の落とし先 | `DropTarget` | Drop target | furniture、touch | hhd | `DropTarget_UpdateSelect` |
| ゴミ箱部品 | `TrashPart` | Trash part | furniture、touch | hhd | `TrashPart_GetDropPosition` |
| ゴミ箱レイアウト | `TrashLayout` | Trash layout | furniture、layout | hhd | `TrashLayout_BindAnims` |
| 家具カタログ | `Catalog_` | Catalog | catalog、furniture | hhd | `Catalog_LoadVisibleIcons` |

## マップ・建物・フィールド

| 日本語の呼び名 | コード上の名前 | 英語 | タグ | スコープ | 例 |
| --- | --- | --- | --- | --- | --- |
| フィールド | `Field_` | Field | map | acnl | `Field_GrowUp` |
| フィールド | `Field_` | Field | map | hhd | `Field_TileToWorldFlat` |
| フィールドの物 | `FieldObj_` | Field object | map | acnl | `FieldObj_PlayPlantEffect` |
| フィールド属性 | `FieldAttr_` | Field attributes | map | acnl | `FieldAttr_CanPlaceItem` |
| 地図の基底 | `MapBase` | Map base | map | acnl | `MapBase_PutIconAtTile` |
| 島の状態 | `IslandRuntime` | Island runtime | island、map | acnl | `IslandRuntime_GetItemQuadrant` |
| 建物 | `Building_` | Building | building | acnl | `Building_GetFootprint` |
| 構造物 | `Structure_` | Structure | building | acnl | `Structure_StampAll` |
| 橋の管理 | `BsStrcMgr` | Structure manager | building | acnl | `BsStrcMgr_TrackBridges` |
| 公共事業のプレビュー | `PwpPreview` | Public works preview | building | acnl | `PwpPreview_Update` |
| 部屋 | `Room_` | Room | building | acnl | `Room_GetInteriorWorldBounds` |
| 部屋 | `Room_` | Room | building、furniture | hhd | `Room_GetMovingFurnitureQuadrant` |
| 部屋データ | `RoomData` | Room data | building、furniture | acnl | `RoomData_SetWallpaper` |

## プレイヤー・住民・会話

| 日本語の呼び名 | コード上の名前 | 英語 | タグ | スコープ | 例 |
| --- | --- | --- | --- | --- | --- |
| プレイヤー | `Player_` | Player | player | acnl | `Player_OnDayChange` |
| プレイヤー状態 | `PlayerState_` | Player state | player-state | acnl | `PlayerState_GetAttributes` |
| プレイヤー動作 | `PlayerAction_` | Player action | player-state | acnl | `PlayerAction_PutAwayWait` |
| プレイヤーモデル | `PlayerModel_` | Player model | player、model | acnl | `PlayerModel_CalcAnim` |
| プレイヤー外見 | `PlayerAppearance_` | Player appearance | player | acnl | `PlayerAppearance_SetEyeColor` |
| 顔の記録 | `LookRecord_` | Look record | player | acnl | `LookRecord_GetFace` |
| 目の種類 | `PlayerLook_` | Player look | player | hhd | `PlayerLook_GetEyeType` |
| 目の色ボタン | `ColorButtonPart` | Color button part | player、button | hhd | `ColorButtonPart_SetEyeColor` |
| 髪のボタン | `HairButtonPart` | Hair button part | player、button | hhd | `HairButtonPart_SetHairColor` |
| 住民 | `Villager_` | Villager | villager | acnl | `Villager_TryMoveIn` |
| 住民の動作 | `NpcAction_` | NPC action | villager | acnl | `NpcAction_ConsumeRequest` |
| 会話の文字送り | `TalkSeq_` | Talk sequence | message | acnl | `TalkSeq_StepText` |
| ルビ付きメッセージ | `MsgStream_` | Message stream | message | acnl | `MsgStream_ReadRubyCode` |
| メッセージ | `Msg_` | Message | message | acnl | `Msg_FormatLabel03d` |
| チャット欄 | `ChatWindow` | Chat window | chat | acnl | `ChatWindow_ConsumeInputResult` |
| 手紙 | `Letter_` | Letter | message | acnl | `Letter_InitFromCurrentPlayer` |
| 郵便 | `Mail_` | Mail | message | acnl | `Mail_SendSpTsunekichi` |
| 掲示板 | `Bbs_` | Bulletin board | message | acnl | `Bbs_RemovePostAtIndex` |

## 音・入力・システム

| 日本語の呼び名 | コード上の名前 | 英語 | タグ | スコープ | 例 |
| --- | --- | --- | --- | --- | --- |
| カタログのページ音 | `HHD_Audio_` | Catalog slide audio | catalog | hhd | `HHD_Audio_UpdateCatalogSlide` |
| タッチ入力 | `Touch_` | Touch input | touch | acnl | `Touch_ResetState` |
| タッチ入力 | `TouchInput_` | Touch input | touch | hhd | `TouchInput_Update` |
| ボタン入力 | `GameInput_` | Game input | button | acnl | `GameInput_IsMaskReleased` |
| ボタン入力 | `HhdGameInput_` | Game input | button | hhd | `HhdGameInput_IsMaskHeld` |
| ドラッグ操作 | `DragControl` | Drag control | touch | acnl | `DragControl_AppendIconGroup` |
| ドラッグ追跡 | `DragTracker` | Drag tracker | touch | hhd | `DragTracker_Update` |
| セーブ | `Save_` | Save | save-data | acnl | `Save_RunDayChange` |
| 家のセーブ | `HouseSave` | House save | save-data、building | acnl | `HouseSave_UpdateOnDayChange` |
| セーブ用カウンター | `HHD_SaveCounters_` | Save counters | save-data | hhd | `HHD_SaveCounters_GetBase` |
| 時刻 | `Time_` | Time | save-data | acnl | `Time_LoadFromSave` |
| 日付 | `Date_` | Date | save-data | acnl | `Date_GetRaw` |
| 通信 | `Net_` | Network | player | acnl | `Net_IsMultiplayer` |
| 通信転送 | `NetTransfer_` | Network transfer | player | acnl | `NetTransfer_SendSegments` |
| ファイル資源 | `FileRes` | File resource | layout | acnl | `FileRes_RequestLoadAsync` |
| アーカイブ資源 | `ArcResAccReader` | Archive resource reader | layout | acnl | `ArcResAccReader_Ctor` |
| ヒープ | `Heap_` | Heap | heap | acnl | `Heap_CreateNamed` |
| ヒープアロケータ | `HeapAllocator` | Heap allocator | heap | acnl | `HeapAllocator_DestroyHeap` |
| フレームワーク | `Framework_` | Framework | sead | acnl | `Framework_GetFPS` |
| 状態機械 | `StateMachine` | State machine | player-state | hhd | `StateMachine_ChangeState` |

