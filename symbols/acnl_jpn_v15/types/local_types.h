// ローカルの型（IDA の print_decls の出力を、名前順・依存順に並べた物）

struct ACNL_BbsPost;
struct ACNL_NetPeerAckStatePartial;
struct ACNL_NetPeerTxFrameStatePartial;
struct ACNL_TownTransferFragmentHeader;
struct ACNL_TownTransferState;
struct AcnlBsMenuChestPrefixF006;
struct AcnlButtonNodeSetupF011;
struct AcnlChangeStockItemPrefixF006;
struct AcnlControllerPrefixF005;
struct AcnlDragControlPrefixF010;
struct AcnlDragEndpointsF008;
struct AcnlDragIconGroupF010;
struct AcnlDragIconGroupF012;
struct AcnlEncryptedValueF010;
struct AcnlFurnitureFootprint_F016;
struct AcnlFurnitureLifecyclePrefix_F016;
struct AcnlFurniturePlacementRecord_F016;
struct AcnlIntrusiveNodeF010;
struct AcnlItemDragIconNodeF009;
struct AcnlItemOptionDescriptorF010;
struct AcnlItemSelectRowF010;
struct AcnlItemSelectRowF011;
struct AcnlItemSelectSystemPrefixF010;
struct AcnlLayoutRecordPrefix_F016;
struct AcnlMenuScreenListF006;
struct AcnlMenuScreenNodeF006;
struct AcnlPartsDragNodeF010;
struct AcnlPartsDragNodeF012;
struct AcnlPlayerInventoryFinanceF010;
struct AcnlRoomCameraPrefix;
struct AcnlUiAnimStorageF010;
struct AcnlUiMtx34F005;
struct AcnlUiPoint2F005;
struct AcnlUiPoint2IF005;
struct AcnlUiPoint3F005;
struct AcnlUiRectF005;
struct AcnlWordFix65F011;
struct AttachProcessEvent;
struct AttachThreadEvent;
struct BsMenuRoomLightSwitch_T022;
struct CodeSetHeader;
struct CpuRegisters;
struct DebugEventInfo;
struct DebuggerBreakExceptionEvent;
struct DigRecord;
struct DmaConfig;
struct DmaDeviceConfig;
struct DropData;
struct ERRF_ExceptionData;
struct ERRF_ExceptionInfo;
struct ERRF_FatalErrInfo;
struct ExceptionEvent;
struct ExitProcessEvent;
struct ExitThreadEvent;
struct FS_ProgramInfo;
struct FaderBase;
struct FaultExceptionEvent;
struct FieldActionActive;
struct FieldObjDef;
struct FpuRegisters;
struct FurnitureFootprintDescriptorPrefix_F016;
struct GohanItemActionPmf8;
struct GohanNativeDate;
struct IPCStaticBuffer;
struct IslandRuntimeBuilding;
struct IslandRuntimeData;
struct IslandRuntimeItem;
struct ItemCategoryRangeEntry;
struct ItemID;
struct ItemParamRecord;
struct LetterDragWindowAttachmentPrefix_F014;
struct LightEvent;
struct LightSemaphore;
struct MapEvent;
struct MemInfo;
struct NwlytLayoutDrawPrefix_F015;
struct NwlytPaneDrawPrefix_F015;
struct NwlytTrigRecord_F015;
struct OutputStringEvent;
struct PageInfo;
struct PlayerC4ArgumentBlock;
struct PlayerC5ArgumentBlock;
struct PlayerStateContextPrefix;
struct RecursiveLock;
struct RoomCameraInterpolation16;
struct RoomCameraModeEntry16;
struct RoomCameraPmf8;
struct RoomCameraProfile20;
struct RoomTransitionKindPair;
struct ScheduleInOutEvent;
struct StopPointExceptionEvent;
struct SvcResult32;
struct SvcResult64;
struct SvcResult8;
struct SvcResultGetDebugThreadParam;
struct SvcResultHandle;
struct SvcResultHandlePair;
struct SvcResultQueryMemory;
struct SyscallInOutEvent;
struct T022_GraphicMemoryMgrPrefix;
struct T022_HouseSaveExteriorPrefix;
struct T022_ModelHolderPrefix;
struct T022_RoomViewSurfacePrefix;
struct T022_RoomWallPartPrefix;
struct TI_C;
struct TI_S;
struct TI_V;
struct TLS;
struct ThreadContext;
struct TiledByteGridPrefix;
struct UiAnim;
struct UserBreakExceptionEvent;
struct WeatherParticleGroupPrefix;
struct WeatherParticleSlot;
union __n128;
union __n64;
struct cxxabi_class_type_info;
struct cxxabi_si_class_type_info;
struct cxxabi_vmi_class_type_info;
union float16x2_t;
union float16x4_t;
union float16x8_t;
union float32x2_t;
union float32x4_t;
union float64x2_t;
union int16x2_t;
union int16x4_t;
union int16x8_t;
union int32x2_t;
union int32x4_t;
union int64x2_t;
union int8x16_t;
union int8x8_t;
union poly128_t;
union poly16x4_t;
union poly16x8_t;
union poly8x16_t;
union poly8x8_t;
struct svbool_t;
struct svfloat16_t;
struct svfloat32_t;
struct svfloat64_t;
struct svint16_t;
struct svint32_t;
struct svint64_t;
struct svint8_t;
struct svuint16_t;
struct svuint32_t;
struct svuint64_t;
struct svuint8_t;
union uint16x2_t;
union uint16x4_t;
union uint16x8_t;
union uint32x2_t;
union uint32x4_t;
union uint64x2_t;
union uint8x16_t;
union uint8x8_t;

// type: ACNL_BbsPost
#pragma pack(push, 2)
struct ACNL_BbsPost
{
  unsigned __int8 unknown_0[426];
  unsigned __int16 stateFlags;
};
#pragma pack(pop)

// type: ACNL_BbsPostStateFlags
enum __bitmask ACNL_BbsPostStateFlags
{
  ACNL_BBS_POST_PRESENT = 0x1,
};

// type: ACNL_NetPacketType
enum ACNL_NetPacketType
{
  ACNL_PKT_ROOM_REPORT = 0x1,
  ACNL_PKT_OUTDOOR_READY_A = 0x66,
  ACNL_PKT_OUTDOOR_READY_B = 0x67,
  ACNL_PKT_OUTDOOR_RETURN_REQUEST = 0x6A,
  ACNL_PKT_OUTDOOR_RELOAD = 0x6B,
  ACNL_PKT_BBS_POST = 0x81,
  ACNL_PKT_BBS_DELETE = 0x82,
};

// type: ACNL_NetPeerAckStatePartial
#pragma pack(push, 2)
struct ACNL_NetPeerAckStatePartial
{
  unsigned __int8 unknown0[24];
  unsigned __int8 pendingAckCount[4];
};
#pragma pack(pop)

// type: ACNL_NetPeerTxFrameStatePartial
#pragma pack(push, 2)
struct ACNL_NetPeerTxFrameStatePartial
{
  unsigned __int8 unknown0[4];
  unsigned __int8 *frameBase[4];
  unsigned int frameCursor[4];
  unsigned __int8 unackedFrameCount[4];
};
#pragma pack(pop)

// type: ACNL_TownTransferFragmentHeader
#pragma pack(push, 2)
struct ACNL_TownTransferFragmentHeader
{
  unsigned int streamOffset;
};
#pragma pack(pop)

// type: ACNL_TownTransferState
#pragma pack(push, 2)
struct ACNL_TownTransferState
{
  unsigned int unknown_0;
  unsigned int streamOffset;
};
#pragma pack(pop)

// type: ACNL_TransferType
enum __bitmask ACNL_TransferType
{
  ACNL_TRANSFER_TOWN = 0xC,
};

// type: AcnlBsMenuChestPrefixF006
#pragma pack(push, 2)
struct AcnlBsMenuChestPrefixF006
{
  void *vtable;
  unsigned __int8 unknown_4[4];
  unsigned int menu_id;
  unsigned __int8 unknown_12[28];
  void *state_vtable;
  const char *state_name;
  unsigned __int8 state_active;
  unsigned __int8 unknown_49[3];
  void *state_calc;
  int state_adjust;
  unsigned int state_frames;
  unsigned __int8 state_changed;
  unsigned __int8 unknown_65[3];
  void *state_table;
  unsigned int state_count;
  void *cabinet;
  unsigned __int8 item_drag_window[33896];
  unsigned __int8 drag_controls[280];
  unsigned __int8 choice_window[3172];
  unsigned __int8 item_name_window[1264];
  int hovered_index;
  int named_index;
  unsigned __int8 input_locked;
  unsigned __int8 unknown_38701[3];
  unsigned int build_step;
};
#pragma pack(pop)

