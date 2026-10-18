# ゲーム内3Dモデルの任意配置

2026-09-20更新（IDA / gpt-6-astra）。対象は主IDB `ida/db/acnl_jpn_v15_annotated.i64` と対応する日本版更新code。
目的は、木を起点に家具・公共事業・人間モデルを任意位置へ表示すること。
ワールド内配置と、ゲームカメラに依存しない画面固定配置の双方を扱う。組み込み先のメニューは前提にしない。

**木1種類の独立生成・指定位置への表示・OFFでの消去を実機確認した（IDA-gpt-6-astra-F001、HIGH）。**
不足していたのはゲーム座標から曲面状の描画座標への変換と傾きの設定。設計・実行手順・画像は [tree_live_plan](tree_live_plan.md)。**透明度、移動中の画面固定、pixel位置/倍率変更も木1体で実機確認（IDA-gpt-6-astra-F002/F003）。** 専用材質とlate passの実装・初版の失敗原因は [alpha_screen_plan](alpha_screen_plan.md)。常用3gx、場面移動時の寿命管理、他種への一般化は未完了。以下の旧静的結果は個々の根拠に従いMEDIUMのまま扱う。

## 表示の構成

モデル資源の取得、独立したモデルインスタンス、表示先を分ける。
ゲーム内の木を増殖させるアクター処理にはマップ状態・地形・成長・衝突等が混ざるため、
表示用インスタンスを基本とする。衝突・会話・家具の操作や永続配置は別途要求された場合の機能。

| 表示先 | 座標と描画 | 将来の拡張 |
|---|---|---|
| ワールド | ワールド位置・回転・倍率。ゲームのカメラで描く | 複数モデル、ポーズ、アニメーション |
| 画面固定 | 画面上の位置・大きさを指定。独立したビュー/投影を使う | 上下画面、回転プレビュー、複数表示 |

画面固定は3D形状を保った表示。平面画像化や、常にカメラを向く板ポリゴンへの置換を必須にしない。
投影を別にすれば固定透視投影でも直交投影でも成立する。ゲームカメラの逆行列を毎回モデルに掛ける方式は、
カリング・照明・地形補正まで分離できないので基本設計にしない。

画面固定の候補は次の2つ。直接描画は専用view/projectionで木1体の実機試験に成功し、テクスチャ合成は未実装。

| 方法 | 利点 | 残る負担 |
|---|---|---|
| 独立カメラで画面へ直接描画 | 追加の色テクスチャを持たずに済む可能性 | 既存描画との順序、深度、viewport、状態復元を専用パスで管理 |
| 独立カメラでテクスチャへ描画し、2Dとして合成 | 画面位置・切り抜き・表示順・複数枠を整理しやすい | 色/深度バッファ、GPU同期、透明背景、追加メモリと描画負荷 |

現行は前者の最小実装。後者は枠ごとの深度や複数表示を必要とするときの候補で、GPU同期とメモリ負担を検証してから選ぶ。
既存の影マップは別用途なので、そこへモデルを登録するだけの実装はしない。

## 共通の入口と寿命

