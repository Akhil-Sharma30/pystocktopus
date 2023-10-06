import pytest
from PyStoAnalyzer.core import StockExtractor

ticker_values='AMZN'
timespan= 'DAY'
stock_closing_price_list = StockExtractor.ticker_data_collection(ticker_values,'day',1,'2023-08-09')
print(stock_closing_price_list)
def test_ticker_data_collection():
