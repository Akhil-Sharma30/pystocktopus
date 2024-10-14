import config
from core import StockExtractor
from stock_csv import CSVDataHandler
from stock_forecasting import ModelStockData
import pandas as pd
from news_analysis import News
import logging

# Set up logging configuration
logging.basicConfig(
    filename="Demo_file_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    try:
        data = StockExtractor.ticker_data_collection(
            ticker_values=ticker_values,
            timespan=timespan,
            multiplier=multiplier,
            user_date=user_date,
            days=days,
        )
        logging.info(f"Stock data collected for tickers: {ticker_values}")
    except Exception as e:
        logging.error(f"Error collecting stock data: {str(e)}")

    try:
        CSVDataHandler.close_list_csv(data)
        logging.info("CSV data list successfully closed and saved.")

        result = CSVDataHandler.combine_data_csv(
            data_values=ticker_values, close_list=data
        )
        logging.info(f"CSV data combined successfully: {result}")
    except Exception as e:
        logging.error(f"Error handling CSV data: {str(e)}")

    try:
        df = pd.read_csv("Your-CSV-FilePath")
        logging.info("CSV file loaded successfully.")

        # Store the second column name in a variable
        second_column_name = df.columns[1]
        logging.info(f"Second column name: {second_column_name}")
    except Exception as e:
        logging.error(f"Error reading CSV file: {str(e)}")

    try:
        prediction = ModelStockData.create_fit_train_rnn(
            csv_file="GUI_GENERATED_DATA.csv",
            epochs=400,
            stock_closing_price_column_name="Your-column-name-for-analysis-and-training",
        )
        logging.info(f"Model training and prediction complete: {prediction}")
    except Exception as e:
        logging.error(f"Error in model training or prediction: {str(e)}")

    try:
        result = News.new_data_extract(ticker_values=Article, predict_date=predict)
        logging.info(f"News data extracted for analysis: {result}")

        ans = News.news_predict_analysis(result)
        logging.info(f"News analysis result: {ans}")
    except Exception as e:
        logging.error(f"Error in news analysis: {str(e)}")

    try:
        News.create_csv_with_predictions(
            csv_filename="stock_data.csv", analysis_results=ans
        )
        logging.info("CSV file created with predictions.")
    except Exception as e:
        logging.error(f"Error creating CSV with predictions: {str(e)}")


if __name__ == "__main__":
    config.api_key = "your-polygon-api-key"
    config.news_api = "your-news-api-key"

    ticker_values = ["YOUR-STOCK(Ticker)-NAME"]
    Article = ["YOUR-STOCK-NAME-FOR-NEWS-ANALYSIS"]
    timespan = "day"
    multiplier = 2
    user_date = "2023-10-01"
    predict = "2024-10-01"
    days = 340

    # Calling the func
    main(ticker_values, Article, timespan, multiplier, user_date, predict, days)