// type: AcnlButtonNodeSetupF011
#pragma pack(push, 2)
struct AcnlButtonNodeSetupF011
{
  void *hit_pane;
  void *animation_group;
  unsigned int unknown8;
  unsigned int unknown12;
  unsigned int shortcut;
  unsigned int index;
  unsigned int flags;
};
#pragma pack(pop)

// type: AcnlCatalogSoundId_F015
enum AcnlCatalogSoundId_F015
{
  ACNL_SE_SYS_BOOK_ICON_SELECTED_F015 = 0x1000413,
  ACNL_SE_SYS_CTLG_TOP_BTN_SELECTED_F015 = 0x100046C,
};

// type: AcnlChangeStockItemPrefixF006
#pragma pack(push, 2)
struct AcnlChangeStockItemPrefixF006
{
  void *vtable;
  unsigned __int8 unknown_4[32];
  const char *base_layout_name;
  unsigned __int8 arc_reader[584];
  unsigned __int8 base_layout[332];
  unsigned __int8 in_anim[40];
  unsigned __int8 out_anim[40];
  unsigned __int8 base_controls[1584];
  unsigned int base_build_step;
  void *state_vtable;
  const char *state_name;
  unsigned __int8 state_active;
  unsigned __int8 unknown_2633[3];
  void *state_calc;
  int state_adjust;
  unsigned int state_frames;
  unsigned __int8 state_changed;
  unsigned __int8 unknown_2649[3];
  void *state_table;
  unsigned int state_count;
  const char *slot_layout_name;
  const char **tab_groups;
  const char *slot_position_name;
  unsigned __int8 slot_layout[332];
  unsigned __int8 animations[360];
  void *active_scroll_anim;
  unsigned __int8 unknown_3368[8];
  void *slot_root_pane;
  unsigned __int8 tab_and_page_nodes[1824];
  unsigned __int8 tab_controls[320];
  unsigned __int8 page_controls[320];
  unsigned __int8 total_page_text[196];
  unsigned __int8 current_page_text[196];
  unsigned int current_tab;
  unsigned int page_by_tab[4];
  unsigned int page_count;
  unsigned int controls_index_base;
  unsigned int page_sound;
  unsigned int chosen_control;
  unsigned __int8 tabs_enabled;
  unsigned __int8 unknown_6273[3];
  unsigned int build_step;
  unsigned __int8 item_widgets[8760];
  unsigned __int8 item_cursor[480];
  unsigned __int8 setup_done;
  unsigned __int8 unknown_15521[3];
  unsigned int item_index_base;
};
#pragma pack(pop)

// type: AcnlClosetMenuIdF006
enum AcnlClosetMenuIdF006
{
  AcnlClosetMenu_Normal_F006 = 0x3D,
  AcnlClosetMenu_Warehouse_F006 = 0x89,
};

// type: AcnlPointerFlagsF005
enum __bitmask AcnlPointerFlagsF005
{
  AcnlPointerValid_F005 = 0x1,
  AcnlPointerPressed_F005 = 0x2,
  AcnlPointerReleased_F005 = 0x4,
  AcnlPointerClearPosition_F005 = 0x8,
};

// type: AcnlUiPoint2F005
#pragma pack(push, 2)
struct AcnlUiPoint2F005
{
  float x;
  float y;
};
#pragma pack(pop)

// type: AcnlUiPoint2IF005
#pragma pack(push, 2)
struct AcnlUiPoint2IF005
{
  int x;
  int y;
};
#pragma pack(pop)

// type: AcnlControllerPrefixF005
#pragma pack(push, 2)
struct AcnlControllerPrefixF005
{
  void *vtable;
  unsigned int pressed;
  unsigned int released;
  unsigned int repeat;
  AcnlPointerFlagsF005 pointer_flags;
  AcnlUiPoint2IF005 pixel_int;
  AcnlUiPoint2F005 pointer_min;
  AcnlUiPoint2F005 pointer_max;
  unsigned __int8 unknown_to_button_count[208];
  int button_count;
  int axis0_bit;
  int axis1_bit;
  int pointer_bit;
  unsigned int unknown_268;
  unsigned int held;
  AcnlUiPoint2F005 pixel_float;
};
#pragma pack(pop)

// type: AcnlMenuScreenNodeF006
#pragma pack(push, 2)
struct AcnlMenuScreenNodeF006
{
  void *vptr;
  AcnlMenuScreenNodeF006 *prev;
  AcnlMenuScreenNodeF006 *next;
  void *actor;
  unsigned __int8 menu_id;
  unsigned __int8 padding[3];
};
#pragma pack(pop)

// type: AcnlMenuScreenListF006
#pragma pack(push, 2)
struct AcnlMenuScreenListF006
{
  void *vptr;
  AcnlMenuScreenNodeF006 *head;
  AcnlMenuScreenNodeF006 *tail;
};
#pragma pack(pop)

// type: AcnlIntrusiveNodeF010
#pragma pack(push, 2)
struct AcnlIntrusiveNodeF010
{
  void **vtable;
  struct AcnlIntrusiveNodeF010 *prev;
  struct AcnlIntrusiveNodeF010 *next;
};
#pragma pack(pop)

// type: AcnlUiAnimStorageF010
#pragma pack(push, 2)
struct AcnlUiAnimStorageF010
{
  unsigned __int8 storage[40];
};
#pragma pack(pop)

// type: AcnlDragIconGroupF010
#pragma pack(push, 2)
struct AcnlDragIconGroupF010
{
  AcnlMenuScreenListF006 nodes;
  AcnlIntrusiveNodeF010 registry;
  void *layout;
  void *source_pane;
  AcnlUiAnimStorageF010 select_anim;
  unsigned int unknown72;
  AcnlUiAnimStorageF010 animations[6];
  unsigned __int8 flags316[4];
};
#pragma pack(pop)

// type: AcnlPartsDragNodeF010
#pragma pack(push, 2)
struct AcnlPartsDragNodeF010
{
  unsigned __int8 button[224];
  AcnlUiAnimStorageF010 drag_anim;
  unsigned int mode;
  unsigned __int8 unknown268[24];
  AcnlDragIconGroupF010 *group;
  unsigned __int16 unknown296;
  unsigned __int16 unknown298;
  unsigned __int8 active;
  unsigned __int8 enabled;
  unsigned __int8 pad[2];
};
#pragma pack(pop)

// type: AcnlDragControlPrefixF010
#pragma pack(push, 2)
struct AcnlDragControlPrefixF010
{
  AcnlMenuScreenListF006 nodes;
  unsigned __int8 unknown12[168];
  AcnlPartsDragNodeF010 *source;
  unsigned int state_calc;
  unsigned int state_adjust;
  unsigned __int8 unknown192[16];
  unsigned __int16 input_mode;
  unsigned __int8 source_order;
  unsigned __int8 pad211;
  unsigned int flags;
  int repeat_counter;
  int repeat_threshold;
  unsigned __int8 first_repeat;
  unsigned __int8 pad225[3];
  AcnlMenuScreenListF006 groups;
  unsigned __int8 unknown240[8];
  unsigned __int8 dragging;
  unsigned __int8 unknown249[11];
  AcnlPartsDragNodeF010 *target;
};
#pragma pack(pop)

// type: AcnlDragEndpointsF008
#pragma pack(push, 2)
struct AcnlDragEndpointsF008
{
  unsigned __int8 unknown_0[180];
  void *source_node;
  unsigned __int8 unknown_184[76];
  void *target_node;
};
#pragma pack(pop)

// type: AcnlDragIconGroupF012
#pragma pack(push, 2)
struct AcnlDragIconGroupF012
{
  AcnlMenuScreenListF006 nodes;
  unsigned int registry[3];
  void *layout;
  void *pane;
  AcnlUiAnimStorageF010 select_anim;
  unsigned int unknown72;
  AcnlUiAnimStorageF010 animations[6];
  unsigned __int8 active;
  unsigned __int8 can_start_drag;
  unsigned __int8 can_click;
  unsigned __int8 can_receive_drop;
};
#pragma pack(pop)

