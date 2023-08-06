from os import path

import pytest

tools = pytest.importorskip("niftypet.ninst.tools")


def test_resources():
    assert path.exists(tools.path_resources)
    assert tools.resources.DIRTOOLS


def test_gpu():
    assert tools.dev_info == tools.gpuinfo
