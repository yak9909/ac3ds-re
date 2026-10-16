# 引き継ぎ — F-241 loader lifecycle trace の失敗と安全な再開

最終更新: 2026-09-02

この文書は、GPU 自前チートメニューの「ロード中にも上画面で常に描く」経路を調べるために入れた
F-240 lifecycle trace がクラッシュした件の完全な引き継ぎである。
次担当は、`AGENTS.md`、本書、`RE/STATE.md`、`RE/TODO.md` の F-241 節、
`RE/FINDINGS.md` の F-239〜F-241 を読むまで動的作業をしないこと。

## 現在の実機状態

- F-241 で loader Layout の heap object を破損した。停止 PC は stock
  `LayoutList_SetDisplay` の `0x00566E44` であり、正常な停止状態ではない。
- game/GPU state を安全に戻せる範囲の処理は完了した。
  `0x005683E4=0xEB09218F`、`0x001280CC=0xE92D41F0`、software breakpoint 0 件。
- `probe_loader_submit_lifecycle.py` の uninstall と独立 read-back により、
  cave `0x00838D20..0x00838EA4` と LOG `0x009B3000..0x009B4240` は zero を確認した。
- ただし Layout の破損前 `+4/+8/+C` は保存していない。**現在のゲームを Resume しない。**
  ユーザーがゲームを再起動し、IDA Remote GDB Debugger で再アタッチする必要がある。

## F-241 の原因（HIGH）

F-240 trace は `0x5683E4`（nonzero Layout replay の直前）と
`0x1280CC`（`GpuCmd_SplitAndSubmit` entry）をフックした。ログ自体は
`0x009B3000` で、`code.bin.i64` の `.bss` (`0x97C768..0xAF2694`, RW) にある。
従って原因は `.text` / 未マップ領域への CPU write ではない。

共通 emitter は次の危険な block copy を使っていた。

```arm
LDMIA R2, {R0-R3}
STMIA R1!, {R0-R3}
```

replay stage の第2 word は Layout pointer である。最初の `LDMIA` は `R1` を
`0x3225A2B4`（loader Layout）に変えるため、次の `STMIA` は LOG ではなくその Layout へ書く。
しかも STM の base `R1` は register list にも含まれる。

二つの独立した実機証拠は一致した。

1. fault context は `PC=0x00838E60`、`R1=0x3225A2C4`、`R2=0x0000001A`。
   これは第一 STM の 16-byte writeback と、次の `ADD R2,#0x10` 後の `id 0x0A` と整合する。
2. 停止中の `0x3225A2B4` 先頭は実際に
   `{0x00000001, 0x3225A2C4, 0x0000000A, 0x00000000}` だった。

Layout vptr が失われたため、ケーブを脱出して hook を戻しても、後続 stock
`LayoutList_SetDisplay(0x566E30)` が不正な Layout を使って再び SIGSEGV した。
これはゲーム本体の loader/replay 構造の反証ではなく、観測ケーブ自身の register lifetime 欠陥である。

## 禁止事項

- `PATCHES/probe_loader_submit_lifecycle.py` の `MODE_OVERRIDE="install"` を使わない。
  script は F-241 guard で RuntimeError を返すよう変更済みであり、guard を外してはいけない。
- `LDM/STM` の block copy で、destination register を LDM の register list に含めない。
  base register 自身を STM list に含めることも禁止する。
- 現 boot の heap pointer、loader Layout pointer、record manager pointer を再利用しない。
- F-235 tail natural-submission、F-201 型の cursor 改変、F-238 auto-reorder を混ぜない。
- いきなり UI画像（スプライト）、order 変更、buffer extension、submit hook を組み合わせない。

## 再起動・再アタッチ後の安全な開始順

1. ユーザーにゲーム再起動と IDA 再アタッチをしてもらい、手動 Suspend を依頼する。
2. **依頼前に** ida-pro-mcp で `state==-1`、PC、SP、LR、BP数を読み、`RE/STATE.md` と比較する。
   実行時 heap address は boot ごとに再取得する。
3. 静的な確認は必ず idalib-mcp の `code.bin.i64`（`acnl_code`）で行い、終わったら close する。
   debug IDB の xref を静的根拠にしない。
4. `0x5683E4` と `0x1280CC` が stock、候補 cave が zero、候補 LOG が `.bss` 内で zero かつ
   現用テーブルと重ならないことを、**別経路二つ**で確認する。
5. 新規 trace は最初に replay hook **一箇所だけ**を使う。outer `PUSH {R0-R3,R12,LR}` のあと、
   `R12=LOG`、定数を一時 register に置き、`STR` **1語だけ**を private LOG に書く。
   `POP` 後は stock BL と stock resume をそのまま通す。submit hook、LDM、STM、loop、ring はまだ入れない。
6. `run_timed.py` で短時間だけ実行し、停止後に LOG 値、hook stock復元、cave/log zero を確認する。
   その最小 trace が複数回安定してから、第二の 1 word field を足す。

## loader 解析として保持する知見

- F-234: visible loader transition の上画面 replay は `id 8 (len 0x180) -> id 10 (len 0x2C0)`。
- `id 10` Layout は `tc_load_01..03.bclim`、`load_wait_kind.bclan`、
  `Layout/common/save_wait.arc` から loader image と独立同定済み。
- F-239/F-240: stopped snapshot の `id=10` / length 0 node と、実際に replay された id=10 Layoutは
  同一視できない。id または固定 heap pointerだけで image identity を決めない。
- 目標は、ロード画像の後にも自前 UI画像（スプライト）を描ける、常時利用可能な GPU 経路である。
  この lifecycle trace は、その安全な最終提出/保持の同定に向けた観測だった。

## 参照先

- 現在の状態: `RE/STATE.md`
- 原因・根拠: `RE/FINDINGS.md` F-241
- 次作業: `RE/TODO.md` F-241 節
- recovery の一般則: `DOCS/crash_recovery.md`
- 一時観測記録: `scratchpad/ACTIVE_2026-09-02_TITLE_F238.md`
- GPU チートメニュー全体: `HANDOFF_CHEATMENU.md`