// type: AcnlEncryptedValueF010
#pragma pack(push, 2)
struct AcnlEncryptedValueF010
{
  unsigned int ciphertext;
  unsigned __int16 salt;
  unsigned __int8 rotation;
  unsigned __int8 checksum;
};
#pragma pack(pop)

// type: AcnlFurnitureFootprint_F016
#pragma pack(push, 2)
struct AcnlFurnitureFootprint_F016
{
  unsigned __int8 kind;
  unsigned __int8 rotation;
};
#pragma pack(pop)

// type: ItemID
#pragma pack(push, 2)
struct ItemID
{
  unsigned __int16 id;
  unsigned __int16 flags;
};
#pragma pack(pop)

// type: ItemParamRecord
#pragma pack(push, 2)
struct ItemParamRecord
{
  unsigned __int8 unknown_00[10];
  unsigned __int8 category;
  unsigned __int8 unknown_0B[6];
  unsigned __int8 furnitureFamily;
  unsigned __int8 unknown_12[7];
  unsigned __int8 placementInfo;
  unsigned __int8 unknown_1A[4];
};
#pragma pack(pop)

// type: AcnlFurnitureLifecyclePrefix_F016
#pragma pack(push, 2)
struct AcnlFurnitureLifecyclePrefix_F016
{
  unsigned __int8 unknown00[15];
  unsigned __int8 destroyRequested;
  unsigned __int8 unknown10[86];
  unsigned __int8 createFlags;
  unsigned __int8 unknown67[1405];
  ItemID item;
  unsigned __int8 spawnX;
  unsigned __int8 spawnZ;
  unsigned __int8 spawnRotation;
  unsigned __int8 spawnLayer;
  unsigned __int8 requestKind;
  unsigned __int8 gap5ED[3];
  const ItemParamRecord *itemParam;
  void *furnitureInfo;
  unsigned __int8 state;
  unsigned __int8 gap5F9[443];
  unsigned __int8 currentLayer;
};
#pragma pack(pop)

// type: AcnlFurniturePlacementRecord_F016
#pragma pack(push, 2)
struct AcnlFurniturePlacementRecord_F016
{
  ItemID item;
  unsigned __int8 x;
  unsigned __int8 z;
  unsigned __int8 rotation;
  unsigned __int8 layer;
  unsigned __int8 requestKind;
  unsigned __int8 reserved[3];
};
#pragma pack(pop)

// type: AcnlFurnitureState_F016
enum AcnlFurnitureState_F016
{
  FtrStateReady_F016 = 0x2,
  FtrStateDestroyImmediately_F016 = 0x7,
};

// type: AcnlItemDragIconNodeF009
#pragma pack(push, 2)
struct AcnlItemDragIconNodeF009
{
  unsigned int vtable;
  unsigned __int8 unknown004[213];
  unsigned __int8 icon_interaction;
  unsigned __int8 unknown218[83];
  unsigned __int8 accepts_input;
  unsigned __int8 unknown302[2];
  void *icon_accessor;
  unsigned __int8 layout_storage[332];
  void *disabled_animation;
  unsigned __int8 unknown644[20];
  void *number_pane;
  void *selection_pane;
  unsigned __int16 item_id;
  unsigned __int16 item_flags;
  unsigned __int8 unknown676[200];
};
#pragma pack(pop)

// type: AcnlItemOptionDescriptorF010
#pragma pack(push, 2)
struct AcnlItemOptionDescriptorF010
{
  unsigned __int8 text_kind;
  unsigned __int8 pad1[3];
  unsigned int clear_text;
  const char *message_archive;
  int message_index;
  unsigned int flags0;
  unsigned int flags1;
  unsigned int action_id;
  unsigned __int8 sound_kind;
  unsigned __int8 text_flags[3];
};
#pragma pack(pop)

// type: AcnlItemSelectRowF010
#pragma pack(push, 2)
struct AcnlItemSelectRowF010
{
  unsigned int flags0;
  unsigned int flags1;
  unsigned __int8 word[156];
  unsigned __int8 sound_kind;
  unsigned __int8 pad[3];
  unsigned int action_id;
};
#pragma pack(pop)

// type: AcnlWordFix65F011
#pragma pack(push, 2)
struct AcnlWordFix65F011
{
  void *vptr;
  unsigned __int16 *buffer;
  unsigned int capacity;
  unsigned __int8 flags;
  unsigned __int8 pad13[3];
  int metadata0;
  int metadata1;
  unsigned __int16 text[65];
  unsigned __int8 tail[2];
};
#pragma pack(pop)

// type: AcnlItemSelectRowF011
#pragma pack(push, 2)
struct AcnlItemSelectRowF011
{
  unsigned int flags0;
  unsigned int flags1;
  AcnlWordFix65F011 word;
  unsigned __int8 sound_kind;
  unsigned __int8 pad165[3];
  unsigned int action_id;
};
#pragma pack(pop)

// type: AcnlItemSelectSystemPrefixF010
#pragma pack(push, 2)
struct AcnlItemSelectSystemPrefixF010
{
  void **vtable;
  unsigned __int8 preparing;
  unsigned __int8 pad[3];
  unsigned int count;
  AcnlItemSelectRowF010 *rows;
  unsigned int capacity;
  AcnlItemSelectRowF010 name;
  int cancel_index;
  unsigned __int8 flags196[6];
  unsigned __int8 unknown202[14];
  unsigned __int8 built;
  unsigned __int8 pad217[3];
};
#pragma pack(pop)

// type: AcnlKeyboardResultF007
enum AcnlKeyboardResultF007
{
  AcnlKeyboard_KeepPrevious = 0xFFFFFFFF,
  AcnlKeyboard_Cancel = 0x1,
  AcnlKeyboard_Submit = 0x2,
};

// type: AcnlLayoutRecordPrefix_F016
#pragma pack(push, 2)
struct AcnlLayoutRecordPrefix_F016
{
  unsigned __int8 unknown00[16];
  unsigned __int8 innerLayout[269];
  unsigned __int8 recordDirty;
  unsigned __int8 unknown11E[2];
};
#pragma pack(pop)

// type: AcnlPartsDragNodeF012
#pragma pack(push, 2)
struct AcnlPartsDragNodeF012
{
  unsigned __int8 button[224];
  AcnlUiAnimStorageF010 drag_anim;
  void *drop_hit_pane;
  unsigned __int8 unknown268[24];
  AcnlDragIconGroupF012 *group;
  unsigned __int16 touch_x;
  unsigned __int16 touch_y;
  unsigned __int8 active;
  unsigned __int8 enabled;
  unsigned __int8 pad[2];
};
#pragma pack(pop)

// type: AcnlPlayerInventoryFinanceF010
#pragma pack(push, 2)
struct AcnlPlayerInventoryFinanceF010
{
  unsigned __int8 unknown0[27532];
  AcnlEncryptedValueF010 bank;
  AcnlEncryptedValueF010 loan;
  AcnlEncryptedValueF010 medals;
  unsigned __int8 unknown_after_medals[44];
  ItemID pocket[16];
  unsigned __int8 pocket_flags[16];
  unsigned __int8 unknown_after_pocket[744];
  AcnlEncryptedValueF010 wallet;
  unsigned __int8 unknown_after_wallet[9184];
  ItemID storage[180];
};
#pragma pack(pop)

// type: RoomCameraPmf8
#pragma pack(push, 2)
struct RoomCameraPmf8
{
  unsigned int functionOrOffset;
  signed int thisAdjustmentTag;
};
#pragma pack(pop)

// type: AcnlRoomCameraPrefix
#pragma pack(push, 2)
struct AcnlRoomCameraPrefix
{
  void *vtable;
  float base[3];
  float offset[3];
  unsigned __int16 polar;
  unsigned __int16 yaw;
  float distance;
  float target[3];
  float eye[3];
  unsigned __int8 gap_3C[182];
  unsigned __int8 mode;
  unsigned __int8 requestedMode;
  unsigned __int8 gap_F4[32];
  float targetBase[3];
  float targetOffset[3];
  unsigned __int16 targetPolar;
  unsigned __int16 targetYaw;
  float targetDistance;
  unsigned __int8 gap_134[1];
  signed __int8 interpolationId;
  unsigned __int8 gap_136[6];
  const unsigned __int8 *profileIds;
  RoomCameraPmf8 yawSetter;
  RoomCameraPmf8 verticalSetter;
  unsigned __int8 gap_150[4];
  float transitionFrame;
  unsigned __int8 gap_158[80];
  unsigned __int8 yawIndex;
  unsigned __int8 verticalIndex;
  unsigned __int8 gap_1AA[16];
  unsigned __int8 inputBlocked;
};
#pragma pack(pop)

