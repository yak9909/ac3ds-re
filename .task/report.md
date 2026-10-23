## 結果

完了。現在のsymbolsからARM向け試験を生成し、-fno-short-enums無し・有りの両方で8構造体・55メンバー全てのoffsetofとsizeofがlayout_after.jsonに一致した。各構造体のsizeof・alignofも一致。F0737を最新の型名・メンバー・検証結果に更新した。新規記録の確度はMEDIUMのままで、実機操作はしていない。

gohanが使える現在の型名と大きさは次の通り。Prefixは既知の部分であり、sizeofは派生オブジェクトの確保サイズを表さない。

| 型名 | IDAの大きさ | ARMコンパイラの大きさ | 用途 |
|---|---|---|---|
| SeadControllerBasePrefix | 0x134 | 同じ | 共通欄。pointer_flagsはunsigned int、unk_12Cはfloat[2]。 |
| SeadControllerPrefix | 0x15C | 同じ | 先頭base、manager、SeadOffsetList型のaddons / wrappers。 |
| SeadControllerWrapperPrefix | 0x194 | 同じ | 先頭base、source、enabled、source_bit_index。 |
| SeadOffsetList | 0x10 | 同じ | prev / next / count / offset。offsetは要素からリストノードまでのバイト位置。 |
| AcnlPadReaderPrefix | 0x32 | 同じ | previous_held、bool resync_previous_held_pendingを含む部分型。 |
| AcnlPadState | 0x10 | 同じ | held / pressed / released、符号付き16-bit circle_x/y。 |
| AcnlUiPoint2 | 0x8 | 同じ | float x/y。 |
| AcnlUiPoint2I | 0x8 | 同じ | int x/y。 |
| AcnlPointerFlags | 4 | 既定1 / -fno-short-enums有り4 | 旗の列挙のみ。構造体の欄の型には使わない。 |

Controller / Wrapperは先頭のbaseを介して共通欄を使う。base.pointer_flagsは+0x10、4バイトのunsigned int。base.heldは+0x110、base.axis0.x/yは+0x11C/+0x120、base.unk_12Cは+0x12Cのfloat[2]。SeadOffsetList.offsetは+0xC。reader.previous_heldは+8、bool resync_previous_held_pendingは+0x30で、真なら次の読取りで履歴を同期してから消える。全対象欄の位置・大きさはIDAとコンパイラの両設定で一致した。

試験にはlocal_types.hから抽出した宣言を使い、IDA固有の整数型の綴りと__bitmask注記だけを適応した。コンパイラはdevkitARM release 61 / arm-none-eabi-g++ 13.1.0、ARMv6K。列挙単体の大きさは設定で変わるが、格納欄をunsigned intにしたため後続位置に影響しない。SeadOffsetList、offset、float配列、boolの変更は既に別ワーカーがIDBとsymbolsへ反映した状態を検証した。今回IDBは開いていない。

証拠は作業場基準の `_local/evidence/109/`。layout_after.jsonが修正後のIDA値、layout_test_after.cppが生成試験、layout_test_after.logがコンパイルログ、layout_test_after_results.jsonが両設定の全測定値と入力SHA-256、verify_arm_layout.pyが再現手順。作業ツリー内に_localは作らない。

検査: lint: 761 件の記録、エラーなし。audit: 1024 ファイル、問題 0 件。いずれもtools用venvのPythonで成功。今回変更したファイルの実内容も同じ監査器で問題0件。

## 結論と根拠の要約

- ACNL-F0737: 現在の型名・欄の型に更新。pointer_flagsはunsigned int、リストはSeadOffsetList.offset、unk_12Cはfloat[2]、readerの同期旗はbool resync_previous_held_pending。ARMコンパイラの両設定で8構造体・55メンバーの位置と大きさがIDAに一致。
- ACNL-F0738: 0x003534C8は成功経路の全体ゼロ化分岐の合流後、履歴保存・条件付きSELECT統合の前。無条件かつ非PC相対のLDRだが、全体ゼロ化後の値を読む場合があり、失敗経路では通らない。
- ACNL-F0739: 装置padから読むのはheldとcircle_x/yで、padのedge語は読まない。装置+0x1634 bit0がボタン/軸、bit1がタッチを独立に制御。読み手の単一性は直書きオフセットと分割加算の検索範囲に限定。
- ACNL-F0740: 正常読取りでpad held bit13は除去され、下流転写にも受け皿は無い。bit12→held0x80は静的確認、物理ZLの同定とZRの全経路での非到達は実機未確認。
- ACNL-F0741: 0x0053CDE8で必要なローカル値はR4=self、R8=旧held、R9=旧valid。R0〜R3/R12/呼出し側保存VFPの装置更新後の値に後続処理の依存は無い。復帰・callee保存状態を壊してよいという意味ではない。
- ACNL-F0742: pad0x8→held0x800（START）、pad0x4→held0x1000（読み替え前SELECT）。旧SELECT時の0x8観測は上流統合後の装置キャッシュとして説明できる。

## 訂正の提案

ACNL-F0737とACNL-F0742のsupersedesは空にした。以下はいずれも一部の訂正（kind=partial）として提案する。旧記録をstate: supersededにする関係ではない。

`kb.py relate --file` に渡せるTSVの行:

```tsv
before	after	kind
ACNL-F0721	ACNL-F0737	partial
ACNL-F0723	ACNL-F0737	partial
ACNL-F0426	ACNL-F0737	partial
ACNL-F0379	ACNL-F0742	partial
```

- ACNL-F0721・F0723・F0426 → ACNL-F0737: 型名・欄の型と部分型である旨の更新。F0721の離し・旧状態R8/R9の扱いなど、各記録の結論は有効。
- ACNL-F0379 → ACNL-F0742: 訂正する範囲は0x800をSELECTのbitと呼んだ名前づけ。読み替えが働く時にSELECT単独で0x800が立つ実測とは整合し、その実測を取り消さない。転写命令と上流の条件付き統合から区別できるが、旧測定時の状態再現は未実施。
- 事前確認の1は「SELECT読み替えの2経路の合流後」ではなく、全体ゼロ化の分岐の合流後。4は「held全体が更新されない」ではなく「ボタン/軸更新を飛ばす」。タッチ更新によるheldのpointer bit変更は起こり得る。

## 統合・重複の提案

ACNL-F0738はACNL-F0723の共通点D0を否定せず、より前の非PC相対点C8と全体ゼロ化の限定を補う。ACNL-F0741とF0737の欄一覧はF0721と重なるため、将来topics/acnl/input.mdへ整理できる。現時点で同カテゴリのtopicは無い。

## 新しいタグの提案

なし。

## 未確認点

CTRPF標準Hookの移設・呼出し規約・実機動作、読取り失敗の頻度と場面差、global byte0x009778D8の意味と書き手、全間接aliasの読み手、物理ZL/ZR、旧実測時のパッチ状態・global byte値。指定の事前確認ファイルは作業ツリーに無かったため、依頼文に転載された内容を使った。

## 次の1手

オーケストラが上記TSVのkind=partialの関係をkb.py relateで適用し、取り込む。supersedesはF0737/F0742とも空のまま。gohanは上記型名で生成し直す。実機を許可した別作業でSELECT/STARTと読取り失敗時・タッチの組合せを同時観測する。
