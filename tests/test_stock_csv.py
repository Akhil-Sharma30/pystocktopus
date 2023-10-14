from __future__ import annotations

import pandas as pd
from pystocktopus.stock_csv import CSVDataHandler

# Define the path to the user's CSV file and the column names for tickers and amounts
user_csv_file = "tests/TestCSV.csv"
column_ticker_name = "Tickers"
column_amount_name = "Amount"

# Print the user's CSV file path
print(user_csv_file)

# Read ticker values from the CSV file using the specified column name
ticker_values = CSVDataHandler.csv_data_reader(user_csv_file, column_ticker_name)

# Read amount values from the CSV file using the specified column name
amount_values = CSVDataHandler.csv_data_reader(user_csv_file, column_amount_name)


# Using the assert to test the values
def test_csv_data_reader():
    assert (
        CSVDataHandler.csv_data_reader(user_csv_file, column_ticker_name)
        == ticker_values
    )
    assert (
        CSVDataHandler.csv_data_reader(user_csv_file, column_amount_name)
        == amount_values
    )


# Sample closing data for SONY and AMZN stocks
closing_data = {
    "SONY": [93.6, 93.49, 91.07, 90.03, 90.19, 90.44, 89.82, 83.85],
    "AMZN": [133.68, 131.69, 128.21, 128.91, 139.57, 142.22, 139.94, 137.85],
}

# Combine the amount values with the closing data
result = CSVDataHandler.combine_data_csv(amount_values, closing_data)


def test_combine_data_csv():
    assert CSVDataHandler.combine_data_csv(amount_values, closing_data) == result


def test_update_csv():
    CSVDataHandler.update_csv(user_csv_file, result)
    dataframe = pd.read_csv(user_csv_file)
    assert "Price Calculated" in dataframe.columns


CSVDataHandler.close_list_csv(closing_data)
