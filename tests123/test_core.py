import pytest
from stockify.core import StockExtractor

ticker_values='APPL'
timespan= 'DYX'
stock_closing_price_list = StockExtractor.ticker_data_collection(ticker_values,'day',1,'2023-08-09')

