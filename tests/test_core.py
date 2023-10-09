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
