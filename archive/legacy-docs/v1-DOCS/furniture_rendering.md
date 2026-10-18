# 家具アクターの読込・3Dプレビュー・描画経路

対象は JPN 無印版の `code.bin.i64`。通常カタログ mode 0 で選択した家具が、
`Item` から `AcFtr` 系アクター、モデルリソース、NintendoWare g3d の描画レイヤーへ至る経路をまとめる。
本ページは静的解析を主根拠とし、Remote GDBの値は失敗段階の照合にだけ用いる。

## 結論

現在の屋外カタログで3Dが出ない理由は、屋外にCatalogカメラ、Catalog専用ライト、または
Catalog用描画passが無いからではない。これらはroom 0でも生成される共通基盤である。

stockの屋外room 0に無いものは **`BsFtrMgr` オブジェクトそのもの**である。room 0の
家具容量表には38枠あるが、容量値はmanagerを自動生成しない。stockではroom flagsのbit `0x8`
が立つ部屋だけが、type `0xEE` (`BsFtrMgr`) を含む室内共通screen groupを生成する。

初版と第2版はいずれも実機private stateが
`owned manager=0 / status=3 / g_BsFtrMgr=0 / actor=0` になった。精密に再読したbyteは、
`ScStage` (`0x3308638C`, vptr `0x8F2480`) もsaved `BsMenuTab`
(`0x32C851B8`, vptr `0x8F3710`) も `+14=1 / +15=0` である。
`UiScreen_OpenChild` (`0x51EC58`) のparent gateは両者とも通過するため、以前の
「`ScStage +15=1`でfactory前に拒否」という判定は撤回する。

第2版でparentを `BsMenuTab` へ変更しても同じ即時失敗になったことから、失敗点はchild生成後の
generic create phaseにある。room 0の容量38をlate createにもそのまま適用し、phase 1で大量の
bank heapを一括確保する経路は、容量1版がbank count 1でphase 1を通過したことで動的にも
支持された。

さらに、`g_BsFtrMgr` は生成phase 1の末尾で公開され、その後に
`Ftr/Common/FtrCommon.bcres` の非同期完了待ちと生成phase 3が続く。Catalog側はactor生成に
失敗しても選択cacheを先に更新するため、更新版はmanager `+19` の生成完了bit
`(byte & 3) == 3` を待ってから選択cacheを1回だけ無効化する。2026-08-25に
初版active stateを保持したまま更新版へ移行し、読戻し確認後にプロセスを再開した。

ただし「cacheを無効化しない」だけでは不十分だった。容量1版ではmanager `+19=1` の時点で
`g_BsFtrMgr`が公開され、同frameのstock preview bodyがtype `0xBC` actorを生成した。
このprovisional actorのvptrから命令語 `0xE1A04000` を関数pointerとして呼び、SIGSEGVになった。
従ってowned managerのstatus 1中は、stock preview bodyへ戻らずupdate全体からreturnする必要がある。

## room生成と `BsFtrMgr`

`sub_5B3F38` はroomのscreen群を次の順で生成する。

1. 全room共通group `unk_884004`
2. room flags bit `0x8` が立つ場合だけ室内共通group `unk_884388`
3. room固有descriptor

`unk_884388` の4エントリは `0x952C20` から始まり、静的初期化 `sub_78A6B8` が次を設定する。

| type | class / factory | 備考 |
|---:|---|---|
| `0xEE` | `BsFtrMgr`, factory `0x7F1BE4` | 家具actor、heap、共通家具resourceの所有者 |
| `0x26F` | `fgobj::Proc`, ctor `0x59DC30` | field object処理 |
| `0x5B` | `BsIndoorPlateMgr`, ctor `0x2AAA14` | 室内plate管理 |
| `0xA3` | factory thunk `0x7B1428` | class名未確定のためIDBではrenameしない |

