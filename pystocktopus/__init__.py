"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

pystocktopus: help you maintain your stock dashboard and also predict future for a stock based upon past data
"""


from __future__ import annotations

import pystocktopus.config
from pystocktopus.stock_csv import CSVDataHandler
from pystocktopus.news_analysis import News
from pystocktopus.core import StockExtractor
import pystocktopus.pattern_tool
