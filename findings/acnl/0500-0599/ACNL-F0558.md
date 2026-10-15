---
id: ACNL-F0558
aliases:
- IDA-unknown-F024
- V2-F024
title: 描画順は静的に確定できる。描画状態は bcres の PICA コマンド列にある（2026-09-18、MEDIUM）
summary: 利用者の見立て「描画順は静的解析で確認できるはず」は正しかった。(1) **描画順＝マテリアルのレイヤー**。Scene_DrawLayers 0x4EB840 は外側で i=0..3 を回し、メッシュごとに material→(+8 の元 ResMaterial)+32 の下位バイトが i と一致するときだけ sub_48D26C 0x48D26C で GPU コマンドを積む（FuncNode は i==0 で node[82]、i==1 で node[83] のコールバッ
date: '2026-09-18'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5158976
- 4772460
- 1798288
- 2257588
- 2257604
- 2257628
- 2257616
- 5159956
- 5178112
- 5168244
- 5168080
- 5168280
- 5675936
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:4235-4238
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0550"]
---
## IDA-unknown-F024: 描画順は静的に確定できる。描画状態は bcres の PICA コマンド列にある（2026-09-18、MEDIUM）

利用者の見立て「描画順は静的解析で確認できるはず」は正しかった。(1) **描画順＝マテリアルのレイヤー**。Scene_DrawLayers 0x4EB840 は外側で i=0..3 を回し、メッシュごとに material→(+8 の元 ResMaterial)+32 の下位バイトが i と一致するときだけ sub_48D26C 0x48D26C で GPU コマンドを積む（FuncNode は i==0 で node[82]、i==1 で node[83] のコールバック）。**同一レイヤー内は配列 #0 の並び順＝Scene_SubmitNode で積んだ順**で並べ替えは無い。romfs 全体（bcres 1,907 ファイル / 名前つきマテリアル 2,577 個、tools/models3d/dump_material_state.py --survey）でレイヤーは 0:2160・1:401・2:4・3:12 に分布し、完全不透明（ONE/ZERO）の割合はレイヤー0 が 1839/2160=85%、レイヤー1 は 27/401=7%、レイヤー2 は 0（フェード）、レイヤー3 も 0（レンズフレア、全部 SRC_A+ONE の加算）。**m_UnitCursor はレイヤー 1** なので不透明ジオメトリの後に描かれる。(2) **描画状態はコード側に無い**。sub_48D26C の末尾 Mem_CopyBytes(g_GpuCmdPtr, mesh+0x68, mesh+0x6C) が MTOB に焼かれた PICA コマンド列をそのまま GPU へ流すので、romfs を読めば確定できる。m_UnitCursor は 0x0100=0x00E40100(blend_mode=1) / **0x0101=0x01160000＝RGB は src*SRC_ALPHA + dst*ONE の加算合成**、A は src*ONE+dst*ZERO / 0x0104=0x10（アルファテスト無効）/ 0x0105・0x0106 ステンシル無効 / **0x0107=0x41＝深度テスト有効・LESS**（byte mask=1 なので深度書き込みビットは書き換えず直前の状態を引き継ぐ）。よって「地面に埋まる部分は隠れる」「地面より明るく光る（黒は透明）」「影マップ（シーン番号2）に積まなければ影は落ちない」までが静的に言える。残る実機項目は見た目の現物確認と、同一平面に置いたときの Z ファイトだけ。(3) **前提の訂正**: 設計書 §3.1 の「上画面パス(1024)と右目/下画面パス(1040)の両方に出る」は誤り。Frame_DrawPass1025 0x1B7090（display 0x401＝下画面）は ssys_ma_lyt_LayoutMgr_RenderBottom しか呼ばず **Render_DrawScene0/1 を呼ばない**。1024=0x400 上画面左目、1040=0x410 上画面右目（旧 F-253 の実測 0x400→0x410→0x401 と一致）。正しくは「番号 0 に積めば上画面の左右両目に出る。下画面には出ない」。Render_FrameEnd は右目パス末尾なので 1 フレームに 1 回・左目パスより前に submit すれば足りる。(4) **アニメ API**（呼び出し元 sub_227020 0x2272B4/0x2272C4/0x2272DC/0x2272D0 で連続して呼ばれる順）: 0x4EBC14 資源に結び付けて作る（内部で Heap_CreateNamed_0 が名前 "MaterialAnim::build" のヒープを作り sub_566700 で縮める。失敗時 0）→ 0x4F0300 スロットへ割り当て（node[82] 非0 のときだけ node[10] の表の [slot + node[83]*行長] へ *(anim+8) を書く。範囲外は黙って無視）→ 0x4EDC74 float を 1 つ設定（**VFP s0 渡し**、内部オブジェクト +64）→ 0x4EDBD0 評価モード選択（0/1 で sub_4D3EFC / sub_4D3E70、どちらでも anim+4 に保存）→ 0x4EDC98 フレーム確定（+76 の関数を +80 で呼び、+60=+56、+56=+68、+88=1。常に 1 を返す）。UnitCursor のアニメ 3 本は **全部 MaterialAnimation**（UnitCursor ループ150 / UnitCursorNG ループ150 / UnitCursorRotate ワンタイム3）で、"MaterialAnim::build" と整合する。(5) **ヒープ量**: sub_736158 の第9引数=1 の問い合わせ経路を Unicorn で回すと UnitCursor（マスク 0x834・個数 3）は **3,064 B**（最大アライン 32）。同じ道具で木 fg_treeA_4 のマスク0=932 / マスク0x10=1664 を再現でき、IDA-unknown-F011 の値と一致するので道具自体の検算になっている。組み立て側の payload＋アラインだけで、アロケータ諸経費・GPU/VRAM は含まない。(6) **スレッド**: FileRes_RequestLoadAsync 0x569BA0 はロックで守られたキューへ繋ぐだけでスレッドを選ばない（非同期フラグ0 なら sub_569EFC の同期経路でフレームが止まる）。反証条件: レイヤー以外に並べ替えを行う経路がある、MTOB の PICA コマンドが実行時に書き換えられる、Frame_DrawPass1025 から 3D シーンが描かれる経路がある。根拠 docs/topics/unit_cursor_outdoor.md §3.1/§10、work/evidence/unit_cursor/material_state.txt、tools/models3d/dump_material_state.py、tools/models3d/query_model_size.py、tools/bcres_anim_dump.py。

