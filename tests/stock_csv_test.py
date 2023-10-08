import pytest
from pytest_mock import Mocker

from CSVDataHandler import CSVDataHandler


def test_csv_data_reader(mocker: Mocker):
    """Tests the `csv_data_reader()` function."""

    # Mock the `open()` function
    mock_file = mocker.Mock()
    mock_file.read.return_value = """
header1,header2
value1,value2
value3,value4
"""
    mocker.patch("open", return_value=mock_file)

    # Call the `csv_data_reader()` function
    data_values = CSVDataHandler.csv_data_reader("test.csv", "header2")

    # Assert that the function returned the correct data
    assert data_values == ["value2", "value4"]


def test_get_value():
    """Tests the `_getValue()` function."""

    # Initialize a dictionary of closing prices
    closing_price = {
        "Ticker A": [100.00, 101.00],
        "Ticker B": [99.00, 100.00]
    }

    # Call the `_getValue()` function
    last_values = CSVDataHandler._getValue(closing_price)

    # Assert that the function returned the correct data
    assert last_values == [101.00, 100.00]


def test_combine_data_csv():
    """Tests the `combine_data_csv()` function."""

    # Initialize a list of bought shares ticker values
    data_values = ["10", "20"]

    # Initialize a dictionary of closing prices
    close_list = {
        "Ticker A": [100.00, 101.00],
        "Ticker B": [99.00, 100.00]
    }

    # Call the `combine_data_csv()` function
    results = CSVDataHandler.combine_data_csv(data_values, close_list)

    # Assert that the function returned the correct data
    assert results == [1000.00, 2000.00]


def test_update_csv(mocker: Mocker):
    """Tests the `update_csv()` function."""

    # Mock the `open()` function
    mock_file = mocker.Mock()
    mock_file.read.return_value = """
header1,header2
value1,value2
"""
    mocker.patch("open", return_value=mock_file)

    # Mock the `to_csv()` method from Pandas
    mock_to_csv = mocker.Mock()
    mock_to_csv.return_value = None
    mocker.patch("pandas.DataFrame.to_csv", return_value=mock_to_csv)

    # Call the `update_csv()` function
    CSVDataHandler.update_csv("test.csv", [100.00, 200.00])

    # Assert that the `to_csv()` method was called with the correct arguments
    mock_to_csv.assert_called_with(mock_file, "test.csv", index=False)


def test_close_list_csv(mocker: Mocker):
    """Tests the `close_list_csv()` function."""

    # Mock the `open()` function
    mock_file = mocker.Mock()
    mock_file.write.return_value = None
    mocker.patch("open", return_value=mock_file)

    # Initialize a dictionary of ticker symbols and closing prices
    ticker_data = {
        "Ticker A": [100.00, 101.00],
        "Ticker B": [99.00, 100.00]
    }

    # Call the `close_list_csv()` function
    CSVDataHandler.close_list_csv(ticker_data)

    # Assert that the `write()` method was called with the correct arguments
    mock_file.write.assert_called_with("""Date,Ticker A,Ticker B
Date_1,100.0,99.0
Date_2,101.0,100.0
""")


# import pytest
# from PyStoAnalyzer.stock_csv import CSVDataHandler

# user_csv_file='TestCSV.csv'
# column_ticker_name="Tickers"
# column_amount_name = "Amount"
# print(user_csv_file)

# ticker_values = CSVDataHandler.csv_data_reader(user_csv_file,column_ticker_name)
# amount_values = CSVDataHandler.csv_data_reader(user_csv_file,column_amount_name)
# print(ticker_values)
# print(amount_values)

# closing_data={'SONY': [93.6, 93.49, 91.07, 90.03, 90.19, 90.44, 89.82, 83.85], 'AMZN': [133.68, 131.69, 128.21, 128.91, 139.57, 142.22, 139.94, 137.85]}

# result = CSVDataHandler.combine_data_csv(amount_values,closing_data)
# print(result)

# CSVDataHandler.update_csv(user_csv_file,result)
# CSVDataHandler.close_list_csv(closing_data)