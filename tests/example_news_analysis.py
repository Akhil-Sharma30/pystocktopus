from __future__ import annotations

from pystocktopus.news_analysis import News

# Create a list of tickers to extract news articles for
ticker_values = ["GOOGL"]

# Specify the date range to extract news articles for
predict_date = "2023-08-05"

# Call the new_data_extract() method to extract news articles for the given tickers and date range
news_articles = News.new_data_extract(ticker_values, predict_date)


def test_new_data_extract():
    assert News.new_data_extract(ticker_values, predict_date) == news_articles


# Call the news_predict_analysis() method to predict the sentiment of the news articles for each ticker
analysis_results = News.news_predict_analysis(news_articles)

# Call the create_csv_with_predictions() method to create a CSV file with the predicted sentiment for each ticker
csv_filename = "news_predictions.csv"
News.create_csv_with_predictions(csv_filename, analysis_results)
