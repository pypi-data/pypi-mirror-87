import io
from os import path

import pytest

from niftypet.ninst import install_tools as tls


def test_query(capsys, monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("y"))
    assert tls.query_yesno("hello")
    out, _ = capsys.readouterr()
    assert "hello [Y/n]" in out
    assert "Please respond with" not in out

    monkeypatch.setattr("sys.stdin", io.StringIO("N"))
    assert not tls.query_yesno("hello")
    out, _ = capsys.readouterr()
    assert "Please respond with" not in out

    monkeypatch.setattr("sys.stdin", io.StringIO("what\ny"))
    assert tls.query_yesno("hello")
    out, _ = capsys.readouterr()
    assert "Please respond with" in out


def test_check_platform():
    tls.check_platform()


def test_check_depends():
    deps = tls.check_depends()
    assert not {"cmake", "cuda", "git"} - deps.keys()


def test_check_version():
    deps = tls.check_version({})
    assert not {"RESPATH", "REGPATH", "DCM2NIIX", "HMUDIR"} - deps.keys()


def test_install_tool(tmp_path, monkeypatch):
    dname = tmp_path / "install_tool"
    monkeypatch.setenv("PATHTOOLS", str(dname))
    assert not path.exists(dname)
    with pytest.raises(UnboundLocalError):
        tls.install_tool("", {})
    assert path.exists(dname)
