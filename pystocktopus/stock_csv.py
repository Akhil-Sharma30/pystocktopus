# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations

import csv
import os
import logging  # Import logging module

import pandas as pd

# Configure logging
logging.basicConfig(
    filename="csv_data_handler.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)


class CSVDataHandler:
    """Class for handling CSV data."""

    @staticmethod
    def csv_data_reader(csv_file, csv_stock_column_name: str) -> list[str]:
        """Reads the data from the specified column in a CSV file.

        Args:
            csv_file (str): The path to the CSV file.
            csv_stock_column_name (str): The name of the column to read.

        Returns:
            List[str]: A list of the values in the specified column.
        """
        data_values: list[str] = []

        try:
            logging.info(
                f"Attempting to read column '{csv_stock_column_name}' from CSV file: {csv_file}"
            )
            with open(csv_file) as file:
                csv_reader = csv.reader(file)

                # Read the header row to get column names
                header = next(csv_reader)

                # Find the index of the column
                data_column_index = -1
                for i, col_name in enumerate(header):
                    if (
                        col_name.lower() == csv_stock_column_name.lower()
                    ):  # Case-insensitive comparison
                        data_column_index = i

                # Check if the column was found
                if data_column_index == -1:
                    raise ValueError(f"No {csv_stock_column_name} column found.")

                logging.info(
                    f"Column '{csv_stock_column_name}' found at index {data_column_index}."
                )

                # Read the data from the specified column
                for row in csv_reader:
                    if data_column_index < len(row):
                        data_values.append(row[data_column_index])

                logging.info(
                    f"Successfully read {len(data_values)} rows from column '{csv_stock_column_name}'."
                )

        except FileNotFoundError:
            logging.error(f"File not found: {csv_file}")
            raise FileNotFoundError(f"File not found: {csv_file}")
        except Exception as e:
            logging.error(f"Error reading CSV file: {str(e)}")
            raise e

        return data_values

    @staticmethod
    def _getValue(closing_price: dict[float, float]):
        """Extracts the last value from each key in a dictionary.

        Args:
            closing_price (Dict[float, float]): A dictionary of closing prices.

        Returns:
            List[float]: A list of the last values in the dictionary.
        """
        logging.info("Extracting last values from the closing price dictionary.")
        last_values = []

        for _key, value_list in closing_price.items():
            if value_list:
                last_value = value_list[-1]
                last_values.append(last_value)

        logging.info(
            f"Extracted {len(last_values)} values from closing price dictionary."
        )
        return last_values

    @staticmethod
    def combine_data_csv(
        data_values: list[float], close_list: dict[float, float]
    ) -> list[float]:
        logging.info("Combining data values with closing prices.")
        data_extractor = CSVDataHandler._getValue(close_list)

        results: list[float] = []
        for bought, closing_price in zip(data_values, data_extractor):
            results.append(float(bought) * float(closing_price))

        logging.info(f"Combined data into {len(results)} result values.")
        return results

    @staticmethod
    def update_csv(
        csv_path: str, results: list[float], new_column_name: str = "Price Calculated"
    ) -> None:
        """Updates the CSV file with a new column for the calculated values."""
        try:
            logging.info(
                f"Updating CSV file: {csv_path} with new column '{new_column_name}'."
            )

            df = pd.read_csv(csv_path)
            df[new_column_name] = results

            df.to_csv(csv_path, index=False)

            logging.info(
                f"Successfully added '{new_column_name}' column with {len(results)} values to the CSV file."
            )

        except FileNotFoundError:
            logging.error(f"CSV file not found: {csv_path}")
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        except Exception as e:
            logging.error(f"Error updating CSV file: {str(e)}")
            raise e

    @staticmethod
    def close_list_csv(
        ticker_data: dict[str, list[float]],
        closing_data_fieldname: list[str] | None = None,
        csv_file_name="stock_data.csv",
    ) -> None:
        """Stores the closing list stock results in a CSV file."""
        if closing_data_fieldname is None:
            closing_data_fieldname = ["closing_stock_data"]

        if not ticker_data:
            logging.warning("Ticker data is empty. No CSV file will be created.")
            return

        try:
            logging.info(f"Writing closing stock data to CSV file: {csv_file_name}")
            with open(csv_file_name, "w", newline="") as csvfile:
                fieldnames = ["Date"] + [
                    f"{field}_{ticker}"
                    for ticker in ticker_data
                    for field in closing_data_fieldname
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                num_rows = len(next(iter(ticker_data.values())))
                for i in range(num_rows):
                    data_row = {"Date": f"Date_{i + 1}"}
                    for ticker, close_list in ticker_data.items():
                        for field in closing_data_fieldname:
                            data_row[f"{field}_{ticker}"] = close_list[i]
                    writer.writerow(data_row)

            logging.info(
                f"CSV file '{csv_file_name}' created successfully with {num_rows} rows."
            )
            file_path = os.path.abspath(csv_file_name)
            logging.info(f"CSV file saved at: {file_path}")

        except Exception as e:
            logging.error(f"Error writing closing list data to CSV: {str(e)}")
            raise e