村room 0のroom固有type列に `0xEE` は無い。従ってstock屋外では `g_BsFtrMgr == 0` であり、
Catalogの3D経路は安全にnull actorへ縮退する。一方、`BsFtrMgr_CreateResources`
(`0x68FC44`) が参照する容量表はroom 0へ `0x26`（38）を返す。
これは「外部からmanagerを正しく生成した時に38枠を確保できる」ことを意味するだけで、
stockでmanagerが存在する根拠ではない。

## `BsFtrMgr` の3段階生成

RTTIは `BsFtrMgr`、vtableは `0x8F2BE8`、typeは `0xEE`、サイズは2240 bytes。
generic wrapper `UiScreen_CreatePhases` (`0x81EDFC`) がvtable slot 16～18を順に呼ぶ。

| phase | function | 処理 | return |
|---:|---|---|---|
| 1 | `BsFtrMgr_CreateResources` `0x68FC44` | 共通heap、actor record buffer、最大50 bankのCPU/VRAM heapを確保 | 成否 |
| 2 | `BsFtrMgr_WaitCommonResource` `0x68FB3C` | `Ftr/Common/FtrCommon.bcres` を非同期で開き完了待ち | 3=待機、1=失敗、2=完了 |
| 3 | `BsFtrMgr_PopulateRoom` `0x68F1C0` | 共通transitionを初期化し、map上の家具actorを走査・生成 | 完了 |

生成状態はobject `+19` の下位2bitで管理される。

- bit 0: phase 1を呼び終えた
- bit 1: phase 2が完了しphase 3も呼び終えた
- 完全生成済み: `(manager[19] & 3) == 3`

重要なのは、`BsFtrMgr_CreateResources` が `0x6900E4` で `g_BsFtrMgr = this` とする時点である。
これはphase 1の中であり、phase 2/3より前である。従ってglobalの公開は「利用可能になり始めた」合図で、
全resourceとUiScreen生成の完了通知ではない。

manager `+20` は最大50件の
`BankTable<Bank<96000,1,false,BankVramConfig<20500,15,5500,15,true>>,50>` である。
1 actorごとに次を持つ。

- CPU heap: 96,000 bytes
- VRAM A: 20,500 bytes
- VRAM B: 5,500 bytes
- actor側handle: `actor+792` のowner/index

room 0の38 bankではCPU heapだけで3,648,000 bytes、VRAMは合計988,000 bytesを要求し、
別に35,840-byteの共通heapも作る。各bankのCPU 96,000-byte確保が1件でもnullなら
`BsFtrMgr_CreateResources` は0を返す。`UiScreen_CreatePhases` (`0x81EDFC`) はこれを
generic result 1（失敗）へ変換し、`sub_51EF38` は新規childをその場で破棄する。
そのためフレーム後の観測が `owned=0 / g_BsFtrMgr=0` になることと整合する。

`AcFtr_LoadResources` はこのbankのCPU heapがnullならモデルを読まずにreturn 2を返す。
これはクラッシュを避ける安全縮退だが、外見上は「actor生成が進んだのに何も描かれない」状態になる。

## Catalog選択からactor typeの決定まで

入口は `BsMenuCatalog_UpdatePreview` (`0x21A9FC`) で、実処理は
`CatalogPreview_UpdateActor` (`0x690E28`)。mode 0かつ有効な選択indexの時だけ動く。

```text
FtrListの選択変更
  -> BsMenuCatalog_UpdatePreview
  -> CatalogPreview_UpdateActor(&g_CatalogPreview, Item)
       -> ItemParam_GetRecord(Item)
       -> ItemParam_GetFurnitureActorType(record)
       -> UiScreen_OpenById(type, g_BsFtrMgr, request(mode=2), 0, 0)
```

`g_CatalogPreview` は `+0` がactor pointer、`+4` がcached Item。
カテゴリ3、4、`0x29` はItem `8312`へ正規化される。item適格性を通り、room flag
`0x10000` が立っていない時にactor生成を試みる。村room 0はこの拒否bitを持たない。

