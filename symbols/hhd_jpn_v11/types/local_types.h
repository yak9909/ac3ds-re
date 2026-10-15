// ローカルの型（IDA の print_decls の出力を、名前順・依存順に並べた物）

struct HhdRoomCameraPrefix;
struct HhdRoomCameraSpline;
struct HhdRoomCameraSplinePoint;
struct RoomCameraInterpolation16;
struct RoomCameraModeEntry16;
struct RoomCameraPmf8;
struct RoomCameraProfile20;
union __n128;
union __n64;
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

// type: BOOL
typedef int BOOL;

// type: HhdRoomCameraSplinePoint
#pragma pack(push, 2)
struct HhdRoomCameraSplinePoint
{
  float x;
  float y;
  float z;
  float distance;
  int polar;
};
#pragma pack(pop)

// type: HhdRoomCameraSpline
#pragma pack(push, 2)
struct HhdRoomCameraSpline
{
  unsigned int pointCount;
  HhdRoomCameraSplinePoint *points;
  unsigned int constantCount;
  HhdRoomCameraSplinePoint *constant;
  unsigned int linearCount;
  HhdRoomCameraSplinePoint *linear;
  unsigned int quadraticCount;
  HhdRoomCameraSplinePoint *quadratic;
  unsigned int cubicCount;
  HhdRoomCameraSplinePoint *cubic;
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

// type: HhdRoomCameraPrefix
#pragma pack(push, 2)
struct HhdRoomCameraPrefix
{
  void *vtable;
  float base[3];
  float offset[3];
  unsigned __int16 polar;
  unsigned __int16 yaw;
  float distance;
  float fieldOfView;
  unsigned __int8 gap_28[238];
  unsigned __int8 mode;
  unsigned __int8 requestedMode;
  unsigned __int8 gap_118[36];
  float targetBase[3];
  float targetOffset[3];
  unsigned __int16 targetPolar;
  unsigned __int16 targetYaw;
  float targetDistance;
  float targetFov;
  unsigned __int8 gap_160[1];
  signed __int8 interpolationId;
  unsigned __int8 gap_162[6];
  const unsigned __int8 *roomSplineProfileIds;
  const unsigned __int8 *otherProfileIds;
  const unsigned __int8 *alternateProfileIds;
  unsigned __int8 gap_174[28];
  float transitionFrame;
  unsigned __int8 gap_194[47];
  unsigned __int8 inputBlocked;
  unsigned __int8 gap_1C4[2];
  unsigned __int8 controlsBlocked;
  unsigned __int8 gap_1C7[5];
  float yawVelocity;
  float zoomVelocity;
  float zoomPosition;
  float zoomMaximum;
  RoomCameraProfile20 continuousProfile;
  unsigned __int8 gap_1F0[12];
  HhdRoomCameraSpline *roomSpline;
  unsigned __int8 verticalHeld;
};
#pragma pack(pop)

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

// type: RoomCameraPmf8
#pragma pack(push, 2)
struct RoomCameraPmf8
{
  unsigned int functionOrOffset;
  signed int thisAdjustmentTag;
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

// type: va_list
typedef void **va_list;
