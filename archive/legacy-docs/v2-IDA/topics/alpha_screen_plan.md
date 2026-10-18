# 木の透明度・画面固定 / IDA-gpt-6-astra-D002

2026-09-20、IDA / gpt-6-astra。**木1体の透明度、移動中の画面固定、pixel位置/倍率変更、OFF復元を実機確認。** IDAから適用する試験実装であり、常用gohan.3gxへの統合はまだ行っていない。用途やメニュー構成を前提にしない。

## 実機結果

| 操作 | 結果・根拠 |
|---|---|
| world alpha 255→128→0→255 | 不透明→半透明→消失→不透明。generic{128,0,255}.png、共有材質hash不変 |
| 20秒移動 | game viewは変化、私有view/projectionのfloat32 bytesは不変、追加1200 draws。movement_comparison.json PASSとafter_movement.png |
| 原点pixel(320,180)、倍率0.6 | 右側へ縮小表示。float32検算(320.0000001721932,179.9999993471087)、screen_placed.png |
| 同位置でalpha128 | 背景が透け、位置/大きさは維持。screen_alpha128.png |
| OFF | 木が消えcounter1480から増えない。入口NOP・材質/vtable復元。screen_off.png、final_restored_state.json PASS |

20秒試験は持ち物を閉じる時間を含む利用者操作。他は1500ms自動Suspend。画像は非前面Chokistreamの対象HWNDをPrintWindowで取得し実見。Image Sequenceとの直接比較は未実施。
根拠ルート: `work/evidence/models3d/alpha_screen_20260920/`。初回alphaはここ、修正版と移動以降は `reboot1/`。

## 透明度（IDA-gpt-6-astra-F002、HIGH）

- `0x4ADD44(out8,Material*,Allocator*,mask)` にmask `0x800` を渡し、専用heapへ728Bのcopyを生成。caller/callee assemblyで4レジスタ引数、stack/VFP入力なしを照合。out={pointer,0}、fragment block一致、cache key+720=0を確認。
- 共有ResMaterialを変更せず、Material+80をcopyへ向ける。generic Activate `0x49C08C` → `0x49CA24` がcopy+280..+360を使う。**木のSimpleMaterialActivator `0x4A17B8` はMaterial+8しか使わず、source変更だけでは効かなかった。**
- scratch+0x110に元RTTIとvtable4slotを複製し、この木のslot3だけgenericへ変更。genericはthis(R0)を参照せずR1=context/R2=Material、destructor等の元slotを保持。
- alpha255は元fragop。alpha<255はconstant-alpha/one-minus-constant-alpha RGB blend、depth write OFF、framebuffer read ON。元alpha test/TEVを保ち葉の切抜きを維持。PICA配置はassemblyとcitro3d/libctru定義を照合。既存source alphaの一般的な乗算ではない。
- OFFでMaterial+80とactivator vtableを元へ。copyはMaterial本来の破棄配列へ登録せず専用heap内に保持し、GPU終了未検証のままfreeしない。

実装 `tools/models3d/tree_alpha.py`。元bytes/owner/停止/BP/pendingを確認し、独立読戻しを必須化。共有SHA-256は前後とも `ae65cc8056f102b3a183bc827cebcaf2c79d9ea7a626d50610c8efcfafe0fdd2`。

## 画面固定（IDA-gpt-6-astra-F003、HIGH）

- Render_DrawSceneIndexedの記録list replay直後NOP `0x4EF1B0` に専用pass。world submitはOFF。list内部の切替案は右目replayへ左目camera復元を流すため却下。
- 保存R10がscene0、屋外、owner一致の時だけ描画。DrawMeshのR0は **[0x94CA48]のwrapper**。wrapper+8==[0x94CA44]、low context+40==[0x94CA58]もguardする。
- `0x494D3C(lowContext,privateSource,1)` → `0x48D26C(wrapper,mesh,node)` → `0x494D3C(lowContext,元camera,1)`。material/model cacheを失効してこの木をbindし、各eyeの実camera行列を復元。global camera本体には書かない。
- private sourceは完全camera objectではなく、CameraBindが読むview+328/48Bとprojection+424/64B。全50命令を確認。初回に捕獲して固定、比較用game行列は別欄へ毎回保存。
- core R0–R12/LR、PSR flags/GE、D0–D15/FPSCRを保存、SP192Bで8B整列。全480BのLDR/分岐/定数境界/領域重複、正常/無効/owner・context不一致等10ケースのARM監査PASS後に適用。実測command span7120B。
- `tree_screen.place(x,y,zoom)` は原点を上画面pixelで指定。LCD回転によりx=200*(1-clip.y/w)、y=120*(1-clip.x/w)。projection先頭2行だけを変更しclip z/wを保持。float32へ丸めた到達pixelを**書込み前**に計算確認。

実装 `tree_screen.py`、生成/監査 `build_screen_hook.py`。適用binary SHA-256 `9615f12da641a5fea12a96b8043cbae64dbe884b117b41e0d0e1bb6cfbc3c44d`。

## 失敗と訂正

初版はDrawMesh R0へ別物のscene renderer [0x94CA40]を渡し、PC0x495948でSIGSEGV。正しいcaller0x4EBA2Cと実機chainで[0x94CA48]と確定。fault registers/stack/memoryを保存し、入口と材質だけ復元、PCを強制復帰せず利用者が再起動した。初版の模擬contextも同じ誤認を含み、監査PASSだけでは契約を証明できなかった。
修正版は3つのglobalを区別して誤ったglobalへ無効値を置く検査と実機guardを追加。新bootで資源/割当を再生成して正常表示・移動確認を完了。旧bootのscreen_fault.json、fault_*.bin、ida_warning.pngを保存。

移動比較の初回falseはruntime tupleとJSON listの型違い。両JSONのfloat32 bytesで不変を確認し、snapshot返値もlistに統一。実機行列を書き直した修正ではない。

## 制限・次の工程

上画面・屋外・木1種類の最小試験。overlayは深度テスト/書込みOFF。自己遮蔽用depth buffer、透明面ソート、独立照明、任意材質のalpha乗算、下画面/UI最前面、実機左右目の個別画像比較は未完了。資源解放前の停止、GPU参照終了後の破棄、場面遷移、OOMを詰めてから常用3gxへ移す。

現在Suspend、screen/world入口と材質/vtable復元済み。scratch/heap/caveは保持、未解放。work/STATE.mdとactive_session.jsonを読み、再起動後に旧pointerを使わない。最新指示でcommit/push/XML出力は行わず解析を優先。
