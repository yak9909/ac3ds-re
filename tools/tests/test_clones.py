"""同形検出の正規化、代表選択、symbols 更新を IDA なしで試す。"""
import csv
import io
from pathlib import Path

import pytest

import clones
import symlib as sl


def body(instructions, mode="ARM"):
    lines = ["[function comments]", "MOV R0, #999", "[disassembly]"]
    for i, instruction in enumerate(instructions):
        lines.append(f"0x{0x100000 + i * 4:08X} {mode} loc_ABC: {instruction}")
    lines += ["0x00100100 data pool: DCD 123", "  ; ignored", "[pseudocode]", "not code"]
    return "\n".join(lines) + "\n"


@pytest.mark.parametrize("left,right", [
    ("BL sub_1234", "BL NamedFunction"),
    ("BNE.W 0x1234", "BNE.W loc_5678"),
    ("CBZ R2, loc_12", "CBZ R2, 0x3456"),
    ("LDR R0, =0x12", "LDR R0, =(SomeName+0x34)"),
    ("LDR R1, [PC,#0x20]", "LDR R1, [PC,#-12]"),
    ("ADR R3, label", "ADR R3, 0x1234"),
    ("MOVW R1, #:lower16:label", "MOVW R1, #:lower16:other"),
    ("LDR R0, NamedData", "LDR R0, OtherData"),
    ("LDR R0, NamedData", "LDR R0, 0x123456"),
    ("MOV R0, #0x10", "mov r0, #16"),
])
def test_normalize_equivalent(left, right):
    assert clones.normalize_instruction(left) == clones.normalize_instruction(right)


@pytest.mark.parametrize("left,right", [
    ("MOV R0, #1", "MOV R0, #2"),
    ("ADD R0, R1, #4", "SUB R0, R1, #4"),
    ("BLX R0", "BLX R1"),
    ("LDR R0, [R1,#4]", "LDR R0, [R1,#8]"),
    ("MOV R0, R1,LSL#1", "MOV R0, R1,LSR#1"),
    ("SVC 0x32", "SVC 0x33"),
    ("MCR P15, 0, R0, C7, C10, 4", "MCR P15, 0, R0, C7, C10, 5"),
    ("PUSH {R0-R3,LR}", "PUSH {R0-R4,LR}"),
    ("IT EQ", "IT NE"),
    ("MOV R0, FP", "MOV R0, IP"),
])
def test_normalize_distinct(left, right):
    assert clones.normalize_instruction(left) != clones.normalize_instruction(right)


def make_export(path, entries):
    path.mkdir()
    buf = io.StringIO()
    buf.write("generated\nidb_input_sha256: sha\nsymbols_commit: commit\nmode: full\n")
    writer = csv.DictWriter(buf, ["name", "address", "file", "decompile", "symbols_commit"], delimiter="\t")
    writer.writeheader()
    for address, name, instructions, mode in entries:
        rel = f"functions/{address:08X}.txt"
        file = path / rel
        file.parent.mkdir(exist_ok=True)
        file.write_text(body(instructions, mode), encoding="utf-8")
        writer.writerow(dict(name=name, address=sl.fmt_addr(address), file=rel,
                             decompile="ok", symbols_commit="commit"))
    (path / "index.txt").write_text(buf.getvalue(), encoding="utf-8")


def row(address, name, clone=""):
    r = dict.fromkeys(sl.COLUMNS["functions"], "")
    r.update(address=sl.fmt_addr(address), name=name, clone_of=clone, size="24", source="analysis")
    return r


