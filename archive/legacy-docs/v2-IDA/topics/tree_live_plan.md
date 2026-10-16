# 木モデル最小実機試験 / IDA-gpt-6-astra-D001

目的: 既に準備済みのSeason資源 fg_treeA_4 を独立instanceとして指定world座標へ表示する。島/セーブの設置データは変更しない。画面固定と種類一般化は後続。
承認: 2026-09-19利用者の設計→検証→実装→検査/逆アセンブル→適用。実機停止確認済み。

## 結果（2026-09-20 / IDA-gpt-6-astra-F001）

**木1体の表示とOFFでの消去に成功。** 半分の大きさでplayer右36の位置。`work/evidence/models3d/live_20260919/curved_enabled.png` と `curved_disabled.png`。非前面Chokistream画像を実見し、実行counterと行列も照合した。Image Sequenceとの直接比較は未実施。

| 版 | 変更 | 画面 | counter |
|---|---|---|---|
| raw | playerのゲームxyzをそのままmatrixへ | 木は見えない | 46 |
| curved | 座標変換＋X傾き、資源/hook/倍率は同じ | 木が見える | 92 |
| OFF | enable=0 | 木が消える | 92 |
| 別位置・等倍 | 同じnodeをplayer左48・Z+32へ、倍率1.0 | 左手前に等倍の木 | 139 |
| 再OFF | hook元NOPへ復元 | 木が消える | 139 |

追加試験は `tree_pose.py` の段階的APIで実施。`second_enabled.png` / `second_disabled.png` と `pose_second_observed.json`。同じnodeの行列を変更したため、再生成/追加確保なしで位置と倍率を変更できた。最終値は `final_live_state.json`。

0x590034の正常経路は `0x52CDD8(out_xyz, game_xyz)` → `0x56689C(matrix, returned_angle)` → `0x4ED794(holder,matrix)` → `0x4ECFEC(holder)`。曲面用のY/Zは通常の平面上のゲーム座標とは異なる。行列へのコピー成功だけでは座標解釈を証明できない。独立float32計算は `python tools/models3d/verify_curved_pose.py` で全値一致。

最終状態: hook0x1B721Cは元NOP、enable0、ACNL Suspend、BP0、未完了callなし。scratch/専用heap/nodeは保持。OFFは解放ではない。割当台帳 `tree_state.json` はこのboot専用。再起動を跨いで実行しない。

### 継続操作の入口

- `gui_file.py` はlocalhost GUI MCPの1回のみの要求。書込みタイムアウト時は再送せず `pending_call.json` と実機PC/SP/TIDを読み取る。
- `tree_live.py` のimportは実機を変更しない。`park()` → 別要求で `finish_park()`、`begin_call(...)` → 別要求で `finish_call()`。異常停止は自動でPCを戻さない。
- 生成済みの同一bootでの位置変更: `tree_live.park()` → 別要求で `finish_park()` → `tree_pose.begin(x,y,z,scale)` → **停止を確認しながら別要求で `tree_pose.finish()` を4回** → `tree_pose.show()`。ON/OFFの画像を保存し、終わったら `tree_pose.hide()` → `tree_live.timed()` → 停止を再確認。途中の戻り未確認では次の呼出しを再送しない。`hide()`はfreeもResumeもしない。
- 表示hook本体は `display.bin`、入口4Bは `display_hook.bin`。`display_audit.json` のhashは本体に対するもの。取り違えた照合は一度失敗し、適用せず正しい対象で再検査した。
- 成功・失敗を含む全操作は `events.jsonl`。再現時に今回bootの絶対heapアドレスをそのまま使わず、資源同定/空き領域/確保からやり直す。
- `gui_read_resource.py` は元paddingを保存する初回専用。現在の台帳を上書きして再実行しない。

### 常用実装前に残ること

