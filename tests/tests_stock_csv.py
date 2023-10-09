import pytest
from pystocktopus.stock_csv import CSVDataHandler

# Set the path to the CSV file
csv_file = "stock_data.csv"

# Set the name of the column to read
csv_stock_column_name = "closing_stock_data_AAPL"

# Read the data from the specified column in the CSV file
data_values = CSVDataHandler.csv_data_reader(csv_file, csv_stock_column_name)

# Set the path to the CSV file containing the closing prices
close_file = "closing_prices.csv"

# Read the closing prices from the CSV file
close_list = CSVDataHandler.csv_data_reader(close_file, csv_stock_column_name)

# Combine the data of the bought shares ticker and closing price values
combined_values = CSVDataHandler.combine_data_csv(data_values, close_list)

# Update the CSV file with predicted and calculated values
CSVDataHandler.update_csv(csv_file, combined_values, new_column_name="Price Calculated")

# Store the Closing_List Stock Result in the .CSV file
closing_data_fieldname = ["closing_stock_data"]
ticker_data = {"AAPL": data_values, "MSFT": combined_values}
CSVDataHandler.close_list_csv(ticker_data, closing_data_fieldname)
