# F-398: 内蔵キーボードを開かずPCから日本語候補を取得

追記（F-407）: 3DS実機でも、アプレットを起動せず独立contextから17/6/143候補を取得・原本と順位一致。
内蔵タイトルからコード/辞書をRAMへ読み、SD/3gxへの同梱は不要だった。
最新は [ネイティブ検証結果](system_keyboard_native_loader.md)。以下はF-398時点のPC解析記録。

2026-09-10。原本ARMと提供済み辞書をUnicornで実行し、保存済み実機の
「かんじ」17件、「わたしはねこがすきです」6件を順序込みで再現した。
実機への接続・書込み・ビルド・3gx変更は行っていない。

## 不足していた初期化

旧Probeはファイル辞書slot2..6を登録するが、関数型辞書slot7..9を省略していた。
日本語初期化0x18CDDCの0x18D238..0x18D354は次を登録する。
エントリはctx+236+36*slot、種別byte+0=1、関数pointer+4、頻度u16六個+20。
その他の欄は0。ctxはapp+8。

| slot | 関数 | 頻度六個 |
|---|---|---|
| 7 | 0x19BECC | 0,0,10,0,10,0 |
| 8 | 0x19C334 | 10,0,950,1000,10,0 |
| 9 | 0x16B890 | 0,0,10,0,10,0 |

idalibの逆コンパイルとSTR/STRH/STRBの命令列を照合。
さらに二つの保存済み実機appで各36 bytesがPC構築値と完全一致した（HIGH）。
これらを0x18C628の前に登録すると、同じ0x111FD4の戻り時点で17件/6件になる。
欠けていた3件/5件のrecord+16は0x19BECC。表記変換も原本処理を実行する。
UI側で文字列を足す処理を自作したわけではない。

**F-397の「wrapper直後1件→UI段階6件」は初期化不足による比較だった。**
追加時点の差という解釈は撤回する。旧Probeの既定値は過去試験再現用に維持し、
新APIだけui_callbacks=Trueを指定する。

## 取得方法

リポジトリ直下で実行:

```powershell
python -X utf8 SYSTEM_KEYBOARD/query_candidates.py "わたしはねこがすきです"
python -X utf8 SYSTEM_KEYBOARD/query_candidates.py "かんじ" --output scratchpad/candidates.json
python -X utf8 SYSTEM_KEYBOARD/verify_full_candidates.py
```

APIはSYSTEM_KEYBOARD.query_candidates.query_candidates(text, limit=300)。
毎回新規の未学習contextを使用。入力1..55 UTF-16 code units、NUL不可。
最初に0x111FD4(mode0)、続いて原本getter0x1181D0を順に呼ぶ。
このgetterは初期50件を超えると0x11768Cへ追加検索を要求する。
0x1099DCのUI列挙上限に合わせ最大300件。limit_reached=trueの場合、
全件取得済みとは判断しない。exhausted=trueはgetterの0戻りを確認した場合のみ。
OSやmutexの模擬実装は不要。

## 検証

証拠SYSTEM_KEYBOARD/evidence/f398_full_candidates.json、f398_initializer_asm.json。
二つの実機候補列と完全一致し、別の原本record decoderでも同じ文字列を確認。
旧初期化14件/1件が維持されること、件数制限、不正入力4件の拒否も確認した。
追加PC試験: あ49件、か143件、し195件、とうきょう4件、123は2件。
「か」「し」は初期50件を超えて取得できる。追加入力は実機比較済みではない。

文章の6件は「私は猫が好きです」「わたしはねこがすきです」
「ワタシハネコガスキです」「ﾜﾀｼﾊﾈｺｶﾞｽｷです」
「ワタシハネコガスキデス」「ﾜﾀｼﾊﾈｺｶﾞｽｷﾃﾞｽ」。

今回達成したのはPCでの日本語予測候補取得。実機の個人学習・ユーザー辞書は
取り込んでおらず、全入力・全設定で実機と一致する保証はない。
3DS上でアプレットを起動せず同じAPIを利用する方法は引き続き未検証。
自前メニューやgohanへの組込みを前提にしていない。
