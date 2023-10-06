from __future__ import annotations

import importlib.metadata

import PyStoAnalyzer as m


def test_version():
    assert importlib.metadata.version("PyStoAnalyzer") == m.__version__