ここで以前の解析を訂正する。actor typeは現在room descriptorから選ばれない。
`Item/Param/Item.bin` の30-byte recordにある `+17` の家具family byteを読み、
`g_FurnitureActorTypeByFamily` の固定表へ通す。86 familyが実行ファイル内のtype
`0xBB`～`0xEB`へ対応し、各typeには `AcFtrChair`、`AcFtrBed`、`AcFtrAudio` などの
具体的factoryが存在する。従って屋外roomのCROに家具factoryを追加する必要はない。

`CatalogPreview_UpdateActor` はactor生成を試す前にcached Itemを書き換える。
`g_BsFtrMgr == 0`、親が生成途中、または `UiScreen_OpenById` が0を返した場合でもCatalog本体は継続し、
同じ選択は再試行しない。別品へ移動、再度選び直し、またはcacheの明示的無効化が必要になる。

## `AcFtr` の3段階生成

共通基底はRTTI `AcFtr`、main vtableは `0x8F1894`。Catalog requestのmodeは2である。

### phase 1: `AcFtr_CreatePrepare` (`0x56DE24`)

- requestのItemを `actor+1508`、mode 2を `actor+1516` へ保存
- `ItemParam` pointerを `actor+1520` へ保存
- preview位置・scale recordを `actor+1524` へ保存
- preview座標を `x=0`, `z=0`, `y=record[2]-18`、scaleを `record[1]*0.01` に設定
- `actor+792` を `g_BsFtrMgr+20` のbank tableへ登録
- `actor+784` を現在sceneへ登録

manager bank登録とscene登録の論理積がこのphaseの成功条件である。

### phase 2: `AcFtr_LoadResources` (`0x56DAE4`)

manager bankの96KB CPU heapを取得し、派生classのvirtual load処理を呼ぶ。
通常 `AcFtr` 系は `ItemModel_BuildPath` (`0x4E9320`) で `ItemParam_GetModelName`
のmodel名から次を構築する。

- `Item/Model/%s.bcres`
- 必要に応じて `Item/Model/%s_mtl.bcres`
- jewel系では `Item/Model/%s_jwl.bcres`
- mannequinは専用分岐

初回queueは `ItemModel_LoadFirst` (`0x4E9674`)、継続pollは
`ItemModel_LoadPoll` (`0x4E94B8`)。remake可能品はさらに次を読む。

- `Ftr/Remake/Texture/%s_base_%02d.bcres`
- `Ftr/Remake/Texture/%s_fabric_%02d.bcres`
- 対応するbase/fabric variation

return 3は非同期待ち、1は失敗、2は完了。mode 2だからといってモデル読込を省略する分岐はない。

### phase 3: `AcFtr_CreateFinalize` (`0x56D66C`)

material名 `m_b_j`, `m_b`, `lp_m_b`, `env_mtl`, `m_f`, `lp_m_f`,
`base_00`, `fabric_00` をbindし、派生classからloaded modelを取得する。
`ModelInstance_Create` (`0x4F048C`) がNintendoWare g3d model instanceを構築し、
preview scaleを反映する。mode 2では `ModelInstance_SetRenderLayer` (`0x317BD0`) が
全model entryのfield `+664` を2へ変更し、既存render keyを無効化する。

以後 `AcFtr_UpdateModel` (`0x5749EC`) がtransform、material、light関連状態を更新する。
GPU commandの生成自体はNintendoWare側のrendererへ委譲され、家具固有コードが毎frame
直接draw commandを発行する設計ではない。

## renderer、Catalog camera、Catalog light

### renderer layer 2

global renderer初期化 `0x4E97CC` は `dword_9C3098[3]` と
`dword_9C30A4[3]` を3組すべて生成し、`nw::gfx::BasicRenderQueue` とmaterial/depth key factoryを作る。
frame処理 `0x4F1CE4` は3組すべてを反復する。Catalog previewが指定するindex 2はこの第3組であり、
room生成物ではない。

### `CameraCatalog`