def test_end_to_end(tmp_path):
    export, symbols, out = tmp_path / "export", tmp_path / "symbols", tmp_path / "clones.txt"
    instructions = ["PUSH {R4,LR}", "LDR R0, =123", "BL sub_123", "MOV R4, #1", "POP {R4,PC}"]
    entries = [(0x100000, "sub_100000", instructions, "ARM"),
               (0x100020, "OldName", instructions, "ARM"),
               (0x100040, "Name2", instructions, "ARM"),
               (0x100060, "sub_100060", instructions, "ARM"),
               (0x100080, "sub_100080", instructions, "Thumb"),
               (0x1000A0, "ThumbName", instructions, "Thumb"),
               (0x1000C0, "short", instructions[:4], "ARM"),
               (0x1000E0, "short2", instructions[:4], "ARM")]
    make_export(export, entries)
    rows = [row(0x100020, "CurrentName", "0x00100040"), row(0x100040, "Name2"),
            row(0x100000, ""), row(0x1000A1, "ThumbName"), row(0x100100, "Outside", "0x00900000")]
    sl.write_table(symbols, "functions", rows)
    before = {p.name: p.read_bytes() for p in (symbols / "functions").glob("*.csv")}
    result = clones.run("test", export, out, symbols)
    assert (result["groups"], result["functions"], result["named_groups"]) == (2, 6, 2)
    assert before == {p.name: p.read_bytes() for p in (symbols / "functions").glob("*.csv")}
    text = out.read_text(encoding="utf-8")
    assert "representative=0x00100020" in text and "representative=0x001000A1" in text
    assert "CurrentName" in text and "OldName" not in text
    assert "instructions=5" in text and b"\r" not in out.read_bytes()
    result = clones.run("test", export, out, symbols, update=True)
    assert result["symbols_updated"] == 2
    updated = sl.read_table(symbols, "functions")
    assert len(updated) == len(rows)
    by_addr = {r["address"]: r for r in updated}
    assert by_addr["0x00100020"]["clone_of"] == ""
    assert by_addr["0x00100040"]["clone_of"] == "0x00100020"
    assert by_addr["0x00100000"]["clone_of"] == ""
    assert by_addr["0x00100100"]["clone_of"] == "0x00900000"
    assert clones.run("test", export, out, symbols, update=True)["symbols_updated"] == 0
    assert clones.run("test", export, out, symbols, minimum=4)["groups"] == 3


def test_no_names_and_mixed_modes(tmp_path):
    export = tmp_path / "export"
    make_export(export, [(0x100040, "sub_100040", ["BX LR"], "ARM"),
                         (0x100020, "sub_100020", ["BX LR"], "ARM")])
    functions = clones.read_functions(export, [], 1)
    assert clones.group_functions(functions)[0][0].address == 0x100020
    assert clones.instruction_sequence(body(["BX LR"], "ARM")) != clones.instruction_sequence(body(["BX LR"], "Thumb"))
    text = body(["MOV R0, #1", "BX LR"]).replace("loc_ABC:", "Namespace::Function:")
    assert clones.instruction_sequence(text) == clones.instruction_sequence(body(["MOV R0, #1", "BX LR"]))
    mixed = body(["MOV R0, #1", "BX LR"]).replace("0x00100004 ARM", "0x00100004 Thumb")
    assert clones.instruction_sequence(mixed) != clones.instruction_sequence(body(["MOV R0, #1", "BX LR"]))
    with pytest.raises(ValueError, match="disassembly"):
        clones.instruction_sequence("[pseudocode]\n")
    with pytest.raises(ValueError, match="行を読めない"):
        clones.instruction_sequence("[disassembly]\nunreadable\n")
    with pytest.raises(ValueError, match="1 以上"):
        clones.run("test", export, tmp_path / "out", tmp_path / "symbols", minimum=0)


def test_cli(tmp_path, capsys):
    export = tmp_path / "export"
    make_export(export, [(0x100000, "sub_100000", ["BX LR"], "ARM")])
    assert clones.main(["--build", "acnl_jpn_v15", "--export", str(export),
                        "--symbols", str(tmp_path / "symbols"), "--min-instructions", "1"]) == 0
    assert (export / "clones.txt").exists()
    assert '"groups": 0' in capsys.readouterr().out
