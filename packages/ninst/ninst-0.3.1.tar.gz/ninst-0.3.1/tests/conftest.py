import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def noninteractive():
    if os.getenv("DISPLAY", False):
        pytest.skip("Need to call pytest with DISPLAY=''")


@pytest.fixture(scope="session")
def nvml():
    import pynvml

    try:
        pynvml.nvmlInit()
    except pynvml.NVMLError as exc:
        pytest.skip(str(exc))
    return pynvml
