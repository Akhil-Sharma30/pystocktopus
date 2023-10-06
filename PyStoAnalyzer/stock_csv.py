"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

PyStoAnalyzer.
"""
import csv
from typing import List,Dict
import pandas as pd
import os

class CSVDataHandler:

    #Store the data in the csv in List
    @staticmethod
    def csv_data_reader(
                    csv_file, 
                    csv_stock_column_name: str) -> List[str]:
        data_values: List[str] = []
        
        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.reader(file)
                
                # Read the header row to get column names
                header = next(csv_reader)
                
                # Find the index of the column
                data_column_index = -1
                for i, col_name in enumerate(header):
                    if col_name.lower() == csv_stock_column_name.lower():  # Case-insensitive comparison
                        data_column_index = i
                
                # Check if the column was found
                if data_column_index == -1:
                    print(f"No {csv_stock_column_name} column found.")
                else:
                    # Read the data from the specified column
                    for row in csv_reader:
                        if data_column_index < len(row):
                            data_values.append(row[data_column_index])
                    
                    # Print the selected column values
                    print(f"Values in the {csv_stock_column_name} column:")
                    for value in data_values:
                        print(value)
        
        except FileNotFoundError:
            print(f"File '{csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return data_values

    @staticmethod
    def _getValue(closing_price: Dict[float,float]):
        # Initialize a list to store the last values
        last_values = []

        # Iterate through the dictionary and extract the last value from each key
        for key, value_list in closing_price.items():
            if value_list:  # Check if the list is not empty
                last_value = value_list[-1]
                last_values.append(last_value)

        return last_values

    #Combine the data of the bought shares ticker and closing price values
    @staticmethod
    def combine_data_csv(data_values: List[float],close_list: Dict[float,float]) -> List[float]:
        
        #Fetch the values in the Dict and store it in the list
        data_extractor = CSVDataHandler._getValue(close_list)

        results: List[float]= []
        for bought, closing_price in zip(data_values,data_extractor):
            results.append(float(bought) * float(closing_price))
        return results

    # Update the csv with predicted and calculated values
    @staticmethod
    def update_csv(
                csv_path: str, 
                results: List[float],
                new_column_name: str= 'Price Calculated') -> None:
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_path)

            # Create a new column named "Calculated" and assign the values from 'results' to it
            df[new_column_name] = results

            # Write the updated DataFrame back to the CSV file
            df.to_csv(csv_path, index=False)

            print(f"Float values added to the {new_column_name} column in the CSV file.")

        except FileNotFoundError:
            print(f"File '{csv_path}' not found. Could you specify the file?")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    # Store the Closing_List Stock Result in the .CSV file
    @staticmethod
    def close_list_csv(
              ticker_data: Dict[str, List[float]],
              closing_data_fieldname: List[str] = ['closing_stock_data']) -> None:
        
        if not ticker_data:
            return  # Return early if ticker_data is empty

        # Create a CSV file with ticker names as columns
        csv_file_name = "stock_data.csv"

        try:
            with open(csv_file_name, 'w', newline='') as csvfile:
                fieldnames = ['Date'] + list(ticker_data.keys())  # Add a 'Date' column
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()  # Write the header row

                # Assuming that all lists in ticker_data have the same length
                num_rows = len(next(iter(ticker_data.values())))
                for i in range(num_rows):
                    data_row = {'Date': f'Date_{i + 1}'}  # Add a date identifier
                    for ticker, close_list in ticker_data.items():
                        data_row[ticker] = close_list[i]
                    writer.writerow(data_row)

            # Print success message with file name and path
            file_path = os.path.abspath(csv_file_name)
            print(f"CSV file '{csv_file_name}' created successfully at '{file_path}'")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