| VA | 現行IDB名 | 根拠と制約 |
|---|---|---|
| `0x4A5F20` | `G3dResource_FindModelByName` | 読込済み資源の相対ポインタ辞書からモデルを検索。instanceを生成する関数ではない |
| `0x4F048C` | `ModelInstance_Create` | 家具と地面オブジェクトの双方から到達。出力holder `+4`がTransformNode。返値とholderを検査するが、OOMは内部でnull参照し得るため事後検査だけでは不十分 |
| `0x4ED008` | `g3d_SkeletalModel_Ctor` | 12-byte holderの初期化。wrapperのRTTIと中のnode型は別 |
| `0x52CDD8` | `FieldPosition_ToRenderSpace` | game xyz→曲面上のrender xyz、戻り値u16はX傾き。屋外ではraw player座標をそのままmatrixへ渡さない |
| `0x56689C` | `Matrix3x4_AppendRotationX16` | 上記の戻り角でmatrixをX回転。並進を保持。SetMatrix/Updateの前に呼ぶ |
| `0x4ED57C` | `TransformNodeHolder_SetTranslation` | holder内nodeの位置を書き、更新bitを立てる |
| `0x4ED794` | `TransformNodeHolder_SetMatrix3x4` | `0x135C28`で12 floatsをコピーし更新bitを立てる |
| `0x4ED6B4` | `TransformNodeHolder_SetScale` | 独立倍率。ゼロ付近の値を補正するため直接書込みとは挙動が異なる |
| `0x4ECFEC` | `TransformNodeHolder_UpdateWorldAndSkeleton` | world変換→条件付き骨格更新。正常callerは姿勢行列設定後に呼ぶ |
| `0x4ED630` | `Scene_SubmitNode` | holderを指定sceneへ毎フレーム登録。永続的なマップ配置ではない |
| `0x4F053C` | `ModelInstance_Destroy` | `0x4F0184`による前処理後、holderのnodeを破棄 |
| `0x4ED668` | `SceneNodeHolder_Destroy` | nodeのdtorと所有allocatorによるfreeを呼び、holder `+4`をクリア |

node内のmatrixは `+0x4C`、translationは `+0x58/+0x68/+0x78`、scaleは `+0x7C/+0x80/+0x84`、
更新bitは `+0x88` の `0x800`。計算と命令照合は `verification.json` に保存。
world更新は下記の正常callerと照合済み。独立した表示物に必要な親/global状態、カリングと登録の実行順序、公開APIの回転表現は引き続き確認する。

資源は参照元が破棄されるまで無期限に借りられるものではない。モデルの生成・更新・登録・破棄は
ゲームの適切な実行文脈で行い、描画中のデータをGUI等の別スレッドから直接変更しない。
シーンから外した直後にGPU参照まで消えると仮定しない。部屋・季節変更では先に表示を停止し、
保留中の描画と生成要求を解消してから、instance、専用material/animation、資源の順を検証して解放する。

## 木の入口

通常の地面オブジェクト分岐は `0x58FB40` 内の `0x58FD20` から以下へ到達する。

```text
Item_GetFieldObjDef(Item)
  -> def+0xCのshape索引（0x87未満、範囲外は0へ補正）
  -> *(fgManager+0x414) + 22 * shapeIndex
  -> record+5のモデル名（record+0x15を終端化）
  -> FieldSeasonResource_FindModel(name) [0x5992D4]
  -> G3dResource_FindModelByName(fgManager+0x34, name)
  -> sub_58EEC0
  -> ModelInstance_Create
```

stride 22は `0x58FD5C/60/64` のADD/LSLから計算し、decompileだけから推定していない。
`fgManager` の入口は `off_948E70`、屋外判定は `byte_948E5F`。実行時ポインタはこのbootで取り直す。
`sub_58EEC0` はマス座標をワールド座標へ変換し、地面の高さ・カテゴリ状態を処理するので、
このラッパを「任意3D座標の表示API」としてそのまま呼ばない。

`0x599490` は `Fg/Param/FgShape.bin` と `Fg/Bcres/Season%02d.bcres` を読み、
`treeA/treeA2` という資源内名称も参照する。これはroot+0x28の別辞書内の名称で、下記のモデル名と同一視しない。
`0x590750` の `fg_treeB_d/fg_treeB_d_t` は別の専用経路であり、通常の木全般の代表と決めつけない。

