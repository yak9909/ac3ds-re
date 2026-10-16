# 内蔵日本語辞書の取得と主要辞書の候補抽出（F-362）

2026-09-08。利用者がFILESへ配置したCIAをctrtoolで展開した。
目的は内蔵のかな→漢字辞書・候補の取得。自前メニューやgohan.3gxには依存しない。
ビルド、ゲームメモリの書き込み、実機の再開は行っていない。

## 取得できたもの

`FILES/extracted_system_keyboard/word_tables/japanese_main.csv` に、主要辞書2本の
**75,770レコード**を保存した。読み・候補のペアを重複除外すると**65,729組**。
これは辞書エントリの一覧であり、文脈・学習・品詞接続を反映した実機の候補順位ではない。

| ファイル | 取得・解析状態 |
|---|---|
| `JA_small/32/njubase1.a` | 全5,992レコードをCSV化、元のARM読取処理と全件一致 |
| `JA_small/32/njubase2.a` | 全69,778レコードをCSV化、元のARM読取処理と全件一致 |
| `JA_small/32/njtan.a` | 単漢字系の辞書種別0x00000002。原本取得済み、単語一覧化は未実施 |
| `JA_small/32/njfzk.a` | 付属語系の辞書種別0x00000001。原本取得済み、単語一覧化は未実施 |
| `JA_small/32/njexyomi.a` | 種別0x00040000。原本取得済み、読み/候補getterも特定。単語一覧化は未実施 |
| `JA_small/njcon.a` | 接続規則系の辞書種別0x000F0000。原本取得済み、接続規則の再現は未実施 |

辞書検索例（CSV中の重複を除いた候補。順番は実機順位ではない）:

- `かんじ`: 感じ、漢字、幹事、監事、寛治、完治、寛二
- `とうきょう`: 東京
- `どうぶつ`: 動物
- `あい`: 愛、あい、アイ、藍、間

## 入力と展開の検証

| 入力 | SHA-256 |
|---|---|
| `FILES/000400300000C002.0000000b (CTR-N-HKYJ).cia` | `a12eac5ce5834066d22c00c95953889e7e3d8d17c785ee8df5bcd5f61b605d9c` |
| `FILES/0004009B00011902.00000000 (CTR-P-CTAP).cia` | `516469805c1329f5edc3892804a83b1149792f8074c9b68ad342f8b230a19b25` |

