import pytest
from stockify.stock_csv import CSVDataHandler

user_csv_file='TestCSV.csv'
column_ticker_name="Tickers"
column_amount_name = "Amount"
print(user_csv_file)

ticker_values = CSVDataHandler.csv_data_reader(user_csv_file,column_ticker_name)
amount_values = CSVDataHandler.csv_data_reader(user_csv_file,column_amount_name)
print(ticker_values)
print(amount_values)

closing_data = ['1','2','3','4']

result = CSVDataHandler.combine_data_csv(amount_values,closing_data)
print(result)

CSVDataHandler.update_csv(user_csv_file,result)
# CSVDataHandler.close_list_csv(closing_data)