ファイル所在の索引は `artifacts/base/romfs_index.txt` と `artifacts/update/romfs_index.txt`。
base側にSeason/FgShape、update側にFg.bin/FgItemOutsideがある。更新側に無いファイルを欠落と即断しない。
ctrtoolで展開済み。baseはSound/asrでエラーとなり10753/12938ファイルの**部分展開**、updateは4150ファイルすべて完了。
必要なFgShape/Fg.bin/Seasonの25資源は取得できており、独立RomFS parserが原本の該当bytesと全件一致を確認した。
base全体の展開完了や欠落音声の正常性を主張しない。`romfs_extraction.json`と`work/logs/models3d_ctrtool_*.log`に状態を残す。

## 最小候補の具体化（IDA-unknown-F009）

**Item `0x26` → shape `0x25` → `fg_treeA_4`**を最初の候補とする。
更新版`Fg.bin`は4064 bytes、索引コード`0x2FD064`の16-byte/254-record形式に合う。`+0xC`のshape値から
base `FgShape.bin`を22-byte strideで引き、`+5`の文字列を得た。base側Fg.binは別形式なので更新版のstrideを流用しない。

索引に存在する**Season00..22の23資源**すべてで、モデル辞書の名前とモデル自身の名前が`fg_treeA_4`で一致。
CMDLのtypeは`0x40000012`、mesh/materialは各1。Season00のモデルfile offsetは`0x1BFC0`（VAではない）。
DICTの相対ポインタ・件数・範囲も検証した。同じ木本体へ到達する果実Itemもあるが、果実等の別処理まで同一とは限らない。
見た目と配置の実機試験は未実施。

## 生成ABIと共有範囲（IDA-unknown-F010）

`0x58EEF8`の正常field callerから、`ModelInstance_Create`の全引数をassemblyで確認した。

| 場所 | 値・役割 |
|---|---|
| R0 | 初期化済みholder。正常callerではfield object+0x58 |
| R1 | lookupしたResModel* |
| R2 | `ssys::ma::HeapAllocator`オブジェクト。正常callerではfield object+0x20 |
| R3 | 正常callerではR2と同じallocator。普通のModel以外の資源分岐でも使うため推測で0にしない |
| stack+0 | materialフィールドのcopy mask。正常値0 |
| stack+4 | 補助メタデータ生成flagの下位byte。正常値0 |
| stack+8 | 補助count。正常値1、descriptor+0x1Cとholder+8へ渡る |

下位wrapper `0x48E350`のdecompileにはfloatのような表示があるが、core registerのallocator pointerをVFP経由で運んでいる。
その疑似型からC ABI宣言を作らない。型は今回変更していない。
`0x736158`のtype分岐で、この木は`nwgfx_Model_Create` (`0x4AB270`)へ進み、node本体は`0x220` bytes。
holder ctorのRTTIは`g3d::SkeletalModel`（vtable `0x8FCCE8`）でも、中のnodeが骨格モデルとは限らない。

mesh記述子は`0x4AA0BC`でinstanceへコピーされ、相対ポインタ表・visibilityも個別に持つ。
ただし元のgeometry/texture等まで複製するわけではない。materialは`0x4AF068`でwrapperを作っても、mask0では元ResMaterialのフィールドを共有する。
`Material_GetResourceForMask` (`0x523D38`)は要求bitがcopy maskに含まれなければ元資源を返す。
nonzero maskの基本private materialは`0x2D8` bytesで、追加領域はbitに依存する。
mask `0x10`は比較検証に使った値で、全材質の完全コピーや画面固定に必要な設定だと確定したものではない。
共有資源へ`ResModel_SetRenderLayer`を呼んで個別モデル設定とする方法は採用しない。

### allocatorと失敗条件

field object ctor `0x59033C`は`+0x20`に`ssys::ma::HeapAllocator`を構築（`0x5667E8`）。vtableは`0x90053C`、
wrapper `+4`がheapで、binder `0x12D3A4`が設定する。生heap pointerやmalloc領域をallocatorとして渡せない。
allocator `0x569B54`はalignment0を1へ補正し、heap vtable+0x18へsize+alignmentとalignmentを渡す。free `0x569B44`はslot+0x1Cを使う。
他のfield objectのallocatorはそのownerのheap resetに巻き込まれるので借用しない。

