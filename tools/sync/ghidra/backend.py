"""Ghidra API 部分。JVM 起動後にのみ読み込む。"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
import tempfile
import time
from pathlib import Path

import pyghidra
from common import LANGUAGE, COMPILER, function_range, normalize_c, prototype_declaration, type_units, resolve_target, global_type_expression, enum_declaration, target_mode


def address(program, offset):
    return program.getAddressFactory().getDefaultAddressSpace().getAddress(offset)


def create(project, data, segments):
    from java.lang import Object
    from java.math import BigInteger
    from java.io import ByteArrayInputStream
    from ghidra.program.database import ProgramDB
    from ghidra.program.util import DefaultLanguageService
    from ghidra.program.model.lang import LanguageID, CompilerSpecID
    from ghidra.app.cmd.disassemble import DisassembleCommand
    from ghidra.app.cmd.function import CreateFunctionCmd
    lang = DefaultLanguageService.getLanguageService().getLanguage(LanguageID(LANGUAGE))
    consumer = Object()
    program = ProgramDB("independent", lang, lang.getCompilerSpecByID(CompilerSpecID(COMPILER)), consumer)
    try:
        with pyghidra.transaction(program, "raw code.bin segments"):
            memory = program.getMemory()
            for seg in segments:
                size = seg["end"] - seg["start"]
                at = address(program, seg["start"])
                if seg["offset"] is None:
                    block = memory.createUninitializedBlock(seg["name"], at, size, False)
                else:
                    offset = seg["offset"]
                    block = memory.createInitializedBlock(seg["name"], at, ByteArrayInputStream(data[offset:offset + size]), size, pyghidra.task_monitor(), False)
                block.setRead(seg["read"])
                block.setWrite(seg["write"])
                block.setExecute(seg["execute"])
            entry = address(program, segments[0]["start"])
            program.getSymbolTable().addExternalEntryPoint(entry)
            program.getProgramContext().setValue(program.getRegister("TMode"), entry, address(program, segments[0]["end"] - 1), BigInteger.ZERO)
            DisassembleCommand(entry, None, True).applyTo(program)
            CreateFunctionCmd(entry).applyTo(program)
        before = time.monotonic()
        log = pyghidra.analyze(program)
        elapsed = time.monotonic() - before
        starts = [int(f.getEntryPoint().getOffset()) for f in program.getFunctionManager().getFunctions(True)]
        project.getProjectData().getRootFolder().createFile("independent", program, pyghidra.task_monitor())
        return {"functions": len(starts), "starts": starts, "auto_seconds": elapsed, "analysis_log": str(log),
                "ghidra_version": str(__import__("ghidra.framework", fromlist=["Application"]).Application.getApplicationVersion())}
    finally:
        program.release(consumer)


class Counts:
    def __init__(self):
        self.results = {}

    def attempt(self, category, identity, operation):
        count = self.results.setdefault(category, {"success": 0, "failure": 0, "examples": []})
        try:
            operation()
            count["success"] += 1
        except Exception as exc:
            count["failure"] += 1
            if len(count["examples"]) < 8:
                count["examples"].append({"item": str(identity), "error": str(exc)[:1000]})


def import_symbols(project, tables, types_dir):
    from java.math import BigInteger
    from ghidra.program.model.symbol import SourceType
    from ghidra.program.model.address import AddressSet
    from ghidra.program.model.listing import CodeUnit
    from ghidra.app.cmd.disassemble import DisassembleCommand
    from ghidra.app.cmd.function import ApplyFunctionSignatureCmd
    from ghidra.app.util.cparser.C import CParser
    from ghidra.util.data import DataTypeParser
    from ghidra.program.model.data import DataTypeConflictHandler
    root = project.getProjectData().getRootFolder()
    if project.getProjectData().getFile("/symbols") is not None:
        raise FileExistsError("symbols は既存。取り込み済みのコピーは上書きしない")
    staging = root.createFolder("symbols_copy")
    copied = project.getProjectData().getFile("/independent").copyTo(staging, pyghidra.task_monitor())
    copied = copied.setName("symbols")
    copied.moveTo(root)
    staging.delete()
    counts = Counts()
    for key in ("functions", "function_names", "prototypes", "global_names", "global_types", "comments", "types", "type_preamble"):
        counts.results[key] = {"success": 0, "failure": 0, "examples": []}
    with pyghidra.program_context(project, "/symbols") as program:
        dtm = program.getDataTypeManager()
        parser = CParser(dtm, True, None)
        data_parser = DataTypeParser(dtm, dtm, None, DataTypeParser.AllowedDataTypes.ALL)
        def parse(declaration):
            declaration, enum_size = enum_declaration(declaration)
            datatype = parser.parse(declaration)
            if enum_size is not None:
                datatype = datatype.copy(dtm)
                datatype.setLength(enum_size)
                datatype = dtm.addDataType(datatype, DataTypeConflictHandler.REPLACE_HANDLER)
            return datatype

        def check(at):
            if not program.getMemory().contains(at):
                raise ValueError("メモリ範囲外")
        with pyghidra.transaction(program, "symbols import (independent untouched)"):
            for path in sorted(types_dir.glob("*.h")):
                for name, declaration in type_units(path.read_text(encoding="utf-8")):
                    counts.attempt("type_preamble" if name == "forward_declarations" else "types",
                                   path.name + ":" + name, lambda d=declaration: parse(d))
            for row in tables["functions"]:
                def function(row=row):
                    start, end, thumb = function_range(row)
                    at, last = address(program, start), address(program, end)
                    if not program.getMemory().getExecuteSet().contains(AddressSet(at, last)):
                        raise ValueError("関数の範囲が実行セグメントの外")
                    fm = program.getFunctionManager()
                    body = AddressSet(at, last)
                    # 境界の衝突は明示し、別関数を勝手に消さない。
                    for other in fm.getFunctionsOverlapping(body):
                        if other.getEntryPoint() != at:
                            raise ValueError("別の関数と境界が衝突: " + str(other.getEntryPoint()))
                    fn = fm.getFunctionAt(at)
                    register = program.getRegister("TMode")
                    # 同じ TMode 値でも、既存命令がある範囲への設定を Ghidra は拒否する。
                    # symbols コピーだけを再逆アセンブルする。
                    program.getListing().clearCodeUnits(at, last, False)
                    program.getProgramContext().setValue(register, at, last, BigInteger.valueOf(int(thumb)))
                    cmd = DisassembleCommand(at, body, True)
                    if not cmd.applyTo(program):
                        raise ValueError("逆アセンブル失敗: " + str(cmd.getStatusMsg()))
                    if fn is None:
                        fn = fm.createFunction(None, at, body, SourceType.USER_DEFINED)
                    else:
                        fn.setBody(body)
                    if fn is None or fn.getBody() != body:
                        raise ValueError("関数の境界の設定に失敗")
                counts.attempt("functions", row["address"], function)
                at = address(program, int(row["address"], 0) & ~1)
                if row["name"]:
                    def name(row=row, at=at):
                        fn = program.getFunctionManager().getFunctionAt(at)
                        if fn is None:
                            raise ValueError("関数がない")
                        fn.setName(row["name"], SourceType.USER_DEFINED)
                    counts.attempt("function_names", row["address"], name)
                if row["prototype"]:
                    def prototype(row=row, at=at):
                        fn = program.getFunctionManager().getFunctionAt(at)
                        if fn is None:
                            raise ValueError("関数がない")
                        decl = prototype_declaration(row["prototype"], str(fn.getName()))
                        signature = parse(decl)
                        signature.setCallingConvention(program.getCompilerSpec().getDefaultCallingConvention().getName())
                        cmd = ApplyFunctionSignatureCmd(at, signature, SourceType.USER_DEFINED)
                        if not cmd.applyTo(program):
                            raise ValueError(str(cmd.getStatusMsg()))
                        if "__noreturn" in row["prototype"]:
                            fn.setNoReturn(True)
                    counts.attempt("prototypes", row["address"], prototype)
            for row in tables["globals"]:
                at = address(program, int(row["address"], 0))
                if row["name"]:
                    def label(row=row, at=at):
                        check(at)
                        program.getSymbolTable().createLabel(at, row["name"], SourceType.USER_DEFINED).setPrimary()
                    counts.attempt("global_names", row["address"], label)
                if row["type"]:
                    def datatype(row=row, at=at):
                        check(at)
                        dt = data_parser.parse(global_type_expression(row["type"]))
                        length = int(dt.getLength())
                        if length <= 0 or (row["size"] and length > int(row["size"], 0)):
                            raise ValueError("型サイズが CSV の範囲を超える、または未確定")
                        program.getListing().clearCodeUnits(at, at.add(length - 1), False)
                        program.getListing().createData(at, dt)
                    counts.attempt("global_types", row["address"], datatype)
            kinds = {"func": CodeUnit.PLATE_COMMENT, "line": CodeUnit.EOL_COMMENT, "repeatable": CodeUnit.REPEATABLE_COMMENT}
            for row in tables["comments"]:
                def comment(row=row):
                    at = address(program, int(row["address"], 0))
                    check(at)
                    program.getListing().setComment(at, kinds[row["kind"]], row["text"])
                counts.attempt("comments", row["address"] + ":" + row["kind"], comment)
        program.save("symbols imported", pyghidra.task_monitor())
        return {"counts": counts.results, "functions_after": program.getFunctionManager().getFunctionCount(),
                "unsupported_tables": {key: len(tables[key]) for key in ("lvars", "vtables")},
                "types_in_manager": dtm.getDataTypeCount(True),
                "types_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(types_dir.glob("*.h"))}}


@contextmanager
def dump_program(project, view, create_requested, scratch):
    if not create_requested:
        with pyghidra.program_context(project, "/" + view) as program:
            yield program
        return
    if view != "independent":
        raise ValueError("--create は independent のコピーだけで使う")
    with tempfile.TemporaryDirectory(prefix="dump-", dir=scratch) as folder:
        copy_project = pyghidra.open_project(folder, "dump", create=True)
        try:
            source = project.getProjectData().getFile("/independent")
            source.copyTo(copy_project.getProjectData().getRootFolder(), pyghidra.task_monitor())
            with pyghidra.program_context(copy_project, "/independent") as program:
                yield program
        finally:
            copy_project.close()


def create_dump_function(program, requested, mode):
    from java.math import BigInteger
    from ghidra.app.cmd.disassemble import DisassembleCommand
    from ghidra.app.cmd.function import CreateFunctionCmd
    at = address(program, requested)
    memory = program.getMemory()
    if not memory.contains(at) or not memory.getBlock(at).isExecute():
        raise ValueError("指定番地が実行セグメントの外")
    fm = program.getFunctionManager()
    with pyghidra.transaction(program, "discover requested entry in temporary copy"):
        existing = fm.getFunctionContaining(at)
        if existing is not None:
            fm.removeFunction(existing.getEntryPoint())
        program.getListing().clearCodeUnits(at, at, False)
        program.getProgramContext().setValue(program.getRegister("TMode"), at, at,
                                            BigInteger.valueOf(int(mode == "thumb")))
        command = DisassembleCommand(at, None, True)
        if not command.applyTo(program):
            raise ValueError("逆アセンブル失敗: " + str(command.getStatusMsg()))
        command = CreateFunctionCmd(at)
        if not command.applyTo(program):
            raise ValueError("Ghidra による関数作成失敗: " + str(command.getStatusMsg()))
        function = fm.getFunctionAt(at)
        if function is None:
            raise ValueError("指定番地に関数を作成できない")
        return function


def dump(project, view, target, rows, out, manifest, *, create_requested=False, mode=None, scratch=None):
    from ghidra.app.decompiler import DecompInterface
    from ghidra.util.task import ConsoleTaskMonitor
    with dump_program(project, view, create_requested, scratch) as program:
        native = ((str(f.getName()), int(f.getEntryPoint().getOffset()))
                  for f in program.getFunctionManager().getFunctions(True))
        requested = resolve_target(target, rows, native)
        at = address(program, requested)
        selected_mode = target_mode(target, requested, rows, mode) if create_requested else None
        fn = (create_dump_function(program, requested, selected_mode) if create_requested
              else program.getFunctionManager().getFunctionContaining(at))
        lines = ["build: " + manifest["build"], "code_sha256: " + manifest["code_sha256"],
                 "view: " + view, "language: " + str(program.getLanguageID()),
                 "requested: " + target, f"requested_address: 0x{requested:08X}"]
        if fn is None:
            raise ValueError("このビューで関数を認識していない: " + str(at))
        if create_requested:
            lines = ["開始の番地は指定から与えた。境界と中身は Ghidra の解析",
                     "temporary_copy: independent", "mode: " + selected_mode] + lines
        lines += [f"entry: 0x{fn.getEntryPoint().getOffset():08X}", "name: " + str(fn.getName()),
                  "body: " + str(fn.getBody()), "prototype: " + str(fn.getSignature()), "", "[disassembly]"]
        for inst in program.getListing().getInstructions(fn.getBody(), True):
            raw = bytes((int(x) & 255 for x in inst.getBytes())).hex(" ")
            lines.append(f"0x{inst.getAddress().getOffset():08X}  {raw:<32} {inst}")
        decompiler = DecompInterface()
        try:
            if not decompiler.openProgram(program):
                raise RuntimeError(decompiler.getLastMessage())
            result = decompiler.decompileFunction(fn, 120, ConsoleTaskMonitor())
            lines += ["", "[decompilation]"]
            if result.decompileCompleted():
                lines.append(str(result.getDecompiledFunction().getC()))
            else:
                lines.append("ERROR: " + str(result.getErrorMessage()))
                out.write_text("\n".join(lines), encoding="utf-8")
                raise RuntimeError(result.getErrorMessage())
        finally:
            decompiler.dispose()
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def compare_boundaries(project, ida):
    different, absent = [], []
    with pyghidra.program_context(project, "/independent") as program:
        fm = program.getFunctionManager()
        starts = {int(f.getEntryPoint().getOffset()) for f in fm.getFunctions(True)}
        for at in sorted(ida - starts):
            function = fm.getFunctionContaining(address(program, at))
            if function is None:
                absent.append(f"0x{at:08X}")
            else:
                different.append({"ida": f"0x{at:08X}", "ghidra": f"0x{function.getEntryPoint().getOffset():08X}"})
    return {"ida_start_inside_other_function_count": len(different),
            "ida_start_without_function_count": len(absent),
            "inside_other_function_examples": different[:8],
            "without_function_examples": absent[:8]}
