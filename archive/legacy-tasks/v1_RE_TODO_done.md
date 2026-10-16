# RE_TODO.md — 完了済み項目

原本の完了表記を保持した抜粋。出所の行番号は各見出しに記す。

<!-- source line 3 -->
## 2026-09-12 GitHub転送タスク完了

main/IDA/Ghidraを作成し、指定6フォルダ全件のIDAへの送信・照合完了。Ghidraは将来の解析資料/プロジェクト待ちで今回の転送漏れではない。再開時は [GITHUB_UPLOAD.md](../project_v2/work/GITHUB_UPLOAD.md) の完了記録を読み、初回の認証失敗や送信中メモを再実行しない。


<!-- source line 7 -->
## 2026-09-12 チャット漢字候補：実装・ビルド・PC検証完了

次は新しいgohanの最小実機確認（普通チャットで「かんじ」→自前メニュー「チャット漢字候補」→一覧/取消/再実行、既存UIとしずえ遷移）。まだ適用/Resumeしていない。作業開始前にboot・現行プラグイン・停止状態を取り直す。[手順と復元先](../project_v2/docs/topics/chat_kanji.md)。


<!-- source line 11 -->
## 2026-09-11 環境整備タスク完了

次回は [project_v2/work/STATE.md](../project_v2/work/STATE.md) → [SKILLS.md](../project_v2/SKILLS.md)。内蔵変換研究の残る課題は [keyboard.md](../project_v2/docs/topics/keyboard.md)。以下の古い準備記録を未完了タスクとして再実行しない。


<!-- source line 15 -->
## F-407 実機成功: キーボード非起動で候補17/6/143件を取得（2026-09-11、最新・HIGH）

利用者がF407を配置・ACNL再起動/再アタッチ。Suspend/bp0、実機headerと全生成コードアンカー、成果物/現行ソースhashを照合した。要求2の展開・辞書配置・315再配置が成功し全解放された後、要求3で「かんじ」「わたしはねこがすきです」「か」を各1回実行。候補17/6/143件が原本PCと全順位一致。前2入力は保存済み実機SWKBD候補列とも直接一致。「か」は初回50件からgetterが143件まで追加検索し、終端0を確認した。

各要求は既存検証用3gxの独立スレッドで実行。キーボード起動/APTなし、辞書・元codeは内蔵タイトルからRAMへRead、SD/3gxへのリソース同梱なし。内蔵FSのOpen/Size/全Read/CRC/Close/Releaseすべて成功、5 MiB arenaのFree完了。変換3要求はstage10/state2/failure0、prepared1/executed1/exhausted1/stack_guard1/freed1。arenaは各回0x061BE000。各5000ms走行後の観測であり、変換時間そのものの測定ではない。

結果はSYSTEM_KEYBOARD/evidence/f407_engine/hardware_prepare.json、hardware_kanji.json、hardware_phrase.json、hardware_ka.jsonへ個別保存。report全34452 bytesを別の実機読取りで保存し143候補を独立に再デコードして一致。hardware_verified.json、hardware_final_report.bin、hardware_final_state.json参照。ソース・3gx/ELF・検証器・実機証拠をBACKUP/plugin_f407_hardware_confirmedへ保存。

最終ACNL Suspend(-1)、PC0x0056085C、bp0、command0。実機はF407版（SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385、exe258048/heap10227712）、report0x07033AE0、command0x07033ADC、input0x0703212C。試験arena/FS handle保持なし。F407はゲームコードをフックしないため、この試験で追加した復元待ちフックなし。F406の一時変更は前bootで復元済み。正常gohan/F404ファイルも不変。

詳細DOCS/system_keyboard_native_loader.mdとPlugin/SwkbdEngineProbe/README.md。今後追加試験するならengine_probe_live_f407.pyの既定inspectから現在値を確認し、要求を1回だけ設定してrun_timed.pyで走らせる。自前メニュー統合を前提にしない。

残る未確認事項: 個人学習/ユーザー辞書、長文上限や全入力、明示的な文節境界指定APIの実機試験、並行呼出し、ロードと変換の処理時間内訳。今回の文章6候補取得を、文節境界編集APIまで確認したものとは扱わない。キーボード非起動・実機内蔵資源の取得・再配置・独立contextの予測候補列挙という今回の経路は成功済み。以下は準備時点と過去の履歴。


<!-- source line 39 -->
## F-406 実機ヒープコード実行成功・全復元済み（2026-09-11、最新）

F-405の停止はユーザー提供dumpでカーネルのD-cache clean by MVAに確定。F-406では全体cache SVC 0x92/0x94へ変更し、組立前ソース検査・全4リテラル/1分岐・4条件ABI試験・実機の領域/アンカー照合後に1回だけ実行した。plugin heap 0x061BE000の2命令から0x5Aが返り、control phase4を確認（HIGH）。後続の5 MiB全域照合、内蔵辞書/code全Read/CRC/Close/Release/freeもstate2/failure0で成功。これは最小コードの実行成功であり、変換エンジン本体/VFP/実機候補取得は未検証。

結果をSYSTEM_KEYBOARD/evidence/f406_exec/hardware_result.jsonへ保存後、vtable slot0x07029DD8を0x070012B8へ復元。cave0x00838600の予約全0x200 bytes、control0x009BE840の全0x20 bytesはbackup一致。別の読取りでもゼロ/元vtable/command0を確認しrestored.jsonへ保存。最終ACNL Suspend(-1)、ARM32、PSR0x20000010、PC0x00463E24、SP0x32283B98、bp0。map APIの空リストは未マップ判定に使わない。試験buffer/handles保持なし。F-396 launcherは再起動後に未再適用。

現行の実機プラグインと3gxファイルは独立Plugin/SwkbdProbeのF-404版。gohan正常版は変更なし。次は内蔵取得codeのRAM展開/再配置・辞書context初期化・実機候補照合。辞書やcodeのSD/3gxリソース同梱、自前メニュー統合はしない。詳細DOCS/system_keyboard_plugin_probe.md。


<!-- source line 47 -->
## F-405 解決: キャッシュ処理中のクラッシュ、再起動で一時変更解除

Plugin/crash_dump_00000004.dmpのPC0xFFF2B3F8はMCR p15,0,R1,c7,c10,1。R1=FAR=0x061BE000が試験arenaと一致し、DFSR0x805はsection translation fault/write。ARM11 core1、SVC mode、保存プロセスsocket/TID0x0004013000002E02。ダンプ解析とidalibの保存命令列を照合（HIGH）。他コアの異なるアドレス空間が原因というdispatch仮説はLOW、svc0x91/0x93のどちらかは不明。ユーザー再起動後に旧cave/controlゼロ、元vtable、mailbox idleを確認した。F-405を再実行しない。以前の「結果未回収」は解消済み。pending_state.jsonに解決を記録し、旧記録はpending_state_before_resolution.jsonに保存。

### 残る検証

- RAM上の圧縮.code展開をctrtoolの既存出力と全bytes照合する。原本版と315語の再配置表の整合を確認し、想定外の版は実行前に止める。
- 内蔵RomFSの構造から6辞書を切り出す。既知offsetへの決め打ちを本番の解析器にしない。独立context、領域境界、入出力長を検証する。
- 原本関数の引数、stack/VFPの保存とスタック容量を確かめ、まず1入力で候補列を取得する。PCでの原本実行と保存実機候補を独立比較に使う。
- 解放・復帰・処理時間を実測した後に入力数を増やす。F-406の2命令成功をエンジン全経路や全入力の保証にしない。


<!-- source line 58 -->
## F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11）

利用者が独立swkbd_probe.3gxを配置しACNLを再起動。新規header/生成コードアンカーを照合、Suspend/bp0を確認してmailboxに1要求を設定。5秒の自動Suspend付きResume後、state2/failure0。5,242,880 bytesを確保して全域write/readback成功、内蔵辞書2,045,891 bytesと圧縮.code 471,668 bytesのOpen/GetSize/全体Read/CRC32一致/Close/handle解放がすべて成功。buffer free完了、ログ書出しも成功。現在Suspend/PC0x00137064、command0、試験buffer保持なし。hardware_result.jsonを保存。3gx側で予定の検証容量を確保できた。エンジン本体はまだ実行していない。次は展開・再配置・実行権限と実機候補取得。詳細DOCS/system_keyboard_plugin_probe.md。



<!-- source line 63 -->
## F-403完了・F-404 3gx検証へ移行（2026-09-11）

最新はDOCS/system_keyboard_plugin_probe.md。全辞書2,045,891 bytesの実機取得と全bytes/SHA照合、6辞書個別照合が完了。一時handle/buffer/wrapperは全復元済み。エンジン実機実行は未実施。
System/lyt heapの空きは小さいが、全heapの調査は未完。利用者の指定で3gx側メモリを検証する。現行pluginの総枠5 MiBは実機headerと一致、Lumaは10 MiB設定に対応。独立のPlugin/SwkbdProbeで5 MiBの一時確保・内蔵FS読取り・全解放を検証予定。10 MiBの実機確保は未確認。辞書SD/3gx同梱や自前メニュー統合はしない。gohan正常版を維持。最終読取りstate=-1/PC0x0014E378。



<!-- source line 92 -->
## 最新 F-400: 再配置のPC試験成功・テーブル同梱を避ける方針

利用者はSD/3gxへテーブルをリソース同梱する方式を避けたいと指定。
内蔵辞書RomFSとSWKBD ExeFS .codeを実行時にRAMへ読む方式を候補とし、実機権限は未検証。
52箇所の観測絶対参照を全件idalib xrefで照合。callback3個と合わせ移設し、
元VAをunmapして0x04100000/0x06100000から候補列が一致。未修正コピーは旧19094Cで停止。
これはPCでの再配置可能性の確認。全経路閉包/学習/異なる版の対応は未完。
DOCS/system_keyboard_relocation.md、probe_relocated_engine.pyとf400証拠JSON参照。
今回実機アクセス/ビルド/SD/3gx変更なし。次は全参照の静的網羅と内蔵タイトル読取り権限の確認。



<!-- source line 114 -->
## 最新 F-398: PC候補取得完了

- [x] 関数型辞書slot7..9の初期化を特定、実機保存値と照合。
- [x] かんじ17件・文章6件をPCのみで順序込み再現。
- [x] 初期50件を超える追加列挙、取得API、検証器と文書を保存。
- [ ] 個人学習/ユーザー辞書の候補順位への影響を再現。
- [ ] 3DS上でアプレットを起動しない候補取得の初期化・実行環境を調査。

F-397の表記候補追加箇所調査は解決。差はUI段階ではなくPC側の未登録辞書だった。



<!-- source line 125 -->
## 最新 F-397: 今回の未確定入力から候補・文節取得完了

