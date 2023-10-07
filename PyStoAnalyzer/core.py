"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

PyStoAnalyzer.
"""
from polygon import RESTClient
import PyStoAnalyzer.config as config
from typing import cast,List,TypeVar,Tuple,Any
from urllib3 import HTTPResponse
import json
import csv
import pandas as pd
import datetime

class StockExtractor:
    """Extracts stock data from Polygon.io.
    """
    def ticker_data_collection(
                            ticker_values:List[str],
                            timespan: str,
                            multiplier: int,
                            user_date: str) -> List[float]:
            """Extracts stock data closing price from Polygon.io.

            Args:
                ticker_values (List[str]): A list of stock ticker symbols.
                timespan (str): The time span of the data to collect. Valid values are "day",
                    "week", "month", and "quarter".
                multiplier (int): The multiplier to apply to the time span. For example, a multiplier
                    of 2 will collect data for twice the specified time span.
                user_date (str): The date up to which to collect data.

            Returns:
                List[float]: A list of closing prices for the specified stocks.
            """

            start_date = PastDays._CalculateDate(user_date,10)

            # Initialize the dictionary to store data
            ticker_data = {}
            
            # try:
            #     if config.api_key is not None:
                    # API Declarations
            client: str = RESTClient(api_key=config.api_key)
            # except:
            #     print(f"'{config.api_key}' not found. Could you specify in the PyStoAnalyzer.config?") 
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
        """Calculates the start date for the data collection.

    Args:
        start_date_str (str): The end date for the data collection.
        days_lag (int): The number of days to subtract from the end date to get the start date.

    Returns:
        str: The start date for the data collection in the format "YYYY-MM-DD".
    """
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