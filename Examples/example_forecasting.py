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

# # Create an interactive bar chart of the stock price data with volume and 20-day moving average
# DataAnalysis.interactive_bar(csv_file)

# # Create an interactive candlestick chart of the stock price data
# DataAnalysis.interactive_sticks(csv_file)

# # Perform a basic analysis of the stock price data
# DataAnalysis.stock_analysis(csv_file)