**OOMは安全な失敗返値にならない経路がある。** `0x4AB2BC`の確保失敗でR8=0となり、`0x4AB4A0`へ進むとnullのvtableを参照する。
さらにvirtual Setupの結果を呼出し側が伝播しない。返値とnonnull holderだけで生成の完全成功を保証できない。
専用allocatorの準備・十分な容量・内部確保の失敗対策を先に設計する。下記サイズだけをheap容量として確保して呼ばない。

### 更新と破棄

正常field pose `0x590034`はMatrix3x4設定後、`TransformNodeHolder_UpdateWorldAndSkeleton`を呼ぶ。
これはholder+4に対し`0x4EF69C`でworld変換、`0x4EF624`で条件付き骨格更新を行う。
親nodeまたはidentityとglobal変換状態`0x94CA34`を使うため、任意スレッドから呼べるという根拠にはならない。

`ModelInstance_Destroy`は`ModelInstance_SortMeshPointersForDestroy` (`0x4F0184`)を先に呼ぶ。
描画で並びが変わり得るmesh pointerを昇順に戻し、dtor `0x4AB638`が先頭entryからmesh連続領域をfreeする前提を整える。
局所pointer配列は65要素で、明示的な上限検査は未確認。今回の木はmesh1だが、多数meshの家具/人間まで一般化しない。
この前処理とholder dtorにはGPU完了待ちがない。

## サイズ・ready・資源寿命（IDA-unknown-F011）

`verify_tree_contract.py`はIDAから取得した命令を原本codeと照合し、Unicornの**ARM11MPCore**で
`0x736158`のサイズquery分岐と許可した3補助関数だけを実行する。
コード/読み/書きの範囲を制限し、未知API・SVC・GPU・allocatorのmockは使わない。資源は読み取り専用、stackはcanary検査付き。
独立Python allocation ledgerと**23 Season × 2 masks = 46ケース**が一致した。

| copy mask | builder見積もり | 最大alignment |
|---|---:|---:|
| `0`（正常caller値） | 932 bytes | 32 bytes |
| `0x10`（比較用） | 1664 bytes | 32 bytes |

これはinstance生成データの**query値**。heap wrapperのsize+alignment、heap管理領域、元資源、GPU描画先等は含まない。
実機確保やモデル表示の成功ではない。初版検証器は関数外literalの取り込み漏れで不一致となったため、IDAからliteralを取得し、厳格な読み取り範囲検査も加えて再検証した。

資源ownerはRTTI `fgobj::Proc`（vtable `0x9020DC`）。Setup `0x59C974`は資源ロード後、
**残りのSetup/FuncNode生成より前の`0x59CBB0`で`off_948E70`を公開**する。nonnullはready保証にならない。
Seasonはmanager+0x2Cのholder、+0x34のresource pointerで管理し、ゲーム側が再配置・texture/shader準備を行う。
未準備のraw bcresをそのままCreateへ渡さない。

`fgobj_Proc_Destroy` (`0x59D878`, vtable+0x18)はstock model/FuncNode/field objectを除去し、
`0x59D980`でglobalを消し、`0x59D9D8`でFgShape、`0x59DA04`でSeason、その後heapを解放する。
追加instanceは借りた資源の解放前に終了させる必要があり、globalの変化を後からpollするだけでは遅い。
pointerのアドレス再利用も考慮する。ここで確定したのはCPU側の呼出し順で、GPU retirement/fenceは未確定。

`0x59C8FC`（Proc vtable+0x30）は既存objectの描画リストを用意し、manager+0x45B0のFuncNodeをscene0へ登録する。
今後の実行位置の候補だが、追加の普通Modelをここで直接submitして成立するかは未実測。
manager+0x20はraw heap、field object+0x20はallocator wrapperなので、ownerの違う同offsetを混同しない。

