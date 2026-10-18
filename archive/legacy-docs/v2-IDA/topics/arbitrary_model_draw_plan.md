# 任意モデルの読み込み→描画 / IDA-opus-5-D001

2026-09-20、IDA / opus-5。**2026-09-20 に実機で成立した**（IDA-opus-5-F004。手順と実測は
[arbitrary_20260920/plan.md](../../work/evidence/models3d/arbitrary_20260920/plan.md)）。
以下の §0〜§4 は成立前に書いた設計で、実機結果はそれを支持している。§7 に確定後の差分を置く。
別エージェント（gpt-6-astra）の実機成功2件と、こちらの `UnitCursor` 不可視の失敗を突き合わせ、
「任意のbcresを読んで画面に出す」までの不足分を確定させる。用途・組み込み先は前提にしない。

## 0. 結論

**足場は2本とも既に在り、欠けていたのは「座標の空間」だった。**

| 半分 | 状態 | 出所 |
|---|---|---|
| 任意bcresの**読み込み**（heap→RequestLoad→Setup→FindModelByName→instance生成） | 実機で成功済み。資源・model・activator・両command list・頂点bufferまで確認 | `tools/hw/unitcursor_probe.py`（IDA-unknown-F025〜F029） |
| 生成したinstanceの**描画**（world / 画面固定） | 実機で成功済み。ただし**ゲームが既にロード済みのmodel**（`fg_treeA_4`）を借りている | `tools/models3d/tree_live.py` / `tree_screen.py`（IDA-gpt-6-astra-F001〜F003） |

**両者は同じ関数 `ModelInstance_Create 0x004F048C` で合流する。** 前者はその入力（`ResModel*`）を
任意のファイルから作り、後者はその出力（`node`）を実際に画面へ出した。
つなぐために新しく解析が要る箇所は無く、必要なのは下の3点の修正だけである。

1. **node行列をゲーム座標のまま作らない。** 屋外は `FieldPosition_ToRenderSpace 0x0052CDD8` を通す（§2）。
   こちらの失敗コードは生のプレイヤー座標をそのまま使っており（`tools/hw/unitcursor_hw.py:356`）、
   これは別エージェントが**実機で不可視を実証した配置そのもの**である。
2. **instance holderを `0x004ED008` で構築する**（§4.1）。こちらは16Bゼロ埋めのみで済ませていた。
3. **最初の1体は不透明・レイヤー0・1メッシュのModelを選ぶ**（§3）。`UnitCursor` は
   レイヤー1の加算合成で、描けていても切り分けに向かない。

## 1. 任意モデルは「2種類」しかない（IDA-opus-5-F001）

`ModelInstance_Create 0x004F048C` → `sub_48E350 0x0048E350` → `sub_736158 0x00736158` の
switchは**引数ではなく資源のtypeInfo語（ResModel+0）**で分岐する。呼び出し側からクラスは選べない。

| typeInfo | 生成器 | クラス（RTTI実名） | node vtable | romfs内の個数 |
|---|---|---|---|---|
| `0x40000012` | `nwgfx_Model_Create 0x004AB270` | `nw::gfx::Model` | `0x008FBD00` | **953** |
| `0x40000092` | `sub_49693C 0x0049693C` | `nw::gfx::SkeletalModel` | `0x008FB848` | **379** |

- クラス名はvtable−4のTypeInfo→+4のマングル名から読んだ（`N2nw3gfx5ModelE` / `N2nw3gfx13SkeletalModelE`）。
  switchの見た目からの推定ではない。TypeInfoの基底欄より **SkeletalModel は Model の派生**。
- 個数はbcres 1,907ファイルを**2経路**で数えて一致した（`CMDL`マジックの生走査と、
  CGFXモデル辞書の走査。`tools/models3d/model_preflight.py --survey`）。**この2値以外は1件も無い。**
- `fg_treeA_4` ＝ `0x40000012`（実機で描画成功）、`UnitCursor` ＝ `0x40000092`（不可視）。

→ **「任意モデル」は実質2ケース。うち72%を占めるModel側は既に実機で描けている。**

## 2. 屋外座標は曲がっている（IDA-opus-5-F002）

`FieldPosition_ToRenderSpace 0x0052CDD8` は `Room_GetCurrentId 0x002F75CC` →
`sub_5B40B4 0x005B40B4` で部屋を見て、

