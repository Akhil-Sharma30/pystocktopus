"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

pystocktopus.
"""
from __future__ import annotations

import os

"""
API configuration for the stock and news APIs.

Environment variables:
    Stock_API_KEY: The API key for the stock API.
    news_API_KEY: The API key for the news API.
"""
# API Configeration
api_key = os.environ.get("STOCK_API_KEY")

# News API Configeration
news_api = os.environ.get("NEWS_API_KEY")
