# pystocktopus: Your Ultimate Stock Data Management and Analysis Toolkit

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]



<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/Akhil-Sharma30/pystocktopus/workflows/CI/badge.svg
[actions-link]:             https://github.com/Akhil-Sharma30/pystocktopus/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/pystocktopus
[conda-link]:               https://github.com/conda-forge/pystocktopus-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/Akhil-Sharma30/pystocktopus/discussions
[pypi-link]:                https://pypi.org/project/pystocktopus/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/pystocktopus
[pypi-version]:             https://img.shields.io/pypi/v/pystocktopus
[rtd-badge]:                https://readthedocs.org/projects/pystocktopus/badge/?version=latest
[rtd-link]:                 https://pystocktopus.readthedocs.io/en/latest/?badge=latest

<!-- prettier-ignore-end -->
Managing and analyzing stock data can be a complex and time-consuming task for investors and traders. Keeping track of historical stock data, updating it with new information, and extracting valuable insights from the data are all crucial aspects of making informed investment decisions. 

Introducing **pystocktopus**, a powerful Python package for **Python 3.7+** designed to simplify stock data management, analysis, prediction and also use the news sentiments of stocks volatality.

**pystocktopus** is an easy-to-use and versatile library that empowers users to maintain and analyze their stock data with ease. Whether you are an experienced trader or a novice investor, pystocktopus provides a comprehensive set of tools to streamline your stock-related tasks.

## Key Features

* CSV Data Maintenance:

pystocktopus provides a seamless solution for maintaining your stock data in CSV format. Whether you need to update existing data or extract new data from a CSV file, this package streamlines the process, ensuring that your stock data is always up-to-date and readily accessible.

* Real-time Stock Analysis:

Stay ahead of the curve with real-time stock analysis. pystocktopus offers tools to analyze your stock's performance and predict how news and events will impact its growth. It leverages advanced algorithms to assess whether news sentiment for a specific stock over a defined period is positive or negative, helping you make informed investment decisions.

* Current Closing Price Extraction:

pystocktopus simplifies the process of extracting the current closing price for a specific stock. With just a few lines of code, you can access up-to-the-minute price information, enabling you to monitor your investments with precision.

## Here are some examples of how the package can be used:

## Upgrade your CSV dashboard with new data:
```.py
from pystocktopus.core import StockExtractor

# Define the path to the user's CSV file and the column names for tickers and amounts
user_csv_file = 'TestCSV.csv'
column_ticker_name = "Tickers"
column_amount_name = "Amount"

# Print the user's CSV file path
print(user_csv_file)

# Read ticker values from the CSV file using the specified column name
ticker_values = CSVDataHandler.csv_data_reader(user_csv_file, column_ticker_name)

# Read amount values from the CSV file using the specified column name
amount_values = CSVDataHandler.csv_data_reader(user_csv_file, column_amount_name)

# Print the extracted ticker and amount values
print(ticker_values)
print(amount_values)

# Sample closing data for SONY and AMZN stocks
closing_data = {'SONY': [93.6, 93.49, 91.07, 90.03, 90.19, 90.44, 89.82, 83.85], 
                'AMZN': [133.68, 131.69, 128.21, 128.91, 139.57, 142.22, 139.94, 137.85]}

# Combine the amount values with the closing data
result = CSVDataHandler.combine_data_csv(amount_values, closing_data)

# Update the user's CSV file with the combined data
CSVDataHandler.update_csv(user_csv_file, result)

# Close and clean up resources for the closing data
CSVDataHandler.close_list_csv(closing_data)

```

# Do something with the extracted data
# For example, plot the closing prices over time:

```.py
# Load the CSV dashboard
dashboard = pystocktopus.load_dashboard("my_dashboard.csv")

# Calculate a technical indicator, such as the moving average
moving_average = dashboard.calculate_moving_average(period=20)

# Perform statistical analysis on the data, such as calculating the correlation between two stocks
correlation = dashboard.calculate_correlation("AAPL", "GOOG")

# Generate a chart of the data, such as a candlestick chart
candlestick_chart = dashboard.plot_candlestick_chart()
```

# Do something with the analysis results
# For example, display the candlestick chart:
```.py
candlestick_chart.show()
Use code with caution. Learn more

Predict stock news sentiment:
Python
import stock_csv_dashboard

# Load the CSV dashboard
dashboard = stock_csv_dashboard.load_dashboard("my_dashboard.csv")

# Load the stock news data
news_data = stock_csv_dashboard.load_news_data("AAPL")

# Predict the sentiment of the stock news articles
sentiments = dashboard.predict_news_sentiment(news_data)
```

# Do something with the sentiment predictions
# For example, identify the most positive and negative news articles:
```.py
most_positive_news = news_data[sentiments == "Positive"].sort_values("score", ascending=False).head(1)
most_negative_news = news_data[sentiments == "Negative"].sort_values("score", ascending=True).head(1)
```

# Display the most positive and negative news articles:
```.py
import pystocktopus.news_analysis as news

result_strings = {
    "Ticker1": "Day1: i am excellent\nDay2: i am good\n",
    "Ticker2": "Day1: Title3\nDay2: Title4\n",
}
news_data = news.News.news_predict_analysis(result_strings)
print(news_data)
csv_filename = 'Test_result'
news.News.create_csv_with_predictions(csv_filename,news_data)
```

# Get the current closing price for Apple
```.py
from pystocktopus.core import StockExtractor

ticker_values='AMZN'
timespan= 'DAY'
stock_closing_price_list = StockExtractor.ticker_data_collection(ticker_values,'day',1,'2023-08-09')
print(stock_closing_price_list)
```

# Do something with the current closing price
# For example, print it to the console:
```.py
print("Current closing price for Apple:", stock_closing_price_list)
```

### Install pystocktopus

`pystocktopus` uses modern `Python` packaging and can be installed using `pip` -
```
python -m pip install pystocktopus
```
### Setting-up API Key
To use the software properly setup these *API keys* to completely use the features of the 
project -

1. `Newsapi` access from [this](https://newsapi.org/).
2. `Polygon.io` API access from [this](https://polygon.io/).

#### Use this to Setup API Globally
```
#Polyon API KEY
export api_key="YOUR-API-KEY"

#NewsApi KEY
export news_api="YOUR-API-KEY"

```

## Contributing

If you want to contribute to `pystocktopus` (thanks!), please have a look at our
[Contributing Guide](https://github.com/Akhil-Sharma30/pystocktopus/blob/main/CONTRIBUTING.md).