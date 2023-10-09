from __future__ import annotations

import importlib.metadata

import pystocktopus as m


def test_version():
    assert importlib.metadata.version("pystocktopus") == m.__version__