`BsCamera_Ctor` (`0x68EDDC`) は全roomの `BsCamera+768` に
`CameraCatalog` (vtable `0x8E84F0`) を内包する。
`BsCamera_CreateContexts` (`0x68EAB8`) は通常context `+20` に加えてCatalog context `+220` も初期化する。
`BsCamera_ActivateContext` (`0x68EA64`) はsecondary camera pointerの有無で両contextを切り替える。
room 0だけCatalog cameraを構築しない分岐はない。

### Catalog専用3灯

`BsLightMgr_CreateRoomLights` (`0x190578`) はroom固有lightを作った後、対応room経路では次の3灯を
生成してactiveにする。この処理は店内だけではなくroom 0にも到達する。

| type | class |
|---:|---|
| `0x105` | `BsLightDiffuseCatalog` |
| `0x106` | `BsLightAmbientCatalog` |
| `0x107` | `BsLightHemiSphereCatalog` |

従って屋外では専用ライトが無く屋外lightだけで家具が描かれる、という以前の予想は誤りである。

## 破棄経路

Catalogで選択解除・別品選択・画面終了になると `0x6910B8` が現在preview actorへ
`vc_UPDATE_MENU` (`0x51F4C0`) を送り、`g_CatalogPreview+0` を0へ戻す。
`AcFtr_DestroyBegin` / `Wait` / `Finalize` (`0x570330`, `0x5702BC`, `0x56F448`) は
model/remake resourceを解放し、scene handleとmanager bank handleを解除する。

一時 `BsFtrMgr` は `BsFtrMgr_BeginDestroy` / `Unpublish` / `DestroyResources`
(`0x690CD8`, `0x690CB8`, `0x690964`) の順で破棄され、phase 2で `g_BsFtrMgr` が0へ戻る。
preview actorをmanagerより先に閉じるstockの親子順序を維持する必要がある。

## 更新版patchの実装条件

第2版は次を実装した。

1. `UiScreen_OpenById(0xEE, savedBsMenuTab, ...)` の戻りをadapter-owned pointerとして保持する。
2. `g_BsFtrMgr == ownedPointer` だけでは再試行しない。
3. `(ownedPointer[19] & 3) == 3` を確認してからCatalog `object+8160` を `-1` にする。
4. cache無効化は1回だけ行い、actor生成後は `g_CatalogPreview+0` を観測対象にする。
5. Catalog終了時はpreview actorの終了を先に要求し、その後にowned managerを閉じる。
6. manager生成phase 1/2/3の失敗時は3DなしでCatalogを継続し、nullを描画しない。

第2版でも3Dなしを実機確認したため、第3版のscript sourceは追加で次を実装する。

7. `0x68FD2C` でroom容量を受け取った直後、adapter stateがactiveかつpreview statusが0の間だけ
   容量を1へ制限する。通常のroom load、既存manager、Catalog終了後には作用しない。

容量1でphase 1まで進んだ実機結果から、第4版はさらに次を実装する。

8. manager生成を要求した同一frameはstock preview bodyへ入らない。
9. preview status 1でmanager未公開、またはpublished managerの
   `(manager[0x13] & 3) != 3` の間は、保存registerを復元してpreview update自体からreturnする。
10. status 3（manager生成失敗）だけはstockの3Dなし経路へ戻す。

第4版再開時、manager phase 3自身のroom populateでも同じtype `0xBC` crashが起きたため、第5版は
さらに次を実装する。

11. `BsFtrMgr_PopulateRoom`のcommon初期化は実行する。
12. adapter-owned managerに限り `Field_GetMapManager`を0としてfield map走査を省く。
13. 時刻設定とphase 3 returnはstockどおり実行し、create flag bit 1を正常に立てる。

manager完成後、選択Item `0x2EA3`自身もItemParam family 1からtype `0xBC` (`AcFtrLoop`)を
選び、generic createの `vptr+8=0xE1A04000`で3回目のSIGSEGVになった。停止中実機では
ItemParam base `0x32FF8280`、record `0x3301399A`、record `+0x11=1`、family table result
`0xBC`を確認した。従って今回はdefault fallbackではなく正規のfamily選択である。

