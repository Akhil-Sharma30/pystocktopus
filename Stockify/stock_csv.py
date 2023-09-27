"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

Stockify.
"""
import csv
from typing import List
from stock_analysis_tool import StockAnalyizer

class CSVDataHandler:

    # Initialize the variable for the csv path finder
    csv_path: str = input("Enter the path for the csv file: ")

    csv_ticker_column_name: str = input("Enter the name of ticker column in the csv: ")
    csv_stock_bought_column_data: str =input("Enter the name of column in the csv having the stock bought amount: ")
    # Open the CSV file for reading
    csv_file: str = csv_path  # Replace with your CSV file's path

    def csv_ticker_store(csv_file: str,csv_ticker_column_name: str):
        # Reading the data inside the ticker column in the csv
        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.reader(file)
                
                # Read the header row to get column names
                header: List[str] = next(csv_reader)
                
                # Find the index of the 'tickers' column
                ticker_column_index = -1
                for i, col_name in enumerate(header):
                    if col_name.lower() == csv_ticker_column_name:
                        ticker_column_index = i
                
                if ticker_column_index != -1:
                    # Initialize a list to store the values in the 'tickers' column
                    ticker_values: List[str] = []

                    # Read the data from the 'tickers' column
                    for row in csv_reader:
                        if ticker_column_index < len(row):
                            ticker_values.append(row[ticker_column_index: int])
                    
                    # Print the selected column values
                    print("Values in the 'tickers' column:")
                    for value in ticker_values:
                        print(value)
                else:
                    print("No 'tickers' column found.")
                
                # You can use the ticker_values list in your further processing
                
        except FileNotFoundError:
            print(f"File '{csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def csv_share_bought_store(csv_file,csv_stock_bought_column_data: str) -> None:
        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.reader(file)
                
                # Read the header row to get column names
                header = next(csv_reader)
                
                # Find the index of the 'bought' column
                bought_column_index = -1
                for i, col_name in enumerate(header):
                    if col_name.lower() == csv_stock_bought_column_data:
                        bought_column_index = i
                
                if bought_column_index != -1:
                    # Initialize a list to store the values in the 'bought' column
                    bought_values = []

                    # Read the data from the 'bought' column
                    for row in csv_reader:
                        if bought_column_index < len(row):
                            bought_values.append(row[bought_column_index])
                    
                    # Print the selected column values
                    print("Values in the 'bought' column:")
                    for value in bought_values:
                        print(value)
                else:
                    print("No 'bought' column found.")
            
        except FileNotFoundError:
            print(f"File '{csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def combine_data_csv(self,bought_values: float) -> List[float]:
        results: List[float]= []
        for bought, closing_price in zip(bought_values, StockAnalyizer.close_list):
            results.append(float(bought) * float(closing_price))
        return results

    # Update the csv with predicted and calculated values
    def update_csv(self,csv_path: str,results : List[float]) -> None:
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_path)
            
            if 'price' not in df.columns:
                print("No 'price' column found in the CSV file.")
            else:
                # Add the values from 'results' under the "price" 
                df.loc[:1, 'price'] = results

                # Write the updated DataFrame back to the CSV file
                df.to_csv(CSVDataHandler.csv_file, index=False)
                
                print("Float values added to the 'price' column in the CSV file.")
            
        except FileNotFoundError:
            print(f"File '{CSVDataHandler.csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")