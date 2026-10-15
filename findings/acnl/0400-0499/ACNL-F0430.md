---
id: ACNL-F0430
aliases:
- IDA-gpt-6-F001
title: 収録チートの天気返却と島チャット数字制限の意味（2026-10-11）
summary: '解析: IDA/idalib-mcp、実モデルgpt-6。主IDB acnl_jpn_v15_annotated.i64、code SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。既存gohan.md §17.8/JOKER・Adios・Vapecord原sourceの出自は変更しない。実機は操作せず確度MEDIUM（複数静的根拠）。'
date: '2026-10-11'
category: misc
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6481704
- 11338072
- 5756992
tags:
- chat
supersedes: []
source: IDA:work/FINDINGS.md:110-120
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F001: 収録チートの天気返却と島チャット数字制限の意味（2026-10-11）

- 解析: IDA/idalib-mcp、実モデルgpt-6。主IDB acnl_jpn_v15_annotated.i64、code SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。既存gohan.md §17.8/JOKER・Adios・Vapecord原sourceの出自は変更しない。実機は操作せず確度MEDIUM（複数静的根拠）。
- 天気: 原AR「曇り」の0x62E728=E3A00002は、現在の天気返却MOV R0,R4を値2へ固定するもの。JOKER選択2「くもり空」と既存仕様、直前の3→5/4→6変換をassemblyで照合。雨を冬に雪へ読み替える通常結果も返却固定で置き換わる。特殊部屋の早期returnはこのpatchへ到達しない。0..6の7ARと天気選択CPP2を個別に照合、4の「嵐」と「雨」の命名差は専用値の存在を意味しない。
- キーボード: vc_NUMBERS(0xAD0158)は複数の入力制約flags。島チャット初期化0x193A88はbit0x20を設定。BsSkbの送信処理は0x57D840/0x57DA98で同bitを調べ、sub_57D9A8→sub_747430→sub_3DEBD8へ進みUnicode数字の個数を閾値と比較する。原ARの低byte=2はVapecord morenumberisland/地域表JPNと一致し、この追加検査を外す。別bit0のclassifier sub_522894は単文字の数値範囲を判定し、word_AD0164にも依存する。数字専用の単純変数と断定しない。
- 数字カウント: NUL終端UTF16の半角/全角・上付き/下付き・ローマ・丸数字などを数えるleafをUtf16_CountNumericCharactersへrename、int(const unsigned short*)型を適用。NULLは-1。ASMの範囲/loopとcallerの閾値比較、Python Unicode分類を照合。閾値3/5は画面条件で選ばれ、原名「3文字以上」の一律の境界は保証しない。文字列provider実型や別の検査モードは未命名の理由をDBcommentへ記録。
- DB反映済み: 上記leaf rename/type、TextInputConstraintFlags bitfield enum（確認したbit0/0x20のみ）を定義し0xAD0158へ適用、既存vc名/RTTI名を保持、9箇所へ根拠コメント追記。idb_save成功、Enum size4を読戻し。XMLはcommit前に更新必須、現在Gitは利用者の全作業後一括指示で保留。
- 根拠: work/evidence/cheat_semantics/{weather_asm,initial_1,digit_filter,submit_limits,submit_numeric,numeric_count_wrapper,numeric_count_body,ida_rename,ida_comments}.jsonとreviewed_notes.json。実機効果/全入力flag副作用/0x949530天気CPP副作用は未確認。現物の文字数判定や天気が一致しなければ効果仮説は反証される。
- 追補: SystemConfig_ReadCountryId(元sub_34F8C8)はCFG block0xB0000/4bytesのhigh byteを返す。JOKER「サーバー変更」のJP/GB/KR/FR/US定数は、SystemConfig_GetCountryIsoCode(元sub_34FA24)が引く0x96EBC8の0xBB pointer tableと一致。全table bytesはIDBとSHA確認済み原codeで一致、stride4はindex命令で確定。ニュースcaller0x604BC4も同国情報をURLに使うため島だけの変更とはしない。2関数＋tableをrename/type、CFG IPC wrapperには確定範囲のみcomment（service init未追跡なので旧名保持）。MEDIUM、実機/原チート版全anchor未確認。country_{reader,news_caller,config_ipc,codes,code_table_ida}.json、review_country_override.py、66AR/native1の個別根拠。
- 中断時のDB追補: C4のentry/updateとpacked12B引数型、島runtimeのgetter/constructor/acre/building/item quadrant5関数とpacked0x102A型を保存・読戻し。静的MEDIUM、固定heapはLOW。C4はmarker frameでActor_PlaySoundを呼び、C5 repeat motionとは同bufferの別用途。島のfullwordは建物1の座標＋建物2のIDへまたがり、平地化追加書込みは現行JPNの名前文字列に重なる。未採用32候補は予備証拠として保持し、個別comment達成数へ加えない。根拠play_sound_c4_* / island_runtime_* / docs/topics/cheat_semantics.md。IDB save/close・最新XML/全入力bytes/hash・7関数/4型読戻しPASS、所有者0、実機操作なし。

