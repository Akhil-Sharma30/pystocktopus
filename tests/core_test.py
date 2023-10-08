import pytest
from unittest import mock as Mocker
import json

from PyStoAnalyzer.core import StockExtractor, PastDays
import PyStoAnalyzer.config as config


def test_ticker_data_collection(mocker: Mocker):
    """Tests the `ticker_data_collection()` function."""

    # Mock the `get_aggs()` method from the Polygon API client
    ticker = "AAPL"
    timespan = "day"
    multiplier = 2
    user_date = "2023-08-04"

    mock_response = mocker.Mock()
    mock_response.data = json.dumps({
        "results": [
            {
                "c": 150.00
            },
            {
                "c": 151.00
            }
        ]
    })
    mocker.patch("polygon.RESTClient.get_aggs", return_value=mock_response)

    # Call the `ticker_data_collection()` function
    ticker_data = StockExtractor.ticker_data_collection([ticker], timespan, multiplier, user_date)

    # Assert that the function returned the correct data
    assert ticker_data[ticker] == [150.00, 151.00]


def test_calculate_date():
    """Tests the `CalculateDate()` function."""

    # Start date string
    start_date_str = "2023-08-04"

    # Days to subtract
    days_lag = 10

    # Expected start date
    expected_start_date = "2023-07-25"

    # Calculate the start date
    start_date = PastDays.CalculateDate(start_date_str, days_lag)

    # Assert that the calculated start date is correct
    assert start_date == expected_start_date

# import pytest
# from PyStoAnalyzer.core import StockExtractor

# @pytest.fixture
# def stock_extractor_instance():
#     return StockExtractor()

# def test_ticker_data_collection(stock_extractor_instance):
#     ticker_values = 'AMZN'
#     timespan = 'DAY'
#     stock_closing_price_list = stock_extractor_instance.ticker_data_collection(ticker_values, timespan, 1, '2023-08-09')
#     assert isinstance(stock_closing_price_list, list)
#     assert len(stock_closing_price_list) == 1  # Adjust this based on the expected number of results
#     # Add more specific assertions as needed to validate the result

# if __name__ == "__main__":
#     pytest.main()