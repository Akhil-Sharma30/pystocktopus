from polygon import RESTClient
import config
import requests
from typing import cast,List
from urllib3 import HTTPResponse
import json
import csv

# API Declarations
API_Key = config.api_key
client = RESTClient(api_key=API_Key)

class stock:
    #Initializing the parameters for the stock preditions
    ticker: List[str]=input("Give your stock name {eg: Apple:APPL}: ")
    timespan: str = input("Give size of the time window {eg: day}: ")
    multiplier: int = input("Give size of the timespan multiplier {eg: 1}: ")
    start_date: str = input("Give the starting date {format '2023-0X-XX'} : ")
    end_date: str = input("Give the ending date {format '2023-0X-XX'} : ")

    data_Collection = cast(
        HTTPResponse,
        client.get_aggs(
            ticker,
            int(multiplier),
            timespan,
            start_date,
            end_date,
            raw=True
        ),
    )
    data_Processing = json.loads(data_Collection.data)
    print(data_Processing)

class csv_data_extractor:

    # Initialize the variable for the csv path finder
    csv_path = input("Enter the path for the csv file: ")

    # Open the CSV file for reading
    csv_file = csv_path  # Replace with your CSV file's path

    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            
            # Read the header row to get column names
            header = next(csv_reader)
            
            # Find the index of the 'tickers' column
            ticker_column_index = -1
            for i, col_name in enumerate(header):
                if col_name.lower() == 'tickers':
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