// type: AcnlUiMtx34F005
#pragma pack(push, 2)
struct AcnlUiMtx34F005
{
  float m[3][4];
};
#pragma pack(pop)

// type: AcnlUiPoint3F005
#pragma pack(push, 2)
struct AcnlUiPoint3F005
{
  float x;
  float y;
  float z;
};
#pragma pack(pop)

// type: AcnlUiRectF005
#pragma pack(push, 2)
struct AcnlUiRectF005
{
  float left;
  float top;
  float right;
  float bottom;
};
#pragma pack(pop)

// type: ArbitrationType
enum ArbitrationType
{
  ARBITRATION_SIGNAL = 0x0,
  ARBITRATION_WAIT_IF_LESS_THAN = 0x1,
  ARBITRATION_DECREMENT_AND_WAIT_IF_LESS_THAN = 0x2,
  ARBITRATION_WAIT_IF_LESS_THAN_TIMEOUT = 0x3,
  ARBITRATION_DECREMENT_AND_WAIT_IF_LESS_THAN_TIMEOUT = 0x4,
};

// type: uint32_t
typedef unsigned int uint32_t;

// type: u32
typedef uint32_t u32;

// type: uint64_t
typedef unsigned __int64 uint64_t;

// type: u64
typedef uint64_t u64;

// type: AttachProcessEvent
struct AttachProcessEvent
{
  u64 program_id;
  char process_name[8];
  u32 process_id;
  u32 other_flags;
};

// type: AttachThreadEvent
struct AttachThreadEvent
{
  u32 creator_thread_id;
  u32 thread_local_storage;
  u32 entry_point;
};

// type: BOOL
typedef int BOOL;

// type: BsMenuRoomLightSwitch_T022
struct BsMenuRoomLightSwitch_T022
{
  void *vtable;
  unsigned __int8 unknown_004[52];
  unsigned __int8 roomLightLayout[332]; ///< IDA-gpt-6.1-sol-F004 / 0x32592CのBuild/FindPaneとrom_lgt資源で照合。MEDIUM。
  unsigned __int8 unknown_184[752];
  void *angleGuidePane;                 ///< IDA-gpt-6.1-sol-F004 / 0x32592CのBuild/FindPaneとrom_lgt資源で照合。MEDIUM。
};

// type: uint16_t
typedef unsigned __int16 uint16_t;

// type: u16
typedef uint16_t u16;

// type: uint8_t
typedef unsigned __int8 uint8_t;

// type: u8
typedef uint8_t u8;

// type: CodeSetHeader
struct CodeSetHeader
{
  u8 name[8];
  u16 version;
  u16 padding[3];
  u32 text_addr;
  u32 text_size;
  u32 ro_addr;
  u32 ro_size;
  u32 rw_addr;
  u32 rw_size;
  u32 text_size_total;
  u32 ro_size_total;
  u32 rw_size_total;
  u32 padding2;
  u64 program_id;
};

// type: CpuRegisters
struct CpuRegisters
{
  u32 r[13];
  u32 sp;
  u32 lr;
  u32 pc;
  u32 cpsr;
};

// type: DebugEventType
enum DebugEventType
{
  DBGEVENT_ATTACH_PROCESS = 0x0,
  DBGEVENT_ATTACH_THREAD = 0x1,
  DBGEVENT_EXIT_THREAD = 0x2,
  DBGEVENT_EXIT_PROCESS = 0x3,
  DBGEVENT_EXCEPTION = 0x4,
  DBGEVENT_DLL_LOAD = 0x5,
  DBGEVENT_DLL_UNLOAD = 0x6,
  DBGEVENT_SCHEDULE_IN = 0x7,
  DBGEVENT_SCHEDULE_OUT = 0x8,
  DBGEVENT_SYSCALL_IN = 0x9,
  DBGEVENT_SYSCALL_OUT = 0xA,
  DBGEVENT_OUTPUT_STRING = 0xB,
  DBGEVENT_MAP = 0xC,
};

// type: int32_t
typedef int int32_t;

// type: s32
typedef int32_t s32;

// type: DebuggerBreakExceptionEvent
struct DebuggerBreakExceptionEvent
{
  s32 thread_ids[4];
};

// type: ExceptionEventType
enum ExceptionEventType
{
  EXCEVENT_UNDEFINED_INSTRUCTION = 0x0,
  EXCEVENT_PREFETCH_ABORT = 0x1,
  EXCEVENT_DATA_ABORT = 0x2,
  EXCEVENT_UNALIGNED_DATA_ACCESS = 0x3,
  EXCEVENT_ATTACH_BREAK = 0x4,
  EXCEVENT_STOP_POINT = 0x5,
  EXCEVENT_USER_BREAK = 0x6,
  EXCEVENT_DEBUGGER_BREAK = 0x7,
  EXCEVENT_UNDEFINED_SYSCALL = 0x8,
};

// type: FaultExceptionEvent
struct FaultExceptionEvent
{
  u32 fault_information;
};

// type: StopPointType
enum StopPointType
{
  STOPPOINT_SVC_FF = 0x0,
  STOPPOINT_BREAKPOINT = 0x1,
  STOPPOINT_WATCHPOINT = 0x2,
};

// type: StopPointExceptionEvent
struct StopPointExceptionEvent
{
  StopPointType type;
  u32 fault_information;
};

// type: UserBreakType
enum UserBreakType
{
  USERBREAK_PANIC = 0x0,
  USERBREAK_ASSERT = 0x1,
  USERBREAK_USER = 0x2,
  USERBREAK_LOAD_RO = 0x3,
  USERBREAK_UNLOAD_RO = 0x4,
};

// type: UserBreakExceptionEvent
struct UserBreakExceptionEvent
{
  UserBreakType type;
  u32 croInfo;
  u32 croInfoSize;
};

// type: ExceptionEvent
struct ExceptionEvent
{
  ExceptionEventType type;
  u32 address;
  union
  {
    FaultExceptionEvent fault;
    StopPointExceptionEvent stop_point;
    UserBreakExceptionEvent user_break;
    DebuggerBreakExceptionEvent debugger_break;
  };
};

// type: ExitProcessEventReason
enum ExitProcessEventReason
{
  EXITPROCESS_EVENT_EXIT = 0x0,
  EXITPROCESS_EVENT_TERMINATE = 0x1,
  EXITPROCESS_EVENT_DEBUG_TERMINATE = 0x2,
};

// type: ExitProcessEvent
struct ExitProcessEvent
{
  ExitProcessEventReason reason;
};

// type: ExitThreadEventReason
enum ExitThreadEventReason
{
  EXITTHREAD_EVENT_EXIT = 0x0,
  EXITTHREAD_EVENT_TERMINATE = 0x1,
  EXITTHREAD_EVENT_EXIT_PROCESS = 0x2,
  EXITTHREAD_EVENT_TERMINATE_PROCESS = 0x3,
};

// type: ExitThreadEvent
struct ExitThreadEvent
{
  ExitThreadEventReason reason;
};

// type: MemPerm
enum MemPerm
{
  MEMPERM_READ = 0x1,
  MEMPERM_WRITE = 0x2,
  MEMPERM_EXECUTE = 0x4,
  MEMPERM_READWRITE = 0x3,
  MEMPERM_READEXECUTE = 0x5,
  MEMPERM_DONTCARE = 0x10000000,
};

// type: MemState
enum MemState
{
  MEMSTATE_FREE = 0x0,
  MEMSTATE_RESERVED = 0x1,
  MEMSTATE_IO = 0x2,
  MEMSTATE_STATIC = 0x3,
  MEMSTATE_CODE = 0x4,
  MEMSTATE_PRIVATE = 0x5,
  MEMSTATE_SHARED = 0x6,
  MEMSTATE_CONTINUOUS = 0x7,
  MEMSTATE_ALIASED = 0x8,
  MEMSTATE_ALIAS = 0x9,
  MEMSTATE_ALIASCODE = 0xA,
  MEMSTATE_LOCKED = 0xB,
};