## 種類を増やす際の境界

| 種類 | 既存の足場 | 追加確認 |
|---|---|---|
| 木 | Item0x26/fg_treeA_4、23 Season、共通Create/更新/破棄を照合 | 安全な実行位置・allocator・GPU終了、揺れ/果実等の別部品 |
| 家具 | AcFtr→Item/Model、旧F92では家具の3D表示成功 | remake/material、カテゴリ別モデル。旧実験の服カテゴリはクラッシュしており全種類へ一般化しない |
| 公共事業 | Strc資源のファイル索引とAcStrc関連の既存解析 | 本体/CROのロード範囲、複数部品、固有アニメーション。木と同じ生成契約とはまだ確認していない |
| 人間 | RTTI `HumanModel` / `PlayerModel`、Player/HumanAnim資源 | 頭・顔・服・骨格・姿勢の合成と各資源の所有者。単一bcresの読込みだけで完結するとしない |

種類ごとの資源解決を独立させ、共通の表示ハンドルは姿勢・表示先・生成/破棄状態を管理する案。
人間等の複数部品も一つの表示ハンドルにまとめられるようにする。呼出し側へ生のゲームポインタを公開しない。
これは設計案で、C++のABI宣言や実装済みAPIではない。

## 旧資料からの訂正（IDA-unknown-F008）

1. **旧 `ModelInstance_SetRenderLayer` (`0x317BD0`) は資源側の関数。** 現行名を `ResModel_SetRenderLayer` に修正。
   `0x58EA60`の資源lookup結果を`0x58EA78`へ渡し、その後でinstanceを生成するcallerをassemblyで確認。
   AcFtrもholderではなくresource getter（vtable `+0xD8`）の結果を渡す。関数内はresource
   `+0xBC/+0xC0`から相対辞書を辿り、entry `+0x298`を書き換える。共有資源へ実行すれば他instanceへ影響し得る。
   copy maskによる分離経路は上記で確認したが、layerを含む必要フィールドの安全な組合せは未確定。
2. **sceneIndex 2は自由なプレビュー枠ではない。** `Render_DrawScene2` (`0x4E976C`) は
   `BsShadowMapMgr`が存在するときだけ描画先/状態を切替えて`Scene_DrawLayers`を呼び、復元する。
   ownerは`0x264C08`の文字列だけでなく、RTTI/vtableの対応でも照合。旧「無条件」は呼出し地点と関数内条件を混同している。
3. **render-layer、sceneIndex、display IDを分ける。** 数字が同じでも同一の選択値ではない。
   Catalogカメラ自体は存在するが、`BsCamera_ActivateContext`は通常/副カメラ状態でコンテキストを選ぶ。
   メニューを開く処理や既存カメラの切替を、本件の独立表示の実装として採用しない。

旧文書は参照専用なので書き換えず、現行IDBとこの文書で訂正する。

## 次の検証

1. 木1体の生成/pose/scene0登録は実機成功。次はowner解放前かつGPU参照終了後の破棄位置を確定する。
   専用heapは128KiBで生成成功したが最小容量/OOM時の完全な安全性は未証明。
2. 2位置・倍率0.5/1.0の表示/OFFを確認済み。追加回転を確認し、ゲームのcurve係数が変わる場面でもposeを更新する。
   非表示とメモリ解放を区別し、場面遷移・再生成を検証してから常用3gxへ進む。
3. 同じモデルを独立ビューへ載せ、ゲームカメラ移動、上下画面、左右目、深度/透明度/描画順を比較する。
   既存2D Layoutへ3Dモデルを渡すだけでは成立しない。画面固定パスの呼出し契約と状態復元を検証する。

実機試験前に元命令・ABI・全LDR/分岐・領域台帳・復元経路を検証する。監査済注入コードは `tools/models3d/{call_guard.s,build_display_hook.py}`。今回gohan/3gxは変更していない。