- [x] 新しいswkbd PID50を列挙して確認、停止取得、コード/各領域一致、detach成功。
- [x] 「わたしはねこがすきです」の全6候補の順序を保存。
- [x] 内部文節「わたしは/ねこが/すきです」を原本読みdecoderと独立PC結果で照合。
- [x] mode1文節領域が空でも別の予測内部リストに結果があることを文書化。
- [ ] 別入力でも内部リストとUI対象範囲を比較し、境界変更後の更新条件を検証。
- [ ] 原本wrapper直後1件→実機UI6件となる表記候補追加箇所を特定。

今回の指定入力について、変換ボタン確認や追加の実機操作は不要になった。
現在ACNLはSuspend、SWKBDは取得後detach済み。詳細DOCS/system_keyboard_prediction_segments.md。


<!-- source line 144 -->
## 最新 F-396: 通常チャット用ランチャー移設・再適用完了

- [x] 再起動後の停止/元命令/空き領域確認。旧ケーブとGUI v2の重複を検出。
- [x] SWKBDだけ0x00838200へ移設。ビルド前後検証・実機監査・適用・独立読み戻しPASS。
- [x] F-394正常3gxとGUI/しずえhookの不変確認。Suspendを保持。
- [ ] Resumeして通常チャットから移設版の起動を確認。
- [ ] 「わたしはねこがすきです」未確定時と変換操作後をSWKBD側で取得し、F-395のmode/editor範囲を比較。

旧0x00838D20を使う保存済みスクリプトは実行しない。現行版とmanifestを使う。


<!-- source line 277 -->
## ~~TODO-124: 色（RGB）の帰属を確定する~~ — **完了**（F-187 / F-189 / F-190）

**達成。** 位置・大きさ・色・アルファのすべてを自前で制御できる。
実装は **`PATCHES/cave_add_sprite2.py`**。

原因は 2 つだった。

1. **相乗り先のバッチを間違えていた。** `+37 = 3` は色を持たないバッチ。
   色を使うなら **`+37 = 7`**（行列 0..2 ＋ 色 3..6）のバッチに乗る
2. **アンカー（基準点）を直していなかった。** 幾何エントリの後ろ 2 ワードは
   中央揃えなら `(-幅/2, +高さ/2)`。幅・高さだけ変えると画面外へ飛ぶ

---


<!-- source line 291 -->
## ~~TODO-125: 自前テクスチャで「絵」を出す~~ — **完了**（F-191）

**達成。** 自前バッファのテクスチャが GPU に読まれ、タイリング込みで絵が出せる。

原因は **`reg 0x083`（ラップ・フィルタ・テクスチャ種別）を上書きしていなかった**こと。
`0x082` / `0x085` / `0x08E` の 3 つだけでは足りず、相乗り先の
64x64 ETC1 用パラメータが残って縞模様になっていた。

**必要な 4 レジスタ:**

```
reg 0x082 = 高さ<<16 | 幅
reg 0x083 = 0        （bit1 拡大 / bit2 縮小フィルタ。0 = ニアレストでくっきり）
reg 0x085 = PA >> 3  （リニア FCRAM なら PA = VA - 0x10000000）
reg 0x08E = 形式     （0=RGBA8, 9=LA4, 12=ETC1 …）
```

---


<!-- source line 310 -->
## ~~TODO-126: 自前スプライトだけ別のテクスチャにする~~ — **完了**（F-192 / F-193）

**達成。** 実装は **`PATCHES/cave_own_batch.py`**。
`DrawCtx_FlushBatch` をラッパで包んで 2 回呼び、自前スプライトを独立したバッチにする。
**ゲームの描画には一切影響しない。**

踏んだ落とし穴 2 つ:

1. **素通り経路で `R1`（cursor）を壊して SIGSEGV**（`DOCS/crash_recovery.md`）。
   判定は `R6` と `R12` だけで行う
2. **フラッシュが配列の `[0].w0` をヘッダで潰す**（F-192）。
   2 回目の前に「配列ポインタ − 4」から復元する


<!-- source line 323 -->
## ~~TODO-127: SD 画像 / ビットマップフォント~~ — **完了**（F-194 / F-195）

**達成。** 実装は **`PATCHES/cave_draw_sprites.py`**。
64x64 の LA4 アトラスに 8x8 グリフを並べ、UV で 1 文字ずつ切り出して
4 枚のスプライトとして「ACNL」を地図の上に描画した。

**★描画順は「フレーム内で何回目のフラッシュか」で決まる**（1 フレーム約 42 回）。
最後のフラッシュで描けば最前面になる。

---


<!-- source line 347 -->
## ~~TODO-129: 8 枚を超えるスプライトを描く~~ — **完了**（F-198）

**達成。** 「ACNL GUI OK」11 文字を 2 チャンクで描画。

**最後のチャンクを大きさ 0 のダミーで埋めて全チャンクを 7 枚にそろえる**と、
カウンタも索引も定数のままで外側ループを 1 つ足すだけで済む。

あわせて見た目を壊していた **4 つの独立した原因**を潰した（F-198）。
特に **相乗り先の縮尺（0.5）** と **整数倍でない拡大率** はドット絵に必須の条件。

---


<!-- source line 359 -->
## TODO-131: 描画順を安定させる — ★★★★★**完了**（F-203 〜 F-212）

`PATCHES/cave_draw_topmost.py`。**常に最前面に描かれ、メニュー開閉でも順序が変わらない。**
線幅は均一、ノイズなし。実機で確認済み。

### 効いた注入点

**下画面のパス（`Frame_DrawPass1040`）で最後に再生されるレイアウト
（リスト id 15）の「記録本体の直後」= `0x568770` の NOP。**

### 途中でつまずいた 6 点（すべて F- 番号あり）

| 症状 | 原因 | 対策 |
|---|---|---|
| 発火 0 回 | 記録要求フラグが立っていないと記録が走らない | 入口でフラグを立てる（F-204） |
| 上画面に出た | 「最後に再生」は画面ごとに違う | パスごとに測り直す（F-205） |
| 直前のボタンの色になる | マテリアルを自前で積んでいない | `Material_EmitState` を自分で呼ぶ（F-206） |
| テクスチャ全面が貼られる | `drawctx+1692` が 0 で UV が読まれない | 1 にする（F-207） |
| 半端な拡大・ノイズ | レイアウトごとに投影が違う | 縮尺を測り直す（F-208） |
| フックを外しても残像 | 記録済みリストは記録し直すまで残る | フラグを 1 回立てて掃除（F-204） |

### ★その後に見つかって直した 3 点（F-210 〜 F-212）

| 症状 | 原因 | 対策 |
|---|---|---|
| セーブ確認ウィンドウで消える | リスト id を固定で狙っていた | **実行時に追いかける**（F-210） |
| 同上（真因） | マテリアルを「たまたま」で選んでいた | **条件で選ぶ**（F-211） |
| たまに別の色を拾う | 借りたマテリアルが定数色を持っていた（`P_crsl_00`） | **定数色が中立のものだけ選ぶ**（F-212） |

実機で確認済み: **常に真っ白、常に最前面。** どんな場面でも消えない。

### 残っている未確認事項

- 追いかける対象が 1 つも見つからない場面があるか（そのときは前フレームの値を保持する）
- マテリアルの定数色は `+0x10 / +0x14 / +0x18` の 3 つしか見ていない。
  `+0x1C 〜 +0x2C` も色なので、色付きを取りこぼす可能性は残る

---


<!-- source line 456 -->
## TODO-130: CTRPF プラグインへ移植する — ★★★★★**完了**（F-213 〜 F-217）

`Plugin/CTRPluginFramework-BlankTemplate-0.8.0/Sources/OwnGui.cpp`。
メニュー項目「自前 GUI を最前面に描く」を ON にすると組み込み、OFF で素に戻す。

### できていること

- `cave_draw_topmost.py` の `MODE = "export"` が `includes/GuiCaves.h` を吐く
- **書き出したバイト列が実機のものと一致することを確認済み（不一致 0）**
- 確保用ケーブを実機メモリへ置いて逆アセンブルで検証済み
  （このとき `MOV R1,#0x4000` が `0x1000` になっていた誤りを発見・修正）
- ビルド成功（`CTRPluginFramework-BlankTemplate-0.8.0.3gx`、**762,889 バイト**）
- ★テンプレートの Makefile が `.elf` をリンクし直さない誤りを修正した。
  直すまで「ビルドは通るのに .3gx が数日前のまま」だった

### 実機で 1 回クラッシュして直したこと

`svcFlushDataCacheRange`（Luma 独自 SVC）でカーネル内の書き込みフォルト。
`svcFlushProcessDataCache`（標準 SVC）へ変更した。
**このときバッファの確保（0x329D8500）は成功していた**ので、
ゲームのアロケータをプラグインから呼ぶ部分は実機で動くことが確定した。

途中経過を段階ごとに `/CTRPF_OwnGui.txt` へ書き出すようにしたので、
次にクラッシュしたら「どこまで進んだか」がファイルに残る。

### 実機で確かめること

1. SD の `/luma/plugins/00086200/` へ `.3gx` を置き、Rosalina で plugin loader を ON
2. メニューから「自前 GUI を最前面に描く」を ON
3. 「ACNL GUI OK」が下画面の最前面に出るか → **確認済み**
4. OFF で素に戻るか → **確認済み**
5. `/CTRPF_OwnGui.txt` に確保したアドレスとテクスチャ PA が出るか → **確認済み**
   （ログは `.3gx` と同じ場所に出る）
6. タイトル/ロード画面でも文字として白で出るか → **確認済み**（F-214）

### ★タイトル/ロード画面での不具合を修正（F-214）

「色つきの板」になっていた。原因は**中立なマテリアルが 1 つも無い場面がある**こと
（ロード画面では Picture 320 個中、条件 1 は 295 個、条件 1+3 は **0 個**）。
マテリアルの枠を優先/予備の 2 つに分け、予備は**定数色を一時的に中立化してから積み、
直後に戻す**ようにして解決。実機で確認済み。

### ★しずえ会話の切り替わりで消える件も修正（F-215）

中立化を **`+0x10` 〜 `+0x30` の 9 語**へ広げた（3 語では `P_soft_B` の
アルファ 0x80 と合成モード `0x6AA` が残り、白を描いても見えなかった）。

**★描画後に `Material_EmitState` を呼ぶ「後始末」は誤り。**
内部で `DrawCtx_FlushBatch` を呼ぶので、中身が確定していないバッチが流れて
モザイク状の乱れになる。実機で 1 回踏んで外した。

### ★SD からの任意画像の読み込み — **完了**（F-216 / F-217）

