from __future__ import annotations

import importlib.metadata

import stockify as m


def test_version():
    assert importlib.metadata.version("stockify") == m.__version__
