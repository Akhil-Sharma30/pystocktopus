# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations

from datetime import datetime, timedelta
import logging
import os
from typing import List
from dotenv import load_dotenv

import pandas as pd
from newsapi import NewsApiClient
from pystocktopus.config import news_api
from transformers import pipeline

logging.basicConfig(
    filename="stock_model.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)

class News:
    """Class for handling news data."""

    def _recursive_character_splitter(
        self, text: str, context_window: int
    ) -> List[str]:

        if len(text) <= context_window:
            return [text]

        point = text.rfind("\n\n", 0, end=context_window)
        if point == -1:
            point = text.rfind("\n", 0, context_window)
        if point == -1:
            point = text.rfind(" ", 0, context_window)
        if point == -1:
            point = context_window

        p1 = text[:point].strip()
        p2 = text[point:].strip()
        return [p1] + self._recursive_character_splitter(
            p2, context_window=context_window
        )

    @staticmethod
    def _combine_news_article(all_articles):
        """Combines the news articles for each ticker into a single string.

        Args:
            all_articles (Dict[str, Dict]): A dictionary of news articles for each ticker.

        Returns:
            Dict[str, str]: A dictionary of combined news articles for each ticker.
        """
        result_strings = {}

        # Iterate through the ticker values and their corresponding articles
        for ticker, articles in all_articles.items():
            result_string = ""
            for day, article in enumerate(articles["articles"], start=1):
                title = article.get("title", "No Title Found")
                result_string += f"Day{day}: {title}\n"

            result_strings[ticker] = result_string

        return result_strings

    @staticmethod
    def new_data_extract(ticker_values, predict_date, days:int = 10):
        """Extracts news articles for a given list of tickers and date range.

        Args:
            ticker_values (List[str]): A list of ticker values to extract news articles for.
            predict_date (str): The date to predict news articles for.

        Returns:
            Dict[str, str]: A dictionary of news articles for each ticker.
        """
        load_dotenv()
        # Initialize the News API client (you may need to install the newsapi-python package)
        newsapi = NewsApiClient(api_key=os.getenv("NEWS_API"))

        # Initialize a dictionary to store the results
        results_dict = {}

        # Define date range
        start_date = datetime.strptime(predict_date, "%Y-%m-%d")
        end_date = start_date - timedelta(days=days)

        # Iterate through the ticker values and fetch articles for each
        for ticker in ticker_values:
            all_articles = newsapi.get_everything(
                q=ticker,
                sources="bbc-news,the-verge",
                from_param=start_date,
                to=end_date,
                language="en",
                sort_by="relevancy",
            )

            # Store the result in the dictionary
            results_dict[ticker] = all_articles

        return News._combine_news_article(results_dict)

    @staticmethod
    def news_predict_analysis(Data: dict[str, str]) -> dict[str, str]:
        """Predicts the sentiment of the news articles for each ticker.

        Args:
            Data (Dict[str, str]): A dictionary of news articles for each ticker.

        Returns:
            Dict[str, str]: A dictionary of predicted sentiment for each ticker.
        """

        # Initialize the text classification pipeline
        pipe = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )

        # Initialize a dictionary to store the analysis results
        analysis_results: dict[str, str] = {}

        # Iterate through the result_strings dictionary
        for ticker, content in Data.items():
            # Analyze the content for each ticker value using the pipeline
            data = content.split("\n")
            postive = 0
            negative = 0
            for d in data:
                sentiment = pipe(d)[0]
                if sentiment["label"] == "NEGATIVE":
                    negative += 1
                else:
                    postive += 1

            # Store the analysis results in the dictionary
            analysis_results[ticker] = "NEGATIVE" if negative >= postive else "POSITIVE"

        return analysis_results

    @staticmethod
    def create_csv_with_predictions(
        csv_filename: str,
        analysis_results,
        column_name_for_prediction="news_prediction_for_stock",
    ):
        """Creates a CSV file with the predicted sentiment for each ticker.

        Args:
            csv_filename (str): The path to the CSV file to create.
            analysis_results (Dict[str, Dict]): A dictionary of predicted sentiment results for each ticker.
            column_name_for_prediction (str): The name of the column in the CSV file to store the predicted sentiment.

        Raises:
            Exception: If an error occurs while creating the CSV file.
        """
        try:
            # Create a new DataFrame with the "Ticker" and "column_name_for_prediction" columns
            data = []
            for ticker, result in analysis_results.items():
                prediction_label = (
                    result["labels"][0] if "labels" in result else ""
                )  # Assuming you want the first label as the prediction
                data.append(
                    {"Ticker": ticker, column_name_for_prediction: prediction_label}
                )

            # Convert the data to a DataFrame
            dataframe = pd.DataFrame(data)

            # Save the new DataFrame to the new CSV file
            dataframe.to_csv(csv_filename, index=False)

            # Print a message with the location of the saved CSV file
            logging.info(f"New CSV file created at: {csv_filename}")

        except Exception as e:
            raise e
