"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

pystocktopus: help you maintain your stock dashboard and also predict future for a stock based upon past data
"""

from __future__ import annotations

from .config import api_key, news_api
from .core import StockExtractor
from .news_analysis import News
from .stock_csv import CSVDataHandler
from .stock_forecasting import ModelStockData