`PATCHES/make_gui_image.py` で PNG を `.acgx` へ変換し、
SD の `/luma/plugins/00086200/gui_image.acgx` に置けば下画面の最前面に描かれる。
無ければ埋め込みのフォントアトラスのまま動く。

**変換は PC 側でやり切る。** 3DS の GPU は 8x8 タイル + Morton 順・2 の冪しか読めず、
展開器をプラグインへ持ち込むと失敗の仕方が増えるため。
PIL は入っていないので **zlib だけで PNG を読む**。

途中で **`reg 0x082` が `(幅<<16)|高さ` だった**ことが判明した（F-216）。
64x64 の正方形しか使っていなかったので、逆に書いていても気付けなかった。

### ★実機で確かめたこと / まだのこと

| 項目 | 状態 |
|---|---|
| タイル化・転送・寸法/形式ワード・スプライト表・UV | ○ 実機で確認（`apply_gui_image.py` 経由） |
| **半透明（アルファブレンド）** | **○ 実機で確認（F-218）** |
| **プラグインが SD からファイルを読む部分** | **○ 実機で確認**（LA4 と RGBA8 の両方。F-219） |

**★CTRPF のパスはプラグインのフォルダ基準**（F-219）。
絶対パス 1 本だけ見ていたので見つからず、黙って埋め込みへ落ちていた。
候補を順に試し、どれで開けたかをログに残すよう直した。

確認するには `.acgx` を **`.3gx` と同じフォルダ**へ `gui_image.acgx` の名前で置く。
`/CTRPF_OwnGui.txt` に「画像を開いた: …」が出れば読み込み経路が通っている。

### 残り

- 起動直後に ON にすると落ちる件は **TODO-133 として保留**（対策コードは外した）
- バッファは 0x4000 バイト固定。RGBA8 なら 64x64、LA4 なら 128x128 まで。
  もっと大きな画像を扱うなら確保の大きさを増やす必要がある（未検証）

---




<!-- source line 1293 -->
## TODO-120 [★達成 / F-169] 自前テクスチャを四角形に貼る

**達成。** 自前で確保したメモリに自前で詰めた市松模様が、
自前サイズ（80x80）の四角形に貼られて表示された。

適用は `PATCHES/cave_own_texture.py`。
`(オフセット, 値)` のテーブル駆動なので、値だけ差し替えれば実験できる。


<!-- source line 1301 -->
## TODO-119 [★達成 / F-168] 自前の四角形を 1 枚描く

**達成。** 時計の分の 1 文字目を幅 40 / 高さ -40 に書き換えて拡大表示させた。
`CopyToCommandBuffer` で 2 枚目を追加する経路と、
ゲーム自身のコピーを直接書き換える経路の**両方で成立**。

適用は `PATCHES/cave_own_quad.py`（`WHICH` で 2 経路を切替）。

**★位置を動かす実験では、まず大きさだけを変えて位置は据え置くこと。**
`(X, Y)` は pane の変換行列に対する相対座標なので、大きく動かすと
画面外やシザー矩形の外に出て「描けていない」と誤診する（F-168 で実際に踏んだ）。


<!-- source line 1313 -->
## TODO-118 [★解決 / F-167] 頂点属性（regs 0x200-0x22F）

**前提が外れていた。2D の矩形に頂点属性の解析は不要。**

テキストの batch には `reg 0x200`-`0x226` が**一つも入っていない**。
グリフは**頂点シェーダの float 定数から四角形を生成**して描かれる。

```
c[0x40 + 2k]     = (u0, v0, u1, v1)        UV。0..1
c[0x40 + 2k + 1] = (幅, 高さ, X, Y)         レイアウト単位。高さは負
reg 0x228 NUMVERTICES = 6 * グリフ数
reg 0x22E DRAWELEMENTS = 1
```

解読は `scratchpad/decode_text_batch.py`。詳細は F-167。


<!-- source line 1329 -->
## TODO-117 [★解決 / F-163〜F-166] GPU 可視メモリの入手経路

**解決した。** `g_GfxAllocator->Alloc(size, 0x80)` をフック内（ゲームのスレッド上）から
呼べば、**GPU が実際に読めるメモリ**が得られる。実機で証明済み（F-166）。

```cpp
u32  alloc = *(u32 *)0x0094CA30;
u32  vt    = *(u32 *)alloc;
typedef void *(*AllocFn)(u32, u32, u32);
void *p = ((AllocFn)*(u32 *)(vt + 8))(alloc, size, 0x80);
u32   pa = (u32)p - 0x10000000;      // reg 0x085 に入れるのは pa >> 3
```

- プラグインからの `linearAlloc` / `svcControlMemory` は**カーネルが `OutOfMemory`**（F-163）
- 証明は「フォントアトラスの記述子（`table + 0x14*i + 8` = PA>>3）を
  自前バッファに向けたら時計の文字が四角になった」（F-166）
- キャッシュ flush は `svcFlushProcessDataCache(CUR_PROCESS_HANDLE, ...)`（未実測）


<!-- source line 1357 -->
## TODO-115 [★解決 / F-147 / F-171 / F-175 / F-176 / F-177] UI の有無に依らず描く

**★解決。相乗り点は `nwlyt_Pane_DrawRecursive` (`0x73B524`)。**

実測（60 秒、建物の出入り・メニュー開閉を含む、1785 フレーム）:

| 経路 | 関数 | ゼロフレーム |
|---|---|---|
| TextBox | `sub_73CF48` | 83.8% |
| Picture | `nwlyt_Picture_DrawToCommandList` (`0x73CB58`) | 3.3% |
| **Pane 走査** | **`nwlyt_Pane_DrawRecursive` (`0x73B524`)** | **0.00%** |

**1 フレームも欠けない。** ロード中の「読み込み中」画像も
Picture ではない Pane 型で描かれており、その区間も Pane は 9 枚/フレーム走る。

F-147 より、この関数は cursor を `R1` で受け取り各 Pane の draw slot(+0x68) へ渡し、
戻り `R0` を次の可視 child へ渡す。**UI command stream を伸ばす走査本体。**

**次の作業（TODO-122 へ）**: ここに相乗りして自前の四角形を 1 枚出す。
F-176 より Picture は `drawctx+1640/1644/1648` の配列に四角形を溜め、
26 個で `sub_4B8360` が一括で流す。**カウンタを 1 増やして 1 エントリ足せばよい。**


<!-- source line 1416 -->
## TODO-112 [F-147] 2D panelをlist 32へ追加する最小経路を確定する

`nw::lyt::Picture` とTextBoxはともにPane treeのcursorを伸ばし、会話layoutではlist 32へ記録後、
main list 1へreplayされる。次は `nwlyt_Picture_DrawToCommandList` (`0x73CB58`) の入口/出口cursorを
同一Pictureについて採取し、1枚のPictureが占める正確なcommand rangeと、batch flush境界を取る。
再描画が起きない画面ではtraceが0件になり得るため、会話遷移・選択変更などlayoutがdirtyになる
操作で採取する。

その結果を使い、次の二案を比較する。

- native `nw::lyt::Picture` を既存Layoutに安全に追加して正規record/replayへ乗せる（所有権・破棄を要解析）。
- self-owned command rangeをlist 32 record/replayの明確な境界へ追加する（state restore・容量管理を要解析）。

いずれもscene `FuncNode` のworld/shadow pipelineを2D UI templateとして流用しない。F-147は
UI list 32を正規の画面固定panel候補として裏付けたが、新規panelの実装自体は未着手である。

**主要部完了（F-149）**: `0x4D71B8`で本文フレーム6 Pictureと`T_msg_00`を相対配置のまま
追加し、実機で別位置の整列したフレーム/本文を確認した。cursor rangeも入口/出口traceで取得済み。
残りは話者名・汎用asset・lifetimeを含む一般化である。


<!-- source line 1466 -->
## TODO-00 [完了] 3x3 フックを外す

セッション2開始時に確認したところ `0x598688` は `EB0017C9`（未設置）だった。
ゲーム再起動でメモリパッチが消えていたため対応不要。

---


<!-- source line 1473 -->
## TODO-01 [完了] 3x3 マス掘り

周囲 8 マスに穴・抉れ・土しぶきが中心マスと同期して発生する。実機確認済み。
構成は F-34、経緯は F-31、`Field_SetItemAt` が要る理由は F-33、
CTRPF ページについては F-32。

**残るのは恒久化のみ（TODO-06）。**

---


<!-- source line 1483 -->
## TODO-01b [完了] `FieldAction_Dispatch` の case 3 到達経路

`FieldObj_ApplyRecordByAction` (`0x5A06D4`) の jumptable
（`0x5A0754`、base = `0x5A075C`、29ケース）で解決した。
**case 19（掘る）= `0x5A09D8`** で、`Item_InitWithId(&tmp, 0x9E)` の後
`FieldObj_SpawnActor` を呼ぶ。詳細は F-29。

---


<!-- source line 1492 -->
## TODO-02 アイテム名の確定

ID 158（穴と推定）、38、43、`0x20A1`-`0x20A6` の実体が未確定。
アイテム名テーブルは romfs 側にあり `.code` からは引けない。
ROM を展開して名前テーブルを参照する必要がある。

