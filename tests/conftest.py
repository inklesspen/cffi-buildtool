import pathlib

import pytest


@pytest.fixture(scope="session")
def examples():
    return pathlib.Path(__file__).parent.parent / "examples"
