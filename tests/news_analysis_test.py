import pytest
from pytest_mock import Mocker

from PyStoAnalyzer.news_analysis import News
from PyStoAnalyzer.config import news_api


def test_new_data_extract(mocker: Mocker):
    """Tests the `new_data_extract()` function."""

    # Mock the `get_everything()` method from the News API client
    ticker_values = ["AAPL", "GOOGL"]
    predict_date = "2023-08-04"
    days_lag = 2

    mock_response = mocker.Mock()
    mock_response.get.return_value = {
        "status": "ok",
        "articles": [
            {
                "title": "Apple to release new iPhone in September"
            },
            {
                "title": "Google announces new AI project"
            }
        ]
    }
    mocker.patch("newsapi.NewsApiClient.get_everything", return_value=mock_response)

    # Call the `new_data_extract()` function
    results_dict = News.new_data_extract(ticker_values, predict_date, days_lag)

    # Assert that the function returned the correct data
    assert results_dict["AAPL"] == ["Apple to release new iPhone in September"]
    assert results_dict["GOOGL"] == ["Google announces new AI project"]


def test_news_predict_analysis(mocker: Mocker):
    """Tests the `news_predict_analysis()` function."""

    # Mock the `text-classification` pipeline from Transformers
    data = {
        "AAPL": "Apple to release new iPhone in September",
        "GOOGL": "Google announces new AI project"
    }

    mock_response = mocker.Mock()
    mock_response.return_value = [
        {"label": "positive"},
        {"label": "negative"}
    ]
    mocker.patch("transformers.pipeline.text_classification", return_value=mock_response)

    # Call the `news_predict_analysis()` function
    analysis_results = News.news_predict_analysis(data)

    # Assert that the function returned the correct data
    assert analysis_results["AAPL"]["labels"] == ["positive"]
    assert analysis_results["GOOGL"]["labels"] == ["negative"]


def test_create_csv_with_predictions(mocker: Mocker):
    """Tests the `create_csv_with_predictions()` function."""

    # Mock the `to_csv()` method from Pandas
    analysis_results = {
        "AAPL": {"labels": ["positive"]},
        "GOOGL": {"labels": ["negative"]}
    }
    csv_filename = "news_predictions.csv"
    column_name_for_prediction = "news_prediction_for_stock"

    mock_response = mocker.Mock()
    mock_response.return_value = None
    mocker.patch("pandas.DataFrame.to_csv", return_value=mock_response)

    # Call the `create_csv_with_predictions()` function
    News.create_csv_with_predictions(csv_filename, analysis_results, column_name_for_prediction)

    # Assert that the `to_csv()` method was called with the correct arguments
    mocker.assert_called_with(mock_response, csv_filename, index=False)

# import pytest
# import PyStoAnalyzer.news_analysis as news

# # Define your ticker values
# ticker_values = ['SONY', 'NIKE']
# predict_date = '2023-09-30'

# data = news.News.new_data_extract(ticker_values,predict_date)
# print(data)
# result_strings = {
#     "Ticker1": "Day1: i am excellent\nDay2: i am good\n",
#     "Ticker2": "Day1: Title3\nDay2: Title4\n",
# }
# news_data = news.News.news_predict_analysis(data)
# print(news_data)
# csv_filename = 'Test_result'
# news.News.create_csv_with_predictions(csv_filename,news_data)