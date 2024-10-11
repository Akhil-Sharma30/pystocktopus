import config
from core import StockExtractor
from stock_csv import CSVDataHandler
# from stock_forecasting import ModelStockData
import pandas as pd
from news_analysis import News

config.api_key = "your-polygon-api-key"
config.news_api = "your-news-api-key"

ticker_values = ["AAPL"]
timespan = "day"
multiplier = 2
user_date = "2023-10-01"
predict = "2024-10-01"

data = StockExtractor.ticker_data_collection(ticker_values,timespan,multiplier,user_date)
print(data)

CSVDataHandler.close_list_csv(data)
# # result = CSVDataHandler.combine_data_csv(data_values=ticker_values,close_list=data)
# # print(result)
# df = pd.read_csv("stock_data.csv")
# print()
# # Store the second column name in a variable
# second_column_name = df.columns[1]

# # Print the stored column name
# print(second_column_name)
# # prediction = ModelStockData.create_and_fit_lstm_model(
# #     csv_file="stock_data.csv",
# #     epochs=500,
# #     stock_closing_price_column_name="closing_stock_data_GOOGL",
# # )
# # print(prediction)

# result = News.new_data_extract(ticker_values=ticker_values, predict_date=predict)
# # print(result)
# ans = News.news_predict_analysis(result)
# print(ans)

# News.create_csv_with_predictions(csv_filename="stock_data.csv",analysis_results=ans)