- **フラグ無し**: `out = in`（3語のコピー）。→ **屋内は変換不要。**
- **フラグ有り**: `CurvedWorld_TransformPosition 0x0075CAB4` を呼ぶ。→ **屋外は必須。**

ゲートは `g_RoomFlagTable[roomId] & 2`（`0x00883328`、4バイト間隔＝`LDR R0,[R2,R0,LSL#2]` で確認、
`roomId < 0xA5`）。**165部屋中37部屋が曲がっており、128部屋は平ら**（id 0・1 は曲がる側）。

変換そのもの（`0x0075CAB4`）は
`radius = in.y + coeff[0]` /
`angle = u16(trunc(f32(f32(coeff[1] * in.z) * 182.04444885253906)))` /
`out = (in.x, cos16(angle) * radius, sin16(angle) * radius)` で、平行移動ではない。
ゲームのsin/cos表を使わずPythonの三角関数で独立に再現し、捕獲点で一致した。

```
raw    (2158.788330078125, 112.0,               1114.8851318359375)
render (2158.788330078125, -318.4991760253906,   370.951416015625 )  ← 独立計算
実機                        -318.4910583496094,   370.9418640136719   ← 別エージェント捕獲
```

**y で約431、z で約744ずれる。** モデル尺0.5・木1本が高さ100程度の世界で、
生座標を渡した物体は画面外に置かれる。こちらの `UnitCursor` が
「全ての状態を正しくしたのに1画素も出ない」だった説明として、これが最有力である。

さらにnode行列は平行移動だけでなく**同じ角度のX回転**を含む（`tools/models3d/verify_curved_pose.py`）。

```
[ s,     0,       0,     x  ]
[ 0,  s*cos,  -s*sin,    y' ]
[ 0,  s*sin,   s*cos,    z' ]
```

こちらのコードは単位回転＋生座標だったので、**位置と姿勢の両方**が間違っていた。

## 3. 最初の1体の選び方

`tools/models3d/model_preflight.py <bcres> [model名]` が実機なしで次を出す。

- クラス（§1）・メッシュ数・マテリアル数
- **instanceに要るCPUバイト数**。`sub_736158` の問い合わせ経路（第9引数=1）を
  Unicornでそのまま回した値なので当てはめではない（アロケータ諸経費・GPU/VRAMは含まない下限）
- 各マテリアルの**レイヤー**と焼き込み済みPICA状態（blend / depth / alpha test）

候補の条件は「1モデル・1メッシュ・1マテリアル・`0x40000012`」で、romfs全体に**281件**ある。
最小の推奨は `Other/book.bcres`（7,040 B）。

```
book  nw::gfx::Model 0x40000012  meshes 1 materials 1  instance 1,396 B (align 32)
      layer=0  RGB src*ONE+dst*ZERO（完全不透明）  depth test=1 LT  alpha test 無効
```

**レイヤー0の完全不透明**なので、カメラ前にあれば地面を隠す。見えなければ
「ブレンドで薄い」ではなく「そこに無い」と即断できる。対して `UnitCursor` は
レイヤー1・`src*SRC_A + dst*ONE` の加算合成で、判定材料として弱い
（色が黒だから不可視という説は旧記録で既に否定済み。ここでは
「一発目の切り分けに向かない」という理由だけで避ける）。

## 4. 手順（2026-09-20 にこの通り実機で実行し、成立した）

park は `0x001B721C`（`BL BaseObj_RunDrawPhase` 直後のNOP）、復帰は `RET_TRAP 0x00838FFC`。
以下は既存2本のスクリプトの**合成**で、新規に逆アセンブルが要る関数は無い。

### 4.1 生成（probe側を借りる。差分は2点）

| 段 | 呼ぶもの | 出所 |
|---|---|---|
| S1 | `0x004B8CF0(0x600, 32)` scratch確保 | tree |
| S2 | `HeapAllocator_Ctor 0x005667E8` ×2（**`*allocr == 0` のときだけ**） | probe |
| S3 | `Heap_CreateNamed_0 0x0031785C` 資源用 `0x40000` / instance用 `0x20000`、親 `[0x0094CC48]` | probe |
| S4 | `G3dResHolder_Ctor 0x004ED860` | probe |
| S5 | `G3dResHolder_RequestLoad 0x00317920(holder, path, heap, 128)` を1に戻るまでフレーム送り | probe |
| S6 | `Setup 0x00317958(holder, allocr, 0, 1)` | probe |
| S7 | `FindModelByName 0x004A5F20(holder+4, name)` → `+4` が `CMDL` であること | probe |
| **S8** | **`0x004ED008(node_holder)`** で instance holder を構築（`node_holder+0 == 0x008FCCE8` を確認） | **tree。probeに欠けていた** |
| S9 | `ModelInstance_Create 0x004F048C(node_holder, model, allocr2, allocr2, **0, 0, 1**)` | tree（probeは `(0x834, 1, 3)`） |
| S10 | 戻り値1 **かつ** `holder+4` 非0 **かつ** `node+0x1EC`（activator）非0 | probe / IDA-unknown-F025 |

