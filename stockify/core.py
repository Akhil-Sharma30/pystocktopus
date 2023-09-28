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
import stockify.config as config
import datetime

class StockExtractor:

    def _CalculateStartDate(start_date_str):
        try:
            # Convert the start_date string to a datetime object
            end_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            
            # Calculate the end_date by subtracting 20 days from start_date
            start_date = end_date - datetime.timedelta(days=10)
            
            # Convert the end_date to a string in the same format as the input
            start_date_str = start_date.strftime('%Y-%m-%d')
            
            return start_date_str
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def ticker_data_collection(
                            ticker_values:List[str],
                            timespan: str,
                            multiplier: int,
                            user_date: str) -> List[float]:

            start_date = StockExtractor._CalculateStartDate(user_date)

            # Initialize the closing price variable 
            close_list: List[float]=[]
            # Checking if it is empty or not
            if close_list:
                close_list = []
            
            try:
                if config.api_key:
                    # API Declarations
                    client: str = RESTClient(api_key=config.api_key)
            except:
                print(f"'{config.api_key}' not found. Could you specify in the stockify.config?") 
                return
            
            for ticker in ticker_values:
                aggs_csv: Tuple[int,str,str,str] = client.get_aggs(
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
                    
                    for bar in raw_data_stock:
                        if "c" in bar:
                            close_list.append(bar["c"])
        
            return close_list

