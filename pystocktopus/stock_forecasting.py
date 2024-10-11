# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations
import logging  # Import the logging module

import mplfinance as fplt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import tensorflow as tf
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adamax

# Configure logging
logging.basicConfig(
    filename="stock_model.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)


class ModelStockData:
    def _csvDataCollection(
        csv_file: str, sequence_length, stock_closing_price_column_name: str
    ):
        """Collects and prepares data from a CSV file for training a sequential model."""
        logging.info("Starting CSV data collection from %s.", csv_file)

        try:
            dataframe = pd.read_csv(csv_file)
            data = dataframe[stock_closing_price_column_name].values.reshape(-1, 1)

            # Scale the data to be between 0 and 1
            scaler = MinMaxScaler()
            data = scaler.fit_transform(data)
            print(data.shape)
            # Split the data into training and testing sets
            # train_size = int(len(data) * 0.8)
            # train_data = data[:train_size]
            # print(f'train data ={train_data}')
            # test_data = data[train_size:]
            # print(f'test data ={test_data}')
            # logging.info("Data split into training and test sets successfully.")

            # Create sequences of data for training
            def create_sequences(data, seq_length):
                sequences = []
                for i in range(len(data) - seq_length):
                    x = data[i : i + seq_length]
                    y = data[i + seq_length]
                    print("################")
                    print(len(x), len(y))
                    sequences.append((x, y))

                print(len(sequences))
                return np.array(sequences)

            # seq_length = sequence_length
            # train_sequences = create_sequences(train_data, seq_length)
            # test_sequences = create_sequences(test_data, seq_length)

            # Separate input sequences (X) and target values (y)
            # X_train = np.stack(data[:, 0])  # Stack input sequences
            # y_train = np.stack(data[:, 1])  # Stack target sequences

            # X_test = np.stack(data[:, 0])  # Stack input sequences
            # y_test = np.stack(data[:, 1])  # Stack target sequences

            # Convert NumPy arrays to TensorFlow tensors
            X_tensorflow_train = tf.convert_to_tensor(data, dtype=tf.float32)
            y_tensorflow_train = tf.convert_to_tensor(data, dtype=tf.float32)

            logging.info("Data collection completed successfully.")

            return (
                X_tensorflow_train,
                y_tensorflow_train,
                scaler,
            )

        except Exception as e:
            logging.error("Error during CSV data collection: %s", str(e))
            raise

    def _mean_absolute_percentage_error(y_true, y_pred):
        """Calculates the mean absolute percentage error (MAPE) between two arrays."""
        try:
            mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
            logging.info("MAPE calculated successfully.")
            return mape
        except Exception as e:
            logging.error("Error in calculating MAPE: %s", str(e))
            raise

    @staticmethod
    def create_and_fit_lstm_model(
        csv_file: str,
        sequence_length: int = 10,
        layers: int = 10,
        lstm_units: list | None = None,
        epochs=650,
        lr: float = 0.0008,
        stacked: bool = True,
        progress_callback=None,  # progress_callback will be a callable
        stock_closing_price_column_name: str = "closing_stock_data_GOOGL",
    ) -> None:


        logging.info("Creating and fitting LSTM model with %d epochs.", epochs)

        if lstm_units is None:
            lstm_units = [16]

        try:
            (
                X_tensorflow_train,
                y_tensorflow_train,
                scaler,
            ) = ModelStockData._csvDataCollection(
                csv_file, sequence_length, stock_closing_price_column_name
            )

            input_shape = (1, 1)
            if stacked is False:
                model = Sequential()
                model.add(LSTM(layers, activation="relu", input_shape=input_shape))
                model.add(Dense(1))
            else:
                model = Sequential()
                model.add(LSTM(1, activation="relu", input_shape=input_shape))
                model.add(Dense(1))

            custom_optimizer = Adamax(
                learning_rate=lr, weight_decay=0.001, epsilon=1e-08
            )
            model.compile(optimizer=custom_optimizer, loss="mean_squared_error")

            # Define a custom callback class to monitor progress
            class ProgressCallback(tf.keras.callbacks.Callback):
                def on_epoch_end(self, epoch, logs=None):
                    # Call the progress_callback function if provided
                    if progress_callback:
                        loss = logs.get('loss')  # Get the loss for the current epoch
                        progress_callback(epoch + 1, loss)  # Update progress

            # Pass the ProgressCallback instance to model.fit
            model.fit(
                X_tensorflow_train, 
                y_tensorflow_train, 
                epochs=epochs, 
                callbacks=[ProgressCallback()]
            )

            logging.info("Model fitting completed successfully.")

            predicted_prices = model.predict(X_tensorflow_train)

            # Inverse transform the scaled data to get the actual stock prices
            predicted_prices = scaler.inverse_transform(predicted_prices)
            mape_values = []

            for i in range(len(X_tensorflow_train)):
                mape = ModelStockData._mean_absolute_percentage_error(
                    y_tensorflow_train[i], predicted_prices[i]
                )
                mape_values.append(mape)

            min_mape_index = np.argmin(mape_values)
            logging.info("Lowest MAPE achieved at index %d.", min_mape_index)

            return predicted_prices[min_mape_index][0]

        except Exception as e:
            logging.error("Error in creating and fitting LSTM model: %s", str(e))
            raise

class DataAnalysis:
    """Class for performing data analysis on stock data."""

    @staticmethod
    def stock_analysis(
        csv_file: str, stock_closing_price_column_name: str = "closing_stock_data_SONY"
    ) -> None:
        """Performs a basic analysis of a stock price dataset.

        Args:
            csv_file (str): The path to the CSV file containing the stock price data.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.

        Returns:
            None
        """
        data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        fplt.plot(data, type="candle", title="Google", ylabel="Price ($)")

        fig = go.Figure(
            data=go.Scatter(
                x=data.index,
                y=data[stock_closing_price_column_name],
                mode="lines+markers",
            )
        )
        fig.show()

    def interactive_sticks(
        csv_file: str, stock_closing_price_column_name: str = "closing_stock_data_SONY"
    ):
        """Creates an interactive candlestick chart of a stock price dataset.

        Args:
            csv_file (str): The path to the CSV file containing the stock price data.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.

        Returns:
            None
        """
        data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(
            go.Candlestick(
                x=data.index,
                close=data[stock_closing_price_column_name],
            )
        )

    def interactive_bar(
        csv_file: str,
        stock_closing_price_column_name: str = "closing_stock_data_SONY",
        volume_column_name: str = "Volume",
        title_name: str = "data",
    ):
        """Creates an interactive bar chart of a stock price dataset with volume and 20-day moving average.

        Args:
            csv_file (str): The path to the CSV file containing the stock price data.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.
            volume_column_name (str): The name of the column in the CSV file containing
                the volume data.
            title_name (str): The title of the chart.

        Returns:
            None
        """
        data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(
            go.Bar(x=data.index, y=data[volume_column_name], name=volume_column_name),
            secondary_y=True,
        )
        fig3.update_layout(xaxis_rangeslider_visible=False)
        fig3.show()
        fig3.add_trace(
            go.Scatter(
                x=data.index,
                y=data[stock_closing_price_column_name].rolling(window=21).mean(),
                marker_color="blue",
                name="20 Day MA",
            )
        )
        fig3.add_trace(
            go.Bar(x=data.index, y=data[volume_column_name], name=volume_column_name),
            secondary_y=True,
        )
        fig3.update_layout(title={"text": title_name, "x": 0.5})
        fig3.update_yaxes(range=[0, 70000000], secondary_y=True)
        fig3.update_yaxes(visible=False, secondary_y=True)
        fig3.update_layout(xaxis_rangeslider_visible=False)  # hide range slider
        fig3.show()
