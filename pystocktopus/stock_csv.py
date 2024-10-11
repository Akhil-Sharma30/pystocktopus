# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations

import csv
import os

import pandas as pd


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
                    raise f"No {csv_stock_column_name} column found."

                # Read the data from the specified column
                for row in csv_reader:
                    if data_column_index < len(row):
                        data_values.append(row[data_column_index])

        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as e:
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
        # Initialize a list to store the last values
        last_values = []

        # Iterate through the dictionary and extract the last value from each key
        for _key, value_list in closing_price.items():
            if value_list:  # Check if the list is not empty
                last_value = value_list[-1]
                last_values.append(last_value)

        return last_values

    # Combine the data of the bought shares ticker and closing price values
    @staticmethod
    def combine_data_csv(
        data_values: list[float], close_list: dict[float, float]
    ) -> list[float]:
        # Fetch the values in the Dict and store it in the list
        data_extractor = CSVDataHandler._getValue(close_list)

        results: list[float] = []
        for bought, closing_price in zip(data_values, data_extractor):
            results.append(float(bought) * float(closing_price))
        return results

    # Update the csv with predicted and calculated values
    @staticmethod
    def update_csv(
        csv_path: str, results: list[float], new_column_name: str = "Price Calculated"
    ) -> None:
        """Combines the data of the bought shares ticker and closing price values.

        Args:
            data_values (List[float]): A list of the bought shares ticker values.
            close_list (Dict[float, float]): A dictionary of closing prices.

        Returns:
            List[float]: A list of the combined values.
        """
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_path)

            # Create a new column named "Calculated" and assign the values from 'results' to it
            df[new_column_name] = results

            # Write the updated DataFrame back to the CSV file
            df.to_csv(csv_path, index=False)

            print(
                f"Float values added to the {new_column_name} column in the CSV file."
            )

        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as e:
            raise e

    # Store the Closing_List Stock Result in the .CSV file
    @staticmethod
    def close_list_csv(
        ticker_data: dict[str, list[float]],
        closing_data_fieldname: list[str] | None = None,
        csv_file_name = "stock_data.csv"
    ) -> None:
        """Stores the closing list stock results in a CSV file.

        Args:
            ticker_data (Dict[str, List[float]]): A dictionary of ticker symbols and closing prices.
            closing_data_fieldname (List[str]): A list of the names of the columns to create in the CSV file.

        Raises:
            ValueError: If the ticker_data dictionary is empty.
        """

        if closing_data_fieldname is None:
            closing_data_fieldname = ["closing_stock_data"]
        if not ticker_data:
            return  # Return early if ticker_data is empty

        # Create a CSV file with ticker names as columns

        try:
            with open(csv_file_name, "w", newline="") as csvfile:
                # Update fieldnames to include "Date" and columns for each ticker with custom field names
                fieldnames = ["Date"] + [
                    f"{field}_{ticker}"
                    for ticker in ticker_data
                    for field in closing_data_fieldname
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()  # Write the header row

                # Assuming that all lists in ticker_data have the same length
                num_rows = len(next(iter(ticker_data.values())))
                for i in range(num_rows):
                    data_row = {"Date": f"Date_{i + 1}"}  # Add a date identifier
                    for ticker, close_list in ticker_data.items():
                        for field in closing_data_fieldname:
                            data_row[f"{field}_{ticker}"] = close_list[i]
                    writer.writerow(data_row)

                # Print success message with file name and path
                file_path = os.path.abspath(csv_file_name)
                print(
                    f"CSV file '{csv_file_name}' created successfully at '{file_path}'"
                )

        except Exception as e:
            raise e