- **S8について**: `0x004ED008` は `holder+0` に `vtbl_g3d_SkeletalModel 0x008FCCE8` を、`holder+8` に0を置く。
  `ModelInstance_Create` は `holder+4` と `holder+8` しか書かないので、これを飛ばすと vtable が0のままになる。
  **ただしこれは不可視の原因ではない**。`TransformNodeHolder_SetMatrix3x4 0x004ED794` も
  `UpdateWorldAndSkeleton 0x004ECFEC` も `holder+4` しか参照しないことを逆アセンブルで確認した。
  破棄時に危険なので直すべき欠陥であって、§2の座標問題と混同しない。
- **S9の引数について**: `(0x834, 1, 3)` はゲームの `AcObjUnitCursor` が使う値、`(0, 0, 1)` は
  素の野外呼び出し元 `sub_58EEC0` と、**実機で描画に成功した木**の値。一発目は後者にする。
  `a5` ＝材質コピーマスク→`model+0x188`、`a7`→`SceneNode+72/+324` と `holder+8`（IDA-unknown-F023）。
  こちらが観測した `node+0x228 = 0` / `+0x22C = -1` の差は `a7 = 3` 側でのみ見ており、
  `a7 = 1` へ戻したうえで測り直すまで原因候補として扱わない。

### 4.2 配置（ここが新しい必須段）

```
xyz   = ゲーム座標（プレイヤーは [0x00AA7994] → +0x14 の3 float）
angle = FieldPosition_ToRenderSpace 0x0052CDD8 (&out_xyz, &xyz)   ← 戻り値がu16角度
行列  = scale と angle から §2 の3x4を組む
        （または Matrix3x4_AppendRotationX16 0x0056689C）
        TransformNodeHolder_SetMatrix3x4 0x004ED794 (node_holder, &行列)
        TransformNodeHolder_UpdateWorldAndSkeleton 0x004ECFEC (node_holder)
```

**書き込む前に `tools/models3d/verify_curved_pose.py` と同じ float32 計算で到達座標を出し、
カメラ位置との差が妥当（画面内）であることを確かめる。** 別エージェントが
「書込み前にpixelを計算確認」した手順（IDA-gpt-6-astra-F003）をworld側にも適用する。

屋内で試す場合は `g_RoomFlagTable[roomId] & 2` が0なので変換は恒等になる。
**この呼び出しを省くのではなく、常に通す**（部屋によって分岐するのはゲーム側の仕事）。

### 4.3 描画（2経路とも既に実機で通っている）

- **world**: park `0x001B721C` でシーン0へsubmit。上画面の左右両目に出る。下画面には出ない（IDA-unknown-F024(3)）。
- **画面固定**: `Render_DrawSceneIndexed` の記録list replay直後のNOP `0x004EF1B0` で専用pass。
  `CameraBind 0x00494D3C(lowContext, 私有source, 1)` → `DrawMesh 0x0048D26C(**[0x0094CA48]**, mesh, node)` →
  元cameraへ復帰。**`[0x0094CA40]` はscene rendererで別物**（別エージェントがここでSIGSEGVを出している）。

### 4.4 成功条件と切り分け

| 見えた | 結論 |
|---|---|
| 出た | 任意モデルの読み込み→描画が成立。§1のModel側は解決 |
| 出ない | まず **同じ座標に `fg_treeA_4` を置いて出るか**を見る。出るなら資源側（読み込み・頂点buffer）、出ないなら座標側 |

この対照実験は既存の素材だけで組めるので、**一発目から用意しておく**。
こちらの過去の失敗は、この対照を持たずに内部欄の比較へ進んだことで長引いた。

## 5. 未解決・危険

- **SkeletalModel（379件）は未検証。** 木はModelなので、`UnitCursor` を含む
  `0x40000092` 側が曲がった座標で出るかは**まだ誰も試していない**（別エージェントのF001も明記）。
  §4を `UnitCursor` へ当てるのは、Model側で1体出たあとの2段目にする。
