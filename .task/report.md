## 結果

完了。9型を番号の無い名前へ改名し、symbolsの関数型・依存型・コメント参照を統一した。全対象欄の位置と型サイズを作業用IDBで検査し、書出し後も対象9型・依存型の宣言に名前とコメント以外の変更が無いこと、旧型名の残存が0件であることを確認した。新規6記録は静的根拠に合わせMEDIUMとした（物理ZL/ZRの同定は未確認）。

gohanが使える型名とIDA上の大きさは次の通り。Prefixは部分型であり、sizeofを派生オブジェクトの確保サイズとして使わない。

| 型名 | IDA型サイズ | 用途 |
|---|---|---|
| SeadControllerBasePrefix | 0x134 | 共通欄。held、pointer_flags、axis0、edge、保持フレーム数、画素座標。 |
| SeadControllerPrefix | 0x15c | Controllerの既知prefix。先頭base、manager、addons、wrappers。 |
| SeadControllerWrapperPrefix | 0x194 | Wrapperの既知prefix。先頭base、source、enabled、source_bit_index。 |
| AcnlControllerOffsetList | 0x10 | addons / wrappers のリストヘッダー。 |
| AcnlPadReaderPrefix | 0x32 | previous_held と seed_previous_held を含むreaderの部分型。 |
| AcnlPadState | 0x10 | held / pressed / released と符号付き16-bit circle_x/y。 |
| AcnlUiPoint2 | 0x8 | float x/y。画素と軸で共用。 |
| AcnlUiPoint2I | 0x8 | int32 x/y。 |
| AcnlPointerFlags | 0x4 | Valid / Pressed / Released / ClearPosition。列挙子の接頭辞は AcnlPointerFlags_。 |

Controller/Wrapperの共通欄は `base.held`（先頭から+0x110）、`base.pointer_flags`（+0x10）、`base.axis0.x/y`（+0x11C/+0x120）。画素座標は `base.pixel_int.x/y`（+0x14/+0x18）、`base.pixel_float.x/y`（+0x114/+0x118）。`base` は先頭で、edgeは+4/+8/+0xC、保持フレーム数配列は+0x2C、button_countは+0xFC、axis0_bit/axis1_bitは+0x100/+0x104、pointer_bitは+0x108、idle_framesは+0x10C。パッドはheld/pressed/releasedが+0/+4/+8、circle_x/yが+0xC/+0xE。reader.previous_heldは+8、seed_previous_heldは+0x30。依頼の欄は全て一致した。

検査の詳細は `_local/evidence/109/layout.json`、`verification.json`、`symbol_delta.json`。作業用IDBの変更を `tools/sync/export_symbols.py` で書き出し、元からIDBとsymbolsで食い違っていた対象外の型宣言や自動関数追加は採用していない。Git/ghの直接実行、正本IDB、実機操作は行っていない。

検査: `python tools/audit.py` は 開始時の1023ファイルでは旧notes.mdのCRLFを1件検出。LF修正後、同じscan_fileで現在の全1024ファイルを再監査し問題0件。`python tools/kb.py lint` は761件・エラーなし。変更ファイル実内容の同じ監査器による追加検査も問題0件。

## 結論と根拠の要約

- ACNL-F0737: 番号無しの9型と対象欄を確定。Init、入力producer、edge計算、Wrapperの独立した静的参照を照合し、IDBと宣言差分でレイアウトを確認。
- ACNL-F0738: 0x003534C8は成功経路の全体ゼロ化分岐の合流後、履歴保存・条件付きSELECT統合の前。無条件かつ非PC相対のLDRだが、全体ゼロ化後の値を読む場合があり、失敗経路では通らない。
- ACNL-F0739: 装置padから読むのはheldとcircle_x/yで、padのedge語は読まない。装置+0x1634 bit0がボタン/軸、bit1がタッチを独立に制御。読み手の単一性は直書きオフセットと分割加算の検索範囲に限定。
- ACNL-F0740: 正常読取りでpad held bit13は除去され、下流転写にも受け皿は無い。bit12→held0x80は静的確認、物理ZLの同定とZRの全経路での非到達は実機未確認。
- ACNL-F0741: 0x0053CDE8で必要なローカル値はR4=self、R8=旧held、R9=旧valid。R0〜R3/R12/呼出し側保存VFPの装置更新後の値に後続処理の依存は無い。復帰・callee保存状態を壊してよいという意味ではない。
- ACNL-F0742: pad0x8→held0x800（START）、pad0x4→held0x1000（読み替え前SELECT）。旧SELECT時の0x8観測は上流統合後の装置キャッシュとして説明できる。

## 訂正の提案

- ACNL-F0379のSELECT=0x800、START=0x1000推定、および「生HIDの並びが逆」をACNL-F0742で訂正する。転写命令と上流の条件付き統合が独立に一致し、装置+0x15C0は既に読み替え後になり得る。旧実測の数値自体は否定せず、測定時の状態再現は未実施。
- ACNL-F0721/ACNL-F0723/ACNL-F0426はACNL-F0737のsupersedesに指定した。訂正範囲は旧型名・部分型の範囲表記のみで、各記録の他の結論を取り消す提案ではない。
- 事前確認の1は「SELECT読み替えの2経路の合流後」ではなく、全体ゼロ化の分岐の合流後。4は「held全体が更新されない」ではなく「ボタン/軸更新を飛ばす」。タッチ更新によるheldのpointer bit変更は起こり得る。

## 統合・重複の提案

ACNL-F0738はACNL-F0723の共通点D0を否定せず、より前の非PC相対点C8と全体ゼロ化の限定を補う。ACNL-F0741とF0737の欄一覧はF0721と重なるため、将来topics/acnl/input.mdへ整理できる。現時点で同カテゴリのtopicは無い。

## 新しいタグの提案

なし。

## 未確認点

CTRPF標準Hookの移設・呼出し規約・実機動作、読取り失敗の頻度と場面差、global byte0x009778D8の意味と書き手、全間接aliasの読み手、物理ZL/ZR、旧実測時のパッチ状態・global byte値。指定の事前確認ファイルは作業ツリーに無かったため、依頼文に転載された内容を使った。

## 次の1手

オーケストラが記録のbyを実行モデル情報からstampし、訂正範囲を確認して取り込む（現在の新規記録はkb.py new既定のby:auto）。gohanは上記型名で生成し直す。実機を許可した別作業でSELECT/STARTと読取り失敗時・タッチの組合せを同時観測する。
