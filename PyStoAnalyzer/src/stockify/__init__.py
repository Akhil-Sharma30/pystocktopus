"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

PyStoAnalyzer: help you maintain your stock dashboard and also predict future for a stock based upon past data
"""


from __future__ import annotations

from ._version import version as __version__

__all__ = ("__version__",)

import PyStoAnalyzer.config
from PyStoAnalyzer.stock_csv import CSVDataHandler
from PyStoAnalyzer.new_analysis import News
import PyStoAnalyzer.core
import PyStoAnalyzer.pattern_tool
