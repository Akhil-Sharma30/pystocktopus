# Stockify

Stockify is a Python project for collecting and analyzing stock market data using the Polygon API. It provides functionalities to fetch historical stock data, perform calculations, and update CSV files with the collected data.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetch historical stock market data for multiple tickers.
- Calculate start and end dates based on user input.
- Combine and analyze stock data.
- Update CSV files with calculated values.
- Store collected data in a CSV file.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/stockify.git


## Usage

### Configuration
Before using **Stockify**, you need to *configure your API key* in the stockify.config module.

### Collecting Stock Data
To collect stock data, you can use the *ticker_data_collection* function provided by Stockify. 
Here's an example:
```
from stockify.stock_extractor import StockExtractor

ticker_values = ["AAPL", "GOOGL"]
timespan = "day"
multiplier = 1
user_date = "2023-09-20"

ticker_data = StockExtractor.ticker_data_collection(ticker_values, timespan, multiplier, user_date)
```
> This function will fetch historical stock data for the specified tickers.