- **資源の解放が未設計。** probe側もtree側もheap・scratch・instanceを保持したままで、
  GPUが参照し終わった保証が無い。場面転換・OOMは詰めていない。
- **instanceバイト数は下限。** `model_preflight` の値にアロケータ諸経費とGPU/VRAMは入らない。
  ヒープ不足は `ModelInstance_Create` が1を返したまま activator を0にする（IDA-unknown-F025）ので、
  戻り値だけで成功と扱わない。
- **同時に1体まで。** 複数体・アニメ・影（シーン2）・深度ソートは本設計の範囲外。

## 6. 実機なしで通せる検証

```
python tools/models3d/model_preflight.py --survey            # クラス2種・個数の2経路一致
python tools/models3d/model_preflight.py <bcres> [model名]   # クラス/バイト数/レイヤー/blend
python tools/models3d/verify_curved_pose.py                  # 曲がり変換のfloat32再現
python tools/hw/verify_unitcursor_hw.py                      # 読み込み側の番地51項目
```

## 7. 実機で確定したこと（2026-09-20、IDA-opus-5-F004）

`Other/book.bcres` を自前ヒープへ読み、`(0, 0, 1)` で instance を作り、
`FieldPosition_ToRenderSpace 0x0052CDD8` で姿勢を作って `0x004ED630(holder, 0)` へ
毎フレーム提出したところ、**上画面に本が現れた**。1,500 ms で実行 49 回・提出 49 回。

§0 の 3 点の修正はいずれも正しかった。加えて実機でしか分からなかったこと:

- **GPU アドレス変換は自前ヒープの資源でも通る**。属性コマンド列の `0x0200`/`0x0203` が
  自前 bcres のファイル内 offset を指していた。IDA-unknown-F027 の「黙って 0 になる」経路は
  romfs から自分で読んだ資源では踏まなかった。
- **`G3dResHolder_Setup` の `holder+12` は成否ではない**。`sub_4A5A74 0x004A5A74` が
  各オブジェクトの結果を OR した値で、Setup 自身が bit1 を見て 2 回目を回す。
  こちらは `0x80000006`、ゲーム自身の Season ホルダ `0x33109070` は `0`。どちらも描画は正常。
  呼び出し元 `ScStage_LoadIndoorRes` は Setup の戻り値を読んでいない。
- **計器は 2 本持つ**。「ケーブが走った回数」と「実際に submit した回数」を分けておくと、
  出なかったときに instance 側の検査落ちか描画側かを 1 回の走行で切り分けられる。

### 2026-09-21 追試（IDA-opus-5-F005 / F006 / F007）

- **SkeletalModel も描けた。** `UnitCursor`（`0x40000092`）を同じ手順・同じ `(0, 0, 1)` で置いたら出た。
  `book` と同じフレームに並べ、枠を片方ずつ切って帰属を確定させた（4 枚の画像と画素差分）。
  **§1 の 2 クラスは両方とも実機で描けたことになる。**
- **IDA-unknown-F029 の `node+0x228`/`+0x22C` は棄却。** 描けた `UnitCursor` の値は `0` / `-1` で、
  `a7=3` のときと同じ。`book`（Model）は `0x30FE8F44` / `0xBCD` だが、これはクラス差であって
  可視性の条件ではない。**`a7` も原因ではなかった。**
- **OFF の画像を取得した。** `enable=0` で両方消える。§4.4 の切り分け表は実測で埋まった。
- **ヒープ量は測って決める。** 親ヒープは `sead::ExpHeap` で、vtable スロット15 `0x0074D744` が
  `getFreeSize()`。`0x40000`/`0x20000` は実使用 7,544 B / 1,400 B に対し 35 倍過大で、
  2 体目で親の残り 109,976 B を超えて失敗した。**ファイル長＋1 KiB と `model_preflight` の値で決める。**
- **park の BP は `0x1B7220` へ。** 同じ boot 内で `0x1B721C` へフック語を書いて戻すと、
  以後その番地の BP で `continue_process` が失敗する。`0x1B7220` は次の NOP で xref は落下 1 件のみ、
  SP も一致するので同値。**`continue_process()` を直接呼ばず `run_timed.py` を通すこと。**

**まだやっていない**: 資源・instance・ヒープの解放。骨・アニメ（今回は静止姿勢のみ）。
複数の部屋・尺・3 体以上。§5 の危険はそのまま残っている。