// type: MapEvent
struct MapEvent
{
  u32 mapped_addr;
  u32 mapped_size;
  MemPerm memperm;
  MemState memstate;
};

// type: OutputStringEvent
struct OutputStringEvent
{
  u32 string_addr;
  u32 string_size;
};

// type: ScheduleInOutEvent
struct ScheduleInOutEvent
{
  u64 clock_tick;
};

// type: SyscallInOutEvent
struct SyscallInOutEvent
{
  u64 clock_tick;
  u32 syscall;
};

// type: DebugEventInfo
struct DebugEventInfo
{
  DebugEventType type;
  u32 thread_id;
  u32 flags;
  u8 remnants[4];
  union
  {
    AttachProcessEvent attach_process;
    AttachThreadEvent attach_thread;
    ExitThreadEvent exit_thread;
    ExitProcessEvent exit_process;
    ExceptionEvent exception;
    ScheduleInOutEvent scheduler;
    SyscallInOutEvent syscall;
    OutputStringEvent output_string;
    MapEvent map;
  };
};

// type: DebugFlags
enum DebugFlags
{
  DBG_INHIBIT_USER_CPU_EXCEPTION_HANDLERS = 0x1,
  DBG_SIGNAL_FAULT_EXCEPTION_EVENTS = 0x2,
  DBG_SIGNAL_SCHEDULE_EVENTS = 0x4,
  DBG_SIGNAL_SYSCALL_EVENTS = 0x8,
  DBG_SIGNAL_MAP_EVENTS = 0x10,
};

// type: DebugThreadParameter
enum DebugThreadParameter
{
  DBGTHREAD_PARAMETER_PRIORITY = 0x0,
  DBGTHREAD_PARAMETER_SCHEDULING_MASK_LOW = 0x1,
  DBGTHREAD_PARAMETER_CPU_IDEAL = 0x2,
  DBGTHREAD_PARAMETER_CPU_CREATOR = 0x3,
};

// type: DigRecord
#pragma pack(push, 2)
struct DigRecord
{
  struct ItemID item0;
  struct ItemID item1;
  struct ItemID item2;
  unsigned __int8 flags;
  unsigned __int8 playerIdx;
  unsigned __int8 wX;
  unsigned __int8 wY;
  unsigned __int8 actionID;
  unsigned __int8 state;
  unsigned __int8 pad[3];
  unsigned __int8 pNo;
};
#pragma pack(pop)

// type: int16_t
typedef __int16 int16_t;

// type: s16
typedef int16_t s16;

// type: int8_t
typedef char int8_t;

// type: s8
typedef int8_t s8;

// type: DmaDeviceConfig
struct DmaDeviceConfig
{
  s8 deviceId;
  s8 allowedAlignments;
  s16 burstSize;
  s16 transferSize;
  s16 burstStride;
  s16 transferStride;
};

// type: DmaConfig
struct DmaConfig
{
  s8 channelId;
  s8 endianSwapSize;
  u8 flags;
  u8 _padding;
  DmaDeviceConfig srcCfg;
  DmaDeviceConfig dstCfg;
};

// type: DropData
#pragma pack(push, 2)
struct DropData
{
  struct ItemID ItemToReplace;
  struct ItemID ItemToPlace;
  struct ItemID ItemToShow;
  unsigned __int8 wX;
  unsigned __int8 wY;
  unsigned __int8 DropType;
  unsigned __int8 State;
  unsigned __int8 Slot;
  unsigned __int8 Flags;
};
#pragma pack(pop)

// type: DropFlags
enum __bitmask DropFlags
{
  DROPFLAG_IsInside = 0x1,
  DROPFLAG_PlayerSide = 0x2,
  DROPFLAG_FruitTree_MASK = 0x1C,
  DROPFLAG_CrashTree = 0x20,
  DROPFLAG_HitCount_MASK = 0xC0,
};

// type: ERRF_ErrType
enum ERRF_ErrType : unsigned __int8
{
  ERRF_ERRTYPE_GENERIC = 0x0,
  ERRF_ERRTYPE_NAND_DAMAGED = 0x1,
  ERRF_ERRTYPE_CARD_REMOVED = 0x2,
  ERRF_ERRTYPE_EXCEPTION = 0x3,
  ERRF_ERRTYPE_FAILURE = 0x4,
  ERRF_ERRTYPE_LOG_ONLY = 0x5,
};

// type: ERRF_ExceptionType
enum ERRF_ExceptionType
{
  ERRF_EXCEPTION_PREFETCH_ABORT = 0x0,
  ERRF_EXCEPTION_DATA_ABORT = 0x1,
  ERRF_EXCEPTION_UNDEFINED = 0x2,
  ERRF_EXCEPTION_VFP = 0x3,
};

// type: ERRF_ExceptionInfo
struct ERRF_ExceptionInfo
{
  ERRF_ExceptionType type;
  u8 reserved[3];
  u32 fsr;
  unsigned int __unnamed_1;
  u32 fpexc;
  u32 fpinst;
  u32 fpinst2;
};

// type: ERRF_ExceptionData
struct ERRF_ExceptionData
{
  ERRF_ExceptionInfo excep;
  CpuRegisters regs;
};

// type: ERRF_FatalErrInfo
struct ERRF_FatalErrInfo
{
  ERRF_ErrType type;
  u8 revHigh;
  u16 revLow;
  u32 resCode;
  u32 pcAddr;
  u32 procId;
  u64 titleId;
  u64 appTitleId;
  union
  {
    ERRF_ExceptionData exception_data;
    char failure_mesg[96];
  } data;
};

// type: EventState
enum EventState
{
  CLEARED_STICKY = 0xFFFFFFFE,
  CLEARED_ONESHOT = 0xFFFFFFFF,
  SIGNALED_ONESHOT = 0x0,
  SIGNALED_STICKY = 0x1,
};

// type: FS_ProgramInfo
struct FS_ProgramInfo
{
  u64 titleId;
  u8 mediaType;
  u8 _padding[7];
};

// type: FaderBase
#pragma pack(push, 2)
struct FaderBase
{
  void **vtbl;
  unsigned __int8 screen;
  unsigned __int8 state;
  unsigned __int8 doneFlags;
  unsigned __int8 pad;
  int duration;
  int counter;
};
#pragma pack(pop)

// type: FaderKind
enum FaderKind
{
  FADERKIND_Wipe = 0x0,
  FADERKIND_ColorBlack = 0x1,
  FADERKIND_Moment = 0x2,
  FADERKIND_ColorWhite = 0x4,
  FADERKIND_ColorWhite2 = 0x5,
};

// type: FallActorKind
enum FallActorKind
{
  FALLKIND_Shake = 0x0,
  FALLKIND_ShakeStrong = 0x2,
  FALLKIND_Fall = 0x4,
  FALLKIND_FallReverse = 0x5,
};

// type: FieldActionActive
#pragma pack(push, 2)
struct FieldActionActive
{
  unsigned __int8 wX;
  unsigned __int8 wY;
  unsigned __int8 playerNo;
  unsigned __int8 flags;
  unsigned __int8 actionID;
};
#pragma pack(pop)

// type: FieldObjCategory
enum FieldObjCategory
{
  CAT_Hole = 0x0,
  CAT_Tree = 0x4,
  CAT_Bamboo = 0x8,
  CAT_Rock = 0xA,
  CAT_Plant_11 = 0xB,
  CAT_Plant_12 = 0xC,
  CAT_Plant_13 = 0xD,
  CAT_Rose_14 = 0xE,
  CAT_Plant_15 = 0xF,
  CAT_Plant_16 = 0x10,
  CAT_Plant_17 = 0x11,
  CAT_Plant_19 = 0x13,
  CAT_Plant_20 = 0x14,
  CAT_Plant_27 = 0x1B,
  CAT_Plant_28 = 0x1C,
  CAT_NotFieldObj = 0x1D,
};