`A:\Disassemble\acnl\ROM\` が既にある。中身を確認すること。

---


<!-- source line 1608 -->
## TODO-09 [完了] 木にぶつかって切り倒す

実機で確認済み。**パッチは 1 つも当てず、`0x59BBB0` のフック 1 箇所だけで完結する。**
詳細は F-40 / F-41 / F-42。

| 項目 | 状態 |
|---|---|
| ぶつかって一撃で切り倒す | 動作 |
| 対象に応じた結果アイテム（木→切り株、竹→切断竹） | 動作 |
| 倒れる演出（物理・壁との当たり判定込み） | 動作 |
| **倒れる方向がぶつかった側に追従** | **動作** |
| 「揺する」が素の挙動（揺れるだけ） | 動作 |
| 斧が素の挙動（3 回） | 動作 |
| キューが詰まらない | 動作 |

`PATCHES/cave_tree.py`（`MODE = "install" / "uninstall" / "status"`）。ケーブは `0x01E81200`、40 ワード。

### 残っている検討事項

1. **恒久化 (`code.ips`)** — `0x01E81200` は CTRPF の空ページで `.code` の一部ではないため
   IPS に含められない。`.text` 内の死にコードへ移す必要がある。40 ワード必要。
   土しぶきケーブ（19 ワード）と合わせて **59 ワード**。TODO-06 を参照。
2. **木以外への影響** — `kind == 0` で分岐しているので、低木など他の
   フィールドオブジェクトにぶつかったときも介入する。実害は確認していないが未検証。
   必要なら `Item_IsGrowableCategory` で絞る。
3. **打撃カウンタの残留** — ぶつかったマスのカウンタを 3 にするので、
   万一そのまま倒れなかった場合、そのマスは次の斧一撃で倒れる状態が残る。
   ぶつかれば倒れるので実用上は問題にならない。

---


<!-- source line 1639 -->
## TODO-10 [完了] 実機と同じ `.code` イメージを用意する

`dump_code.py` で吸い出した。**`NCCH/exefs/code_runtime.bin`、10,485,760 バイト、
VA `0x100000` - `0xB00000`。** アンカー 17 件すべて一致（F-46）。

`VA = ファイルオフセット + 0x100000`。IDA で新規に開くときは
ARM little endian / 32bit / ARMv6K、ロードアドレス `0x00100000`。

### 残っていること

1. ~~IDA で新規 IDB を作る~~ **完了。** `make_elf.py` で ARM ELF ヘッダを被せ、
   idalib-mcp のセッション `acnl` で開いた（`code_runtime.elf.i64`）。
   関数 73 件・型 6 件・コメント 14 件を反映済み。**`xrefs_to` が使える**（F-48）。
2. **`.code` 外のマップ領域の同定**（F-46）—
   `0xB10000`-`0xBD0000` / `0xBF0000`-`0xC40000` / `0xC50000`-`0xC60000`。
   `0xC00000` は ARM コード。CTRPF 側か、ゲームの別セグメントか未確認。
3. **`romfs/` を ACNL のものへ差し替える** — アイテム名・アニメ尺は romfs 側にある。
   現在置かれているのはマリオカート 7。

- **TODO-11** Vapecord `Daytime` / `EnvironmentDaytime`（採光パッチ、時刻とは別物）。
  JPN `DAY1 0x4AFD84` / `DAY2 0x1E6CB4`(float 1.25 を書く) / `DAY3 0x4AFD8C` / `DAY4 0x4AFDA8`。
  素の値と、`E3A01788` = `MOV R1,#0x2200000` / `E8871015` = `STM R7,{R0,R2,R4,R12}` が
  何を書き換えているのかは未確認 (F-60 §7)。
- **TODO-12** `g_TimeOffsetNs`(0x9564F8) を直接動かす時間変更が成立するか実機で確認する。
  静的には最も筋が良いはずだが、`Time_AnchorFromSave` がいつ張り直すかを観測していない。

- **TODO-13** `sub_596C84`（HOST5/6 の包含関数）の正体。呼び出し元 8 件以上の汎用処理で、
  drop.cpp の作者も「unnecessary?」と書いている (F-61)。
- **TODO-14** host drop を実機で検証していない。静的解析のみ。
  ホストを騙るパッチなので**オンラインでは相手側の状態を壊しうる**。試すならローカル限定で。

- ~~**TODO-15**~~ 解決 (F-63)。`sub_598EC4` = `Drop_FindAdjacentHole`
  「隣接 3 マスから ID 158 = Hole を探す」判定。「ドロップ15x15」とは実際に衝突する。
- **TODO-16** `Drop_FindTargetTile` の第 5 引数 `a5` の呼び出し元。
  非 0 だと添字が `(i+1) % 9` のままで 15x15 化が効かない (F-62)。
- **TODO-17** 「ドロップ15x15」の副作用を実機で確認する。
  `0x859248`（斧・スコップ）と `0x859254`（植物エフェクト、ID 159-215）が潰れるはず (F-62)。

- **TODO-18** `sub_5E284C`（`0x5E284C`）がメニュー項目追加関数かの確認。
  `ItemMenu_Build` の命名根拠なので確定させたい (F-63, 現状 MEDIUM)。
- **TODO-19** `Item_CanPlant` / `Item_CanPlaceHere` が呼ぶ
  `sub_5B3CD4` / `sub_76BD4C` / `sub_769FB4` / `sub_767930` の中身 (F-63)。

- **TODO-20** FOXXY `pseudoType0x21` の画面上の効果。静的には 2 レコードの合成が追えない (F-64)。
- **TODO-21** `g_DigRecordArray` の `state = 2` になったレコードを後段で処理するものの特定 (F-64)。
- **TODO-22** FOXXY の USA→JPN 差分 `0x16C8` が有効な帯域の境界。
  `0x594000`-`0x5A3000` では確認済みだが、`CLEARLOCKED` だけ `0x2C44` なので単純な一定差ではない (F-64)。

- **TODO-23** ドロップ種別 1-0x22 の各意味の対応付け。
  `0x0A` ドロップ / `0x0B` スコップ / `0x0C` 花植える / `0x0D` マイデザ /
  `0x0F` 置いても見えない / `0x21` 無検証・無演出 は確定 (F-65)。残りは未確認。
- ~~**TODO-24**~~ 完了 (F-93)。A は何も起きず、B は変化なし。原因は判定が 2 段だったこと。
- ~~**TODO-25**~~ 完了 (F-93)。2 行とも当てれば通常ドロップでも重ね置き可。実機確認済み。
- **TODO-25** オンライン髪型変更チートを隔離環境で動的検証する (F-66)。
  - `player+0x148` を監視し、状態キック先が `+0x1A8` / `+0x2D4` のどちらになるか確認。
  - `DD000000 00000100` は標準 CTRPF では R。配布文の A と実際の入力順（R 状態キック → A アクションか）を確認。
  - 判定 NOP 3 箇所と `0x70→0xB9` のうち必要最小限、および `0x060D0600` が必須かを切り分ける。
  - remote sync が存在するため、野良オンラインでは行わずローカル通信か同意済みの検証相手だけで試す。
  - F-67 の頭装備保持＋1 tick 即時化候補を実機で確認する。自分側の Hat/Accessory、セーブ再読込後、
    パッチ済み相手、未パッチ相手の 4 条件を分けて観測する。
  - 即時化中に通常の目色変更・Mii マスク変更を行い、状態 `0xB9` 全体への副作用を確認する。

- **TODO-26 [主要項目完了]** `PATCHES/cave_hair_instant.py` のA入力後を実機確認する (F-68)。
  - **確認済み**: 男「けだるいゆるさ」 (`0x0C`) が即時表示される。
  - **確認済み**: Hat、Accessoryを含む衣装8枠が全て維持される。
  - **確認済み**: Uninstall後にゲート3箇所・hook・caveが全て元へ戻る。
  - 保存後の再読込でも HairStyle `0x0C` が維持されるか。
  - オンライン人数が0以外の隔離テストでは元の虫取り網処理へ戻り、profileを変更しないか。

- **TODO-27 [第7版・服preview crash静的解析待ち]** 通常カタログ mode 0 の屋外統合 (F-69～F-92)。
  - `BsMenuMgr` の常設子、11タブ、27状態、command byte、`MENU_FLAGS`契約、Catalogの
    init/update/end、field X ownerとの非対称を `code.bin.i64` で再構築済み。
    詳細は `DOCS/menu_system.md`。
  - **訂正済み:** `BsMenuMgr+500` は `BsHandCursor`、`+480` が `BsMenuTab`。
    Catalog初期化はcursorだけを隠し、fieldタブを退場させない（F-80）。
  - **訂正済み:** Catalogは通常持ち物用 `MENU_FLAGS 0x08/0x10`を立てない。
    そのため「メニュー終了まで待機」`0x6D7194` はgenericな待機として流用できない（F-80）。
  - **最新失敗の原因確定:** constructor成功後にタブを退場させた版は、退場完了後
    `0x08==0` を見て `0x20`を即時発行し、生成済みCatalogを表示前に終了させた（F-81）。
    ghost閉じるbuttonはCatalogではなく `BsMenuTab` index 10。
  - **終了後lockの原因確定:** Catalogは自身と背景だけを終了し、field Xが開始したplayer
    state `0x16`、controller state 5、タブ、cursor、地図を戻さない。開始ownerと終了ownerの
    不一致であり、Catalog destructorの失敗ではない（F-82）。
  - **3Dの静的判定:** stock room 0は `BsFtrMgr` type `0xEE`を生成しないが、容量38枠と
    Item.bin家具family用の固定actor factoryは利用できる（F-83/F-84）。
  - **F-86訂正:** active `ScStage` とsaved `BsMenuTab` は精密再読で共に
    `+14=1/+15=0`。両者ともchild gateを通り、parent拒否説は撤回した。
  - **二つ目の不具合:** `g_BsFtrMgr` はphase 1中に公開されるため、nonnullだけでcacheを
    無効化すると早過ぎる。Catalogは失敗後に同一品を再試行しない（F-83/F-84）。
  - **除外済み:** `CameraCatalog`、Catalog専用3灯、renderer layer 2はroom 0にも存在する。
    camera/light/pass欠落を再調査しない（F-85）。詳細は `DOCS/furniture_rendering.md`。
  - saved `BsMenuTab` parent＋完全ready待ちの第2版でも、実機は
    `owned=0/status=3/g_BsFtrMgr=0/actor=0` で3Dなし。
  - **F-87静的最有力:** room 0容量38はphase 1でCPU 3,648,000 bytes＋VRAM 988,000 bytesを
    late allocationする。CPU bank heapが1件でもnullならnew childは同一呼出し中に破棄される。
  - 第3版はadapter activeかつpreview status 0の間だけ `0x68FD2C` で容量を1へ制限し、
    `(byte[19]&3)==3` 待ちとCatalog `+8160` cacheの1回再試行を維持する。適用・読戻し済み。
  - **F-87動的裏付け:** 容量1でmanager `+24=1`、`+19=1`、published pointer nonnullまで
    到達した。以前の38-bank phase 1即時失敗説を支持する。
  - **F-88クラッシュ原因確定:** 第3版はready待ち中もstock preview bodyへ戻ったため、phase 1
    公開直後にtype `0xBC` actorを生成し、`BLX` targetが命令語 `0xE1A04000`になった。
    例外actorを基底vtableへ戻してstock破棄へ渡し、クラッシュ状態は回収済み。
  - 第4版はmanager生成frameとstatus 1の未ready期間にpreview update全体からreturnする。
    例外停止中にprivate stateを保持して差し替え、読戻し後に再開済み。
  - **F-89:** 2回目はmanager phase 3のfield map走査が屋外Item `0x2090`をdefault
    type `0xBC`で生成した別経路。Catalog cached Item `0x2EA3`ではない。
  - 第5版はadapter-owned phase 3だけ `Field_GetMapManager`を0にし、map走査を省く。
    進行中actorはstock破棄し、走査後へ戻してmanager完了bit `3`を命令stepで確認済み。
  - **F-90:** 3回目は選択Item `0x2EA3`自身。record family 1が正規にtype `0xBC`
    (`AcFtrLoop`)を選ぶが、屋外objectのgeneric create vptr+8は `0xE1A04000`だった。
  - 同objectの4 vptrを基底`AcFtr`へ戻して例外直前から再実行すると、pre/create/postは
    `0x6E3A10 / 0x81F2B8 / 0x307D08`、create result 2、preview actor attachまで成功。
  - 第6版はadapter active中のpreview openだけtype `0xBC -> 0xBB`にする。Item requestは不変。
  - **3D成功:** 第6版で `0x2EA3`「0のランプ」と `0x2E78`「12つぶのぶどう」を連続表示。
    どちらもfamily 1/type `0xBC`を基底`0xBB`へ置換したactorである。
  - **F-91:** `0x2C89`「1UPキノコ」はfamily 3/type `0xBD`で、同じprimary
    `vptr+8=0xE1A04000`によりSIGSEGV。モデル固有ではなく特殊actor family共通の生成契約差。
  - 第7版はadapter active中のpreview openだけ、特殊家具type範囲 `0xBC..0xEB -> 0xBB`とする。
    例外actorは基底vptrでcreate result 2、Item `0x2C89`としてattach済み。
  - **家具3D確認完了:** 1UPキノコを含む家具は一通り表示された。通常家具に対する基底化は有効。
  - **F-92:** 壁紙・絨毯などは非表示。服カテゴリへ移動すると
    `0x317BD0` (`ModelInstance_SetRenderLayer`) でSIGSEGV。以前の無効vtable crashとは別段階。
  - 作業中断・電源断のため、服crash時のregister、stack、actor、個別Itemは未採取。
  - **次回は静的解析から開始:** `CatalogPreview_UpdateActor`のカテゴリ3/4/41変換、mannequin分岐、
    `AcFtr_CreateFinalize -> ModelInstance_SetRenderLayer`のcallerと引数を追う。
  - rev7の範囲fallbackが服用派生actorまで基底化した影響か、屋外で服model instanceが
    未初期化なのかを静的に分離してから、guardを家具だけへ狭めるか服専用初期化を追加する。
  - 壁紙・絨毯がstock室内Catalogでどのpreview経路を使うかも別途比較する。
  - 3DS電源断後はruntime patchが消える。Remote GDB再接続後、必要時にrev7を再installする。
  - 現在部屋ID `0x3C` の偽装や、室内のactor/factory/light pointerの屋外持越しは行わない。


