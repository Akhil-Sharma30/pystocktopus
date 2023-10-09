from pystocktopus.stock_csv import CSVDataHandler

# Define the path to the user's CSV file and the column names for tickers and amounts
user_csv_file = 'TestCSV.csv'
column_ticker_name = "Tickers"
column_amount_name = "Amount"

# Print the user's CSV file path
print(user_csv_file)

# Read ticker values from the CSV file using the specified column name
ticker_values = CSVDataHandler.csv_data_reader(user_csv_file, column_ticker_name)

# Read amount values from the CSV file using the specified column name
amount_values = CSVDataHandler.csv_data_reader(user_csv_file, column_amount_name)

# Print the extracted ticker and amount values
print(ticker_values)
print(amount_values)

# Sample closing data for SONY and AMZN stocks
closing_data = {'SONY': [93.6, 93.49, 91.07, 90.03, 90.19, 90.44, 89.82, 83.85], 
                'AMZN': [133.68, 131.69, 128.21, 128.91, 139.57, 142.22, 139.94, 137.85]}

# Combine the amount values with the closing data
result = CSVDataHandler.combine_data_csv(amount_values, closing_data)

# Update the user's CSV file with the combined data
CSVDataHandler.update_csv(user_csv_file, result)

# Close and clean up resources for the closing data
CSVDataHandler.close_list_csv(closing_data)