// type: FieldObjDef
#pragma pack(push, 2)
struct FieldObjDef
{
  unsigned __int16 unk00;
  unsigned __int8 unk02[8];
  unsigned __int8 category;
  unsigned __int8 unk0B;
  unsigned __int8 unk0C;
  __int8 growStages;
  unsigned __int8 unk0E[2];
};
#pragma pack(pop)

// type: FieldObjItemId
enum FieldObjItemId
{
  ITEM_CedarStump = 0x14,
  ITEM_CutBamboo = 0x21,
  ITEM_Cedar = 0x2B,
  ITEM_Bamboo = 0x39,
  ITEM_Hole = 0x9E,
  ITEM_FlowerFirst = 0x9F,
  ITEM_RedRoses = 0xB2,
  ITEM_GoldRoses = 0xBA,
  ITEM_JacobsLadder = 0xC8,
  ITEM_LuckyClover = 0xC9,
  ITEM_Dandelion = 0xCA,
  ITEM_CloverWeed = 0xCC,
  ITEM_Rafflesia = 0xCD,
  ITEM_WiltedFirst = 0xCE,
  ITEM_FlowerLast = 0xF7,
  ITEM_BrokenRedFlower = 0xFA,
  ITEM_Empty = 0x7FFE,
};

// type: FpuRegisters
struct FpuRegisters
{
  union
  {
    float s[32];
  };
  u32 fpscr;
  u32 fpexc;
};

// type: FurnitureFootprintDescriptorPrefix_F016
#pragma pack(push, 2)
struct FurnitureFootprintDescriptorPrefix_F016
{
  const int (*rotations[4])[2];
  unsigned __int8 cellCount;
  unsigned __int8 unknown11[3];
};
#pragma pack(pop)

// type: GohanItemActionPmf8
#pragma pack(push, 2)
struct GohanItemActionPmf8
{
  int (*method)(void *actor);
  int encodedThisAdjustment;
};
#pragma pack(pop)

// type: GohanNativeDate
#pragma pack(push, 2)
struct GohanNativeDate
{
  int year;
  unsigned __int8 month;
  unsigned __int8 day;
  unsigned __int8 weekday;
  unsigned __int8 hour;
  unsigned __int8 minute;
  unsigned __int8 second;
  unsigned __int16 millis;
};
#pragma pack(pop)

// type: GohanPocketAction
enum GohanPocketAction
{
  GohanPocketAction_Place = 0x0,
  GohanPocketAction_Release = 0xF,
  GohanPocketAction_Eat = 0x10,
  GohanPocketAction_Cancel = 0x29,
  GohanPocketAction_Wall = 0x2A,
};

// type: Handle
typedef u32 Handle;

// type: IPCStaticBuffer
struct IPCStaticBuffer
{
  u32 descriptor;
  void *p;
};

// type: IslandRuntimeBuilding
#pragma pack(push, 2)
struct __attribute__((packed)) IslandRuntimeBuilding
{
  unsigned __int16 id;
  unsigned __int8 x;
  unsigned __int8 z;
};
#pragma pack(pop)

// type: IslandRuntimeItem
#pragma pack(push, 2)
struct __attribute__((packed)) IslandRuntimeItem
{
  unsigned __int16 id;
  unsigned __int16 flags;
};
#pragma pack(pop)

// type: IslandRuntimeData
#pragma pack(push, 2)
struct __attribute__((packed)) IslandRuntimeData
{
  unsigned __int8 unknown_header[2];
  unsigned __int16 acres[4][4];
  struct IslandRuntimeItem items[4][256];
  struct IslandRuntimeBuilding buildings[2];
};
#pragma pack(pop)

// type: ItemCategory
enum ItemCategory
{
  ITEM_CATEGORY_CLOTH = 0x6,
  ITEM_CATEGORY_DRESS = 0x7,
  ITEM_CATEGORY_MUSIC_JACKET = 0x2F,
  ITEM_CATEGORY_MUSIC_JACKET_WALL = 0x31,
  ITEM_CATEGORY_MUSIC_ORGEL = 0x32,
  ITEM_CATEGORY_CLOTH_WALL = 0x93,
  ITEM_CATEGORY_DRESS_WALL = 0x94,
};

// type: ItemCategoryRangeEntry
#pragma pack(push, 2)
struct ItemCategoryRangeEntry
{
  unsigned __int16 firstId;
  unsigned __int16 lastIdInclusive;
  unsigned int count;
  const char *name;
};
#pragma pack(pop)

// type: LetterDragWindowAttachmentPrefix_F014
#pragma pack(push, 2)
struct LetterDragWindowAttachmentPrefix_F014
{
  unsigned __int8 beforeRoot[632];
  void *rootPane;
  unsigned __int8 betweenRootAndParent[340];
  void *parentPane;
};
#pragma pack(pop)

// type: LightLock
typedef u32 LightLock;

// type: LightEvent
struct LightEvent
{
  EventState state;
  LightLock lock;
};

// type: LightSemaphore
struct LightSemaphore
{
  s32 current_count;
  s16 num_threads_acq;
  s16 max_count;
};

// type: MapExFlags
enum MapExFlags
{
  MAPEXFLAGS_PRIVATE = 0x1,
};

// type: MemInfo
struct MemInfo
{
  u32 base;
  u32 size;
  MemPerm perm;
  MemState state;
};

// type: MemOp
enum MemOp
{
  MEMOP_FREE = 0x1,
  MEMOP_RESERVE = 0x2,
  MEMOP_ALLOC = 0x3,
  MEMOP_MAP = 0x4,
  MEMOP_UNMAP = 0x5,
  MEMOP_PROT = 0x6,
  MEMOP_REGION_APP = 0x100,
  MEMOP_REGION_SYSTEM = 0x200,
  MEMOP_REGION_BASE = 0x300,
  MEMOP_OP_MASK = 0xFF,
  MEMOP_REGION_MASK = 0xF00,
  MEMOP_LINEAR_FLAG = 0x10000,
  MEMOP_ALLOC_LINEAR = 0x10003,
};

// type: MsgStreamCode
enum MsgStreamCode
{
  MSGCODE_Ruby = 0xE,
  MSGCODE_Type15 = 0xF,
};

// type: NwlytDrawInfoCalcFlags_F014
enum NwlytDrawInfoCalcFlags_F014
{
  NwlytDrawInfoCalcFlags_ForceHiddenMatrices = 0x4,
};

// type: NwlytPaneDrawPrefix_F015
#pragma pack(push, 2)
struct NwlytPaneDrawPrefix_F015
{
  void *vtable;
  unsigned int nextSiblingLink;
  unsigned int previousSiblingLink;
  NwlytPaneDrawPrefix_F015 *parent;
  unsigned __int8 gap_10[4];
  unsigned int firstChildLink;
  unsigned int lastChildLink;
  unsigned __int8 gap_1C[152];
  unsigned __int8 localAlpha;
  unsigned __int8 globalAlpha;
  unsigned __int8 gap_B6;
  unsigned __int8 drawFlags;
};
#pragma pack(pop)

// type: NwlytLayoutDrawPrefix_F015
#pragma pack(push, 2)
struct NwlytLayoutDrawPrefix_F015
{
  unsigned __int8 gap_00[16];
  NwlytPaneDrawPrefix_F015 *rootPane;
};
#pragma pack(pop)

// type: NwlytTrigRecord_F015
#pragma pack(push, 2)
struct NwlytTrigRecord_F015
{
  float sine;
  float cosine;
  float sineDelta;
  float cosineDelta;
};
#pragma pack(pop)

// type: PV
typedef void *PV;

// type: PageInfo
struct PageInfo
{
  u32 flags;
};

// type: PerfCounterOperation
enum PerfCounterOperation
{
  PERFCOUNTEROP_ENABLE = 0x0,
  PERFCOUNTEROP_DISABLE = 0x1,
  PERFCOUNTEROP_GET_VALUE = 0x2,
  PERFCOUNTEROP_SET_VALUE = 0x3,
  PERFCOUNTEROP_GET_OVERFLOW_FLAGS = 0x4,
  PERFCOUNTEROP_RESET = 0x5,
  PERFCOUNTEROP_GET_EVENT = 0x6,
  PERFCOUNTEROP_SET_EVENT = 0x7,
  PERFCOUNTEROP_SET_VIRTUAL_COUNTER_ENABLED = 0x8,
};

