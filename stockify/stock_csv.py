"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

Stockify.
"""
import csv
from typing import List
#from stock_analysis_tool import StockAnalyizer
import pandas as pd
import os

class CSVDataHandler:

    #Store the data in the csv in List
    @staticmethod
    def csv_data_reader(csv_file, csv_stock_column_name: str) -> List[str]:
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


    #Combine the data of the bought shares ticker and closing price values
    @staticmethod
    def combine_data_csv(data_values: List[float],close_list: List[float]) -> List[float]:
        
        results: List[float]= []
        for bought, closing_price in zip(data_values,close_list):
            results.append(float(bought) * float(closing_price))
        return results

    # Update the csv with predicted and calculated values
    @staticmethod
    def update_csv(csv_path: str, results: List[float],new_column_name: str= 'Price Calculated') -> None:
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
    def close_list_csv(close_list: List[float], closing_data_fieldname: List[str] = ['closing_stock_data']) -> None:
        if not close_list:
            return  # Return early if close_list is empty
        
        # Create a CSV file using the value(s) of closing_data_fieldname as the file name
        csv_file_name = "_".join(closing_data_fieldname) + ".csv"

        try:
            with open(csv_file_name, 'w', newline='') as csvfile:
                fieldnames: List[str] = closing_data_fieldname  # Heading for the CSV file
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()  # Write the header row

                for close_data in close_list:
                    data_row = {field: close_data for field in closing_data_fieldname}
                    writer.writerow(data_row)
                
            # Print success message with file name and path
            file_path = os.path.abspath(csv_file_name)
            print(f"CSV file '{csv_file_name}' created successfully at '{file_path}'")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")