<!-- source line 2027 -->
## ~~TODO-135: シーケンスを「曲・効果音」として合成する~~ — **効果音は完了**（F-243 / F-244）

**達成。** BGM を除く seq 型 2,839 件を WAV 化（`SOUND/out/seq_wav/`、100.2 分）。
CSEQ 命令表はラベル境界一致 **100.00%**。残りは `SEQ_BGM_*` 595 曲（同じ仕組みで出せる）と、
包絡の時定数の精密化。以下は着手時のメモ。

F-242 で素材は全部揃った。残るのは **CSEQ のバイトコードを解釈して、
CBNK の楽器定義と CWAR の波形で合成する**こと。

これができると 2 つ手に入る:

1. `SEQ_BGM_*` 595 曲と、内蔵シーケンスの効果音を音として書き出せる
2. **1 効果音 ↔ 1 波形の対応が確定する**（現状は bank 経由の候補集合どまり）

### 分かっていること

- CSEQ = `0x5000 DATA`（バイトコード）+ `0x5001 LABL`（名前 + オフセット）
- sound の開始位置は `SOUND/index/sounds.csv` の `seq_offset`（DATA 先頭からのバイト）
- `0xFE` + u16 = AllocateTrack（トラックのビットマスク、3 バイト）。
  BCSAR の `seq_offset` はこれを**読み飛ばした後**を指す（F-242 で 449 件から確定）
- 観測されたシーケンス先頭バイト: `0x80` `0x81` `0x88` `0x89` `0x8A` `0xA0` `0xA1`
  `0xB1` `0xB4` `0xB6` `0xC0` `0xC1` `0xC3` `0xC7` `0xCA` `0xCC` `0xCD` `0xD0` `0xD1`
  `0xD3` `0xD4` `0xE1` `0xF0` `0xFF`（`0xFF` は終端）
- CBNK INFO は `{u32 count, {u32 warcItemId, u32 waveIndexInWarc}[count]}` の波形スロット表を持ち、
  楽器エントリ（`0x5900`）はそのスロット番号を持つ（実測: bank 335 が 0/1、bank 405 が 4/5）

### 進め方

1. まず**楽器エントリ（`0x5900`）の全フィールド**を確定する。
   スロット番号の位置は掴めているが、キー範囲・エンベロープ・ルート音は未確定。
   1 波形しか持たないバンク（多数ある）を使えば当たりを取りやすい。
2. 次にバイトコードを**逆アセンブルだけ**する（音にしない）。
   `SOUND/index/sequences.csv` の 33,344 ラベルが正解データになる。
   ラベル位置から次のラベルまでを 1 シーケンスとして、命令長が矛盾なく埋まるかで検証できる。
3. 合成は最後。プログラム番号 → スロット → 波形が引ければ、
   単発の効果音は「その波形をピッチ変更して鳴らすだけ」で足りることが多い。

**注意:** 5 件（`SE_SYS_WIN_SELECT_ITEM_CLOSE` / `SE_OBJ_FISH_STRUGGLE_HAND` /
`SE_IND_SICK_CLOSE` / `SE_FUR_DARU_MATORYOSIKA_OPEN` / `SE_FUR_DARU_MATORYOSIKA_CLOSE`）は
自分と同名のラベルとは別のシーケンスを鳴らす。ラベル名を信じて対応付けないこと。


<!-- source line 2136 -->
## 完了

- [x] 上画面に描く / 下画面に描く / 上下の描き分け
- [x] 常に最前面（優先度 `0xFF`）
- [x] 常時表示（ロード・メニュー・フェードで消えない）
- [x] ゲームを止めない
- [x] 座標系の確定（1 単位 = 1px、原点は画面中央）
- [x] ASCII フォント（128x128 LA4、61 文字）
- [x] メニューのレイアウト（枠・タイトル帯・カーソル・6 項目）
- [x] 拡大率の整数倍化（線幅の不揃いを解消）


<!-- source line 2243 -->
## 2026-09-04 追加（F-287 確定・基準版の固定）

- [x] 実機で復旧を確認（利用者「直りました」）
- [x] `BASELINE/gui_render_ok_f287/` へ基準版を保存（21 ファイル + SHA-256 + README）
- [x] `PATCHES/verify_baseline.py`（差分検出 / `--restore`）
- [x] `CLAUDE.md` に索引と教訓 2 件を追加
- [ ] `.bss` の各領域の大きさを **1 箇所から生成**する形に作り直す（F-287 の再発防止）
- [ ] F-283 の要素を **1 つずつ**入れ直す（美咲フォント → アニメ → 項目型）。
      1 要素ごとに検査 7 本 + 実機確認。壊れたら `verify_baseline.py --restore` で戻す


<!-- source line 2373 -->
## 2026-09-05 追加（F-293。正規経路で描画成功）

- [x] **`.bss` に nw::lyt のオブジェクトを自前で組み、ゲームの `Layout_RecordPaneTree` に描かせた**
- [x] **CAVE_Q(205 語) を撤去**。前エージェントの残骸（下画面の白帯）も解消
- [x] 位置が画素単位で一致することを実測
- [x] **色は頂点カラー `+0x140` で 1 枚ずつ変えられる**（F-280 の制約が消滅）
- [ ] 文字を Picture N 枚で並べる。**1 枚ごとにオブジェクトが要る**（木を歩くのはゲーム側）
- [ ] `.bss` の確保計画（Picture は詰めれば 1 枚 0x160 程度）。上画面 119 枚で約 42KB
- [ ] A1 / A2 を縮める（投影の直接呼び出しは vtable +0x18 に任せられる）
- [ ] プラグインへの移植
- [ ] `mat+0x4D` bit1 の意味を詰める（立てると描画が止まる）


<!-- source line 2888 -->
## 2026-09-09 F-386 内蔵SWKBD漢字確定後

- [x] パッチを残したまま通常チャットを再度開き、`漢字テスト` を入力して右ボタンで確定。
- [x] `read_native_chat_result.py` で結果コード2、offset=0、length=5 UTF-16単位、
  共有ページの `漢字テスト`、APT状態0、run count=2を回収。
- [x] 利用者の正常復帰報告と、結果コード・UTF-16共有メモリ・APT状態を照合。
- [x] 候補一覧・候補順位・文節境界を得るため、SWKBD実行中に候補生成・描画・辞書参照の
  どこを観測するかを、F-363の静的番地と今回の実機起動経路を使って設計する。
- [ ] 次の実機書込み前に、観測パッチの全分岐・全PC相対LDR・領域重複・失敗時復帰を
  機械検証し、停止中実機の現行パッチ/BSSと突き合わせる。


<!-- source line 139 -->
- [x] 利用者が移設後の内蔵キーボードで指定入力を未確定保持。

<!-- source line 140 -->
- [x] read_phrase_snapshot.pyと検査器を準備。保存済みapp＋模擬editor、異常7件の検査PASS。

<!-- source line 2167 -->
- [x] `GuiCaves.h` の自動生成（`PATCHES/export_gui.py`）

<!-- source line 2168 -->
- [x] `GuiRender` / `OwnGui` / `GuiMenu` の書き直し

<!-- source line 2169 -->
- [x] ビルドせずに移植を照合する道具（`PATCHES/verify_plugin_port.py`）

<!-- source line 2170 -->
- [x] ビルド（警告 0 件）

<!-- source line 2182 -->
- [x] 十字キーの連続入力（200ms / 60ms）とスライドパッドの無効化

<!-- source line 2183 -->
- [x] 美咲ゴシック第2 8px（グリフを実行時にアトラスへ焼く）

<!-- source line 2184 -->
- [x] 登場・退場／選択追従／明滅／跳ね返りのアニメーション

<!-- source line 2185 -->
- [x] 項目型（フォルダ・チェック・アクション・10進・16進・小数・スライダー・リスト）

<!-- source line 2186 -->
- [x] 未適用の黄色表示・X で適用・L で全戻し・閉じる確認

<!-- source line 2187 -->
- [x] 説明とホットキーの常時表示

<!-- source line 2188 -->
- [x] 通知（チェックボックスの適用が変わったときだけ）

<!-- source line 2220 -->
- [x] F-283 / F-285 を `BACKUP/f283_f285_20260904/` へ退避

<!-- source line 2221 -->
- [x] `cave_node_record.py` の容量・`.bss`・`LIST_SIZE` を F-282 へ差し戻し

<!-- source line 2222 -->
- [x] `GuiCaves.h` 再生成（下 38 枚 / 上 134 枚 / 色 24 / LIST 0x8000）

<!-- source line 2223 -->
- [x] `GuiRender.cpp` / `GuiMenu.cpp` を F-282 版へ書き直し（焼き込みアトラス・アニメ無し）

