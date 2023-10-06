import pytest
from PyStoAnalyzer.stock_csv import CSVDataHandler

user_csv_file='TestCSV.csv'
column_ticker_name="Tickers"
column_amount_name = "Amount"
print(user_csv_file)

ticker_values = CSVDataHandler.csv_data_reader(user_csv_file,column_ticker_name)
amount_values = CSVDataHandler.csv_data_reader(user_csv_file,column_amount_name)
print(ticker_values)
print(amount_values)

closing_data={'SONY': [93.6, 93.49, 91.07, 90.03, 90.19, 90.44, 89.82, 83.85], 'AMZN': [133.68, 131.69, 128.21, 128.91, 139.57, 142.22, 139.94, 137.85]}

result = CSVDataHandler.combine_data_csv(amount_values,closing_data)
print(result)

CSVDataHandler.update_csv(user_csv_file,result)
CSVDataHandler.close_list_csv(closing_data)