1. fgobj owner解放前にsubmit停止・instance破棄する。globalポインタの事後pollだけでは間に合わない。
2. GPUが参照する領域/終了条件を確認してheapを返す。待ち時間だけで安全としない。
3. 別位置/倍率は2条件で成功。追加回転/場面遷移、OOM、再生成を検証する。画面固定cameraは別試験。
4. ここまでの試験コードをgohanへそのまま常駐移植せず、生成/更新/終了を描画スレッドへ依頼する状態機械にする。既存Gui/Shizueのhookとcave台帳を衝突させない。

## 前提と失敗時
- 現boot: resource_snapshot.json。fg manager=0x3310DAD8 / resource=0x30C91F00 / model=0x30CADEC0。全て操作直前に再照合する。
- resource辞書とmodelヘッダ独立照合、type0x40000012/mesh1/material1。ordinary ModelでありSkeletalModel末尾+0x228は存在しない。
- 元コード32bytes×6地点一致。text末尾[0x838018,0x839000)は全0、getmemregionsでr-x。
- 固定heapアドレスの再利用禁止。既存unitcursor stateは使わない。
- 実機へのgame callはFrame_DrawPass1024の0x1B721Cで停止して行う。自動Suspendを先に予約し別要求で正常returnを確認。異常停止ならレジスタ/PCを強制復帰させない。
- ARM32/T=0、SP8整列。R0-R12/SP/LR/PC/PSRを保存、D0-D15/FPSCRは実行するARM wrapper自体で保存/復元する（GDBの0埋め値に依存しない）。
- wrapperの全命令/BLX先/分岐/stack、現boot使用範囲を監査。元bytesを保存。書込み→flushcaches→独立読戻し。
- Lumaのgetmemregionsはpacket容量で途中まで。未表示のheap/stackをマップ済みと断定せず、必要範囲の読出し成功とconvertvatopaで追加確認。

## 段階
1. BPでpark（1500ms停止予約、失敗なら呼出ししない）。
2. 無引数Room_GetCurrentIdでcall/復元の往復だけ検証。
3. lyt Alloc(size0x200,align32)でscratch。専用HeapAllocator_ctor、Heap_CreateNamed_0(size0x20000,parent=[0x94CC48],SafeString,1,0)。
4. 戻り値1 AND heap非0。既存heapにctorを再実行しない。余裕のある専用heapからordinary Modelを生成。資源は既存Seasonを借用。
5. holder ctor→ModelInstance_Create(holder,model,allocator,allocator,0,0,1)。return1/holder+4非0/Model vtable/MaterialActivator非0/mesh1/全cmd pointerを検査。
6. player付近の座標を設定→UpdateWorldAndSkeletonでlocal/world双方を読戻す。
7. 検査済みのsubmit hookを0x1B721Cへ適用。R0-R12/LR/PSR/D0-D15/FPSCRを保存し、scene0へ1instanceだけsubmit。manager/resource一致guard、enableとframe counterはscratch。
8. Chokistream前後を保存しtimed Resume→停止再確認→PNG実見とframe counter照合。
9. 問題時は停止したまま。正常時にenable0→hook元bytes復元。GPU完了を未確認のままheapを解放しない。保持領域/復元操作をboot台帳に残す。

heap解放と屋外遷移時の寿命管理が未確定のまま常用3gxにしない。最初の実験は短時間・1instance。


## pose修正の事前検査 / 2026-09-20
stock 0x590034 assemblyから0x52CDD8(out_xyz,in_xyz)と0x56689C(matrix,u16angle)を追加。前者はR0/R1のみ、後者もR0/R1のみ、stack引数なし。calleeのVFP入力なし、既存guardで全VFP/FPSCR保護。0x60BB94は曲面係数singletonを返し、0x75CAB4が半径/角度からxyzを出力する。scratch+0xC0に12B入力、+0xD0に12B出力（matrix+0x80の48Bと非重複、scratch0x200以内）。実行前に原本関数bytes照合、guard/hookのhash照合、pendingなしを確認する。元hookは外してからpark。
