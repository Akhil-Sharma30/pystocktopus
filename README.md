# pystocktopus: Your Ultimate Stock Data Management and Analysis Toolkit

<!-- ![PyPI - Version](https://img.shields.io/pypi/v/pystocktopus)
![Codecov](https://img.shields.io/codecov/c/github/Akhil-Sharma30/pystocktopus)
![PyPI - License](https://img.shields.io/pypi/l/pystocktopus)
![GitHub](https://img.shields.io/github/license/Akhil-Sharma30/pystocktopus)
![GitHub Repo stars](https://img.shields.io/github/stars/Akhil-Sharma30/pystocktopus)
![GitHub Discussions](https://img.shields.io/github/discussions/Akhil-Sharma30/pystocktopus)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pystocktopus)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Akhil-Sharma30/pystocktopus/CI) -->

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status](https://readthedocs.org/projects/pystocktopus/badge/?version=latest)](https://pystocktopus.readthedocs.io/en/latest/?badge=latest)
![GitHub issues](https://img.shields.io/github/issues/Akhil-Sharma30/pystocktopus)

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]
![GitHub](https://img.shields.io/github/license/Akhil-Sharma30/pystocktopus?color=green)

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
[rtd-link]:                 pystocktopus.readthedocs.io/en/latest/

<!-- prettier-ignore-end -->

Managing and analyzing stock data can be a complex and time-consuming task for
investors and traders. Keeping track of historical stock data, updating it with
new information, and extracting valuable insights from the data are all crucial
aspects of making informed investment decisions.

Introducing **pystocktopus**, a powerful Python package for **Python 3.7+**
designed to simplify stock data management, analysis, prediction and also use
the news sentiments of stocks volatality.

**pystocktopus** is an easy-to-use and versatile library that empowers users to
maintain and analyze their stock data with ease. Whether you are an experienced
trader or a novice investor, pystocktopus provides a comprehensive set of tools
to streamline your stock-related tasks.

## Key Features

- CSV Data Maintenance:

pystocktopus provides a seamless solution for maintaining your stock data in CSV
format. Whether you need to update existing data or extract new data from a CSV
file, this package streamlines the process, ensuring that your stock data is
always up-to-date and readily accessible.

- Real-time Stock Analysis:

Stay ahead of the curve with real-time stock analysis. pystocktopus offers tools
to analyze your stock's performance and predict how news and events will impact
its growth. It leverages advanced algorithms to assess whether news sentiment
for a specific stock over a defined period is positive or negative, helping you
make informed investment decisions.

- Current Closing Price Extraction:

pystocktopus simplifies the process of extracting the current closing price for
a specific stock. With just a few lines of code, you can access up-to-the-minute
price information, enabling you to monitor your investments with precision.

## Here are some examples of how the package can be used:

## Upgrade your CSV dashboard with new data:

```.py
from pystocktopus.stock_csv import CSVDataHandler

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

# For example, want to predict some data using past Closing price

```.py
# Import the necessary modules
from __future__ import annotations

from pystocktopus.stock_forecasting import ModelStockData

# Specify the path to the CSV file containing the stock data
csv_file = "stock_data-2.csv"

# Create and fit an LSTM model to the stock data
ModelStockData.create_and_fit_lstm_model(
    csv_file, sequence_length=10, epochs=50, stacked=False
)
print(ModelStockData)
```

# For example, display the candlestick chart:

```.py
from pystocktopus.stock_forecasting import DataAnalysis

# Create an interactive bar chart of the stock price data with volume and 20-day moving average
DataAnalysis.interactive_bar(csv_file)

# Create an interactive candlestick chart of the stock price data
DataAnalysis.interactive_sticks(csv_file)

# Perform a basic analysis of the stock price data
DataAnalysis.stock_analysis(csv_file)
```

# Do something with the sentiment predictions

# For example, identify the most positive and negative news articles:

```.py
from pystocktopus.news_analysis import News

# Create a list of tickers to extract news articles for
ticker_values = ["GOOGL"]

# Specify the date range to extract news articles for
predict_date = "2023-08-05"

# Call the new_data_extract() method to extract news articles for the given tickers and date range
news_articles = News.new_data_extract(ticker_values, predict_date)

# Call the news_predict_analysis() method to predict the sentiment of the news articles for each ticker
analysis_results = News.news_predict_analysis(news_articles)

# Call the create_csv_with_predictions() method to create a CSV file with the predicted sentiment for each ticker
csv_filename = "news_predictions.csv"
News.create_csv_with_predictions(csv_filename, analysis_results)

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

# Get the current closing price for Amazon

```.py
# Import the StockExtractor class from the pystocktopus.core library.
from pystocktopus.core import StockExtractor

# Set the ticker values, timespan, multiplier, and user date.
ticker_values = ["AMZN", "SONY"]
timespan = "DAY"
multiplier = 1
user_date = "2023-09-20"

# Extract the closing prices for the specified tickers, timespan, multiplier, and user date.
Closing_price = StockExtractor.ticker_data_collection(ticker_values, timespan, multiplier, user_date)

# Print the closing prices to the console.
print(Closing_price)
```

# Do something with the current closing price

# For example, print it to the console:

```.py
print("Current closing price for Amazon:", Closing_price)
```

### Install pystocktopus

`pystocktopus` uses modern `Python` packaging and can be installed using `pip` -

```
python -m pip install pystocktopus
```

### Setting-up API Key

To use the software properly setup these _API keys_ to completely use the
features of the project -

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