例外objectの4 vptrを基底`AcFtr`へ戻すと、pre/create/post targetは
`0x6E3A10 / 0x81F2B8 / 0x307D08`、create resultは2となり、preview actorへattachできた。
この結果から第6版はさらに次を実装する。

14. `0x690FF8` のpreview open callをguard付きwrapperへ接続する。
15. adapter activeかつtype `0xBC`だけを完全な基底type `0xBB`へ置換する。
16. Item request、manager、その他のactor type、通常室内Catalogは変更しない。

第6版の再開後、Item `0x2EA3`「0のランプ」と `0x2E78`「12つぶのぶどう」は3D表示された。
両者ともrecord family 1/type `0xBC`で、基底`0xBB`置換でもItem requestからモデルを正しく
読めることを実機確認した。次のItem `0x2C89`「1UPキノコ」はrecord `0x3300FA8E`、family 3、
type `0xBD`だった。生成objectのprimary vptrも `0x7B1430`で、`vptr+8=0xE1A04000`により
同型のSIGSEGVになった。従って問題はAcFtrLoopだけでなく、このlate outdoor previewで
特殊家具actorをgeneric UiScreen childとして生成する契約全般にある。

第7版は14～16を次のように一般化する。

17. adapter activeかつ `CatalogPreview_UpdateActor`のopen callだけを対象にする。
18. family table由来の特殊家具type `0xBC..0xEB`を基底`0xBB`へ置換する。
19. family 0の`0xBB`、範囲外type、Item request、通常の室内/field actor生成は変更しない。

停止中のtype `0xBD` actorも基底vptrでpre/create/postを完了し、create result 2、
`g_CatalogPreview={ actor=0x30C51C70, Item=0x2C89 }`へattachできた。

第5版は2回目のSIGSEGV例外停止中にprivate stateを保持して適用し、失敗actorを基底`AcFtr`の
stock破棄経路へ渡した。進行中phase 3はmap走査後へ送り、manager `+19`が`3`になるまでstep確認した。
第6版では3回目のactorを基底`AcFtr`として正常attachし、2品の3D表示を確認した。
第7版では4回目のtype `0xBD` actorも同様にattach済み。次の確認点は1UPキノコの目視表示と、
複数familyを跨ぐ連続選択である。カメラやライトの有無を最初から再調査する必要はない。

## 第7版の実機適用範囲と服カテゴリcrash

第7版で1UPキノコを含む家具は一通り3D表示された。通常家具では、派生field挙動を省いて
基底`AcFtr`へ置換してもItem requestからmodel/resourceを読み、layer 2で描画できる。

一方、壁紙・絨毯などは表示されなかった。さらに服カテゴリへ移動すると
`PC=0x317BD0` (`ModelInstance_SetRenderLayer`) でSIGSEGVになった。この関数は
`AcFtr_CreateFinalize`から呼ばれ、g3d model instanceの全entryへlayer 2を書き込む。
従って服カテゴリの失敗はactor生成入口の無効vptrではなく、model instance生成後または
生成失敗後のfinalize/layer設定にある。

服・mannequin系は専用resource/model分岐を持つため、特殊type全域を基底`0xBB`へ落とす
第7版guardが必要な派生初期化まで失わせた可能性がある。ただしcrash時のregisterとobjectを
採取していないため、これはLOW仮説である。次回は `CatalogPreview_UpdateActor`の服Item変換と
mannequin分岐、`AcFtr_CreateFinalize`から渡されるmodel instanceを静的に解析してから再実験する。

## 未解決範囲

選択中の `0x2EA3` は外部ID表では「0のランプ」。しかしworkspaceの `NCCH/romfs` は別ゲームであり、
対象ACNLの `Item/Param/Item.bin` と `Item/Model` が無い。同Itemのfamily byteは実行中recordから
`1`と確定したが、model名とremake resource有無は静的ファイルから確定できない。実行ファイル側の汎用読込・描画経路と
actor family tableは確定済みで、この不足は屋外全カテゴリで3Dが出ない説明にはならない。
