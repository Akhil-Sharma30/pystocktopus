"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

Stockify.
"""
from polygon import RESTClient
import stockify.config as config
from typing import cast,List,TypeVar,Tuple,Any
from urllib3 import HTTPResponse
import json
import csv
import pandas as pd
import datetime

class StockExtractor:

    def ticker_data_collection(
                            ticker_values:List[str],
                            timespan: str,
                            multiplier: int,
                            user_date: str) -> List[float]:

            start_date = PastDays._CalculateDate(user_date,10)

            # Initialize the dictionary to store data
            ticker_data = {}
            
            # try:
            #     if config.api_key is not None:
                    # API Declarations
            client: str = RESTClient(api_key=config.api_key)
            # except:
            #     print(f"'{config.api_key}' not found. Could you specify in the stockify.config?") 
            #     return
            
            for ticker in ticker_values:
                aggs_csv: Tuple[int, str, str, str] = client.get_aggs(
                    ticker,
                    int(multiplier),
                    timespan,
                    start_date,
                    user_date,
                    raw=True
                )

                data = json.loads(aggs_csv.data)

                if "results" in data:
                    raw_data_stock = data["results"]

                    close_list = []
                    for bar in raw_data_stock:
                        if "c" in bar:
                            close_list.append(bar["c"])

                    # Store the close_list in the dictionary with ticker as the key
                    ticker_data[ticker] = close_list

            return ticker_data
    
class PastDays:
     
     @staticmethod
     def _CalculateDate(start_date_str,days_lag):
        try:
            # Convert the start_date string to a datetime object
            end_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            
            # Calculate the end_date by subtracting 20 days from start_date
            start_date = end_date - datetime.timedelta(days=days_lag)
            
            # Convert the end_date to a string in the same format as the input
            start_date_str = start_date.strftime('%Y-%m-%d')
            
            return start_date_str
        except Exception as e:
            print(f"An error occurred: {str(e)}")