<!-- source line 2224 -->
- [x] `OwnGui.cpp` の取り外し順序を修正（`LOG+0xE8` を**フックを外す前に**見る）

<!-- source line 2225 -->
- [x] 検証 5 本（照合・監査・リテラル・プレビュー・成果物）＋ビルド

<!-- source line 2233 -->
- [x] 記録されたコマンド列を直読みし、先頭 144 バイトがリングのゴミだと確定

<!-- source line 2234 -->
- [x] `RING`(0x200) と `MATCMD` の重なりを解消（`0x9B5800` / `0x9B5A00`）

<!-- source line 2235 -->
- [x] `_check_layout()` の RING を `0x80` → `0x200` に是正（再発防止）

<!-- source line 2236 -->
- [x] `OwnGui.cpp` の `ZeroBss(kGuiRing, ...)` も `0x200` へ

<!-- source line 2237 -->
- [x] 再生成・検証 3 本・ビルド

<!-- source line 2238 -->
- [x] 実機の生きているプロセスへ最小修正（リテラル 1 語 + TEV 書き戻し）

<!-- source line 2255 -->
- [x] Chokistream の画面ウィンドウを AI が読めることを確認

<!-- source line 2256 -->
- [x] `PATCHES/grab_screen.ps1`（上下切り出し・連写・画素差 %）

<!-- source line 2261 -->
- [x] 実物の Picture を捕獲し、構造（幅/高さ/行列/UV/材質埋め込み）を実測

<!-- source line 2262 -->
- [x] 複製した自前 Picture で `nwlyt_Picture_DrawToCommandList` を呼び、**1 枚描けた**

<!-- source line 2263 -->
- [x] 位置・大きさが自前の値で効くことを 3 通りで確認

<!-- source line 2264 -->
- [x] 片付け（フック復元・ケーブとクローンをゼロ埋め・自前 GUI 無傷を確認）

<!-- source line 2273 -->
- [x] `TextBox_UpdateDrawState`(0x4B7DEC) から記述子 → PICA レジスタの対応表を確定

<!-- source line 2274 -->
- [x] `unk_97B74C` の実測ヘッダで裏取り（ユニット0 = 082/085/08E/083）

<!-- source line 2275 -->
- [x] **自前アトラスを貼って実機で確認**（文字がそのまま出た）

<!-- source line 2283 -->
- [x] 色の欄を特定（`*(mat+48)&3` で分岐、モード1 は `*(mat+16)`→0x0DB / `*(mat+20)`→0x0F3）

<!-- source line 2284 -->
- [x] **実機で色を変えられることを確認**（`0xFF0000FF` で赤。書式は `0xAABBGGRR`）

<!-- source line 2285 -->
- [x] **外部参照 5 語を 0 にしても描画継続**＋12 秒の走行に耐えることを確認
      （★「場面変化に耐えた」と書いていたが根拠が無かった。場面変化は未検証）

<!-- source line 2295 -->
- [x] `sub_73B650` を読み、UV キャッシュ（`*(pic+212)` / `*(mat+77)` bit2 / `*(pic+216)`）を特定

<!-- source line 2296 -->
- [x] テクスチャ記述子の全欄を確定（`+0x08`/`+0x0C` が UV 倍率。段 1 の記述を訂正）

<!-- source line 2297 -->
- [x] **UV 再計算を強制して 15 秒の走行に耐えることを実機で確認**
      （★「場面変化」は未検証。放置では場面は変わらない）

<!-- source line 2307 -->
- [x] 判定をフレーム基準にして、元の Picture に依存しない形にした

<!-- source line 2308 -->
- [x] **ロードを跨いでクローンが生き残ることを実測**（外部参照を全部 0 にした状態で）

<!-- source line 2309 -->
- [x] 見えない原因を特定 = **乗り込む位置**（下画面の全画面背景の直前に割り込んでいた）

<!-- source line 2317 -->
- [x] `build_q` のスプライトループを `Picture_DrawToCommandList` 呼びへ置換（`Q_PICTURE_CALL`）

<!-- source line 2318 -->
- [x] 再利用 Picture 雛形 `PIC = 0x9B6000`（0x400）と packed 色配列 `0x9B6400` / `0x9B6460`

<!-- source line 2319 -->
- [x] マテリアル消失ガード（`LOG+0x08`。実測 0 発火 / 記録 4823 回）

<!-- source line 2320 -->
- [x] 実機で 3 矩形 → 全メニューまで表示成功（前エージェント）

<!-- source line 2321 -->
- [x] **Picture 経路の座標系を実測で確定**＝手書き経路と同一（F-290）

<!-- source line 2330 -->
- [x] **H-1（チャンク 0 の残像）を修正**（判定を StartSave のあと・`endrec` へ）。実機 A/B/C で確認

<!-- source line 2331 -->
- [x] **`audit_node_cave.py` の既定対象が旧ファイルだった欠陥を修正**（+ `PIC_FN` を許容）

<!-- source line 2339 -->
- [x] RTTI で `nw::lyt::Picture` / `Pane` / `Material` と確定。継承も確定

<!-- source line 2340 -->
- [x] ペイン工場から **Picture = 344 バイト**を確定（文書の「約 0x320」を訂正）

<!-- source line 2341 -->
- [x] Pane / Picture / Material / TexMap の全フィールドを ctor と取得子から確定

<!-- source line 2342 -->
- [x] TexMap の `+0x14/+0x18/+0x1C` が**派生キャッシュ**であることを確定（`sub_4B9830`）

<!-- source line 2343 -->
- [x] アンカーの旧 IDB コメントの誤り（縦 1 の分岐落ち）を訂正

<!-- source line 2344 -->
- [x] IDB へコメント反映・保存

<!-- source line 2353 -->
- [x] F-291 の結論を別関数 7 系統で再検証 → **矛盾 0**

<!-- source line 2354 -->
- [x] 本物の `ssys::ma::lyt::Layout` vtable を特定し、自前 vtable と一致することを確認

<!-- source line 2355 -->
- [x] `Layout_RecordPaneTree` / `DrawPaneTreeToCurrentList` / `Pane_DrawRecursive` を読み切り、
      **レイアウトに必要な欄が 10 個ほどしかない**ことを確定

<!-- source line 2365 -->
- [x] **実機のレイアウト・Pane 木・Material・TexMap で静的結論を全数検証 → 矛盾ゼロ**

<!-- source line 2366 -->
- [x] `ROR32(+0x0C,16) = +0x18` と 書式表`[2]=9` を**触っていない実データ**で確認

<!-- source line 2367 -->
- [x] 実物が派生 `6Layout` であること、`+0x18` を上書きしていることを把握

<!-- source line 2368 -->
- [x] Material の位置は規則的（常に +416）と訂正

<!-- source line 2387 -->
- [x] 利用者が実機でロード・操作を跨いで正常動作を確認（F-293 追記）

<!-- source line 2388 -->
- [x] `nw::font::Font` が抽象インタフェース（24 純粋仮想）＝**自前フォントが可能**と確定

<!-- source line 2389 -->
- [x] `Glyph` 構造を `nwfont_ResFont_GetGlyph` から確定（テクスチャ番地 / セル UV / 幅 / 書式）

<!-- source line 2399 -->
- [x] `nw::lyt` のアロケータ（`sub_4B8CF0`）から **64KB を借りられた**

<!-- source line 2400 -->
- [x] **F-221 の訂正**: 0x4000 上限は g_GfxAllocator のヒープの性質。Alloc 関数の制限ではない

<!-- source line 2401 -->
- [x] 共有 Material + 共有 texMap + Picture[N] の配置で **メニュー全体 74 枚を描画**

<!-- source line 2402 -->
- [x] 一括転送（bytearray → 0x1000 ずつ）で書き込み時間切れを解消

<!-- source line 2410 -->
- [x] **アロケータ vtable +0x0C = `ssys::ma::Allocator::Free` `0x00569B44` を特定**

<!-- source line 2411 -->
- [x] `Alloc` / `Free` が対称（ヘッダ無し）であることを静的に確認

<!-- source line 2412 -->
- [x] `alloc_lyt_heap.py MODE="free"` を実装（17 語、事前監査つき）

<!-- source line 2413 -->
- [x] `build_pane_tree.py MODE="detach"`（描画だけ止める。vtable は触らない）

<!-- source line 2414 -->
- [x] **実機で 確保 → 解放 → 再確保 → 組み直し の往復を成立させた**
      解放後に同一番地が返る＝空きリストへ戻った裏取り

<!-- source line 2419 -->
- [x] **下画面のペインツリーを組む**（F-297。上 74 枚 / 下 110 枚が独立した輪で同時描画）

<!-- source line 2420 -->
- [x] **容量**: F-296 の解放機構で `0x10000` → `0x20000` へ借り直した（371 枚ぶん）

<!-- source line 2431 -->
- [x] `BASELINE/gui_spec_v2/README.md` を制定（**探索では書き換えない**）

<!-- source line 2432 -->
- [x] `DrawSelf` の呼び出し規約を静的に確定（`0x73B524`）

<!-- source line 2433 -->
- [x] Picture のバッチ遅延と `DrawCtx_FlushBatch(drawctx, cursor)` を静的に確定

<!-- source line 2449 -->
- [x] 最新の到達点F-302と基準仕様v2の未実装CAVE_TXTを区別。F-299の容量式を静的IDBと実装で照合。

<!-- source line 2450 -->
- [x] TextBoxのバッチ再利用分岐を確認。容量からCPU/GPUの速さを断定しない。

<!-- source line 2451 -->
- [x] 実機の既知GUIフックが素、管理スロットがゼロであることを確認。STATE先頭を更新。

<!-- source line 2460 -->
- [x] 独立Pane＋TextWriter/標準バッチの経路を静的に調査。

<!-- source line 2461 -->
- [x] Init/Reset/DrawString/Build/提出prefix/提出/suffixの引数を標準TextBox経路のassemblyと照合。

<!-- source line 2462 -->
- [x] ResFontの取得子とCMAP/GetGlyph、writer座標処理を確認し証拠JSONへ保存。

<!-- source line 2473 -->
- [x] 借りた nw::lyt ヒープが GPU 可視であることを実機で確認（アトラス専用確保が不要に）

<!-- source line 2474 -->
- [x] 自前アトラス生成器 `make_font_nwfont.py`（nw::font の 1 画素余白・CMAP 方式 0 に対応）

<!-- source line 2475 -->
- [x] 倍率と Y の式を静的に確定し、ゲームのフォントで検算

<!-- source line 2476 -->
- [x] `own_font.py`（フォント資源 + TextBox をデータだけで組む）。領域の重なり検査つき

<!-- source line 2487 -->
- [x] `ResFont` vtable 26 スロットの全数解析（推測ゼロ）

