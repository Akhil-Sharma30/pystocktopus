import pytest
from pystocktopus.core import StockExtractor

ticker_values = ['AMZN','SONY']
timespan = 'DAY'
multiplier = 1
user_date = '2023-09-20'

def test_ticker_data_collection():
    assert StockExtractor.ticker_data_collection(ticker_values,timespan,multiplier,user_date) == True