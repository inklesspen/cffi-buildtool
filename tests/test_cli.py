import pathlib

import pytest

import cffi_buildtool.cli


def dont_exit(_status: int):
    pass


def test_read_sources(examples: pathlib.Path, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cffi_buildtool.cli.parser, "exit", dont_exit)
    srcdir = examples / "read-sources" / "cffi" / "netstring"
    cdef = srcdir / "_netstring.cdef.txt"
    csrc = srcdir / "_netstring.csrc.c"
    output = tmp_path / "out.c"
    cffi_buildtool.cli.run(["read-sources", "_netstring", str(cdef), str(csrc), str(output)])
    generated = output.read_text()
    assert "netstring_read" in generated


def test_exec_python(examples: pathlib.Path, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cffi_buildtool.cli.parser, "exit", dont_exit)
    pyfile = examples / "exec-python" / "cffi" / "netstring" / "_netstring.c.py"
    output = tmp_path / "out.c"
    cffi_buildtool.cli.run(["exec-python", str(pyfile), str(output)])
    generated = output.read_text()
    assert "netstring_read" in generated


def test_read_sources_same_input_fails(capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        cffi_buildtool.cli.run(["read-sources", "_netstring", "-", "-", "-"])
    _stdout, stderr = capsys.readouterr()
    assert "are the same file and should not be" in stderr