<!-- source line 2488 -->
- [x] `FINF[0x07]` = 読み取り器の選択（必ず 1）を確定。F-304 の PC=0 の真因

<!-- source line 2489 -->
- [x] `FINF[0x01]` = 行送り、CWDH は 0 でよい、倍率と Y の式を確定

<!-- source line 2490 -->
- [x] 実機なしの検算 2 本（`verify_own_font.py` 8 検査 / `verify_font_deps.py` 番地照合）

<!-- source line 2491 -->
- [x] **実機で自前フォント描画に成功**（コードケーブ 0 語）

<!-- source line 2507 -->
- [x] ケーブが呼ぶ 9 関数の引数と副作用を静的に確定

<!-- source line 2508 -->
- [x] TextWriter のひな型 25 語を全語確定（`sub_4D5B18` + `sub_7E8488`）

<!-- source line 2509 -->
- [x] `.text` の空きをゼロ連続で機械測定（`0x838810` は空きではなかった）

<!-- source line 2510 -->
- [x] ケーブ 75 語を実装 → 監査 → objdump → **実機のバイトを逆アセンブルして確認**

<!-- source line 2511 -->
- [x] **実機で TextWriter 直呼びの描画に成功**

<!-- source line 2512 -->
- [x] import 経路の `sys.exit()` を塞ぎ、`importlib.reload()` を入れた

<!-- source line 2531 -->
- [x] **nw::lyt ヒープの実残量を確定させた**（F-309）。正体は **`sead::ExpHeap`**、
      `+0x1C`=先頭 / `+0x20`=総量 で解釈は**正しかった**（先頭を推測したのが誤りだった）。
      **空き 1,200,132 B (1.14 MB)、空きブロックは 1 個。** 1,200 文字の 445KB は余裕で入る。
      測り直しは `PATCHES/probe_lyt_heap.py`（読み取り専用）

<!-- source line 2535 -->
- [x] **場面をまたいで最小の空きを測った**（F-310。利用者にタイトルから進める・
      住民に話しかける等をしてもらった）。**空きは 3.16MB 〜 0.61MB まで動く。**
      最悪時に配れるのは **738,876 B**、断片化で空きが 5 個に割れる場面もある。
      → **上限は 1,000 文字前後。1,200 文字は破綻するのでやめる**

<!-- source line 2556 -->
- [x] 3gx の名前を `gohan` に統一（`Makefile` の `TARGET`、`plgInfo`、`PluginMenu`）

<!-- source line 2557 -->
- [x] v1 のファイルを `_v1_retired/` へ退避（ビルドされない。正本は BASELINE）

<!-- source line 2558 -->
- [x] `export_gui_v2.py` / `export_font_nw.py` でヘッダを生成（ケーブは書き直さない）

<!-- source line 2559 -->
- [x] `GuiV2.cpp`（描画本体）/ `OwnGui.cpp`（組み込み）/ `GuiMenu.cpp`（最小 GUI）

<!-- source line 2560 -->
- [x] 記録コマンドリストの安全弁を実装（§4.7 / 仕様書 §8 の未実装項目）

<!-- source line 2561 -->
- [x] `verify_plugin_port_v2.py` 7 群 すべて 0 件

<!-- source line 2562 -->
- [x] `gohan.3gx` までビルド（警告 0）

<!-- source line 2563 -->
- [x] ケーブを objdump で逆アセンブルして確認

<!-- source line 2585 -->
- [x] 真因: `InitBss()` が `GuiV2::Install()` の**あと**にあり、`node+0x20` を消していた
      （実機ログの「list は非 0 なのに記録長 0」で確定）

<!-- source line 2587 -->
- [x] `Enable()` の順序を修正 + `node+0x20` の検査を組み込みに追加

<!-- source line 2588 -->
- [x] `Commit()` が生きているオブジェクトを `memset` しないよう分離（`BLX 0` 予防）

<!-- source line 2589 -->
- [x] 輪は `root+0x14` を最後に公開

<!-- source line 2590 -->
- [x] `node+0xB0` を Install でも設定

<!-- source line 2591 -->
- [x] アトラスに塗り潰しのマス（列 15/行 15）を追加し、矩形の UV をマス内側へ

<!-- source line 2592 -->
- [x] `FillSlot` で TextBox の `+0xFE`(dirty) を立て直す

<!-- source line 2593 -->
- [x] `verify_plugin_port_v2.py` に**群 8（順序と禁止事項）**を追加

<!-- source line 2600 -->
- [x] 原因は中央整列での半画素（ペイン高にセル高 7 を入れていた。正しくは行送り 8）

<!-- source line 2601 -->
- [x] `FillSlot()` のペイン高を `kFontLinefeed` へ

<!-- source line 2602 -->
- [x] 仕様書 §3.1 と検証器 2 本に条件を追加

<!-- source line 2607 -->
- [x] 段 1: フォント基盤（美咲 362 字＋PixelMplus 27 字を 1 枚に。CMAP 方式 2 + CWDH）
      `PATCHES/make_font_ui.py` 検証 6 本 0 件 / `Includes/GuiFontUi.h` を生成

<!-- source line 2612 -->
- [x] **`LIST_SIZE` を上げられるか** → **上げられる。** `BL 0x5685A4` 129 箇所の R3 を走査し、
      ゲーム自身が `0x10000` を 3 箇所、`0x11000` を 1 箇所、**`0x18000` を 1 箇所**で使用

<!-- source line 2614 -->
- [x] **記録の 1 文字あたり** → `sub_4D6CE0` の語数を式にして **約 61 B/字**。
      式（338 語）と F-308 の実測（306 語、17 字）が 10.5% 以内で一致

<!-- source line 2616 -->
- [x] **1 本のバッチに複数文字列** → `sub_4D6570` が全件をマテリアルごとにまとめる設計そのもの

<!-- source line 2636 -->
- [x] F-313 の結論を他の点と突き合わせた（F-314）。誤り 1 件を訂正、2 件は独立に裏付け

<!-- source line 2651 -->
- [x] `LIST_SIZE 0x10000` を実機で確認（`list=42/43`）

<!-- source line 2652 -->
- [x] `LIST_SIZE` が nngx ヒープからだけ減ることを実機で確認（nw::lyt は ±0）

<!-- source line 2653 -->
- [x] 借用 `0x50000` を実機で確認

<!-- source line 2654 -->
- [x] **CMAP 方式 2 / CWDH / 256x128 / 日本語**を実機で確認（字形番号 7/7 一致）

<!-- source line 2655 -->
- [x] **F-316**: シート記述子 `+0x0C` は `(幅<<16)|高`。正方形では露呈しない誤りを訂正

<!-- source line 2656 -->
- [x] 記録量の模型を実測から作り直した（**552 B/文字列 + 48 B/字 + 204 B/Picture**）

<!-- source line 2657 -->
- [x] 仕様書 v2 を**改訂 3**（検証器 31 項目・命令 26 件で 0 件）

<!-- source line 2679 -->
- [x] 削除ケーブ 43 語（束縛中を避ける守りつき）を作り、objdump と idalib で検証

<!-- source line 2680 -->
- [x] 実機で **132,192 B が丸ごと戻る**ことを確認（`g_GpuCmdPtr` 等は無傷）

<!-- source line 2681 -->
- [x] 仕様書 §5.3 の順序を訂正（**フックを外してから削除**）

<!-- source line 2682 -->
- [x] 監査が LDR を 1 件も見ていなかったのを修正（検査件数を必ず出すようにした）

<!-- source line 2683 -->
- [x] `OwnGui.cpp` に `DeleteCmdLists()`、`Disable()` の順序を訂正

<!-- source line 2684 -->
- [x] 検証器に `kDelCave` の照合と `Disable()` の順序検査を追加

<!-- source line 2689 -->
- [x] `GuiFontUi.h`（美咲 362 + PixelMplus 27 + 塗り潰し 1）を `GuiV2.cpp` へ

<!-- source line 2690 -->
- [x] `DrawText` / `MeasureText` を UTF-8 + CWDH 可変幅 + 書体選択に

<!-- source line 2691 -->
- [x] 安全弁を `552 x 本数 + 48 x 字数 + 204 x 枚数` に（F-315 の実測式）

<!-- source line 2692 -->
- [x] `WriteCaves` が A1/A2 の `LIST_SIZE` を上 `0x10000` / 下 `0x8000` へ

<!-- source line 2693 -->
- [x] 書き換える語 79 がリテラルであることを静的に検査（群 1 に追加）

<!-- source line 2694 -->
- [x] 検証器の群 2/3 を UI フォント用に書き直し（`own_font_data.build_ui` が正本）

<!-- source line 2695 -->
- [x] ★実機で確認（2026-09-06「実際には問題なく描画されました」）

<!-- source line 2696 -->
- [x] 一式を `BASELINE/gui_v2_ok_f319/` と `BACKUP/f319_uifont_20260906/` へ凍結

<!-- source line 2701 -->
- [x] クラッシュダンプの読み方を `DOCS/crash_recovery.md` に文書化

<!-- source line 2702 -->
- [x] `__createThread` が TLS の magic を確かめないことを逆アセンブルで確定

<!-- source line 2710 -->
- [x] 段 4a GuiV2 の枠を作り直す（不均一スロット 50+2 / Picture 24 枚/画面 /
      借用 0x60000 / LIST_SIZE 上 0x18000）

<!-- source line 2712 -->
- [x] ★`OwnGui` の `BorrowHeap(0x30000)` 直書きと `kBorrowBytes 0x50000` の
      食い違いを潰した（検証器が片方しか見ていなかった）

<!-- source line 2714 -->
- [x] 段 4b メニュー木・選択・スクロール・説明パネル・下帯

<!-- source line 2715 -->
- [x] 段 5 アニメーション（開閉 320 / 追従 100 / スクロール 100 / 脈動 1800 /
      値の跳ね 100 / 起動の跳ね 80 / 端の跳ね 100 / 連続入力 200→60）

<!-- source line 2717 -->
- [x] インラインリスト（180ms・6 行）とダイアログ（160ms）

<!-- source line 2718 -->
- [x] `PATCHES/preview_menu.py`（実機なしで見た目を PNG 確認）

<!-- source line 2719 -->
- [x] 検証器の群 5 を **Simulator の ui-model.js / app.js との突き合わせ**へ

<!-- source line 2722 -->
- [x] ★実機で確認（2026-09-07。メニュー・行・値・2 書体の使い分けが出た）

<!-- source line 2723 -->
- [x] 一式を `BASELINE/gui_v2_ok_f322/` と `BACKUP/f322_simulator_menu_20260907/` へ凍結

<!-- source line 2729 -->
- [x] 症状の切り分け（画素幅の偶奇と一致。字数ではない）

