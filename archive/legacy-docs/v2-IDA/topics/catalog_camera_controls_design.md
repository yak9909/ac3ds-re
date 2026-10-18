# リスト操作と模様替え中のカメラ移動

IDA-gpt-6.1-sol-F015 / T002、2026-10-10。新追加は実機未確認、静的MEDIUM。基点15d7aeb1（hhd_room_camera1）は利用者実機PASS。

## 最新要件と方針

- 開いているリストの背後にある開くタブとACNL InteriorEditorをフェードで隠す。リスト内の上段・カテゴリ・品の一覧は表示する。閉じると表示を戻す。
- Xは最後に実際に開けたリスト（家具/壁家具/壁紙床）を開く。初回は家具。各リストのカテゴリ/スクロール記憶を既存のまま使う。Xの押下edgeだけを使い、読み込み/出入りの途中やメニュー中は二重要求しない。
- B閉じるはInputStepに既に実装済みなので維持する。
- 家具/壁家具のカテゴリ行だけ0x01000413（SE_SYS_BOOK_ICON_SELECTED、GROUP_STATIC）を使う。上段Tabの決定音は現行0x0100046Cを維持する。スクロールでカテゴリ境界が変わる場合もカテゴリ選択音へ揃える。
- 利用者追加回答により、スライドパッドpanはHHDカメラONかつ模様替えmode25だけ。通常室内のプレイヤー操作は保持する。リスト/メニュー/入力禁止中は停止。

## フェードの根拠と設計

ModuleIndoor Editor_SubmitLayouts 0xB3DD10とChip_SubmitLayouts 0xB430F0のassembly/別経路を照合。対象Layoutはeditor+664、chip+1176+i*1120+36（112枠）、range+128200+36。Layout中のnw::lyt::Layoutは+16、rootPaneはそこから+16。子リングはPane+20、linkはchild+4。

本体nwlyt_Pane_CalculateMtx 0x4B6154がアニメ用alpha+180から描画用globalAlpha+181を作る。nwlyt_Pane_DrawRecursive 0x73B524はglobalAlphaを描画へ渡す。root alphaだけではinfluencedのない子を隠せないため、コマンド生成0x4D7174のMITMで対象treeのglobalAlphaだけを一時乗算する。元の全byteを退避し、native描画後に必ず復元。localAlpha、可視bit、親、アニメ、Submit回数を変更しない。他のUIとリスト内容は対象にしない。

6フレームのopacityをリスト状態から更新する。Loading/Opening/Open/Closing中に0へ、Closedで255へ戻す。退場/失敗/scene変更は対象を解除。treeの退避はプラグイン私有の固定領域、深さ/容量を越えた場合は復元してnativeへ渡す。既存GuiRendererの同関数末尾hookは保持し、入口MITMの原bytes/6地点を検査して導入する。ゲームheap/caveを追加しない。

## panの根拠と設計

CameraGame_UpdateEye 0x1A15B0の原命令とsin/cos表0x89B680より、yaw0ではeyeは注視点の+Z側。水平forward=(-sin(yaw),-cos(yaw))、right=(cos(yaw),-sin(yaw))。上へ倒した入力をforwardへ、右をrightへ投影する。AngleU16_Sin 0x47D2C4/Cos 0x47D28CはR0=u16角、返値S0のhard-float ABIを使用。

panX/Zはゲームスレッド私有。native ApplyTargetが作った基準位置へ毎回加えるため累積二重加算しない。Yは変更しない。カメラ/部屋/scene/ON世代変更とOFFで0へ戻す。特殊modeでは表示適用を止め、native演出へ任せる。mode25だけでアナログを取得し、非模様替え時はpanを表示しない。斜め入力は大きさを正規化し、中心の小さな揺れを除く。

## 検証

原SHA/ARM32 LE/imagebase/ロード範囲/T=0、main/CROの独立6地点を照合。ソース→必須しずえ→ビルド→linked全分岐/リテラル/境界/ABI/VFP/領域/hashの順。panは四方と斜めyaw、analog中心/最大/斜め、mode0/25/特殊、list/menu/禁止、OFF/scene変更を検査。フェードは対象のnative tree draw、子alpha、別UI、tree容量/深さ、後始末と全bytes復元を検査する。Xの最初/3種最後タブ/失敗/長押し/再開/遷移/Bの既存経路も検査。

各DBへ確定概念の型/コメントを保存し、最新XML/bytesを検証する。新作業枝work/catalog-camera-controlsへpush、hhd_room_camera1は復元用として保持する。こちらから実機へ書込み/Resumeしない。新追加の実機確認は利用者が行う。
