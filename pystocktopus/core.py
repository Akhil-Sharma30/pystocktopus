# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations

import datetime
import json
import os
from polygon import RESTClient
from dotenv import load_dotenv

import pystocktopus.config as config


class StockExtractor:
    """Extracts stock data from Polygon.io."""

    def ticker_data_collection(
        ticker_values: list[str], timespan: str, multiplier: int, user_date: str, days = 500
    ) -> list[float]:
        """Extracts stock data closing price from Polygon.io.

        Args:
            ticker_values (List[str]): A list of stock ticker symbols.
            timespan (str): The time span of the data to collect. Valid values are "day",
                "week", "month", and "quarter".
            multiplier (int): The multiplier to apply to the time span. For example, a multiplier
                of 2 will collect data for twice the specified time span.
            user_date (str): The date up to which to collect data.
            days (int): The number of days to be data retrieved for.

        Returns:
            List[float]: A list of closing prices for the specified stocks.
        """

        start_date = PastDays.CalculateDate(user_date, days)

        # Initialize the dictionary to store data
        ticker_data = {}

        # try:
        #     if config.api_key is not None:
        # API Declarations
        load_dotenv()
        client: str = RESTClient(api_key=os.getenv("POLYGON_API"))
        # except:
        #     print(f"'{config.api_key}' not found. Could you specify in the pystocktopus.config?")
        #     return

        for ticker in ticker_values:
            aggs_csv: tuple[int, str, str, str] = client.get_aggs(
                ticker, int(multiplier), timespan, start_date, user_date, raw=True
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
    def CalculateDate(start_date_str: str, days_lag: int):
        """Calculates the start date for the data collection.

        Args:
            start_date_str (str): The end date for the data collection.
            days_lag (int): The number of days to subtract from the end date to get the start date.

        Returns:
            str: The start date for the data collection in the format "YYYY-MM-DD".
        """
        try:
            # Convert the start_date string to a datetime object
            end_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")

            # Calculate the end_date by subtracting 20 days from start_date
            start_date = end_date - datetime.timedelta(days=days_lag)

            # Convert the end_date to a string in the same format as the input
            return start_date.strftime("%Y-%m-%d")

        except Exception as e:
            raise e
