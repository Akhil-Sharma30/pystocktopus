from __future__ import annotations

import importlib.metadata


def test_version():
    assert importlib.metadata.version("pystocktopus") == "0.1"