// type: PlayerC4ArgumentBlock
#pragma pack(push, 2)
struct __attribute__((packed)) PlayerC4ArgumentBlock
{
  unsigned __int16 motion_id;
  int sound_id;
  unsigned __int8 sound_marker_frame;
  __int16 duration_frames;
  unsigned __int8 exit_state;
  unsigned __int8 unknown_0A;
  unsigned __int8 unknown_0B;
};
#pragma pack(pop)

// type: PlayerC5ArgumentBlock
#pragma pack(push, 2)
struct PlayerC5ArgumentBlock
{
  unsigned __int16 initial_motion_id;
  unsigned __int16 repeat_motion_id;
  unsigned __int8 unknown_04;
  unsigned __int8 repeat_count_limit;
  unsigned __int8 unknown_06;
  unsigned __int8 unknown_07;
};
#pragma pack(pop)

// type: PlayerStateContextPrefix
#pragma pack(push, 2)
struct PlayerStateContextPrefix
{
  unsigned __int8 unknown_000[424];
  unsigned __int8 unknown_state_1a8;
  unsigned __int8 current_state;
  unsigned __int8 previous_state;
  unsigned __int8 resume_state;
  unsigned __int8 player_index;
};
#pragma pack(pop)

// type: ProcessOp
enum ProcessOp
{
  PROCESSOP_GET_ALL_HANDLES = 0x0,
  PROCESSOP_SET_MMU_TO_RWX = 0x1,
  PROCESSOP_GET_ON_MEMORY_CHANGE_EVENT = 0x2,
  PROCESSOP_SIGNAL_ON_EXIT = 0x3,
  PROCESSOP_GET_PA_FROM_VA = 0x4,
  PROCESSOP_SCHEDULE_THREADS = 0x5,
};

// type: PseudoHandles
enum PseudoHandles
{
  CUR_THREAD_HANDLE = 0xFFFF8000,
  CUR_PROCESS_HANDLE = 0xFFFF8001,
};

// type: RecursiveLock
struct RecursiveLock
{
  LightLock *lock;
  u32 thread_tag;
  u32 counter;
};

// type: ResetType
enum ResetType
{
  RESET_ONESHOT = 0x0,
  RESET_STICKY = 0x1,
  RESET_PULSE = 0x2,
};

// type: ResourceLimitType
enum ResourceLimitType
{
  RESLIMIT_PRIORITY = 0x0,
  RESLIMIT_COMMIT = 0x1,
  RESLIMIT_THREAD = 0x2,
  RESLIMIT_EVENT = 0x3,
  RESLIMIT_MUTEX = 0x4,
  RESLIMIT_SEMAPHORE = 0x5,
  RESLIMIT_TIMER = 0x6,
  RESLIMIT_SHAREDMEMORY = 0x7,
  RESLIMIT_ADDRESSARBITER = 0x8,
  RESLIMIT_CPUTIME = 0x9,
};

// type: Result
enum Result
{
  SUCCESS = 0x0,
  GSP_ALREADY_DONE = 0x2BEB,
  OS_ALREADY_INITIALIZED = 0x8A01BF9,
  SRV_ALREADY_INITIALIZED = 0x8A067F9,
  GSP_BUSY = 0xC8402BF0,
  APT_ALREADY_EXISTS = 0xC8A0CFFC,
  APT_NO_DATA = 0xC8A0CFEF,
  OS_SESSION_CLOSED = 0xC920181A,
  OS_WOULD_BLOCK = 0xD0401834,
  GSP_PERMANENT = 0xD8202A06,
  OS_OUT_OF_MEM = 0xD8601837,
  GSP_INVALID_STATE_516 = 0xD8A02A04,
  GSP_INVALID_STATE_517 = 0xD8A02A05,
  SRV_NOT_INITIALIZED = 0xD8A067F8,
  CFG_INVALID_HANDLE = 0xD8A103F7,
  CFG_ALREADY_INITIALIZED = 0xD8A103F9,
  SVC_QUERY_FAILED = 0xD8A12C08,
  OS_INVALID_COMMAND_HEADER = 0xD900182F,
  OS_WRONG_ARGUMENT_48 = 0xD9001830,
  OS_WRONG_ARGUMENT_49 = 0xD9001831,
  SRV_INVALID_STRING_LENGTH = 0xD9006405,
  SVC_TOO_BIG_ADDR = 0xD9012FF1,
  SVC_TOO_BIG_SIZE = 0xD9012FF2,
  CFG_CANCELLED = 0xD92103FB,
  HID_ALREADY_INITIALIZED = 0xE0A04FF9,
  APT_NOT_INITIALIZED = 0xE0A0CFF8,
  APT_ALREADY_INITIALIZED = 0xE0A0CFF9,
  SVC_ALREADY_INIT = 0xE0A12FF9,
  GSP_NOT_IMPLEMENTED = 0xE0C02BF4,
  SVC_ALIGN_ADDR = 0xE0E01BF1,
  SVC_INVALID_SIZE = 0xE0E01BF2,
  SVC_INVALID_PARAMS = 0xE0E01BF5,
  SVC_INVALID_OPERATION = 0xE0E01BEE,
  GSP_INVALID_ARGUMENT = 0xE0E02A01,
  GSP_INVALID_SELECTION = 0xE0E02BE8,
  GSP_INVALID_SIZE = 0xE0E02BEC,
  GSP_MISALIGNED_SIZE = 0xE0E02BF2,
  GSP_INVALID_ADDRESS = 0xE0E02BF5,
  SVC_INVALID_HANDLE = 0xE1612FF7,
};

// type: RoomCameraDpadMask
enum RoomCameraDpadMask
{
  ROOM_CAMERA_UP = 0x10000,
  ROOM_CAMERA_DOWN = 0x20000,
  ROOM_CAMERA_LEFT = 0x40000,
  ROOM_CAMERA_RIGHT = 0x80000,
};

// type: RoomCameraInterpolation16
#pragma pack(push, 2)
struct RoomCameraInterpolation16
{
  float parameter0;
  float duration;
  float parameter2;
  float parameter3;
};
#pragma pack(pop)

// type: RoomCameraModeEntry16
#pragma pack(push, 2)
struct RoomCameraModeEntry16
{
  RoomCameraPmf8 enter;
  RoomCameraPmf8 calc;
};
#pragma pack(pop)

// type: RoomCameraProfile20
#pragma pack(push, 2)
struct RoomCameraProfile20
{
  float x;
  float y;
  float z;
  float distance;
  unsigned __int16 polar;
  unsigned __int16 yaw;
};
#pragma pack(pop)

// type: RoomFlags
enum __bitmask RoomFlags
{
  ROOMFLAG_Outdoor1 = 0x2,
  ROOMFLAG_Outdoor2 = 0x4,
  ROOMFLAG_Indoor = 0x8,
  ROOMFLAG_Town = 0x20,
};

// type: RoomTransitionKindPair
#pragma pack(push, 2)
struct RoomTransitionKindPair
{
  unsigned __int16 requested_kind;
  unsigned __int16 current_kind;
};
#pragma pack(pop)

// type: ServiceOp
enum ServiceOp
{
  SERVICEOP_STEAL_CLIENT_SESSION = 0x0,
  SERVICEOP_GET_NAME = 0x1,
};

// type: SvcResult32
struct SvcResult32
{
  Result result;
  u32 value;
};

// type: int64_t
typedef __int64 int64_t;

// type: s64
typedef int64_t s64;

// type: SvcResult64
#pragma pack(push, 1)
struct SvcResult64
{
  Result result;
  s64 value;
};
#pragma pack(pop)

// type: SvcResult8
struct SvcResult8
{
  Result result;
  u8 value;
};

// type: SvcResultGetDebugThreadParam
struct SvcResultGetDebugThreadParam
{
  Result result;
  s64 unused;
  u32 out;
};

// type: SvcResultHandle
struct SvcResultHandle
{
  Result result;
  Handle handle;
};

// type: SvcResultHandlePair
struct SvcResultHandlePair
{
  Result result;
  Handle handle1;
  Handle handle2;
};

// type: SvcResultQueryMemory
struct SvcResultQueryMemory
{
  Result result;
  MemInfo mem_info;
  PageInfo page_info;
};

// type: T022_GraphicMemoryMgrPrefix
struct T022_GraphicMemoryMgrPrefix
{
  void *vtable;
  unsigned int reserved04;
  void *defaultFcramHeap;
  void *rootVramA;
  void *rootVramB;
  void *commandHeap;
  void *vramAHeap;
  void *vramBHeap;
};