## 根拠

- 新しい取得結果: `work/evidence/models3d/static_initial.json`（キー名は作業用ラベルで意味の確定ではない）。
- IDA bytes: `idb_bytes.json`。元codeとの12領域一致、独立Capstone ARM逆アセンブル、RTTI、計算: `verification.json` / `independent_arm.txt`。
- 再現: `tools/python/idalib/Scripts/python.exe tools/models3d/verify_static.py`。IDBや実機は変更しない。
- IDBの命名・コメント・読戻し: `idb_updates.json`。更新は静的注釈のみ。
- XMLも更新・独立検証済み。`artifacts/exchange/ida/acnl_jpn_v15.xml` に新しい名前を確認し、保存IDBのSHAとmanifestを照合。`work/evidence/models3d/final_verification.json`。
- 続きの静的結果: `tree_static.json`＋`tree_lifecycle.json`。raw結果の作業ラベルは関数名の確定ではない（例: size_wrapper_candidateはSceneContext ctor）。
- 資源同定/原本照合: `tree_assets.json`、再現`python tools/models3d/inspect_tree_assets.py`。展開は`prepare_assets.py`で検証後にctrtoolを使う。部分展開は自動上書きしない。
- ARM11と独立計算: `tree_idb_bytes.json`、`tree_contract.json`、`tree_independent_arm.txt`。再現`tools/python/idalib/Scripts/python.exe tools/models3d/verify_tree_contract.py`。
- 今回の注釈6名称/10コメント: `tree_idb_plan.json`、`tree_idb_updates.json`。今回のXML読戻しは`tree_final_verification.json`。
- 旧実機結果の参照: `reference/old_project/RE/FINDINGS.md` F70/F82–F92/F111/F119/F120、`reference/old_project/DOCS/furniture_rendering.md`。

## 家具の設置範囲表示（UnitCursor）を素材にする

模様替えで家具を掴むと家具の下に出る範囲表示は、パーティクルではなく `romfs/Ftr/Chip/UnitCursor.bcres` の 3D モデル（IDA-unknown-F019）。
屋内の場面でしか資源が読まれず（`ScStage_LoadIndoorRes` 0x611928）、表示クラス `AcObjUnitCursor` は `ModuleIndoor.cro` にあり、
位置も家具オブジェクト番号から取るため、屋外へそのまま持ち出せない。屋外で出すなら本資料の任意モデル表示と同じ手順で、
`UnitCursor.bcres` を自前のヒープへ読み、`G3dResource_FindModelByName` → `ModelInstance_Create` →
`TransformNodeHolder_SetMatrix3x4` → `TransformNodeHolder_UpdateWorldAndSkeleton` → `Scene_SubmitNode` を使う。
色や「置けない」表示を変えるなら資源内の `VisibilityAnimation` / `MaterialAnimation`（`UnitCursor` / `UnitCursorNG` / `UnitCursorRotate`）を併用する。
資源のモデルは `UnitCursor` 1 つだけで、`UnitCursorLine` などはノード名。アニメ 3 本のうち `UnitCursorRotate`（3 フレーム）は
家具の大きさ（`0x00690B68` の 0〜3）をフレームにして静止させる「形の選択」に使われ、明滅は `UnitCursor` / `UnitCursorNG`（各 150 フレーム）が作る。
詳細と根拠は `work/evidence/unit_cursor/README.md`。
なお**家具モデルそのものは屋外でも表示される**（`g_RoomFurnitureCapacity` 0x008835BC が村 38・オートキャンプ場 10 など非0で、
`BsFtrMgr_CreateResources` がその数だけ枠を作る。IDA-unknown-F020）。屋外に無いのは UnitCursor の資源と表示クラスだけ。

屋外で UnitCursor を出す段取りと未解明点の一覧は `work/evidence/unit_cursor/outdoor_plan.md`（IDA-unknown-F021）。