ctrtool v1.3.0は[Project_CTR公式リリース](https://github.com/3DSGuy/Project_CTR/releases/tag/ctrtool-v1.3.0)から取得し、
`scratchpad/tools/ctrtool-v1.3.0/ctrtool.exe`へ配置。
`--verify --contents=...`でCIA内容を取り出し、続いてNCCHを
`--verify --exheader=... --exefsdir=... --romfsdir=...`で展開した。
正確な引数・終了コード・入力ハッシュは抽出ルートの`extraction_manifest.json`と`unpack_manifest.json`。

CIA内容ハッシュ、SWKBDのexheader/ExeFS/RomFSの内容ハッシュ、両RomFSのIVFC各階層はGOOD。
**Ticket/TMD/NCCHヘッダの署名はFAIL**。終了コード0と署名検証成功を混同しない。
復号済みNCCHであることは確認したが、署名不一致の原因までは確定していない。
各ディレクトリの`ctrtool_cia.log`/`ctrtool_ncch.log`に保存した。
ファイル名の`0000000b`やTMDのversionだけで現在の本体にインストールされた版を断定しない。
同時に提供されたsysnandダンプは今回の辞書取得に使っていない。

## キーボード本体との対応

**以下の番地はすべてSWKBDの番地。ACNLの同じ番地を呼んではいけない。**
`SYSTEM_KEYBOARD/prepare_elf.py`で展開codeをELFへ無変更で包み、別IDB
`FILES/extracted_system_keyboard/swkbd_jpn/swkbd.elf.i64`をidalibの`swkbd_jpn`で解析した。
textは0x00100000、rodataは0x001A0000、dataは0x001B3000。
コピーは全セグメントで元データと一致。ELFのBSS末尾は保守的なマッピングで、実行時変数配置の証明ではない。

- `0x0018C18C Swkbd_MountLanguageDictionary`: `0x001A4158`の表をlanguage index×16バイトで参照。
  ARMの`LSL #4`と`LDRD [entry,#8]`を確認。先頭エントリの内部言語値1、TitleIDは`0x0004009B00011902`。
  `dict:`としてマウントした後、言語別初期化を行う。
- `0x0018CDDC Swkbd_LoadLanguageDictionarySet`: 日本語の分岐で上記JA_smallの6ファイルを指定。
  抽出RomFSの実ファイル名との一致を確認した。
- 主要辞書はtype`0x00050000`。単純なUnix静的ライブラリではなくNJDC形式。
  [Qt 5.15に収録されたOpenWnnの辞書種別定義](https://github.com/qt/qtvirtualkeyboard/blob/5.15/src/plugins/openwnn/3rdparty/openwnn/wnnDictionary/include/nj_dic.h)にはこの種別がない。
  公開版の読取処理をそのまま使わず、提供されたSWKBD自身から形式を導いた。
  比較用ソースと取得ハッシュは`scratchpad/openwnn_reference/manifest.json`。

## 主要辞書レコードの形式

すべてファイル内オフセット。ヘッダ整数・文字列はビッグエンディアン。

| 位置 | 内容と根拠 |
|---|---|
| header+0x20 | 10バイト単語レコード領域。ARM `0x001677B0`〜`0x001677D4`が`base + 10*ID - 10`で計算 |
| header+0x24 | UTF-16BE文字列領域。読みgetter`0x00139E9C`と候補getter`0x00167708`の双方で参照 |
| header+0x28 | 文字列領域の次の領域。全参照の上限検査に使用 |
| header+0x50 | 単語数と整合する値。全件抽出・全ARM照合、および次行の領域境界式で検証 |
| header+0x64 | `records_base + 10*count`と一致する次領域 |
| record+0x00 | 読みのUTF-16長=`(byte >> 1) & 0x3F` |
| record+0x01..0x03 | 読み文字列の24ビット相対オフセット |
| record+0x04 | 候補のUTF-16長=`(byte >> 1) & 0x3F`、bit7は候補長0時のカタカナ化指定 |
| record+0x05..0x07 | 候補文字列の24ビット相対オフセット |
| record+0x08..0x09 | F-363で前後品詞表の索引と確認。頻度は別の2バイト/単語の表。詳細は`system_keyboard_conversion.md` |

候補長が0の場合、bit7なしなら読みをそのまま返す。bit7ありなら、読みのU+3041..U+3093を
U+0060だけ進めてカタカナ化する。`0x0014A494`と`0x0014E530`の分岐に対応する。
明示文字列62,426件、カタカナ化6,717件、読みそのまま6,627件。

## 再現と独立照合

```powershell
python SYSTEM_KEYBOARD/extract_dictionary.py
python SYSTEM_KEYBOARD/extract_dictionary.py --query かんじ
& 'C:/Users/<伏せ字>/anaconda3/python.exe' SYSTEM_KEYBOARD/verify_dictionary_arm.py --all
```

抽出スクリプトは出力前に全レコードを検査する。ヘッダサイズ、終端NJDC、領域間の順序、
レコード領域境界、全読み/候補の範囲と最大長、UTF-16BEの妥当性、埋込みNULを確認した。

独立照合はUnicorn 2.1.4で**元のARM命令を変更せず**、
`0x00139E9C`と`0x00167708`をPC内で実行した。
辞書オブジェクトは読取コードで確認したresident block形式で構築する。
OS・APT・実機・GDBを使わず、コードと辞書は読取専用、戻り先と命令数に上限を設定。
**75,770件すべてで読み・候補がPython結果と一致、不一致0件。**
`word_tables/verification_arm_all.json`に結果を保存した。
照合時のCSVのSHA-256は`afb312c8dbda5fa536c2713a017cdf2fbbc7f23daa475c4bc2040abfa88e037a`。
静的根拠は`SYSTEM_KEYBOARD/evidence/swkbd_dictionary_static.json`と専用IDBにも保存。

confidenceはプロジェクト基準では**MEDIUM**（複数静的証拠＋ローカルARM実行）。
実機上での動的観測を行ったという意味のHIGHにはしない。

## 残る確認

**F-363で順位・頻度/品詞・接続表・文節/学習の解析が進んだ。**
結果と現在の未検証範囲は[候補順位・文節変換](system_keyboard_conversion.md)を参照。
以下はF-362終了時点の記録。

- njtan/njfzk/njexyomiの単語一覧化、njconの接続規則の解析。
- 品詞・頻度・文節処理・予測/学習を使った候補生成と順位。CSVの単語検索だけでは再現しない。
- 実機で確定前の候補配列を観測する経路。
- ACNL/CTRPFからの安全な起動と復帰。F-359のAPT低位関数特定から先の実機確認は未実施。
  辞書の取得には今回これらの呼出しは必要なかった。
