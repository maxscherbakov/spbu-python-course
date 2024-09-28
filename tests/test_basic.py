import pytest
import project  # on import will print something from __init__ file

from typing import Any


def setup_module(module: Any) -> None:
    print("basic setup module")


def teardown_module(module: Any) -> None:
    print("basic teardown module")


def test_1() -> None:
    assert 1 + 1 == 2


def test_2() -> None:
    assert "1" + "1" == "11"
