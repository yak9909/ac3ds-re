---
id: ACNL-F0433
aliases:
- TreeSitter-gpt-6-F001
title: C++由来107チート本体の局所化と部分集合の実出力照合（2026-10-10）
summary: '2026-10-11 CHEATSのみの追補: message(5).cppは施設状態変更8callbackと8tableを含み、原型CHARS_U8_MAP/items宣言は欠ける。原range-forのiは局所変数なのに旧scoped閉包が別drop.cppのiへ束縛していたため、CHEATS専用contractで原AST/range declarator/table/Write8と字面以外の束縛を照合し当該偽依存を除外。局所u8 id/const char*nameとv'
date: '2026-10-10'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:136-163
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## TreeSitter-gpt-6-F001: C++由来107チート本体の局所化と部分集合の実出力照合（2026-10-10）

- 2026-10-11 CHEATSのみの追補: message(5).cppは施設状態変更8callbackと8tableを含み、原型CHARS_U8_MAP/items宣言は欠ける。原range-forのiは局所変数なのに旧scoped閉包が別drop.cppのiへ束縛していたため、CHEATS専用contractで原AST/range declarator/table/Write8と字面以外の束縛を照合し当該偽依存を除外。局所u8 id/const char*nameとvector<string>は明示的な補完で元型復元としない。原fileそのもの対char*/u32・string/u8の2仮定baselineと実生成bodyのhost320条件（全選択肢/負値取消/Write拒否/繰返し、窓/全byte）一致、8個別/結合ARM C++11と原body token/全table/hash PASS。CheatsNativeReviewへ収録、原55file/3097候補を2381関数/3047原候補＋metadata50、CHEATS未処理0へ一意partitionし専用台帳/CHEATS.mdを出力。MEDIUM（観測可能なソース補完契約）、LOW（欠落原型/固定番地・対象版/意味・保存/反映/実機）。正の範囲外choice、AR runtime全体、実機は未検証。CTRPF生成20fileはhash不変、中断維持。根拠cheats_facility_contract_gate.json/cheats_facility_generation_report.json/cheats_scope_gate.jsonとCHEATS専用ログ。
- 2026-10-11中断時の訂正/根拠: 原mainのSetupLanguage(false)を専用startupへspecializeし、Configの実17method call閉包・元型/path/version/File/窓/再帰を同じ局所型へ合成。原3CPPそのもの対host246条件＋ARM C++17 PASS。File/Directory/System/窓は自メモリのmock、SD/実機/壊れたoffsetは未検証。Lifecycle31試行は旧NotifySysFont/Item等未解決で全失敗、採用0。初回成功した両NPCFunctionはstatic CurrAddress writerと別4callbackの参照から消費側合成が必要と分かり撤回。Process::ReadString等の読み取りsignalだけではselectorの完結を証明しない。source_proven_withdrawals/shared_state_consumers.pyへ原宣言/writer AST/非shadow consumer/body hashを保存、全verifierが再構成しPASS_PARTIAL。全2644/955不変、MEDIUM（ソース契約）、実機未確認。利用者指示によりCTRPF作業は中断、CHEATS由来だけへ移行。根拠language_startup_contract_gate.json/lifecycle_generation_report.json/collection_gate.json。
- 2026-10-11 stateful Languageの契約: 両実Language header/CPPは同hash、TextID表は異なる。TextIDはglobal enumで、main→Config::SetupLanguage(false)が設定・言語binaryを読み込む。CPP5method＋inline/default/data fieldを局所classへ移し、唯一のstatic instance=nullptrは同じLanguage*&型のprivate static storage getterで保持する。CPPの3参照だけを変換、field layoutとconst/default/戻り値・引数を保持。実原Language.cpp/headerを直接compileした対照とのhost384条件とARM C++17構文PASS（size/align/型/同一singleton/get/load/選択・File失敗/繰返し/trace）。確度MEDIUM（ソース契約）、SDK Fileは自byte配列mock、SD/実機/原malformed offsetは未確認。source kernelだけでは未loadなのでcallback採用数へ加えない。language_class_contract_gate.json、language_source_contract.py、verify_language_contract.py。
- lifecycleの静的根拠: Language依存287未処理callback、うち52は元closureにgameplay effect signalなし。原mainのfalse引数、原Configの設定read/writeとFiles.h/Config.hpp、両版version341/331を照合。current SDKにUpdateLocalizedEntries APIがないが原SetupLanguageのtrue経路だけであり、startup falseへのspecializationは独立照合後に採用可能（未実装）。bootstrapのHomeMenu/File作用を設定消費側の代用にしない。全2644/955未処理、language_lifecycle_queue.json、analyze_language_lifecycle.py。
- 2026-10-11 template/namespace続報: 実両版Address.hppのCallはT(*)(Args...)による値引数call、WriteはC++17 if constexpr/is_same_vでu32→Patch/u16/u8/float/u64→各Process API/他型false。local class member templateは使えないため、新TemplateAddressReviewだけreceiver先行一度評価・明示型と値引数変換・constexpr分岐を保持するgeneric lambdaへ変換する。原body/bytes/hashは別に保持して変換expression/full再構成を照合、通常stageの原token保持とは区別。実原template定義対host208条件一致（void/scalar/混合8引数/明示型/参照/非自明copy/評価順/unsupported型・拒否/繰返し）、backend/mock、自己processの実u32 code/dataだけ。アドレスの現行版一致/callee型/実機はLOW、変換契約はMEDIUM。address_template_contract_gate.json、lower_address_templates.py。
- namespace補正/独立照合: qualified namespace定義は外側namespaceと実header prototypeの祖先/型/defaultの2sourceで識別し、classと混同しない。型forwardと実definitionの同scope一致を確認して先行宣言を保持。親の通常/匿名helperと兄弟namespace capsuleのstatic methodを局所Contextへ置き、元の関数pointer型と呼出しを保持する。実Game/GameKeyboard/Inventory helper本体対完全生成prefixをhost624条件で比較、一致/arena不変/trace/static pointer型PASS。master無効keyboard pointerの生読取りは未実行、SDK Read/Address解決はmock、実機証明ではない。10関数追加、全2644/3361原候補/955group未処理、ARM C++17・実出力全partition gate PASS_PARTIAL。namespace_contract_gate.json、localize_namespaces.py、generate_declaration_collection.py、verify_namespace_contract.py。
- 解析ソフト: Tree-sitter / 補助: GNU ARM C++11コンパイラ、原ファイルbytes/SHA検査。モデル: gpt-6（今回のsystem表記）。この段階はソース解析のみでIDA/Ghidra/実機を使っていないため、実際のソース解析器をIDへ記載する。元の全件抽出/重複整理はIDA-gpt-6.1-sol-F018（前担当記録）として帰属を保つ。
- 対象: `reference/old_project/REFERENCES/CHEATS`と`CTRPF PROJECTS`の台帳4417候補。原2498fileのSHAはinputs.jsonで保持。出力は独立gohan作業枝`work/reference-cheat-collection`の`reference/cheat_collection`、原本不変。
- 107 callback/152原候補をNativeReview.hpp/.cppへ収録。閉じた関数、または固定幅整数のtypedefだけが依存にある関数を採用し、型別名47件も各関数内へ移設。変数や状態をファイル外へ作らず、原登録/ホットキー/別名/出典をコメントへ保存。改行/末尾空白の整形はraw string不存在とtoken同一を確認して行う。
- 独立照合: 原ファイルを再読し物理bytes切片/全出典hash/原body tokenを確認する経路、実生成定義/ヘッダ/関数外宣言とARM C++11コンパイルを確認する経路。個別109試行で107成功、2件はPlayer型/Hotkeys名前空間の未解決として保留。依存抽出の閉包だけでは完結を証明できないことも実証した。結合cpp構文PASS。
- 全体AR2367＋native107=2474関数、3185原候補。全4417候補のgroupは生成/理由付き未処理1125group/攻撃専用の非実行記録31groupへ一意に分かれる。実出力/原bytes/hash/定義とヘッダ/状態局所化は`PASS_PARTIAL`。全件の変換は未完了。
- 確度: MEDIUM（ソースの局所化・原処理保持・構文と対応）、LOW（ゲームの意味/名前/地域・更新版の一致）。実機未確認。反証/残課題: 不一致出典bytes、未解決依存、異なるbuildのアドレス、原コード自身の未初期化/不適切書込み、ループ等のAR原engineとの実行意味差。部分gateを全件完了や実機成功へ昇格しない。
- 根拠: `tools/cheat_collection/generate_native_collection.py`、`verify_collection.py`、`refresh_collection.py`、`work/evidence/cheat_collection/{native_generation_report,collection_gate,ar_source_and_syntax}.json`、`work/logs/cheat_collection_native_*.log`、gohanのprovenance/status/pending。

