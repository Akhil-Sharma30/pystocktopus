# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations

import datetime
import json
import os
import logging
from polygon import RESTClient
from dotenv import load_dotenv

import pystocktopus.config as config

# Configure logging
logging.basicConfig(
    filename="stock_extractor.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)


class StockExtractor:
    """Extracts stock data from Polygon.io."""

    def ticker_data_collection(
        ticker_values: list[str],
        timespan: str,
        multiplier: int,
        user_date: str,
        days: int,
    ) -> list[float]:
        """Extracts stock data closing price from Polygon.io.

        Args:
            ticker_values (List[str]): A list of stock ticker symbols.
            timespan (str): The time span of the data to collect. Valid values are "day",
                "week", "month", and "quarter".
            multiplier (int): The multiplier to apply to the time span. For example, a multiplier
                of 2 will collect data for twice the specified time span.
            user_date (str): The date up to which to collect data.
            days (int): The number of days to retrieve data for.

        Returns:
            List[float]: A list of closing prices for the specified stocks.
        """

        start_date = PastDays.CalculateDate(user_date, days)

        # Initialize the dictionary to store data
        ticker_data = {}

        try:
            logging.info("Starting data collection for tickers: %s", ticker_values)

            # API Declarations
            load_dotenv()
            api_key = os.getenv("POLYGON_API")
            if api_key is None:
                logging.error("Polygon API key not found in environment variables.")
                raise ValueError("API key not found")

            client: str = RESTClient(api_key=api_key)

            for ticker in ticker_values:
                logging.info("Collecting data for ticker: %s", ticker)

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
                    logging.info(
                        "Collected %d data points for ticker: %s",
                        len(close_list),
                        ticker,
                    )
                else:
                    logging.warning("No results found for ticker: %s", ticker)

            logging.info("Data collection completed successfully for all tickers.")
            return ticker_data

        except Exception as e:
            logging.error("Error during data collection: %s", str(e))
            raise


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

            # Calculate the start_date by subtracting the days_lag from the end_date
            start_date = end_date - datetime.timedelta(days=days_lag)

            logging.info(
                "Calculated start date: %s from end date: %s with a lag of %d days",
                start_date.strftime("%Y-%m-%d"),
                start_date_str,
                days_lag,
            )

            # Return the start_date as a string in the format "YYYY-MM-DD"
            return start_date.strftime("%Y-%m-%d")

        except Exception as e:
            logging.error("Error calculating date: %s", str(e))
            raise