// type: T022_HouseSaveExteriorPrefix
#pragma pack(push, 2)
struct T022_HouseSaveExteriorPrefix
{
  unsigned int unknown_00;
  unsigned __int8 currentExteriorKind;
  unsigned __int8 currentExteriorProperties[8];
  unsigned __int8 plannedExteriorKind;
  unsigned __int8 plannedExteriorProperties[8];
  unsigned __int8 unknown_16[2];
};
#pragma pack(pop)

// type: T022_ModelHolderPrefix
#pragma pack(push, 2)
struct T022_ModelHolderPrefix
{
  unsigned int vtable;
  unsigned int node;
};
#pragma pack(pop)

// type: T022_RoomWallPartPrefix
#pragma pack(push, 2)
struct T022_RoomWallPartPrefix
{
  unsigned __int8 unknown0[12];
  T022_ModelHolderPrefix model;
  unsigned __int8 unknown1[44];
};
#pragma pack(pop)

// type: T022_RoomViewSurfacePrefix
#pragma pack(push, 2)
struct T022_RoomViewSurfacePrefix
{
  unsigned int vtable;
  unsigned __int8 unknown0[14384];
  T022_ModelHolderPrefix floorModel;
  unsigned __int8 unknown1[672];
  T022_RoomWallPartPrefix wallParts[4];
};
#pragma pack(pop)

// type: cxxabi_class_type_info
struct cxxabi_class_type_info
{
  void *vptr;
  char *name;
};

// type: TI_C
typedef struct cxxabi_class_type_info TI_C;

// type: cxxabi_si_class_type_info
struct cxxabi_si_class_type_info
{
  void *vptr;
  char *name;
  void *base;
};

// type: TI_S
typedef struct cxxabi_si_class_type_info TI_S;

// type: cxxabi_vmi_class_type_info
struct cxxabi_vmi_class_type_info
{
  void *vptr;
  char *name;
  unsigned int flags;
  unsigned int base_count;
};

// type: TI_V
typedef struct cxxabi_vmi_class_type_info TI_V;

// type: TLS
struct TLS
{
  u32 userStorage[16];
  u32 exHandler;
  u32 exHandlerSPCtl;
  u32 exHandlerCtxCtl;
  u32 _reserved[13];
  u32 commandBuffer[64];
  IPCStaticBuffer staticBuffers[16];
};

// type: TextInputConstraintFlags
enum __bitmask TextInputConstraintFlags
{
  TextInputConstraint_FilterNumericCharacters = 0x1,
  TextInputConstraint_CheckNumericCountOnSubmit = 0x20,
};

// type: ThreadContext
struct ThreadContext
{
  CpuRegisters cpu_registers;
  FpuRegisters fpu_registers;
};

// type: ThreadContextControlFlags
enum ThreadContextControlFlags
{
  THREADCONTEXT_CONTROL_CPU_GPRS = 0x1,
  THREADCONTEXT_CONTROL_CPU_SPRS = 0x2,
  THREADCONTEXT_CONTROL_CPU_REGS = 0x3,
  THREADCONTEXT_CONTROL_FPU_GPRS = 0x4,
  THREADCONTEXT_CONTROL_FPU_SPRS = 0x8,
  THREADCONTEXT_CONTROL_FPU_REGS = 0xC,
  THREADCONTEXT_CONTROL_ALL = 0xF,
};

// type: TiledByteGridPrefix
#pragma pack(push, 2)
struct TiledByteGridPrefix
{
  unsigned __int8 *data;
  unsigned int width;
  unsigned int height;
};
#pragma pack(pop)

// type: UiAnim
#pragma pack(push, 2)
struct UiAnim
{
  void *res;
  float totalFrames;
  float curTime;
  float prevTime;
  float rate;
  unsigned __int8 flags;
  unsigned __int8 pad[3];
  void *sub;
};
#pragma pack(pop)

// type: WeatherParticleSlot
#pragma pack(push, 2)
struct WeatherParticleSlot
{
  float world_position[3];
  unsigned __int8 unknown_0c[44];
};
#pragma pack(pop)

// type: WeatherParticleGroupPrefix
#pragma pack(push, 2)
struct WeatherParticleGroupPrefix
{
  unsigned __int8 unknown_000[300];
  struct WeatherParticleSlot particles[400];
  unsigned int active_count;
  unsigned int update_frame;
};
#pragma pack(pop)

// type: __n128
union __attribute__((aligned(8))) __n128
{
  unsigned __int64 n128_u64[2];
  unsigned __int32 n128_u32[4];
  unsigned __int16 n128_u16[8];
  unsigned __int8 n128_u8[16];
  __int64 n128_i64[2];
  __int32 n128_i32[4];
  __int16 n128_i16[8];
  __int8 n128_i8[16];
  float n128_f32[4];
  double n128_f64[2];
};

// type: __n64
union __attribute__((aligned(8))) __n64
{
  unsigned __int64 n64_u64[1];
  unsigned __int32 n64_u32[2];
  unsigned __int16 n64_u16[4];
  unsigned __int8 n64_u8[8];
  __int64 n64_i64[1];
  __int32 n64_i32[2];
  __int16 n64_i16[4];
  __int8 n64_i8[8];
  float n64_f32[2];
  double n64_f64[1];
};

// type: float16x4_t
typedef __n64 float16x4_t;

// type: float16x2_t
typedef float16x4_t float16x2_t;

// type: float16x8_t
typedef __n128 float16x8_t;

// type: float32x2_t
typedef __n64 float32x2_t;

// type: float32x4_t
typedef __n128 float32x4_t;

// type: float64x2_t
typedef __n128 float64x2_t;

// type: int16x4_t
typedef __n64 int16x4_t;

// type: int16x2_t
typedef int16x4_t int16x2_t;

// type: int16x8_t
typedef __n128 int16x8_t;

// type: int32x2_t
typedef __n64 int32x2_t;

// type: int32x4_t
typedef __n128 int32x4_t;

// type: int64x2_t
typedef __n128 int64x2_t;

// type: int8x16_t
typedef __n128 int8x16_t;

// type: int8x8_t
typedef __n64 int8x8_t;

// type: intptr_t
typedef int intptr_t;

// type: poly128_t
typedef __n128 poly128_t;

// type: poly16x4_t
typedef __n64 poly16x4_t;

// type: poly16x8_t
typedef __n128 poly16x8_t;

// type: poly8x16_t
typedef __n128 poly8x16_t;

// type: poly8x8_t
typedef __n64 poly8x8_t;

// type: size_t
typedef unsigned int size_t;

// type: svbool_t
struct svbool_t
{
  unsigned __int8 body[1];
};

// type: svfloat16_t
struct svfloat16_t
{
  short float body[1];
};

// type: svfloat32_t
struct svfloat32_t
{
  float body[1];
};

// type: svfloat64_t
struct svfloat64_t
{
  double body[1];
};

// type: svint16_t
struct svint16_t
{
  __int16 body[1];
};

// type: svint32_t
struct svint32_t
{
  __int32 body[1];
};

// type: svint64_t
struct svint64_t
{
  __int64 body[1];
};

// type: svint8_t
struct svint8_t
{
  __int8 body[1];
};

// type: svuint16_t
struct svuint16_t
{
  unsigned __int16 body[1];
};

// type: svuint32_t
struct svuint32_t
{
  unsigned __int32 body[1];
};

// type: svuint64_t
struct svuint64_t
{
  unsigned __int64 body[1];
};

// type: svuint8_t
struct svuint8_t
{
  unsigned __int8 body[1];
};

// type: uint16x4_t
typedef __n64 uint16x4_t;

// type: uint16x2_t
typedef uint16x4_t uint16x2_t;

// type: uint16x8_t
typedef __n128 uint16x8_t;

// type: uint32x2_t
typedef __n64 uint32x2_t;

// type: uint32x4_t
typedef __n128 uint32x4_t;

// type: uint64x2_t
typedef __n128 uint64x2_t;

// type: uint8x16_t
typedef __n128 uint8x16_t;

// type: uint8x8_t
typedef __n64 uint8x8_t;

// type: uintptr_t
typedef unsigned int uintptr_t;

// type: va_list
typedef void **va_list;
