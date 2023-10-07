import pytest
from PyStoAnalyzer.core import StockExtractor

@pytest.fixture
def stock_extractor_instance():
    return StockExtractor()

def test_ticker_data_collection(stock_extractor_instance):
    ticker_values = 'AMZN'
    timespan = 'DAY'
    stock_closing_price_list = stock_extractor_instance.ticker_data_collection(ticker_values, timespan, 1, '2023-08-09')
    assert isinstance(stock_closing_price_list, list)
    assert len(stock_closing_price_list) == 1  # Adjust this based on the expected number of results
    # Add more specific assertions as needed to validate the result

if __name__ == "__main__":
    pytest.main()