- 続報Address局所化: 原Address.hpp/.cpp/Addresses.hppからenum/TitleID/全tableとmethodを抽出し、元callback tokenを保持して46関数をAddressReviewへ追加。13試行は他依存不足で保留。全2520関数/1079group未処理。原3.4.1は11method・Read32失敗で0保存、masterは10method・直接readと異なる初期region/LoadRegion署名を持つ。推測の共通化は行わず各原本を保持。
- 独立実行照合: upstream Address.cppそのものをmock Process＋host自身のVirtualAlloc arenaでcompileし、生成local classと比較。両版の全table row/8地域＋EURWL/不明TitleID、default/copy/offset/branch decode/patch拒否/unpatch/再読/繰返しcallbackを20実行で照合PASS_HOST_CONTRACT。masterの無効アドレス直接readは未試験。関数ごとのprivate cache分離と初回LoadRegionは利用者の局所化要件による差としてコメント記載。実機HIGHに昇格しない。根拠address_generation_report/address_contract_gate/collection_gate.json、generate_address_collection.py/verify_address_contract.py。

- 2026-10-11続報: ID表Power.txtの実チート雛形を拾い直し原4418候補へ訂正、旧全group IDを保持。XX6雛形をuint8配列引数へ変換して原行/hash/ARM構文を照合。相手権限回避drop断片は非実行metadataのみ。refined sidecarはtype fieldのstd::string等を宣言名と誤認する208宣言を修正し、939閉包が変化した（元group/出自不変）。通常helper/overload/defaultを局所化してDeclarationReview63関数、原FOXXY SDKを使うLegacyReview23関数を追加。全2612関数/3329原候補/987group未処理、全実出力gate PASS_PARTIAL。根拠cpp_dependency_refinement_report.json、declaration_generation_report.json、legacy_generation_report.json、collection_gate.json。
- helper独立照合: 原SetUpKB三overloadと原prototypeを直接host compileし、実原Keyboard.hpp＋mock backendを介してlocal class/functorと18条件（型3種/defaultと明示callback/成功・取消・error/繰返し）で結果・callback副作用・設定の一致を確認。PASS_HOST_HELPER_CONTRACT、確度MEDIUM（ソース移設）、実機/表示・番地一致は未検証。keyboard_helper_contract_gate.json、verify_keyboard_helper_contract.py。原SDKのInputChangeEvent/OnInputChangeと現行KeyboardEventは型/APIが違い、単なる置換は採用しない。
- scope続報: 新sidecarはqualified末尾の裸名混入、参照引数名/parenthesized関数pointer名、preproc_arg内の参照を補正。実Makefileのliteral include経路とheaderのusingを追跡し、824閉包変更/97依存record追加。JOKERのZstd/Gameは原クラスAPI＋実Game.cpp＋camera callerが固有ゲーム補助処理を示し、圧縮ライブラリという旧folder分類を依存sidecarだけで訂正。元group/旧・refined来歴は不変、完全C++bindingは未証明。Scoped17/ScopedLegacy1、検証済みAddress全表/method/private cacheと他依存を合成したScopedAddress4を追加。全2634関数/3351原候補/965group未処理、PASS_PARTIAL。
- static class独立照合: data/virtual/base/templateを持たない原static APIだけを対象に、参照されるmethodをlocal classへ移し、未使用prototypeを除く。元Game.cppと元Game.hppそのものをhost compileし、local classのCameraAddrPtr/CameraRotX/Yを自プロセスの割当だけで256条件照合、値とstatic関数pointer型が一致。SDK Processはmock、他Game method/実機/ARM実行は未試験。確度MEDIUM（局所化/署名）、番地の現行版一致はLOW。static_class_contract_gate.json、verify_static_class_contract.py、scope_cpp_dependencies.py、scoped_*_generation_report.json、collection_gate.json。実生成helper本体のtokenも独立に検査する。

> 既存記録の解析ソフト: IDA / 解析モデル: unknown（利用者指定）。2026-09-19のID移行・文書編集: gpt-6-astra。本文の解析結果と確度は変更していない。新規記録は実際の担当モデルを記載する。規則: [record_ids](../docs/record_ids.md)、対応表: `record_ids.IDA.json`。

旧版F番号は `reference/old_project/RE/FINDINGS.md` に保管。現在のIDは解析ソフト/モデルを含む完全IDとし、旧番号は対応表と出典で引く。

