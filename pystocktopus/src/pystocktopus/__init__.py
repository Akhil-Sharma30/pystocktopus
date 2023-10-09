"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

pystocktopus: help you maintain your stock dashboard and also predict future for a stock based upon past data
"""


from __future__ import annotations

from ._version import version as __version__

__all__ = ("__version__",)

import pystocktopus.config
from pystocktopus.stock_csv import CSVDataHandler
from pystocktopus.news_analysis import News
import pystocktopus.core
import pystocktopus.pattern_tool
