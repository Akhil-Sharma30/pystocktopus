"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

pystocktopus.
"""

from __future__ import annotations

import os
import logging

# Configure logging
logging.basicConfig(
    filename="pystocktopus_config.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)

"""
API configuration for the stock and news APIs.

Environment variables:
    STOCK_API_KEY: The API key for the stock API.
    NEWS_API_KEY: The API key for the news API.
"""

# API Configuration
api_key = os.environ.get("STOCK_API_KEY")
if api_key:
    logging.info("Successfully loaded STOCK_API_KEY.")
else:
    logging.error("STOCK_API_KEY not found in environment variables.")

# News API Configuration
news_api = os.environ.get("NEWS_API_KEY")
if news_api:
    logging.info("Successfully loaded NEWS_API_KEY.")
else:
    logging.error("NEWS_API_KEY not found in environment variables.")
