import pytest
import PyStoAnalyzer.new_analysis as news

# Define your ticker values
ticker_values = ['SONY', 'NIKE']
predict_date = '2023-09-30'

data = news.News.new_data_extract(ticker_values,predict_date)
print(data)
result_strings = {
    "Ticker1": "Day1: i am excellent\nDay2: i am good\n",
    "Ticker2": "Day1: Title3\nDay2: Title4\n",
}
news_data = news.News.news_predict_analysis(data)
print(news_data)
csv_filename = 'Test_result'
news.News.create_csv_with_predictions(csv_filename,news_data)