<!-- source line 2730 -->
- [x] 経路を idalib で確認（アンカー -幅/2 / 整列 +幅*0.5 / 原点 -文字幅/2）

<!-- source line 2731 -->
- [x] 横を左アンカー + 左寄せにして `/2` を経路から消した

<!-- source line 2732 -->
- [x] 検査を群 8 に追加、仕様書 §3.1 を書き直し

<!-- source line 2733 -->
- [x] ★実機で確認（2026-09-07「問題なく表示されました」）

<!-- source line 2748 -->
- [x] 移行で何がどれだけ変わるかを機械で見積もり

<!-- source line 2749 -->
- [x] 静的に確定していることの棚卸し（色・書体・位置が**字ごと**にバッチへ入る）

<!-- source line 2750 -->
- [x] 静的（F-337。`scratchpad/MEMO_f337_textwriter_static.md`）
      `DrawString` はカーソル 2 欄しか壊さない / 吐き出しは 16 字ごと・色の連 6 本ごと /
      提出は 1 フレームに何度でも呼べる / バッチは通常メモリ
      （★「書体を混ぜると群が分かれる」は誤り。群の鍵は**記述子 +0x08**＝
        テクスチャの物理番地なので、同じアトラスなら 1 群のまま。F-339 で実機確認）

<!-- source line 2755 -->
- [x] 記録の式を実測で確定（F-338）

<!-- source line 2756 -->
- [x] ★**実機で「1 本のバッチに複数文字列」を確かめた（F-339。通過）**
      34 字・3 本・色 3 種・書体 2 種が 1 本のバッチから正しく出た

<!-- source line 2758 -->
- [x] ★色替え・書体替えの費用を分解した（**F-340**。実機 15 点）

<!-- source line 2759 -->
- [x] ★★費用の式を**逆アセンブルの写し**に置き換えた（**F-341**。実機 19 点で誤差 0、
      うち 3 点は予言してから測った）。正本 `PATCHES/batch_cost_exact.py`
      字 12 語 / 吐き出し 28 語（16 字ごと・色替え 6 回ごと）/ 色替え 16 語 / 書体替え 0
      ★現在色の初期値は **writer+0x18＝最後に描いた文字列の色**

<!-- source line 2763 -->
- [x] あふれたときの守りを静的に確定（F-340。超えた字は静かに捨てられる／
      `batch+0x06` で語数の上限を外から縛れる／コマンド語の器は最悪でも 73%）

<!-- source line 2765 -->
- [x] ★★設計を数字で決めた（**F-342**。`PATCHES/design_shared_batch.py`）
      ★費用の 8 割は**コマンド語の器の取りすぎ**（1 字 312 B 取って 48 B しか使わない）。
      `batch+0x20` は誰も読まないので詰められる（5 関数を読んで確認・実機でも確認）

<!-- source line 2768 -->
- [x] **第 1 段（案 B）をプラグインへ投入**: `GuiV2::BatchCmdWords()`。
      配置 438,784 -> 231,552 B（借用の 99.2% -> 52.3%）。検証器 群 4 を更新し異常 0 件
      ★**まだビルドしていない**

<!-- source line 2772 -->
- [x] 空いた 207,296 B の使い道を決めた（**F-343**。利用者の判断）
      **通知 2 -> 7 件**（借用は据え置き）+ 上画面 `LIST_SIZE` 0x20000 -> 0x28000
      配置 271,616 B（61%）/ 上の記録 103,728 B（0x28000 の 79%）。検証器 0 件・ビルド成功
      ★矩形の枠を画面ごとに分けた（上 86 / 下 56）。共通のままだと下画面が上限を超えた

<!-- source line 2776 -->
- [x] ★**手紙で落ちる件を直した（F-344）**。借用 0x6C000 -> 0x50000 / 通知 7 -> 5 /
      矩形 上 86 -> 74。配置 255,616 B（78%）。検証器 0 件・ビルド成功

<!-- source line 2778 -->
- [x] ★**実機で確認済み: 手紙が開ける**（F-346。利用者「手紙が開けました」）
      アトラス以外をプラグインの `.bss` へ移し、借用を 442,368 -> 36,864 B にした
      退避 `BACKUP/plugin_full_20260907_f346/`

<!-- source line 2783 -->
- [x] **キーボードの移植・ローカル検証・ビルド**（F-349。今回の依頼で過去の保留を解除）
      通常/小型×かな/カナ/QWERTY、数値DEC/HEX/小数。`DOCS/keyboard.md`。
      重なりなし5矩形の枠、`oIdx`をu16化。借用0x9000維持、plugin0x70000、下LIST_SIZE0x2D000。
      C++とSimulatorの10,943入力遷移/15描画場面/既存検証群/ARM構文検査後に3gx生成。

<!-- source line 2791 -->
- [x] ★**入力の無効化を実装した（F-350〜F-355）**。ケーブ 2 本 + 制御ブロック。
      A `0x0053CDF4`（ボタン一括 + タッチ）/ B `0x003534E0`（SELECT を読み替えの手前で消す）
      ★真因: ゲームは `sub_483020` で **SELECT を START に読み替えて bit2 を消す**

<!-- source line 2808 -->
- [x] **「ゲームスピード変更」チート `0054C6E8` の解析（F-356）**。
      `sub_54C684` = フレームペーシング（`sead::GameFrameworkCtrNw4c` vtable スロット 31、
      本作の派生は `UlcdFramework` / `sub_24F0A8`）。
      `MVN R0,#0xFF000000` で「前フレームの VBlank カウンタ」を巨大定数に置き換え、
      待ちループへ入らせない = フレーム制限の撤廃。

<!-- source line 2817 -->
- [x] **`this+0x70` を実機で確定 = 2（2 VBlank 待ち = 30fps）**（F-357）。

<!-- source line 2818 -->
- [x] **「FPS だけ上げて進行速度は据え置き」は不可能と確定**（F-357）。
      メインループ `sub_54C818` が 1 反復 = Calc 1 回 = 提示 1 回で、
      Calc へ dt が渡らない（`MethodTree_WalkAndInvoke(node)` のみ）。
      実測: `+0x70` 2->1 で周期 33.751->17.770 ms（1.899 倍速）。

<!-- source line 2829 -->
- [x] `BsFgProc::Setup` の正体を確定（`fgobj::Proc` のスロット 3 = `0x0059C974` ＋同名ヒープ）。
      **フィールド読み込み（準備中）の 1 ステップで、しずえ会話とは無関係**。

<!-- source line 2838 -->
- [x] しずえ会話スキップ: 経路を端から端まで確定（F-359）。
      `Room_UseExit(vc_ROOMDAT(), プレイヤー番号, 1, 0, 1, 1.0f)` を呼べば村へ出る。
      部屋 0x63 の出口表は 4 本で出口番号 = プレイヤー番号 0..3。

<!-- source line 2847 -->
- [x] ★**しずえ会話スキップ 実機で成功**（F-361。2026-09-08）。手順は `DOCS/skip_isabelle.md`。

<!-- source line 2872 -->
- [x] Resumeし、フレンドチャットではなく通常チャットを一回開く。

<!-- source line 2873 -->
- [x] 内蔵ソフトウェアキーボードが表示されたら、最初はキャンセルしてゲーム復帰を確認する。

<!-- source line 2874 -->
- [x] 再度Suspendし、`0x009BDD00` のstate/run count、Prepare/Start/Wait結果、
  `0x009BE138` のSwkbdResult、`0x009BE144/148` のtext offset/lengthを読み取る。

<!-- source line 2876 -->
- [x] キャンセル復帰が安全なら、かな入力→漢字確定を一回試し、共有ページのUTF-16結果と
  入力中の候補表示を別々に評価する。現在版は確定文字をゲーム内チャットへ送らない。

<!-- source line 2880 -->
- [x] 通常チャットを入口に内蔵ソフトウェアキーボードを起動。

<!-- source line 2881 -->
- [x] 最初はキャンセルし、APT状態0・ハンドル解放成功・ゲーム復帰を確認。

<!-- source line 2882 -->
- [x] パッチを残したまま通常チャットを閉じて再度開き、かなを入力して漢字候補を選ぶ。

<!-- source line 2883 -->
- [x] 右ボタンで確定後にSuspendし、`SYSTEM_KEYBOARD/read_native_chat_result.py` で
  `SwkbdResult`、text offset/length、共有ページのUTF-16確定文字を回収する。

<!-- source line 2901 -->
- [x] 入力変更経路と表示経路の2経路から、SWKBD内のapp pointer、表示候補cache、
  全候補数、選択index、表示件数を確定。

<!-- source line 2903 -->
- [x] 書込み・Resume・breakpointを行わない `read_live_candidates.py` を作成。

<!-- source line 2904 -->
- [x] 元ARM 8語、12候補fixture、折返しindex、異常系5件をオフライン検証してPASS。

<!-- source line 2905 -->
- [x] ACNLをResumeして内蔵SWKBDを開き、候補を表示したままRosalinaのProcess Listで
  `swkbd`を空いている通常GDBポート（第一候補4001）へ割り当てる。

<!-- source line 2907 -->
- [x] GDB接続でSWKBDをSuspendし、`read_live_candidates.py`相当の検証付き取得で入力・全候補数・
  選択index・表示中候補を取得する。ACNL用番地/スクリプトをSWKBDへ使わない。

<!-- source line 2909 -->
- [x] 表示候補の実機順位をF-363のPC再現と比較した。今回の差3件は候補末尾の文字種変換と確定。

<!-- source line 2914 -->
- [x] ACNLをSuspendしてもSWKBDが動き続けることを画面とACNL state=2で確認。

<!-- source line 2915 -->
- [x] 未確定`かんじ`を維持し、Rosalina Process Listで`swkbd`をport 4001へ割り当てた。

<!-- source line 2916 -->
- [x] port 4001へ`arm-none-eabi-gdb`で接続してSWKBD自身を一時Suspendした。

<!-- source line 2917 -->
- [x] 検証付き読取を行い、全17候補を回収後にdetachしてSWKBDをResumeした。

<!-- source line 2921 -->
- [x] `swkbd`をGDB port 4001へ割り当て、PID 60へ読み取り専用でattach。

<!-- source line 2922 -->
- [x] 実行コード全量照合、app pointer、入力cache、全候補数、選択index、表示cacheを回収。

<!-- source line 2923 -->
- [x] app全域から17件の88-byte候補recordを回収し、F-363の独立PC結果と照合。

<!-- source line 2924 -->
- [x] 特殊record 3件を供給済み原本ARMでローカル復号し、全17件の順位を確定。

<!-- source line 2925 -->
- [x] 各取得後にdetachしてSWKBDを再開。対象への書込み・breakpoint設置なし。
