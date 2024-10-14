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

# Set up logging configuration
logging.basicConfig(
    filename="news_analysis.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)


class News:
    """Class for handling news data."""

    def _recursive_character_splitter(
        self, text: str, context_window: int
    ) -> List[str]:
        logging.info("Splitting text into smaller chunks with the context window.")
        if len(text) <= context_window:
            return [text]

        point = text.rfind("\n\n", 0, context_window)
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
        """Combines the news articles for each ticker into a single string."""
        logging.info("Combining news articles for each ticker.")
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
    def new_data_extract(ticker_values, predict_date, days: int = 10):
        """Extracts news articles for a given list of tickers and date range."""
        logging.info(
            f"Extracting news data for tickers: {ticker_values} from {predict_date} for {days} days."
        )
        load_dotenv()

        try:
            # Initialize the News API client
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
                    from_param=start_date,
                    to=end_date,
                    language="en",
                    sort_by="relevancy",
                )

                # Log the number of articles fetched
                logging.info(
                    f"Fetched {len(all_articles.get('articles', []))} articles for {ticker}."
                )

                # Store the result in the dictionary
                results_dict[ticker] = all_articles

            return News._combine_news_article(results_dict)

        except Exception as e:
            logging.error(f"Error occurred during news data extraction: {e}")
            raise e

    @staticmethod
    def news_predict_analysis(data: dict[str, str]) -> dict[str, str]:
        """Predicts the sentiment of the news articles for each ticker."""
        logging.info("Starting sentiment analysis on news data.")
        try:
            # Initialize the text classification pipeline
            pipe = pipeline(
                "text-classification",
                model="MonoHime/rubert-base-cased-sentiment-new",
            )

            # Initialize a dictionary to store the analysis results
            analysis_results: dict[str, str] = {}

            # Iterate through the result_strings dictionary
            for ticker, content in data.items():
                logging.info(f"Analyzing sentiment for ticker: {ticker}")
                data = content.split("\n")
                positive = 0
                negative = 0
                for d in data:
                    sentiment = pipe(d)[0]
                    if sentiment["label"] == "NEGATIVE":
                        negative += 1
                    else:
                        positive += 1

                # Store the analysis results in the dictionary
                analysis_results[ticker] = (
                    "NEGATIVE" if negative >= positive else "POSITIVE"
                )
                logging.info(
                    f"Sentiment for {ticker}: {'NEGATIVE' if negative >= positive else 'POSITIVE'}"
                )

            return analysis_results

        except Exception as e:
            logging.error(f"Error occurred during sentiment analysis: {e}")
            raise e

    @staticmethod
    def create_csv_with_predictions(
        csv_filename: str,
        analysis_results,
        column_name_for_prediction="news_prediction_for_stock",
    ):
        """Creates a CSV file with the predicted sentiment for each ticker."""
        logging.info(f"Creating CSV file: {csv_filename} with sentiment predictions.")
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

            # Log the CSV creation success
            logging.info(f"New CSV file created successfully at: {csv_filename}")

        except Exception as e:
            logging.error(f"Error occurred while creating the CSV file: {e}")
            raise e
