from polygon import RESTClient
from config import api_key
import requests
from typing import cast,List
from urllib3 import HTTPResponse
import json
import csv
import pandas as pd

# API Declarations
client = RESTClient(api_key=api_key)

class csv_data_extractor:

    # Initialize the variable for the csv path finder
    csv_path = input("Enter the path for the csv file: ")

    csv_ticker_column_name = input("Enter the name of ticker column in the csv: ")
    csv_stock_bought_column_data =input("Enter the name of column in the csv having the stock bought amount: ")
    # Open the CSV file for reading
    csv_file = csv_path  # Replace with your CSV file's path

    def csv_ticker_store(csv_file,csv_ticker_column_name):
        # Reading the data inside the ticker column in the csv
        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.reader(file)
                
                # Read the header row to get column names
                header = next(csv_reader)
                
                # Find the index of the 'tickers' column
                ticker_column_index = -1
                for i, col_name in enumerate(header):
                    if col_name.lower() == csv_ticker_column_name:
                        ticker_column_index = i
                
                if ticker_column_index != -1:
                    # Initialize a list to store the values in the 'tickers' column
                    ticker_values = []

                    # Read the data from the 'tickers' column
                    for row in csv_reader:
                        if ticker_column_index < len(row):
                            ticker_values.append(row[ticker_column_index])
                    
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

    def csv_share_bought_store(csv_file: str,csv_stock_bought_column_data: str) -> None:
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

    def combine_data_csv(bought_values: float) -> List[float]:
        results = []
        for bought, closing_price in zip(bought_values, stock.close_list):
            results.append(float(bought) * float(closing_price))
        return results

    # Update the csv with predicted and calculated values
    def update_csv(csv_path: str,results : List[float]) -> None:
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_path)
            
            if 'price' not in df.columns:
                print("No 'price' column found in the CSV file.")
            else:
                # Add the values from 'results' under the "price" 
                df.loc[:1, 'price'] = results

                # Write the updated DataFrame back to the CSV file
                df.to_csv(csv_data_extractor.csv_file, index=False)
                
                print("Float values added to the 'price' column in the CSV file.")
            
        except FileNotFoundError:
            print(f"File '{csv_data_extractor.csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

class stock:
    #Initializing the parameters for the stock preditions
    ticker: List[str]=input("Give your stock name {eg: Apple:APPL}: ")
    timespan: str = input("Give size of the time window {eg: day}: ")
    multiplier: int = input("Give size of the timespan multiplier {eg: 1}: ")
    start_date: str = input("Give the starting date {format '2023-0X-XX'} : ")
    end_date: str = input("Give the ending date {format '2023-0X-XX'} : ")

    # Initialize the closing price variable 
    close_list=[]

    def ticker_data_collection(ticker: str,timespan: str,multiplier: int,start_date: str,end_date: str) -> None:
        #Checking if it is empty or not
        if close_list:
            close_list = []

        # Iterate through each tickers and store the value of the closing date
        for ticker in csv_data_extractor.ticker_values:
            aggs = client.get_aggs(
                ticker,
                int(multiplier),
                timespan,
                start_date,
                end_date,
                raw=True
            )
            
            data = json.loads(aggs.data)
            
            if "results" in data:
                raw_data_stock = data["results"]
                
                for bar in raw_data_stock:
                    if "c" in bar:
                        close_list.append(bar["c"])

        # Debugging intialized 
        #print(close_list)

    def close_list_csv(close_list: list)-> None:
        if not close_list:
            return  # Return early if close_list is empty

        with open(csv_data_extractor.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['closing_stock_data']  # Heading for the CSV file
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Write the header row

            for close_data in close_list:
                writer.writerow({'closing_data': close_data})

        
