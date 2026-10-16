# ゴミ箱の入場座標と既存選択肢 / IDA-gpt-6-F014・T017

2026-10-14、担当GPT-6/idalib。JPN更新code.bin SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。T016実機でtrashが依然未表示。今回修正版の実機成功は未確認。

## 入場時の座標

LetterDragWindowBaseのroot+632は0x31F2B8でpocketのN_pos_ltrへ実際にAppendChildされる。native background Submit 0x26EF4C→LayoutCalc 0x568030→root CalculateMtx 0x4B8EA0→Pane 0x4B6154。Paneはvisible bit0が落ち、DrawInfo+136 bit2も無いと、matrix更新と子の走査を省く。描画側0x73B524もvisible bitで子を省くが、描画とmatrix計算は別。

旧pluginはletter rootを隠してから、その子ボタンのworld matrixをゴミ箱の座標源にした。入場時に座標が画面外なら、親N_pos_ltrが移動してもhidden treeは古い座標のまま残る。原ARMによる独立probeは画面外中心[-560,-80,0]→親移動後も同値→DrawInfoの強制計算bit2で[150,-80,0]を再現し、rootのvisibleは0のまま。これは静的callerと別経路の証拠。実機の個別matrix値は未取得で、確度はMEDIUM。

修正はletterのアニメ評価だけを行い（時刻を進めず、引数のvisible-only bit0を外す）、background DrawInfoのbit2を一時有効にしてnative LayoutCalcを呼ぶ。flag全byteを元へ戻してから通常描画へ渡し、letter rootは非表示を維持する。AddLayoutを重ねず、trash自身のdrag禁止/click/drop/音/資源復帰を保つ。以前のPCfixtureはLayoutCalc/Draw/Bindをmockし、完成matrixを書いており、この失敗を検出できなかった。

## CHEATSの既存方式

利用者訂正により追加2項目の自作descriptor/文言は撤去。CHEATS ui.txt:L66とACNL_ALPCメニュー.txt:L16の「たべる」は0x19C150をNOP化、drop.txt:L6とメニュー.txt:L9の配置項目は0x19BFB0をNOP化。原JPN ARMの条件分岐はそれぞれ0x0A000009/0x0A000017。builderそのものがROMのindex43/action16、又は部屋条件に応じたindex15/21/22/action0やwall action42を作り、native PMFで実行する。別ビルド番地へ流用しない。

GUIの個別checkbox bit4/bit5へ対応付け、gohanのPatchListでcache flush込みの可逆切替とする。変更前の命令が自分の前状態と合わなければ競合通知し、他の変更を上書きしない。既存4追加項目は従来通り6行容量とcancelを保持。CHEATS由来コードの整理は再開しない。資料の該当部分を参照するだけ。

根拠work/evidence/gohan_pocket_trash_visibility、成果物artifacts/plugins/gohan_pocket_trash_visibility1。正常・旧15版/main/実機/SD/中断整理保持、全検証とDB/XML完了後に最後一括Git保存。

## 検証結果

原ARM probeと最新runtime3終了0。製品FrameStepからnative LayoutCalc/AnimateRecursive/CalculateMtx/Rect/Affineを実行し、hidden sourceの親移動に追従、hidden保持/全flagbyte復元/既存force bit保持/non-dragを確認。PatchList本体のSTRを実行し全64mask・OFF・競合拒否・flush呼出しを検証。元のbuilder部分を実行してROM text43/action16とtext15/action0の生成を確認。旧53＋新4=57case、75anchor21CPP/4334parser/font欠字0/linked/scroll、DB/XML122名73func注記14構造体2Enum/global/T/hash成功。FS/GPU/アニメ資源payloadとOS cacheflushはendpoint、実機の見た目/タイミングは未確認。途中fixtureの不存在Write32 symbolとimport不足を訂正し、製品の成否と混同しない。sourceと成果物hash・旧版保持はmanifestを正とする。
